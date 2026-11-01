import assert from "node:assert/strict";
import { analyzeText } from "../src/engine.js";
import { adaptIpaToUkrainian } from "../src/ipa-ua.js";
import { renderRtgsTokens } from "../src/rtgs-reference.js";
import { renderRtgsUkrainianTokens } from "../src/rtgs-ukrainian.js";

// Adversarial mixed-script corpus derived from real Thai orthographic hazards.
// These are runtime/contract tests, not a pronunciation gold benchmark.
const corpus = [
  "วันนี้ฉันเดินไปดูเงินที่ธนาคารแล้วถามว่าเงินจริงหรือไม่?",
  "วันจันทร์ วันศุกร์ และวันเสาร์",
  "ฉันเห็นสัตว์ในฟิล์มเรื่องหนึ่ง แต่ไม่รู้ว่ามันสร้างจากเรื่องจริงหรือไม่",
  "อย่าเพิ่งเศร้า! เธออยู่ที่ไหน อย่างไร และอยากไปไหม?",
  "ไกลกับใกล้มีเสียงต่างกันหรือไม่?",
  "ฤดูนี้มีฤทธิ์ของสมุนไพรอะไรบ้าง?",
  "ฤๅษีอธิบายทฤษฎีเรื่องเสียงไทยอย่างไร?",
  "เงิน 10 บาท + 25 บาท = 35 บาท.",
  "ก่า ก้า ก๊า ก๋า กะ กา กิ กี กึ กือ กุ กู",
  "กรุงเทพ ประเทศไทย เชียงใหม่ ภูเก็ต ขอนแก่น"
];

const modes = ["strict", "soft", "super-soft"];
let thaiTokenCount = 0;
let syllableCount = 0;
let fallbackCount = 0;

for (const source of corpus) {
  for (const mode of modes) {
    const tokens = analyzeText(source, { mode });
    const thai = tokens.filter(token => token.kind === "thai");
    assert(thai.length > 0, `No Thai tokens for ${mode}: ${source}`);
    thaiTokenCount += thai.length;

    for (const token of thai) {
      assert.equal(typeof token.input, "string");
      assert(token.input.length > 0);
      assert(Array.isArray(token.syllables));
      if (mode === "strict" && token.segmentationStatus === "unresolved") {
        assert.equal(token.syllables.length, 0, "strict mode must withhold unsegmented pronunciation");
      }
      if (mode === "super-soft") {
        assert(token.syllables.length > 0, `heuristic mode must preserve coverage: ${token.input}`);
      }

      for (const syllable of token.syllables) {
        syllableCount += 1;
        if (syllable.status === "approximate:orthographic-fallback") {
          fallbackCount += 1;
          assert.equal(syllable.evidenceStatus, "UNVERIFIED_ORTHOGRAPHIC_FALLBACK");
          assert(syllable.warnings?.length, "fallback must explain uncertainty");
          if (syllable.warnings.some(w => w.includes("структурно можливе читання"))) {
            assert.equal(syllable.tone, null, "heuristic structural fallback must not expose tone as confirmed");
            assert.equal(syllable.toneIpa, null, "heuristic structural fallback must not expose tone contour as confirmed");
            assert.equal(syllable.phoneticIpa, null, "heuristic fallback must not invent a surface-phonetic layer");
          }
        }

        if (syllable.phonemicIpa) {
          const adapted = adaptIpaToUkrainian(syllable.phonemicIpa);
          assert.equal(adapted.status, "adapted", `IPA must be accepted by adapter: ${syllable.input}`);
          assert.equal(syllable.ukrainian, adapted.output,
            `Ukrainian result must be derived from the exact IPA: ${syllable.input}`);
        }
        if (mode === "strict" && syllable.status !== "analyzed") {
          assert.equal(syllable.phonemicIpa ?? null, null, "strict mode must withhold IPA for unsupported syllables");
          assert.equal(syllable.ukrainian ?? null, null, "strict mode must withhold Ukrainian output for unsupported syllables");
        }
      }
    }
  }
}

// Explicit source-attested controls must survive all three profiles with provenance.
for (const [word, ipa, tone, ua] of [
  ["เงิน", "ŋɤn", "mid", "нген"],
  ["เดิน", "dɤːn", "mid", "ден"],
  ["ไกล", "klaj", "mid", "клай"],
  ["ใกล้", "klaj", "falling", "клай"],
  ["ออก", "ʔɔːk", "low", "ок"]
]) {
  for (const mode of modes) {
    const token = analyzeText(word, { mode }).find(item => item.kind === "thai");
    assert(token?.syllables?.length, `missing lexical control ${word} in ${mode}`);
    const syllable = token.syllables[0];
    assert.equal(syllable.phonemicIpa, ipa);
    assert.equal(syllable.tone, tone);
    assert.equal(syllable.ukrainian, ua);
    assert(syllable.sources?.length || syllable.sourceId || syllable.rulesApplied?.some(rule => rule.includes("LEXICAL-IPA-OVERRIDE")));
  }
}

// Compare both explicitly separate RTGS output paths on the same tokenization.
const rtgsTokens = analyzeText("เงินจริง วันจันทร์ ไปดู 25 บาท");
const rtgs = renderRtgsTokens(rtgsTokens);
const rtgsUa = renderRtgsUkrainianTokens(rtgsTokens);
assert.equal(typeof rtgs, "string");
assert.equal(typeof rtgsUa, "string");
assert(rtgs.length > 0 && rtgsUa.length > 0);
assert(rtgs.includes("25") && rtgsUa.includes("25"), "numbers must pass through both RTGS renderers");

// Ensure the three profiles remain distinct in their uncertainty policy.
const unresolvedSource = "ธนาคาร";
const strict = analyzeText(unresolvedSource, { mode: "strict" });
const soft = analyzeText(unresolvedSource, { mode: "soft" });
const heuristic = analyzeText(unresolvedSource, { mode: "super-soft" });
assert(strict.some(token => token.kind === "thai"));
assert(soft.some(token => token.kind === "thai"));
assert(heuristic.some(token => token.kind === "thai" && token.syllables.length > 0));
assert(fallbackCount > 0, "corpus must exercise the orthography-derived fallback path");

// These forms caused visibly malformed output in the reported run. Strict mode
// must abstain unless a reviewed lexical pronunciation is available.
for (const word of ["วันนี้", "เห็น", "เพิ่ง", "อะไร", "บ้าง", "อธิบาย"]) {
  const strictTokens = analyzeText(word, { mode: "strict" }).filter(token => token.kind === "thai");
  assert(strictTokens.length > 0, `strict mode lost Thai input: ${word}`);
  for (const token of strictTokens) {
    for (const syllable of token.syllables || []) {
      assert.equal(syllable.phonemicIpa ?? null, null, `strict mode guessed IPA for ${word}`);
      assert.equal(syllable.ukrainian ?? null, null, `strict mode guessed Ukrainian output for ${word}`);
    }
  }
  const heuristicTokens = analyzeText(word, { mode: "super-soft" }).filter(token => token.kind === "thai");
  assert(heuristicTokens.length > 0 && heuristicTokens.every(token => token.syllables.length > 0),
    `heuristic mode must preserve a visibly provisional result for ${word}`);
}

console.log(JSON.stringify({
  result: "PASS",
  corpus_cases: corpus.length,
  modes: modes.length,
  thai_tokens_seen: thaiTokenCount,
  syllables_checked: syllableCount,
  fallback_syllables_seen: fallbackCount,
  scope: "runtime and adapter-contract regression; not linguistic accuracy gold"
}, null, 2));
