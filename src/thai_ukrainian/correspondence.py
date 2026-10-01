from __future__ import annotations
import csv
from pathlib import Path
from .models import Candidate
ROOT=Path(__file__).resolve().parents[2]
UA_VECTORS=ROOT/"data"/"ua_target_vectors.csv"
FEATURES=("consonantal","sonorant","syllabic","voice","continuant","nasal","lateral","rhotic","labial","coronal","dorsal","palatal","palatalized","affricate","aspirated","long")
WEIGHTS={"consonantal":2.0,"sonorant":1.5,"syllabic":1.0,"voice":1.0,"continuant":1.5,"nasal":1.5,"lateral":1.0,"rhotic":1.0,"labial":1.5,"coronal":1.5,"dorsal":1.5,"palatal":2.0,"palatalized":1.5,"affricate":1.5,"aspirated":0.5,"long":0.5}
THAI_FEATURES={
"p":(1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0),"pʰ":(1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0),"b":(1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0),
"t":(1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0),"tʰ":(1,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0),"d":(1,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0),
"k":(1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0),"kʰ":(1,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0),
"tɕ":(1,0,0,0,1,0,0,0,0,1,0,1,0,1,0,0),"tɕʰ":(1,0,0,0,1,0,0,0,0,1,0,1,0,1,1,0),
"m":(1,1,0,1,0,1,0,0,1,0,0,0,0,0,0,0),"n":(1,1,0,1,0,1,0,0,0,1,0,0,0,0,0,0),"ŋ":(1,1,0,1,0,1,0,0,0,0,1,0,0,0,0,0),
"f":(1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0),"s":(1,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0),"h":(1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0),
"w":(1,1,0,1,1,0,0,0,1,0,0,0,0,0,0,0),"j":(1,1,0,1,1,0,0,0,0,0,0,1,0,0,0,0),
"r":(1,1,0,1,1,0,0,1,0,1,0,0,0,0,0,0),"l":(1,1,0,1,1,0,1,0,0,1,0,0,0,0,0,0),
"ʔ":(1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)}

def _rows():
    with UA_VECTORS.open(encoding="utf-8",newline="") as f:return list(csv.DictReader(f))
def _num(x):
    if x in ("","na",None):return None
    return int(x)
def rank_ukrainian_candidates(ipa:str)->list[Candidate]:
    if ipa not in THAI_FEATURES:return [Candidate("UNRESOLVED",ipa,float("inf"),"unresolved",notes="No Thai feature vector.")]
    source=dict(zip(FEATURES,THAI_FEATURES[ipa]));out=[]
    for row in _rows():
        cost=0.0;m=[]
        for f in FEATURES:
            tv=_num(row.get(f))
            if tv is None:continue
            if source[f]!=tv:cost+=WEIGHTS[f];m.append(f)
        out.append(Candidate(row["segment_id"],row["ipa"],cost,"feature-ranked",tuple(m),"Distance is a declared model parameter, not probability."))
    return sorted(out,key=lambda x:(x.distance,x.candidate_id))
def candidates_for(ipa:str,limit:int=10):return rank_ukrainian_candidates(ipa)[:limit]
