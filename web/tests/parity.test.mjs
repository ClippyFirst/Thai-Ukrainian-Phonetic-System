import fs from "node:fs";
import {analyze,analyzeText,tokenizeText} from "../src/engine.js";

const fixture = JSON.parse(fs.readFileSync(new URL("./fixtures.json", import.meta.url), "utf8"));
if (!Array.isArray(fixture) || fixture.length < 27) throw new Error("Parity fixture set is unexpectedly small");

const seen = new Set();
const required = ["กฉ","กผ","จริง","สร้าง","เศร้า","ไซร้","ไกล","ใกล้","ไก่"];
if (required.some(input => !fixture.some(x => x.input === input))) throw new Error("required linguistic regression probes are missing");
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


const textRegression = analyzeText("ครอบครัว, รถบัส Bangkok 123 ๆ");
const thaiTokens = textRegression.filter(x => x.kind === "thai");
if (thaiTokens.length !== 2 || thaiTokens.some(x => x.segmentationStatus !== "lexicon")) throw new Error("Thai text segmentation regression failed");
if (thaiTokens[0].syllables.map(x => x.input).join("|") !== "ครอบ|ครัว") throw new Error("Unexpected ครอบครัว segmentation");
if (thaiTokens[1].syllables.map(x => x.input).join("|") !== "รถ|บัส") throw new Error("Unexpected รถบัส segmentation");
const unknown = analyzeText("กากล้าขายแล้วไหว้แสดง")[0];
if (unknown.segmentationStatus !== "unresolved" || unknown.syllables.length !== 0 || !unknown.warnings.some(x => x.includes("IPA and Ukrainian output are withheld"))) throw new Error("Unknown continuous Thai text leaked a whole-word phonetic result without segmentation");
if (!textRegression.some(x => x.kind === "latin" && x.input === "Bangkok")) throw new Error("Latin tokenization regression failed");
if (!textRegression.some(x => x.kind === "number" && x.input === "123")) throw new Error("Number tokenization regression failed");
if (!textRegression.some(x => x.kind === "thai_marker" && x.input === "ๆ")) throw new Error("Thai repetition-marker tokenization regression failed");
const ua = analyze("กวน");
if (ua.status !== "analyzed" || ua.onset.join("") !== "ก" || ua.coda !== "น" || !ua.phonemicIpa.endsWith("n") || !ua.ukrainian.endsWith("н")) throw new Error("Medial ua glide/coda regression failed");
const cold = analyze("หนาว");
if (cold.status !== "analyzed" || cold.onset.join("") !== "หน" || cold.coda !== null || cold.phonemicIpa !== "naːw" || cold.ukrainian !== "нау") throw new Error("Leading ห + vowel-glide regression failed");
const star = analyze("ดาว");
if (star.status !== "analyzed" || star.onset.join("") !== "ด" || star.coda !== null || star.phonemicIpa !== "daːw" || star.ukrainian !== "дау") throw new Error("Terminal ว nucleus regression failed");
for (const text of ["แสดง", "กกรกา"]) {
  const a = analyze(text);
  if (a.status !== "unresolved:nonconforming-consonant-sequence" || a.phonemicIpa !== null) throw new Error("Illegal multi-consonant onset was accepted: " + text);
}
const pepper = analyzeText("พริก")[0];
if (!pepper || pepper.segmentationStatus !== "lexicon" || pepper.syllables[0].phonemicIpa?.slice(-1) !== "k" || pepper.syllables[0].ukrainian?.slice(-1) !== "к") throw new Error("Thai final /k/ regression failed for พริก");
console.log("Thai text tokenizer/segmentation regression passed");

const lexicalRegression = ["จริง","สร้าง","ศรี","ทราบ","ทรง","ทรัพย์","แทรก","เศร้า","จันทร์","ศุกร์","เสาร์","สัตว์","ฟิล์ม","ฤทธิ์","เตอร์","เทอร์","ยนต์","ไซต์","กอล์ฟ","อย่า","อยู่","อย่าง","อยาก"];
for (const input of lexicalRegression) {
  const a = analyze(input);
  if (a.status !== "analyzed" || !a.phonemicIpa) throw new Error("Lexical regression unresolved in browser engine: " + input);
  if (input === "ศรี" && (a.normalized !== "สี" || a.phonemicIpa !== "siː" || a.ukrainian !== "сі")) throw new Error("Thai false-cluster lexical reading mismatch for ศรี");
  if (input === "แทรก" && (a.normalized !== "แซก" || a.phonemicIpa !== "sɛːk" || a.coda !== "ก")) throw new Error("Thai preposed-vowel false-cluster coda mismatch for แทรก");
  if (input === "อย่าง" && a.normalized !== "หย่าง") throw new Error("Thai lexical normalization mismatch for อย่าง");
  if (input === "เตอร์" && a.normalized !== "เตอ") throw new Error("Thai lexical normalization mismatch for เตอร์");
}
const ambiguousThray = analyze("ทราย");
if (ambiguousThray.status !== "analysis-dependent:special-orthography" || ambiguousThray.phonemicIpa != null || ambiguousThray.ukrainian != null || !ambiguousThray.specialAnalyses?.some(x => x.rule_id === "SP-THR-001")) {
  throw new Error("Sense-ambiguous ทราย must not receive an unconditional false-cluster reading: " + JSON.stringify(ambiguousThray));
}
console.log("Thai lexical regression passed");

const textLexiconRegression = new Map([
  ["ทฤษฎี","ทริด|สะ|ดี"], ["คอมพิวเตอร์","คอม|พิว|เตอร์"], ["โทรศัพท์","โท|ระ|สับ"],
  ["อยาก","หยาก"], ["ฤๅษี","รือ|สี"], ["ทราบ","ทราบ"], ["ทราย","ทราย"], ["ทรง","ทรง"], ["ทรัพย์","ทรัพย์"], ["แทรก","แทรก"]
]);
for (const [input, expected] of textLexiconRegression) {
  const token = analyzeText(input)[0];
  if (!token || token.segmentationStatus !== "lexicon" || token.syllables.map(x => x.input).join("|") !== expected) {
    throw new Error("Text lexicon regression failed: " + input);
  }
}
console.log("Thai extended text lexicon regression passed");

const unicodeHazards = [
  ["กา\u0001", "U+0001"],
  ["กา\u007f", "U+007F"],
  ["กา\u0085", "U+0085"],
  ["กา\u200b", "U+200B"],
  ["กา\u202e", "U+202E"],
];
for (const [input, codepoint] of unicodeHazards) {
  const result = analyze(input);
  if (result.status !== "unresolved:unsupported-symbol" ||
      result.phonemicIpa != null || result.phoneticIpa != null ||
      result.ukrainian != null) {
    throw new Error("Unsupported Unicode control/format character leaked a Thai result (" + codepoint + "): " + JSON.stringify(result));
  }
}
const normalizedThai = analyze("  ก่า  ");
if (normalizedThai.normalized !== "ก่า" || normalizedThai.phonemicIpa == null) {
  throw new Error("Thai NFC/trim normalization contract regressed");
}
console.log("Thai Unicode normalization and malformed-input contract passed");

const nelTokens = tokenizeText("\u0085กา\u0085");
if (nelTokens.map(token => token.kind + ":" + token.input).join("|") !== "punctuation:\u0085|thai:กา|punctuation:\u0085") {
  throw new Error("Thai tokenizer silently treated U+0085 as layout whitespace: " + JSON.stringify(nelTokens));
}

const asciiBoundaryTokens = analyzeText(" \tกา\r\nขา ").filter(token => token.kind === "thai");
if (asciiBoundaryTokens.map(token => token.input).join("|") !== "กา|ขา" ||
    asciiBoundaryTokens.some(token => token.syllables.length !== 1 || token.syllables[0].status !== "analyzed")) {
  throw new Error("Thai ASCII layout whitespace did not preserve two independently analyzed tokens");
}
for (const control of ["\u000b", "\u000c"]) {
  const result = analyze("กา" + control + "ขา");
  if (result.status !== "unresolved:unsupported-symbol" || result.phonemicIpa != null || result.phoneticIpa != null || result.ukrainian != null) {
    throw new Error("Thai parser accepted unsupported layout control U+" + control.codePointAt(0).toString(16) + ": " + JSON.stringify(result));
  }
}


for (const spelling of ["ฤ", "ฤๅ", "ฦ", "ฦๅ"]) {
  const result = analyze(spelling);
  if (result.status !== "analysis-dependent:special-orthography" ||
      result.phonemicIpa != null || result.phoneticIpa != null || result.ukrainian != null ||
      !result.specialAnalyses?.length) {
    throw new Error("Thai special vowel letter was assigned a lexical reading without word evidence: " + spelling + ": " + JSON.stringify(result));
  }
}
console.log("Thai special vowel-letter uncertainty contract passed");
