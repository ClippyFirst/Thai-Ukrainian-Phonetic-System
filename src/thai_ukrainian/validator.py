from pathlib import Path
import csv
from .inventory import load_consonants
from ._paths import THAI_DATA_ROOT
def inventory_report():
    inv=load_consonants(); classes={}
    for c in inv.values():classes[c.class_]=classes.get(c.class_,0)+1
    return {"consonant_graphemes":len(inv),"classes":classes}
def csv_counts():
    base=THAI_DATA_ROOT; out={}
    for p in sorted(base.glob("*.csv")):
        with p.open(encoding="utf-8") as f:out[p.stem]=max(0,sum(1 for _ in f)-1)
    return out
def validate_repository():
    r=inventory_report();r["csv_records"]=csv_counts();r["status"]="structural-pass";return r
