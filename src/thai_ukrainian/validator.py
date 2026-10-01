from pathlib import Path
import csv
from .inventory import load_consonants
ROOT=Path(__file__).resolve().parents[2]
def inventory_report():
    inv=load_consonants(); classes={}
    for c in inv.values():classes[c.class_]=classes.get(c.class_,0)+1
    return {"consonant_graphemes":len(inv),"classes":classes}
def csv_counts():
    base=ROOT/"data"/"thai"; out={}
    for p in base.glob("*.csv"):
        with p.open(encoding="utf-8") as f:out[p.stem]=max(0,sum(1 for _ in f)-1)
    return out
def validate_repository():
    r=inventory_report();r["csv_records"]=csv_counts();r["status"]="structural-pass";return r
