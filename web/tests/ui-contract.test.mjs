import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";

const elements = new Map();
function element(id) {
  if (!elements.has(id)) {
    elements.set(id, {
      id, value: "", hidden: true, className: "", textContent: "", innerHTML: "",
      listeners: {}, focused: false,
      addEventListener(type, callback) { this.listeners[type] = callback; },
      focus() { this.focused = true; },
      querySelectorAll() { return []; },
      click() { this.listeners.click?.({}); }
    });
  }
  return elements.get(id);
}
const examples = ["กา", "พริก", "มา", "ไฟ", "หมา", "ใหม่", "จริง"].map(example => ({
  dataset: { example }, listeners: {},
  addEventListener(type, callback) { this.listeners[type] = callback; },
  click() { this.listeners.click?.({}); }
}));

globalThis.document = {
  getElementById: element,
  querySelectorAll(selector) { return selector === "[data-example]" ? examples : []; }
};

await import("../src/app.js?ui-contract-test");

const input = element("thai-input");
const status = element("status");
const output = element("results");
const analyze = element("analyze");
const clear = element("clear");

input.value = "พริก";
analyze.click();
assert.equal(output.hidden, false);
assert.match(output.innerHTML, /Цілісний результат/);
assert.match(output.innerHTML, /Український фонетичний кандидат/);
assert.match(output.innerHTML, /IPA — проміжне представлення/);
assert.match(output.innerHTML, /<details class="analysis-details">/);
assert.match(output.innerHTML, /ФОНОЛОГІЧНА IPA/);
assert.match(output.innerHTML, /aria-labelledby=/);
assert.equal(status.className, "status");
assert.match(status.textContent, /Проаналізовано 1 токен/);

input.value = "ทดสอบ";
analyze.click();
assert.equal(status.className, "status notice");
assert.match(status.textContent, /потребують додаткової перевірки/);
assert.doesNotMatch(output.innerHTML, /ФОНОЛОГІЧНА IPA/);
assert.match(output.innerHTML, /unresolved/);

let prevented = false;
input.value = "พริก";
input.listeners.keydown({
  ctrlKey: true, metaKey: false, key: "Enter",
  preventDefault() { prevented = true; }
});
assert.equal(prevented, true);
assert.equal(status.className, "status");

for (const example of examples) {
  example.click();
  assert.equal(input.value, example.dataset.example);
  assert.equal(output.hidden, false);
  assert.match(output.innerHTML, /ФОНОЛОГІЧНА IPA/, `example ${example.dataset.example} should expose IPA`);
  assert.doesNotMatch(output.innerHTML, /segmentationStatus|unresolved:unsupported-symbol/);
}

// Source-attested lexical IPA overrides are resolved outputs too; they must
// not trigger the unresolved-token notice merely because their provenance is
// represented by a distinct segmentation status.
input.value = "เงินเดิน";
analyze.click();
assert.match(output.innerHTML, /Результат 1: เงิน/);
assert.match(output.innerHTML, /Результат 2: เดิน/);
assert.equal((output.innerHTML.match(/class="label">ФОНОЛОГІЧНА IPA<\/span>/g) || []).length, 2);
assert.equal(status.className, "status");

// A longer CC0 dictionary word must win over a supported substring.
// กาแฟ contains กา, but the engine must not claim IPA for only that substring.
input.value = "กาแฟ";
analyze.click();
assert.match(output.innerHTML, /Результат 1: กาแฟ/);
assert.doesNotMatch(output.innerHTML, /Результат 2:/);
assert.doesNotMatch(output.innerHTML, /ФОНОЛОГІЧНА IPA/);
assert.match(output.innerHTML, /unresolved/);
assert.equal(status.className, "status notice");

// Whole unspaced Thai runs must split into known lexicon entries, not be
// treated as one dictionary key. Unknown spans must not suppress adjacent IPA.
input.value = "กาไฟมา";
analyze.click();
assert.match(output.innerHTML, /Результат 1: กา/);
assert.match(output.innerHTML, /Результат 2: ไฟ/);
assert.match(output.innerHTML, /Результат 3: มา/);
assert.equal((output.innerHTML.match(/class="label">ФОНОЛОГІЧНА IPA<\/span>/g) || []).length, 3);
assert.equal(status.className, "status");

input.value = "ทดสอบกาไฟ";
analyze.click();
assert.match(output.innerHTML, /Результат 1: ทดสอบ/);
assert.match(output.innerHTML, /unresolved/);
assert.match(output.innerHTML, /Результат 2: กา/);
assert.match(output.innerHTML, /Результат 3: ไฟ/);
assert.equal((output.innerHTML.match(/class="label">ФОНОЛОГІЧНА IPA<\/span>/g) || []).length, 2);
assert.equal(status.className, "status notice");


// A reviewed full-sentence lexicon entry must preserve its reviewed syllable
// decomposition and provide IPA for each syllable without requiring spaces.
input.value = "กินข้าวกับไข่และผลไม้";
analyze.click();
assert.match(output.innerHTML, /Результат 1: กินข้าวกับไข่และผลไม้/);
assert.match(output.innerHTML, /class="continuous-output ua-continuous"[\s\S]*?<pre class="continuous-output-value">[^<]* [^<]*<\/pre>/);
assert.equal((output.innerHTML.match(/class="label">ФОНОЛОГІЧНА IPA<\/span>/g) || []).length, 7);
assert.equal(status.className, "status");

// Punctuation must delimit text runs without preventing following known words
// from being analyzed.
input.value = "กา,ไฟ!มา";
analyze.click();
assert.match(output.innerHTML, /Результат 1: กา/);
assert.match(output.innerHTML, /Токен 2: punctuation/);
assert.match(output.innerHTML, /Результат 3: ไฟ/);
assert.match(output.innerHTML, /Токен 4: punctuation/);
assert.match(output.innerHTML, /Результат 5: มา/);
assert.match(output.innerHTML, /<div class="thai">,<\/div>/);
assert.match(output.innerHTML, /<div class="thai">!<\/div>/);
assert.equal((output.innerHTML.match(/class="label">ФОНОЛОГІЧНА IPA<\/span>/g) || []).length, 3);

// Continuous output joins known syllables into words, separates adjacent
// lexical segments, preserves source punctuation/whitespace, and marks unknowns.
input.value = "กาไฟ มา!";
analyze.click();
assert.match(output.innerHTML, /กา/);
assert.match(output.innerHTML, /continuous-output-value/);
assert.match(output.innerHTML, /!/);
assert.match(output.innerHTML, /Копіювати/);
assert.match(output.innerHTML, /analysis-details/);
assert.doesNotMatch(output.innerHTML, /⟦НЕВИЗНАЧЕНО:/);

// Leading/trailing whitespace and internal spacing survive whole-text assembly.
input.value = "  กา  ไฟ!\n";
analyze.click();
assert.match(output.innerHTML, /<pre class="continuous-output-value">  กา  ไฟ!\\n<\\/pre>/);

// The continuous IPA intermediate includes tone, not only segmental phonemes.
input.value = "กา";
analyze.click();
const ipaPanel = output.innerHTML.match(/class="continuous-output ipa-continuous"[\s\S]*?<pre class="continuous-output-value">([\s\S]*?)<\/pre>/);
assert.ok(ipaPanel, "continuous IPA panel should exist");
assert.match(ipaPanel[1], /˧/, "continuous IPA should preserve the syllable tone");

input.value = "ทดสอบกาไฟ";
analyze.click();
assert.match(output.innerHTML, /⟦НЕВИЗНАЧЕНО: ทดสอบ⟧/);
assert.match(output.innerHTML, /continuous-output-value/);
assert.match(output.innerHTML, /UNRESOLVED/);

input.value = "กาไฟ มา!";
analyze.click();
assert.match(output.innerHTML, /Результат 1: กา/);
assert.match(output.innerHTML, /Результат 2: ไฟ/);
assert.match(output.innerHTML, /Результат 3: มา/);
assert.match(output.innerHTML, /!/);

clear.click();
assert.equal(input.value, "");
assert.equal(output.hidden, true);
assert.equal(status.textContent, "");
assert.equal(input.focused, true);

input.value = "ABC 123";
analyze.click();
assert.equal(status.className, "status notice");
assert.match(status.textContent, /Тайських токенів не знайдено/);
assert.match(output.innerHTML, /ABC/);
assert.match(output.innerHTML, /Тайського тексту для фонетичного перетворення не знайдено/);

const homeHtml = await readFile(new URL("../index.html", import.meta.url), "utf8");
const systemHtml = await readFile(new URL("../system.html", import.meta.url), "utf8");
const styles = await readFile(new URL("../src/styles.css", import.meta.url), "utf8");
assert.match(homeHtml, /БЕТА · ДОСЛІДНИЦЬКА ВЕРСІЯ/);
assert.match(homeHtml, /Вставте цілий текст або статтю/);
assert.match(homeHtml, /<label class="input-label" for="thai-input">Тайський текст<\/label>/);
assert.match(homeHtml, /один суцільний український кандидат/);
for (const example of examples) assert.ok(homeHtml.includes(`data-example="${example.dataset.example}"`), `homepage must expose ${example.dataset.example}`);
assert.match(homeHtml, /system\.html#beta-evidence/);
assert.match(systemHtml, /id="beta-evidence"/);
assert.match(systemHtml, /незалежно перевірених рядків — 0/);
assert.match(systemHtml, /76 із 50 000/);
assert.match(systemHtml, /16 із 50 000/);
assert.match(systemHtml, /192 із 993/);
assert.match(systemHtml, /119 із 993/);
assert.match(styles, /\.beta-notice/);
assert.match(styles, /@media\(max-width:700px\)\{\.beta-notice/);

console.log("Thai current UI uncertainty/accessibility contract passed");
