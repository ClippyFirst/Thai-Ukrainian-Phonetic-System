#!/usr/bin/env python3
"""Emit dictionary-only end-to-end references for the native front-half pipeline."""
from __future__ import annotations

import json
from fastthaig2p import G2P
from fastthaig2p.normalizer import normalize
from fastthaig2p.tokenizer import Tokenizer

CANDIDATES = [
    "สวน", "สวัสดีครับ", "ประเทศไทย", "ภาษาไทย", "กรุงเทพมหานคร",
    "ขอบคุณ", "ธนาคาร", "ดอกเบี้ย 2.5% ต่อปี", "วันที่ 15 ม.ค. 2569",
    "ราคา 1,234 บาท", "คนๆ", "สวัสดี", "แมว", "บ้าน", "น้ำ",
    "การทดสอบระบบ",
]

g2p = G2P()
tokenizer = Tokenizer()
cases = []
for text in CANDIDATES:
    normalized = normalize(text)
    tokens = [token for token in tokenizer.tokenize(normalized) if token.strip()]
    if tokens and all(token in g2p._ipa for token in tokens):
        cases.append({
            "input": text,
            "normalized": normalized,
            "tokens": tokens,
            "expected_ipa": g2p.convert(text),
        })
if len(cases) < 5:
    raise SystemExit(f"Not enough dictionary-only pipeline fixtures: {len(cases)}")
print(json.dumps({
    "upstream_commit": "4e82a291b4cf2876326744c6580121e9986ad354",
    "cases": cases,
}, ensure_ascii=False, indent=2))
