"""Validate source scope for Thai special orthography.

The teaching source supports the syllabic/lexical status of these letters; it
does not provide a universal IPA mapping for every word containing them.
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _rows(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_special_vowel_letter_rules_link_to_official_source_without_overclaiming():
    sources = {row["source_id"]: row for row in _rows(ROOT / "data/thai/sources.csv")}
    claims = {row["claim_id"]: row for row in _rows(ROOT / "data/claims.csv")}
    rules = {row["rule_id"]: row for row in _rows(ROOT / "data/thai/special_orthography.csv")}

    source_id = "SRC-OBEC-SPECIAL-VOWELS-2022"
    assert source_id in sources
    source = sources[source_id]
    assert source["url"] == "https://academic.obec.go.th/images/document/1649040986_d_1.pdf"
    assert "p. 5" in source["notes"]
    claim = claims["CLM-SPECIAL-VOWEL-LETTERS"]
    assert claim["status"] == "analysis-dependent"
    assert source_id in claim["evidence_ids"].split(";")

    for rule_id in ("SP-RUE-001", "SP-RUE-LONG-001", "SP-LUE-001", "SP-LUE-LONG-001"):
        rule = rules[rule_id]
        assert rule["analysis_status"] == "analysis-dependent"
        assert source_id in rule["source_ids"].split(";")
        assert "word-level evidence" in rule["notes"]


def test_leading_o_claim_is_scoped_to_the_attested_lexical_family():
    sources = {row["source_id"]: row for row in _rows(ROOT / "data/thai/sources.csv")}
    claims = {row["claim_id"]: row for row in _rows(ROOT / "data/claims.csv")}
    rules = {row["rule_id"]: row for row in _rows(ROOT / "data/thai/special_orthography.csv")}

    source_id = "SRC-OBEC-SPECIAL-VOWELS-2022"
    claim = claims["CLM-O-NAM-LEXICAL"]
    rule = rules["SP-O-NAM-001"]
    assert source_id in sources
    assert claim["status"] == "analysis-dependent"
    assert source_id in claim["evidence_ids"].split(";")
    assert source_id in rule["source_ids"].split(";")
    assert "p. 7" in rule["notes"]
    assert "do not generalize" in rule["notes"]
