#!/usr/bin/env python3
"""Create a non-executing, hash-based manifest for a local textbook source tree."""
from __future__ import annotations
import argparse, hashlib, json, mimetypes, os
from datetime import datetime, timezone
from pathlib import Path

VERSION = "0.1.0"
EXCLUDED_DIRS = {".git", ".hg", ".svn", ".venv", "venv", "__pycache__", ".ipynb_checkpoints", "node_modules", "_build", "build", "dist", ".tox"}
FORMAT_BY_SUFFIX = {
    ".md": "markdown", ".mdx": "markdown", ".ipynb": "jupyter_notebook",
    ".rmd": "rmarkdown", ".tex": "latex", ".bib": "bibtex", ".pdf": "pdf",
    ".html": "html", ".htm": "html", ".epub": "epub", ".adoc": "asciidoc",
    ".xml": "xml", ".yml": "yaml", ".yaml": "yaml", ".csv": "csv",
    ".json": "json", ".py": "python", ".r": "r"
}

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def scan(root: Path) -> list[dict]:
    artifacts = []
    for current, dirs, filenames in os.walk(root, followlinks=False):
        base = Path(current)
        dirs[:] = sorted(d for d in dirs if d not in EXCLUDED_DIRS and not (base / d).is_symlink())
        for filename in sorted(filenames):
            path = base / filename
            if path.is_symlink() or not path.is_file():
                continue
            rel = path.relative_to(root).as_posix()
            suffix = path.suffix.lower()
            media_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
            artifacts.append({
                "path": rel,
                "sha256": sha256_file(path),
                "byte_size": path.stat().st_size,
                "media_type": media_type,
                "detected_format": FORMAT_BY_SUFFIX.get(suffix),
                "included": True
            })
    return artifacts

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_root", type=Path)
    parser.add_argument("--resource-id", required=True)
    parser.add_argument("--source-uri", required=True)
    parser.add_argument("--source-kind", choices=["git_repository","archive","publisher","oer_platform","local_upload","other"], default="local_upload")
    parser.add_argument("--revision", default=None, help="Prefer a full immutable commit or archive digest.")
    parser.add_argument("--branch-or-tag", default=None)
    parser.add_argument("--output", type=Path, default=Path("source-manifest.json"))
    args = parser.parse_args()
    root = args.source_root.resolve(strict=True)
    if not root.is_dir():
        parser.error("source_root must be a directory")
    artifacts = scan(root)
    digest_input = "".join(a["path"] + ":" + a["sha256"] + "\\n" for a in artifacts)
    tree_digest = hashlib.sha256(digest_input.encode("utf-8")).hexdigest()
    revision_key = args.revision or tree_digest[:16]
    manifest = {
        "manifest_id": f"{args.resource_id}-{revision_key}",
        "resource_id": args.resource_id,
        "edition_id": None,
        "source_uri": args.source_uri,
        "source_kind": args.source_kind,
        "retrieved_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00","Z"),
        "revision": args.revision,
        "branch_or_tag": args.branch_or_tag,
        "scanner_version": VERSION,
        "tree_sha256": tree_digest,
        "artifacts": artifacts
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")
    print(f"Manifest: {args.output}")
    print(f"Files: {len(artifacts)}")
    print(f"Tree SHA-256: {tree_digest}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
