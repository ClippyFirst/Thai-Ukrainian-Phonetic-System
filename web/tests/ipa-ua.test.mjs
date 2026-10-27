import assert from "node:assert/strict";
import fs from "node:fs";
import { adaptIpaToUkrainian } from "../src/ipa-ua.js";
import { analyze } from "../src/engine.js";

const canonical = adaptIpaToUkrainian("kʰaː");
assert.equal(canonical.status, "adapted");
assert.equal(canonical.output, "ка");
assert.deepEqual(canonical.candidates, ["ка"]);
assert(canonical.neutralizedFeatures.includes("aspiration"));
assert(canonical.neutralizedFeatures.includes("length"));
assert(canonical.rulesApplied.includes("UA-K-ASP"));

for (const [ipa, expected] of [
  ["ka", "ка"], ["kʰa", "ка"], ["kaː", "ка"],
  ["iw", "іу"], ["ew", "еу"], ["iaw", "іау"],
  ["pʰaː", "па"], ["tʰaː", "та"], ["tɕʰa", "ча"],
  ["ŋaː", "нга"], ["klaj", "клай"], ["kaw", "кау"]
]) {
  assert.equal(adaptIpaToUkrainian(ipa).output, expected, ipa);
}
assert.equal(adaptIpaToUkrainian("").status, "withheld");
assert.equal(adaptIpaToUkrainian("k☃a").status, "withheld");
assert.equal(adaptIpaToUkrainian("k☃a").output, null);
assert.equal(adaptIpaToUkrainian("kʰaː").sourceIpa, "kʰaː");

// External Thai IPA commonly adds delimiters, tone letters/diacritics, stress,
// and a tie bar. These are parsed as notation, not mistaken for unknown phones.
for (const [ipa, expected] of [
  ["[kʰaː˩˩˦]", "ка"],
  ["/kʰaː/", "ка"],
  ["kʰàː", "ка"],
  ["ˈkʰaː", "ка"],
  ["t͡ɕʰa˥", "ча"],
  ["t͜ɕʰa˦˥", "ча"],
  ["ŋɤːn˧", "нген"],
  ["k̚aː˧", "ка"]
]) {
  const adapted = adaptIpaToUkrainian(ipa);
  assert.equal(adapted.status, "adapted", ipa);
  assert.equal(adapted.output, expected, ipa);
  assert(adapted.inputNotes.length > 0, "notation should be audited: " + ipa);
}
assert.equal(adaptIpaToUkrainian("˥˩").status, "withheld");
assert.equal(adaptIpaToUkrainian("[kʰaː☃]").status, "withheld");

// End-to-end boundary proof: the browser's final Ukrainian result is the
// adaptation of the actual IPA intermediate, and a changed IPA changes output.
const endToEnd = analyze("กา");
assert.equal(endToEnd.status, "analyzed");
assert.equal(endToEnd.ukrainian, adaptIpaToUkrainian(endToEnd.phonemicIpa).output);
assert.notEqual(adaptIpaToUkrainian("ma").output, endToEnd.ukrainian);
assert.equal(adaptIpaToUkrainian("ma").output, "ма");
console.log("IPA → Ukrainian adaptation: canonical, feature-audit, inventory, and rejection tests passed");

// The public UI must describe the same IPA-first adapter contract as the engine.
const serviceHtml = fs.readFileSync(new URL("../index.html", import.meta.url), "utf8");
const systemHtml = fs.readFileSync(new URL("../system.html", import.meta.url), "utf8");
assert(serviceHtml.includes("IPA є проміжним контрольним представленням і обов’язковою межею адаптера"));
assert(serviceHtml.includes("Український кандидат формується з типізованого фонетичного результату через IPA"));
assert(!serviceHtml.includes("а не механічною заміною символів IPA"));
assert(systemHtml.includes("Український результат формується окремим шаром з IPA"));
console.log("Public UI: IPA-first adapter contract matches the implementation");


// Website contract: IPA can be supplied directly, independently of Thai input.
const ipaPanelHtml = fs.readFileSync(new URL("../index.html", import.meta.url), "utf8");
const ipaAppSource = fs.readFileSync(new URL("../src/app.js", import.meta.url), "utf8");
assert(ipaPanelHtml.includes('id="ipa-input"'));
assert(ipaPanelHtml.includes('id="ipa-adapt"'));
assert(ipaPanelHtml.includes('id="ipa-adapter-result"'));
assert(ipaAppSource.includes("adaptIpaToUkrainian(source)"));
console.log("Direct IPA input UI is wired to the same IPA → Ukrainian adapter");


// U+0306 breve can mark extra-shortness; do not silently normalize it away.
assert.equal(adaptIpaToUkrainian("kʰă").status, "withheld");
assert.equal(adaptIpaToUkrainian("kʰă").output, null);
console.log("Ambiguous breve diacritic is preserved and fails closed");
