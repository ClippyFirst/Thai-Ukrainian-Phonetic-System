"""Registry-backed provenance gates for source data and human reviewers."""
from __future__ import annotations

import csv
from datetime import date
from pathlib import Path
from typing import Mapping
from urllib.parse import urlparse

SOURCE_FIELDS = ("source_id", "source_url", "license", "allowed_uses", "verification_status", "verified_by", "verified_at", "notes")
REVIEWER_FIELDS = ("reviewer_id", "language", "roles", "qualification_ref", "verification_status", "verified_by", "verified_at", "scope", "notes")


def _read_registry(path: Path, fields: tuple[str, ...], label: str) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        actual = tuple(reader.fieldnames or ())
        if actual != fields:
            raise ValueError(f"{path}: {label} registry columns must be exactly {fields}; got {actual}")
        return [{key: (value or "").strip() for key, value in row.items()} for row in reader]


def _validate_verification(row: Mapping[str, str], label: str, ident: str) -> None:
    if row["verification_status"] not in {"VERIFIED", "BLOCKED"}:
        raise ValueError(f"{label} {ident!r} has invalid verification_status")
    if not row["verified_by"]:
        raise ValueError(f"{label} {ident!r} requires verified_by")
    try:
        date.fromisoformat(row["verified_at"])
    except ValueError as exc:
        raise ValueError(f"{label} {ident!r} requires ISO verified_at") from exc


def load_source_registry(path: Path) -> dict[str, dict[str, str]]:
    rows = _read_registry(path, SOURCE_FIELDS, "source")
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        ident = row["source_id"]
        parsed = urlparse(row["source_url"])
        if not ident or ident in result:
            raise ValueError(f"source registry IDs must be non-empty and unique: {ident!r}")
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError(f"source {ident!r} requires an absolute HTTP(S) source_url")
        if not row["license"] or not row["allowed_uses"] or not row["notes"]:
            raise ValueError(f"source {ident!r} requires license, allowed_uses and notes")
        _validate_verification(row, "source", ident)
        result[ident] = row
    if not result:
        raise ValueError("source registry must contain at least one source record")
    return result


def load_reviewer_registry(path: Path) -> dict[str, dict[str, str]]:
    rows = _read_registry(path, REVIEWER_FIELDS, "reviewer")
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        ident = row["reviewer_id"]
        if not ident or ident in result:
            raise ValueError(f"reviewer registry IDs must be non-empty and unique: {ident!r}")
        if row["language"] not in {"th", "uk"}:
            raise ValueError(f"reviewer {ident!r} language must be th or uk")
        if not row["roles"] or not row["qualification_ref"] or not row["scope"]:
            raise ValueError(f"reviewer {ident!r} requires roles, qualification_ref and scope")
        _validate_verification(row, "reviewer", ident)
        result[ident] = row
    return result


def validate_source_reference(source_id: str, source_url: str, license_name: str,
                              required_use: str, registry: Mapping[str, Mapping[str, str]],
                              *, row_id: str, require_url: bool = True) -> Mapping[str, str]:
    source = registry.get(source_id.strip())
    if source is None:
        raise ValueError(f"row {row_id!r} uses unregistered source_id {source_id!r}")
    if source["verification_status"] != "VERIFIED":
        raise ValueError(f"row {row_id!r} source {source_id!r} is blocked: {source['notes']}")
    if license_name.strip() != source["license"]:
        raise ValueError(f"row {row_id!r} license does not match source registry for {source_id!r}")
    if require_url and not source_url.strip():
        raise ValueError(f"row {row_id!r} requires source_url for {source_id!r}")
    if source_url.strip() and source_url.strip() != source["source_url"]:
        raise ValueError(f"row {row_id!r} source_url does not match source registry for {source_id!r}")
    allowed = {value.strip() for value in source["allowed_uses"].split(";") if value.strip()}
    if required_use not in allowed:
        raise ValueError(f"row {row_id!r} source {source_id!r} is not approved for {required_use}; allowed uses: {', '.join(sorted(allowed))}")
    return source


def validate_reviewer_reference(reviewer_id: str, qualification_ref: str,
                                registry: Mapping[str, Mapping[str, str]], *,
                                language: str, required_role: str, row_id: str) -> Mapping[str, str]:
    reviewer = registry.get(reviewer_id.strip())
    if reviewer is None:
        raise ValueError(f"row {row_id!r} uses unregistered reviewer_id {reviewer_id!r}")
    if reviewer["verification_status"] != "VERIFIED":
        raise ValueError(f"reviewer {reviewer_id!r} is not VERIFIED")
    if reviewer["language"] != language:
        raise ValueError(f"reviewer {reviewer_id!r} language {reviewer['language']!r} does not satisfy {language!r}")
    roles = {value.strip() for value in reviewer["roles"].split(";") if value.strip()}
    if required_role not in roles:
        raise ValueError(f"reviewer {reviewer_id!r} lacks required role {required_role!r}")
    if qualification_ref.strip() != reviewer["qualification_ref"]:
        raise ValueError(f"row {row_id!r} qualification reference does not match verified reviewer registry")
    return reviewer
