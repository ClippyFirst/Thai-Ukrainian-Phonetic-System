import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { romanizeRtgsWord, romanizeRtgsWords, renderRtgsTokens, romanizeRtgsTokenSequence } from "../src/rtgs-reference.js";
import { adaptRtgsToUkrainian, renderRtgsUkrainianTokens } from "../src/rtgs-ukrainian.js";

const examples = new Map([
  ["กา", "ka"], ["พริก", "phrik"], ["มา", "ma"], ["ไฟ", "fai"], ["หมา", "ma"], ["ใหม่", "mai"], ["ไหม", "mai"], ["เหงา", "ngao"], ["ใกล้", "klai"], ["ใคร", "khrai"], ["จริง", "ching"], ["สามารถ", "samat"], ["สวัสดี", "sawatdi"], ["สร้าง", "sang"], ["ศรี", "si"], ["เศร้า", "sao"], ["ไซร้", "sai"], ["ทรง", "song"], ["ทราม", "sam"], ["พัฒนา", "phatthana"], ["ฤทธิ์", "rit"], ["ฤๅ", "rue"], ["รถไฟ", "rotfai"], ["ผลไม้", "phonlamai"], ["ยูเครน", "yukhren"], ["ทราบ", "sap"], ["ทรัพย์", "sap"], ["แทรก", "saek"], ["อักษร", "akson"]
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
assert.equal(romanizeRtgsWord("ทราย").status, "unavailable");
assert.equal(romanizeRtgsWord("ฦ").status, "unavailable");
assert.equal(romanizeRtgsWord("ๆ").status, "unavailable");
assert.equal(romanizeRtgsWord("ฯ").status, "unavailable");
assert.equal(romanizeRtgsWord("สตรีเศรษฐบุตรบำเพ็ญ").status, "unavailable");
assert.equal(romanizeRtgsWord("พริก").value, "phrik");
assert.equal(romanizeRtgsWords(["กา", "กร"]).length > 0, true);

// Existing analyzer token boundaries are preserved; the RTGS output is never
// fed to the IPA→Ukrainian adapter and non-Thai tokens are passed through.
assert.equal(renderRtgsTokens([
  { kind: "thai", input: "พริก" },
  { kind: "space", input: " " },
  { kind: "latin", input: "ph" }
]), "phrik ph");
assert.equal(renderRtgsTokens([{ kind: "thai", input: "ทราย" }]), "⟦RTGS НЕ ПЕРЕВІРЕНО: ทราย⟧");

// RTGS roman letters are mapped as a separate orthographic method, not via IPA.
for (const [input, expected] of [
  ["phrik", "пхрік"], ["khrai", "кхрай"], ["th", "тх"], ["ch", "ч"],
  ["ngao", "нгао"], ["sawatdi", "саватді"], ["mai", "май"],
  ["ai", "ай"], ["ueai", "уеай"], ["uai", "уай"], ["oei", "оей"],
  ["aeo", "аео"], ["iao", "іао"], ["yukhren", "йукхрен"],
  ["phatthana", "пхаттхана"], ["sip-hok", "сіп-хок"]
]) {
  assert.equal(adaptRtgsToUkrainian(input).status, "adapted", input);
  assert.equal(adaptRtgsToUkrainian(input).output, expected, input);
}
assert.equal(adaptRtgsToUkrainian("zoo").status, "unavailable", "unsupported RTGS letters must fail closed");
assert.equal(adaptRtgsToUkrainian("h").output, "х", "standalone RTGS h is represented as Ukrainian х");
assert.equal(adaptRtgsToUkrainian("kh").output, "кх");
assert.equal(adaptRtgsToUkrainian("ph").output, "пх");
assert.equal(adaptRtgsToUkrainian("th").output, "тх");
assert.equal(adaptRtgsToUkrainian("a-1!").output, "а-1!");
assert.equal(renderRtgsUkrainianTokens([
  { kind: "thai", input: "พริก" },
  { kind: "space", input: " " },
  { kind: "latin", input: "ph" }
]), "пхрік ph", "non-Thai text must pass through unchanged");
assert.equal(renderRtgsUkrainianTokens([{ kind: "thai", input: "ทราย" }]), "⟦RTGS НЕ ПЕРЕВІРЕНО: ทราย⟧");
const sequence = romanizeRtgsTokenSequence([{ kind: "thai", input: "พริก" }]);
assert.equal(sequence[0].romanized, "phrik");
assert.equal(sequence[0].status, "transliterated");

const source = await readFile(new URL("../src/rtgs-reference.js", import.meta.url), "utf8");
assert.doesNotMatch(source, /adaptIpaToUkrainian|ipa-ua/);
assert.doesNotMatch(source, /fetch\s*\(|XMLHttpRequest/);
const app = await readFile(new URL("../src/app.js", import.meta.url), "utf8");
assert.ok(app.includes("renderRtgsTokens(tokens)"));
assert.ok(app.includes("АУДИТ IPA → УКРАЇНСЬКА"));
assert.doesNotMatch(app, /adaptIpaToUkrainian\(source\)/, "the main app must not expose a duplicate standalone IPA input path");
assert.ok(app.includes("Довідковий запис латиницею"));
assert.ok(app.includes("renderRtgsUkrainianTokens(tokens)"));
assert.doesNotMatch(source, /adaptRtgsToUkrainian|ipa-ua/, "RTGS source module remains independent of the IPA adapter");
console.log("RTGS offline port, shared IPA audit, and no-network contract: OK");
