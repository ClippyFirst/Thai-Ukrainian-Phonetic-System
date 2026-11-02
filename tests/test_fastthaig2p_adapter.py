import unittest
from unittest.mock import patch

from thai_ukrainian.adapters.fastthaig2p import (
    FastThaiG2PAdapter,
    FastThaiG2PUnavailable,
    UPSTREAM_COMMIT,
)


class FakeEngine:
    def __init__(self, result="/kʰaː˥˩/"):
        self.result = result
        self.received = []

    def convert(self, text):
        self.received.append(text)
        return self.result


class FastThaiG2PAdapterTests(unittest.TestCase):
    def test_adapter_preserves_upstream_ipa_exactly(self):
        raw = " /kʰaː˥˩.t͡ɕuʔ˨˩/  /ŋɤn˧/ "
        engine = FakeEngine(raw)
        adapter = FastThaiG2PAdapter(engine)
        self.assertEqual(adapter.convert("กา"), raw)
        self.assertEqual(engine.received, ["กา"])

    def test_adapter_rejects_non_string_input_and_output(self):
        adapter = FastThaiG2PAdapter(FakeEngine())
        with self.assertRaisesRegex(TypeError, "text must be a string"):
            adapter.convert(None)
        with self.assertRaisesRegex(TypeError, "must return a string"):
            FastThaiG2PAdapter(FakeEngine(123)).convert("กา")

    def test_optional_dependency_failure_is_actionable(self):
        with patch(
            "thai_ukrainian.adapters.fastthaig2p.import_module",
            side_effect=ModuleNotFoundError("fastthaig2p"),
        ):
            with self.assertRaisesRegex(FastThaiG2PUnavailable, "optional"):
                FastThaiG2PAdapter()

    def test_metadata_pins_upstream_source(self):
        self.assertEqual(UPSTREAM_COMMIT, "c4759eef7df03e11fcbb9aa83efe8cf21709fd2f")
        self.assertEqual(FastThaiG2PAdapter.metadata()["source_commit"], UPSTREAM_COMMIT)


if __name__ == "__main__":
    unittest.main()
