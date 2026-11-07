#!/usr/bin/env python3
"""Compare the browser RTGS port with pinned PyThaiNLP 5.4.0.

The per-token checks verify implementation parity, not linguistic correctness.
The end-to-end checks additionally compare the browser's full newmm tokenizer
against PyThaiNLP using the same pinned CC0 dictionary. Neither comparator is
an independently adjudicated RTGS gold set.
"""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

os.environ.setdefault("PYTHAINLP_OFFLINE", "1")
from pythainlp.tokenize import word_tokenize
from pythainlp.transliterate.royin import _romanize, _should_add_syllable_separator
from pythainlp.util import Trie

ROOT = Path(__file__).resolve().parents[1]
ORTHOGRAPHIC_CORRECTIONS = {"ใหม่": "mai", "ไหม": "mai", "เหงา": "ngao", "ให้": "hai", "ใกล้": "klai", "ใคร": "khrai", "จริง": "ching", "สามารถ": "samat", "สวัสดี": "sawatdi", "สร้าง": "sang", "ศรี": "si", "เศร้า": "sao", "ไซร้": "sai", "ทรง": "song", "ทราม": "sam", "พัฒนา": "phatthana", "ฤทธิ์": "rit", "ฤๅ": "rue", "รถไฟ": "rotfai", "ผลไม้": "phonlamai", "ยูเครน": "yukhren", "ทราบ": "sap", "ทรัพย์": "sap", "แทรก": "saek", "อักษร": "akson"}
CORPUS = ROOT / "docs" / "research" / "rtgs-parity-corpus.json"
DICTIONARY = ROOT / "data" / "thai" / "words_th_cc0.txt"
NODE = r"""
import { readFile } from 'node:fs/promises';
import { romanizeRtgsWord, romanizeRtgsWords } from './web/src/rtgs-reference.js';
import { romanizeRtgsTokenSequence } from './web/src/rtgs-phonological.js';
import { createFastThaiG2PNativeTokenizer } from './web/src/fastthaig2p-tokenizer.js';
let input = '';
for await (const chunk of process.stdin) input += chunk;
const corpus = JSON.parse(input);
const words = (await readFile('data/thai/words_th_cc0.txt', 'utf8')).split(/\r?\n/u).filter(Boolean);
const tokenizer = createFastThaiG2PNativeTokenizer(words);
const result = {
  words: corpus.words.map(word => romanizeRtgsWord(word).value),
  sequences: corpus.sequences.map(words => romanizeRtgsWords(words)),
  unsupported: (corpus.unsupported || []).map(word => ({ word, status: romanizeRtgsWord(word).status })),
  texts: (corpus.text_inputs || []).map(text => {
    const tokens = tokenizer.tokenize(text);
    const result = romanizeRtgsTokenSequence(tokens.map(value => ({
      input: value, kind: /[\u0E00-\u0E7F]/u.test(value) ? "thai" : "other"
    })));
    return { tokens, romanized: result.output };
  }),
  official: (corpus.official_examples || []).map(({ input }) => {
    const tokens = tokenizer.tokenize(input);
    const result = romanizeRtgsTokenSequence(tokens.map(value => ({
      input: value, kind: /[\u0E00-\u0E7F]/u.test(value) ? "thai" : "other"
    })));
    return { input, tokens, romanized: result.output };
  })
};
process.stdout.write(JSON.stringify(result));
"""

def romanize_reference_tokens(words: list[str]) -> str:
    output: list[str] = []
    for index, word in enumerate(words):
        romanized = _romanize(word)
        if index > 0 and romanized:
            previous = output[-1] if output else ""
            if _should_add_syllable_separator(words[index - 1], word, previous):
                romanized = "a" + romanized
        output.append(romanized)
    return "".join(output)


def main() -> int:
    corpus = json.loads(CORPUS.read_text(encoding="utf-8"))
    dictionary_words = DICTIONARY.read_text(encoding="utf-8").splitlines()
    reference_dictionary = Trie(dictionary_words)
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
        expected = romanize_reference_tokens(words)
        if got != expected:
            failures.append(f"sequence {words!r}: browser={got!r}; PyThaiNLP={expected!r}")

    text_count = 0
    for text, got in zip(corpus.get("text_inputs", []), actual.get("texts", []), strict=True):
        expected_tokens = word_tokenize(text, engine="newmm", custom_dict=reference_dictionary)
        if got["tokens"] != expected_tokens:
            failures.append(
                f"tokenizer {text!r}: browser={got['tokens']!r}; "
                f"PyThaiNLP newmm={expected_tokens!r}"
            )
            continue
        text_count += 1

    for case, got in zip(corpus.get("official_examples", []), actual.get("official", []), strict=True):
        if got["romanized"] != case["expected"]:
            failures.append(
                f"official RTGS {case['input']!r}: browser={got['romanized']!r}; "
                f"published={case['expected']!r}; tokens={got['tokens']!r}"
            )

    if failures:
        print("RTGS parity / official acceptance FAILED:")
        print("\n".join(failures))
        return 1
    print(
        "RTGS implementation parity PASS: "
        f"{len(corpus['words'])} token inputs, {len(corpus['sequences'])} presegmented sequences, "
        f"{text_count} end-to-end Thai text inputs; PyThaiNLP 5.4.0; "
        f"{len(corpus.get('official_examples', []))} official-standard examples checked."
    )
    print("Tokenizer parity is implementation parity only; official examples are the independent rule-source acceptance gate.")
    if known_divergences:
        print("Documented orthographic corrections (intentional upstream divergences):")
        print("\n".join(known_divergences))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
