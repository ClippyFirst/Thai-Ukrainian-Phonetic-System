"""Smoke-test runtime data access from an installed wheel, outside the source checkout."""
from __future__ import annotations

from importlib.metadata import version

from thai_ukrainian.api import analyze_syllable
from thai_ukrainian.inventory import load_consonants
from thai_ukrainian.lexical_ipa import load_lexical_ipa_overrides
from thai_ukrainian.orthographic_rules import load_orthographic_rules
from thai_ukrainian.segmentation import load_word_dictionary
from thai_ukrainian.special import load_special_rules
from thai_ukrainian.text import LEXICON
from thai_ukrainian.validator import validate_repository


def main() -> None:
    assert version("thai-ukrainian-phonetic-system")
    assert len(load_consonants()) == 44
    assert len(load_word_dictionary()) == 60963
    assert "ทราม" in LEXICON
    assert "ทราม" in load_lexical_ipa_overrides()
    assert load_orthographic_rules()
    assert load_special_rules()
    assert analyze_syllable("กา").status == "analyzed"
    assert validate_repository()["status"] == "structural-pass"
    print("wheel runtime data smoke: OK")


if __name__ == "__main__":
    main()
