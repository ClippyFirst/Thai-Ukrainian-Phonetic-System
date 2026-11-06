#!/usr/bin/env python3
"""Generate independent pinned FastThaiG2P OOV reference cases for the browser port."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = ROOT / "build" / "FastThaiG2P"
sys.path.insert(0, str(UPSTREAM))

from fastthaig2p.g2p import G2P  # noqa: E402
from fastthaig2p.normalizer import normalize  # noqa: E402


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
    engine = G2P()
    selected: dict[str, str] = {}
    rejected: dict[str, str] = {}
    for candidate in CANDIDATES:
        normalized = normalize(candidate)
        for token in engine._tokenizer.tokenize(normalized):
            if not token or token in engine._ipa or not re.fullmatch(r"[ก-๛]+", token):
                continue
            if engine._tokenizer.tokenize(normalize(token)) != [token]:
                continue
            result = engine.convert(token).strip()
            if not (result.startswith("/") and result.endswith("/") and len(result) > 2):
                rejected[token] = result
                continue
            selected[token] = result
            if len(selected) >= 24:
                break
        if len(selected) >= 24:
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
                "cases": [{"token": token, "ipa": ipa} for token, ipa in sorted(selected.items())],
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
