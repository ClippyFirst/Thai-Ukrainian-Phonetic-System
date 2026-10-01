from __future__ import annotations
from .models import SyllableAnalysis
from .inventory import load_consonants
from .orthography import normalize_thai,tone_mark,detect_vowel,decompose_thai,TONE_CHARS

SHORT_CODA={"p","t","k","ʔ"}
SONORANT_CODA={"m","n","ŋ","j","w"}
TRUE_CLUSTER_FIRST={"ก","ข","ค","ต","ป","ผ","พ"}
TRUE_CLUSTER_SECOND={"ร","ล","ว"}
LEADING_H_FIRST={"ห"}
LEADING_H_SECOND={"ง","ญ","น","ม","ย","ร","ล","ว"}
VOWEL_SIGN_CHARS=set("ะาิีึืุูเแโใไำั็")
SUPPORTED_SPECIAL_CHARS={"์"}

def _consonants(s,inv):return [c for c in s if c in inv]

def _surface_residual_vowel_signs(s, vowel):
    cleaned="".join(c for c in s if c not in TONE_CHARS)
    matched=vowel.get("matched_text","")
    if not matched:
        return [c for c in cleaned if c in VOWEL_SIGN_CHARS]
    residual=cleaned.replace(matched,"",1)
    return [c for c in residual if c in VOWEL_SIGN_CHARS]

def _is_valid_complex_onset(onset):
    if len(onset)!=2:return True
    if onset[0] in TRUE_CLUSTER_FIRST and onset[1] in TRUE_CLUSTER_SECOND:return True
    if onset[0] in LEADING_H_FIRST and onset[1] in LEADING_H_SECOND:return True
    return False

def _split_onset_coda(s,inv,vowel):
    cs=_consonants(s,inv)
    if not cs:return [],None
    if not vowel.get("explicit") and len(cs) == 1:return cs,None
    consumed={
        "V-X-IAW":["ย","ว"],"V-X-UAJ":["ว","ย"],"V-X-AJ":["ย"],"V-X-AW":["ว"],
        "V-X-IW":["ว"],"V-X-UJ":["ย"],"V-X-EW":["ว"],"V-X-EW-L":["ว"],
        "V-X-EAW":["ว"],"V-X-EY":["ย"],"V-X-OY":["ย"],"V-X-OJ":["ย"],
        "V-X-AW-S":["ว"],"V-X-UEY":["ย"],
    }.get(vowel.get("id"),[])
    if consumed:
        tmp=list(cs)
        for ch in reversed(consumed):
            if tmp and tmp[-1]==ch:tmp.pop()
        cs=tmp
    if vowel.get("terminal_glide") and cs and cs[-1] in {"ย","ว"}:return cs[:-1],None
    vowel_chars=set("ะาิีึืุูเแโใไำั็")
    last_v=max((i for i,c in enumerate(s) if c in vowel_chars),default=-1)
    last_c=max((i for i,c in enumerate(s) if c in inv),default=-1)
    if len(cs)>1 and last_c>last_v:
        proposed=cs[:-1]
        if not _is_valid_complex_onset(proposed):return [cs[0]],None
        return proposed,cs[-1]
    if len(cs)>1 and not _is_valid_complex_onset(cs):return [cs[0]],None
    return cs,None

def parse_syllable(syllable:str)->SyllableAnalysis:
    s=normalize_thai(syllable);inv=load_consonants();cs=_consonants(s,inv)
    allowed=set(inv)|TONE_CHARS|VOWEL_SIGN_CHARS|SUPPORTED_SPECIAL_CHARS
    unsupported=[c for c in s if c not in allowed]
    if unsupported:
        return SyllableAnalysis(syllable,s,grapheme_order=[x["char"] for x in decompose_thai(s)],
            status="unresolved:unsupported-symbol",
            warnings=[f"Unsupported symbol(s) in syllable: {''.join(dict.fromkeys(unsupported))}"])
    if len([c for c in s if c in TONE_CHARS])>1:
        return SyllableAnalysis(syllable,s,grapheme_order=[x["char"] for x in decompose_thai(s)],
            status="unresolved:multiple-tone-marks",
            warnings=["More than one Thai tone mark occurs in a single supplied syllable; tone cannot be inferred deterministically."])
    if not cs:return SyllableAnalysis(syllable,s,status="unresolved:no-onset",warnings=["No Thai consonant grapheme detected."])
    v=detect_vowel(s)
    residual_vowels=_surface_residual_vowel_signs(s,v)
    if residual_vowels:
        return SyllableAnalysis(syllable,s,grapheme_order=[x["char"] for x in decompose_thai(s)],
            onset=cs[:1],onset_class=inv[cs[0]].class_,status="unresolved:multiple-vowel-signs",
            warnings=[f"Unconsumed vowel sign(s) remain outside the detected vowel/rime pattern: {''.join(residual_vowels)}"])
    onset,coda=_split_onset_coda(s,inv,v)
    first=inv[onset[0]]
    coda_ipa=inv[coda].coda_ipa if coda else None
    warnings=[]
    complex_invalid=(len(cs)>len(onset)+(1 if coda else 0) and len(cs)>=2 and v["explicit"])
    if complex_invalid:warnings.append("Adjacent consonants are not licensed as a standard Thai complex onset; explicit syllable/lexical segmentation is required.")
    status=("unresolved:nonconforming-consonant-sequence" if complex_invalid else
            ("unresolved:implicit-vowel" if not v["explicit"] else
             ("analyzed" if not coda or inv[coda].coda_allowed else "invalid:coda-not-licensed")))
    if coda:live_dead="dead" if coda_ipa in SHORT_CODA else ("live" if coda_ipa in SONORANT_CODA else None)
    else:live_dead=None if not v["explicit"] else ("live" if v.get("terminal_glide") or v["ipa"].endswith(("m","j","w","ŋ")) else ("dead" if v["length"]=="short" else "live"))
    if len(onset)>=2:
        second_ipa=inv[onset[1]].onset_ipa
        tone_class=first.class_ if second_ipa in {"m","n","ŋ","j","w","r","l"} else inv[onset[1]].class_
    else:tone_class=first.class_
    if not v["explicit"]:warnings.append("Implicit vowel detected but unresolved; lexical or morphological validation required.")
    if "์" in s:warnings.append("Thanthakhat/silent-mark construction detected; lexical parsing required.")
    if "ห" in s and len(cs)>1 and cs[0]=="ห":warnings.append("ห นำ construction detected; class-changing analysis required.")
    if "รร" in s:warnings.append("รร construction detected; contextual interpretation required.")
    return SyllableAnalysis(input=syllable,normalized=s,grapheme_order=[x["char"] for x in decompose_thai(s)],
        onset=onset,onset_class=first.class_,tone_class=tone_class,vowel=v["ipa"],vowel_id=v["id"],vowel_length=v["length"],
        coda=coda,coda_ipa=coda_ipa,tone_mark=tone_mark(s),live_dead=live_dead,warnings=warnings,status=status)
