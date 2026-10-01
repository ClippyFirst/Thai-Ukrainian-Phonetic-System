from __future__ import annotations
import unicodedata

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
"ไ":("aj","long","V-X-AI","j"),"ใ":("aj","long","V-X-AI","j"),"ำ":("am","short","V-X-AM",None),"ั":("a","short","V-11",None),
"็":(None,None,None,None),
}

# Common Thai orthographic diphthong/glide patterns. These are kept separate
# from the core JIPA vowel inventory because analyses vary in how they group
# them phonologically.
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
    for pattern in sorted(VOWEL_SIGNATURES,key=len,reverse=True):
        if pattern in s:
            ipa,length,vid=VOWEL_SIGNATURES[pattern]
            return {"pattern":pattern,"ipa":ipa,"length":length,"id":vid,"explicit":True,"terminal_glide":None}
    for pattern,ipa,length,vid,glide in sorted(GLIDE_PATTERNS,key=lambda x:len(x[0]),reverse=True):
        p=pattern.replace("-","")
        if p and p in s:
            return {"pattern":pattern,"ipa":ipa,"length":length,"id":vid,"explicit":True,"terminal_glide":glide}
    x="".join(c for c in s if not (0x0E01<=ord(c)<=0x0E2E))
    sequence_patterns=[
        ("เ"+"ี"+"ยะ","ia","short","V-19"),("เ"+"ี"+"ย","iaː","long","V-20"),
        ("เ"+"ื"+"อะ","ɯa","short","V-21"),("เ"+"ื"+"อ","ɯaː","long","V-22"),
        ("เ"+"ะ","e","short","V-03"),("เ","eː","long","V-04"),("แ"+"ะ","ɛ","short","V-05"),("แ","ɛː","long","V-06"),
        ("เ"+"อ"+"ะ","ɤ","short","V-09"),("เ"+"อ","ɤː","long","V-10"),("โ"+"ะ","o","short","V-15"),("โ","oː","long","V-16"),
        ("เ"+"าะ","ɔ","short","V-17"),("เ"+"า","aw","short","V-X-AW-S"),
    ]
    for pat,ipa,length,vid in sequence_patterns:
        if pat in x:return {"pattern":pat,"ipa":ipa,"length":length,"id":vid,"explicit":True,"terminal_glide":"w" if vid=="V-X-AW-S" else None}
    for pattern in sorted(SIGNATURES,key=len,reverse=True):
        if pattern in s:
            ipa,length,vid,glide=SIGNATURES[pattern]
            return {"pattern":pattern,"ipa":ipa,"length":length,"id":vid,"explicit":True,"terminal_glide":glide}
    return {"pattern":"∅","ipa":"a","length":"short","id":"V-11","explicit":False,"terminal_glide":None}
