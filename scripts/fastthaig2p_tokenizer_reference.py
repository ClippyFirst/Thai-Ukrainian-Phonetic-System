#!/usr/bin/env python3
"""Emit exact tokenizer references from FastThaiG2P's pinned custom newmm dictionary."""
from __future__ import annotations

import json
from fastthaig2p.normalizer import normalize
from fastthaig2p.tokenizer import Tokenizer

CASES = [
    "สวัสดีครับ", "ประเทศไทยมีภาษาไทย", "ธนาคารกรุงเทพ", "กรุงเทพมหานคร",
    "ฉันชอบภาษาไทย", "ภาษาไทย ภาษาอังกฤษ", "คริปโต", "เด็กๆ", "A10G",
    "เวลา 8:00 น.", "ราคา 1,234.50 บาท", "เลขที่ 214/12 ม.10",
    "ติดตามผ่าน LINE หรือ Facebook", "บริษัทจำกัด",
    "สวัสดีครับ ขอบคุณมาก", "การทดสอบระบบ FastThaiG2P",
]

tokenizer = Tokenizer()
print(json.dumps({
    "upstream_commit": "4e82a291b4cf2876326744c6580121e9986ad354",
    "pythainlp_version": "5.4.0",
    "cases": [
        {"input": text, "normalized": normalize(text), "expected": tokenizer.tokenize(normalize(text))}
        for text in CASES
    ],
}, ensure_ascii=False, indent=2))
