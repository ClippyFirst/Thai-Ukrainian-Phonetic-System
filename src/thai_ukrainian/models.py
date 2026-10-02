from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class Consonant:
    grapheme: str
    codepoint: str
    class_: str
    onset_ipa: str | None
    coda_ipa: str | None
    coda_allowed: bool
    notes: str = ""

@dataclass(frozen=True)
class ToneResult:
    tone: str
    contour_ipa: str
    rule_id: str
    evidence_status: str = "core"

@dataclass(frozen=True)
class Candidate:
    candidate_id: str
    ipa: str
    distance: float
    status: str
    mismatches: tuple[str, ...] = ()
    notes: str = ""

@dataclass
class SyllableAnalysis:
    input: str
    normalized: str
    grapheme_order: list[str] = field(default_factory=list)
    onset: list[str] = field(default_factory=list)
    onset_class: str | None = None
    tone_class: str | None = None
    vowel: str | None = None
    vowel_id: str | None = None
    vowel_length: str | None = None
    coda: str | None = None
    coda_ipa: str | None = None
    tone_mark: str | None = None
    live_dead: str | None = None
    tone: ToneResult | None = None
    phonemic_ipa: str | None = None
    phonetic_ipa: str | None = None
    ukrainian_candidates: list[Candidate] = field(default_factory=list)
    selected_candidate: str | None = None
    rules_applied: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    status: str = "analyzed"
    sources: list[str] = field(default_factory=list)
    special_analyses: list[dict[str, str]] = field(default_factory=list)
    ukrainian_orthography_candidates: list[str] = field(default_factory=list)
    selected_ukrainian_orthography: str | None = None

    def as_dict(self) -> dict[str, Any]:
        d=self.__dict__.copy()
        d["tone"]=None if self.tone is None else self.tone.__dict__
        d["ukrainian_candidates"]=[x.__dict__ for x in self.ukrainian_candidates]
        return d

@dataclass(frozen=True)
class SyllablePosition:
    index: int
    total: int
    label: str

    @property
    def is_initial(self) -> bool:
        return self.label in {"standalone", "initial"}

    @property
    def is_final(self) -> bool:
        return self.label in {"standalone", "final"}

@dataclass
class WordAnalysis:
    input: str
    syllables: list[SyllableAnalysis] = field(default_factory=list)
    positions: list[SyllablePosition] = field(default_factory=list)
    segmentation_status: str = "explicit"
    warnings: list[str] = field(default_factory=list)
    status: str = "analyzed"

    @property
    def phonemic_ipa(self) -> str:
        return ".".join(a.phonemic_ipa or "?" for a in self.syllables)

    @property
    def phonetic_ipa(self) -> str:
        return ".".join(a.phonetic_ipa or "?" for a in self.syllables)

    def as_dict(self) -> dict[str, Any]:
        return {
            "input": self.input,
            "segmentation_status": self.segmentation_status,
            "status": self.status,
            "syllables": [
                {"position": {"index": p.index, "total": p.total, "label": p.label},
                 "analysis": a.as_dict()}
                for a, p in zip(self.syllables, self.positions)
            ],
            "phonemic_ipa": self.phonemic_ipa,
            "phonetic_ipa": self.phonetic_ipa,
            "warnings": self.warnings,
        }
