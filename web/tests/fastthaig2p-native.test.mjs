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

let requestedUrl;
const loaded = await loadFastThaiG2PNativeDictionary({
  url: "https://example.test/native.json",
  fetchImpl: async url => {
    requestedUrl = url;
    return { ok: true, json: async () => ({ "สวน": "/sua̯n˩˩˦/" }) };
  }
});
assert.equal(requestedUrl, "https://example.test/native.json");
assert.equal(loaded["สวน"], "/sua̯n˩˩˦/");
await assert.rejects(
  loadFastThaiG2PNativeDictionary({
    fetchImpl: async () => ({ ok: false, status: 404 })
  }),
  error => error.code === "native_dictionary_unavailable"
);

console.log("FastThaiG2P native JavaScript dictionary-adapter contracts passed");
