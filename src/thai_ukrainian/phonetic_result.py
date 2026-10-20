from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import SyllableAnalysis


@dataclass(frozen=True)
class PhoneticSegment:
    """One IPA segment with the evidence trail that produced the analysis."""

    ipa: str
    kind: str
    provenance: tuple[str, ...] = ()
    certainty: str = "SUPPORTED"


@dataclass(frozen=True)
class PhoneticResult:
    """Typed contract between Thai phonology and downstream language adapters.

    phonemic_ipa is the adapter input. broad_surface_ipa is a separate,
    conservative surface representation and is never silently substituted for it.
    Tone remains metadata rather than being appended to the segmental IPA string.
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
        ipa = analysis.phonemic_ipa
        segments: list[PhoneticSegment] = []
        if ipa:
            # Longest-match inventory. Length is attached to the preceding vowel,
            # not treated as a segment in its own right.
            symbols = (
                "tɕʰ", "tɕ", "kʰ", "pʰ", "tʰ",
                "ŋ", "ɯ", "ɤ", "ɛ", "ɔ", "ʔ",
                "k", "p", "t", "d", "b", "m", "f", "n", "s", "r", "l",
                "j", "w", "h", "a", "i", "e", "u", "o",
            )
            i = 0
            while i < len(ipa):
                if ipa[i] == "ː":
                    if segments and segments[-1].kind == "vowel":
                        previous = segments[-1]
                        segments[-1] = PhoneticSegment(
                            previous.ipa + "ː", previous.kind, previous.provenance,
                            previous.certainty,
                        )
                    else:
                        segments.append(PhoneticSegment("ː", "unknown", tuple(analysis.rules_applied), "UNCERTAIN"))
                    i += 1
                    continue
                match = next((symbol for symbol in symbols if ipa.startswith(symbol, i)), None)
                if match is None:
                    segments.append(PhoneticSegment(ipa[i], "unknown", tuple(analysis.rules_applied), "UNSUPPORTED"))
                    i += 1
                    continue
                kind = "vowel" if match in {"a", "i", "e", "u", "o", "ɛ", "ɔ", "ɯ", "ɤ"} else "consonant"
                segments.append(PhoneticSegment(match, kind, tuple(analysis.rules_applied)))
                i += len(match)

        status = "SUPPORTED" if analysis.status == "analyzed" and ipa and all(
            segment.certainty == "SUPPORTED" for segment in segments
        ) else ("UNCERTAIN" if analysis.status.startswith("analysis-dependent") else "UNSUPPORTED")
        return cls(
            phonemic_ipa=ipa,
            broad_surface_ipa=analysis.phonetic_ipa,
            segments=tuple(segments),
            vowel_length=analysis.vowel_length,
            tone_category=analysis.tone.tone if analysis.tone else None,
            tone_contour_ipa=analysis.tone.contour_ipa if analysis.tone else None,
            status=status,
            provenance=tuple(dict.fromkeys([*analysis.sources, *analysis.rules_applied])),
            uncertainty=tuple(analysis.warnings),
        )

    def as_dict(self) -> dict:
        return {
            "phonemic_ipa": self.phonemic_ipa,
            "broad_surface_ipa": self.broad_surface_ipa,
            "segments": [
                {"ipa": s.ipa, "kind": s.kind, "provenance": list(s.provenance), "certainty": s.certainty}
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
