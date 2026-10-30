"""Canonical runtime-data locations for source and installed distributions."""
from __future__ import annotations

from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent
PACKAGED_DATA_ROOT = PACKAGE_ROOT / "_data"
SOURCE_DATA_ROOT = PACKAGE_ROOT.parents[1] / "data"

# Editable/source checkouts use the canonical repository data. Wheels carry a
# deliberately limited runtime subset inside the package itself.
DATA_ROOT = PACKAGED_DATA_ROOT if PACKAGED_DATA_ROOT.is_dir() else SOURCE_DATA_ROOT
THAI_DATA_ROOT = DATA_ROOT / "thai"
