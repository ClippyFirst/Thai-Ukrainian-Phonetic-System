from __future__ import annotations

import csv
import json
import socket
import tempfile
import threading
import urllib.error
import urllib.request
from importlib.metadata import version as distribution_version
import unittest
from pathlib import Path
from unittest.mock import patch
from http.server import ThreadingHTTPServer

import thai_ukrainian
from thai_ukrainian.batch import analyze_input, load_batch, write_batch
from thai_ukrainian.server import APIHandler
from thai_ukrainian.cli import main


class CliBatchApiTests(unittest.TestCase):
    def test_analyze_input_has_stable_top_level_fields(self):
        result = analyze_input("กา")
        for key in ("input", "status", "analyses", "ipa", "phonetic_ipa", "tones", "tone_ipa", "ukrainian_orthography", "warnings"):
            self.assertIn(key, result)

    def test_txt_batch_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            source = root / "input.txt"
            output = root / "output.jsonl"
            source.write_text("กา\nนา\n", encoding="utf-8")
            rows = load_batch(source)
            self.assertEqual([r["thai"] for r in rows], ["กา", "นา"])
            results = [analyze_input(r["thai"]) | {"id": r["id"]} for r in rows]
            write_batch(results, output)
            records = [json.loads(line) for line in output.read_text(encoding="utf-8").splitlines()]
            self.assertEqual(len(records), 2)
            self.assertEqual(records[0]["input"], "กา")

    def test_tsv_batch_uses_tab_delimiter(self):
        with tempfile.TemporaryDirectory() as d:
            source = Path(d) / "input.tsv"
            source.write_text("thai\tnote\nกา\tfixture\n", encoding="utf-8")
            rows = load_batch(source)
            self.assertEqual(rows, [{"id": "1", "thai": "กา"}])

    def test_json_non_object_request_returns_400_not_500(self):
        server = ThreadingHTTPServer(("127.0.0.1", 0), APIHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            url = f"http://127.0.0.1:{server.server_port}/analyze"
            for payload in ([], None, "not-an-object"):
                request = urllib.request.Request(
                    url,
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with self.subTest(payload=payload):
                    with self.assertRaises(urllib.error.HTTPError) as raised:
                        urllib.request.urlopen(request, timeout=3)
                    self.assertEqual(raised.exception.code, 400)
                    body = json.loads(raised.exception.read().decode("utf-8"))
                    self.assertEqual(body["error"], "invalid_request")
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=3)

    def test_negative_content_length_is_rejected_before_reading_body(self):
        server = ThreadingHTTPServer(("127.0.0.1", 0), APIHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            body = json.dumps({"text": "กา"}).encode("utf-8")
            request = (
                b"POST /analyze HTTP/1.1\r\n"
                b"Host: 127.0.0.1\r\n"
                b"Content-Type: application/json\r\n"
                b"Content-Length: -1\r\n"
                b"Connection: close\r\n\r\n"
                + body
            )
            with socket.create_connection(("127.0.0.1", server.server_port), timeout=3) as client:
                client.sendall(request)
                client.shutdown(socket.SHUT_WR)
                response = b""
                while chunk := client.recv(4096):
                    response += chunk
            self.assertTrue(response.startswith(b"HTTP/1.0 400"), response)
            self.assertIn(b'"error": "invalid_request"', response)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=3)

    def test_unexpected_api_error_is_logged_but_not_exposed(self):
        server = ThreadingHTTPServer(("127.0.0.1", 0), APIHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            url = f"http://127.0.0.1:{server.server_port}/analyze"
            request = urllib.request.Request(
                url,
                data=json.dumps({"text": "กา"}).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with self.assertLogs("thai_ukrainian.server", level="ERROR") as captured:
                with patch(
                    "thai_ukrainian.server.analyze_input",
                    side_effect=RuntimeError("secret-internal-detail"),
                ):
                    with self.assertRaises(urllib.error.HTTPError) as raised:
                        urllib.request.urlopen(request, timeout=3)
            self.assertEqual(raised.exception.code, 500)
            body = json.loads(raised.exception.read().decode("utf-8"))
            self.assertEqual(body, {"error": "analysis_failed", "detail": "Internal server error."})
            self.assertNotIn("secret-internal-detail", json.dumps(body))
            self.assertIn("secret-internal-detail", captured.output[0])
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=3)

    def test_package_and_http_server_share_distribution_version(self):
        installed_version = distribution_version("thai-ukrainian-phonetic-system")
        self.assertEqual(thai_ukrainian.__version__, installed_version)
        self.assertEqual(APIHandler.server_version, f"thai-ua/{installed_version}")

    def test_citation_metadata_matches_package_version(self):
        installed_version = distribution_version("thai-ukrainian-phonetic-system")
        citation = (Path(__file__).parents[1] / "CITATION.cff").read_text(encoding="utf-8")
        self.assertIn(f"version: {installed_version}", citation.splitlines())

    def test_csv_batch(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            source = root / "input.csv"
            output = root / "output.csv"
            with source.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=["thai", "note"])
                writer.writeheader()
                writer.writerow({"thai": "กา", "note": "fixture"})
            main(["batch", str(source), "-o", str(output)])
            with output.open(encoding="utf-8-sig", newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(rows[0]["input"], "กา")

    def test_cli_analyze(self):
        with patch("builtins.print") as mocked:
            self.assertEqual(main(["analyze", "กา", "--compact"]), 0)
            payload = json.loads(mocked.call_args.args[0])
            self.assertEqual(payload["input"], "กา")


if __name__ == "__main__":
    unittest.main()
