#!/usr/bin/env python3
"""Emit deterministic FastThaiG2P → typed IPA → Ukrainian parity fixtures.

This script is intentionally runnable both in CPython and inside Pyodide.
It exercises the same pinned upstream engine and project adapters in both
runtimes; it does not label any output as linguistic gold.
"""
from __future__ import annotations

import json
from typing import Any

from thai_ukrainian.fastthaig2p_adapter import FastThaiG2PAdapter
from thai_ukrainian.ukrainian_adaptation import adapt_phonetic_result

INPUTS = ("กา", "สวน", "กรุงเทพมหานคร", "สวัสดีครับ")


def build_payload() -> dict[str, Any]:
    engine = FastThaiG2PAdapter()
    cases: list[dict[str, Any]] = []
    for text in INPUTS:
        output = engine.convert(text)
        typed_groups = output.to_phonetic_results() if output.complete_ipa else ()
        words: list[dict[str, Any]] = []
        ukrainian_words: list[str] = []
        for word_index, (word_ipa, typed_syllables) in enumerate(
            zip(output.word_groups, typed_groups)
        ):
            syllables: list[dict[str, Any]] = []
            ukrainian_parts: list[str] = []
            for typed in typed_syllables:
                adapted = adapt_phonetic_result(typed)
                syllables.append({
                    "external_ipa": typed.external_ipa,
                    "tone_category": typed.tone_category,
                    "tone_contour_ipa": typed.tone_contour_ipa,
                    "vowel_length": typed.vowel_length,
                    "status": typed.status,
                    "adaptation": adapted,
                })
                ukrainian_parts.append(
                    adapted["output"] if adapted["output"] is not None
                    else "⟦НЕВИЗНАЧЕНО⟧"
                )
            ukrainian_word = "".join(ukrainian_parts)
            ukrainian_words.append(ukrainian_word)
            token = output.token_paths[word_index] if word_index < len(output.token_paths) else None
            words.append({
                "token": token.token if token else None,
                "path": token.path if token else None,
                "ipa": word_ipa,
                "syllables": syllables,
                "ukrainian": ukrainian_word,
            })
        cases.append({
            "input": text,
            "raw_ipa": output.raw_ipa,
            "complete_ipa": output.complete_ipa,
            "word_groups": list(output.word_groups),
            "syllable_ipa": list(output.syllable_ipa),
            "passthrough_text": output.passthrough_text,
            "dictionary_hit_count": output.dictionary_hit_count,
            "oov_rule_fallback_count": output.oov_rule_fallback_count,
            "ukrainian": " ".join(ukrainian_words) if output.complete_ipa else None,
            "words": words,
        })
    return {"upstream_commit": "4e82a291b4cf2876326744c6580121e9986ad354", "cases": cases}


if __name__ == "__main__":
    print(json.dumps(build_payload(), ensure_ascii=False, sort_keys=True, separators=(",", ":")))
