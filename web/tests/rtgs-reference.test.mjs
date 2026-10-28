import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { romanizeRtgsWord, romanizeRtgsWords, renderRtgsTokens } from "../src/rtgs-reference.js";

const examples = new Map([
  ["กา", "ka"], ["พริก", "phrik"], ["มา", "ma"], ["ไฟ", "fai"], ["หมา", "ma"], ["ใหม่", "mai"], ["ไหม", "mai"], ["เหงา", "ngao"]
]);
for (const [thai, expected] of examples) {
  const result = romanizeRtgsWord(thai);
  assert.equal(result.status, "transliterated", thai);
  assert.equal(result.value, expected, thai);
  assert.equal(result.source, "PyThaiNLP 5.4.0 royin port + ClippyFirst orthographic correction");
}
assert.equal(romanizeRtgsWord("test").status, "unavailable");
assert.equal(romanizeRtgsWord("").status, "unavailable");
assert.equal(romanizeRtgsWord("ห").value, "");
assert.equal(romanizeRtgsWord("ให้").value, "hai");
assert.equal(romanizeRtgsWord("พริก").value, "phrik");
assert.equal(romanizeRtgsWords(["กา", "กร"]).length > 0, true);

// Existing analyzer token boundaries are preserved; the RTGS output is never
// fed to the IPA→Ukrainian adapter and non-Thai tokens are passed through.
assert.equal(renderRtgsTokens([
  { kind: "thai", input: "พริก" },
  { kind: "space", input: " " },
  { kind: "latin", input: "ph" }
]), "phrik ph");

const source = await readFile(new URL("../src/rtgs-reference.js", import.meta.url), "utf8");
assert.doesNotMatch(source, /adaptIpaToUkrainian|ipa-ua/);
assert.doesNotMatch(source, /fetch\s*\(|XMLHttpRequest/);
const app = await readFile(new URL("../src/app.js", import.meta.url), "utf8");
assert.ok(app.includes("renderRtgsTokens(tokens)"));
assert.ok(app.includes("adaptIpaToUkrainian(source)"));
assert.ok(app.includes("RTGS не позначає тон"));
console.log("RTGS offline port, UI separation, and no-network contract: OK");
