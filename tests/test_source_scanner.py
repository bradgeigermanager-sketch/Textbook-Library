import hashlib, tempfile, unittest
from pathlib import Path
from scripts.source_scanner import scan

class ScannerTests(unittest.TestCase):
    def test_hash_and_relative_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "chapter.md").write_text("# Intro", encoding="utf-8")
            item = scan(root)[0]
            self.assertEqual(item["path"], "chapter.md")
            self.assertEqual(item["sha256"], hashlib.sha256(b"# Intro").hexdigest())
            self.assertEqual(item["detected_format"], "markdown")

    def test_excludes_build_and_git(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for folder in (".git", "_build", "chapters"):
                (root / folder).mkdir()
                (root / folder / "file.txt").write_text("x", encoding="utf-8")
            paths = {x["path"] for x in scan(root)}
            self.assertEqual(paths, {"chapters/file.txt"})

if __name__ == "__main__":
    unittest.main()
