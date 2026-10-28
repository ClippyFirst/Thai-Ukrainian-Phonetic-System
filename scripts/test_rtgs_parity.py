#!/usr/bin/env python3
"""Compare the browser RTGS port with pinned PyThaiNLP 5.4.0.

This verifies per-token implementation parity, not tokenizer parity or
linguistic correctness. PyThaiNLP is test-only, never loaded by the website.
"""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

os.environ.setdefault("PYTHAINLP_OFFLINE", "1")
from pythainlp.transliterate.royin import _romanize, _should_add_syllable_separator

ROOT = Path(__file__).resolve().parents[1]
ORTHOGRAPHIC_CORRECTIONS = {"ใหม่": "mai", "ไหม": "mai", "เหงา": "ngao", "ให้": "hai", "ใกล้": "klai", "ใคร": "khrai", "จริง": "ching", "สามารถ": "samat", "สวัสดี": "sawatdi", "สร้าง": "sang", "ศรี": "si", "เศร้า": "sao", "ไซร้": "sai", "ทรง": "song", "ทราม": "sam", "พัฒนา": "phatthana", "ฤทธิ์": "rit", "ฤๅ": "rue", "รถไฟ": "rotfai", "ผลไม้": "phonlamai", "ยูเครน": "yukhren", "ทราบ": "sap", "ทรัพย์": "sap", "แทรก": "saek", "อักษร": "akson"}
CORPUS = ROOT / "docs" / "research" / "rtgs-parity-corpus.json"
NODE = r"""
import { romanizeRtgsWord, romanizeRtgsWords } from './web/src/rtgs-reference.js';
let input = '';
for await (const chunk of process.stdin) input += chunk;
const corpus = JSON.parse(input);
const result = {
  words: corpus.words.map(word => romanizeRtgsWord(word).value),
  sequences: corpus.sequences.map(words => romanizeRtgsWords(words)),
  unsupported: (corpus.unsupported || []).map(word => ({ word, status: romanizeRtgsWord(word).status }))
};
process.stdout.write(JSON.stringify(result));
"""

def main() -> int:
    corpus = json.loads(CORPUS.read_text(encoding="utf-8"))
    run = subprocess.run(
        ["node", "--input-type=module", "-e", NODE],
        input=json.dumps(corpus, ensure_ascii=False),
        text=True,
        capture_output=True,
        cwd=ROOT,
        check=True,
    )
    actual = json.loads(run.stdout)
    failures: list[str] = []
    known_divergences: list[str] = []

    for word, got in zip(corpus["words"], actual["words"], strict=True):
        expected = _romanize(word)
        if word in ORTHOGRAPHIC_CORRECTIONS:
            corrected = ORTHOGRAPHIC_CORRECTIONS[word]
            if got != corrected:
                failures.append(f"orthographic correction {word!r}: browser={got!r}; expected={corrected!r}")
            if expected != corrected:
                known_divergences.append(f"{word}: PyThaiNLP={expected!r}, ClippyFirst={corrected!r}")
        elif got != expected:
            failures.append(f"word {word!r}: browser={got!r}; PyThaiNLP={expected!r}")

    for item in actual.get("unsupported", []):
        if item["status"] != "unavailable":
            failures.append(f"unsupported token {item['word']!r} did not abstain: {item['status']!r}")

    for words, got in zip(corpus["sequences"], actual["sequences"], strict=True):
        expected_parts: list[str] = []
        for i, word in enumerate(words):
            romanized = _romanize(word)
            if i > 0 and romanized:
                previous = expected_parts[-1] if expected_parts else ""
                if _should_add_syllable_separator(words[i - 1], word, previous):
                    romanized = "a" + romanized
            expected_parts.append(romanized)
        expected = "".join(expected_parts)
        if got != expected:
            failures.append(f"sequence {words!r}: browser={got!r}; PyThaiNLP={expected!r}")

    if failures:
        print("RTGS parity FAILED against PyThaiNLP 5.4.0:")
        print("\n".join(failures))
        return 1
    print(
        "RTGS parity PASS: "
        f"{len(corpus['words'])} token inputs and {len(corpus['sequences'])} presegmented sequences; "
        "PyThaiNLP 5.4.0. Tokenizer parity is not tested."
    )
    if known_divergences:
        print("Documented orthographic corrections (intentional upstream divergences):")
        print("\n".join(known_divergences))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
