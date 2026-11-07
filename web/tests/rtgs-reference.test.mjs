import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { romanizeRtgsWord, romanizeRtgsWords, renderRtgsTokens, romanizeRtgsTokenSequence } from "../src/rtgs-reference.js";
import { adaptRtgsToUkrainian, renderRtgsUkrainianTokens } from "../src/rtgs-ukrainian.js";

const examples = new Map([
  ["กา", "ka"], ["พริก", "phrik"], ["มา", "ma"], ["ไฟ", "fai"], ["หมา", "ma"], ["ใหม่", "mai"], ["ไหม", "mai"], ["เหงา", "ngao"], ["ใกล้", "klai"], ["ใคร", "khrai"], ["จริง", "ching"], ["สามารถ", "samat"], ["สวัสดี", "sawatdi"], ["สร้าง", "sang"], ["ศรี", "si"], ["เศร้า", "sao"], ["ไซร้", "sai"], ["ทรง", "song"], ["ทราม", "sam"], ["พัฒนา", "phatthana"], ["ฤทธิ์", "rit"], ["ฤๅ", "rue"], ["รถไฟ", "rotfai"], ["ผลไม้", "phonlamai"], ["ยูเครน", "yukhren"], ["ทราบ", "sap"], ["ทรัพย์", "sap"], ["แทรก", "saek"], ["อักษร", "akson"]
]);
for (const [thai, expected] of examples) {
  const result = romanizeRtgsWord(thai);
  assert.equal(result.status, "transliterated", thai);
  assert.equal(result.value, expected, thai);
  assert.equal(result.source, "PyThaiNLP 5.4.0 royin port + ClippyFirst orthographic correction");
}
assert.equal(romanizeRtgsWord("กรุงเทพมหานคร").value, "krung thep maha nakhon", "Bangkok's official RTGS name must preserve all four lexical components");
assert.equal(romanizeRtgsWord("กรุงเทพมหานคร").source, "Royal Society of Thailand official proper-name form");
assert.equal(romanizeRtgsTokenSequence([
  { kind: "thai", input: "กรุงเทพ" },
  { kind: "thai", input: "มหานคร" }
]).map(item => item.value).join(""), "krung thep maha nakhon", "reviewed proper names must survive tokenizer boundary splits");
const separatedBangkokParts = romanizeRtgsTokenSequence([
  { kind: "thai", input: "กรุงเทพ" },
  { kind: "space", input: " " },
  { kind: "thai", input: "มหานคร" }
]);
assert.equal(separatedBangkokParts.length, 3, "lexical merging must not cross whitespace boundaries");
assert.notEqual(separatedBangkokParts[0].input + separatedBangkokParts[2].input, "กรุงเทพมหานคร");
assert.equal(romanizeRtgsWord("test").status, "unavailable");
assert.equal(romanizeRtgsWord("").status, "unavailable");
assert.equal(romanizeRtgsWord("ห").value, "");
assert.equal(romanizeRtgsWord("ให้").value, "hai");
assert.equal(romanizeRtgsWord("ทราย").status, "unavailable");
assert.equal(romanizeRtgsWord("ฦ").status, "unavailable");
assert.equal(romanizeRtgsWord("ๆ").status, "unavailable");
assert.equal(romanizeRtgsWord("ฯ").status, "unavailable");
assert.equal(romanizeRtgsWord("สตรีเศรษฐบุตรบำเพ็ญ").status, "unavailable");
assert.equal(romanizeRtgsWord("พริก").value, "phrik");
assert.equal(romanizeRtgsWords(["กา", "กร"]).length > 0, true);

// Existing analyzer token boundaries are preserved; the RTGS output is never
// fed to the IPA→Ukrainian adapter and non-Thai tokens are passed through.
assert.equal(renderRtgsTokens([
  { kind: "thai", input: "พริก" },
  { kind: "space", input: " " },
  { kind: "latin", input: "ph" }
]), "phrik ph");
assert.equal(renderRtgsTokens([{ kind: "thai", input: "ทราย" }]), "⟦RTGS НЕ ПЕРЕВІРЕНО: ทราย⟧");

// RTGS roman letters are mapped as a separate orthographic method, not via IPA.
for (const [input, expected] of [
  ["phrik", "пхрік"], ["khrai", "кхрай"], ["th", "тх"], ["ch", "ч"],
  ["ngao", "нгау"], ["sawatdi", "саватді"], ["mai", "май"],
  ["ai", "ай"], ["ueai", "иай"], ["uai", "уай"], ["oei", "ей"],
  ["aeo", "еу"], ["iao", "іау"], ["ue", "и"], ["ae", "е"], ["oe", "е"],
  ["io", "іу"], ["eo", "еу"], ["ao", "ау"], ["yukhren", "юкхрен"],
  ["phatthana", "пхаттхана"], ["sip-hok", "сіп-хок"]
]) {
  assert.equal(adaptRtgsToUkrainian(input).status, "adapted", input);
  assert.equal(adaptRtgsToUkrainian(input).output, expected, input);
}
assert.equal(adaptRtgsToUkrainian("zoo").status, "unavailable", "unsupported RTGS letters must fail closed");
assert.equal(romanizeRtgsWord("เกาะ").value, "ko", "the RTGS /ɔ/ rime must win over the later short-e fallback pattern");
assert.equal(adaptRtgsToUkrainian("ko").output, "ко");
assert.equal(adaptRtgsToUkrainian("h").output, "х", "standalone RTGS h is represented as Ukrainian х");
assert.equal(adaptRtgsToUkrainian("rue").output, "ри");
assert.equal(adaptRtgsToUkrainian("ri").output, "рі");
assert.equal(adaptRtgsToUkrainian("rit").output, "ріт");
assert.equal(adaptRtgsToUkrainian("kh").output, "кх");
assert.equal(adaptRtgsToUkrainian("ph").output, "пх");
assert.equal(adaptRtgsToUkrainian("th").output, "тх");
assert.equal(adaptRtgsToUkrainian("a-1!").output, "а-1!");
assert.equal(renderRtgsUkrainianTokens([
  { kind: "thai", input: "พริก" },
  { kind: "space", input: " " },
  { kind: "latin", input: "ph" }
]), "пхрік ph", "non-Thai text must pass through unchanged");
assert.equal(renderRtgsUkrainianTokens([{ kind: "thai", input: "ทราย" }]), "⟦RTGS НЕ ПЕРЕВІРЕНО: ทราย⟧");
const sequence = romanizeRtgsTokenSequence([{ kind: "thai", input: "พริก" }]);
assert.equal(sequence[0].romanized, "phrik");
assert.equal(sequence[0].status, "transliterated");

const adapterSource = await readFile(new URL("../src/rtgs-ukrainian.js", import.meta.url), "utf8");
assert.doesNotMatch(adapterSource, /adaptIpaToUkrainian|ipa-ua/, "RTGS → Ukrainian adapter must remain independent of IPA");
assert.match(adapterSource, /RIME_SEQUENCES/);
const matrices = await readFile(new URL("../../docs/ukrainian-correspondence-matrices.md", import.meta.url), "utf8");
const vowelRegistry = (await readFile(new URL("../../data/thai/vowels.csv", import.meta.url), "utf8"))
  .trim().split(/\r?\n/).slice(1).map(line => line.split(","));
const vowelSource = new Map(vowelRegistry.map(row => [row[0], { pattern: row[1], ipa: row[2] }]));
const phoneticRimeMatrix = matrices.split("## 3. Фонетична матриця: голосні та рими")[1].split("## 4.")[0];
const rtgsRimeMatrix = matrices.split("## 5. Романізаційна матриця: рими")[1].split("## 6.")[0];
assert.equal((phoneticRimeMatrix.match(/^\| V-/gm) || []).length, 41, "phonetic matrix must cover all 41 registered rimes");
assert.equal((rtgsRimeMatrix.match(/^\| V-/gm) || []).length, 41, "RTGS matrix must cover all 41 registered rimes");
for (const [section, hasIpa] of [[phoneticRimeMatrix, true], [rtgsRimeMatrix, false]]) {
  const rows = [...section.matchAll(/^\| (V-[^|]+) \| ([^|]+) \| ([^|]+) \|/gm)];
  assert.equal(rows.length, 41);
  for (const row of rows) {
    const sourceRow = vowelSource.get(row[1].trim());
    assert.ok(sourceRow, "missing source vowel ID " + row[1]);
    assert.equal(row[2].trim(), sourceRow.pattern, "Thai pattern drift for " + row[1]);
    if (hasIpa) assert.equal(row[3].trim().replace(/^\//, "").replace(/\/$/, ""), sourceRow.ipa, "IPA drift for " + row[1]);
  }
}
const consonantRegistry = (await readFile(new URL("../../data/thai/consonants.csv", import.meta.url), "utf8"))
  .trim().split(/\r?\n/).slice(1).map(line => line.split(","));
const onsetMatrix = matrices.split("### 2.1 Початок складу (onset)")[1].split("### 2.2")[0];
const onsetGraphemes = [...onsetMatrix.matchAll(/^\| ([ก-๛ ]+) \|/gm)].flatMap(match => match[1].trim().split(/\s+/));
assert.deepEqual(new Set(onsetGraphemes), new Set(consonantRegistry.map(row => row[1])), "onset matrix must inventory all source consonants");
const onsetSource = new Map(consonantRegistry.map(row => [row[1], row[4]]));
const onsetRows = [...onsetMatrix.matchAll(/^\| ([ก-๛ ]+) \| ([^|]+) \|/gm)];
for (const row of onsetRows) {
  const ipa = row[2].trim().replace(/^\//, "").replace(/\/$/, "");
  for (const grapheme of row[1].trim().split(/\s+/)) {
    if (grapheme === "อ") continue; // carrier can be a glottal onset or zero onset by structural role
    assert.equal(onsetSource.get(grapheme), ipa, "onset IPA drift for " + grapheme);
  }
}
const codaMatrix = matrices.split("### 2.2 Кінець складу (coda)")[1].split("## 3.")[0];
const codaGraphemes = [...codaMatrix.matchAll(/^\| ([ก-๛ ]+) \|/gm)].flatMap(match => match[1].trim().split(/\s+/));
assert.deepEqual(new Set(codaGraphemes), new Set(consonantRegistry.filter(row => row[6] === "true").map(row => row[1])), "coda matrix must match source coda_allowed inventory");
const codaSource = new Map(consonantRegistry.map(row => [row[1], row[5]]));
const codaRows = [...codaMatrix.matchAll(/^\| ([ก-๛ ]+) \| ([^|]+) \|/gm)];
for (const row of codaRows) {
  const ipa = row[2].trim().replace(/^\//, "").replace(/\/$/, "");
  for (const grapheme of row[1].trim().split(/\s+/)) {
    assert.equal(codaSource.get(grapheme), ipa, "coda IPA drift for " + grapheme);
  }
}
const rtgsOnsetMatrix = matrices.split("### 4.1 Початок складу")[1].split("### 4.2")[0];
const rtgsOnsetGraphemes = [...rtgsOnsetMatrix.matchAll(/^\| ([ก-๛ ]+) \|/gm)].flatMap(match => match[1].trim().split(/\s+/));
assert.deepEqual(new Set(rtgsOnsetGraphemes), new Set(consonantRegistry.map(row => row[1])), "RTGS onset matrix must inventory all source consonants");
const rtgsCodaMatrix = matrices.split("### 4.2 Кінець складу")[1].split("## 5.")[0];
const rtgsCodaGraphemes = [...rtgsCodaMatrix.matchAll(/^\| ([ก-๛ ]+) \|/gm)].flatMap(match => match[1].trim().split(/\s+/));
assert.deepEqual(new Set(rtgsCodaGraphemes), new Set(consonantRegistry.filter(row => row[6] === "true").map(row => row[1])), "RTGS coda matrix must cover the same positional inventory");
for (const [input, expected] of [
  ["ueai", "иай"], ["iao", "іау"], ["aeo", "еу"], ["oei", "ей"],
  ["uai", "уай"], ["uea", "иа"], ["ai", "ай"], ["am", "ам"],
  ["ao", "ау"], ["io", "іу"], ["ui", "уй"], ["eo", "еу"],
  ["oi", "ой"], ["ia", "іа"], ["ue", "и"], ["oe", "е"],
  ["ae", "е"], ["ua", "уа"]
]) {
  assert.equal(adaptRtgsToUkrainian(input).output, expected, input);
}
for (const [input, expected] of [["ya", "я"], ["ye", "є"], ["yi", "ї"], ["yo", "йо"], ["yu", "ю"]]) {
  assert.equal(adaptRtgsToUkrainian(input).output, expected, input);
}
const source = await readFile(new URL("../src/rtgs-reference.js", import.meta.url), "utf8");
assert.doesNotMatch(source, /adaptIpaToUkrainian|ipa-ua/);
assert.doesNotMatch(source, /fetch\s*\(|XMLHttpRequest/);
const app = await readFile(new URL("../src/app.js", import.meta.url), "utf8");
assert.ok(app.includes("new Worker("), "the public app must use the local FastThaiG2P worker");
assert.ok(app.includes("fastthaig2p-worker.js"), "the public app must load the Pyodide worker");
assert.equal(app.includes("fetch("), false, "the public app must not send Thai text to an API");
assert.match(app, /import\("\.\/rtgs-romanizer\.js"\)/, "RTGS must be exposed only through the separately labelled optional romanizer");
assert.doesNotMatch(app, /renderRtgsTokens|renderRtgsUkrainianTokens|adaptRtgsToUkrainian|rtgs-ukrainian/);
assert.doesNotMatch(app, /analyzeText|analyze\(/, "the browser must not execute a second G2P engine");
assert.doesNotMatch(app, /adaptIpaToUkrainian\(source\)/, "the browser must not expose a parallel IPA input path");
assert.doesNotMatch(source, /adaptRtgsToUkrainian|ipa-ua/, "RTGS source module remains independent of the IPA adapter");
// The published method matrices must stay executable specifications: every
// displayed RTGS → Ukrainian value is checked against the actual adapter.
const rtgsRimeTable = matrices
  .split("## 5. Романізаційна матриця: рими")[1]
  .split("### 5.1")[0];
const rtgsRimeRows = [...rtgsRimeTable.matchAll(/^\| (V-[^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|$/gm)];
assert.equal(rtgsRimeRows.length, 41, "all registered RTGS rime rows must be checked against the adapter");
for (const row of rtgsRimeRows) {
  const rtgs = row[3].trim();
  const ukrainian = row[4].trim();
  assert.equal(adaptRtgsToUkrainian(rtgs).status, "adapted", "RTGS matrix rime must be supported: " + row[1]);
  assert.equal(adaptRtgsToUkrainian(rtgs).output, ukrainian, "RTGS matrix Ukrainian rime output drift: " + row[1]);
}

const rtgsOnsetRows = [...rtgsOnsetMatrix.matchAll(/^\| ([ก-๛ ]+) \| ([^|]+) \| ([^|]+) \|/gm)];
for (const row of rtgsOnsetRows) {
  const rtgs = row[2].trim();
  const ukrainian = row[3].trim();
  if (rtgs === "—") continue;
  assert.equal(adaptRtgsToUkrainian(rtgs).output, ukrainian, "RTGS onset matrix output drift: " + row[1]);
}
const rtgsCodaRows = [...rtgsCodaMatrix.matchAll(/^\| ([ก-๛ ]+) \| ([^|]+) \| ([^|]+) \|/gm)];
for (const row of rtgsCodaRows) {
  const rtgs = row[2].trim();
  const ukrainian = row[3].trim();
  if (rtgs === "—") continue;
  assert.equal(adaptRtgsToUkrainian(rtgs).output, ukrainian, "RTGS coda matrix output drift: " + row[1]);
}

const rtgsSequenceMatrix = matrices.split("## 6. RTGS-склади та рими → українська")[1].split("## 7.")[0];
const rtgsSequenceRows = [...rtgsSequenceMatrix.matchAll(/^\| ([a-z]+) \| ([^|]+) \|/gm)];
assert.ok(rtgsSequenceRows.length >= 25, "RTGS digraph/rime sequence table must remain populated");
for (const row of rtgsSequenceRows) {
  const sequence = row[1].trim();
  const ukrainian = row[2].trim();
  assert.equal(adaptRtgsToUkrainian(sequence).output, ukrainian, "RTGS sequence table output drift: " + sequence);
}

console.log("RTGS offline port, shared IPA audit, and no-network contract: OK");
