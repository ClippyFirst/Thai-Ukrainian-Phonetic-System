import assert from "node:assert/strict";
import { createTltkOovFallback } from "../src/fastthaig2p-tltk-oov.js";

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

console.log("Native TLTK OOV synthetic parser contract: PASS");
