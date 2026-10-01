from .models import SyllableAnalysis
from .inventory import load_consonants
from .orthography import normalize_thai, TONE_MARKS

SHORT_MARKS = set("ะิึุัำ")

def parse_syllable(syllable):
    s = normalize_thai(syllable)
    inv = load_consonants()
    consonants = [c for c in s if c in inv]
    if not consonants:
        return SyllableAnalysis(syllable, s, status="unresolved:no-onset")
    first = inv[consonants[0]]
    marks = [TONE_MARKS[c] for c in s if c in TONE_MARKS]
    coda = consonants[-1] if len(consonants) > 1 else None
    coda_ipa = inv[coda].coda_ipa if coda else None
    has_vowel = any(ch in "ะาิีึืุูเแโใไำั" for ch in s)
    vowel_length = "short" if any(ch in SHORT_MARKS for ch in s) else ("long" if has_vowel else None)
    live_dead = None
    if vowel_length == "short":
        live_dead = "dead"
    if coda_ipa:
        live_dead = "dead" if coda_ipa in {"p","t","k","ʔ"} else "live"
    return SyllableAnalysis(
        syllable, s, [consonants[0]], first.class_, None, vowel_length,
        coda, coda_ipa, marks[-1] if marks else None, live_dead,
        status="partial" if not has_vowel else "analyzed"
    )
