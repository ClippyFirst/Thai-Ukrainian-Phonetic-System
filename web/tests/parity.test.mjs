import fs from "node:fs";
import {analyze,analyzeText} from "../src/engine.js";

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


const textRegression = analyzeText("กากล้าขายแล้วไหว้แสดง, Bangkok 123 ๆ");
const thaiToken = textRegression.find(x => x.kind === "thai");
if (!thaiToken || thaiToken.segmentationStatus !== "lexicon") throw new Error("Thai text segmentation regression failed");
if (thaiToken.syllables.map(x => x.input).join("|") !== "กา|กล้า|ขาย|แล้ว|ไหว้|แส|ดง") throw new Error("Unexpected Thai syllable segmentation");
if (!textRegression.some(x => x.kind === "latin" && x.input === "Bangkok")) throw new Error("Latin tokenization regression failed");
if (!textRegression.some(x => x.kind === "number" && x.input === "123")) throw new Error("Number tokenization regression failed");
if (!textRegression.some(x => x.kind === "thai_marker" && x.input === "ๆ")) throw new Error("Thai repetition-marker tokenization regression failed");
console.log("Thai text tokenizer/segmentation regression passed");

const lexicalRegression = ["จริง","สร้าง","เศร้า","จันทร์","ศุกร์","เสาร์","สัตว์","ฟิล์ม","ฤทธิ์","อย่า","อยู่","อยาก"];
for (const input of lexicalRegression) {
  const a = analyze(input);
  if (a.status !== "analyzed" || !a.phonemicIpa) throw new Error("Lexical regression unresolved in browser engine: " + input);
}
console.log("Thai lexical regression passed");

const textLexiconRegression = new Map([
  ["ทฤษฎี","ทริด|สะ|ดี"], ["คอมพิวเตอร์","คอม|พิว|เตอร์"], ["โทรศัพท์","โท|ระ|สับ"],
  ["อยาก","หยาก"], ["ฤๅษี","รือ|สี"]
]);
for (const [input, expected] of textLexiconRegression) {
  const token = analyzeText(input)[0];
  if (!token || token.segmentationStatus !== "lexicon" || token.syllables.map(x => x.input).join("|") !== expected) {
    throw new Error("Text lexicon regression failed: " + input);
  }
}
console.log("Thai extended text lexicon regression passed");
