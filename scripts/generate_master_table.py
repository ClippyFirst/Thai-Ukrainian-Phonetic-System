from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
THAI = ROOT / "data" / "thai"
OUT = ROOT / "data" / "derived"
MARKS = {"": None, "่": "mai_ek", "้": "mai_tho", "๊": "mai_tri", "๋": "mai_chattawa"}

UA_SEGMENTS = {
    "tɕʰ": "ч", "tɕ": "ч", "pʰ": "п", "tʰ": "т", "kʰ": "к",
    "p": "п", "b": "б", "m": "м", "f": "ф", "t": "т", "d": "д",
    "n": "н", "s": "с", "r": "р", "l": "л", "k": "к", "ŋ": "н",
    "h": "х", "w": "в", "j": "й", "ʔ": "",
    "iː": "і", "i": "і", "eː": "е", "e": "е", "ɛː": "е", "ɛ": "е",
    "aː": "а", "a": "а", "uː": "у", "u": "у", "oː": "о", "o": "о",
    "ɔː": "о", "ɔ": "о", "ɯː": "и", "ɯ": "и", "ɤː": "и", "ɤ": "и",
}

def rows(name: str):
    with (THAI / name).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def surface_for(onset: str, vowel: dict[str, str], coda: str | None, mark: str) -> str:
    p = vowel["orthographic_pattern"]
    special = {
        "ไ/ใ": "ไ" + onset, "ำ": onset + "ำ",
        "อ-ย": onset + "าย", "อ-ว": onset + "าว",
        "อิ-ว": onset + "ิว", "อุ-ย": onset + "ุย",
        "เ-็ว": "เ" + onset + "็ว", "เอ-ว": "เ" + onset + "ว",
        "แ-ว": "แ" + onset + "ว", "เ-ย": "เ" + onset + "ย",
        "โ-ย": "โ" + onset + "ย", "เ-า": "เ" + onset + "า",
        "เ-ียว": "เ" + onset + "ียว", "อัว-ย": onset + "ัวย",
        "ือย": onset + "ือย",
    }
    if p in special:
        base = special[p]
    elif "อ" in p:
        base = p.replace("อ", onset, 1).replace("-", "")
    else:
        base = onset + p.replace("-", "")
    chars = list(base)
    insert_at = len(onset) + (1 if base.startswith(("เ", "แ", "โ", "ใ", "ไ")) else 0)
    if mark:
        chars.insert(insert_at, mark)
    if coda:
        chars.append(coda)
    return "".join(chars)

def live_dead(vowel, coda):
    if coda:
        return "dead" if coda["coda_ipa"] in {"p", "t", "k", "ʔ"} else "live"
    return "dead" if vowel["length"] == "short" else "live"

def tone_for(rules, cls, ld, length, mark):
    m = mark or "none"
    for r in rules:
        if r["tone_mark"] != m or r["tone_class"] != cls:
            continue
        if r["live_dead"] not in {"*", ld} or r["vowel_length"] not in {"*", length}:
            continue
        return r
    return None

def ua_from_ipa(ipa: str) -> str:
    keys = sorted(UA_SEGMENTS, key=len, reverse=True)
    out, i = [], 0
    while i < len(ipa):
        for k in keys:
            if ipa.startswith(k, i):
                out.append(UA_SEGMENTS[k])
                i += len(k)
                break
        else:
            return ""
    return "".join(out)

def build():
    cons, vows, rules = rows("consonants.csv"), rows("vowels.csv"), rows("tone_rules.csv")
    initials = [r for r in cons if r["onset_ipa"]]
    codas = [r for r in cons if r["coda_allowed"].strip().lower() == "true"]
    OUT.mkdir(parents=True, exist_ok=True)
    rich_path = OUT / "thai_ukrainian_master.csv"
    simple_path = OUT / "thai_ukrainian_master_2col.csv"
    count, status_counts = 0, {}
    with rich_path.open("w", encoding="utf-8", newline="") as f, simple_path.open("w", encoding="utf-8", newline="") as g:
        w, s = csv.writer(f), csv.writer(g)
        w.writerow(["thai","thai_type","ipa","tone","tone_ipa","tone_mark","ukrainian","status","source_basis"])
        s.writerow(["Thai","Ukrainian"])
        for c in initials:
            for v in vows:
                for coda in [None] + codas:
                    for mark_char, mark_id in MARKS.items():
                        ld = live_dead(v, coda)
                        tone = tone_for(rules, c["class"], ld, v["length"], mark_id)
                        ipa = c["onset_ipa"] + v["ipa"] + (coda["coda_ipa"] if coda else "")
                        status = "tone-resolvable-structural" if tone else "structural-tone-unresolved"
                        status_counts[status] = status_counts.get(status, 0) + 1
                        thai = surface_for(c["grapheme"], v, coda["grapheme"] if coda else None, mark_char)
                        ua = ua_from_ipa(ipa)
                        w.writerow([thai,"structural_syllable",ipa,tone["tone"] if tone else "",tone["contour_ipa"] if tone else "",mark_id or "",ua,status,"44×40×(1+38)×5 structural space; IPA-first"])
                        s.writerow([thai,ua])
                        count += 1
    manifest = {
        "rows": count,
        "expected_rows": len(initials)*len(vows)*(1+len(codas))*len(MARKS),
        "initial_graphemes": len(initials), "vowel_records": len(vows),
        "coda_graphemes": len(codas), "tone_mark_states": len(MARKS),
        "principle": "Thai orthography → phonology → IPA → Ukrainian approximation",
        "status": "structural-combinatorial-space",
        "warning": "Rows are structural combinations, not lexical or corpus-attested Thai syllables. Tone-resolvable only means that the declared tone-rule registry resolves the combination.",
        "status_counts": status_counts,
    }
    (OUT/"thai_ukrainian_master.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return manifest

if __name__ == "__main__":
    print(json.dumps(build(), ensure_ascii=False, indent=2))
