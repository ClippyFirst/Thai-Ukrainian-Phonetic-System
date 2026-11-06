import assert from "node:assert/strict";
import {
  createFastThaiG2PNativeEngine,
  loadFastThaiG2PNativeDictionary,
  parseFastThaiG2POutput,
  NATIVE_PORT_STAGE
} from "../src/fastthaig2p-native.js";

const parsed = parseFastThaiG2POutput("/sua̯n˩˩˦/ /kʰrap̚˦˥/");
assert.deepEqual(parsed.wordGroups, ["sua̯n˩˩˦", "kʰrap̚˦˥"]);
assert.deepEqual(parsed.syllables, ["sua̯n˩˩˦", "kʰrap̚˦˥"]);
assert.equal(parsed.passthrough, "");
assert.equal(parseFastThaiG2POutput("สวน").passthrough, "สวน");

const engine = createFastThaiG2PNativeEngine({
  dictionary: {
    "สวน": "/sua̯n˩˩˦/",
    "ครับ": "/kʰrap̚˦˥/"
  }
});
assert.equal(engine.stage, NATIVE_PORT_STAGE);
assert.equal(engine.convert("สวน ครับ").raw_ipa, "/sua̯n˩˩˦/ /kʰrap̚˦˥/");
assert.equal(engine.convert("สวน ครับ").coverage.dictionary_tokens, 2);
assert.equal(engine.convert("สวน").words[0].syllables[0].tone, "rising");
assert.equal(engine.convert("สวน").words[0].syllables[0].vowel_length, null);
assert.match(engine.convert("สวน").warnings.join(" "), /лише словниковий адаптер/);
assert.throws(() => engine.convert("невідоме"), error => error.code === "native_dictionary_miss");
assert.throws(() => engine.convert("สวน!"), error => error.code === "native_dictionary_miss");
assert.throws(() => engine.convert("   "), error => error.code === "empty_input");
assert.throws(
  () => createFastThaiG2PNativeEngine({ dictionary: { "bad": "not-ipa" } }),
  /Invalid source-attributed IPA/
);

const dictionaryText = JSON.stringify({ "สวน": "/sua̯n˩˩˦/" });
const dictionaryBytes = new TextEncoder().encode(dictionaryText);
const dictionaryHash = [...new Uint8Array(await crypto.subtle.digest("SHA-256", dictionaryBytes))]
  .map(value => value.toString(16).padStart(2, "0"))
  .join("");
const manifest = {
  schema_version: 1,
  upstream_commit: "4e82a291b4cf2876326744c6580121e9986ad354",
  stage: "dictionary-and-normalizer-data-only; not a complete runtime",
  dictionary_license: "CC-BY-SA-4.0",
  dictionary_entries: 1,
  assets: [{
    path: "native/fastthaig2p-ipa.json",
    sha256: dictionaryHash,
    size_bytes: dictionaryBytes.byteLength
  }]
};
const loaded = await loadFastThaiG2PNativeDictionary({
  url: "https://example.test/native/fastthaig2p-ipa.json",
  manifestUrl: "https://example.test/native/manifest.json",
  fetchImpl: async url => {
    if (String(url).endsWith("manifest.json")) {
      return { ok: true, json: async () => manifest };
    }
    return { ok: true, arrayBuffer: async () => dictionaryBytes.buffer };
  }
});
assert.equal(loaded["สวน"], "/sua̯n˩˩˦/");

await assert.rejects(
  loadFastThaiG2PNativeDictionary({
    manifestUrl: "https://example.test/native/manifest.json",
    fetchImpl: async () => ({ ok: false, status: 404 })
  }),
  error => error.code === "native_manifest_unavailable"
);
await assert.rejects(
  loadFastThaiG2PNativeDictionary({
    manifestUrl: "https://example.test/native/manifest.json",
    fetchImpl: async () => ({ ok: true, json: async () => ({}) })
  }),
  error => error.code === "native_manifest_invalid"
);

console.log("FastThaiG2P native JavaScript dictionary-adapter contracts passed");
