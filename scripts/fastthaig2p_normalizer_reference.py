#!/usr/bin/env python3
"""Emit deterministic reference cases from the pinned FastThaiG2P normalizer."""
from __future__ import annotations

import json
from pythainlp.tokenize import word_tokenize
from fastthaig2p.normalizer import normalize

CASES = [
    "คนๆ", "คนๆๆ", "ไทยๆ", "ราคา 1,234.50 บาท", "เวลา 8:00 น.",
    "เบอร์ 081-234-5678", "somchai.w@gmail.com", "5 km",
    "อุณหภูมิ 25°C", "เลข ๑๒๓", "A10G", "แผน A", "ม.ค. 2026",
    "USD 25.50", "Google WiFi", "214/12 ม.10", "ห้อง 2B-13",
    "ติดตามผ่าน LINE หรือ Facebook",
]

print(json.dumps({
    "upstream_commit": "4e82a291b4cf2876326744c6580121e9986ad354",
    "pythainlp_version": "5.4.0",
    "cases": [
        {"input": text, "tokens": word_tokenize(text), "expected": normalize(text)}
        for text in CASES
    ],
}, ensure_ascii=False, indent=2))
