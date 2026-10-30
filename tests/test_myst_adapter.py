import tempfile, unittest
from pathlib import Path
from scripts.myst_adapter import parse_file

class MystAdapterTests(unittest.TestCase):
    def test_heading_code_and_equation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "chapter.md"
            source.write_text("# Motion\\n\\nA paragraph.\\n\\n```python\\nprint(1)\\n```\\n\\n$$\\nx^2\\n$$\\n", encoding="utf-8")
            nodes, blocks = parse_file(source, root, "edition-1", 0)
            self.assertEqual(nodes[0]["title"], "Motion")
            self.assertIn("code", [b["block_type"] for b in blocks])
            self.assertIn("equation", [b["block_type"] for b in blocks])

if __name__ == "__main__":
    unittest.main()
