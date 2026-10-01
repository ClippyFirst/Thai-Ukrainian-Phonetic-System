from __future__ import annotations
import unicodedata

TONE_MARKS={"่":"mai_ek","้":"mai_tho","๊":"mai_tri","๋":"mai_chattawa"}
TONE_CHARS=set(TONE_MARKS)
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
SIGNATURES={
"ะ":("a","short","V-11"),"า":("aː","long","V-12"),
"ิ":("i","short","V-01"),"ี":("iː","long","V-02"),
"ึ":("ɯ","short","V-07"),"ื":("ɯː","long","V-08"),
"ุ":("u","short","V-13"),"ู":("uː","long","V-14"),
"เ":("eː","long","V-04"),"แ":("ɛː","long","V-06"),"โ":("oː","long","V-16"),
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

def detect_vowel(text:str):
    s=_clean(text)
    for pattern in sorted(VOWEL_SIGNATURES,key=len,reverse=True):
        if pattern in s:
            ipa,length,vid=VOWEL_SIGNATURES[pattern]
            return {"pattern":pattern,"ipa":ipa,"length":length,"id":vid,"explicit":True}
    for pattern in sorted(SIGNATURES,key=len,reverse=True):
        if pattern in s:
            ipa,length,vid=SIGNATURES[pattern]
            return {"pattern":pattern,"ipa":ipa,"length":length,"id":vid,"explicit":True}
    return {"pattern":"∅","ipa":"a","length":"short","id":"V-11","explicit":False}
