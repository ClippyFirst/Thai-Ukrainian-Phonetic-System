from .models import SyllableAnalysis
from .inventory import load_consonants
from .orthography import normalize_thai, TONE_MARKS

SHORT_MARKS=set("ะิึุัำ")
VOWEL_MARKS=set("ะาิีึืุูเแโใไำั็")

def parse_syllable(syllable):
    s=normalize_thai(syllable)
    inv=load_consonants()
    cs=[c for c in s if c in inv]
    if not cs:
        return SyllableAnalysis(syllable,s,status="unresolved:no-onset")

    first=inv[cs[0]]
    marks=[TONE_MARKS[c] for c in s if c in TONE_MARKS]
    vowel_positions=[i for i,ch in enumerate(s) if ch in VOWEL_MARKS]
    has_vowel=bool(vowel_positions)

    coda=None
    if len(cs)>1 and has_vowel:
        last_c_index=max(i for i,ch in enumerate(s) if ch in inv)
        last_v_index=max(vowel_positions)
        if last_c_index>last_v_index:
            coda=cs[-1]

    coda_ipa=inv[coda].coda_ipa if coda else None
    length="short" if any(ch in SHORT_MARKS for ch in s) else ("long" if has_vowel else None)

    if length is None:
        live=None
    elif coda_ipa:
        live="dead" if coda_ipa in {"p","t","k","ʔ"} else "live"
    else:
        live="dead" if length=="short" else "live"

    return SyllableAnalysis(
        syllable,s,[cs[0]],first.class_,None,length,coda,coda_ipa,
        marks[-1] if marks else None,live,
        status="partial" if not has_vowel else "analyzed"
    )
