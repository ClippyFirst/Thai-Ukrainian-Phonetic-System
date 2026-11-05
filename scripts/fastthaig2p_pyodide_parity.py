#!/usr/bin/env python3
"""Emit the shared FastThaiG2P service contract for CPython/Pyodide parity.

This is software-runtime evidence only; outputs are not linguistic gold.
"""
from __future__ import annotations

import json
from typing import Any

from thai_ukrainian.fastthaig2p_service import (
    UPSTREAM_COMMIT,
    FastThaiG2PAnalysisError,
    analyze_with_fastthaig2p,
)

INPUTS = ("กา", "สวน", "กรุงเทพมหานคร", "สวัสดีครับ")


def build_payload() -> dict[str, Any]:
    cases: list[dict[str, Any]] = []
    for text in INPUTS:
        try:
            result: dict[str, Any] = {
                "status_code": 200,
                "body": analyze_with_fastthaig2p(text),
            }
        except FastThaiG2PAnalysisError as exc:
            result = {
                "status_code": exc.status_code,
                "detail": exc.detail,
            }
        cases.append({"input": text, "result": result})
    return {"upstream_commit": UPSTREAM_COMMIT, "cases": cases}


if __name__ == "__main__":
    print(
        json.dumps(
            build_payload(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
    )
