"""Evidence-gated Thai function-marker analysis for research diagnostics.

This module annotates candidate grammatical functions in an already tokenized
sequence. It does not perform word segmentation, full morphological parsing,
POS tagging, or pronunciation inference. Candidate annotations never modify IPA
or Ukrainian outputs.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Any


@dataclass(frozen=True)
class MorphologyCandidate:
    token_index: int
    token: str
    rule_id: str
    category: str
    label: str
    status: str
    scope: str
    evidence: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "token_index": self.token_index,
            "token": self.token,
            "rule_id": self.rule_id,
            "category": self.category,
            "label": self.label,
            "status": self.status,
            "scope": self.scope,
            "evidence": self.evidence,
        }


# The input is an existing token stream. Unknown or unsegmented text must not
# be silently split here: morphological interpretation depends on boundaries.
def analyze_morphology(tokens: Iterable[Mapping[str, Any] | str]) -> dict[str, Any]:
    """Return contextual marker candidates over an explicit token sequence.

    Only Thai tokens participate. Each rule is a conservative local cue, not a
    proof of the token's part of speech or meaning. Polyfunctional forms are
    labelled ambiguous/context-dependent instead of being forced into one role.
    """
    normalized: list[tuple[int, str, str]] = []
    for index, item in enumerate(tokens):
        if isinstance(item, str):
            text, kind = item, "thai"
        else:
            text = str(item.get("input", item.get("text", "")))
            kind = str(item.get("kind", "thai"))
        if text and kind == "thai":
            normalized.append((index, text, kind))

    candidates: list[MorphologyCandidate] = []
    for position, (original_index, token, _) in enumerate(normalized):
        previous = normalized[position - 1][1] if position else None
        following = normalized[position + 1][1] if position + 1 < len(normalized) else None
        is_final = following is None
        add = lambda rule_id, category, label, status, scope, evidence: candidates.append(
            MorphologyCandidate(original_index, token, rule_id, category, label, status, scope, evidence)
        )

        if token == "ไม่" and following:
            add("TH-MORPH-NEG-001", "polarity", "negation marker candidate",
                "contextual-candidate", "likely scopes over following predicate; predicate boundary/POS not established",
                "Thai negation commonly precedes the expression it negates; surface order alone does not establish scope.")
        elif token == "จะ" and following:
            add("TH-MORPH-MOD-001", "modality/aspect", "prospective/modal marker candidate",
                "contextual-candidate", "following predicate candidate",
                "จะ commonly precedes a predicate in prospective or modal constructions; it is not a verb inflection.")
        elif token == "กำลัง" and following:
            has_yu = any(value == "อยู่" for _, value, _ in normalized[position + 1:])
            add("TH-MORPH-ASP-001", "aspect", "progressive marker candidate",
                "contextual-candidate", "following predicate; paired อยู่ is recorded when present",
                "กำลัง is used in progressive constructions; tokenization and syntactic scope remain unverified.")
        elif token == "อยู่":
            has_kamlang = any(value == "กำลัง" for _, value, _ in normalized[:position])
            if has_kamlang and previous:
                add("TH-MORPH-ASP-002", "aspect", "progressive construction candidate",
                    "contextual-candidate", "construction may span กำลัง … อยู่",
                    "อยู่ can participate in a progressive construction but also has lexical/location uses.")
            elif previous:
                add("TH-MORPH-AMB-001", "ambiguous-function", "aspectual or lexical use",
                    "analysis-dependent", "requires predicate and discourse context",
                    "อยู่ is polyfunctional; the sequence alone is insufficient to force a grammatical-marker analysis.")
        elif token == "แล้ว" and previous:
            add("TH-MORPH-ASP-003", "aspect", "completive/change-of-state marker candidate",
                "analysis-dependent", "relation to preceding predicate is unverified",
                "แล้ว can mark completion/change of state but also has other discourse and lexical uses.")
        elif token == "ไหม" and is_final:
            add("TH-MORPH-Q-001", "question", "yes/no question particle candidate",
                "contextual-candidate", "clause-final; clause boundary is assumed from end of supplied input",
                "Final ไหม commonly marks a polar question; punctuation and discourse context may change the analysis.")
        elif token in {"ครับ", "ค่ะ", "คะ", "จ้ะ", "จ๊ะ"} and is_final:
            add("TH-MORPH-POL-001", "discourse/politeness", "politeness particle candidate",
                "contextual-candidate", "final token in supplied span",
                "These forms can function as politeness/register particles; speaker, interaction and lexical use are not inferred.")
        elif token == "และ" and previous and following:
            add("TH-MORPH-COORD-001", "coordination", "coordinator candidate",
                "contextual-candidate", "links adjacent token candidates",
                "และ commonly coordinates constituents; constituent types and phrase boundaries are not established.")
        elif token == "ของ" and previous and following:
            add("TH-MORPH-GEN-001", "nominal-relation", "possessive/genitive linker candidate",
                "analysis-dependent", "relation between neighboring constituents is unverified",
                "ของ may introduce a possessive/genitive relation but also has lexical uses.")
        elif token in {"การ", "ความ"} and following:
            add("TH-MORPH-NOM-001", "derivation/nominalization", "nominalizer candidate",
                "analysis-dependent", "possible derivation of following predicate/adjective",
                "การ and ความ can participate in nominalization; the lexical base and construction must be checked.")
        elif token in {"ถูก", "โดน"} and following:
            add("TH-MORPH-VOICE-001", "voice/construction", "passive-affectee construction candidate",
                "analysis-dependent", "following predicate candidate",
                "ถูก and โดน can mark passive/affected constructions but also occur as lexical verbs.")
        elif token == "เคย" and following:
            add("TH-MORPH-ASP-004", "aspect/experience", "experiential marker candidate",
                "contextual-candidate", "following predicate candidate",
                "เคย commonly marks prior experience; clause structure and scope remain unverified.")

    return {
        "schema_version": "1.0",
        "mode": "conservative-function-marker-candidates",
        "status": "research-only",
        "input_token_count": len(normalized),
        "candidate_count": len(candidates),
        "candidates": [candidate.as_dict() for candidate in candidates],
        "limitations": [
            "This is not a complete Thai morphological analyzer or POS tagger.",
            "Word boundaries are inherited from the supplied token sequence and are not validated here.",
            "Candidate labels are contextual cues, not certainty scores or adjudicated analyses.",
            "No candidate changes the phonological IPA or IPA-to-Ukrainian pipeline.",
            "Compounding, derivation, reduplication, classifiers, names, scope and discourse require broader evidence and review.",
        ],
    }
