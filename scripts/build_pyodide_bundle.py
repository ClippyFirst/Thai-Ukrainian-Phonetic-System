#!/usr/bin/env python3
"""Stage a same-origin Pyodide runtime bundle and write its auditable manifest."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import zipfile
from pathlib import Path, PurePosixPath
from email.parser import Parser


EXPECTED = {"fastthaig2p", "pythainlp", "thai-ukrainian-phonetic-system", "tzdata"}
PYODIDE_VERSION = "0.29.5"


def wheel_metadata(path: Path) -> tuple[str, str, str]:
    with zipfile.ZipFile(path) as archive:
        metadata_path = next(
            (name for name in archive.namelist() if name.endswith(".dist-info/METADATA")),
            None,
        )
        wheel_path = next(
            (name for name in archive.namelist() if name.endswith(".dist-info/WHEEL")),
            None,
        )
        if not metadata_path or not wheel_path:
            raise ValueError(f"Missing wheel metadata: {path.name}")
        metadata = Parser().parsestr(archive.read(metadata_path).decode("utf-8"))
        wheel_text = archive.read(wheel_path).decode("utf-8")
        if "Root-Is-Purelib: true" not in wheel_text or "Tag: py3-none-any" not in wheel_text and "Tag: py2.py3-none-any" not in wheel_text:
            raise ValueError(f"Non-pure wheel cannot be installed by this browser loader: {path.name}")
        return metadata["Name"].lower().replace("_", "-"), metadata["Version"], metadata.get("License-Expression") or metadata.get("License") or "UNSPECIFIED"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--purpose", choices=("ci", "pages"), required=True)
    parser.add_argument("--pyodide-dist", type=Path, required=True)
    parser.add_argument("--wheels", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--rights-manifest", type=Path, required=True)
    args = parser.parse_args()

    rights = json.loads(args.rights_manifest.read_text(encoding="utf-8"))
    if args.purpose == "pages" and rights.get("redistribution_approved") is not True:
        raise SystemExit("Refusing public Pages bundle: third-party redistribution is not approved in the rights manifest.")

    if not args.pyodide_dist.is_dir():
        raise SystemExit(f"Pyodide distribution directory not found: {args.pyodide_dist}")
    if not (args.pyodide_dist / "pyodide.mjs").is_file():
        raise SystemExit("Pyodide npm distribution is incomplete: pyodide.mjs missing")

    wheel_paths = sorted(args.wheels.glob("*.whl"))
    wheel_records = []
    for path in wheel_paths:
        package, version, license_name = wheel_metadata(path)
        wheel_records.append({
            "package": package,
            "version": version,
            "filename": path.name,
            "sha256": sha256(path),
            "size_bytes": path.stat().st_size,
            "license": license_name,
        })
    found = {item["package"] for item in wheel_records}
    if found != EXPECTED:
        raise SystemExit(f"Unexpected browser wheel set: expected {sorted(EXPECTED)}, found {sorted(found)}")

    pyodide_record = {
        "version": PYODIDE_VERSION,
        "license": "MPL-2.0",
        "source": "https://www.npmjs.com/package/pyodide",
    }
    if args.output.exists():
        shutil.rmtree(args.output)
    runtime_out = args.output / "pyodide"
    wheels_out = args.output / "wheels"
    shutil.copytree(args.pyodide_dist, runtime_out)
    wheels_out.mkdir(parents=True)
    for item in wheel_records:
        shutil.copy2(args.wheels / item["filename"], wheels_out / item["filename"])

    runtime_records = []
    for path in sorted(runtime_out.rglob("*")):
        if path.is_file():
            runtime_records.append({
                "path": path.relative_to(args.output).as_posix(),
                "sha256": sha256(path),
                "size_bytes": path.stat().st_size,
            })

    bundle_manifest = {
        "schema_version": 1,
        "purpose": "ephemeral-ci" if args.purpose == "ci" else "public-pages",
        "redistribution_approved": rights.get("redistribution_approved") is True,
        "pyodide": pyodide_record,
        "wheels": wheel_records,
        "runtime_files": runtime_records,
    }
    (args.output / "bundle-manifest.json").write_text(
        json.dumps(bundle_manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "purpose": bundle_manifest["purpose"],
        "wheel_count": len(wheel_records),
        "wheel_bytes": sum(item["size_bytes"] for item in wheel_records),
        "runtime_file_count": len(runtime_records),
        "runtime_bytes": sum(item["size_bytes"] for item in runtime_records),
        "redistribution_approved": bundle_manifest["redistribution_approved"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
