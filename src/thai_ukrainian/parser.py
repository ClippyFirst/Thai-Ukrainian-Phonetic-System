from __future__ import annotations
from .models import SyllableAnalysis
from .inventory import load_consonants
from .orthography import normalize_thai,tone_mark,detect_vowel,decompose_thai,TONE_CHARS
from .special import detect_special_orthography
from .orthographic_rules import classify_o_role

SHORT_CODA={"p","t","k","ʔ"}
SONORANT_CODA={"m","n","ŋ","j","w"}
TRUE_CLUSTER_FIRST={"ก","ข","ค","ต","ป","ผ","พ","ท"}
TRUE_CLUSTER_SECOND={"ร","ล","ว"}
LEADING_H_FIRST={"ห"}
LEADING_H_SECOND={"ง","ญ","น","ม","ย","ร","ล","ว"}
PREPOSED_VOWEL_CHARS={"เ","แ","โ","ใ","ไ"}
VOWEL_SIGN_CHARS=set("ะาิีึืุูเแโใไำั็")

# High-confidence lexical readings for orthographic forms whose surface spelling
# cannot be resolved by the productive grapheme rules alone. These are not a
# general-purpose dictionary: each entry is an explicit evidence-gated reading
# used to prevent the core parser from fabricating an IPA analysis.
LEXICAL_READINGS={
    "จริง":"จิง",
    "สร้าง":"ส้าง",
    "เศร้า":"เส้า",
    "ไซร้":"ไซ้",
    "จันทร์":"จัน",
    "ศุกร์":"สุก",
    "เสาร์":"เสา",
    "สัตว์":"สัด",
    "พันธุ์":"พัน",
    "ฟิล์ม":"ฟิม",
    "โทรศัพท์":"โท|ระ|สับ",
    "อาทิตย์":"อา|ทิด",
    "ฤดู":"รึ|ดู",
    "ฤทธิ์":"ริด",
    "ฤๅษี":"รือ|สี",
    "ฤษี":"รึ|สี",
    "ทฤษฎี":"ทริด|สะ|ดี",
    "อย่า":"หย่า",
    "อยู่":"หยู่",
    "อย่าง":"หยา่ง",
    "อยาก":"หยาก",
}
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
        "V-X-AW-S":["ว"],"V-X-UEY":["ย"],"V-X-UA":["ว"],
    }.get(vowel.get("id"),[])
    if consumed:
        tmp=list(cs)
        for ch in reversed(consumed):
            if tmp and tmp[-1]==ch:tmp.pop()
        cs=tmp
    if vowel.get("terminal_glide") and vowel.get("id") != "V-X-AI" and cs and cs[-1] in {"ย","ว"}:return cs[:-1],None
    cleaned="".join(c for c in s if c not in TONE_CHARS)
    if len(cs)>=2 and any(c in PREPOSED_VOWEL_CHARS for c in cleaned):
        if _is_valid_complex_onset(cs[:2]):
            if len(cs)==2:return cs,None
            if len(cs)==3:return cs[:2],cs[2]
            return [cs[0]],None
    vowel_chars=set("ะาิีึืุูเแโใไำั็")
    last_v=max((i for i,c in enumerate(s) if c in vowel_chars),default=-1)
    last_c=max((i for i,c in enumerate(s) if c in inv),default=-1)
    if len(cs)>1 and last_c>last_v:
        proposed=cs[:-1]
        if not _is_valid_complex_onset(proposed):return [cs[0]],None
        return proposed,cs[-1]
    if len(cs)>1 and not _is_valid_complex_onset(cs):return [cs[0]],None
    return cs,None

def _o_interpretation(text: str) -> dict[str, str]:
    rule=classify_o_role(text)
    return {
        "grapheme":"อ",
        "rule_id":rule.rule_id,
        "role":rule.role.value,
        "priority":str(rule.priority),
        "evidence_status":rule.evidence_status,
        "ukrainian_action":rule.ukrainian_action,
    }

def parse_syllable(syllable:str)->SyllableAnalysis:
    s=normalize_thai(syllable);inv=load_consonants();cs=_consonants(s,inv)
    o_rule=classify_o_role(s) if "อ" in s else None
    if o_rule and o_rule.role.value in {"vowel_component", "orthographic_component"}:
        cs=[c for c in cs if c != "อ"]
    interpretations=[_o_interpretation(s)] if o_rule and o_rule.role.value != "unknown" else []

    special_rules = detect_special_orthography(s)
    if special_rules:
        special = [{"rule_id": r["rule_id"], "construction": r["construction"], "status": r["analysis_status"], "candidate_ipa": r["candidate_ipa"], "notes": r["notes"]} for r in special_rules]
        return SyllableAnalysis(syllable,s,grapheme_order=[x["char"] for x in decompose_thai(s)],
            status="analysis-dependent:special-orthography",
            warnings=["Special Thai orthography requires lexical/contextual adjudication; no single IPA was forced."],
            special_analyses=special, orthographic_interpretations=interpretations)

    allowed=set(inv)|TONE_CHARS|VOWEL_SIGN_CHARS|SUPPORTED_SPECIAL_CHARS
    unsupported=[c for c in s if c not in allowed]
    if unsupported:
        return SyllableAnalysis(syllable,s,grapheme_order=[x["char"] for x in decompose_thai(s)],
            status="unresolved:unsupported-symbol",
            warnings=[f"Unsupported symbol(s) in syllable: {''.join(dict.fromkeys(unsupported))}"],
            orthographic_interpretations=interpretations)
    if len([c for c in s if c in TONE_CHARS])>1:
        return SyllableAnalysis(syllable,s,grapheme_order=[x["char"] for x in decompose_thai(s)],
            status="unresolved:multiple-tone-marks",
            warnings=["More than one Thai tone mark occurs in a single supplied syllable; tone cannot be inferred deterministically."],
            orthographic_interpretations=interpretations)

    # อ is an onset carrier only when the classifier says it is VOWEL_CARRIER.
    # In that case it is retained as the structural onset for tone/IPA analysis.
    # In VOWEL_COMPONENT/ORTHOGRAPHIC_COMPONENT configurations it remains part
    # of the vowel spelling and is not promoted to an onset.
    if o_rule and o_rule.role.value == "vowel_carrier" and not cs:
        cs=["อ"]
    if not cs:
        return SyllableAnalysis(syllable,s,grapheme_order=[x["char"] for x in decompose_thai(s)],
            status="unresolved:no-onset",warnings=["No Thai consonant grapheme detected."],
            orthographic_interpretations=interpretations)

    v=detect_vowel(s)
    if v.get("analysis_dependent"):
        # The orthography does not determine vowel length here (e.g. เดิน vs เงิน).
        # Preserve structural onset/coda information, but withhold tone/IPA until
        # lexical evidence selects one of the declared vowel candidates.
        onset, coda = _split_onset_coda(s, inv, v)
        if not onset:
            onset = cs[:1]
        first = inv[onset[0]] if onset else None
        return SyllableAnalysis(
            input=syllable, normalized=s,
            grapheme_order=[x["char"] for x in decompose_thai(s)],
            onset=onset, onset_class=first.class_ if first else None,
            tone_class=first.class_ if first else None,
            coda=coda, coda_ipa=inv[coda].coda_ipa if coda else None,
            tone_mark=tone_mark(s), status="analysis-dependent:vowel-length",
            warnings=["The closed เ-ิ- spelling does not determine /ɤ/ vs /ɤː/ without lexical evidence; no IPA or tone was forced."],
            orthographic_interpretations=interpretations,
        )

    residual_vowels=_surface_residual_vowel_signs(s,v)
    if residual_vowels:
        return SyllableAnalysis(syllable,s,grapheme_order=[x["char"] for x in decompose_thai(s)],
            onset=cs[:1],onset_class=inv[cs[0]].class_,status="unresolved:multiple-vowel-signs",
            warnings=[f"Unconsumed vowel sign(s) remain outside the detected vowel/rime pattern: {''.join(residual_vowels)}"],
            orthographic_interpretations=interpretations)

    # Standalone ไอ/ใอ uses อ only as a vowel carrier. It is not a coda.
    if v.get("id") == "V-X-AI":
        if cs == ["อ"]:
            onset, coda = ["อ"], None
        elif len(cs) == 1:
            onset, coda = cs, None
        elif any(c in PREPOSED_VOWEL_CHARS for c in "".join(c for c in s if c not in TONE_CHARS)) and _is_valid_complex_onset(cs[:2]):
            onset, coda = (cs, None) if len(cs) == 2 else (cs[:2], cs[2])
        else:
            onset, coda = cs[:-1], cs[-1]
    else:
        onset,coda=_split_onset_coda(s,inv,v)
    # Carrier forms have a structural carrier onset even though the grapheme is
    # not an independent Ukrainian segment.
    if o_rule and o_rule.role.value == "vowel_carrier" and not onset:
        onset=["อ"]
    if not onset:
        return SyllableAnalysis(
            input=syllable,normalized=s,grapheme_order=[x["char"] for x in decompose_thai(s)],
            status="unresolved:empty-onset-after-vowel-analysis",
            warnings=["Vowel/rime analysis consumed all consonant candidates; the generated structural form cannot be assigned an onset deterministically."],
            orthographic_interpretations=interpretations)

    first=inv[onset[0]]
    coda_ipa=inv[coda].coda_ipa if coda else None
    warnings=[]
    complex_invalid=(len(cs)>len(onset)+(1 if coda else 0) and len(cs)>=2 and v["explicit"])
    if complex_invalid:warnings.append("Adjacent consonants are not licensed as a standard Thai complex onset; explicit syllable/lexical segmentation is required.")
    status=("unresolved:nonconforming-consonant-sequence" if complex_invalid else
            ("analyzed" if v.get("resolved", v["explicit"]) and (not coda or inv[coda].coda_allowed)
             else ("unresolved:implicit-vowel" if not v.get("resolved", v["explicit"]) else
                   ("invalid:coda-not-licensed" if coda else "unresolved:unresolved-vowel"))))
    if coda:live_dead="dead" if coda_ipa in SHORT_CODA else ("live" if coda_ipa in SONORANT_CODA else None)
    else:live_dead=None if not v["explicit"] else ("live" if v.get("terminal_glide") or v["ipa"].endswith(("m","j","w","ŋ")) else ("dead" if v["length"]=="short" else "live"))
    if len(onset)>=2:
        second_ipa=inv[onset[1]].onset_ipa
        tone_class=first.class_ if second_ipa in {"m","n","ŋ","j","w","r","l"} else inv[onset[1]].class_
    else:tone_class=first.class_
    if not v["explicit"] and not v.get("resolved", False):
        warnings.append("Implicit vowel could not be resolved without lexical or morphological evidence.")
    elif not v["explicit"] and v.get("resolved"):
        warnings.append("Closed-syllable inherent /o/ resolved structurally; this is not lexical word segmentation.")
    if "์" in s:warnings.append("Thanthakhat/silent-mark construction detected; lexical parsing required.")
    if "ห" in s and len(cs)>1 and cs[0]=="ห":warnings.append("ห นำ construction detected; class-changing analysis required.")
    if "รร" in s:warnings.append("รร construction detected; contextual interpretation required.")
    return SyllableAnalysis(input=syllable,normalized=s,grapheme_order=[x["char"] for x in decompose_thai(s)],
        onset=onset,onset_class=first.class_,tone_class=tone_class,vowel=v["ipa"],vowel_id=v["id"],vowel_length=v["length"],
        coda=coda,coda_ipa=coda_ipa,tone_mark=tone_mark(s),live_dead=live_dead,warnings=warnings,status=status,
        orthographic_interpretations=interpretations)
