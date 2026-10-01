from __future__ import annotations
import csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def rows(name):
    with (ROOT/"data"/"thai"/name).open(encoding="utf-8") as f:return list(csv.DictReader(f))
cons=rows("consonants.csv"); vows=rows("vowels.csv")
initials=[r for r in cons if r["onset_ipa"]]
codas=[r for r in cons if r["coda_allowed"]]
marks=[None,"mai_ek","mai_tho","mai_tri","mai_chattawa"]
# This is a structural upper bound, not a lexicon.
structural=len(initials)*len(vows)*len(codas)*len(marks)
open_space=len(initials)*len(vows)*len(marks)
report={
"initial_grapheme_options":len(initials),
"vowel_records":len(vows),
"coda_grapheme_options":len(codas),
"tone_mark_states":len(marks),
"open_syllable_structural_upper_bound":open_space,
"closed_syllable_structural_upper_bound":structural,
"combined_upper_bound":open_space+structural,
"status":"structural-combinatorial-space",
"warning":"Counts do not mean orthographic validity, phonotactic validity, lexical attestation, or corpus attestation."
}
out=ROOT/"docs"/"syllable-space.json"
out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(report,ensure_ascii=False,indent=2))
