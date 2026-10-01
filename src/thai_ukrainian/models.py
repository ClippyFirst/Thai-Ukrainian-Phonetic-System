from dataclasses import dataclass, field

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

@dataclass
class SyllableAnalysis:
    input: str
    normalized: str
    onset: list[str] = field(default_factory=list)
    onset_class: str | None = None
    vowel: str | None = None
    vowel_length: str | None = None
    coda: str | None = None
    coda_ipa: str | None = None
    tone_mark: str | None = None
    live_dead: str | None = None
    tone: ToneResult | None = None
    ipa: str | None = None
    rules_applied: list[str] = field(default_factory=list)
    candidates: list[dict] = field(default_factory=list)
    status: str = "analyzed"
    sources: list[str] = field(default_factory=list)
