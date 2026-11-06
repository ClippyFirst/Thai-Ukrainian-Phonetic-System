#!/usr/bin/env python3
"""Generate independent pinned FastThaiG2P OOV reference cases for the browser port.

The diagnostic block records upstream segmentation/scoring internals for parity debugging.
"""
from __future__ import annotations

import gzip
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = ROOT / "build" / "FastThaiG2P"
sys.path.insert(0, str(UPSTREAM))
sys.path.insert(0, str(ROOT / "src"))

from fastthaig2p import _th2ipa  # noqa: E402
from thai_ukrainian.fastthaig2p_adapter import FastThaiG2PAdapter  # noqa: E402
from thai_ukrainian.fastthaig2p_service import (  # noqa: E402
    FastThaiG2PAnalysisError,
    analyze_with_fastthaig2p,
)


CANDIDATES = (
    "ทดสอบ", "ทดสอบระบบ", "ภาษาไทย", "สวัสดีครับ", "ขอบคุณ", "เกษตรกรรม",
    "ปัญญาประดิษฐ์", "วิทยาศาสตร์", "เครื่องจักร", "นวัตกรรม", "การวิเคราะห์",
    "ชลประทาน", "มันสำปะหลัง", "ข้าวโพด", "ยางพารา", "อุตสาหกรรม",
    "ยูเครน", "ประเทศไทย", "คอมพิวเตอร์", "โทรศัพท์", "รถยนต์", "ผลผลิต",
    "การทดลอง", "ความปลอดภัย", "เทคโนโลยี", "การเกษตร", "ปุ๋ยอินทรีย์",
    "ชีววิทยา", "เศรษฐศาสตร์", "ภาษาศาสตร์", "สัทศาสตร์", "สัทวิทยา",
    "พจนานุกรม", "การออกเสียง", "การถอดเสียง", "การประมวลผลภาษา",
)


def main() -> None:
    engine = FastThaiG2PAdapter()
    g2p = engine._engine
    normalize = engine._normalize
    data_pack = ROOT / "web" / "vendor" / "native-oov" / "tltk-oov-data.json.gz"
    if not data_pack.is_file():
        raise SystemExit("The extracted TLTK OOV data pack is required before generating parity fixtures.")
    tltk_words = json.loads(gzip.decompress(data_pack.read_bytes()))["word_dictionary"]
    selected: dict[str, dict[str, object]] = {}
    rejected: dict[str, str] = {}
    for candidate in (*CANDIDATES, *tltk_words):
        normalized = normalize(candidate)
        for token in g2p._tokenizer.tokenize(normalized):
            if not token or token in g2p._ipa or not re.fullmatch(r"[ก-๛]+", token):
                continue
            if g2p._tokenizer.tokenize(normalize(token)) != [token]:
                continue
            try:
                response = analyze_with_fastthaig2p(token, engine=engine)
            except FastThaiG2PAnalysisError as error:
                if len(rejected) < 30:
                    rejected[token] = str(error.detail)
                continue
            if response["coverage"]["rule_fallback_tokens"] != 1 or not response["raw_ipa"].startswith("/"):
                if len(rejected) < 30:
                    rejected[token] = response["raw_ipa"]
                continue
            if token == "กขส":
                # Guard the upstream segmentation/scoring anchor that exposed
                # the initial browser-port mismatch; keep diagnostics out of CI output.
                assert _th2ipa.sylparse(token) == "กขส"
                full = _th2ipa.prob_trisyl(["กขส"])
                split_two = _th2ipa.prob_trisyl(["ก", "ขส"])
                split_three = _th2ipa.prob_trisyl(["ก", "ข", "ส"])
                assert full > split_two > split_three
            selected[token] = response
            if len(selected) >= 64:
                break
        if len(selected) >= 64:
            break
    if not selected:
        raise SystemExit(
            "No single-token OOV references were produced. Expand CANDIDATES; "
            "do not replace missing references with invented expected IPA."
        )
    output = ROOT / "build" / "tltk-oov-reference.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "fastthaig2p_commit": "4e82a291b4cf2876326744c6580121e9986ad354",
                "cases": [{"token": token, "response": response} for token, response in sorted(selected.items())],
                "rejected": rejected,
            },
            ensure_ascii=False,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"reference_cases": len(selected), "rejected": len(rejected), "output": str(output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
