from dataclasses import dataclass

@dataclass(frozen=True)
class Candidate:
    thai_ipa: str
    ukrainian_candidate: str
    distance: float
    dimension: str
    status: str
    notes: str

SEED = {
    "p": ["p"], "pʰ": ["p"], "b": ["b", "p"],
    "t": ["t"], "tʰ": ["t"], "d": ["d", "t"],
    "k": ["k"], "kʰ": ["k"], "tɕ": ["tʃ"], "tɕʰ": ["tʃ"],
    "m": ["m"], "n": ["n"], "ŋ": [], "f": ["f"], "s": ["s"],
    "h": ["h"], "w": ["w"], "j": ["j"], "r": ["r"], "l": ["l"], "ʔ": []
}

def rank_ukrainian_candidates(ipa):
    values = SEED.get(ipa, [])
    if not values:
        return [Candidate(ipa, "UNRESOLVED", float("inf"), "segmental", "unresolved", "No direct seed; target inventory adapter required")]
    return [Candidate(ipa, x, 0.0 if x == ipa else 1.0, "segmental", "heuristic-seed", "Candidate, not identity claim") for x in values]
