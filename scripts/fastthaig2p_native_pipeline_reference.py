#!/usr/bin/env python3
"""Emit dictionary-only end-to-end references for the native front-half pipeline."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from thai_ukrainian.fastthaig2p_adapter import FastThaiG2PAdapter
from thai_ukrainian.fastthaig2p_service import analyze_with_fastthaig2p
from fastthaig2p.normalizer import normalize
from fastthaig2p.tokenizer import Tokenizer

CANDIDATES = [
    "สวน", "สวัสดีครับ", "ประเทศไทย", "ภาษาไทย", "กรุงเทพมหานคร",
    "ขอบคุณ", "ธนาคาร", "ดอกเบี้ย 2.5% ต่อปี", "วันที่ 15 ม.ค. 2569",
    "ราคา 1,234 บาท", "คนๆ", "สวัสดี", "แมว", "บ้าน", "น้ำ",
    "การทดสอบระบบ",
]

adapter = FastThaiG2PAdapter()
tokenizer = Tokenizer()
cases = []
for text in CANDIDATES:
    normalized = normalize(text)
    tokens = [token for token in tokenizer.tokenize(normalized) if token.strip()]
    if tokens and all(token in adapter._engine._ipa for token in tokens):
        cases.append({
            "input": text,
            "normalized": normalized,
            "tokens": tokens,
            "expected_ipa": adapter._engine.convert(text),
            "expected_result": analyze_with_fastthaig2p(text, engine=adapter),
        })
if len(cases) < 5:
    raise SystemExit(f"Not enough dictionary-only pipeline fixtures: {len(cases)}")
print(json.dumps({
    "upstream_commit": "4e82a291b4cf2876326744c6580121e9986ad354",
    "cases": cases,
}, ensure_ascii=False, indent=2))
