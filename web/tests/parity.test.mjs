import fs from "node:fs";
import {analyze} from "../src/engine.js";

const fixture = JSON.parse(fs.readFileSync(new URL("./fixtures.json", import.meta.url), "utf8"));
if (!Array.isArray(fixture) || fixture.length < 20) throw new Error("Parity fixture set is unexpectedly small");

const seen = new Set();
if (!fixture.some(x => x.input === "กฉ") || !fixture.some(x => x.input === "กผ")) throw new Error("coda-license regression probes are missing");
const pick = a => ({
  input: a.input,
  status: a.status,
  phonemicIpa: a.phonemicIpa ?? null,
  phoneticIpa: a.phoneticIpa ?? null,
  tone: a.tone ?? null,
  toneIpa: a.toneIpa ?? null,
  ukrainian: a.ukrainian ?? null,
});

let failures = 0;
for (const row of fixture) {
  if (!row?.input || seen.has(row.input)) {
    console.error("duplicate/invalid fixture:", row?.input);
    failures++;
    continue;
  }
  seen.add(row.input);
  const got = pick(analyze(row.input));
  for (const key of Object.keys(got)) {
    if (got[key] !== row.expected?.[key]) {
      console.error(row.input, key, JSON.stringify(got[key]), JSON.stringify(row.expected?.[key]));
      failures++;
    }
  }
}
if (failures) throw new Error(failures + " parity assertions failed");
console.log("web/python parity: " + fixture.length + " fixtures passed");
