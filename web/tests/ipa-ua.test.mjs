import assert from "node:assert/strict";
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
