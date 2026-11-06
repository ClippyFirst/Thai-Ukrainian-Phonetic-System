from __future__ import annotations

import bz2
import tempfile
import unittest
from pathlib import Path

from scripts.verify_tltk_fallback_provenance import PAIRS, verify


class TltkFallbackProvenanceTests(unittest.TestCase):
    def test_all_assets_and_compression_sizes_are_reported(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fast = root / "fast"
            tltk = root / "tltk"
            (fast / "fastthaig2p").mkdir(parents=True)
            (fast / "data/fallback").mkdir(parents=True)
            (tltk / "tltk").mkdir(parents=True)
            (fast / "fastthaig2p/_th2ipa.py").write_text(
                "Thai Language Toolkit : version  1.3.8\n", encoding="utf-8"
            )
            (tltk / "setup.py").write_text(
                "version='1.9.1'\nlicense='BSD-3-Clause'\n"
                "'License :: OSI Approved :: BSD License'\n"
                + "\n".join(PAIRS),
                encoding="utf-8",
            )
            (tltk / "README.rst").write_text(
                "As of version 1.2.2, the package license has changed to the "
                "New BSD License (BSD-3-Clause).",
                encoding="utf-8",
            )
            (tltk / "MANIFEST.in").write_text("include LICENSE.txt\n", encoding="utf-8")
            (tltk / "LICENSE").write_text(
                "GNU LESSER GENERAL PUBLIC LICENSE", encoding="utf-8"
            )
            (tltk / "LICENSE.txt").write_text(
                "Redistribution and use in source and binary forms", encoding="utf-8"
            )
            (tltk / "PKG-INFO").write_text(
                "Version: 1.1.7\nLicense: GPLv3", encoding="utf-8"
            )

            for name, (fast_rel, tltk_rel, transform) in PAIRS.items():
                fast_path = fast / fast_rel
                tltk_path = tltk / tltk_rel
                fast_path.parent.mkdir(parents=True, exist_ok=True)
                tltk_path.parent.mkdir(parents=True, exist_ok=True)
                payload = ("fallback-" + name).encode("utf-8")
                fast_path.write_bytes(payload)
                tltk_path.write_bytes(
                    bz2.compress(payload) if transform == "bzip2_decompressed" else payload
                )

            report = verify(fast, tltk)

            self.assertEqual(report["verified_assets"], 6)
            self.assertEqual(
                report["license_scope"],
                "BSD-3-CLAUSE_SUPPORTED_FOR_TLTK_1.9.1_PACKAGED_FALLBACK_ASSETS; RETAIN_REPOSITORY_LGPL_NOTICE_AS_HISTORICAL_CONTEXT",
            )
            self.assertTrue(report["pinned_tltk_package_manifest_includes_license"])
            self.assertTrue(report["pinned_tltk_fallback_assets_in_package_data"])
            self.assertEqual(report["pinned_tltk_package_license_file"], "BSD-3-Clause")
            self.assertEqual(
                report["fallback_data_size_bytes"],
                sum((fast / pair[0]).stat().st_size for pair in PAIRS.values()),
            )
            self.assertGreater(report["fallback_data_gzip_size_bytes"], 0)
            self.assertLess(report["fallback_data_gzip_savings_ratio"], 1)
            self.assertTrue(all(item["verified"] for item in report["assets"]))
            self.assertEqual(
                next(item for item in report["assets"] if item["asset"] == "sylform_var.pkl")["transform"],
                "bzip2_decompressed",
            )


if __name__ == "__main__":
    unittest.main()
