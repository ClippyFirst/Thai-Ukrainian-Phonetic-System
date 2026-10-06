from __future__ import annotations
import json
from pathlib import Path
from thai_ukrainian.api import analyze_syllable
PROBES=["กา","กาน","กาล","กรา","กล้า","คน","เกะ","เก","เกา","หงา","ไหม","ไหว้"]
def main():
    rows=[]
    for text in PROBES:
        a=analyze_syllable(text)
        rows.append({"input":text,"expected":{"input":text,"status":a.status,"phonemicIpa":a.phonemic_ipa,"phoneticIpa":a.phonetic_ipa,"tone":a.tone.tone if a.tone else None,"toneIpa":a.tone.contour_ipa if a.tone else None,"ukrainian":a.ukrainian_transliteration}})
    Path("web/tests/fixtures.python.json").write_text(json.dumps(rows,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
if __name__=="__main__": main()
