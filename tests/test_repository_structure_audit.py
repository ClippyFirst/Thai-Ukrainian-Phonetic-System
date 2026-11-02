from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from audit_repository_structure import build_report, _python_module, _resolve_python_import
import ast


class RepositoryStructureAuditTests(unittest.TestCase):
    def test_package_initializer_and_relative_import_resolution(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            package = root / "src" / "sample"
            package.mkdir(parents=True)
            init = package / "__init__.py"
            init.write_text("from .alpha import run\n", encoding="utf-8")
            alpha = package / "alpha.py"
            alpha.write_text("from . import beta\n", encoding="utf-8")
            beta = package / "beta.py"
            beta.write_text("VALUE = 1\n", encoding="utf-8")

            self.assertEqual(_python_module(init, root), "sample")
            self.assertEqual(_python_module(alpha, root), "sample.alpha")
            known = {"sample", "sample.alpha", "sample.beta"}
            init_tree = ast.parse(init.read_text(encoding="utf-8"))
            alpha_tree = ast.parse(alpha.read_text(encoding="utf-8"))
            self.assertEqual(
                _resolve_python_import("sample", init_tree.body[0], known, is_package=True),
                {"sample.alpha"},
            )
            self.assertEqual(
                _resolve_python_import("sample.alpha", alpha_tree.body[0], known),
                {"sample", "sample.beta"},
            )

    def test_report_builds_python_browser_html_and_workflow_edges(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "src" / "sample").mkdir(parents=True)
            (root / "scripts").mkdir()
            (root / "tests").mkdir()
            (root / "web" / "src").mkdir(parents=True)
            (root / "web" / "tests").mkdir()
            (root / ".github" / "workflows").mkdir(parents=True)

            (root / "src" / "sample" / "__init__.py").write_text(
                "from .alpha import run\n", encoding="utf-8"
            )
            (root / "src" / "sample" / "alpha.py").write_text(
                "from . import beta\ndef run(): return beta.VALUE\n", encoding="utf-8"
            )
            (root / "src" / "sample" / "beta.py").write_text(
                "VALUE = 1\n", encoding="utf-8"
            )
            (root / "scripts" / "check.py").write_text("print('ok')\n", encoding="utf-8")
            (root / "tests" / "test_alpha.py").write_text(
                "from sample import alpha\ndef test_shared_name():\n    assert alpha.run() == 1\n",
                encoding="utf-8",
            )
            (root / "tests" / "test_beta.py").write_text(
                "from sample import beta\ndef test_shared_name():\n    assert beta.VALUE == 1\n",
                encoding="utf-8",
            )
            (root / "web" / "src" / "main.js").write_text(
                "import { value } from './util.js';\nexport { value };\n", encoding="utf-8"
            )
            (root / "web" / "src" / "util.js").write_text(
                "export const value = 1;\n", encoding="utf-8"
            )
            (root / "web" / "index.html").write_text(
                '<html><head><link rel="stylesheet" href="style.css"></head>'
                '<body><script type="module" src="src/main.js"></script></body></html>',
                encoding="utf-8",
            )
            (root / ".github" / "workflows" / "ci.yml").write_text(
                "steps:\n  - run: python scripts/check.py\n", encoding="utf-8"
            )

            report = build_report(root, revision="fixture")
            self.assertEqual(report["revision"], "fixture")
            self.assertIn(
                {"source": "sample.alpha", "target": "sample.beta"},
                report["python_import_edges"],
            )
            self.assertIn(
                {"source": "web/src/main.js", "target": "web/src/util.js"},
                report["browser_import_edges"],
            )
            self.assertIn(
                {"source": "web/index.html", "kind": "script", "target": "src/main.js"},
                report["html_asset_edges"],
            )
            self.assertIn(
                {"workflow": ".github/workflows/ci.yml", "target": "scripts/check.py"},
                report["workflow_script_references"],
            )
            self.assertEqual(report["summary"]["test_functions"], 2)
            self.assertEqual(report["summary"]["exact_duplicate_test_name_clusters"], 1)
            self.assertEqual(report["parse_errors"], [])

    def test_test_name_overlap_is_only_a_review_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "tests").mkdir()
            (root / "tests" / "test_one.py").write_text(
                "def test_same_contract():\n    assert True\n", encoding="utf-8"
            )
            (root / "tests" / "test_two.py").write_text(
                "def test_same_contract():\n    assert True\n", encoding="utf-8"
            )
            report = build_report(root)
            candidates = report["test_overlap_review_candidates"]["exact_duplicate_names"]
            self.assertEqual(candidates[0]["test_name"], "test_same_contract")
            self.assertIn("not grounds for deleting a test", " ".join(report["limitations"]))


if __name__ == "__main__":
    unittest.main()
