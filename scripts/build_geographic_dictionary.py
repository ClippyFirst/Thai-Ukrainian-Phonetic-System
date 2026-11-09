#!/usr/bin/env python3
"""Build a provenance-preserving Thai-text CSV with RTGS and IPA→Ukrainian output.

The internal typed IPA route is preferred. When explicitly enabled, complete
FastThaiG2P external IPA is a provisional fallback and is kept in its own
unclassified IPA column; Ukrainian is still produced only by the IPA adapter.
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

THAI_RANGE = range(0x0E00, 0x0E80)
OUTPUT_FIELDS = (
    "romanization_rtgs",
    "ipa_phonemic",
    "ipa_broad_surface",
    "ipa_external_fastthaig2p",
    "ukrainian_from_ipa",
    "pipeline_status",
    "ipa_source",
    "analysis_confidence",
    "external_g2p_coverage",
    "segmentation_method",
    "pipeline_warnings",
    "romanization_method",
)


def _load_pythainlp() -> tuple[Callable[..., str], Callable[..., list[str]]]:
    try:
        from pythainlp.tokenize import word_tokenize
        from pythainlp.transliterate import romanize
        from pythainlp.util.trie import Trie
        from thai_ukrainian.segmentation import load_word_dictionary
    except ImportError as exc:
        raise RuntimeError(
            "Geographic RTGS output requires PyThaiNLP 5.4.0. "
            "Install with: pip install -e '.[geography]'"
        ) from exc
    dictionary = Trie(load_word_dictionary())

    def tokenize_pinned(text: str, **kwargs: Any) -> list[str]:
        return word_tokenize(text, custom_dict=dictionary, **kwargs)

    return romanize, tokenize_pinned


def _load_external_g2p() -> Any:
    try:
        from thai_ukrainian.fastthaig2p_adapter import FastThaiG2PAdapter
        return FastThaiG2PAdapter()
    except (ImportError, RuntimeError) as exc:
        raise RuntimeError(
            "The provisional external-IPA fallback requires the pinned FastThaiG2P extra. "
            "Install with: pip install -e '.[fastthaig2p]'"
        ) from exc


def _contains_thai(value: str) -> bool:
    return any(ord(char) in THAI_RANGE for char in value)


def romanize_rtgs(
    text: str,
    romanize_fn: Callable[..., str],
    tokenize_fn: Callable[..., list[str]],
) -> str:
    """Apply pinned PyThaiNLP newmm boundaries and royin RTGS per Thai token."""
    if not _contains_thai(text):
        return ""
    tokens = tokenize_fn(text, engine="newmm", keep_whitespace=True)
    output: list[str] = []
    for token in tokens:
        if token.isspace() or not _contains_thai(token):
            output.append(token)
        else:
            output.append(romanize_fn(token, engine="royin"))
    return "".join(output)


def _external_ipa_candidate(thai_name: str, adapter: Any) -> dict[str, str] | None:
    """Return complete provisional external IPA and IPA-adapted Ukrainian only."""
    from thai_ukrainian.ukrainian_adaptation import adapt_phonetic_result

    output = adapter.convert(thai_name)
    if not output.complete_ipa:
        return None
    typed_groups = output.to_phonetic_results()
    ukrainian_words: list[str] = []
    for group in typed_groups:
        parts: list[str] = []
        for typed in group:
            adapted = adapt_phonetic_result(typed)
            if adapted.get("output") is None:
                return None
            parts.append(str(adapted["output"]))
        ukrainian_words.append("".join(parts))
    if not ukrainian_words:
        return None
    coverage = (
        f"dictionary_tokens={output.dictionary_hit_count};"
        f"rule_fallback_tokens={output.oov_rule_fallback_count}"
    )
    warnings = [
        "FastThaiG2P external IPA is not adjudicated as phonemic or broad-surface IPA.",
        "Ukrainian output is a provisional practical adaptation of external IPA, not expert-validated.",
        "Tone and vowel-length distinctions are not fully represented in Ukrainian practical spelling.",
    ]
    return {
        "ipa_external_fastthaig2p": output.raw_ipa,
        "ukrainian_from_ipa": " ".join(ukrainian_words),
        "pipeline_status": "PROVISIONAL_EXTERNAL_IPA_NOT_ADJUDICATED",
        "ipa_source": f"FastThaiG2P@{output.__class__.__module__}; upstream commit pinned in adapter",
        "analysis_confidence": "PROVISIONAL_EXTERNAL_G2P",
        "external_g2p_coverage": coverage,
        "pipeline_warnings": " | ".join(warnings),
    }


def analyze_geographic_name(
    thai_name: str,
    romanize_fn: Callable[..., str],
    tokenize_fn: Callable[..., list[str]],
    external_g2p: Any | None = None,
) -> dict[str, str]:
    from thai_ukrainian.text import analyze_text_with_word_segmentation

    rtgs = romanize_rtgs(thai_name, romanize_fn, tokenize_fn)
    empty = {
        "romanization_rtgs": rtgs,
        "ipa_phonemic": "",
        "ipa_broad_surface": "",
        "ipa_external_fastthaig2p": "",
        "ukrainian_from_ipa": "",
        "pipeline_status": "NO_THAI_INPUT",
        "ipa_source": "",
        "analysis_confidence": "UNRESOLVED",
        "external_g2p_coverage": "",
        "segmentation_method": "",
        "pipeline_warnings": "Input contains no Thai text.",
        "romanization_method": "PyThaiNLP 5.4.0 newmm + royin RTGS",
    }
    if not thai_name.strip() or not _contains_thai(thai_name):
        return empty

    tokens = analyze_text_with_word_segmentation(thai_name)
    thai_tokens = [token for token in tokens if token.get("kind") == "thai"]
    segmentation_methods = sorted({
        str(token.get("word_segmentation_method") or token.get("segmentation_status") or "unknown")
        for token in thai_tokens
    })
    phonemic_words: list[str] = []
    surface_words: list[str] = []
    ukrainian_words: list[str] = []
    warnings: list[str] = []
    complete = bool(thai_tokens)

    for token in thai_tokens:
        if token.get("word_segmentation_complete") is False:
            complete = False
            warnings.extend(token.get("warnings", []))
        syllables = token.get("syllables") or []
        if not syllables:
            complete = False
            warnings.extend(token.get("warnings", []))
            if not token.get("warnings"):
                warnings.append(f"No syllable analysis available for {token.get('input', '')!r}.")
            continue

        phonemic_syllables: list[str] = []
        surface_syllables: list[str] = []
        ukrainian_syllables: list[str] = []
        for syllable in syllables:
            typed = syllable.get("phonetic_result") or {}
            phonemic = typed.get("phonemic_ipa") or syllable.get("phonemic_ipa") or syllable.get("phonetic_ipa")
            surface = typed.get("broad_surface_ipa") or syllable.get("phonetic_ipa")
            ukrainian = syllable.get("ukrainian_transliteration")
            if (
                syllable.get("status") != "analyzed"
                or typed.get("status") not in (None, "SUPPORTED")
                or not phonemic
                or not ukrainian
            ):
                complete = False
                warnings.extend(syllable.get("warnings", []))
                warnings.extend(typed.get("uncertainty", []))
                continue
            phonemic_syllables.append(str(phonemic))
            surface_syllables.append(str(surface) if surface else "")
            ukrainian_syllables.append(str(ukrainian))

        if len(phonemic_syllables) != len(syllables):
            complete = False
        else:
            phonemic_words.append(".".join(phonemic_syllables))
            surface_words.append(".".join(surface_syllables))
            ukrainian_words.append("".join(ukrainian_syllables))

    if complete and len(phonemic_words) == len(thai_tokens):
        return {
            "romanization_rtgs": rtgs,
            "ipa_phonemic": " ".join(phonemic_words),
            "ipa_broad_surface": " ".join(surface_words) if all(surface_words) else "",
            "ipa_external_fastthaig2p": "",
            "ukrainian_from_ipa": " ".join(ukrainian_words),
            "pipeline_status": "COMPLETE_MODEL_OUTPUT_NOT_ADJUDICATED",
            "ipa_source": "ClippyFirst typed phonemic IPA",
            "analysis_confidence": "MODEL_NOT_INDEPENDENTLY_ADJUDICATED",
            "external_g2p_coverage": "",
            "segmentation_method": "; ".join(segmentation_methods),
            "pipeline_warnings": " | ".join(dict.fromkeys(str(x) for x in warnings if x)),
            "romanization_method": "PyThaiNLP 5.4.0 newmm + royin RTGS",
        }

    if external_g2p is not None:
        try:
            fallback = _external_ipa_candidate(thai_name, external_g2p)
        except Exception as exc:  # retain a per-row diagnostic; continue the batch
            fallback = None
            warnings.append(f"FastThaiG2P fallback failed: {type(exc).__name__}: {exc}")
        if fallback is not None:
            return {
                **empty,
                "romanization_rtgs": rtgs,
                **fallback,
                "segmentation_method": "; ".join(segmentation_methods),
                "romanization_method": "PyThaiNLP 5.4.0 newmm + royin RTGS",
            }

    if not warnings:
        warnings.append("One or more Thai words could not be fully analyzed; IPA and Ukrainian output withheld.")
    return {
        **empty,
        "romanization_rtgs": rtgs,
        "pipeline_status": "PARTIAL_OR_UNSUPPORTED_WITHHELD",
        "ipa_source": "",
        "analysis_confidence": "UNRESOLVED",
        "segmentation_method": "; ".join(segmentation_methods),
        "pipeline_warnings": " | ".join(dict.fromkeys(str(x) for x in warnings if x)),
        "romanization_method": "PyThaiNLP 5.4.0 newmm + royin RTGS",
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Add RTGS, typed IPA and IPA-derived Ukrainian output to a Thai geographic-name CSV."
    )
    parser.add_argument("input", type=Path, help="Input CSV with a header row.")
    parser.add_argument("-o", "--output", type=Path, required=True, help="Output CSV path.")
    parser.add_argument("--thai-column", default="name_th", help="Thai-name input column (default: name_th).")
    parser.add_argument("--delimiter", default=",", help="One-character CSV delimiter.")
    parser.add_argument("--limit", type=int, default=0, help="Optional maximum rows to process (0 = all).")
    parser.add_argument(
        "--external-g2p", action="store_true",
        help="Use pinned FastThaiG2P as a clearly labelled provisional external-IPA fallback.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if len(args.delimiter) != 1:
        raise SystemExit("--delimiter must be exactly one character.")
    if args.limit < 0:
        raise SystemExit("--limit cannot be negative.")
    if args.input.resolve() == args.output.resolve():
        raise SystemExit("Input and output paths must be different; source data is never overwritten.")
    romanize_fn, tokenize_fn = _load_pythainlp()
    external_g2p = _load_external_g2p() if args.external_g2p else None

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.input.open("r", encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source, delimiter=args.delimiter)
        if not reader.fieldnames:
            raise SystemExit("Input CSV has no header row.")
        if args.thai_column not in reader.fieldnames:
            raise SystemExit(
                f"Thai-name column {args.thai_column!r} not found. "
                f"Available columns: {', '.join(reader.fieldnames)}"
            )
        fields = list(reader.fieldnames)
        for field in OUTPUT_FIELDS:
            if field not in fields:
                fields.append(field)
        count = 0
        with args.output.open("w", encoding="utf-8-sig", newline="") as target:
            writer = csv.DictWriter(target, fieldnames=fields, delimiter=args.delimiter, extrasaction="ignore")
            writer.writeheader()
            for row in reader:
                if args.limit and count >= args.limit:
                    break
                row.update(analyze_geographic_name(row.get(args.thai_column) or "", romanize_fn, tokenize_fn, external_g2p))
                writer.writerow(row)
                count += 1
    print(f"Processed {count} geographic-name rows -> {args.output}")
    print("RTGS is a separate lossy romanization; Ukrainian output is emitted only from the typed IPA adapter.")
    if external_g2p is not None:
        print("FastThaiG2P fallback is explicitly provisional; its external IPA is not relabelled phonemic or broad-surface.")
    print("Model outputs are not independently adjudicated geographic-name pronunciations.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
