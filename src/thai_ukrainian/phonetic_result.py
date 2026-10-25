from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import SyllableAnalysis


SYMBOLS = (
    "tɕʰ", "tɕ", "kʰ", "pʰ", "tʰ", "ŋ", "ɯ", "ɤ", "ɛ", "ɔ", "ʔ",
    "k", "p", "t", "d", "b", "m", "f", "n", "s", "r", "l", "j", "w",
    "h", "a", "i", "e", "u", "o",
)
VOWELS = {"a", "i", "e", "u", "o", "ɛ", "ɔ", "ɯ", "ɤ"}
MODIFIERS = {"ː", "̚", "̯", "̩"}


@dataclass(frozen=True)
class PhoneticSegment:
    """One segment with both phonemic and (when aligned) surface realization."""

    ipa: str
    kind: str
    surface_ipa: str | None = None
    provenance: tuple[str, ...] = ()
    certainty: str = "SUPPORTED"


def _segment_ipa(ipa: str | None, provenance: tuple[str, ...]) -> list[PhoneticSegment]:
    segments: list[PhoneticSegment] = []
    if not ipa:
        return segments
    i = 0
    while i < len(ipa):
        if ipa[i] in MODIFIERS:
            if segments:
                previous = segments[-1]
                segments[-1] = PhoneticSegment(
                    previous.ipa + ipa[i], previous.kind, provenance=previous.provenance,
                    certainty=previous.certainty,
                )
            else:
                segments.append(PhoneticSegment(ipa[i], "unknown", provenance=provenance, certainty="UNCERTAIN"))
            i += 1
            continue
        match = next((symbol for symbol in SYMBOLS if ipa.startswith(symbol, i)), None)
        if match is None:
            segments.append(PhoneticSegment(ipa[i], "unknown", provenance=provenance, certainty="UNSUPPORTED"))
            i += 1
            continue
        kind = "vowel" if match in VOWELS else "consonant"
        segments.append(PhoneticSegment(match, kind, provenance=provenance))
        i += len(match)
    return segments


@dataclass(frozen=True)
class PhoneticResult:
    """Typed contract between Thai phonology and downstream language adapters.

    phonemic_ipa is the adapter input. broad_surface_ipa is a separate,
    conservative surface representation. Tone remains metadata rather than
    being appended to the segmental IPA string.
    """

    phonemic_ipa: str | None
    broad_surface_ipa: str | None
    segments: tuple[PhoneticSegment, ...]
    syllable_boundaries: tuple[int, ...] = (0,)
    word_boundaries: tuple[int, ...] = ()
    vowel_length: str | None = None
    tone_category: str | None = None
    tone_contour_ipa: str | None = None
    status: str = "SUPPORTED"
    provenance: tuple[str, ...] = ()
    uncertainty: tuple[str, ...] = ()

    @classmethod
    def from_syllable_analysis(cls, analysis: "SyllableAnalysis") -> "PhoneticResult":
        provenance = tuple(dict.fromkeys([*analysis.sources, *analysis.rules_applied]))
        segments = _segment_ipa(analysis.phonemic_ipa, provenance)
        surface_segments = _segment_ipa(analysis.phonetic_ipa, provenance)
        if len(segments) == len(surface_segments):
            segments = [
                PhoneticSegment(
                    phonemic.ipa, phonemic.kind, surface.surface_ipa or surface.ipa,
                    phonemic.provenance, phonemic.certainty,
                )
                for phonemic, surface in zip(segments, surface_segments)
            ]
        surface_supported = analysis.phonetic_ipa is None or all(
            segment.certainty == "SUPPORTED" for segment in surface_segments
        )
        status = "SUPPORTED" if (
            analysis.status == "analyzed"
            and analysis.phonemic_ipa
            and all(segment.certainty == "SUPPORTED" for segment in segments)
            and surface_supported
        ) else ("UNCERTAIN" if analysis.status.startswith("analysis-dependent") else "UNSUPPORTED")
        return cls(
            phonemic_ipa=analysis.phonemic_ipa,
            broad_surface_ipa=analysis.phonetic_ipa,
            segments=tuple(segments),
            syllable_boundaries=(0, len(segments)) if segments else (0,),
            vowel_length=analysis.vowel_length,
            tone_category=analysis.tone.tone if analysis.tone else None,
            tone_contour_ipa=analysis.tone.contour_ipa if analysis.tone else None,
            status=status,
            provenance=provenance,
            uncertainty=tuple(analysis.warnings),
        )

    def as_dict(self) -> dict:
        return {
            "phonemic_ipa": self.phonemic_ipa,
            "broad_surface_ipa": self.broad_surface_ipa,
            "segments": [
                {
                    "ipa": s.ipa, "kind": s.kind, "surface_ipa": s.surface_ipa,
                    "provenance": list(s.provenance), "certainty": s.certainty,
                }
                for s in self.segments
            ],
            "syllable_boundaries": list(self.syllable_boundaries),
            "word_boundaries": list(self.word_boundaries),
            "vowel_length": self.vowel_length,
            "tone_category": self.tone_category,
            "tone_contour_ipa": self.tone_contour_ipa,
            "status": self.status,
            "provenance": list(self.provenance),
            "uncertainty": list(self.uncertainty),
        }
