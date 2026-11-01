"""Validation gates for blind, independently reviewed Thai phonetic packets.

The validator checks packet integrity and reviewer separation. It does not
judge linguistic correctness or promote labels to gold automatically.
"""
from __future__ import annotations

from datetime import date
from math import isfinite
from typing import Iterable, Mapping
import unicodedata

from .evidence_registry import validate_reviewer_reference, validate_source_reference

PACKET_FIELDS = (
    "id", "thai", "orthography_validity", "lexical_reading",
    "word_boundaries", "syllable_boundaries", "phonemic_ipa", "broad_surface_ipa", "narrow_ipa",
    "tone_sequence", "vowel_length", "final_glottal", "transcription_level",
    "uncertainty", "abstention_reason", "reviewer_id", "reviewer_qualification_ref",
    "reviewed_at", "audio_source_id", "audio_asset_reference", "audio_time_start", "audio_time_end",
    "source_notes",
)
ANNOTATION_FIELDS = PACKET_FIELDS[2:]
ORTHOGRAPHY_VALUES = {"VALID", "INVALID", "AMBIGUOUS", "UNKNOWN"}
TRANSCRIPTION_LEVELS = {"BROAD_PHONEMIC", "NARROW_ACOUSTIC"}
UNCERTAINTY_VALUES = {"LOW", "MEDIUM", "HIGH", "ABSTAIN"}
FINAL_GLOTTAL_VALUES = {"PRESENT", "ABSENT", "CONTEXTUAL", "UNKNOWN", "NOT_APPLICABLE"}
TONE_VALUES = {"MID", "LOW", "FALLING", "HIGH", "RISING", "UNKNOWN", "NOT_APPLICABLE"}
VOWEL_LENGTH_VALUES = {"SHORT", "LONG", "UNKNOWN", "NOT_APPLICABLE"}


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


def _pairwise_agreement(
    reviewer_a: Mapping[str, Mapping[str, str]],
    reviewer_b: Mapping[str, Mapping[str, str]],
    fields: Iterable[str],
) -> dict:
    """Report descriptive exact agreement without treating it as adjudication or gold."""
    field_results = {}
    for field in fields:
        both_labeled = 0
        exact = 0
        a_only_missing = 0
        b_only_missing = 0
        both_missing = 0
        for ident in reviewer_a:
            value_a = unicodedata.normalize("NFC", (reviewer_a[ident].get(field) or "").strip())
            value_b = unicodedata.normalize("NFC", (reviewer_b[ident].get(field) or "").strip())
            if value_a and value_b:
                both_labeled += 1
                exact += value_a == value_b
            elif not value_a and not value_b:
                both_missing += 1
            elif not value_a:
                a_only_missing += 1
            else:
                b_only_missing += 1
        field_results[field] = {
            "n_both_labeled": both_labeled,
            "exact_agreements": exact,
            "exact_agreement_rate": exact / both_labeled if both_labeled else None,
            "a_only_missing": a_only_missing,
            "b_only_missing": b_only_missing,
            "both_missing": both_missing,
        }
    return {
        "method": "NFC-normalized exact string agreement among rows where both reviewers supplied a value; descriptive only, no chance correction",
        "fields": field_results,
    }


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
    challenge_rows: Iterable[Mapping[str, str]] | None = None,
    reviewer_registry: Mapping[str, Mapping[str, str]] | None = None,
    source_registry: Mapping[str, Mapping[str, str]] | None = None,
) -> dict:
    """Validate one reviewer's completed packet without scoring its judgments."""
    if not reviewer_id.strip():
        raise ValueError("reviewer_id must be supplied")
    indexed = _unique_rows(rows)
    _require_exact_fields(indexed, PACKET_FIELDS, "Thai review packet")
    expected = set(expected_ids)
    if set(indexed) != expected:
        raise ValueError("review packet must cover the exact frozen challenge set")
    challenge_index = _unique_rows(challenge_rows) if challenge_rows is not None else None
    if challenge_index is not None and set(indexed) != set(challenge_index):
        raise ValueError("review packet must match the exact frozen challenge inputs")
    abstentions = 0
    for ident, row in indexed.items():
        if challenge_index is not None and (row.get("thai") or "") != (challenge_index[ident].get("input") or ""):
            raise ValueError(f"review packet source text differs from frozen challenge: {ident}")
        if (row.get("reviewer_id") or "").strip() != reviewer_id:
            raise ValueError(f"all rows must name the same reviewer ({reviewer_id})")
        if not (row.get("reviewer_qualification_ref") or "").strip():
            raise ValueError(f"reviewer_qualification_ref is required: {ident}")
        if reviewer_registry is not None:
            validate_reviewer_reference(
                reviewer_id, row["reviewer_qualification_ref"], reviewer_registry,
                language="th", required_role="THAI_PHONETICIAN", row_id=ident,
            )
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
        if uncertainty != "ABSTAIN":
            required_annotations = (
                "lexical_reading", "word_boundaries", "syllable_boundaries",
                "tone_sequence", "vowel_length", "final_glottal",
            )
            missing_annotations = [
                field for field in required_annotations if not (row.get(field) or "").strip()
            ]
            if missing_annotations:
                raise ValueError(
                    f"non-abstaining review requires lexical, boundary, tone, length and glottal labels for {ident}: "
                    f"{', '.join(missing_annotations)}"
                )
            word_boundaries = row["word_boundaries"].strip()
            syllable_boundaries = row["syllable_boundaries"].strip()
            thai_text = unicodedata.normalize("NFC", row["thai"])
            word_parts = word_boundaries.split("|")
            if any(not part for part in word_parts) or unicodedata.normalize("NFC", "".join(word_parts)) != thai_text:
                raise ValueError(f"word_boundaries must reconstruct the Thai input for {ident}")
            syllable_words = syllable_boundaries.split("|")
            syllable_parts = [part for word in syllable_words for part in word.split(".")]
            if (
                any(not part for part in syllable_parts)
                or unicodedata.normalize("NFC", "".join(syllable_parts)) != thai_text
            ):
                raise ValueError(f"syllable_boundaries must reconstruct the Thai input for {ident}")
            if len(syllable_words) != len(word_parts):
                raise ValueError(f"word and syllable boundary word counts differ for {ident}")
            syllable_count = len(syllable_parts)
            ipa_body = ipa.strip()
            if (ipa_body.startswith("/") and ipa_body.endswith("/")) or (
                ipa_body.startswith("[") and ipa_body.endswith("]")
            ):
                ipa_body = ipa_body[1:-1]
            ipa_words = ipa_body.split("|")
            ipa_syllables = [part for word in ipa_words for part in word.split(".")]
            if (
                any(not part for part in ipa_syllables)
                or len(ipa_words) != len(word_parts)
                or len(ipa_syllables) != syllable_count
            ):
                raise ValueError(f"phonemic IPA syllabification must align with syllable boundaries for {ident}")
            surface_ipa = (row.get("broad_surface_ipa") or "").strip()
            if surface_ipa:
                surface_body = surface_ipa
                if (surface_body.startswith("/") and surface_body.endswith("/")) or (
                    surface_body.startswith("[") and surface_body.endswith("]")
                ):
                    surface_body = surface_body[1:-1]
                surface_words = surface_body.split("|")
                surface_syllables = [part for word in surface_words for part in word.split(".")]
                if (
                    any(not part for part in surface_syllables)
                    or len(surface_words) != len(word_parts)
                    or len(surface_syllables) != syllable_count
                ):
                    raise ValueError(f"surface IPA syllabification must align with syllable boundaries for {ident}")
            tone_values = [value.strip() for value in row["tone_sequence"].split(",")]
            length_values = [value.strip() for value in row["vowel_length"].split(",")]
            glottal_values = [value.strip() for value in row["final_glottal"].split(",")]
            if any(not value for value in tone_values + length_values + glottal_values):
                raise ValueError(f"tone, vowel-length and glottal sequences cannot contain empty values: {ident}")
            if any(value not in TONE_VALUES for value in tone_values):
                raise ValueError(f"invalid tone_sequence value for {ident}")
            if any(value not in VOWEL_LENGTH_VALUES for value in length_values):
                raise ValueError(f"invalid vowel_length value for {ident}")
            if any(value not in FINAL_GLOTTAL_VALUES for value in glottal_values):
                raise ValueError(f"invalid final_glottal value for {ident}")
            if not (len(tone_values) == len(length_values) == len(glottal_values) == syllable_count):
                raise ValueError(f"tone, vowel-length and glottal labels must align with syllables for {ident}")
            audio_source_id = (row.get("audio_source_id") or "").strip()
            if audio_source_id:
                if source_registry is None:
                    raise ValueError(f"audio source registry is required when audio_source_id is supplied: {ident}")
                audio_source = source_registry.get(audio_source_id)
                if audio_source is None:
                    raise ValueError(f"audio source_id is not registered: {ident}")
                validate_source_reference(
                    audio_source_id, audio_source["source_url"], audio_source["license"],
                    "ACOUSTIC_PHONETICS_RESEARCH", source_registry, row_id=ident,
                )
            narrow_ipa = (row.get("narrow_ipa") or "").strip()
            if level == "NARROW_ACOUSTIC":
                if not audio_source_id:
                    raise ValueError(f"narrow acoustic review requires a registered audio_source_id: {ident}")

                if not (narrow_ipa.startswith("[") and narrow_ipa.endswith("]") and len(narrow_ipa) > 2):
                    raise ValueError(f"narrow acoustic review requires a separate bracketed narrow_ipa label: {ident}")
                narrow_body = narrow_ipa[1:-1]
                narrow_words = narrow_body.split("|")
                narrow_syllables = [part for word in narrow_words for part in word.split(".")]
                if (
                    any(not part for part in narrow_syllables)
                    or len(narrow_words) != len(word_parts)
                    or len(narrow_syllables) != syllable_count
                ):
                    raise ValueError(f"narrow IPA syllabification must align with syllable boundaries for {ident}")
                asset = (row.get("audio_asset_reference") or "").strip()
                start = (row.get("audio_time_start") or "").strip()
                end = (row.get("audio_time_end") or "").strip()
                try:
                    start_value, end_value = float(start), float(end)
                except ValueError as exc:
                    raise ValueError(f"narrow acoustic labels require an audio time interval: {ident}") from exc
                if not asset or not isfinite(start_value) or not isfinite(end_value) or start_value < 0 or end_value <= start_value:
                    raise ValueError(f"narrow acoustic labels require a valid audio asset and interval: {ident}")
            elif narrow_ipa:
                raise ValueError(f"narrow_ipa is only valid for NARROW_ACOUSTIC reviews: {ident}")
    return {
        "records": len(indexed),
        "reviewer_id": reviewer_id,
        "abstentions": abstentions,
        "status": "REVIEW_PACKET_VALID_NOT_GOLD",
    }


def validate_independent_pair(
    reviewer_a: Iterable[Mapping[str, str]],
    reviewer_b: Iterable[Mapping[str, str]],
    challenge_rows: Iterable[Mapping[str, str]] | None = None,
    reviewer_registry: Mapping[str, Mapping[str, str]] | None = None,
    source_registry: Mapping[str, Mapping[str, str]] | None = None,
) -> dict:
    """Check reviewer separation and identical item coverage; do not adjudicate."""
    challenge_rows = list(challenge_rows) if challenge_rows is not None else None
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
    validate_review_packet(a.values(), a.keys(), reviewer_a_id, challenge_rows, reviewer_registry, source_registry)
    validate_review_packet(b.values(), b.keys(), reviewer_b_id, challenge_rows, reviewer_registry, source_registry)
    agreement = _pairwise_agreement(
        a, b,
        (
            "orthography_validity", "lexical_reading", "word_boundaries",
            "syllable_boundaries", "phonemic_ipa", "broad_surface_ipa",
            "narrow_ipa", "tone_sequence", "vowel_length", "final_glottal",
            "uncertainty",
        ),
    )
    agreement["joint_abstentions"] = sum(
        a[ident].get("uncertainty") == "ABSTAIN" and b[ident].get("uncertainty") == "ABSTAIN"
        for ident in a
    )
    agreement["one_sided_abstentions"] = sum(
        (a[ident].get("uncertainty") == "ABSTAIN") != (b[ident].get("uncertainty") == "ABSTAIN")
        for ident in a
    )
    return {
        "records": len(a),
        "reviewer_a_id": reviewer_a_id,
        "reviewer_b_id": reviewer_b_id,
        "agreement": agreement,
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
    source_registry: Mapping[str, Mapping[str, str]] | None = None,
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
        if source_registry is not None:
            validate_source_reference(
                row["source_id"], row["source_url"], row["license"],
                "UKRAINIAN_PREFERENCE_INPUT", source_registry, row_id=ident,
            )
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


UKRAINIAN_UNCERTAINTY_VALUES = {"LOW", "MEDIUM", "HIGH", "ABSTAIN"}
UKRAINIAN_SYLLABLE_POLICIES = {
    "PRESERVE_IN_DISPLAY", "DISPLAY_ONLY", "OMIT", "NOT_APPLICABLE"
}
UKRAINIAN_TONE_POLICIES = {
    "NO_ORTHOGRAPHIC_TONE_MARK", "KEEP_EXPLICIT_MARK_WITH_RATIONALE", "NOT_APPLICABLE"
}


def validate_ukrainian_review_packet(
    rows: Iterable[Mapping[str, str]],
    expected_ids: Iterable[str],
    reviewer_id: str,
    source_rows: Iterable[Mapping[str, str]] | None = None,
    reviewer_registry: Mapping[str, Mapping[str, str]] | None = None,
    source_registry: Mapping[str, Mapping[str, str]] | None = None,
) -> dict:
    """Validate one Ukrainian-native preference review, conditional on supplied IPA."""
    if not reviewer_id.strip():
        raise ValueError("reviewer_id must be supplied")
    indexed = _unique_rows(rows)
    _require_exact_fields(indexed, UKRAINIAN_PREFERENCE_FIELDS, "Ukrainian review packet")
    if set(indexed) != set(expected_ids):
        raise ValueError("Ukrainian review packet must cover the exact frozen sample")
    source_index = _unique_rows(source_rows) if source_rows is not None else None
    if source_index is not None and set(indexed) != set(source_index):
        raise ValueError("Ukrainian review packet must match the exact source-attested sample")
    abstentions = 0
    for ident, row in indexed.items():
        if row.get("ipa_reference_status") != "SOURCE_ATTESTED_NOT_GOLD":
            raise ValueError(f"Ukrainian review must preserve the source-attested-not-gold status: {ident}")
        for field in ("source_ipa", "source_id", "source_url", "license"):
            if not (row.get(field) or "").strip():
                raise ValueError(f"Ukrainian review requires {field}: {ident}")
        if source_index is not None:
            source = source_index[ident]
            for packet_field, source_field in (
                ("thai", "thai"), ("source_ipa", "phonemic_ipa"),
                ("source_id", "source_id"), ("source_url", "source_url"),
                ("license", "license"),
            ):
                if (row.get(packet_field) or "") != (source.get(source_field) or ""):
                    raise ValueError(f"Ukrainian review source mismatch for {packet_field}: {ident}")
        if source_registry is not None:
            validate_source_reference(
                row["source_id"], row["source_url"], row["license"],
                "UKRAINIAN_PREFERENCE_INPUT", source_registry, row_id=ident,
            )
        if row.get("criteria_version") != UKRAINIAN_CRITERIA_VERSION:
            raise ValueError(f"Ukrainian review criteria version mismatch: {ident}")
        if (row.get("reviewer_id") or "").strip() != reviewer_id:
            raise ValueError(f"all rows must name the same Ukrainian reviewer ({reviewer_id})")
        if not (row.get("reviewer_qualification_ref") or "").strip():
            raise ValueError(f"reviewer_qualification_ref is required: {ident}")
        if reviewer_registry is not None:
            validate_reviewer_reference(
                reviewer_id, row["reviewer_qualification_ref"], reviewer_registry,
                language="uk", required_role="UKRAINIAN_NATIVE_REVIEWER", row_id=ident,
            )
        try:
            date.fromisoformat((row.get("reviewed_at") or "").strip())
        except ValueError as exc:
            raise ValueError(f"reviewed_at must be an ISO date: {ident}") from exc
        uncertainty = (row.get("uncertainty") or "").strip()
        if uncertainty not in UKRAINIAN_UNCERTAINTY_VALUES:
            raise ValueError(f"invalid Ukrainian preference uncertainty for {ident}")
        preferred = (row.get("preferred_ukrainian_form") or "").strip()
        abstention_reason = (row.get("abstention_reason") or "").strip()
        if uncertainty == "ABSTAIN":
            abstentions += 1
            if preferred or not abstention_reason:
                raise ValueError(f"Ukrainian abstention requires no preferred form and a reason: {ident}")
        elif not preferred:
            raise ValueError(f"preferred_ukrainian_form is required unless abstaining: {ident}")
        if not (row.get("rationale") or "").strip():
            raise ValueError(f"Ukrainian preference rationale is required: {ident}")
        if row.get("syllable_boundary_policy") not in UKRAINIAN_SYLLABLE_POLICIES:
            raise ValueError(f"invalid syllable_boundary_policy for {ident}")
        if row.get("tone_rendering_policy") not in UKRAINIAN_TONE_POLICIES:
            raise ValueError(f"invalid tone_rendering_policy for {ident}")
    return {
        "records": len(indexed),
        "reviewer_id": reviewer_id,
        "abstentions": abstentions,
        "status": "UKRAINIAN_REVIEW_VALID_CONDITIONAL_NOT_GOLD",
    }


def validate_ukrainian_independent_pair(
    reviewer_a: Iterable[Mapping[str, str]],
    reviewer_b: Iterable[Mapping[str, str]],
    source_rows: Iterable[Mapping[str, str]] | None = None,
    reviewer_registry: Mapping[str, Mapping[str, str]] | None = None,
    source_registry: Mapping[str, Mapping[str, str]] | None = None,
) -> dict:
    """Require distinct Ukrainian reviewers and identical IPA-conditioned sample."""
    source_rows = list(source_rows) if source_rows is not None else None
    a = _unique_rows(reviewer_a)
    b = _unique_rows(reviewer_b)
    _require_exact_fields(a, UKRAINIAN_PREFERENCE_FIELDS, "Ukrainian reviewer A packet")
    _require_exact_fields(b, UKRAINIAN_PREFERENCE_FIELDS, "Ukrainian reviewer B packet")
    ids_a = {(row.get("reviewer_id") or "").strip() for row in a.values()}
    ids_b = {(row.get("reviewer_id") or "").strip() for row in b.values()}
    if len(ids_a) != 1 or len(ids_b) != 1 or "" in ids_a or "" in ids_b:
        raise ValueError("each Ukrainian review must contain exactly one reviewer_id")
    reviewer_a_id, reviewer_b_id = next(iter(ids_a)), next(iter(ids_b))
    if reviewer_a_id == reviewer_b_id:
        raise ValueError("independent Ukrainian reviewers must have distinct reviewer_id values")
    if set(a) != set(b):
        raise ValueError("independent Ukrainian reviewers must cover identical item IDs")
    for ident in a:
        for field in ("thai", "source_ipa", "source_id", "criteria_version"):
            if (a[ident].get(field) or "") != (b[ident].get(field) or ""):
                raise ValueError(f"independent Ukrainian reviewer input mismatch for {field}: {ident}")
    validate_ukrainian_review_packet(
        a.values(), a.keys(), reviewer_a_id, source_rows, reviewer_registry, source_registry
    )
    validate_ukrainian_review_packet(
        b.values(), b.keys(), reviewer_b_id, source_rows, reviewer_registry, source_registry
    )
    agreement = _pairwise_agreement(
        a, b,
        (
            "preferred_ukrainian_form", "syllable_boundary_policy",
            "tone_rendering_policy", "uncertainty",
        ),
    )
    agreement["joint_abstentions"] = sum(
        a[ident].get("uncertainty") == "ABSTAIN" and b[ident].get("uncertainty") == "ABSTAIN"
        for ident in a
    )
    agreement["one_sided_abstentions"] = sum(
        (a[ident].get("uncertainty") == "ABSTAIN") != (b[ident].get("uncertainty") == "ABSTAIN")
        for ident in a
    )
    return {
        "records": len(a),
        "reviewer_a_id": reviewer_a_id,
        "reviewer_b_id": reviewer_b_id,
        "agreement": agreement,
        "status": "TWO_UKRAINIAN_REVIEWERS_PRESENT_CONDITIONAL_NOT_GOLD",
    }
