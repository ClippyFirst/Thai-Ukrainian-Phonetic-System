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
assert.match(output.innerHTML, /RTGS — латинська романізація \(не IPA\)/);
assert.match(output.innerHTML, /phrik/);
assert.match(output.innerHTML, /RTGS не позначає тон/);
assert.match(output.innerHTML, /довготу голосних/);
assert.match(output.innerHTML, /<details class="analysis-details">/);
assert.match(output.innerHTML, /ФОНОЛОГІЧНА IPA/);
assert.match(output.innerHTML, /aria-labelledby=/);
assert.equal(status.className, "status");
assert.match(status.textContent, /Проаналізовано 1 токен/);

input.value = "ทดสอบ";
analyze.click();
assert.match(output.innerHTML, /RTGS НЕ ПЕРЕВІРЕНО/);
assert.equal(status.className, "status notice");
assert.match(status.textContent, /потребують перевірки або залишилися невизначеними/);
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

// The source-attested Thai name ยูเครน is split at its documented syllable
// boundary. Both IPA syllables must be exposed; the whole proper name must not
// fall through to the unresolved OOV path.
input.value = "ยูเครน";
analyze.click();
assert.match(output.innerHTML, /Результат 1: ยูเครน/);
assert.match(output.innerHTML, /juː/);
assert.match(output.innerHTML, /kʰreːn/);
assert.match(output.innerHTML, /continuous-output-value[^>]*>йукрен<\/pre>/);
assert.equal((output.innerHTML.match(/class="label">ФОНОЛОГІЧНА IPA<\/span>/g) || []).length, 2);
assert.equal(status.className, "status");

// Source-attested three-syllable direction name; each IPA syllable must
// flow through the same adapter into the continuous Ukrainian candidate.
input.value = "ตะวันออก";
analyze.click();
assert.match(output.innerHTML, /Результат 1: ตะวันออก/);
assert.match(output.innerHTML, /ta/);
assert.match(output.innerHTML, /wan/);
assert.match(output.innerHTML, /ʔɔːk/);
assert.match(output.innerHTML, /continuous-output-value[^>]*>таванок<\/pre>/);
assert.equal((output.innerHTML.match(/class="label">ФОНОЛОГІЧНА IPA<\/span>/g) || []).length, 3);

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


// A curated full-sentence lexicon entry must preserve its reviewed syllable
// decomposition and provide IPA for each syllable without requiring spaces.
input.value = "กินข้าวกับไข่และผลไม้";
analyze.click();
assert.match(output.innerHTML, /Результат 1: กินข้าวกับไข่และผลไม้/);
const phraseUa = output.innerHTML.match(/class="continuous-output ua-continuous"[\s\S]*?<pre class="continuous-output-value">([^<]*)<\/pre>/);
assert.ok(phraseUa, "continuous Ukrainian output should exist for the curated phrase");
assert.equal((phraseUa[1].match(/ /g) || []).length, 5, "curated phrase should preserve its six word groups, not insert spaces between all seven syllables");
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
assert.match(output.innerHTML, /<pre class="continuous-output-value">  ка  фай!\n<\/pre>/);

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

// Soft mode is opt-in: it broadens unknown spans into structural syllable
// candidates, while preserving explicit uncertainty and the IPA→Ukrainian path.
const mode = element("engine-mode");
mode.value = "soft";
input.value = "ทดสอบกาไฟ";
analyze.click();
assert.match(status.textContent, /М’який/);
assert.equal(status.className, "status notice", "soft mode must visibly remain provisional even when every parsed syllable has a candidate");
assert.match(output.innerHTML, /soft-orthographic-clusters/);
assert.match(output.innerHTML, /М’який режим — попередній результат/);
assert.match(output.innerHTML, /IPA — проміжне представлення/);
assert.match(output.innerHTML, /<pre class="continuous-output-value">[^<]*(?:ка|фай)/, "soft mode should emit a recoverable Ukrainian candidate for recognized/structurally parsed spans");
mode.value = "super-soft";
input.value = "ดินแดนที่เป็นประเทศยูเครนสมัยใหม่ ค.ศ. 1917, ฮอลอดอมอร์!";
analyze.click();
assert.match(status.textContent, /Суперм’який/);
assert.match(output.innerHTML, /Суперм’який режим — повне покриття, приблизна вимова/);
assert.match(output.innerHTML, /IPA — проміжне представлення/);
const superSoftUa = output.innerHTML.match(/class="continuous-output ua-continuous".*?<pre class="continuous-output-value">(.*?)<\/pre>/s);
const superSoftIpa = output.innerHTML.match(/class="continuous-output ipa-continuous".*?<pre class="continuous-output-value">(.*?)<\/pre>/s);
assert.ok(superSoftUa, "super-soft Ukrainian output should exist");
assert.ok(superSoftIpa, "super-soft IPA output should exist");
assert.doesNotMatch(superSoftUa[1], /⟦НЕВИЗНАЧЕНО:/, "super-soft mode must not leave unresolved markers in the continuous Ukrainian output");
assert.doesNotMatch(superSoftIpa[1], /⟦UNRESOLVED:/, "super-soft mode must not leave unresolved markers in the continuous IPA output");
assert.match(superSoftUa[1], /1917/);
assert.match(superSoftUa[1], /!/);
assert.match(output.innerHTML, /approximate:orthographic-fallback/);
assert.equal(status.className, "status notice", "full coverage must still be marked provisional");
mode.value = "strict";
input.value = "ทดสอบกาไฟ";
analyze.click();
assert.match(status.textContent, /Строгий/);
assert.match(output.innerHTML, /⟦НЕВИЗНАЧЕНО: ทดสอบ⟧/);
assert.doesNotMatch(output.innerHTML, /soft-orthographic-clusters/);

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

input.value = '**ยูเครน** ([อังกฤษ](https://th.wikipedia.org/wiki/ภาษาอังกฤษ "ภาษาอังกฤษ"): *Ukraine*) [\\[a\\]](https://example.org) &#x20;';
analyze.click();
assert.match(output.innerHTML, /Перед аналізом очищено вікі-\/Markdown-розмітку/);
assert.match(output.innerHTML, /: Ukraine/);
assert.doesNotMatch(output.innerHTML, /wikipedia\.org|example\.org|&#x20;/i);


const homeHtml = await readFile(new URL("../index.html", import.meta.url), "utf8");
const systemHtml = await readFile(new URL("../system.html", import.meta.url), "utf8");
const styles = await readFile(new URL("../src/styles.css", import.meta.url), "utf8");
assert.match(homeHtml, /БЕТА · ДОСЛІДНИЦЬКА ВЕРСІЯ/);
assert.match(homeHtml, /Вставте цілий текст або статтю/);
assert.match(homeHtml, /<label class="input-label" for="thai-input">Тайський текст<\/label>/);
assert.match(homeHtml, /один суцільний український кандидат/);
assert.match(homeHtml, /<select id="engine-mode"/);
assert.match(homeHtml, /value="strict" selected/);
assert.match(homeHtml, /value="soft"/);
assert.match(homeHtml, /value="super-soft"/);
assert.match(homeHtml, /повне покриття, приблизні звуки/);
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


// The standalone IPA form must execute the real adapter and show its audit.
// Unsupported input must fail closed in the visible UI.
const ipaInput = element("ipa-input");
const ipaAdapt = element("ipa-adapt");
const ipaResult = element("ipa-adapter-result");
ipaInput.value = "[kʰaː˩˩˦]";
ipaAdapt.click();
assert.equal(ipaResult.hidden, false);
assert.match(ipaResult.innerHTML, /Український практичний кандидат/);
assert.match(ipaResult.innerHTML, /ка/);
assert.match(ipaResult.innerHTML, /kʰaː/);
assert.match(ipaResult.innerHTML, /tone notation recognized/);

ipaInput.value = "k☃a";
ipaAdapt.click();
assert.match(ipaResult.innerHTML, /Український результат утримано/);
assert.match(ipaResult.innerHTML, /Невідомий або непідтримуваний IPA-символ/);
console.log("Direct IPA input UI: adaptation, audit, and fail-closed behavior passed");
