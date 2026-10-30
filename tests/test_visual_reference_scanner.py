import json, tempfile, unittest, sys
from pathlib import Path
from scripts.visual_reference_scanner import main
class VisualReferenceScannerTests(unittest.TestCase):
 def test_scans_markdown_and_latex(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp)
   (root/"chapter.md").write_text("# Topic\n\n![plot](figures/plot.svg)\n",encoding="utf-8")
   (root/"figure.tex").write_text(r"\includegraphics[width=0.8\textwidth]{figures/diagram.pdf}",encoding="utf-8")
   output=root/"out.json"; old=sys.argv
   try:
    sys.argv=["scanner",str(root),"--edition-id","edition-1","--output",str(output)]
    self.assertEqual(main(),0)
   finally: sys.argv=old
   kinds={x["reference_kind"] for x in json.loads(output.read_text(encoding="utf-8"))}
   self.assertIn("markdown_image",kinds); self.assertIn("latex_includegraphics",kinds)
if __name__=="__main__": unittest.main()
