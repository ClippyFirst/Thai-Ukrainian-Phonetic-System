import assert from "node:assert/strict";

const elements = new Map();
function element(id) {
  if (!elements.has(id)) {
    elements.set(id, {
      id, value: "", hidden: true, className: "", textContent: "", innerHTML: "",
      listeners: {}, disabled: false, focused: false,
      addEventListener(type, callback) { this.listeners[type] = callback; },
      focus() { this.focused = true; },
      querySelectorAll() { return []; },
      click() { return this.listeners.click?.({}); }
    });
  }
  return elements.get(id);
}
const examples = ["กา", "พริก", "มา", "ไฟ", "หมา", "ใหม่", "จริง"].map(example => ({
  dataset: { example }, listeners: {},
  addEventListener(type, callback) { this.listeners[type] = callback; },
  click() { return this.listeners.click?.({}); }
}));

globalThis.document = {
  getElementById: element,
  querySelectorAll(selector) { return selector === "[data-example]" ? examples : []; }
};

const response = {
  input: "พริก",
  engine: "FastThaiG2P",
  upstream_commit: "4e82a291b4cf2876326744c6580121e9986ad354",
  status: "provisional",
  raw_ipa: "/pʰrík/",
  ukrainian: "п'рік",
  words: [{
    thai: "พริก",
    fastthaig2p_ipa: "pʰrík",
    ukrainian: "п'рік",
    syllables: [{
      ipa: "pʰrik", raw_ipa: "pʰrík", tone: "high", tone_ipa: "˦˥",
      vowel_length: "short", ukrainian: "п'рік", adaptation_status: "provisional",
      rules_applied: ["UA-P-ASP"], neutralized_features: ["tone"],
      provenance: ["FastThaiG2P@4e82a291b4cf2876326744c6580121e9986ad354"],
      warnings: ["PROVISIONAL: IPA is not independently adjudicated."]
    }]
  }],
  warnings: ["Український запис попередній."]
};
let requests = [];
let nextWorkerMessage = { type: "result", result: response };
let deferNextWorkerMessage = false;
let deferredWorkerResponse;
let workerInstance;
class FakeWorker {
  constructor(url, options) {
    this.url = url;
    this.options = options;
    this.listeners = {};
    workerInstance = this;
  }
  addEventListener(type, callback) { this.listeners[type] = callback; }
  postMessage(message) {
    requests.push(message);
    const responseMessage = { ...nextWorkerMessage, requestId: message.requestId };
    if (deferNextWorkerMessage) {
      deferNextWorkerMessage = false;
      deferredWorkerResponse = () => this.listeners.message?.({ data: responseMessage });
    } else {
      queueMicrotask(() => this.listeners.message?.({ data: responseMessage }));
    }
  }
  terminate() {}
}
globalThis.Worker = FakeWorker;

await import("../src/app.js?ui-contract-test");

const input = element("thai-input");
const status = element("status");
const output = element("results");
const analyze = element("analyze");
const clear = element("clear");
const diagnostics = element("technical-diagnostics");
const diagnosticDetails = element("diagnostic-details");

input.value = "พริก";
await analyze.click();
assert.equal(output.hidden, false);
assert.match(output.innerHTML, /Попередній результат FastThaiG2P/);
assert.match(output.innerHTML, /result-feature-grid/);
assert.match(output.innerHTML, /class="continuous-output ua-continuous"/);
assert.match(output.innerHTML, /Українськими літерами/);
assert.match(output.innerHTML, /п&#39;рік/);
assert.match(output.innerHTML, /IPA FastThaiG2P/);
assert.match(output.innerHTML, /високий/);
assert.match(output.innerHTML, /короткий/);
assert.match(output.innerHTML, /pʰrík/);
assert.match(output.innerHTML, /lang="th">พริก/);
assert.match(output.innerHTML, /експертно підтверджено/);
assert.match(output.innerHTML, /Цей результат попередній/);
assert.doesNotMatch(output.innerHTML, /PROVISIONAL|not independently adjudicated/);
assert.match(output.innerHTML, /upstream commit/);
assert.equal(status.className, "status notice");
assert.match(status.textContent, /Український запис попередній/);
assert.equal(requests.length, 1);
assert.equal(requests[0].type, "analyze");
assert.equal(requests[0].text, "พริก");
assert.equal(workerInstance.options.type, "module");
assert.match(String(workerInstance.url), /fastthaig2p-worker\.js$/);
assert.doesNotMatch(await (await import("node:fs/promises")).readFile(new URL("../src/app.js", import.meta.url), "utf8"), /analyzeText|renderRtgsTokens|renderRtgsUkrainianTokens/);

for (const example of examples) {
  await example.click();
  assert.equal(input.value, example.dataset.example);
  assert.equal(output.hidden, true, "changing the input must invalidate the previous result");
  assert.equal(requests.length, 1, "choosing an example must not trigger analysis automatically");
}
assert.equal(requests.length, 1);
assert.equal(element("input-count").textContent, "Знаків: 4");
assert.match(status.textContent, /Приклад додано/);
await analyze.click();
assert.equal(requests.length, 2);
assert.equal(requests[1].text, "จริง");

let prevented = false;
input.value = "พริก";
await input.listeners.keydown({
  ctrlKey: true, metaKey: false, key: "Enter",
  preventDefault() { prevented = true; }
});
assert.equal(prevented, true);
assert.equal(requests.length, 3);

input.value = "";
await analyze.click();
assert.equal(status.className, "status error");
assert.match(status.textContent, /Введіть тайський текст/);

input.value = "ทดสอบ";
nextWorkerMessage = {
  type: "error",
  code: "incomplete_ipa",
  diagnostic: "Upstream FastThaiG2P: unsupported token"
};
await analyze.click();
assert.equal(status.className, "status error");
assert.match(status.textContent, /Не вдалося визначити вимову всього тексту/);
assert.doesNotMatch(status.textContent, /Upstream|unsupported|FastThaiG2P/);
assert.equal(diagnostics.hidden, false, "technical diagnostics should be available after an error");
assert.match(diagnosticDetails.textContent, /unsupported token/, "raw diagnostics stay in the optional details");
assert.equal(output.hidden, true, "an incomplete upstream result must not fall back to the old engine");

// A response for an input that changed while analysis was running must never render.
nextWorkerMessage = { type: "result", result: response };
input.value = "พริก";
deferNextWorkerMessage = true;
const staleRun = analyze.click();
assert.equal(analyze.disabled, true, "analysis action is locked while the worker is running");
input.value = "กา";
input.listeners.input();
assert.equal(output.hidden, true, "editing input invalidates prior output immediately");
deferredWorkerResponse();
await staleRun;
assert.equal(output.hidden, true, "a stale worker response must not render");
assert.match(status.textContent, /Текст змінився під час аналізу/);
assert.equal(analyze.disabled, false, "analysis action unlocks after the stale response is discarded");

clear.click();
assert.equal(input.value, "");
assert.equal(output.hidden, true);
assert.equal(status.textContent, "");
assert.equal(diagnostics.hidden, true, "editing/clearing input hides stale diagnostics");

console.log("FastThaiG2P-only UI contract: local worker routing, provisional disclosure and fail-closed behavior passed");
