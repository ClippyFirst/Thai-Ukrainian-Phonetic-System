#!/usr/bin/env python3
"""Build a reproducible static import/entry-point graph and test-overlap inventory.

This is a static dependency audit, not a complete runtime call graph. Dynamic imports,
reflection, plugin loading and runtime-generated paths are reported as review sites.
"""
from __future__ import annotations

import argparse
import ast
import difflib
import hashlib
import json
import re
from collections import defaultdict
from html.parser import HTMLParser
from importlib.util import resolve_name
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PYTHON_ROOTS = ("src", "scripts", "tests")
JS_IMPORT = re.compile(
    r"(?:\bimport\s+(?:[^'\";]*?\s+from\s+)?|\bexport\s+[^'\";]*?\s+from\s*)['\"]([^'\"]+)['\"]"
)
WORKFLOW_COMMAND = re.compile(
    r"(?<![\w/])(?:python(?:3(?:\.\d+)?)?|node)\s+((?:scripts|tests|web/tests)/[A-Za-z0-9_./-]+)"
)
DYNAMIC_JS = re.compile(r"\b(?:import\s*\(|require\s*\()")
DYNAMIC_PYTHON_NAMES = {"__import__", "import_module", "spec_from_file_location"}


def _python_module(path: Path, root: Path = ROOT) -> str | None:
    relative = path.relative_to(root).as_posix()
    if not relative.endswith(".py"):
        return None
    if relative.startswith("src/"):
        name = relative[4:-3].replace("/", ".")
        return name[:-9] if name.endswith(".__init__") else name
    if relative.startswith("scripts/"):
        return relative[:-3].replace("/", ".")
    if relative.startswith("tests/"):
        return relative[:-3].replace("/", ".")
    return None


def _python_files(root: Path) -> list[Path]:
    return sorted(
        path for folder in PYTHON_ROOTS
        for path in (root / folder).rglob("*.py")
        if path.is_file()
    )


def _resolve_python_import(
    module: str, node: ast.AST, known: set[str], *, is_package: bool = False
) -> set[str]:
    targets: set[str] = set()
    if isinstance(node, ast.Import):
        for alias in node.names:
            if alias.name in known:
                targets.add(alias.name)
        return targets

    if not isinstance(node, ast.ImportFrom):
        return targets

    if node.level:
        package = module if is_package else module.rpartition(".")[0]
        if not package:
            return targets
        relative = "." * node.level + (node.module or "")
        try:
            base = resolve_name(relative, package)
        except (ImportError, ValueError):
            return targets
    else:
        base = node.module or ""

    if base in known:
        targets.add(base)
    for alias in node.names:
        candidate = f"{base}.{alias.name}" if base else alias.name
        if candidate in known:
            targets.add(candidate)
    return targets


def _html_assets(path: Path) -> list[dict[str, str]]:
    class Assets(HTMLParser):
        def __init__(self) -> None:
            super().__init__()
            self.items: list[dict[str, str]] = []

        def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
            values = dict(attrs)
            if tag == "script" and values.get("src"):
                self.items.append({"kind": "script", "target": str(values["src"])})
            elif tag == "link" and values.get("href"):
                rel = (values.get("rel") or "").lower()
                if "stylesheet" in rel:
                    self.items.append({"kind": "stylesheet", "target": str(values["href"])})

    parser = Assets()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser.items


def _resolve_js_import(source: Path, specifier: str, known: set[str]) -> str | None:
    if not specifier.startswith("."):
        return None
    candidate = (source.parent / specifier).as_posix()
    options = [candidate, candidate + ".js", candidate + "/index.js"]
    return next((item for item in options if item in known), None)


def _test_inventory(path: Path, tree: ast.AST, root: Path = ROOT) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_"):
            rows.append({
                "file": path.relative_to(root).as_posix(),
                "name": node.name,
                "line": node.lineno,
                "assert_statements": sum(isinstance(child, ast.Assert) for child in ast.walk(node)),
                "body_sha256": hashlib.sha256(
                    ast.dump(ast.Module(body=node.body, type_ignores=[]), include_attributes=False).encode("utf-8")
                ).hexdigest(),
            })
    return rows


def build_report(root: Path = ROOT, revision: str | None = None) -> dict[str, Any]:
    root = root.resolve()
    py_paths = sorted(
        path for folder in PYTHON_ROOTS
        for path in (root / folder).rglob("*.py")
        if path.is_file()
    )
    py_modules = {
        _python_module(path, root): path for path in py_paths if _python_module(path, root)
    }
    known_py = set(py_modules)
    py_edges: set[tuple[str, str]] = set()
    parse_errors: list[dict[str, str]] = []
    dynamic_sites: list[dict[str, Any]] = []
    test_inventory: list[dict[str, Any]] = []
    test_imports: dict[str, set[str]] = defaultdict(set)

    for module, path in py_modules.items():
        try:
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(path))
        except (OSError, UnicodeError, SyntaxError) as error:
            parse_errors.append({"file": path.relative_to(root).as_posix(), "error": str(error)})
            continue

        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                for target in _resolve_python_import(
                    module, node, known_py, is_package=path.name == "__init__.py"
                ):
                    if target != module:
                        py_edges.add((module, target))
                        if module.startswith("tests."):
                            test_imports[module].add(target)
            elif isinstance(node, ast.Call):
                func = node.func
                name = func.id if isinstance(func, ast.Name) else (
                    func.attr if isinstance(func, ast.Attribute) else ""
                )
                if name in DYNAMIC_PYTHON_NAMES:
                    dynamic_sites.append({
                        "file": path.relative_to(root).as_posix(),
                        "line": node.lineno,
                        "kind": "python-dynamic-import",
                        "expression": name,
                    })

        if path.relative_to(root).as_posix().startswith("tests/"):
            test_inventory.extend(_test_inventory(path, tree, root))

    js_paths = sorted((root / "web" / "src").glob("*.js"))
    js_test_paths = sorted((root / "web" / "tests").glob("*.mjs"))
    all_js_paths = js_paths + js_test_paths
    known_js = {path.relative_to(root).as_posix() for path in all_js_paths}
    js_edges: set[tuple[str, str]] = set()
    browser_test_inventory: list[dict[str, Any]] = []
    for path in all_js_paths:
        relative = path.relative_to(root).as_posix()
        source = path.read_text(encoding="utf-8")
        for match in JS_IMPORT.finditer(source):
            target = _resolve_js_import(Path(relative), match.group(1), known_js)
            if target:
                js_edges.add((relative, target))
        if path in js_test_paths:
            browser_test_inventory.append({
                "file": relative,
                "assertion_calls": len(re.findall(
                    r"\bassert(?:\.(?:equal|deepEqual|match|doesNotMatch|ok|throws|rejects|strictEqual|notEqual))?\s*\(",
                    source,
                )),
                "imports_local_modules": sorted(
                    target for edge_source, target in js_edges if edge_source == relative
                ),
                "suite_style": "TOP_LEVEL_ASSERTION_SCRIPT",
            })
        for match in DYNAMIC_JS.finditer(source):
            dynamic_sites.append({
                "file": relative,
                "line": source.count("\n", 0, match.start()) + 1,
                "kind": "javascript-dynamic-import-or-require",
                "expression": match.group(0),
            })

    html_edges: list[dict[str, str]] = []
    for path in sorted((root / "web").glob("*.html")):
        relative = path.relative_to(root).as_posix()
        for item in _html_assets(path):
            html_edges.append({"source": relative, **item})

    workflow_refs: list[dict[str, str]] = []
    workflows = root / ".github" / "workflows"
    if workflows.exists():
        for path in sorted(workflows.glob("*.yml")) + sorted(workflows.glob("*.yaml")):
            text = path.read_text(encoding="utf-8")
            for match in WORKFLOW_COMMAND.finditer(text):
                workflow_refs.append({
                    "workflow": path.relative_to(root).as_posix(),
                    "target": match.group(1),
                })

    by_name: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in test_inventory:
        by_name[item["name"]].append(item)
    exact_name_clusters = [
        {"test_name": name, "instances": rows}
        for name, rows in sorted(by_name.items()) if len(rows) > 1
    ]
    by_body: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in test_inventory:
        by_body[item["body_sha256"]].append(item)
    exact_body_clusters = [
        {"body_sha256": digest, "instances": rows}
        for digest, rows in sorted(by_body.items()) if len(rows) > 1
    ]
    near_name_candidates: list[dict[str, Any]] = []
    names = sorted(by_name)
    for index, left in enumerate(names):
        for right in names[index + 1:]:
            ratio = difflib.SequenceMatcher(None, left, right).ratio()
            if ratio >= 0.92:
                near_name_candidates.append({"left": left, "right": right, "similarity": round(ratio, 3)})

    files_for_hash = sorted(set(py_paths + all_js_paths))
    hashes = {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in files_for_hash
    }
    return {
        "schema_version": "1.0",
        "revision": revision,
        "analysis_kind": "STATIC_IMPORT_AND_ENTRYPOINT_GRAPH_NOT_COMPLETE_RUNTIME_CALL_GRAPH",
        "summary": {
            "python_modules": len(py_modules),
            "python_import_edges": len(py_edges),
            "browser_modules": len(js_paths),
            "browser_test_files": len(js_test_paths),
            "browser_test_assertion_calls": sum(item["assertion_calls"] for item in browser_test_inventory),
            "browser_import_edges_including_test_dependencies": len(js_edges),
            "html_asset_edges": len(html_edges),
            "workflow_script_references": len(workflow_refs),
            "test_functions": len(test_inventory),
            "exact_duplicate_test_name_clusters": len(exact_name_clusters),
            "exact_duplicate_test_body_clusters": len(exact_body_clusters),
            "near_duplicate_name_candidates": len(near_name_candidates),
            "dynamic_import_sites": len(dynamic_sites),
            "parse_errors": len(parse_errors),
        },
        "python_import_edges": [
            {"source": source, "target": target}
            for source, target in sorted(py_edges)
        ],
        "browser_import_edges": [
            {"source": source, "target": target}
            for source, target in sorted(js_edges)
        ],
        "browser_test_inventory": browser_test_inventory,
        "html_asset_edges": html_edges,
        "workflow_script_references": workflow_refs,
        "test_inventory": test_inventory,
        "test_module_imports": {
            module: sorted(imports) for module, imports in sorted(test_imports.items())
        },
        "test_overlap_review_candidates": {
            "exact_duplicate_names": exact_name_clusters,
            "exact_duplicate_bodies_manual_review_only": exact_body_clusters,
            "similar_names_only_not_proof_of_redundancy": near_name_candidates,
        },
        "dynamic_import_review_sites": dynamic_sites,
        "parse_errors": parse_errors,
        "source_sha256": hashes,
        "limitations": [
            "Static imports do not reveal every call edge, reflection target, runtime plugin, or generated import.",
            "A test-name match or similarity is only a manual-review candidate; it is never grounds for deleting a test.",
            "Python test-to-module edges reflect imports, not complete behavioral coverage.",
            "The report must be reviewed alongside workflow commands, package entry points and generated-data consumers.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Write JSON report to this path; stdout if omitted")
    parser.add_argument("--revision", default=None, help="Repository revision represented by this checkout")
    args = parser.parse_args()
    report = build_report(revision=args.revision)
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 1 if report["parse_errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
