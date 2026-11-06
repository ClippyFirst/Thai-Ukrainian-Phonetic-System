import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { normalizeFastThaiG2PText } from "../src/fastthaig2p-normalizer.js";

const referencePath = process.argv[2];
const dataPath = process.argv[3];
if (!referencePath || !dataPath) {
  throw new Error("Usage: node fastthaig2p-normalizer-parity.test.mjs <python-reference.json> <normalizer-data.json>");
}
const reference = JSON.parse(await readFile(referencePath, "utf8"));
const data = JSON.parse(await readFile(dataPath, "utf8"));
for (const testCase of reference.cases) {
  const actual = normalizeFastThaiG2PText(testCase.input, {
    data,
    wordTokenize: () => testCase.tokens
  });
  assert.equal(actual, testCase.expected, `Normalizer mismatch for ${JSON.stringify(testCase.input)}`);
}
console.log(`FastThaiG2P native normalizer matched ${reference.cases.length} pinned CPython cases`);
