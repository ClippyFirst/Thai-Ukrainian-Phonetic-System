"""Registry-backed provenance gates for source data and human reviewers."""
from __future__ import annotations

import csv
from datetime import date
from pathlib import Path
import re
from math import isfinite
from typing import Mapping
from urllib.parse import urlparse

SOURCE_FIELDS = ("source_id", "source_url", "license", "allowed_uses", "verification_status", "verified_by", "verified_at", "notes")
REVIEWER_FIELDS = ("reviewer_id", "language", "roles", "qualification_ref", "verification_status", "verified_by", "verified_at", "scope", "notes")
AUDIO_ASSET_FIELDS = (
    "asset_id", "source_id", "dataset_revision", "asset_uri", "file_sha256",
    "speaker_ref", "microphone", "overlap_status", "duration_seconds",
    "verification_status", "verified_by", "verified_at", "notes",
)
AUDIO_MICROPHONES = {"NEAR_FIELD", "FAR_FIELD", "LAVALIER", "HEADSET", "OTHER", "UNKNOWN"}
AUDIO_OVERLAP_STATES = {"NONE", "PRESENT", "UNKNOWN"}


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



def load_audio_asset_registry(
    path: Path, source_registry: Mapping[str, Mapping[str, str]]
) -> dict[str, dict[str, str]]:
    """Load exact, file-level audio provenance; an empty header-only registry is valid."""
    rows = _read_registry(path, AUDIO_ASSET_FIELDS, "audio asset")
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        ident = row["asset_id"]
        if not ident or ident in result:
            raise ValueError(f"audio asset IDs must be non-empty and unique: {ident!r}")
        if row["dataset_revision"].lower() in {"main", "master", "latest", "default", "head"}:
            raise ValueError(f"audio asset {ident!r} requires an immutable dataset_revision, not a moving alias")
        asset_uri = urlparse(row["asset_uri"])
        if asset_uri.scheme not in {"http", "https"} or not asset_uri.netloc:
            raise ValueError(f"audio asset {ident!r} requires an absolute HTTP(S) asset_uri")
        required = (
            "source_id", "dataset_revision", "asset_uri", "file_sha256", "speaker_ref",
            "microphone", "overlap_status", "duration_seconds", "notes",
        )
        missing = [field for field in required if not row[field]]
        if missing:
            raise ValueError(f"audio asset {ident!r} requires {', '.join(missing)}")
        if not re.fullmatch(r"[0-9a-fA-F]{64}", row["file_sha256"]):
            raise ValueError(f"audio asset {ident!r} requires a 64-character SHA-256")
        if row["microphone"] not in AUDIO_MICROPHONES:
            raise ValueError(f"audio asset {ident!r} has invalid microphone category")
        if row["overlap_status"] not in AUDIO_OVERLAP_STATES:
            raise ValueError(f"audio asset {ident!r} has invalid overlap_status")
        try:
            duration = float(row["duration_seconds"])
        except ValueError as exc:
            raise ValueError(f"audio asset {ident!r} requires numeric duration_seconds") from exc
        if not isfinite(duration) or duration <= 0:
            raise ValueError(f"audio asset {ident!r} requires positive finite duration_seconds")
        source = source_registry.get(row["source_id"])
        if source is None:
            raise ValueError(f"audio asset {ident!r} uses unregistered source_id {row['source_id']!r}")
        validate_source_reference(
            row["source_id"], source["source_url"], source["license"],
            "ACOUSTIC_PHONETICS_RESEARCH", source_registry, row_id=ident,
        )
        _validate_verification(row, "audio asset", ident)
        result[ident] = row
    return result


def validate_audio_asset_reference(
    asset_id: str,
    source_id: str,
    start: str,
    end: str,
    registry: Mapping[str, Mapping[str, str]],
    *,
    row_id: str,
) -> Mapping[str, str]:
    asset = registry.get(asset_id.strip())
    if asset is None:
        raise ValueError(f"row {row_id!r} uses unregistered audio asset {asset_id!r}")
    if asset["verification_status"] != "VERIFIED":
        raise ValueError(f"row {row_id!r} audio asset {asset_id!r} is blocked")
    if asset["source_id"] != source_id.strip():
        raise ValueError(f"row {row_id!r} audio asset source_id does not match audio_source_id")
    if asset["overlap_status"] != "NONE":
        raise ValueError(f"row {row_id!r} audio asset must be verified as non-overlapping")
    try:
        start_value, end_value = float(start), float(end)
        duration = float(asset["duration_seconds"])
    except ValueError as exc:
        raise ValueError(f"row {row_id!r} requires numeric audio interval") from exc
    if (
        not isfinite(start_value) or not isfinite(end_value)
        or start_value < 0 or end_value <= start_value or end_value > duration
    ):
        raise ValueError(f"row {row_id!r} audio interval must be positive and within the registered asset duration")
    return asset

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
