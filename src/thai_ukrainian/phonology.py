from __future__ import annotations
from .models import SyllableAnalysis

ONSET_IPA={
"ก":"k","ข":"kʰ","ฃ":"kʰ","ค":"kʰ","ฅ":"kʰ","ฆ":"kʰ","ง":"ŋ","จ":"tɕ","ฉ":"tɕʰ","ช":"tɕʰ","ซ":"s","ฌ":"tɕʰ","ญ":"j",
"ฎ":"d","ฏ":"t","ฐ":"tʰ","ฑ":"tʰ","ฒ":"tʰ","ณ":"n","ด":"d","ต":"t","ถ":"tʰ","ท":"tʰ","ธ":"tʰ","น":"n",
"บ":"b","ป":"p","ผ":"pʰ","ฝ":"f","พ":"pʰ","ฟ":"f","ภ":"pʰ","ม":"m","ย":"j","ร":"r","ล":"l","ว":"w","ศ":"s","ษ":"s","ส":"s","ห":"h","ฬ":"l","อ":"ʔ","ฮ":"h"}

LOW_SINGLE={"ค","ฅ","ฆ","ง","ช","ซ","ฌ","ญ","ฑ","ฒ","ณ","ท","ธ","น","พ","ฟ","ภ","ม","ย","ร","ล","ว","ฬ","ฮ"}

def effective_onset(a:SyllableAnalysis)->list[str]:
    if len(a.onset)>=2 and a.onset[0]=="ห" and a.onset[1] in LOW_SINGLE:
        a.rules_applied.append("ORTH-H-NAM")
        return [a.onset[1]]
    return a.onset

def phonologize(a:SyllableAnalysis)->SyllableAnalysis:
    onset=effective_onset(a)
    a.phonemic_ipa="".join(ONSET_IPA.get(c,"?") for c in onset)+(a.vowel or "")+(a.coda_ipa or "")
    a.rules_applied.append("PHON-SEGMENTAL-COMPOSITION")
    return a

def surface_phoneticize(a:SyllableAnalysis)->SyllableAnalysis:
    a.phonetic_ipa=a.phonemic_ipa
    a.rules_applied.append("PHON-SURFACE-BROAD-IPA")
    return a
