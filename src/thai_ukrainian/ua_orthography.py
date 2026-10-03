from __future__ import annotations

# Project-specific phonetic-to-Ukrainian candidate rendering.
# This is not an official Ukrainian transliteration standard.
# It is a transparent orthographic target layer whose alternatives must be
# validated against adjudicated Ukrainian output before being treated as gold.

SEGMENTS = {
    "tɕʰ": ["ч"], "tɕ": ["ч"], "pʰ": ["п"], "tʰ": ["т"], "kʰ": ["к"],
    "p": ["п"], "b": ["б"], "m": ["м"], "f": ["ф"], "t": ["т"], "d": ["д"],
    "n": ["н"], "s": ["с"], "r": ["р"], "l": ["л"], "k": ["к"], "ŋ": ["нг"],
    "h": ["г"], "w": ["в"], "j": ["й"], "ʔ": [""],
    "iː": ["і"], "i": ["і"], "eː": ["е"], "e": ["е"], "ɛː": ["е"], "ɛ": ["е"],
    "aː": ["а"], "a": ["а"], "uː": ["у"], "u": ["у"], "oː": ["о"], "o": ["о"],
    "ɔː": ["о"], "ɔ": ["о"], "ɯː": ["и"], "ɯ": ["и"],
    "ɤː": ["и", "е"], "ɤ": ["и", "е"],
}

def _tokenize(ipa: str) -> list[str]:
    keys = sorted(SEGMENTS, key=len, reverse=True)
    out = []
    i = 0
    while i < len(ipa):
        if ipa[i].isspace() or ipa[i] in ".˧˩˥":
            i += 1
            continue
        for key in keys:
            if ipa.startswith(key, i):
                out.append(key)
                i += len(key)
                break
        else:
            return []
    return out

def candidates_for_ipa(ipa: str, limit: int = 8) -> list[str]:
    tokens = _tokenize(ipa)
    if not tokens:
        return []
    candidates = [""]
    for token in tokens:
        next_candidates = []
        for base in candidates:
            for option in SEGMENTS[token]:
                next_candidates.append(base + option)
        candidates = sorted(set(next_candidates))
        if len(candidates) > limit:
            candidates = candidates[:limit]
    return candidates

def render(ipa: str) -> dict:
    candidates = candidates_for_ipa(ipa)
    return {
        "status": "project-candidate",
        "ipa": ipa,
        "candidates": candidates,
        "selected": candidates[0] if candidates else None,
        "tone_separate": True,
        "validation_status": "not_empirically_calibrated",
    }
