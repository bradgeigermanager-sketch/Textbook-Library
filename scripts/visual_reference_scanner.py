#!/usr/bin/env python3
"""Find non-equation visual references in Markdown, HTML, and LaTeX."""
import argparse, hashlib, json, re
from pathlib import Path
VERSION = "0.1.0"
PATTERNS = [
 ("markdown_image", re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")),
 ("html_image", re.compile(r"<img\b[^>]*?\bsrc=[\"']([^\"']+)[\"'][^>]*>", re.I)),
 ("latex_includegraphics", re.compile(r"\\includegraphics(?:\[[^\]]*\])?\s*\{([^}]+)\}")),
 ("latex_figure", re.compile(r"\\begin\s*\{(figure\*?)\}")),
 ("tikz", re.compile(r"\\begin\s*\{(tikzpicture|pgfpicture)\}")),
 ("pstricks", re.compile(r"\\begin\s*\{(pspicture\*?)\}")),
 ("mermaid", re.compile(r"^\s*\`\`\`mermaid\s*$", re.M)),
 ("graphviz", re.compile(r"^\s*\`\`\`(?:dot|graphviz)\s*$", re.M)),
]
SUFFIXES = {".md", ".mdx", ".tex", ".html", ".htm", ".rst"}
def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument("source_root",type=Path); ap.add_argument("--edition-id",required=True); ap.add_argument("--output",type=Path,required=True)
 a=ap.parse_args(); root=a.source_root.resolve(strict=True); results=[]
 for p in sorted(x for x in root.rglob("*") if x.is_file() and x.suffix.lower() in SUFFIXES and not x.is_symlink()):
  if any(x in {".git","_build","build","dist","node_modules",".venv"} for x in p.relative_to(root).parts): continue
  src=p.read_text(encoding="utf-8",errors="replace"); rel=p.relative_to(root).as_posix()
  for kind,pat in PATTERNS:
   for m in pat.finditer(src):
    line=src.count("\n",0,m.start())+1; groups=[g for g in m.groups() if g is not None]; target=groups[-1] if groups else None
    vid=hashlib.sha256(f"{a.edition_id}|{rel}|{line}|{kind}|{m.group(0)}".encode()).hexdigest()[:24]
    results.append({"visual_id":vid,"edition_id":a.edition_id,"visual_type":"diagram" if kind in {"tikz","pstricks","mermaid","graphviz"} else "illustration" if kind in {"markdown_image","html_image","latex_includegraphics"} else "unknown","reference_kind":kind,"target":target,"source_path":rel,"line":line,"raw_reference":m.group(0),"resolution_status":"unresolved","extraction_method":"source_pattern_scan","parser_version":VERSION,"warnings":["Discovery only; target and meaning require validation."]})
 a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(results,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
 print(f"Visual references: {len(results)}"); print(f"Output: {a.output}"); return 0
if __name__=="__main__": raise SystemExit(main())
