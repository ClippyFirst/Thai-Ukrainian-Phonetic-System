import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { gunzipSync } from "node:zlib";
import { createTltkOovFallback } from "../src/fastthaig2p-tltk-oov.js";
import { createFastThaiG2PNativePipeline } from "../src/fastthaig2p-native.js";

const root = new URL("../../", import.meta.url);
const [compressed, fixtureBytes, dictionaryBytes, normalizerBytes, defaultWordsBytes] = await Promise.all([
  readFile(new URL("web/vendor/native-oov/tltk-oov-data.json.gz", root)),
  readFile(new URL("build/tltk-oov-reference.json", root)),
  readFile(new URL("web/vendor/native/fastthaig2p-ipa.json", root)),
  readFile(new URL("web/vendor/native/fastthaig2p-normalizer.json", root)),
  readFile(new URL("web/vendor/native/pythainlp-default-words.txt", root))
]);
const data = JSON.parse(gunzipSync(compressed).toString("utf8"));
const fixtures = JSON.parse(fixtureBytes);
assert.equal(fixtures.schema_version, 1);
assert.equal(fixtures.fastthaig2p_commit, data.fastthaig2p_commit);
assert.ok(fixtures.cases.length > 0, "Python reference generator must produce actual OOV cases");

const fallback = createTltkOovFallback(data);
const pipeline = createFastThaiG2PNativePipeline({
  dictionary: JSON.parse(dictionaryBytes.toString("utf8")),
  normalizerData: JSON.parse(normalizerBytes.toString("utf8")),
  defaultWords: defaultWordsBytes.toString("utf8").split(/\r?\n/u).filter(Boolean)
});
for (const item of fixtures.cases) {
  const trace = fallback.inspect(item.token);
  const actual = pipeline.convert(item.token, { oovFallback: fallback.convert });
  if (actual.raw_ipa !== item.response.raw_ipa) {
    console.error("TLTK OOV trace:", JSON.stringify({ token: item.token, trace }, null, 2));
  }
  assert.equal(actual.normalized_input, item.token);
  const { normalized_input, ...serviceResult } = actual;
  assert.deepEqual(serviceResult, item.response, "Native typed service JSON must match pinned Python output for " + item.token);
}
console.log("Native TLTK OOV full typed Python-service parity: " + fixtures.cases.length + " reference cases PASS");
