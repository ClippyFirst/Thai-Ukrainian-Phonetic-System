from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from thai_ukrainian.fastthaig2p_adapter import FastThaiG2PAdapter  # noqa: E402
from thai_ukrainian.fastthaig2p_service import (  # noqa: E402
    FastThaiG2PAnalysisError,
    analyze_with_fastthaig2p as _analyze_with_fastthaig2p,
)

logger = logging.getLogger(__name__)
WEB_DIR = ROOT / "web"
app = FastAPI(title="Thai → Ukrainian · FastThaiG2P", version="0.1.0")
_engine: FastThaiG2PAdapter | None = None


class AnalyzeRequest(BaseModel):
    text: str = Field(min_length=1, max_length=2000)


def analyze_with_fastthaig2p(text: str) -> dict[str, Any]:
    try:
        # Keep the injectable module-level engine for API tests; production and
        # the browser worker share the same transport-neutral service function.
        return _analyze_with_fastthaig2p(text, engine=_engine)
    except FastThaiG2PAnalysisError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "engine": "FastThaiG2P"}


@app.post("/api/analyze")
def analyze(request: AnalyzeRequest) -> dict[str, Any]:
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Введіть тайський текст.")
    try:
        return analyze_with_fastthaig2p(request.text)
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Unhandled exception while processing FastThaiG2P API request")
        raise HTTPException(
            status_code=500,
            detail={
                "code": "analysis_failed",
                "message": "Внутрішня помилка сервісу. Спробуйте пізніше.",
            },
        ) from exc


app.mount("/", StaticFiles(directory=WEB_DIR, html=True), name="web")
