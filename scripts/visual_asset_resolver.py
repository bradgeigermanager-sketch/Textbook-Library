#!/usr/bin/env python3
"""Resolve discovered visual references to safe, local source assets.

This tool never fetches URLs, follows symlinks, executes renderers, or copies source
assets. It emits a catalog candidate and a resolution report.
"""
import argparse
import hashlib
import json
import mimetypes
import re
import struct
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote, urlsplit

VERSION = "0.1.0"
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".tif", ".tiff", ".pdf", ".eps"}
EMBEDDED_KINDS = {"tikz", "pstricks", "mermaid", "graphviz", "latex_figure"}
FORMAT_MIME = {
    ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".gif": "image/gif", ".webp": "image/webp", ".svg": "image/svg+xml",
    ".tif": "image/tiff", ".tiff": "image/tiff", ".pdf": "application/pdf",
    ".eps": "application/postscript",
}


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def dimensions(path, suffix):
    try:
        with path.open("rb") as f:
            head = f.read(32)
            if suffix == ".png" and head.startswith(b"\x89PNG\r\n\x1a\n"):
                return struct.unpack(">II", head[16:24])
            if suffix == ".gif" and head[:6] in (b"GIF87a", b"GIF89a"):
                return struct.unpack("<HH", head[6:10])
            if suffix in {".jpg", ".jpeg"}:
                f.seek(2)
                while True:
                    marker = f.read(1)
                    if not marker:
                        break
                    if marker != b"\xff":
                        continue
                    code = f.read(1)
                    while code == b"\xff":
                        code = f.read(1)
                    if code in (b"\xd8", b"\xd9") or not code:
                        continue
                    length_bytes = f.read(2)
                    if len(length_bytes) != 2:
                        break
                    length = int.from_bytes(length_bytes, "big")
                    if code[0] in {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}:
                        data = f.read(5)
                        if len(data) == 5:
                            height = int.from_bytes(data[1:3], "big")
                            width = int.from_bytes(data[3:5], "big")
                            return width, height
                        break
                    f.seek(length - 2, 1)
            if suffix == ".webp" and head[:4] == b"RIFF" and head[8:12] == b"WEBP":
                kind = head[12:16]
                if kind == b"VP8X" and len(head) >= 30:
                    width = 1 + int.from_bytes(head[24:27], "little")
                    height = 1 + int.from_bytes(head[27:30], "little")
                    return width, height
            if suffix == ".svg":
                f.seek(0)
                raw = f.read(2 * 1024 * 1024)
                if b"<!DOCTYPE" in raw.upper() or b"<!ENTITY" in raw.upper():
                    return None
                root = ET.fromstring(raw)
                width = parse_svg_length(root.attrib.get("width"))
                height = parse_svg_length(root.attrib.get("height"))
                if width and height:
                    return width, height
                viewbox = root.attrib.get("viewBox") or root.attrib.get("viewbox")
                if viewbox:
                    nums = re.split(r"[\s,]+", viewbox.strip())
                    if len(nums) == 4:
                        return int(float(nums[2])), int(float(nums[3]))
    except (OSError, ValueError, ET.ParseError, struct.error):
        return None
    return None


def parse_svg_length(value):
    if not value:
        return None
    match = re.fullmatch(r"\s*(\d+(?:\.\d+)?)(?:px)?\s*", value)
    return int(float(match.group(1))) if match else None


def safe_target(target):
    if not target:
        return None, "empty_target"
    decoded = unquote(target.strip())
    parts = urlsplit(decoded)
    if parts.scheme or parts.netloc or decoded.startswith("//"):
        return None, "external_or_nonlocal_reference"
    path_text = parts.path
    if not path_text:
        return None, "empty_path"
    path = Path(path_text)
    if path.is_absolute() or any(part == ".." for part in path.parts):
        return None, "unsafe_path"
    if "\\" in path_text:
        return None, "unsafe_path_separator"
    return path, None


def resolve(root, source_rel, target):
    relative, error = safe_target(target)
    if error:
        return None, error
    source_dir = (root / source_rel).parent
    candidate_lexical = source_dir / relative
    try:
        candidate_lexical.relative_to(root)
    except ValueError:
        return None, "path_escapes_source_root"
    current = root
    for part in candidate_lexical.relative_to(root).parts:
        current = current / part
        if current.is_symlink():
            return None, "unsafe_path"
    candidate = candidate_lexical.resolve(strict=False)
    try:
        candidate.relative_to(root)
    except ValueError:
        return None, "path_escapes_source_root"
    if candidate.exists() and candidate.is_file() and not candidate.is_symlink():
        return candidate, "resolved"
    if not candidate.suffix:
        for suffix in sorted(IMAGE_SUFFIXES):
            alternate = candidate.with_suffix(suffix)
            if alternate.exists() and alternate.is_file() and not alternate.is_symlink():
                return alternate, "resolved_extension_inferred"
    return None, "asset_not_found"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("source_root", type=Path)
    ap.add_argument("discovery_json", type=Path)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--report", type=Path)
    args = ap.parse_args()
    root = args.source_root.resolve(strict=True)
    discoveries = json.loads(args.discovery_json.read_text(encoding="utf-8"))
    records, report = [], []
    for item in discoveries:
        kind = item.get("reference_kind", "unknown")
        source_rel = item.get("source_path", "")
        source_lexical = root / source_rel
        try:
            source_lexical.relative_to(root)
        except ValueError:
            report.append({"visual_id": item.get("visual_id"), "status": "unsafe_source_path"})
            continue
        relative_parts = source_lexical.relative_to(root).parts
        current = root
        unsafe_source = False
        for part in relative_parts:
            current = current / part
            if current.is_symlink():
                unsafe_source = True
                break
        if unsafe_source:
            report.append({"visual_id": item.get("visual_id"), "status": "unsafe_source_path"})
            continue
        source_file = source_lexical.resolve(strict=False)
        try:
            source_file.relative_to(root)
        except ValueError:
            report.append({"visual_id": item.get("visual_id"), "status": "unsafe_source_path"})
            continue
        source_hash = digest(source_file) if source_file.is_file() else None
        target = item.get("target")
        embedded = kind in EMBEDDED_KINDS
        resolved_path, status = (None, "embedded_source_construct") if embedded else resolve(root, source_rel, target)
        asset_path = resolved_path.relative_to(root).as_posix() if resolved_path else None
        suffix = resolved_path.suffix.lower() if resolved_path else ""
        mime = FORMAT_MIME.get(suffix, mimetypes.guess_type(asset_path or "")[0] or ("text/x-" + kind if embedded else "application/octet-stream"))
        dims = dimensions(resolved_path, suffix) if resolved_path and suffix else None
        byte_size = resolved_path.stat().st_size if resolved_path else None
        asset_hash = digest(resolved_path) if resolved_path else None
        record = {
            "visual_id": item["visual_id"],
            "edition_id": item["edition_id"],
            "parent_node_id": None,
            "caption": None,
            "figure_number": None,
            "title": None,
            "visual_type": item.get("visual_type", "unknown"),
            "instructional_role": "unknown",
            "source": {
                "path": source_rel,
                "anchor": None,
                "page": None,
                "line_start": item.get("line"),
                "line_end": item.get("line"),
                "source_uri": None,
                "source_sha256": source_hash
            },
            "asset": {
                "media_type": mime,
                "format": suffix.lstrip(".") or kind,
                "width_px": dims[0] if dims else None,
                "height_px": dims[1] if dims else None,
                "vector": suffix in {".svg", ".pdf", ".eps"} or embedded,
                "embedded": embedded,
                "alt_text": None,
                "storage_path": asset_path,
                "rendered_preview_path": None
            },
            "labels": [],
            "generalized_form_ids": [],
            "related_visual_ids": [],
            "related_block_ids": [],
            "concept_ids": [],
            "citation_ids": [],
            "description": None,
            "accessibility": {
                "alt_text": None,
                "long_description": None,
                "reviewed_by_human": False,
                "ocr_status": "not_run"
            },
            "rendering": {
                "native_renderer": None,
                "fallback_renderer": None,
                "render_status": "source_only" if embedded else "unknown",
                "render_warnings": []
            },
            "review_status": "unreviewed",
            "resolution": {
                "status": status,
                "reference_kind": kind,
                "original_target": target,
                "resolved_path": asset_path,
                "sha256": asset_hash,
                "byte_size": byte_size,
                "resolver_version": VERSION,
                "warnings": item.get("warnings", [])
            }
        }
        records.append(record)
        report.append({"visual_id": item["visual_id"], "status": status, "resolved_path": asset_path, "sha256": asset_hash})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(records, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    report_path = args.report or args.output.with_name(args.output.stem + "-resolution-report.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    counts = {}
    for row in report:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    print(json.dumps({"records": len(records), "statuses": counts, "output": str(args.output), "report": str(report_path)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
