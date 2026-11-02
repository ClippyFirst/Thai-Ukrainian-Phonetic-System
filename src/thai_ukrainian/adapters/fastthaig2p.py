"""Lazy adapter for the pinned optional FastThaiG2P package.

The adapter preserves the upstream IPA string verbatim. It does not normalize,
reinterpret, or adapt IPA to Ukrainian; those operations belong to the
repository's typed PhoneticResult boundary and Ukrainian adapter.
"""
from __future__ import annotations

from importlib import import_module, metadata
from typing import Any

UPSTREAM_REPOSITORY = "https://github.com/awslabs/FastThaiG2P"
UPSTREAM_COMMIT = "c4759eef7df03e11fcbb9aa83efe8cf21709fd2f"
EXPECTED_PACKAGE = "fastthaig2p"
EXPECTED_VERSION = "0.1.0"


class FastThaiG2PUnavailable(RuntimeError):
    """Raised when the optional FastThaiG2P dependency is not installed."""


class FastThaiG2PAdapter:
    """Thin, optional adapter that returns FastThaiG2P's raw IPA output."""

    def __init__(self, engine: Any | None = None) -> None:
        if engine is None:
            try:
                package = import_module("fastthaig2p")
            except ImportError as exc:
                raise FastThaiG2PUnavailable(
                    "FastThaiG2P is optional; install the 'fastthaig2p' extra "
                    "on Python 3.11 or newer."
                ) from exc
            try:
                engine = package.G2P()
            except Exception as exc:
                raise FastThaiG2PUnavailable(
                    f"FastThaiG2P could not initialize: {type(exc).__name__}: {exc}"
                ) from exc
        if not callable(getattr(engine, "convert", None)):
            raise TypeError("FastThaiG2P engine must expose a callable convert(text) method")
        self._engine = engine

    def convert(self, text: str) -> str:
        """Return upstream output unchanged; preserve its spaces, slashes and IPA marks."""
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        result = self._engine.convert(text)
        if not isinstance(result, str):
            raise TypeError("FastThaiG2P convert() must return a string")
        return result

    @staticmethod
    def metadata() -> dict[str, Any]:
        try:
            version = metadata.version(EXPECTED_PACKAGE)
        except metadata.PackageNotFoundError:
            version = None
        return {
            "package": "FastThaiG2P",
            "distribution": EXPECTED_PACKAGE,
            "version": version,
            "expected_version": EXPECTED_VERSION,
            "source_repository": UPSTREAM_REPOSITORY,
            "source_commit": UPSTREAM_COMMIT,
            "configuration": {
                "api": "G2P.convert",
                "dictionary_and_rule_fallback": True,
                "raw_output_preserved": True,
            },
            "python_requires": ">=3.11",
            "runtime_dependency": "pythainlp>=5.3.4",
            "accuracy_status": "NOT_MEASURED_ON_INDEPENDENT_GOLD",
        }
