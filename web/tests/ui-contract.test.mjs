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
assert.match(output.innerHTML, /Три варіанти запису/);
assert.match(output.innerHTML, /Українськими літерами/);
assert.match(output.innerHTML, /02 · Детальний запис звуків/);
assert.match(output.innerHTML, /01 · Латинський запис/);
assert.match(output.innerHTML, /phrik/);
assert.match(output.innerHTML, /01 · Латинський запис/);
assert.doesNotMatch(output.innerHTML, /<details class="rtgs-details"/, "RTGS must be visible without opening a disclosure");
assert.match(output.innerHTML, /Довідковий запис латиницею/);
assert.match(output.innerHTML, /Довідковий запис латиницею/);
const rtgsPosition = output.innerHTML.indexOf('01 · Латинський запис');
const ipaPosition = output.innerHTML.indexOf('02 · Детальний запис звуків');
const ukrainianPosition = output.innerHTML.indexOf('03 · Українськими літерами');
assert.ok(rtgsPosition >= 0 && rtgsPosition < ipaPosition && ipaPosition < ukrainianPosition, 'visible result panels must be ordered RTGS → IPA → Ukrainian');
assert.match(output.innerHTML, /<details class="analysis-details">/);
assert.match(output.innerHTML, /Показати подробиці про окремі частини/);
assert.match(output.innerHTML, /Статус: Словниковий запис/);
assert.match(output.innerHTML, /технічний код: <code>lexicon<\/code>/);
assert.match(output.innerHTML, /ФОНОЛОГІЧНА IPA/);
assert.match(output.innerHTML, /aria-labelledby=/);
assert.equal(status.className, "status");
assert.match(status.textContent, /Готово\. Нижче — три варіанти запису вимови/);

input.value = "ทดสอบ";
analyze.click();
assert.doesNotMatch(output.innerHTML, /RTGS НЕ ПЕРЕВІРЕНО/);
assert.match(output.innerHTML, /Латинський запис/);
assert.equal(status.className, "status notice");
assert.match(status.textContent, /Не всі слова вдалося прочитати впевнено/);
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
assert.match(output.innerHTML, /class="continuous-output ua-continuous"[\s\S]*?<pre class="continuous-output-value">йук(?:'|&#39;)рен<\/pre>/);
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
assert.match(output.innerHTML, /class="continuous-output ua-continuous"[\s\S]*?<pre class="continuous-output-value">таванок<\/pre>/);
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
assert.match(output.innerHTML, /class="continuous-output ua-continuous"[\s\S]*?<pre class="continuous-output-value">  ка  фай!\n<\/pre>/);

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
const modeHint = element("mode-hint");
mode.value = "2";
mode.listeners.change?.();
assert.match(modeHint.textContent, /2\/3 · Структурний профіль/);
input.value = "ทดสอบกาไฟ";
analyze.click();
assert.match(status.textContent, /зробив припущення/);
assert.equal(status.className, "status notice", "soft mode must visibly remain provisional even when every parsed syllable has a candidate");
assert.match(output.innerHTML, /soft-orthographic-clusters/);
assert.match(output.innerHTML, /сервіс зробив припущення/);
assert.match(output.innerHTML, /Попередній структурний розбір/);
assert.match(output.innerHTML, /02 · Детальний запис звуків/);
assert.match(output.innerHTML, /class="continuous-output ua-continuous"[\s\S]*?<pre class="continuous-output-value">[^<]*(?:ка|фай)/, "soft mode should emit a recoverable Ukrainian candidate for recognized/structurally parsed spans");
mode.value = "1";
mode.listeners.change?.();
assert.match(modeHint.textContent, /1\/3 · Евристичний профіль/);
input.value = "ดินแดนที่เป็นประเทศยูเครนสมัยใหม่ ค.ศ. 1917, ฮอลอดอมอร์!";
analyze.click();
assert.match(status.textContent, /приблизне читання/);
assert.match(output.innerHTML, /прочитана приблизно/);
assert.match(output.innerHTML, /Приблизне резервне читання/);
assert.match(output.innerHTML, /02 · Детальний запис звуків/);
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
mode.value = "3";
mode.listeners.change?.();
assert.match(modeHint.textContent, /3\/3 · Консервативний профіль/);
input.value = "ทดสอบกาไฟ";
analyze.click();
assert.match(status.textContent, /Не всі слова вдалося прочитати впевнено/);
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
assert.match(status.textContent, /не знайдено тайських слів/);
assert.match(output.innerHTML, /ABC/);
assert.match(output.innerHTML, /Тайського тексту для фонетичного перетворення не знайдено/);

input.value = '**ยูเครน** ([อังกฤษ](https://th.wikipedia.org/wiki/ภาษาอังกฤษ "ภาษาอังกฤษ"): *Ukraine*) [\\[a\\]](https://example.org) &#x20;';
analyze.click();
assert.match(output.innerHTML, /Перед читанням сервіс прибрав із тексту технічну розмітку посилань/);
assert.match(output.innerHTML, /: Ukraine/);
assert.doesNotMatch(output.innerHTML, /wikipedia\.org|example\.org|&#x20;/i);


const homeHtml = await readFile(new URL("../index.html", import.meta.url), "utf8");
const systemHtml = await readFile(new URL("../system.html", import.meta.url), "utf8");
const styles = await readFile(new URL("../src/styles.css", import.meta.url), "utf8");
const pagesWorkflow = await readFile(new URL("../../.github/workflows/pages.yml", import.meta.url), "utf8");
assert.match(homeHtml, /ТЕСТОВА ВЕРСІЯ/);
assert.match(homeHtml, /Текст залишається у вашому браузері/);
assert.match(pagesWorkflow, /Текст залишається у вашому браузері/);
assert.match(homeHtml, /Можна вставити одне слово або ціле речення/);
assert.match(homeHtml, /<label class="input-label" for="thai-input">Текст тайською<\/label>/);
assert.match(homeHtml, /class="skip-link"/);
assert.match(homeHtml, /id="main-content" tabindex="-1"/);
assert.match(systemHtml, /class="skip-link"/);
assert.match(systemHtml, /id="main-content" tabindex="-1"/);
assert.match(homeHtml, /class="mode-help"/);
assert.match(homeHtml, /20261030-graded-scale-1/);
assert.match(systemHtml, /20261030-graded-scale-1/);
assert.doesNotMatch(homeHtml, /class="usage-guide"/, "the first action should not be pushed down by a long instructional panel");
assert.match(homeHtml, /aria-live="off"/);
assert.match(homeHtml, /<input id="engine-mode" type="range" min="1" max="3" step="1" value="3"/);
assert.match(homeHtml, /class="strictness-scale"/);
assert.match(homeHtml, /1 · Евристичний/);
assert.match(homeHtml, /2 · Структурний/);
assert.match(homeHtml, /3 · Консервативний/);
assert.match(homeHtml, /Суворість інтерпретації · шкала 1–3/);
assert.match(homeHtml, /Методологія рівнів суворості/);
assert.match(homeHtml, /1\/3 · Евристичний/);
for (const example of examples) assert.ok(homeHtml.includes(`data-example="${example.dataset.example}"`), `homepage must expose ${example.dataset.example}`);
assert.match(homeHtml, /system\.html#beta-evidence/);
assert.match(homeHtml, /приблизну вимову українськими літерами/);
assert.match(systemHtml, /Придихові \/kʰ pʰ tʰ tɕʰ\//);
assert.doesNotMatch(homeHtml, /id="ipa-input"|id="ipa-adapt"|id="ipa-adapter-result"/, "the homepage must not duplicate the existing IPA→Ukrainian pipeline as a second input mode");
assert.match(homeHtml, /Що означає результат/);
assert.match(homeHtml, /Вставте слово або речення тайською/);
assert.match(homeHtml, /Тайські звуки не завжди можна точно передати українськими літерами/);
assert.match(homeHtml, /приблизну вимову українськими літерами/);
assert.match(systemHtml, /спочатку визначає, як воно має звучати, а вже потім добирає українські літери/);
assert.match(systemHtml, /id="beta-evidence"/);
assert.match(systemHtml, /Автоматичні тести показують, що програма працює за заданими правилами/);
assert.match(systemHtml, /набору слів і вимов/);
assert.match(systemHtml, /Шкала суворості обробки/);
assert.match(systemHtml, /Зменшення суворості збільшує покриття, але не точність/);
assert.match(systemHtml, /не є каліброваною оцінкою впевненості/);
assert.match(systemHtml, /не маємо незалежно перевіреного фахівцями набору/);
assert.match(systemHtml, /RTGS — окрема латинська система/);
assert.match(systemHtml, /Придихові \/kʰ pʰ tʰ tɕʰ\//);
assert.doesNotMatch(systemHtml, /76 із 50 000|16 із 50 000|192 із 993|119 із 993/);
assert.match(styles, /\.beta-notice/);
assert.match(styles, /\.skip-link:focus/);
assert.match(styles, /min-height:44px/);
assert.match(styles, /\.site-header nav a\{[^}]*min-height:44px/);
assert.match(styles, /\.mode-help summary\{[^}]*min-height:44px/);
assert.match(styles, /\.method-links a\{[^}]*min-height:44px/);
assert.match(styles, /\.text-button,\.copy\{min-height:44px/);
assert.match(styles, /\.rtgs-continuous\{border-top:3px solid var\(--red\)\}/);
assert.match(styles, /\.ipa-continuous\{border-top:3px solid var\(--focus\)\}/);
assert.match(styles, /\.ua-continuous\{border-top:3px solid var\(--blue\)\}/);
assert.doesNotMatch(styles, /\.rtgs-details/, "visible RTGS output must not retain collapsed-disclosure styling");
assert.match(styles, /#engine-mode:focus-visible/);
assert.match(styles, /\.strictness-scale/);
assert.match(styles, /accent-color:var\(--blue\)/);
assert.match(styles, /\.mode-help summary:focus-visible/);
assert.match(styles, /\.mode-help dl/);
assert.doesNotMatch(styles, /\.ipa-adapter-input/, "the removed standalone IPA input must not leave dead adapter styling behind");
assert.match(styles, /prefers-reduced-motion:reduce/);
const appSource = await readFile(new URL("../src/app.js", import.meta.url), "utf8");
assert.match(appSource, /async function copyText/);
assert.match(appSource, /document\.execCommand\('copy'\)/);
assert.match(appSource, /button\.setAttribute\('aria-live', 'polite'\)/);
assert.match(styles, /@media\(max-width:700px\)\{\.beta-notice/);

console.log("Thai current UI uncertainty/accessibility contract passed");

