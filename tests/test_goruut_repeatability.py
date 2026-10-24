from scripts.probe_goruut_repeatability import summarize_case


def test_repeatability_reports_distinct_outputs_without_claiming_accuracy():
    case = summarize_case("TH-G2P-001", "กา", [
        {"repeat_index": 1, "phonetic_output": "kaː˧", "error": None},
        {"repeat_index": 2, "phonetic_output": "ka", "error": None},
        {"repeat_index": 3, "phonetic_output": "kaː˧", "error": None},
    ])
    assert case["successful_nonempty_calls"] == 3
    assert case["unique_nonempty_outputs"] == 2
    assert case["varies_across_repetitions"] is True
    assert case["distinct_outputs"] == ["ka", "kaː˧"]
    assert case["status"] == "VARIABLE_OUTPUT"


def test_repeatability_does_not_count_empty_or_failed_outputs_as_success():
    case = summarize_case("TH-G2P-015", "ทฤษฎี", [
        {"repeat_index": 1, "phonetic_output": None, "error": None},
        {"repeat_index": 2, "phonetic_output": None, "error": "RuntimeError"},
    ])
    assert case["successful_nonempty_calls"] == 0
    assert case["unique_nonempty_outputs"] == 0
    assert case["status"] == "NO_NONEMPTY_OUTPUT"
