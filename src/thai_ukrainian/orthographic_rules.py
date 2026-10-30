import csv
from dataclasses import dataclass
from enum import Enum
from functools import lru_cache


from ._paths import THAI_DATA_ROOT

RULES_PATH = THAI_DATA_ROOT / "orthographic_rules.csv"


class ORole(str, Enum):
    VOWEL_CARRIER = "vowel_carrier"
    VOWEL_COMPONENT = "vowel_component"
    SPECIAL_Y_PATTERN = "special_y_pattern"
    ORTHOGRAPHIC_COMPONENT = "orthographic_component"
    GLOTTAL_ONSET = "glottal_onset"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class OrthographicRule:
    rule_id: str
    pattern: str
    grapheme: str
    role: ORole
    structural_condition: str
    phonological_action: str
    ukrainian_action: str
    priority: int
    evidence_status: str
    notes: str


@lru_cache(maxsize=1)
def load_orthographic_rules() -> list[OrthographicRule]:
    with RULES_PATH.open(encoding="utf-8", newline="") as f:
        return [
            OrthographicRule(
                rule_id=r["rule_id"],
                pattern=r["pattern"],
                grapheme=r["grapheme"],
                role=ORole(r["role"].lower()),
                structural_condition=r["structural_condition"],
                phonological_action=r["phonological_action"],
                ukrainian_action=r["ukrainian_action"],
                priority=int(r["priority"]),
                evidence_status=r["evidence_status"],
                notes=r["notes"],
            )
            for r in csv.DictReader(f)
        ]


def _contains_vowel_pattern(text: str) -> bool:
    # Structural evidence from the registered vowel inventory.  This deliberately
    # checks the complete orthographic construction rather than assigning a
    # phonetic value to อ in isolation.
    from .orthography import detect_vowel

    return bool(detect_vowel(text).get("explicit"))


def classify_o_role(text: str) -> OrthographicRule:
    """Classify อ by its structural role, with deterministic rule precedence.

    Precedence:
      1. special อย- construction
      2. registered vowel-plus-glide / vowel construction containing อ
      3. vowel-carrier construction
      4. explicit unresolved fallback

    The function does not generate IPA or Ukrainian text.  It only supplies the
    structural interpretation consumed by later stages.
    """
    if "อ" not in text:
        return OrthographicRule(
            "ORTH-O-999", "*", "อ", ORole.UNKNOWN, "grapheme absent",
            "not applicable", "not applicable", 999, "not_applicable", ""
        )

    rules = {r.rule_id: r for r in load_orthographic_rules()}

    if text.startswith("อย"):
        return rules["ORTH-O-003"]

    # A syllable beginning with อ is a carrier construction unless a higher-
    # priority special pattern has already matched.  Any following consonant
    # can then be analyzed as a coda (e.g. อัน), not as an onset.
    if text.startswith("อ"):
        return rules["ORTH-O-001"]

    if _contains_vowel_pattern(text):
        from .orthography import detect_vowel
        vowel = detect_vowel(text)
        matched = vowel.get("matched_text", "")
        # Only treat อ as a vowel component when the selected vowel/rime
        # actually consumes it. Otherwise preserve it for ordinary structural
        # validation (e.g. the deliberately malformed test form กาอ).
        if "อ" not in matched:
            return rules["ORTH-O-999"]

        consonants = set("กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬฮ")
        # For preposed-vowel spellings, the first grapheme after เ/แ/โ/ใ/ไ
        # is the onset candidate. Do not mistake a carrier อ in เอย for a
        # real onset just because the final ย belongs to the vowel glide.
        if text and text[0] in {"เ", "แ", "โ", "ใ", "ไ"}:
            has_real_onset = len(text) > 1 and text[1] in consonants and text[1] != "อ"
        else:
            has_real_onset = any(c in consonants for c in text if c != "อ")
        if has_real_onset:
            if "ว" in matched or "ย" in matched:
                return rules["ORTH-O-004"]
            return rules["ORTH-O-002"]
        return rules["ORTH-O-001"]

    return rules["ORTH-O-999"]


def ukrainian_action_for_o(rule: OrthographicRule) -> str:
    """Return a declarative Ukrainian-layer action, never an IPA substitution."""
    return rule.ukrainian_action
