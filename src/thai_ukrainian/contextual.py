from __future__ import annotations

from .models import Consonant

UNRELEASED_FINALS = {"p": "p̚", "t": "t̚", "k": "k̚"}


def surface_ipa_for_consonant(consonant: Consonant, position: str) -> str:
    """Return a conservative position-specific surface IPA realization.

    Position is syllable-internal: onset or coda. Word position is handled
    separately by the word model and must not be inferred here.
    """
    if position == "onset":
        return consonant.onset_ipa or ""
    if position == "coda":
        ipa = consonant.coda_ipa or ""
        return UNRELEASED_FINALS.get(ipa, ipa)
    raise ValueError("position must be 'onset' or 'coda'")


def vowel_surface_context(ipa: str, syllable_context: str) -> str:
    """Keep declared vowel IPA unchanged until an evidence-backed rule exists.

    Thai vowel duration and spectral properties can vary phonetically with
    context and speaking style, but this project does not fabricate a
    deterministic quality-changing allophone without a declared rule.
    """
    if syllable_context not in {"open", "closed"}:
        raise ValueError("syllable_context must be 'open' or 'closed'")
    return ipa
