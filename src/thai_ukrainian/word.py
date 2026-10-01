from __future__ import annotations

from .models import SyllablePosition, WordAnalysis


def position_label(index: int, total: int) -> str:
    if total == 1:
        return "standalone"
    if index == 0:
        return "initial"
    if index == total - 1:
        return "final"
    return "medial"


def analyze_word(syllables: list[str] | tuple[str, ...], *, source: str | None = None) -> WordAnalysis:
    """Analyze a word from an explicit syllable segmentation."""
    from .api import analyze_syllable

    if not syllables:
        raise ValueError("At least one syllable is required.")
    if any(not isinstance(s, str) or not s.strip() for s in syllables):
        raise ValueError("Every syllable must be a non-empty string.")

    analyses = [analyze_syllable(s) for s in syllables]
    total = len(analyses)
    positions = [SyllablePosition(i, total, position_label(i, total)) for i in range(total)]
    warnings: list[str] = []
    if source:
        for analysis in analyses:
            analysis.sources.append(source)
    if any(a.status != "analyzed" for a in analyses):
        warnings.append("One or more syllables did not receive a fully analyzed status.")

    return WordAnalysis(
        input="".join(syllables),
        syllables=analyses,
        positions=positions,
        segmentation_status="explicit",
        warnings=warnings,
        status="analyzed" if not warnings else "partial",
    )
