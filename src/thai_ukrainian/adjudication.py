"""Validation gates for blind, independently reviewed Thai phonetic packets.

The validator checks packet integrity and reviewer separation. It does not
judge linguistic correctness or promote labels to gold automatically.
"""
from __future__ import annotations

from datetime import date
from math import isfinite
from typing import Iterable, Mapping

PACKET_FIELDS = (
    "id", "thai", "stratum", "probe", "orthography_validity", "lexical_reading",
    "word_boundaries", "syllable_boundaries", "phonemic_ipa", "broad_surface_ipa",
    "tone_sequence", "vowel_length", "final_glottal", "transcription_level",
    "uncertainty", "abstention_reason", "reviewer_id", "reviewer_qualification_ref",
    "reviewed_at", "audio_asset_reference", "audio_time_start", "audio_time_end",
    "source_notes",
)
ANNOTATION_FIELDS = PACKET_FIELDS[4:]
ORTHOGRAPHY_VALUES = {"VALID", "INVALID", "AMBIGUOUS", "UNKNOWN"}
TRANSCRIPTION_LEVELS = {"BROAD_PHONEMIC", "BROAD_SURFACE", "NARROW_ACOUSTIC"}
UNCERTAINTY_VALUES = {"LOW", "MEDIUM", "HIGH", "ABSTAIN"}
FINAL_GLOTTAL_VALUES = {"PRESENT", "ABSENT", "CONTEXTUAL", "UNKNOWN", "NOT_APPLICABLE"}


def _unique_rows(rows: Iterable[Mapping[str, str]]) -> dict[str, Mapping[str, str]]:
    indexed: dict[str, Mapping[str, str]] = {}
    for row in rows:
        ident = (row.get("id") or "").strip()
        if not ident:
            raise ValueError("every packet row requires a non-empty id")
        if ident in indexed:
            raise ValueError(f"packet ids must be unique: {ident}")
        indexed[ident] = row
    return indexed


def _require_exact_fields(
    indexed: Mapping[str, Mapping[str, str]], expected_fields: Iterable[str], packet_name: str
) -> None:
    expected = set(expected_fields)
    for ident, row in indexed.items():
        actual = set(row)
        if actual != expected:
            missing = sorted(expected - actual)
            extra = sorted(actual - expected)
            raise ValueError(
                f"{packet_name} fields mismatch for {ident}: missing={missing}, extra={extra}"
            )


def validate_blind_packet(
    rows: Iterable[Mapping[str, str]],
    challenge_rows: Iterable[Mapping[str, str]],
) -> dict:
    """Require a blank, output-blind packet matching the frozen challenge set."""
    indexed = _unique_rows(rows)
    _require_exact_fields(indexed, PACKET_FIELDS, "Thai blind packet")
    expected = _unique_rows(challenge_rows)
    if set(indexed) != set(expected):
        missing = sorted(set(expected) - set(indexed))
        extra = sorted(set(indexed) - set(expected))
        raise ValueError(
            f"packet challenge set mismatch; missing={missing[:5]}, extra={extra[:5]}"
        )
    for ident, row in indexed.items():
        source = expected[ident]
        if (row.get("thai") or "") != (source.get("input") or ""):
            raise ValueError(f"packet input does not match frozen challenge set: {ident}")
        if (row.get("stratum") or "") != (source.get("stratum") or ""):
            raise ValueError(f"packet stratum does not match frozen challenge set: {ident}")
        if (row.get("probe") or "") != (source.get("probe") or ""):
            raise ValueError(f"packet probe does not match frozen challenge set: {ident}")
        filled = [field for field in ANNOTATION_FIELDS if (row.get(field) or "").strip()]
        if filled:
            raise ValueError(
                f"blind packet annotation fields must be blank for {ident}: {', '.join(filled)}"
            )
    return {"records": len(indexed), "status": "BLIND_PACKET_VALID", "labels_prefilled": 0}


def validate_review_packet(
    rows: Iterable[Mapping[str, str]],
    expected_ids: Iterable[str],
    reviewer_id: str,
) -> dict:
    """Validate one reviewer's completed packet without scoring its judgments."""
    if not reviewer_id.strip():
        raise ValueError("reviewer_id must be supplied")
    indexed = _unique_rows(rows)
    _require_exact_fields(indexed, PACKET_FIELDS, "Thai review packet")
    expected = set(expected_ids)
    if set(indexed) != expected:
        raise ValueError("review packet must cover the exact frozen challenge set")
    abstentions = 0
    for ident, row in indexed.items():
        if (row.get("reviewer_id") or "").strip() != reviewer_id:
            raise ValueError(f"all rows must name the same reviewer ({reviewer_id})")
        if not (row.get("reviewer_qualification_ref") or "").strip():
            raise ValueError(f"reviewer_qualification_ref is required: {ident}")
        try:
            date.fromisoformat((row.get("reviewed_at") or "").strip())
        except ValueError as exc:
            raise ValueError(f"reviewed_at must be an ISO date: {ident}") from exc
        orthography = (row.get("orthography_validity") or "").strip()
        level = (row.get("transcription_level") or "").strip()
        uncertainty = (row.get("uncertainty") or "").strip()
        if orthography not in ORTHOGRAPHY_VALUES:
            raise ValueError(f"invalid orthography_validity for {ident}: {orthography!r}")
        if level not in TRANSCRIPTION_LEVELS:
            raise ValueError(f"invalid transcription_level for {ident}: {level!r}")
        if uncertainty not in UNCERTAINTY_VALUES:
            raise ValueError(f"invalid uncertainty for {ident}: {uncertainty!r}")
        ipa = (row.get("phonemic_ipa") or "").strip()
        abstention_reason = (row.get("abstention_reason") or "").strip()
        if uncertainty == "ABSTAIN":
            abstentions += 1
            if ipa or (row.get("broad_surface_ipa") or "").strip():
                raise ValueError(f"ABSTAIN rows must not contain IPA labels: {ident}")
            if not abstention_reason:
                raise ValueError(f"abstention_reason is required: {ident}")
        elif not ipa:
            raise ValueError(f"missing phonemic_ipa requires uncertainty=ABSTAIN: {ident}")
        final_glottal = (row.get("final_glottal") or "").strip()
        if final_glottal and final_glottal not in FINAL_GLOTTAL_VALUES:
            raise ValueError(f"invalid final_glottal value for {ident}: {final_glottal!r}")
        if level == "NARROW_ACOUSTIC":
            asset = (row.get("audio_asset_reference") or "").strip()
            start = (row.get("audio_time_start") or "").strip()
            end = (row.get("audio_time_end") or "").strip()
            try:
                start_value, end_value = float(start), float(end)
            except ValueError as exc:
                raise ValueError(f"narrow acoustic labels require an audio time interval: {ident}") from exc
            if not asset or not isfinite(start_value) or not isfinite(end_value) or start_value < 0 or end_value <= start_value:
                raise ValueError(f"narrow acoustic labels require a valid audio asset and interval: {ident}")
    return {
        "records": len(indexed),
        "reviewer_id": reviewer_id,
        "abstentions": abstentions,
        "status": "REVIEW_PACKET_VALID_NOT_GOLD",
    }


def validate_independent_pair(
    reviewer_a: Iterable[Mapping[str, str]],
    reviewer_b: Iterable[Mapping[str, str]],
) -> dict:
    """Check reviewer separation and identical item coverage; do not adjudicate."""
    a = _unique_rows(reviewer_a)
    b = _unique_rows(reviewer_b)
    ids_a = {(row.get("reviewer_id") or "").strip() for row in a.values()}
    ids_b = {(row.get("reviewer_id") or "").strip() for row in b.values()}
    if len(ids_a) != 1 or len(ids_b) != 1 or "" in ids_a or "" in ids_b:
        raise ValueError("each independent packet must contain exactly one reviewer_id")
    reviewer_a_id, reviewer_b_id = next(iter(ids_a)), next(iter(ids_b))
    if reviewer_a_id == reviewer_b_id:
        raise ValueError("independent reviewers must have distinct reviewer_id values")
    if set(a) != set(b):
        raise ValueError("independent reviewers must cover identical item IDs")
    for ident in a:
        if (a[ident].get("thai") or "") != (b[ident].get("thai") or ""):
            raise ValueError(f"independent reviewer input mismatch: {ident}")
    validate_review_packet(a.values(), a.keys(), reviewer_a_id)
    validate_review_packet(b.values(), b.keys(), reviewer_b_id)
    return {
        "records": len(a),
        "reviewer_a_id": reviewer_a_id,
        "reviewer_b_id": reviewer_b_id,
        "status": "TWO_REVIEWERS_PRESENT_ADJUDICATION_STILL_REQUIRED",
    }


UKRAINIAN_PREFERENCE_FIELDS = (
    "id", "thai", "source_ipa", "ipa_reference_status", "source_id", "source_url",
    "license", "criteria_version", "reviewer_id", "reviewer_qualification_ref",
    "preferred_ukrainian_form", "syllable_boundary_policy", "tone_rendering_policy",
    "uncertainty", "abstention_reason", "reviewed_at", "rationale",
)
UKRAINIAN_CRITERIA_VERSION = "UA-PRACTICAL-TRANSCRIPTION-0.1"
UKRAINIAN_ANNOTATION_FIELDS = UKRAINIAN_PREFERENCE_FIELDS[8:]


def validate_ukrainian_blind_packet(
    rows: Iterable[Mapping[str, str]],
    source_rows: Iterable[Mapping[str, str]],
) -> dict:
    """Validate a candidate-blind UA preference packet conditional on source-attested IPA."""
    indexed = _unique_rows(rows)
    _require_exact_fields(indexed, UKRAINIAN_PREFERENCE_FIELDS, "Ukrainian preference packet")
    expected = _unique_rows(source_rows)
    if set(indexed) != set(expected):
        raise ValueError("Ukrainian packet must cover the exact source-attested IPA sample")
    for ident, row in indexed.items():
        source = expected[ident]
        comparisons = (
            ("thai", "thai"),
            ("source_ipa", "phonemic_ipa"),
            ("source_id", "source_id"),
            ("source_url", "source_url"),
            ("license", "license"),
        )
        for packet_field, source_field in comparisons:
            if (row.get(packet_field) or "") != (source.get(source_field) or ""):
                raise ValueError(f"Ukrainian packet {packet_field} does not match source: {ident}")
        if row.get("ipa_reference_status") != "SOURCE_ATTESTED_NOT_GOLD":
            raise ValueError(f"Ukrainian packet must label conditional IPA as not-gold: {ident}")
        if row.get("criteria_version") != UKRAINIAN_CRITERIA_VERSION:
            raise ValueError(f"Ukrainian packet criteria version mismatch: {ident}")
        filled = [
            field for field in UKRAINIAN_ANNOTATION_FIELDS
            if (row.get(field) or "").strip()
        ]
        if filled:
            raise ValueError(
                f"Ukrainian blind packet reviewer fields must be blank for {ident}: {', '.join(filled)}"
            )
    return {
        "records": len(indexed),
        "status": "CANDIDATE_BLIND_UKRAINIAN_PREFERENCE_PACKET_VALID",
        "ipa_reference_status": "SOURCE_ATTESTED_NOT_GOLD",
    }
