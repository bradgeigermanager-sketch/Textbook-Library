#!/usr/bin/env python3
"""Extract a conservative, non-executing MyST/Markdown chapter structure."""
from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path

VERSION = "0.1.0"
HEADING = re.compile(r"^(#{1,6})\\s+(.+?)\\s*#*\\s*$")
FENCE = re.compile(r"^\\s{0,3}(`{3,}|~{3,})(.*)$")
IMAGE = re.compile(r"!\\[([^]]*)\\]\\(([^)]+)\\)")
CITATION = re.compile(r"\\[@([^]]+)\\]")
MATH_DELIM = re.compile(r"^\\s*\\$\\$\\s*$")

def stable_id(*parts: str) -> str:
    return hashlib.sha256("::".join(parts).encode("utf-8")).hexdigest()[:24]

def read_toc(root: Path) -> list[dict] | None:
    toc = root / "_toc.yml"
    if not toc.exists():
        return None
    try:
        import yaml
    except ImportError:
        return None
    data = yaml.safe_load(toc.read_text(encoding="utf-8")) or {}
    result = []
    def walk(items, parent=None, order_prefix=""):
        for i, item in enumerate(items or []):
            if not isinstance(item, dict):
                continue
            file = item.get("file") or item.get("url")
            title = item.get("title") or (Path(file).name if file else "Untitled")
            entry = {"title": str(title), "file": str(file) if file else None,
                     "parent": parent, "order": order_prefix + str(i)}
            result.append(entry)
            children = item.get("sections") or item.get("chapters")
            if children:
                walk(children, str(file or title), entry["order"] + ".")
    walk(data.get("chapters") or data.get("parts") or [])
    return result

def discover_files(root: Path) -> list[Path]:
    excluded = {".git", "_build", "build", "dist", "node_modules", ".venv"}
    return sorted(p for p in root.rglob("*.md") if not any(x in excluded for x in p.relative_to(root).parts))

def parse_file(path: Path, root: Path, edition_id: str, node_order: int):
    rel = path.relative_to(root).as_posix()
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    nodes, blocks, stack = [], [], []
    current_node = None
    block_order = 0
    in_fence = False
    fence_mark = ""
    in_math = False
    paragraph = []

    def emit(kind, text, start, end, **extra):
        nonlocal block_order
        if current_node is None:
            return
        raw = "\\n".join(text)
        block_id = stable_id(edition_id, rel, str(start), str(block_order), kind)
        block = {"block_id": block_id, "parent_node_id": current_node["node_id"],
                 "block_type": kind, "order": block_order, "text": raw,
                 "raw_source": raw, "source": {"path": rel, "line_start": start,
                 "line_end": end, "page": None, "anchor": None,
                 "content_sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest()},
                 "extraction": {"method": "myst_markdown_heuristic", "parser_name": "myst_adapter",
                 "parser_version": VERSION, "confidence": 0.95 if kind == "heading" else 0.85,
                 "warnings": []}}
        block.update(extra)
        blocks.append(block)
        current_node["content_block_ids"].append(block_id)
        block_order += 1

    def flush(end):
        nonlocal paragraph
        if paragraph:
            txt = "\\n".join(paragraph)
            kind = "list" if re.match(r"^\\s*(?:[-*+] |\\d+[.)] )", txt) else "paragraph"
            emit(kind, paragraph, end-len(paragraph)+1, end)
            paragraph = []

    for n, line in enumerate(lines, 1):
        if in_fence:
            if re.match(r"^\\s{0,3}" + re.escape(fence_mark[0]) + "{" + str(len(fence_mark)) + r",}\\s*$", line):
                emit("code", code_lines, code_start, n, language=code_lang or None)
                in_fence = False
            else:
                code_lines.append(line)
            continue
        fm = FENCE.match(line)
        if fm:
            flush(n-1)
            in_fence, fence_mark = True, fm.group(1)
            code_lang = fm.group(2).strip().split()[0] if fm.group(2).strip() else ""
            code_lines, code_start = [], n+1
            continue
        if MATH_DELIM.match(line):
            flush(n-1)
            if in_math:
                emit("equation", math_lines, math_start, n, math_format="latex")
                in_math = False
            else:
                in_math, math_lines, math_start = True, [], n+1
            continue
        hm = HEADING.match(line)
        if hm:
            flush(n-1)
            level, title = len(hm.group(1)), hm.group(2)
            anchor = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
            while stack and stack[-1][0] >= level:
                stack.pop()
            parent = stack[-1][1] if stack else None
            node_id = stable_id(edition_id, rel, anchor, str(level))
            node = {"node_id": node_id, "edition_id": edition_id, "parent_node_id": parent,
                    "node_type": "chapter" if level == 1 else "section" if level <= 3 else "subsection",
                    "title": title, "order": len(nodes), "source_path": rel,
                    "source_anchor": anchor, "source_line_start": n, "source_line_end": None,
                    "children": [], "content_block_ids": []}
            if parent:
                for previous in nodes:
                    if previous["node_id"] == parent:
                        previous["children"].append(node_id)
                        break
            nodes.append(node)
            current_node = node
            stack.append((level, node_id))
            block_order = 0
            emit("heading", [title], n, n)
            continue
        if in_math:
            math_lines.append(line)
        elif not line.strip():
            flush(n-1)
        else:
            paragraph.append(line)
    flush(len(lines))
    if in_fence:
        emit("code", code_lines, code_start, len(lines), language=code_lang or None)
    if in_math:
        emit("equation", math_lines, math_start, len(lines), math_format="latex")
    for node in nodes:
        node["source_line_end"] = len(lines)
    return nodes, blocks

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("source_root", type=Path)
    ap.add_argument("--edition-id", required=True)
    ap.add_argument("--output-dir", type=Path, required=True)
    args = ap.parse_args()
    root = args.source_root.resolve(strict=True)
    files = discover_files(root)
    toc = read_toc(root)
    if toc:
        ordered = []
        for entry in toc:
            if entry["file"]:
                candidate = (root / entry["file"]).resolve()
                if candidate.is_relative_to(root) and candidate.is_file() and candidate.suffix.lower() == ".md":
                    ordered.append(candidate)
        files = list(dict.fromkeys(ordered + files))
    all_nodes, all_blocks, warnings = [], [], []
    for idx, path in enumerate(files):
        try:
            nodes, blocks = parse_file(path, root, args.edition_id, idx)
            all_nodes.extend(nodes); all_blocks.extend(blocks)
        except (OSError, UnicodeError) as exc:
            warnings.append(f"{path.relative_to(root)}: {exc}")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "chapter-nodes.json").write_text(json.dumps(all_nodes, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")
    (args.output_dir / "content-blocks.json").write_text(json.dumps(all_blocks, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")
    report = {"edition_id": args.edition_id, "parser": "myst_adapter", "parser_version": VERSION,
              "files_discovered": len(files), "nodes_extracted": len(all_nodes),
              "blocks_extracted": len(all_blocks), "warnings": warnings,
              "toc_used": bool(toc)}
    (args.output_dir / "ingestion-report.json").write_text(json.dumps(report, indent=2) + "\\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if not warnings else 2

if __name__ == "__main__":
    raise SystemExit(main())
