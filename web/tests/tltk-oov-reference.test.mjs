import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { gunzipSync } from "node:zlib";
import { createTltkOovFallback } from "../src/fastthaig2p-tltk-oov.js";

const root = new URL("../../", import.meta.url);
const [compressed, fixtureBytes] = await Promise.all([
  readFile(new URL("web/vendor/native-oov/tltk-oov-data.json.gz", root)),
  readFile(new URL("build/tltk-oov-reference.json", root))
]);
const data = JSON.parse(gunzipSync(compressed).toString("utf8"));
const fixtures = JSON.parse(fixtureBytes);
assert.equal(fixtures.schema_version, 1);
assert.equal(fixtures.fastthaig2p_commit, data.fastthaig2p_commit);
assert.ok(fixtures.cases.length > 0, "Python reference generator must produce actual OOV cases");

const fallback = createTltkOovFallback(data);
const mismatches = [];
for (const item of fixtures.cases) {
  const actual = fallback.convert(item.token);
  if (actual !== item.ipa) mismatches.push({ token: item.token, expected: item.ipa, actual });
}
assert.deepEqual(mismatches, [], "Native TLTK OOV IPA must exactly match pinned FastThaiG2P Python output");
console.log("Native TLTK OOV exact Python parity: " + fixtures.cases.length + " reference cases PASS");
