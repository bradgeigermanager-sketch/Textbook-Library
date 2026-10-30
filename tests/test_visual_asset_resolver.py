import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "visual_asset_resolver.py"


class VisualAssetResolverTests(unittest.TestCase):
    def run_resolver(self, root, discoveries):
        discovery = root / "discovery.json"
        output = root / "catalog.json"
        discovery.write_text(json.dumps(discoveries), encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), str(root), str(discovery), "--output", str(output)],
            capture_output=True, text=True, check=True
        )
        return json.loads(output.read_text(encoding="utf-8")), json.loads(
            output.with_name("catalog-resolution-report.json").read_text(encoding="utf-8")
        )

    def test_resolves_png_and_hashes_bytes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "figures").mkdir()
            (root / "chapter.md").write_text("![x](figures/pixel.png)", encoding="utf-8")
            png = bytes.fromhex("89504e470d0a1a0a0000000d4948445200000002000000030806000000")
            (root / "figures" / "pixel.png").write_bytes(png)
            records, report = self.run_resolver(root, [{
                "visual_id": "v1", "edition_id": "e1", "reference_kind": "markdown_image",
                "visual_type": "illustration", "target": "figures/pixel.png",
                "source_path": "chapter.md", "line": 1, "warnings": []
            }])
            self.assertEqual(report[0]["status"], "resolved")
            self.assertEqual(records[0]["asset"]["media_type"], "image/png")
            self.assertEqual(records[0]["asset"]["width_px"], 2)
            self.assertEqual(records[0]["asset"]["height_px"], 3)
            self.assertEqual(len(records[0]["resolution"]["sha256"]), 64)

    def test_rejects_parent_traversal(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "chapter.md").write_text("x", encoding="utf-8")
            records, report = self.run_resolver(root, [{
                "visual_id": "v2", "edition_id": "e1", "reference_kind": "markdown_image",
                "visual_type": "illustration", "target": "../../secret.png",
                "source_path": "chapter.md", "line": 1, "warnings": []
            }])
            self.assertEqual(report[0]["status"], "unsafe_path")
            self.assertIsNone(records[0]["asset"]["storage_path"])

    def test_external_url_is_not_fetched(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "chapter.md").write_text("x", encoding="utf-8")
            _, report = self.run_resolver(root, [{
                "visual_id": "v3", "edition_id": "e1", "reference_kind": "markdown_image",
                "visual_type": "illustration", "target": "https://example.org/a.png",
                "source_path": "chapter.md", "line": 1, "warnings": []
            }])
            self.assertEqual(report[0]["status"], "external_or_nonlocal_reference")

    def test_embedded_construct_is_preserved_as_source_only(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "chapter.tex").write_text(r"\begin{tikzpicture}...\end{tikzpicture}", encoding="utf-8")
            records, report = self.run_resolver(root, [{
                "visual_id": "v4", "edition_id": "e1", "reference_kind": "tikz",
                "visual_type": "diagram", "target": "tikzpicture",
                "source_path": "chapter.tex", "line": 1, "warnings": []
            }])
            self.assertTrue(records[0]["asset"]["embedded"])
            self.assertEqual(report[0]["status"], "embedded_source_construct")
            self.assertEqual(records[0]["rendering"]["render_status"], "source_only")


if __name__ == "__main__":
    unittest.main()
