from __future__ import annotations

import csv
import json
from pathlib import Path
from functools import lru_cache

from thai_ukrainian.api import analyze_syllable
from thai_ukrainian.contextual import surface_ipa_for_consonant, vowel_surface_context
from thai_ukrainian.inventory import load_consonants
from thai_ukrainian.ua_orthography import candidates_for_ipa
from thai_ukrainian.orthographic_rules import load_orthographic_rules
from thai_ukrainian.ukrainian_adaptation import adapt_syllable_to_ukrainian

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
        "V-X-UA": onset+"ว",
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
    # Thai ไ/ใ and other registered final-glide rimes are live for tone
    # calculation even where the vowel nucleus itself is short.
    if vowel["id"] in {"V-X-AI", "V-X-AJ", "V-X-AW", "V-X-IW", "V-X-UJ",
                       "V-X-EW", "V-X-EW-L", "V-X-EAW", "V-X-EY",
                       "V-X-OY", "V-X-OJ", "V-X-AW-S", "V-X-IAW",
                       "V-X-UAJ", "V-X-UEY"}:
        return "live"
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


@lru_cache(maxsize=None)
def ua_from_ipa(ipa: str) -> str:
    candidates = candidates_for_ipa(ipa, limit=1)
    return candidates[0] if candidates else ""

def ua_candidates_from_ipa(ipa: str) -> list[str]:
    return candidates_for_ipa(ipa, limit=8) if ipa else []

def _csv_candidates(ipa: str) -> str:
    return "|".join(ua_candidates_from_ipa(ipa))

def generate_grapheme_tables(cons):
    inv = load_consonants()
    with (OUT / "thai_consonant_correspondence.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "grapheme", "role", "syllable_position", "class",
            "phonemic_ipa", "surface_ipa", "coda_allowed",
            "ukrainian_candidates", "selected_ukrainian", "notes",
            "evidence_status"
        ])
        for row in cons:
            c = inv[row["grapheme"]]
            if c.onset_ipa:
                w.writerow([
                    c.grapheme, "onset", "syllable-initial", c.class_,
                    c.onset_ipa, surface_ipa_for_consonant(c, "onset"),
                    str(c.coda_allowed).lower(), _csv_candidates(c.onset_ipa),
                    ua_from_ipa(c.onset_ipa), c.notes, "registry"
                ])
            if c.coda_allowed and c.coda_ipa:
                w.writerow([
                    c.grapheme, "coda", "syllable-final", c.class_,
                    c.coda_ipa, surface_ipa_for_consonant(c, "coda"),
                    str(c.coda_allowed).lower(), _csv_candidates(c.coda_ipa),
                    ua_from_ipa(c.coda_ipa), c.notes, "registry"
                ])

def generate_orthographic_table():
    """Materialize the machine-readable orthographic rule registry for publication."""
    rules = load_orthographic_rules()
    path = OUT / "thai_orthographic_correspondence.csv"
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "rule_id", "pattern", "grapheme", "role",
            "structural_condition", "phonological_action",
            "ukrainian_action", "priority", "evidence_status", "notes"
        ])
        for r in sorted(rules, key=lambda x: (x.priority, x.rule_id)):
            w.writerow([
                r.rule_id, r.pattern, r.grapheme, r.role.value,
                r.structural_condition, r.phonological_action,
                r.ukrainian_action, r.priority, r.evidence_status, r.notes
            ])


def generate_vowel_tables(vows):
    with (OUT / "thai_vowel_correspondence.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "vowel_id", "orthographic_pattern", "kind", "length",
            "syllable_context", "phonemic_ipa", "surface_ipa",
            "ukrainian_candidates", "selected_ukrainian", "status"
        ])
        for v in vows:
            for context in ("open", "closed"):
                ipa = v["ipa"]
                w.writerow([
                    v["id"], v["orthographic_pattern"], v["kind"], v["length"],
                    context, ipa, vowel_surface_context(ipa, context),
                    _csv_candidates(ipa), ua_from_ipa(ipa), v["status"]
                ])


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
    inv = load_consonants()
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
            "thai", "thai_type", "onset_grapheme",
            "onset_position", "onset_phonemic_ipa", "onset_surface_ipa",
            "vowel_id", "vowel_position", "vowel_phonemic_ipa",
            "vowel_surface_ipa", "coda_grapheme", "coda_position",
            "coda_phonemic_ipa", "coda_surface_ipa",
            "tone_mark", "tone", "tone_ipa",
            "constructed_syllable_ipa",
            "syllable_phonemic_ipa", "syllable_surface_ipa",
            "ukrainian", "ukrainian_from_ipa",
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
                        ua = adapt_syllable_to_ukrainian(analysis) or ""
                        onset_phonemic = c["onset_ipa"]
                        onset_surface = onset_phonemic
                        vowel_phonemic = v["ipa"]
                        vowel_surface = vowel_surface_context(v["ipa"], "closed" if coda else "open")
                        coda_phonemic = coda["coda_ipa"] if coda else ""
                        coda_surface = (
                            surface_ipa_for_consonant(inv[coda["grapheme"]], "coda")
                            if coda else ""
                        )

                        actual_phonemic_ipa = analysis.phonemic_ipa or ""
                        actual_surface_ipa = analysis.phonetic_ipa or ""
                        structured_ua = ua
                        ipa_derived_ua = ua_from_ipa(actual_phonemic_ipa)

                        status_counts[status] = status_counts.get(status, 0) + 1
                        w.writerow([
                            thai, "structural_syllable", c["grapheme"],
                            "syllable-initial", onset_phonemic, onset_surface,
                            v["id"], "syllable-nucleus", vowel_phonemic, vowel_surface,
                            coda["grapheme"] if coda else "",
                            "syllable-final" if coda else "none",
                            coda_phonemic, coda_surface,
                            mark_id or "", tone["tone"] if tone else "",
                            tone["contour_ipa"] if tone else "",
                            ipa,
                            actual_phonemic_ipa, actual_surface_ipa,
                            structured_ua, ipa_derived_ua, status,
                            "not_evaluated_lexically_or_corpus",
                            "machine-declared registry → structural constructor → parser/IPA revalidation"
                        ])
                        s.writerow([thai, ua])
                        count += 1

    generate_grapheme_tables(cons)
    generate_vowel_tables(vows)
    generate_orthographic_table()

    expected = len(initials) * len(vows) * (1 + len(codas)) * len(MARKS)
    manifest = {
        "rows": count,
        "expected_rows": expected,
        "initial_graphemes": len(initials),
        "vowel_records": len(vows),
        "coda_graphemes": len(codas),
        "tone_mark_states": len(MARKS),
        "structural_upper_bound": expected,
        "principle": "IPA-first: Thai orthography → structural orthographic analysis → Thai phonology → tone → IPA → Ukrainian phonetic target; IPA is an independent audit/control layer",
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
