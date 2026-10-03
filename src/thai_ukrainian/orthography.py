from __future__ import annotations
import unicodedata
import re

TONE_MARKS={"่":"mai_ek","้":"mai_tho","๊":"mai_tri","๋":"mai_chattawa"}
TONE_CHARS=set(TONE_MARKS)

VOWEL_SIGNATURES={
"อะ":("a","short","V-11"),"อา":("aː","long","V-12"),"อิ":("i","short","V-01"),"อี":("iː","long","V-02"),
"อึ":("ɯ","short","V-07"),"อือ":("ɯː","long","V-08"),"อุ":("u","short","V-13"),"อู":("uː","long","V-14"),
"เอะ":("e","short","V-03"),"เอ":("eː","long","V-04"),"แอะ":("ɛ","short","V-05"),"แอ":("ɛː","long","V-06"),
"เออะ":("ɤ","short","V-09"),"เออ":("ɤː","long","V-10"),"โอะ":("o","short","V-15"),"โอ":("oː","long","V-16"),
"เอาะ":("ɔ","short","V-17"),"ออ":("ɔː","long","V-18"),"เอียะ":("ia","short","V-19"),"เอีย":("iaː","long","V-20"),
"เอือะ":("ɯa","short","V-21"),"เอือ":("ɯaː","long","V-22"),"อัวะ":("ua","short","V-23"),"อัว":("uaː","long","V-24"),
}

SIGNATURES={
"ะ":("a","short","V-11",None),"า":("aː","long","V-12",None),"ิ":("i","short","V-01",None),"ี":("iː","long","V-02",None),
"ึ":("ɯ","short","V-07",None),"ื":("ɯː","long","V-08",None),"ุ":("u","short","V-13",None),"ู":("uː","long","V-14",None),
"ไ":("aj","short","V-X-AI","j"),"ใ":("aj","short","V-X-AI","j"),"ำ":("am","short","V-X-AM",None),"ั":("a","short","V-11",None),
"็":(None,None,None,None),
}

GLIDE_PATTERNS=[
("าย","aːj","long","V-X-AJ","j"),("าว","aːw","long","V-X-AW","w"),
("ัย","aj","short","V-X-AI","j"),("ัวะ","ua","short","V-23",None),("ัว","uaː","long","V-24",None),
("ิว","iw","short","V-X-IW","w"),("ุย","uj","short","V-X-UJ","j"),
("เ็ว","ew","short","V-X-EW","w"),("เอว","eːw","long","V-X-EW-L","w"),
("แว","ɛːw","long","V-X-EAW","w"),("เอย","ɤːj","long","V-X-EY","j"),
("อย","ɔːj","long","V-X-OY","j"),("โอย","oːj","long","V-X-OJ","j"),
("เ-า","aw","short","V-X-AW-S","w"),
("เ-ียว","iaw","long","V-X-IAW","w"),("วย","uaj","long","V-X-UAJ","j"),("ือย","ɯaj","long","V-X-UEY","j"),
]

# Registered vowel-component consonants. These are consumed structurally
# before generic onset/coda assignment.
NUCLEUS_CONSONANTS={
    "V-X-IAW":["ย","ว"], "V-X-UAJ":["ว","ย"],
    "V-X-AJ":["ย"], "V-X-AW":["ว"], "V-X-IW":["ว"],
    "V-X-UJ":["ย"], "V-X-EW":["ว"], "V-X-EW-L":["ว"],
    "V-X-EAW":["ว"], "V-X-EY":["ย"], "V-X-OY":["ย"],
    "V-X-OJ":["ย"], "V-X-AW-S":["ว"], "V-X-UEY":["ย"],
    "V-X-UA":["ว"],
}

def normalize_thai(text:str)->str:
    return unicodedata.normalize("NFC", text.strip())

def decompose_thai(text:str)->list[dict]:
    s=normalize_thai(text)
    out=[]
    for i,c in enumerate(s):
        role="other"
        if 0x0E01<=ord(c)<=0x0E2E: role="consonant"
        elif c in TONE_CHARS: role="tone_mark"
        elif c in "ะาิีึืุูเแโใไำั็": role="vowel_sign"
        elif c=="์": role="silent_mark"
        out.append({"char":c,"codepoint":f"U+{ord(c):04X}","name":unicodedata.name(c,"UNKNOWN"),
                    "category":unicodedata.category(c),"index":i,"role":role})
    return out

def tone_mark(text:str)->str|None:
    return next((TONE_MARKS[c] for c in text if c in TONE_MARKS),None)

def _clean(text:str)->str:
    return "".join(c for c in normalize_thai(text) if c not in TONE_CHARS)

def detect_vowel(text:str):
    s=_clean(text)
    consonants = "กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬอฮ"
    c = f"[{re.escape(consonants)}]"

    # Composite post-consonant constructions containing อ must be resolved
    # before generic single-sign detection. In these forms อ is a vowel
    # component/length carrier, not an independent /ʔ/.
    composite_patterns=[
        (rf"{c}ือ","ɯː","long","V-08",""),
        (rf"{c}อ","ɔː","long","V-18",""),
    ]

    sequence_patterns=[
        (rf"เ{c}ย","ɤːj","long","V-X-EY"),
        (rf"โ{c}ย","oːj","long","V-X-OJ"),
        (rf"เ{c}ือย","ɯaj","long","V-X-UEY"), (rf"เ{c}อย","ɤːj","long","V-X-EY"),
        (rf"โ{c}อย","oːj","long","V-X-OJ"), (rf"เ{c}ียว","iaw","long","V-X-IAW"),
        (rf"เ{c}็ว","ew","short","V-X-EW"), (rf"เ{c}ว","eːw","long","V-X-EW-L"),
        (rf"แ{c}ว","ɛːw","long","V-X-EAW"), (rf"เ{c}ียะ","ia","short","V-19"),
        (rf"เ{c}ีย","iaː","long","V-20"), (rf"เ{c}ือะ","ɯa","short","V-21"),
        (rf"เ{c}ือ","ɯaː","long","V-22"), (rf"เ{c}อะ","ɤ","short","V-09"),
        (rf"เ{c}อ","ɤː","long","V-10"), (rf"เ{c}าะ","ɔ","short","V-17"),
        (rf"เ{c}า","aw","short","V-X-AW-S"), (rf"เ{c}ะ","e","short","V-03"),
        (rf"แ{c}ะ","ɛ","short","V-05"), (rf"แ{c}","ɛː","long","V-06"),
        (rf"โ{c}ะ","o","short","V-15"), (rf"โ{c}","oː","long","V-16"),
        (rf"เ{c}","eː","long","V-04"),
    ]

    # Standalone ไอ/ใอ uses อ as the carrier; it must not be reinterpreted
    # as a final consonant.
    if s in {"ไอ","ใอ"}:
        return {"pattern":s,"ipa":"aj","length":"short","id":"V-X-AI","explicit":True,
                "terminal_glide":"j","matched_text":s,"nucleus_consonants":["อ"]}

    for pattern,ipa,length,vid in sequence_patterns:
        m=re.search(pattern,s)
        if m:
            return {"pattern":pattern,"ipa":ipa,"length":length,"id":vid,"explicit":True,
                    "terminal_glide":("j" if vid in {"V-19","V-20","V-X-UEY","V-X-EY","V-X-OJ"} else ("w" if vid in {"V-X-AW-S","V-X-IAW","V-X-EW","V-X-EW-L","V-X-EAW"} else None)),
                    "matched_text":m.group(0)}

    for pattern,ipa,length,vid,_ in composite_patterns:
        m=re.search(pattern,s)
        if m:
            return {"pattern":pattern,"ipa":ipa,"length":length,"id":vid,
                    "explicit":True,"terminal_glide":None,"matched_text":m.group(0),
                    "nucleus_consonants":["อ"]}

    for pattern in sorted(VOWEL_SIGNATURES,key=len,reverse=True):
        if pattern in s:
            ipa,length,vid=VOWEL_SIGNATURES[pattern]
            return {"pattern":pattern,"ipa":ipa,"length":length,"id":vid,"explicit":True,"terminal_glide":None,"matched_text":pattern}

    # Reduced อัว written as -ว-: the ว is a vowel component when it sits
    # between the onset and a licensed coda in a syllable with no written
    # vowel sign.
    cs=[ch for ch in s if ch in consonants]
    if len(cs)==3 and cs[1]=="ว":
        return {"pattern":"-ว-","ipa":"uaː","length":"long","id":"V-X-UA",
                "explicit":True,"terminal_glide":None,"matched_text":"",
                "nucleus_consonants":["ว"]}

    for pattern,ipa,length,vid,glide in sorted(GLIDE_PATTERNS,key=lambda x:len(x[0]),reverse=True):
        p=pattern.replace("-","")
        if p and p in s:
            return {"pattern":pattern,"ipa":ipa,"length":length,"id":vid,
                    "explicit":True,"terminal_glide":glide,
                    "nucleus_consonants":NUCLEUS_CONSONANTS.get(vid,[]),"matched_text":p}

    for pattern in sorted(SIGNATURES,key=len,reverse=True):
        if pattern in s:
            ipa,length,vid,glide=SIGNATURES[pattern]
            return {"pattern":pattern,"ipa":ipa,"length":length,"id":vid,"explicit":True,"terminal_glide":glide,"matched_text":pattern}

    # Closed inherent /o/ is a structural syllable rule, not a written vowel
    # form. Only resolve it when the supplied surface provides a defensible
    # onset + final structure; do not invent an /a/ for arbitrary consonant
    # strings or perform lexical segmentation.
    if len(cs)==2:
        return {"pattern":"∅-inherent-o","ipa":"o","length":"short","id":"IV-INHERENT-O",
                "explicit":False,"resolved":True,"terminal_glide":None,"matched_text":"",
                "implicit_reason":"two consonants; second may function as coda"}
    if len(cs)==3 and cs[1] in {"ร","ล","ว"}:
        return {"pattern":"∅-inherent-o","ipa":"o","length":"short","id":"IV-INHERENT-O",
                "explicit":False,"resolved":True,"terminal_glide":None,"matched_text":"",
                "implicit_reason":"complex onset plus final; inherent closed-syllable vowel"}

    return {"pattern":"∅","ipa":None,"length":None,"id":None,"explicit":False,"resolved":False,"terminal_glide":None,"matched_text":""}
