from __future__ import annotations
from .models import SyllableAnalysis

ONSET_IPA={
"ก":"k","ข":"kʰ","ฃ":"kʰ","ค":"kʰ","ฅ":"kʰ","ฆ":"kʰ","ง":"ŋ","จ":"tɕ","ฉ":"tɕʰ","ช":"tɕʰ","ซ":"s","ฌ":"tɕʰ","ญ":"j",
"ฎ":"d","ฏ":"t","ฐ":"tʰ","ฑ":"tʰ","ฒ":"tʰ","ณ":"n","ด":"d","ต":"t","ถ":"tʰ","ท":"tʰ","ธ":"tʰ","น":"n",
"บ":"b","ป":"p","ผ":"pʰ","ฝ":"f","พ":"pʰ","ฟ":"f","ภ":"pʰ","ม":"m","ย":"j","ร":"r","ล":"l","ว":"w","ศ":"s","ษ":"s","ส":"s","ห":"h","ฬ":"l","อ":"ʔ","ฮ":"h"}

def phonologize(a:SyllableAnalysis)->SyllableAnalysis:
    onset="".join(ONSET_IPA.get(c,"?") for c in a.onset)
    a.phonemic_ipa=onset+(a.vowel or "")+(a.coda_ipa or "")
    a.rules_applied.append("PHON-SEGMENTAL-COMPOSITION")
    return a

def surface_phoneticize(a:SyllableAnalysis)->SyllableAnalysis:
    a.phonetic_ipa=a.phonemic_ipa
    a.rules_applied.append("PHON-SURFACE-BROAD-IPA")
    return a
