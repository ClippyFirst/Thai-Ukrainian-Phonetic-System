#!/usr/bin/env python3
"""Trim unused PyThaiNLP corpus assets from the browser runtime wheel.

The FastThaiG2P normalizer uses PyThaiNLP word tokenization for mai yamok.
The required bundled dictionary is words_th.txt (CC0-1.0); retain the corpus
license notice and Python source. Other corpus/model data are not used by this
runtime and are deliberately excluded from the Pages bundle.
"""
from __future__ import annotations

import base64
import csv
import hashlib
import io
import sys
import zipfile
from pathlib import Path, PurePosixPath


REQUIRED = {
    "pythainlp/corpus/words_th.txt",
    "pythainlp/corpus/corpus_license.md",
}


def keep_member(name: str) -> bool:
    if not name.startswith("pythainlp/corpus/"):
        return True
    return name.endswith(".py") or name in REQUIRED


def record_hash(data: bytes) -> str:
    digest = base64.urlsafe_b64encode(hashlib.sha256(data).digest()).rstrip(b"=").decode("ascii")
    return "sha256=" + digest


def slim_wheel(path: Path) -> tuple[int, int, list[tuple[str, int]]]:
    with zipfile.ZipFile(path, "r") as source:
        members = {
            info.filename: source.read(info.filename)
            for info in source.infolist()
            if not info.is_dir() and keep_member(info.filename)
        }
        all_members = {
            info.filename: info.file_size
            for info in source.infolist()
            if not info.is_dir()
        }

    missing = REQUIRED - members.keys()
    if missing:
        raise SystemExit(f"Required PyThaiNLP files are missing: {sorted(missing)}")

    metadata_name = next(
        (name for name in members if name.endswith(".dist-info/METADATA")),
        None,
    )
    record_name = next(
        (name for name in members if name.endswith(".dist-info/RECORD")),
        None,
    )
    wheel_name = next(
        (name for name in members if name.endswith(".dist-info/WHEEL")),
        None,
    )
    if not metadata_name or not record_name or not wheel_name:
        raise SystemExit("PyThaiNLP wheel metadata is incomplete")
    metadata = members[metadata_name].decode("utf-8", errors="replace")
    wheel_metadata = members[wheel_name].decode("utf-8", errors="replace")
    if "Name: pythainlp" not in metadata or "Version: 5.4.0" not in metadata:
        raise SystemExit("Unexpected PyThaiNLP package/version")
    if "Root-Is-Purelib: true" not in wheel_metadata or "Tag: py3-none-any" not in wheel_metadata:
        raise SystemExit("PyThaiNLP wheel is not a pure-Python universal wheel")

    output = io.StringIO(newline="")
    writer = csv.writer(output, lineterminator="\n")
    for name, data in sorted(members.items()):
        if name == record_name:
            continue
        writer.writerow((name, record_hash(data), str(len(data))))
    writer.writerow((record_name, "", ""))
    members[record_name] = output.getvalue().encode("utf-8")

    temporary = path.with_suffix(".slim.whl")
    with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as target:
        for name, data in sorted(members.items()):
            member = PurePosixPath(name)
            if member.is_absolute() or ".." in member.parts:
                raise SystemExit(f"Unsafe wheel path: {name}")
            target.writestr(name, data)
    before = sum(all_members.values())
    after = sum(len(data) for name, data in members.items())
    removed = sorted(
        ((name, size) for name, size in all_members.items() if name not in members),
        key=lambda item: item[1],
        reverse=True,
    )
    temporary.replace(path)
    return before, after, removed


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: slim_pythainlp_wheel.py PATH_TO_PYTHAINLP_WHEEL")
    wheel = Path(sys.argv[1])
    before, after, removed = slim_wheel(wheel)
    print(f"PyThaiNLP source member bytes: {before:,}")
    print(f"PyThaiNLP slim member bytes:   {after:,}")
    print(f"Removed {len(removed)} unused corpus assets ({before - after:,} bytes)")
    for name, size in removed[:20]:
        print(f"  {size:>12,}  {name}")
