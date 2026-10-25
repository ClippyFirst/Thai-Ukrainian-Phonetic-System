import assert from "node:assert/strict";
import fs from "node:fs";
import { adaptIpaToUkrainian } from "../src/ipa-ua.js";

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
console.log("IPA → Ukrainian adaptation: canonical, feature-audit, inventory, and rejection tests passed");

// The public UI must describe the same IPA-first adapter contract as the engine.
const serviceHtml = fs.readFileSync(new URL("../index.html", import.meta.url), "utf8");
const systemHtml = fs.readFileSync(new URL("../system.html", import.meta.url), "utf8");
assert(serviceHtml.includes("IPA є проміжним контрольним представленням і обов’язковою межею адаптера"));
assert(serviceHtml.includes("Український кандидат формується з типізованого фонетичного результату через IPA"));
assert(!serviceHtml.includes("а не механічною заміною символів IPA"));
assert(systemHtml.includes("Український результат формується окремим шаром з IPA"));
console.log("Public UI: IPA-first adapter contract matches the implementation");
