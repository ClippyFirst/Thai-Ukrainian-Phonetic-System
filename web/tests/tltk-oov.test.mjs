import assert from "node:assert/strict";
import { createHash, webcrypto } from "node:crypto";
import { gzipSync } from "node:zlib";
import { createTltkOovFallback, loadTltkOovData } from "../src/fastthaig2p-tltk-oov.js";

const data = {
  schema_version: 1,
  fastthaig2p_commit: "4e82a291b4cf2876326744c6580121e9986ad354",
  tltk_source_commit: "0cef4bcfbdd675f589783dd4134b87b9bb9fbb93",
  tltk_package_version: "1.9.1",
  tltk_package_license: "BSD-3-Clause",
  parser_constants: {
    stable_base: {
      X: { "ก": "k" },
      Y: { "ก": "k" }
    },
    stable_aliases: {
      A: "X", K: "X", C: "X", R: "X", G: "X", E: "X",
      D: "Y", Z: "Y", H: "Y", F: "Y"
    },
    allowed_clusters: { "ก": "ก" },
    english_abbreviations: []
  },
  syllable_patterns: [{ pattern: "X", pronunciation: "X", tone_flag: "N" }],
  syllable_dictionary: [],
  phone_trigrams: [
    ["|", "ก", "|", "k1", 3],
    ["|", "ก", "ก", "k1", 2],
    ["ก", "ก", "|", "k1", 2]
  ],
  syllable_trigrams: [
    ["|", "|", "ก", 3],
    ["|", "ก", "|", 3],
    ["ก", "|", "|", 2]
  ],
  word_dictionary: ["ก"]
};

const fallback = createTltkOovFallback(data);
assert.equal(fallback.convert("ก"), "/k˨˩/");
assert.equal(fallback.convert("ข"), null);
assert.equal(fallback.convert("abc"), null);
assert.equal(fallback.packageVersion, "1.9.1");
assert.equal(fallback.sourceCommit, "4e82a291b4cf2876326744c6580121e9986ad354");

assert.throws(() => createTltkOovFallback({ ...data, tltk_package_license: "GPL-3.0" }),
  /schema is incomplete/);

const payload = Buffer.from(JSON.stringify(data), "utf8");
const compressed = gzipSync(payload, { level: 9, mtime: 0 });
const digest = bytes => createHash("sha256").update(bytes).digest("hex");
const manifest = {
  schema_version: 1,
  license: "BSD-3-Clause",
  tltk_package_version: "1.9.1",
  fastthaig2p_commit: data.fastthaig2p_commit,
  tltk_source_commit: data.tltk_source_commit,
  path: "tltk-oov-data.json.gz",
  compressed_size_bytes: compressed.byteLength,
  compressed_sha256: digest(compressed),
  uncompressed_size_bytes: payload.byteLength,
  uncompressed_sha256: digest(payload)
};
const loaded = await loadTltkOovData({
  baseUrl: new URL("https://example.test/native-oov/"),
  cryptoImpl: webcrypto,
  DecompressionStreamImpl: DecompressionStream,
  fetchImpl: async url => String(url).endsWith("manifest.json")
    ? { ok: true, json: async () => manifest }
    : { ok: true, arrayBuffer: async () => compressed.buffer.slice(compressed.byteOffset, compressed.byteOffset + compressed.byteLength) }
});
assert.equal(loaded.schema_version, 1);
assert.equal(loaded.tltk_package_license, "BSD-3-Clause");

const tampered = compressed.subarray(1);
await assert.rejects(loadTltkOovData({
  baseUrl: new URL("https://example.test/native-oov/"),
  cryptoImpl: webcrypto,
  DecompressionStreamImpl: DecompressionStream,
  fetchImpl: async url => String(url).endsWith("manifest.json")
    ? { ok: true, json: async () => manifest }
    : { ok: true, arrayBuffer: async () => tampered.buffer.slice(tampered.byteOffset, tampered.byteOffset + tampered.byteLength) }
}), error => error.code === "native_oov_asset_corrupt");

console.log("Native TLTK OOV synthetic parser and integrity-loader contracts: PASS");
