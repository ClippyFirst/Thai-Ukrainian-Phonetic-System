import assert from "node:assert/strict";
import fs from "node:fs";
import { adaptIpaToUkrainian } from "../src/ipa-ua.js";
import { analyze } from "../src/engine.js";

const canonical = adaptIpaToUkrainian("kʰaː");
assert.equal(canonical.status, "adapted");
assert.equal(canonical.output, "к\u0027а");
assert.deepEqual(canonical.candidates, ["к\u0027а"]);
assert(canonical.preservedFeatures.includes("aspiration (apostrophe)"));
assert(!canonical.neutralizedFeatures.includes("aspiration"));
assert(canonical.neutralizedFeatures.includes("length"));
assert(canonical.rulesApplied.includes("UA-K-ASP"));

for (const [ipa, expected] of [
  ["ka", "ка"], ["kʰa", "к\u0027а"], ["kaː", "ка"],
  ["iw", "іу"], ["ew", "еу"], ["iaw", "іау"],
  ["pʰaː", "п\u0027а"], ["tʰaː", "т\u0027а"], ["tɕa", "ча"], ["tɕʰa", "ч\u0027а"], ["haː", "га"],
  ["ŋaː", "нга"], ["klaj", "клай"], ["kaw", "кау"]
]) {
  assert.equal(adaptIpaToUkrainian(ipa).output, expected, ipa);
}
assert.equal(adaptIpaToUkrainian("").status, "withheld");
assert.equal(adaptIpaToUkrainian("k☃a").status, "withheld");
assert.equal(adaptIpaToUkrainian("k☃a").output, null);
assert.equal(adaptIpaToUkrainian("kʰaː").sourceIpa, "kʰaː");
const thaiH = adaptIpaToUkrainian("haː");
assert.equal(thaiH.output, "га");
assert(thaiH.rulesApplied.includes("UA-H"));
assert(thaiH.neutralizedFeatures.includes("glottal place and voicing"));
assert.equal(adaptIpaToUkrainian("dʒa").status, "withheld", "voiced /dʒ/ is not a Thai affricate mapping");
for (const ipa of ["tɕa", "tɕʰa"]) {
  const affricate = adaptIpaToUkrainian(ipa);
  assert.equal(affricate.output, ipa === "tɕʰa" ? "ч\u0027а" : "ча", ipa);
  assert(!affricate.output.includes("дж"), ipa);
}

// External Thai IPA commonly adds delimiters, tone letters/diacritics, stress,
// and a tie bar. These are parsed as notation, not mistaken for unknown phones.
for (const [ipa, expected] of [
  ["[kʰaː˩˩˦]", "к\u0027а"],
  ["/kʰaː/", "к\u0027а"],
  ["kʰàː", "к\u0027а"],
  ["ˈkʰaː", "к\u0027а"],
  ["t͡ɕʰa˥", "ч\u0027а"],
  ["t͜ɕʰa˦˥", "ч\u0027а"],
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
assert(serviceHtml.includes("Як формується результат"));
assert(serviceHtml.includes("Основний шлях: тайський текст → структурний і фонологічний аналіз → IPA → адаптація до української графіки"));
assert(!serviceHtml.includes("а не механічною заміною символів IPA"));
assert(systemHtml.includes("Український результат формується окремим шаром з IPA"));
console.log("Public UI: IPA-first adapter contract matches the implementation");


// The homepage exposes the shared IPA-first pipeline, not a second input mode.
const ipaPanelHtml = fs.readFileSync(new URL("../index.html", import.meta.url), "utf8");
const ipaAppSource = fs.readFileSync(new URL("../src/app.js", import.meta.url), "utf8");
assert(!ipaPanelHtml.includes('id="ipa-input"'));
assert(!ipaPanelHtml.includes('id="ipa-adapt"'));
assert(!ipaPanelHtml.includes('id="ipa-adapter-result"'));
assert(ipaAppSource.includes("АУДИТ IPA → УКРАЇНСЬКА"));
assert(!ipaAppSource.includes("adaptIpaToUkrainian(source)"));
console.log("Homepage uses the main IPA-first pipeline; no duplicate IPA input mode");
