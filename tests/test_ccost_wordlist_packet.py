import csv
import json
import tempfile
import unittest
from pathlib import Path

from thai_ukrainian.adjudication import PACKET_FIELDS
from scripts.build_ccost_wordlist_review_packet import generate_packets, inspect_wordlist


def write_wordlist(path, orders):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["A", "B", "C", "D"])
        writer.writeheader()
        for row in zip(*(orders[column] for column in ("A", "B", "C", "D"))):
            writer.writerow(dict(zip(("A", "B", "C", "D"), row)))


class CcostWordlistPacketTests(unittest.TestCase):
    def test_accepts_four_randomized_orders_with_identical_unique_words(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "wordlist.csv"
            words = ["กา", "กะ", "ขา"]
            write_wordlist(path, {
                "A": words,
                "B": ["กะ", "ขา", "กา"],
                "C": ["ขา", "กา", "กะ"],
                "D": ["กา", "ขา", "กะ"],
            })
            result = inspect_wordlist(path, expected_items=3)
            self.assertEqual(result["words"], sorted(words))
            self.assertTrue(result["order_sets_concordant"])
            self.assertEqual(result["order_unique_counts"], {column: 3 for column in "ABCD"})

    def test_reports_duplicates_and_order_set_differences_instead_of_silently_fixing(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "wordlist.csv"
            write_wordlist(path, {
                "A": ["กา", "กะ", "ขา"],
                "B": ["กา", "กะ", "กะ"],
                "C": ["กา", "กะ", "คา"],
                "D": ["กา", "กะ", "ขา"],
            })
            result = inspect_wordlist(path, expected_items=3)
            self.assertFalse(result["order_sets_concordant"])
            self.assertEqual(result["duplicate_words_by_order"]["B"], ["กะ"])
            self.assertEqual(result["missing_from_order_a_set"]["B"], ["ขา"])
            self.assertEqual(result["extra_vs_order_a_set"]["C"], ["คา"])
            self.assertEqual(result["words"], sorted(["กา", "กะ", "ขา", "คา"]))

    def test_identical_sets_with_repeated_items_are_not_declared_concordant(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "wordlist.csv"
            repeated = ["กา", "กะ", "กะ"]
            write_wordlist(path, {column: repeated for column in ("A", "B", "C", "D")})
            result = inspect_wordlist(path, expected_items=3)
            self.assertFalse(result["order_sets_concordant"])
            self.assertEqual(result["duplicate_words_by_order"]["A"], ["กะ"])

    def test_rejects_wrong_item_count_and_whitespace(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "wordlist.csv"
            words = ["กา", "กะ"]
            write_wordlist(path, {column: words for column in ("A", "B", "C", "D")})
            with self.assertRaisesRegex(ValueError, "exactly 3 data rows"):
                inspect_wordlist(path, expected_items=3)
            write_wordlist(path, {
                "A": ["กา", "กะ", "ขา"],
                "B": ["กา", "กะ", "ขา"],
                "C": ["กา", "กะ", "ขา"],
                "D": ["กา", "กะ ขา", "ขา"],
            })
            with self.assertRaisesRegex(ValueError, "contains whitespace"):
                inspect_wordlist(path, expected_items=3)

    def test_generates_candidate_blind_unadjudicated_packets_and_manifest(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "wordlist.csv"
            words = ["กา", "กะ", "ขา"]
            write_wordlist(source, {column: words for column in ("A", "B", "C", "D")})
            out = root / "review"
            result = generate_packets(source, out, expected_items=3)
            challenge = [json.loads(line) for line in (out / "ccost-wordlist-challenge.jsonl").read_text(encoding="utf-8").splitlines()]
            self.assertEqual(len(challenge), 3)
            self.assertTrue(all(row["gold_phonemic_ipa"] is None for row in challenge))
            self.assertEqual([row["input"] for row in challenge], sorted(words))
            with (out / "ccost-wordlist-blind.tsv").open("r", encoding="utf-8", newline="") as stream:
                packet = list(csv.DictReader(stream, delimiter="\t"))
            self.assertEqual(len(packet), 3)
            self.assertEqual(set(packet[0]), set(PACKET_FIELDS))
            self.assertTrue(all(not row["reviewer_id"] and not row["phonemic_ipa"] for row in packet))
            manifest = json.loads((out / "ccost-wordlist-manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["unique_prompt_count"], 3)
            self.assertEqual(manifest["gold_status"], "UNADJUDICATED")
            self.assertEqual(manifest["source_evidence_grade"], "TEXT_WORDLIST_ONLY_NOT_PRONUNCIATION_GOLD")
            self.assertTrue(manifest["scoreable"] is False)
            self.assertEqual(result["status"], "BLIND_PACKET_GENERATED_UNADJUDICATED")


if __name__ == "__main__":
    unittest.main()
