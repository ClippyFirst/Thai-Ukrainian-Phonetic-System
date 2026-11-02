from scripts.run_source_attested_ipa_diagnostic import summarize_results


def test_independent_comparison_denominator_excludes_withheld_non_circular_rows():
    rows = [
        {"circular_source_override": True, "engine_segmental_ipa": "a", "segmental_match": None, "tone_match": None},
        {"circular_source_override": False, "engine_segmental_ipa": "b", "segmental_match": True, "tone_match": True},
        {"circular_source_override": False, "engine_segmental_ipa": None, "segmental_match": None, "tone_match": None},
        {"circular_source_override": True, "engine_segmental_ipa": None, "segmental_match": None, "tone_match": None},
    ]
    summary = summarize_results(rows)
    assert summary["source_records"] == 4
    assert summary["complete_engine_outputs"] == 2
    assert summary["withheld_or_incomplete"] == 2
    assert summary["source_override_circular_count"] == 2
    assert summary["independently_comparable_records"] == 1
    assert summary["segmental_agreements"] == 1
    assert summary["tone_agreements"] == 1
    assert summary["accuracy_claimed"] is False
