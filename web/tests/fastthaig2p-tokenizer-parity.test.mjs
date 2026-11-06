import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { createFastThaiG2PNativeTokenizer } from "../src/fastthaig2p-tokenizer.js";

const referencePath = process.argv[2];
const dictionaryPath = process.argv[3];
if (!referencePath || !dictionaryPath) {
  throw new Error("Usage: node fastthaig2p-tokenizer-parity.test.mjs <python-reference.json> <ipa-dictionary.json>");
}
const reference = JSON.parse(await readFile(referencePath, "utf8"));
const dictionary = JSON.parse(await readFile(dictionaryPath, "utf8"));
const tokenizer = createFastThaiG2PNativeTokenizer(Object.keys(dictionary));
assert.equal(tokenizer.dictionarySize, Object.keys(dictionary).length);
for (const testCase of reference.cases) {
  assert.deepEqual(
    tokenizer.tokenize(testCase.normalized),
    testCase.expected,
    "newmm tokenization mismatch for " + JSON.stringify(testCase.input)
  );
}
console.log("FastThaiG2P native newmm matched " + reference.cases.length + " pinned PyThaiNLP cases");
