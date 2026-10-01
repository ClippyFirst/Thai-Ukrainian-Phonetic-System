from __future__ import annotations
import unicodedata

TONE_MARKS={"่":"mai_ek","้":"mai_tho","๊":"mai_tri","๋":"mai_chattawa"}
TONE_CHARS=set(TONE_MARKS)

# Canonical signatures including the carrier อ.
VOWEL_SIGNATURES={
"อะ":("a","short","V-11"),"อา":("aː","long","V-12"),
"อิ":("i","short","V-01"),"อี":("iː","long","V-02"),
"อึ":("ɯ","short","V-07"),"อือ":("ɯː","long","V-08"),
"อุ":("u","short","V-13"),"อู":("uː","long","V-14"),
"เอะ":("e","short","V-03"),"เอ":("eː","long","V-04"),
"แอะ":("ɛ","short","V-05"),"แอ":("ɛː","long","V-06"),
"เออะ":("ɤ","short","V-09"),"เออ":("ɤː","long","V-10"),
"โอะ":("o","short","V-15"),"โอ":("oː","long","V-16"),
"เอาะ":("ɔ","short","V-17"),"ออ":("ɔː","long","V-18"),
"เอียะ":("ia","short","V-19"),"เอีย":("iaː","long","V-20"),
"เอือะ":("ɯa","short","V-21"),"เอือ":("ɯaː","long","V-22"),
"อัวะ":("ua","short","V-23"),"อัว":("uaː","long","V-24"),
}

# Written-around-the-onset signatures. Thai spelling order is retained as input;
# the value is a phonological nucleus.
SIGN_SEQUENCE_SIGNATURES={
"เอียะ":("ia","short","V-19"),"เอีย":("iaː","long","V-20"),
"เอือะ":("ɯa","short","V-21"),"เอือ":("ɯaː","long","V-22"),
"อัวะ":("ua","short","V-23"),"อัว":("uaː","long","V-24"),
"เ◌ียะ":("ia","short","V-19"),"เ◌ีย":("iaː","long","V-20"),
"เ◌ือะ":("ɯa","short","V-21"),"เ◌ือ":("ɯaː","long","V-22"),
"เ◌ะ":("e","short","V-03"),"เ◌":("eː","long","V-04"),
"แ◌ะ":("ɛ","short","V-05"),"แ◌":("ɛː","long","V-06"),
"เ◌อะ":("ɤ","short","V-09"),"เ◌อ":("ɤː","long","V-10"),
"โ◌ะ":("o","short","V-15"),"โ◌":("oː","long","V-16"),
"เ◌าะ":("ɔ","short","V-17"),"อ◌":("ɔː","long","V-18"),
}

SIGNATURES={
"ะ":("a","short","V-11"),"า":("aː","long","V-12"),
"ิ":("i","short","V-01"),"ี":("iː","long","V-02"),
"ึ":("ɯ","short","V-07"),"ื":("ɯː","long","V-08"),
"ุ":("u","short","V-13"),"ู":("uː","long","V-14"),
"ไ":("ai","long","V-X-AI"),"ใ":("ai","long","V-X-AI"),
"ำ":("am","short","V-X-AM"),"ั":("a","short","V-11"),"็":(None,None,None),
}

def normalize_thai(text:str)->str:
    return unicodedata.normalize("NFC", text.strip())

def decompose_thai(text:str)->list[dict]:
    s=normalize_thai(text)
    return [{"char":c,"codepoint":f"U+{ord(c):04X}","name":unicodedata.name(c,"UNKNOWN"),
             "category":unicodedata.category(c),"index":i} for i,c in enumerate(s)]

def tone_mark(text:str)->str|None:
    return next((TONE_MARKS[c] for c in text if c in TONE_MARKS),None)

def _clean(text:str)->str:
    return "".join(c for c in normalize_thai(text) if c not in TONE_CHARS)

def _without_carrier(s:str)->str:
    return s.replace("อ","")

def detect_vowel(text:str):
    s=_clean(text)
    for pattern in sorted(VOWEL_SIGNATURES,key=len,reverse=True):
        if pattern in s:
            ipa,length,vid=VOWEL_SIGNATURES[pattern]
            return {"pattern":pattern,"ipa":ipa,"length":length,"id":vid,"explicit":True}
    # Surrounding-vowel recognition after removing onset consonants.
    # The signatures are expressed as actual Thai sign sequences.
    x=_without_carrier(s)
    sequence_patterns=[
        ("เ"+"ี"+"ยะ","ia","short","V-19"),
        ("เ"+"ี"+"ย","iaː","long","V-20"),
        ("เ"+"ื"+"อะ","ɯa","short","V-21"),
        ("เ"+"ื"+"อ","ɯaː","long","V-22"),
        ("เ"+"ะ","e","short","V-03"),
        ("เ","eː","long","V-04"),
        ("แ"+"ะ","ɛ","short","V-05"),
        ("แ","ɛː","long","V-06"),
        ("เ"+"อ"+"ะ","ɤ","short","V-09"),
        ("เ"+"อ","ɤː","long","V-10"),
        ("โ"+"ะ","o","short","V-15"),
        ("โ","oː","long","V-16"),
        ("เ"+"า"+"ะ","ɔ","short","V-17"),
        ("เ"+"า","ɔː","long","V-18"),
    ]
    for pat,ipa,length,vid in sequence_patterns:
        if pat in x:return {"pattern":pat,"ipa":ipa,"length":length,"id":vid,"explicit":True}
    # อัว / -ัว can be represented with a carrier or the combining sequence.
    if "ัวะ" in s:return {"pattern":"อัวะ","ipa":"ua","length":"short","id":"V-23","explicit":True}
    if "ัว" in s:return {"pattern":"อัว","ipa":"uaː","length":"long","id":"V-24","explicit":True}
    for pattern in sorted(SIGNATURES,key=len,reverse=True):
        if pattern in s:
            ipa,length,vid=SIGNATURES[pattern]
            return {"pattern":pattern,"ipa":ipa,"length":length,"id":vid,"explicit":True}
    return {"pattern":"∅","ipa":"a","length":"short","id":"V-11","explicit":False}
