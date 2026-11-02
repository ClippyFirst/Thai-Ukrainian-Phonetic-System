#!/usr/bin/env python3
"""Build local blind-review packets from the CCOST controlled monosyllabic word list.

The CCOST source file is supplied by the researcher. Generated files are derived
from CC BY-NC-SA 4.0 material and must retain its non-commercial/share-alike terms.
No pronunciation labels, audio or TextGrid data are created or redistributed.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import unicodedata
from pathlib import Path

from thai_ukrainian.adjudication import PACKET_FIELDS

SOURCE_ID = "CORP-CCOST-WORDLIST"
SOURCE_URL = "https://zenodo.org/records/17366698/files/wordlist.csv?download=1"
SOURCE_LICENSE = "CC-BY-NC-SA-4.0"
SOURCE_ATTRIBUTION = (
    "Pittayaporn et al. (2026), The Chulalongkorn Corpus of Spoken Thai (CCOST), "
    "Zenodo v1.0, DOI 10.5281/zenodo.17366698."
)
ORDER_COLUMNS = ("A", "B", "C", "D")
DEFAULT_EXPECTED_ITEMS = 206


def inspect_wordlist(path: Path, expected_items: int = DEFAULT_EXPECTED_ITEMS) -> dict:
    """Read each order independently and expose duplicates/set differences, never hide them."""
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if tuple(reader.fieldnames or ()) != ORDER_COLUMNS:
            raise ValueError(f"CCOST wordlist must have exactly these columns: {', '.join(ORDER_COLUMNS)}")
        rows = list(reader)

    if len(rows) != expected_items:
        raise ValueError(f"CCOST wordlist must contain exactly {expected_items} data rows; found {len(rows)}")

    orders: dict[str, list[str]] = {column: [] for column in ORDER_COLUMNS}
    for row_number, row in enumerate(rows, start=2):
        for column in ORDER_COLUMNS:
            raw = row.get(column) or ""
            word = unicodedata.normalize("NFC", raw.strip())
            if not word:
                raise ValueError(f"empty CCOST word in column {column}, CSV row {row_number}")
            if any(char.isspace() for char in word):
                raise ValueError(f"controlled word contains whitespace in {column}, CSV row {row_number}")
            orders[column].append(word)

    sets = {column: set(words) for column, words in orders.items()}
    base = sets["A"]
    duplicate_words = {
        column: sorted({word for word in words if words.count(word) > 1})
        for column, words in orders.items()
    }
    missing_from_order = {column: sorted(base - sets[column]) for column in ORDER_COLUMNS}
    extra_in_order = {column: sorted(sets[column] - base) for column in ORDER_COLUMNS}
    no_duplicates = all(len(orders[column]) == len(sets[column]) for column in ORDER_COLUMNS)
    concordant = no_duplicates and all(sets[column] == base for column in ORDER_COLUMNS)
    union = sorted(set().union(*sets.values()))
    return {
        "words": union,
        "order_item_counts": {column: len(orders[column]) for column in ORDER_COLUMNS},
        "order_unique_counts": {column: len(sets[column]) for column in ORDER_COLUMNS},
        "duplicate_words_by_order": duplicate_words,
        "missing_from_order_a_set": missing_from_order,
        "extra_vs_order_a_set": extra_in_order,
        "order_sets_concordant": concordant,
    }


def _challenge_row(index: int, thai: str) -> dict:
    return {
        "id": f"CCOST-WL-{index:03d}",
        "input": thai,
        "stratum": "ccost-controlled-monosyllable",
        "probe": "phonemic-wordlist",
        "orthography_validity": "not_adjudicated",
        "structural_parse_status": "not_adjudicated",
        "lexical_attestation_status": "not_checked",
        "gold_phonemic_ipa": None,
        "gold_broad_surface_ipa": None,
        "gold_tone_category": None,
        "gold_vowel_length": None,
        "gold_syllable_boundaries": None,
        "gold_word_boundaries": None,
        "references": [],
        "adjudication_notes": (
            "CCOST controlled-wordlist input only; pronunciation and segmentation "
            "labels require independent review and are not supplied by this source file."
        ),
    }


def generate_packets(
    wordlist_path: Path,
    output_dir: Path,
    *,
    expected_items: int = DEFAULT_EXPECTED_ITEMS,
) -> dict:
    analysis = inspect_wordlist(wordlist_path, expected_items)
    words = analysis["words"]
    digest = hashlib.sha256(wordlist_path.read_bytes()).hexdigest()
    output_dir.mkdir(parents=True, exist_ok=True)

    challenge_path = output_dir / "ccost-wordlist-challenge.jsonl"
    with challenge_path.open("w", encoding="utf-8", newline="\n") as stream:
        for index, word in enumerate(words, start=1):
            stream.write(json.dumps(_challenge_row(index, word), ensure_ascii=False, separators=(",", ":")) + "\n")

    blind_path = output_dir / "ccost-wordlist-blind.tsv"
    with blind_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=PACKET_FIELDS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for index, word in enumerate(words, start=1):
            row = {field: "" for field in PACKET_FIELDS}
            row["id"] = f"CCOST-WL-{index:03d}"
            row["thai"] = word
            writer.writerow(row)

    concordant = analysis["order_sets_concordant"]
    manifest = {
        "schema_version": "1.0",
        "source_id": SOURCE_ID,
        "source_url": SOURCE_URL,
        "license": SOURCE_LICENSE,
        "attribution": SOURCE_ATTRIBUTION,
        "source_file": wordlist_path.name,
        "source_file_sha256": digest,
        "expected_items_per_order": expected_items,
        "source_orders": list(ORDER_COLUMNS),
        "order_item_counts": analysis["order_item_counts"],
        "order_unique_counts": analysis["order_unique_counts"],
        "duplicate_words_by_order": analysis["duplicate_words_by_order"],
        "missing_from_order_a_set": analysis["missing_from_order_a_set"],
        "extra_vs_order_a_set": analysis["extra_vs_order_a_set"],
        "order_sets_concordant": concordant,
        "unique_prompt_count": len(words),
        "review_layer": "BROAD_PHONEMIC",
        "source_evidence_grade": "TEXT_WORDLIST_ONLY_NOT_PRONUNCIATION_GOLD",
        "gold_status": "UNADJUDICATED",
        "review_packet_status": (
            "BLIND_PACKET_GENERATED_UNADJUDICATED"
            if concordant else "SOURCE_ORDER_DISCREPANCY_REQUIRES_RECONCILIATION"
        ),
        "scoreable": False,
        "license_notice": (
            "This generated review packet is derived from CCOST wordlist material. "
            "Retain CC BY-NC-SA 4.0 attribution and share-alike terms; non-commercial use only."
        ),
        "limitations": [
            "The wordlist supplies Thai prompts only; it contains no IPA, audio, phone labels or tone labels.",
            "Independent qualified reviewers must supply phonemic IPA, syllable boundaries, tone and vowel length.",
            "A set mismatch or within-order duplicate is reported, not silently repaired; reconcile source order discrepancies before freezing the review packet.",
            "This packet cannot support surface/acoustic phonetic claims without separately authorized audio and annotations.",
            "Do not commit generated packets or redistribute them outside the source license terms.",
        ],
        "outputs": [challenge_path.name, blind_path.name],
    }
    manifest_path = output_dir / "ccost-wordlist-manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "items": len(words),
        "source_file_sha256": digest,
        "order_sets_concordant": concordant,
        "status": manifest["review_packet_status"],
        "challenge": str(challenge_path),
        "blind_packet": str(blind_path),
        "manifest": str(manifest_path),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wordlist", type=Path, required=True, help="Researcher-supplied Zenodo wordlist.csv")
    parser.add_argument("--output-dir", type=Path, required=True, help="Local output directory; do not commit generated data")
    args = parser.parse_args()
    print(json.dumps(generate_packets(args.wordlist, args.output_dir), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
