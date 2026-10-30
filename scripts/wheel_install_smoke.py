"""Smoke-test runtime data access from an installed wheel, outside the source checkout."""
from __future__ import annotations

from importlib.metadata import version
import json
from pathlib import Path
import subprocess
import sys

from thai_ukrainian.api import analyze_syllable
from thai_ukrainian._paths import DATA_ROOT, THAI_DATA_ROOT, PACKAGE_ROOT
from thai_ukrainian.correspondence import rank_ukrainian_candidates
from thai_ukrainian.source_final import build_manifest
from thai_ukrainian.inventory import load_consonants
from thai_ukrainian.lexical_ipa import load_lexical_ipa_overrides
from thai_ukrainian.orthographic_rules import load_orthographic_rules
from thai_ukrainian.segmentation import load_word_dictionary
from thai_ukrainian.special import load_special_rules
from thai_ukrainian.text import LEXICON
from thai_ukrainian.validator import validate_repository


def main() -> None:
    assert version("thai-ukrainian-phonetic-system")
    assert DATA_ROOT == PACKAGE_ROOT / "_data"
    assert THAI_DATA_ROOT.is_dir()
    assert (THAI_DATA_ROOT / "WORD-SEGMENTATION-DICTIONARY-LICENSE.md").is_file()
    assert (THAI_DATA_ROOT / "TEXT-LEXICON-DATA-LICENSE.md").is_file()
    assert len(load_consonants()) == 44
    assert len(load_word_dictionary()) == 60963
    assert "ทราม" in LEXICON
    assert "เงิน" in load_lexical_ipa_overrides()
    assert load_orthographic_rules()
    assert load_special_rules()
    assert analyze_syllable("กา").status == "analyzed"
    assert validate_repository()["status"] == "structural-pass"
    assert build_manifest()["status"] == "pass"
    assert rank_ukrainian_candidates("pʰ")

    # Exercise the installed console entry point, not just Python imports.
    console = Path(sys.executable).with_name("thai-ua")
    help_result = subprocess.run([str(console), "--help"], check=True, capture_output=True, text=True)
    assert "analyze" in help_result.stdout
    analysis_result = subprocess.run(
        [str(console), "analyze", "กา", "--compact"],
        check=True,
        capture_output=True,
        text=True,
    )
    cli_payload = json.loads(analysis_result.stdout)
    assert cli_payload["input"] == "กา"
    assert cli_payload["analyses"]
    print("wheel runtime data smoke: OK")


if __name__ == "__main__":
    main()
