import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { lookupRtgsToken, renderRtgsTokens } from "../src/rtgs-reference.js";

const expected = new Map([
  ["กา", "ka"],
  ["พริก", "phrik"],
  ["มา", "ma"],
  ["ไฟ", "fai"],
  ["หมา", "ma"],
  ["ใหม่", "mai"],
]);

for (const [thai, rtgs] of expected) {
  assert.deepEqual(lookupRtgsToken(thai), {
    status: "fixture",
    value: rtgs,
    source: "provisional-fixture"
  });
}

assert.equal(lookupRtgsToken("ทดสอบ").status, "unavailable");
assert.equal(lookupRtgsToken("PHRIK").status, "unavailable");
assert.equal(lookupRtgsToken(" พริก ").status, "unavailable");
assert.equal(lookupRtgsToken("พริก").value, "phrik");

// Token kinds and boundaries come from the existing analyzer; this adapter
// neither tokenizes Thai nor feeds Latin output into the IPA→Ukrainian adapter.
assert.equal(renderRtgsTokens([
  { kind: "thai", input: "พริก" },
  { kind: "space", input: " " },
  { kind: "thai", input: "ทดสอบ" }
]), "phrik ⟦RTGS НЕ ПЕРЕВІРЕНО: ทดสอบ⟧");
assert.equal(renderRtgsTokens([{ kind: "latin", input: "ph" }]), "ph");

const rtgsSource = await readFile(new URL("../src/rtgs-reference.js", import.meta.url), "utf8");
assert.doesNotMatch(rtgsSource, /adaptIpaToUkrainian|ipa-ua/);
const appSource = await readFile(new URL("../src/app.js", import.meta.url), "utf8");
assert.match(appSource, /renderRtgsTokens\\(tokens\\)/);
assert.match(appSource, /adaptIpaToUkrainian\\(source\\)/);
assert.doesNotMatch(rtgsSource, /fetch\\(|XMLHttpRequest|https?:\\/\\//);

console.log("RTGS reference fixtures and pipeline separation: OK");
