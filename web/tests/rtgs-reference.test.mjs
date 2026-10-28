import assert from "node:assert/strict";
import { lookupRtgsToken, renderRtgsTokens } from "../src/rtgs-reference.js";

const expected = new Map([
  ["กา", "ka"],
  ["พริก", "phrik"],
  ["มา", "ma"],
  ["ไฟ", "fai"],
  ["หมา", "ma"],
  ["ใหม่", "mai"],
  ["จริง", "ching"]
]);

for (const [thai, rtgs] of expected) {
  assert.deepEqual(lookupRtgsToken(thai), {
    status: "reviewed",
    value: rtgs,
    source: "project-reviewed-fixture"
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

console.log("RTGS reference fixtures: OK");
