#!/usr/bin/env python3
"""Train and evaluate a reproducible Thai word-frequency Viterbi segmenter.

Training data is downloaded from the pinned UD Thai TUD train split only.
TUD dev selects the token penalty; TUD test and Wisesight are evaluation-only.
Wisesight is never used to fit or tune the model.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import urllib.request
from collections import Counter
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
SOURCE_REPO = "UniversalDependencies/UD_Thai-TUD"
SOURCE_COMMIT = "67413969add552b7030184f16f24fa9f630913bc"
SOURCE_LICENSE = "CC-BY-SA-4.0"
SOURCE_FILES = {
    "train": ("th_tud-ud-train.conllu", "3e910979f396b4a178b77f02098c4692cb211f95"),
    "dev": ("th_tud-ud-dev.conllu", "8a47a662eae988543f1dae2b99188ee33d81a6b8"),
    "test": ("th_tud-ud-test.conllu", "a6036abfe94f09bd9fdd58ae1fe5913ce31f2ce6"),
}
WIS = ROOT / "data" / "benchmark" / "segmentation-gold.tsv"


def is_thai_word(value: str) -> bool:
    return bool(value) and all("\u0e00" <= ch <= "\u0e7f" for ch in value)


def pinned_download(filename: str, expected_blob: str) -> str:
    url = f"https://raw.githubusercontent.com/{SOURCE_REPO}/{SOURCE_COMMIT}/{filename}"
    request = urllib.request.Request(url, headers={"User-Agent": "ClippyFirst-Thai-Segmenter/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        raw = response.read()
    git_blob = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\\0" + raw).hexdigest()
    if git_blob != expected_blob:
        raise ValueError(f"Pinned TUD blob mismatch for {filename}: {git_blob} != {expected_blob}")
    return raw.decode("utf-8")


def parse_conllu_sentences(content: str) -> list[list[tuple[str, bool]]]:
    """Return integer-ID tokens as (form, no_space_after) pairs."""
    sentences: list[list[tuple[str, bool]]] = []
    current: list[tuple[str, bool]] = []
    for line in content.splitlines() + [""]:
        if not line.strip():
            if current:
                sentences.append(current)
                current = []
            continue
        if line.startswith("#"):
            continue
        fields = line.split("\t")
        if len(fields) != 10 or not fields[0].isdigit():
            continue
        form, misc = fields[1], fields[9]
        current.append((form, "SpaceAfter=No" in misc.split("|")))
    return sentences


def training_counts(sentences: Iterable[list[tuple[str, bool]]]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for sentence in sentences:
        for form, _ in sentence:
            if is_thai_word(form):
                counts[form] += 1
    if not counts:
        raise ValueError("TUD training split produced no Thai word tokens")
    return counts


def evaluation_groups(sentences: Iterable[list[tuple[str, bool]]]) -> list[list[str]]:
    groups: list[list[str]] = []
    for sentence in sentences:
        group: list[str] = []
        previous_no_space = False
        for form, no_space_after in sentence:
            if is_thai_word(form):
                if group and previous_no_space:
                    group.append(form)
                else:
                    if len(group) > 1:
                        groups.append(group)
                    group = [form]
                previous_no_space = no_space_after
            else:
                if len(group) > 1:
                    groups.append(group)
                group = []
                previous_no_space = False
        if len(group) > 1:
            groups.append(group)
    return groups


def segment(text: str, counts: dict[str, int], penalty: float) -> list[str]:
    chars = list(text)
    n = len(chars)
    best = [float("-inf")] * (n + 1)
    next_pos = [0] * (n + 1)
    best[n] = 0.0
    max_len = min(max((len(word) for word in counts), default=1), 24)
    for start in range(n - 1, -1, -1):
        best_score = -25.0 + best[start + 1]
        best_end = start + 1
        for end in range(start + 1, min(n, start + max_len) + 1):
            word = "".join(chars[start:end])
            count = counts.get(word)
            if count is None:
                continue
            score = math.log(count + 0.5) - penalty + best[end]
            if score > best_score:
                best_score, best_end = score, end
        best[start], next_pos[start] = best_score, best_end
    output: list[str] = []
    pos = 0
    while pos < n:
        end = next_pos[pos]
        output.append("".join(chars[pos:end]))
        pos = end
    return output


def boundaries(tokens: list[str]) -> set[int]:
    offsets: set[int] = set()
    pos = 0
    for token in tokens[:-1]:
        pos += len(token)
        offsets.add(pos)
    return offsets


def score_groups(groups: list[list[str]], counts: dict[str, int], penalty: float) -> dict:
    tp = fp = fn = exact = 0
    for gold_tokens in groups:
        text = "".join(gold_tokens)
        pred_tokens = segment(text, counts, penalty)
        gold_b, pred_b = boundaries(gold_tokens), boundaries(pred_tokens)
        tp += len(gold_b & pred_b)
        fp += len(pred_b - gold_b)
        fn += len(gold_b - pred_b)
        exact += int(pred_tokens == gold_tokens)
    precision = tp / (tp + fp) if tp + fp else None
    recall = tp / (tp + fn) if tp + fn else None
    denom = 2 * tp + fp + fn
    return {
        "groups": len(groups), "boundary_tp": tp, "boundary_fp": fp, "boundary_fn": fn,
        "boundary_precision": precision, "boundary_recall": recall,
        "boundary_f1": 2 * tp / denom if denom else None,
        "exact_group_matches": exact,
        "exact_group_rate": exact / len(groups) if groups else None,
    }


def load_wisesight_groups() -> list[list[str]]:
    import csv
    import json as json_module
    with WIS.open("r", encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    if len(rows) != 993:
        raise ValueError(f"Expected 993 pinned Wisesight test rows, got {len(rows)}")
    groups: list[list[str]] = []
    for row in rows:
        if row["gold_status"] != "SOURCE_ANNOTATED" or row["license"] != "CC0-1.0" or row["split"] != "test":
            raise ValueError(f"Unexpected Wisesight evidence grade for {row['id']}")
        tokens = json_module.loads(row["gold_tokens_json"])
        group: list[str] = []
        for token in tokens:
            if is_thai_word(token):
                group.append(token)
            else:
                if len(group) > 1:
                    groups.append(group)
                group = []
        if len(group) > 1:
            groups.append(group)
    return groups


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", type=Path, default=Path("/tmp/thai-tud-word-model.json"))
    parser.add_argument("--report", type=Path, default=Path("/tmp/thai-tud-word-segmentation-report.json"))
    parser.add_argument("--text", help="Segment one Thai text span using an existing model JSON.")
    args = parser.parse_args()

    if args.text is not None:
        model = json.loads(args.model.read_text(encoding="utf-8"))
        print(json.dumps({"input": args.text, "tokens": segment(args.text, model["word_counts"], model["token_penalty"]), "model": model["model_id"]}, ensure_ascii=False))
        return 0

    source = {name: pinned_download(filename, blob) for name, (filename, blob) in SOURCE_FILES.items()}
    train_sentences = parse_conllu_sentences(source["train"])
    dev_sentences = parse_conllu_sentences(source["dev"])
    test_sentences = parse_conllu_sentences(source["test"])
    counts = training_counts(train_sentences)
    dev_groups = evaluation_groups(dev_sentences)
    test_groups = evaluation_groups(test_sentences)
    if not dev_groups or not test_groups:
        raise ValueError("TUD held-out split yielded no Thai no-space token groups")

    # Tune only on the declared TUD development split.
    penalties = [x / 2 for x in range(0, 9)]
    tuning = [(score_groups(dev_groups, counts, penalty), penalty) for penalty in penalties]
    _, best_penalty = max(tuning, key=lambda item: (item[0]["boundary_f1"] or -1, item[0]["exact_group_rate"] or -1, -item[1]))
    model = {
        "schema_version": "1.0",
        "model_id": "clippyfirst-tud-unigram-viterbi-v1",
        "source_repository": SOURCE_REPO,
        "source_commit": SOURCE_COMMIT,
        "source_license": SOURCE_LICENSE,
        "training_split": "TUD train only",
        "development_split": "TUD dev; token penalty selected from fixed grid",
        "test_split": "TUD test; never used for tuning",
        "external_test": "Wisesight 993 source-annotated rows; never used for training or tuning",
        "algorithm": "unigram token-frequency Viterbi over Thai code points; unknown-character fallback is explicit",
        "token_penalty": best_penalty,
        "training_sentences": len(train_sentences),
        "training_vocabulary_size": len(counts),
        "word_counts": dict(sorted(counts.items())),
    }
    args.model.parent.mkdir(parents=True, exist_ok=True)
    args.model.write_text(json.dumps(model, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    report = {
        "schema_version": "1.0",
        "status": "RESEARCH_SEGMENTER_DIAGNOSTIC_NOT_RELEASE_VALIDATION",
        "model_id": model["model_id"],
        "source_commit": SOURCE_COMMIT,
        "source_license": SOURCE_LICENSE,
        "training": {"sentences": len(train_sentences), "thai_vocabulary": len(counts), "wisesight_used": False},
        "selected_token_penalty": best_penalty,
        "development": score_groups(dev_groups, counts, best_penalty),
        "test": score_groups(test_groups, counts, best_penalty),
        "wisesight_test_only": score_groups(load_wisesight_groups(), counts, best_penalty),
        "limitations": [
            "TUD annotations inherit the source treebank's tokenization process and are not an independent expert re-adjudication of all word boundaries.",
            "The TUD corpus is licensed CC BY-SA 4.0; preserve attribution and share-alike notices for derived model artifacts.",
            "Metrics are restricted to contiguous Thai-only runs with at least two tokens and are not directly comparable to full-text metrics unless the same filtering is applied.",
            "This research model is not the production default; the current public text API remains conservative and uses the separately evaluated dictionary segmenter.",
        ],
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
