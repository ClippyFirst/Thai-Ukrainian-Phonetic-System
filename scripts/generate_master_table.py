from __future__ import annotations

import csv
import json
from pathlib import Path

from thai_ukrainian.api import analyze_syllable
from thai_ukrainian.ua_orthography import candidates_for_ipa

ROOT = Path(__file__).resolve().parents[1]
THAI = ROOT / "data" / "thai"
OUT = ROOT / "data" / "derived"

MARKS = {"": None, "่": "mai_ek", "้": "mai_tho", "๊": "mai_tri", "๋": "mai_chattawa"}
PREPOSED = ("เ", "แ", "โ", "ใ", "ไ")


def rows(name: str):
    with (THAI / name).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def surface_for(onset: str, vowel: dict[str, str], coda: str | None, mark: str) -> str:
    """Generate one deterministic Thai orthographic surface for a registry row.

    This is a structural constructor, not a claim that the resulting string is
    a lexical Thai syllable. Every generated surface is subsequently re-parsed
    by the research pipeline; mismatches are retained as explicit statuses.
    """
    p, vid = vowel["orthographic_pattern"], vowel["id"]
    special = {
        "V-X-AI": "ไ"+onset, "V-X-AM": onset+"ำ",
        "V-X-AJ": onset+"าย", "V-X-AW": onset+"าว",
        "V-X-IW": onset+"ิว", "V-X-UJ": onset+"ุย",
        "V-X-EW": "เ"+onset+"็ว", "V-X-EW-L": "เ"+onset+"ว",
        "V-X-EAW": "แ"+onset+"ว", "V-X-EY": "เ"+onset+"ย",
        "V-X-OY": onset+"อย", "V-X-OJ": "โ"+onset+"ย",
        "V-X-AW-S": "เ"+onset+"า", "V-X-IAW": "เ"+onset+"ียว",
        "V-X-UAJ": onset+"ัวย", "V-X-UEY": onset+"ือย",
    }
    if vid in special:
        base = special[vid]
    elif "อ" in p:
        base = p.replace("อ", onset, 1).replace("-", "")
    else:
        base = onset + p.replace("-", "")

    # Tone marks are written after the onset consonant, even when the vowel
    # glyph is preposed. This preserves Thai orthographic order.
    insert_at = len(onset) + (1 if base.startswith(PREPOSED) else 0)
    if mark:
        base = base[:insert_at] + mark + base[insert_at:]
    return base + (coda["grapheme"] if coda else "")


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
    candidates = candidates_for_ipa(ipa, limit=1)
    return candidates[0] if candidates else ""


def classify_analysis(a, intended_ipa: str, intended_tone: str | None) -> str:
    """Classify the generated row without hiding parser disagreement."""
    if a.status.startswith("unresolved:"):
        return a.status
    if a.status.startswith("invalid:"):
        return a.status
    if a.status.startswith("analysis-dependent:"):
        return a.status
    if a.phonemic_ipa != intended_ipa:
        return "generation-mismatch:ipa"
    if intended_tone and (a.tone is None or a.tone.tone != intended_tone):
        return "generation-mismatch:tone"
    if not a.phonemic_ipa:
        return "unresolved:no-ipa"
    return "analyzed"


def build():
    cons, vows, rules = rows("consonants.csv"), rows("vowels.csv"), rows("tone_rules.csv")
    initials = [r for r in cons if r["onset_ipa"]]
    codas = [r for r in cons if r["coda_allowed"].strip().lower() == "true"]

    OUT.mkdir(parents=True, exist_ok=True)
    rich_path = OUT / "thai_ukrainian_master.csv"
    simple_path = OUT / "thai_ukrainian_master_2col.csv"

    count = 0
    status_counts: dict[str, int] = {}

    with rich_path.open("w", encoding="utf-8", newline="") as f, simple_path.open("w", encoding="utf-8", newline="") as g:
        w, s = csv.writer(f), csv.writer(g)
        w.writerow([
            "thai", "thai_type", "onset_grapheme", "vowel_id", "coda_grapheme",
            "tone_mark", "tone", "tone_ipa", "ipa", "ukrainian",
            "analysis_status", "attestation_status", "source_basis"
        ])
        s.writerow(["Thai", "Ukrainian"])

        for c in initials:
            for v in vows:
                for coda in [None] + codas:
                    for mark_char, mark_id in MARKS.items():
                        ld = live_dead(v, coda)
                        tone = tone_for(rules, c["class"], ld, v["length"], mark_id)
                        ipa = c["onset_ipa"] + v["ipa"] + (coda["coda_ipa"] if coda else "")
                        thai = surface_for(c["grapheme"], v, coda, mark_char)

                        analysis = analyze_syllable(thai)
                        status = classify_analysis(analysis, ipa, tone["tone"] if tone else None)
                        ua = ua_from_ipa(analysis.phonemic_ipa) if analysis.phonemic_ipa else ""

                        status_counts[status] = status_counts.get(status, 0) + 1
                        w.writerow([
                            thai, "structural_syllable", c["grapheme"], v["id"],
                            coda["grapheme"] if coda else "", mark_id or "",
                            tone["tone"] if tone else "", tone["contour_ipa"] if tone else "",
                            analysis.phonemic_ipa or ipa, ua, status,
                            "not_evaluated_lexically_or_corpus",
                            "machine-declared registry → structural constructor → parser/IPA revalidation"
                        ])
                        s.writerow([thai, ua])
                        count += 1

    expected = len(initials) * len(vows) * (1 + len(codas)) * len(MARKS)
    manifest = {
        "rows": count,
        "expected_rows": expected,
        "initial_graphemes": len(initials),
        "vowel_records": len(vows),
        "coda_graphemes": len(codas),
        "tone_mark_states": len(MARKS),
        "structural_upper_bound": expected,
        "principle": "IPA-first / ИРА: Thai orthography → graphemic analysis → phonology → tone → surface phonetics → IPA → Ukrainian phonetic target → Ukrainian phonology → Ukrainian orthography",
        "status": "structural-combinatorial-space-with-parser-revalidation",
        "warning": "All rows are exhaustive within the declared structural registry, but are not thereby valid, lexical, corpus-attested or semantically translated Thai.",
        "attestation_status": "not_evaluated_lexically_or_corpus",
        "status_counts": status_counts,
    }
    (OUT / "thai_ukrainian_master.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return manifest


if __name__ == "__main__":
    print(json.dumps(build(), ensure_ascii=False, indent=2))
