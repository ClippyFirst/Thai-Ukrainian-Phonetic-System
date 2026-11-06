import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { normalizeFastThaiG2PText } from "../src/fastthaig2p-normalizer.js";
import { createFastThaiG2PNativeTokenizer } from "../src/fastthaig2p-tokenizer.js";

const referencePath = process.argv[2];
const dataPath = process.argv[3];
const defaultWordlistPath = process.argv[4];
if (!referencePath || !dataPath || !defaultWordlistPath) {
  throw new Error("Usage: node fastthaig2p-normalizer-parity.test.mjs <python-reference.json> <normalizer-data.json> <pythainlp-default-words.txt>");
}
const reference = JSON.parse(await readFile(referencePath, "utf8"));
const data = JSON.parse(await readFile(dataPath, "utf8"));
const defaultWords = (await readFile(defaultWordlistPath, "utf8")).split(/\r?\n/u).filter(Boolean);
const defaultTokenizer = createFastThaiG2PNativeTokenizer(defaultWords);
for (const testCase of reference.cases) {
  const tokens = defaultTokenizer.tokenize(testCase.input);
  assert.deepEqual(tokens, testCase.tokens, "default PyThaiNLP newmm mismatch for " + JSON.stringify(testCase.input));
  const actual = normalizeFastThaiG2PText(testCase.input, {
    data,
    wordTokenize: () => tokens
  });
  assert.equal(actual, testCase.expected, "Normalizer mismatch for " + JSON.stringify(testCase.input));
}
console.log("FastThaiG2P native normalizer matched " + reference.cases.length + " pinned CPython cases with the extracted PyThaiNLP default wordlist");
