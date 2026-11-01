import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "benchmark_ipa.py"
GOLD_FIELDS = [
    "id", "text", "gold_ipa", "gold_status", "profile", "source_id", "source_url",
    "license", "transcription_level", "reviewer_a_id", "reviewer_b_id",
    "reviewer_a_qualification_ref", "reviewer_b_qualification_ref",
    "reviewer_a_ipa", "reviewer_b_ipa", "adjudicator_id", "adjudicator_qualification_ref", "adjudication_outcome",
    "adjudication_record_id", "adjudication_notes",
]
PRED_FIELDS = ["id", "engine", "raw_output", "ipa", "status", "version"]


def write_tsv(path, fields, rows):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def gold_row(**changes):
    row = {
        "id": "a", "text": "กา", "gold_ipa": "kaː", "gold_status": "ADJUDICATED",
        "profile": "core-vowel-length", "source_id": "TEST-IPA-CORP",
        "source_url": "https://example.org/record", "license": "CC0-1.0",
        "transcription_level": "BROAD_PHONEMIC", "reviewer_a_id": "TH-PH-01",
        "reviewer_b_id": "TH-PH-02",
        "reviewer_a_qualification_ref": "qualification:TH-PH-01",
        "reviewer_b_qualification_ref": "qualification:TH-PH-02",
        "reviewer_a_ipa": "kaː", "reviewer_b_ipa": "kaː",
        "adjudicator_id": "TH-ADJ-01", "adjudicator_qualification_ref": "qualification:TH-ADJ-01",
        "adjudication_outcome": "AGREEMENT",
        "adjudication_record_id": "ADJ-2026-001", "adjudication_notes": "Independent labels agree.",
    }
    row.update(changes)
    return row


def prediction_row(**changes):
    row = {
        "id": "a", "engine": "candidate", "raw_output": "kaː", "ipa": "kaː",
        "status": "ok", "version": "1",
    }
    row.update(changes)
    return row


class BenchmarkIpaTests(unittest.TestCase):
    def run_benchmark(self, gold_rows, pred_rows, expected_returncode=0):
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            gold, predictions, output = directory / "gold.tsv", directory / "pred.tsv", directory / "report.json"
            sources, reviewers = directory / "sources.tsv", directory / "reviewers.tsv"
            write_tsv(gold, GOLD_FIELDS, gold_rows)
            write_tsv(predictions, PRED_FIELDS, pred_rows)
            write_tsv(sources,
                ["source_id", "source_url", "license", "allowed_uses", "verification_status", "verified_by", "verified_at", "notes"],
                [{"source_id": "TEST-IPA-CORP", "source_url": "https://example.org/record", "license": "CC0-1.0",
                  "allowed_uses": "IPA_GOLD_INPUT", "verification_status": "VERIFIED", "verified_by": "test",
                  "verified_at": "2026-11-01", "notes": "Unit-test fixture source."}],
            )
            write_tsv(reviewers,
                ["reviewer_id", "language", "roles", "qualification_ref", "verification_status", "verified_by", "verified_at", "scope", "notes"],
                [
                    {"reviewer_id": "TH-PH-01", "language": "th", "roles": "THAI_PHONETICIAN", "qualification_ref": "qualification:TH-PH-01", "verification_status": "VERIFIED", "verified_by": "test", "verified_at": "2026-11-01", "scope": "Thai phonetic transcription", "notes": "Unit-test fixture only."},
                    {"reviewer_id": "TH-PH-02", "language": "th", "roles": "THAI_PHONETICIAN", "qualification_ref": "qualification:TH-PH-02", "verification_status": "VERIFIED", "verified_by": "test", "verified_at": "2026-11-01", "scope": "Thai phonetic transcription", "notes": "Unit-test fixture only."},
                    {"reviewer_id": "TH-ADJ-01", "language": "th", "roles": "THAI_PHONETICIAN_ADJUDICATOR", "qualification_ref": "qualification:TH-ADJ-01", "verification_status": "VERIFIED", "verified_by": "test", "verified_at": "2026-11-01", "scope": "Thai phonetic adjudication", "notes": "Unit-test fixture only."},
                ],
            )
            run = subprocess.run(
                [sys.executable, str(SCRIPT), "--gold", str(gold), "--predictions", str(predictions),
                 "--output", str(output), "--source-registry", str(sources), "--reviewer-registry", str(reviewers)],
                cwd=ROOT, text=True, capture_output=True, check=False,
            )
            self.assertEqual(run.returncode, expected_returncode, msg=run.stderr)
            if expected_returncode:
                return run.stderr
            return json.loads(output.read_text(encoding="utf-8"))

    def test_adjudicated_gold_requires_complete_two_reviewer_provenance(self):
        cases = [
            ({"gold_ipa": ""}, "requires non-empty gold_ipa"),
            ({"source_id": ""}, "source_id"),
            ({"profile": ""}, "profile"),
            ({"reviewer_b_id": "TH-PH-01"}, "two distinct reviewers"),
            ({"reviewer_a_ipa": ""}, "reviewer_a_ipa"),
            ({"reviewer_b_qualification_ref": ""}, "reviewer_b_qualification_ref"),
            ({"source_url": ""}, "source_url"),
        ]
        for changes, message in cases:
            with self.subTest(changes=changes):
                stderr = self.run_benchmark([gold_row(**changes)], [], expected_returncode=1)
                self.assertIn(message, stderr)

    def test_agreement_outcome_requires_matching_independent_labels(self):
        row = gold_row(reviewer_b_ipa="ka")
        stderr = self.run_benchmark([row], [], expected_returncode=1)
        self.assertIn("AGREEMENT requires matching reviewer IPA", stderr)

    def test_resolved_disagreement_requires_different_raw_labels(self):
        row = gold_row(adjudication_outcome="RESOLVED_DISAGREEMENT")
        stderr = self.run_benchmark([row], [], expected_returncode=1)
        self.assertIn("RESOLVED_DISAGREEMENT requires differing reviewer IPA", stderr)

    def test_empty_gold_does_not_report_accuracy(self):
        report = self.run_benchmark([], [prediction_row()])
        self.assertEqual(report["gold"]["accuracy_status"], "NOT_MEASURED")
        metrics = report["engines"]["candidate"]
        self.assertEqual(metrics["n_adjudicated_gold_rows"], 0)
        self.assertIsNone(metrics["exact_match_rate"])
        self.assertEqual(metrics["status"], "NOT_MEASURED_NO_ADJUDICATED_GOLD")

    def test_scores_only_adjudicated_rows_and_preserves_diacritics(self):
        pending = gold_row(
            id="b", text="test", gold_ipa="not-gold", gold_status="PROJECT_PROBE_NOT_GOLD",
            source_id="", source_url="", license="", profile="", transcription_level="",
            reviewer_a_id="", reviewer_b_id="", reviewer_a_ipa="", reviewer_b_ipa="",
            adjudicator_id="", adjudicator_qualification_ref="", adjudication_outcome="", adjudication_record_id="", adjudication_notes="",
        )
        report = self.run_benchmark(
            [gold_row(gold_ipa="aː", reviewer_a_ipa="aː", reviewer_b_ipa="aː"), pending],
            [prediction_row(ipa="aː"), prediction_row(id="b", raw_output="not-gold", ipa="not-gold")],
        )
        metrics = report["engines"]["candidate"]
        self.assertEqual(report["gold"]["rows_adjudicated"], 1)
        self.assertEqual(metrics["n_adjudicated_gold_rows"], 1)
        self.assertEqual(metrics["exact_matches"], 1)
        self.assertEqual(metrics["exact_match_rate"], 1.0)

    def test_missing_prediction_row_remains_in_denominator(self):
        second = gold_row(id="b", text="ปา", gold_ipa="paː", reviewer_a_ipa="paː", reviewer_b_ipa="paː", source_id="TEST-IPA-CORP",
                          source_url="https://example.org/record",
                          adjudication_record_id="ADJ-2026-002")
        metrics = self.run_benchmark([gold_row(), second], [prediction_row()])["engines"]["candidate"]
        self.assertEqual(metrics["n_adjudicated_gold_rows"], 2)
        self.assertEqual(metrics["exact_matches"], 1)
        self.assertEqual(metrics["missing_predictions"], 1)
        self.assertEqual(metrics["missing_prediction_rate"], 0.5)
        self.assertEqual(metrics["rows"][1]["status"], "MISSING_ROW")


    def test_benchmark_rejects_mixed_phonemic_and_surface_gold(self):
        surface = gold_row(
            id="b", text="กา", source_id="TEST-IPA-CORP",
            source_url="https://example.org/record",
            transcription_level="BROAD_SURFACE",
            adjudication_record_id="ADJ-2026-002",
        )
        stderr = self.run_benchmark([gold_row(), surface], [], expected_returncode=1)
        self.assertIn("one benchmark run must use one transcription_level", stderr)

    def test_report_stratifies_metrics_by_profile(self):
        second = gold_row(
            id="b", text="ปา", gold_ipa="paː", reviewer_a_ipa="paː", reviewer_b_ipa="paː", profile="core-onset",
            source_id="TEST-IPA-CORP",
            adjudication_record_id="ADJ-2026-002",
        )
        report = self.run_benchmark([gold_row(), second], [prediction_row()])
        profiles = report["engines"]["candidate"]["by_profile"]
        self.assertEqual(profiles["core-vowel-length"]["n"], 1)
        self.assertEqual(profiles["core-onset"]["n"], 1)
        self.assertEqual(profiles["core-onset"]["missing_predictions"], 1)

    def test_mismatch_reports_codepoint_cer(self):
        metrics = self.run_benchmark([gold_row(gold_ipa="k", reviewer_a_ipa="k", reviewer_b_ipa="k")],
                                     [prediction_row(raw_output="g", ipa="g")])["engines"]["candidate"]
        self.assertEqual(metrics["exact_matches"], 0)
        self.assertEqual(metrics["codepoint_cer"], 1.0)


if __name__ == "__main__":
    unittest.main()
