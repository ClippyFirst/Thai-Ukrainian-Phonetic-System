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
assert.match(output.innerHTML, /Результати аналізу/);
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

// Whole unspaced Thai runs must split into known lexicon entries, not be
// treated as one dictionary key. Unknown spans must not suppress adjacent IPA.
input.value = "กาไฟมา";
analyze.click();
assert.match(output.innerHTML, /Результат 1: กา/);
assert.match(output.innerHTML, /Результат 2: ไฟ/);
assert.match(output.innerHTML, /Результат 3: มา/);
assert.equal((output.innerHTML.match(/ФОНОЛОГІЧНА IPA/g) || []).length, 3);
assert.equal(status.className, "status");

input.value = "ทดสอบกาไฟ";
analyze.click();
assert.match(output.innerHTML, /Результат 1: ทดสอบ/);
assert.match(output.innerHTML, /unresolved/);
assert.match(output.innerHTML, /Результат 2: กา/);
assert.match(output.innerHTML, /Результат 3: ไฟ/);
assert.equal((output.innerHTML.match(/ФОНОЛОГІЧНА IPA/g) || []).length, 2);
assert.equal(status.className, "status notice");

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

const homeHtml = await readFile(new URL("../index.html", import.meta.url), "utf8");
const systemHtml = await readFile(new URL("../system.html", import.meta.url), "utf8");
const styles = await readFile(new URL("../src/styles.css", import.meta.url), "utf8");
assert.match(homeHtml, /БЕТА · ДОСЛІДНИЦЬКА ВЕРСІЯ/);
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
