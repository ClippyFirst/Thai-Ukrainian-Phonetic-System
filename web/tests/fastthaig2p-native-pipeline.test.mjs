import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { createFastThaiG2PNativePipeline } from "../src/fastthaig2p-native.js";

const referencePath = process.argv[2];
const dictionaryPath = process.argv[3];
const normalizerPath = process.argv[4];
const defaultWordsPath = process.argv[5];
if (!referencePath || !dictionaryPath || !normalizerPath || !defaultWordsPath) {
  throw new Error("Usage: node fastthaig2p-native-pipeline.test.mjs <reference.json> <ipa.json> <normalizer.json> <default-words.txt>");
}
const [referenceText, dictionaryText, normalizerText, defaultWordsText] = await Promise.all([
  readFile(referencePath, "utf8"),
  readFile(dictionaryPath, "utf8"),
  readFile(normalizerPath, "utf8"),
  readFile(defaultWordsPath, "utf8")
]);
const reference = JSON.parse(referenceText);
const dictionary = JSON.parse(dictionaryText);
const normalizerData = JSON.parse(normalizerText);
const defaultWords = defaultWordsText.split(/\r?\n/u).filter(Boolean);
const pipeline = createFastThaiG2PNativePipeline({ dictionary, normalizerData, defaultWords });
for (const testCase of reference.cases) {
  const result = pipeline.convert(testCase.input);
  assert.equal(result.normalized_input, testCase.normalized);
  assert.deepEqual(result.words.map(word => word.thai), testCase.tokens);
  assert.equal(result.raw_ipa, testCase.expected_ipa);
  assert.equal(result.coverage.rule_fallback_tokens, 0);
  const { normalized_input, ...serviceResult } = result;
  assert.equal(normalized_input, testCase.normalized);
  assert.deepEqual(serviceResult, testCase.expected_result, "complete service JSON parity for " + testCase.input);
}
console.log("FastThaiG2P native front-half pipeline matched " + reference.cases.length + " dictionary-only CPython cases");
