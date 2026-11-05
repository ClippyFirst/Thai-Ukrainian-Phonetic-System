#!/usr/bin/env python3
"""Stage a same-origin Pyodide runtime bundle and write its auditable manifest."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import zipfile
from pathlib import Path
from email.parser import Parser


EXPECTED = {"fastthaig2p", "pythainlp", "thai-ukrainian-phonetic-system", "tzdata"}
EXPECTED_VERSIONS = {
    "fastthaig2p": "0.1.0",
    "pythainlp": "5.4.0",
    "thai-ukrainian-phonetic-system": "0.6.1",
    "tzdata": "2026.6",
}
PYODIDE_VERSION = "0.29.5"
REQUIRED_NOTICES = {
    "licenses/Apache-2.0-FastThaiG2P.txt",
    "licenses/NOTICE-FastThaiG2P.txt",
    "licenses/Apache-2.0-PyThaiNLP.txt",
    "licenses/PyThaiNLP-corpus-license.md",
    "licenses/MPL-2.0-Pyodide.txt",
    "licenses/Apache-2.0-tzdata.txt",
    "licenses/BSD-3-Clause-TLTK.txt",
    "licenses/LGPL-3.0-TLTK-repository-license.txt",
    "licenses/CC-BY-SA-4.0.txt",
    "licenses/MIT-Project.txt",
}


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
    parser.add_argument("--notices-dir", type=Path, required=True)
    args = parser.parse_args()

    rights = json.loads(args.rights_manifest.read_text(encoding="utf-8"))
    if args.purpose == "pages" and rights.get("redistribution_approved") is not True:
        raise SystemExit("Refusing public Pages bundle: third-party redistribution is not approved in the rights manifest.")

    if not args.notices_dir.is_dir():
        raise SystemExit(f"Third-party notices directory not found: {args.notices_dir}")
    notice_paths = sorted(path for path in args.notices_dir.rglob("*") if path.is_file())
    if not notice_paths:
        raise SystemExit("No third-party license/NOTICE files were supplied")
    notice_names = {path.relative_to(args.notices_dir.parent).as_posix() for path in notice_paths}
    missing_notice_names = REQUIRED_NOTICES - notice_names
    if missing_notice_names:
        raise SystemExit(f"Required third-party notices are missing: {sorted(missing_notice_names)}")

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
    fastthaig2p_wheel = next(path for path in wheel_paths if wheel_metadata(path)[0] == "fastthaig2p")
    with zipfile.ZipFile(fastthaig2p_wheel) as archive:
        required_data_notices = {
            "fastthaig2p/data/browser-data-provenance.json",
            "fastthaig2p/data/WIKTIONARY-ATTRIBUTION.md",
        }
        missing_notices = required_data_notices - set(archive.namelist())
        if missing_notices:
            raise SystemExit(f"FastThaiG2P wheel is missing embedded data attribution: {sorted(missing_notices)}")

    for item in wheel_records:
        expected_version = EXPECTED_VERSIONS[item["package"]]
        if item["version"] != expected_version:
            raise SystemExit(
                f"Unexpected {item['package']} version: expected {expected_version}, found {item['version']}"
            )

    dataset_out = args.output / "datasets"
    dataset_out.mkdir(parents=True)
    dataset_path = dataset_out / "fastthaig2p-wiktionary-derived.zip"
    with zipfile.ZipFile(fastthaig2p_wheel) as wheel_archive, zipfile.ZipFile(dataset_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as dataset_archive:
        dataset_members = {
            "fastthaig2p/data/dict.txt": "dict.txt",
            "fastthaig2p/data/ipa.json": "ipa.json",
            "fastthaig2p/data/browser-data-provenance.json": "browser-data-provenance.json",
            "fastthaig2p/data/WIKTIONARY-ATTRIBUTION.md": "WIKTIONARY-ATTRIBUTION.md",
        }
        for source_name, archive_name in dataset_members.items():
            dataset_archive.writestr(archive_name, wheel_archive.read(source_name))
        dataset_archive.write(args.notices_dir / "CC-BY-SA-4.0.txt", "CC-BY-SA-4.0.txt")

    dataset_records = [{
        "path": dataset_path.relative_to(args.output).as_posix(),
        "sha256": sha256(dataset_path),
        "size_bytes": dataset_path.stat().st_size,
        "license": "CC-BY-SA-4.0",
        "attribution": ["Wiktionary contributors", "Kaikki.org / Wiktextract"],
    }]

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

    notice_records = [{
        "path": path.relative_to(args.notices_dir.parent).as_posix(),
        "sha256": sha256(path),
        "size_bytes": path.stat().st_size,
    } for path in notice_paths]

    bundle_manifest = {
        "schema_version": 1,
        "purpose": "ephemeral-ci" if args.purpose == "ci" else "public-pages",
        "redistribution_approved": rights.get("redistribution_approved") is True,
        "pyodide": pyodide_record,
        "wheels": wheel_records,
        "runtime_files": runtime_records,
        "notices": notice_records,\n        "datasets": dataset_records,
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
        "notice_count": len(notice_records),
        "notice_bytes": sum(item["size_bytes"] for item in notice_records),\n        "dataset_count": len(dataset_records),\n        "dataset_bytes": sum(item["size_bytes"] for item in dataset_records),
        "redistribution_approved": bundle_manifest["redistribution_approved"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
