from __future__ import annotations
from .models import SyllableAnalysis
from .inventory import load_consonants
from .orthography import normalize_thai,tone_mark,detect_vowel,decompose_thai

SHORT_CODA={"p","t","k","ʔ"}
SONORANT_CODA={"m","n","ŋ","j","w"}

def _consonants(s,inv):return [c for c in s if c in inv]

def _split_onset_coda(s,inv,vowel):
    cs=_consonants(s,inv)
    if not cs:return [],None
    # With no explicit vowel sign, a single consonant is the onset of an
    # implicit-vowel syllable. Treating it as a coda leaves no onset and
    # previously caused an IndexError in parse_syllable().
    if not vowel.get("explicit") and len(cs) == 1:
        return cs, None
    # Some Thai rimes consume more than one consonant grapheme, e.g. เกียว
    # consumes ย+ว as part of /iaw/. Never let nucleus graphemes leak back
    # into onset/coda classification.
    consumed = {
        "V-X-IAW":["ย","ว"], "V-X-UAJ":["ว","ย"],
        "V-X-AJ":["ย"], "V-X-AW":["ว"], "V-X-IW":["ว"],
        "V-X-UJ":["ย"], "V-X-EW":["ว"], "V-X-EW-L":["ว"],
        "V-X-EAW":["ว"], "V-X-EY":["ย"], "V-X-OY":["ย"],
        "V-X-OJ":["ย"], "V-X-AW-S":["ว"], "V-X-UEY":["ย"],
    }.get(vowel.get("id"), [])
    if consumed:
        tmp=list(cs)
        for ch in reversed(consumed):
            if tmp and tmp[-1]==ch:
                tmp.pop()
        cs=tmp
    if vowel.get("terminal_glide") and cs and cs[-1] in {"ย","ว"}:
        return cs[:-1],None
    vowel_chars=set("ะาิีึืุูเแโใไำั็")
    last_v=max((i for i,c in enumerate(s) if c in vowel_chars),default=-1)
    last_c=max((i for i,c in enumerate(s) if c in inv),default=-1)
    if len(cs)>1 and last_c>last_v:return cs[:-1],cs[-1]
    return cs,None

def parse_syllable(syllable:str)->SyllableAnalysis:
    s=normalize_thai(syllable);inv=load_consonants();cs=_consonants(s,inv)
    if not cs:return SyllableAnalysis(syllable,s,status="unresolved:no-onset",warnings=["No Thai consonant grapheme detected."])
    v=detect_vowel(s);onset,coda=_split_onset_coda(s,inv,v)
    first=inv[onset[0]]
    coda_ipa=inv[coda].coda_ipa if coda else None
    status=("unresolved:implicit-vowel" if not v["explicit"] else ("analyzed" if not coda or inv[coda].coda_allowed else "invalid:coda-not-licensed"))
    if coda:
        live_dead="dead" if coda_ipa in SHORT_CODA else ("live" if coda_ipa in SONORANT_CODA else None)
    else:
        # Without an explicit vowel, vowel quantity and therefore tone
        # cannot be safely inferred at this layer.
        live_dead=None if not v["explicit"] else (
            "live" if v.get("terminal_glide") or v["ipa"].endswith(("m","j","w","ŋ"))
            else ("dead" if v["length"]=="short" else "live")
        )
    warnings=[]
    if not v["explicit"]:warnings.append("Implicit vowel inferred; lexical or morphological validation required.")
    if "์" in s:warnings.append("Thanthakhat/silent-mark construction detected; lexical parsing required.")
    if "ห" in s and len(cs)>1 and cs[0]=="ห":warnings.append("ห นำ construction detected; class-changing analysis required.")
    if "รร" in s:warnings.append("รร construction detected; contextual interpretation required.")
    return SyllableAnalysis(input=syllable,normalized=s,grapheme_order=[x["char"] for x in decompose_thai(s)],
        onset=onset,onset_class=first.class_,vowel=v["ipa"],vowel_id=v["id"],vowel_length=v["length"],
        coda=coda,coda_ipa=coda_ipa,tone_mark=tone_mark(s),live_dead=live_dead,warnings=warnings,status=status)
