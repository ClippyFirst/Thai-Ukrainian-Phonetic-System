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
const nativeRequests = [];
const pyodideRequests = [];
let nextNativeWorkerMessage = { type: "result", result: response };
let nextPyodideWorkerMessage = { type: "result", result: response };
let deferNextNativeWorkerMessage = false;
let deferredNativeWorkerResponse;
let nativeWorkerInstance;
let pyodideWorkerInstance;

class FakeWorker {
  constructor(url, options) {
    this.url = url;
    this.options = options;
    this.listeners = {};
    this.isNative = String(url).includes("fastthaig2p-native-worker.js");
    if (this.isNative) nativeWorkerInstance = this;
    else pyodideWorkerInstance = this;
  }
  addEventListener(type, callback) { this.listeners[type] = callback; }
  postMessage(message) {
    if (this.isNative) {
      nativeRequests.push(message);
      const responseMessage = message.type === "init"
        ? { type: "ready", id: message.id }
        : { ...nextNativeWorkerMessage, id: message.id };
      if (deferNextNativeWorkerMessage) {
        deferNextNativeWorkerMessage = false;
        deferredNativeWorkerResponse = () => this.listeners.message?.({ data: responseMessage });
      } else {
        queueMicrotask(() => this.listeners.message?.({ data: responseMessage }));
      }
      return;
    }
    pyodideRequests.push(message);
    const responseMessage = { ...nextPyodideWorkerMessage, requestId: message.requestId };
    queueMicrotask(() => this.listeners.message?.({ data: responseMessage }));
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
assert.match(output.innerHTML, /class="rtgs-inline-result"/);
assert.match(output.innerHTML, /Показати додатково: романізація латиницею \(RTGS\)/);
assert.match(output.innerHTML, /lang="und-Latn"/);
const appSource = await (await import("node:fs/promises")).readFile(new URL("../src/app.js", import.meta.url), "utf8");
assert.match(appSource, /import\("\.\/rtgs-romanizer\.js"\)/);
assert.match(appSource, /output\.addEventListener\("toggle", handleRtgsDisclosure, true\)/);
assert.match(appSource, /input\.value !== sourceText \|\| !disclosure\.isConnected/);
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
assert.match(output.innerHTML, /коміт вихідного проєкту/);
assert.equal(status.className, "status notice");
assert.match(status.textContent, /Український запис попередній/);
assert.equal(nativeRequests.length, 2);
assert.equal(nativeRequests[0].type, "init");
assert.equal(nativeRequests[1].type, "convert");
assert.equal(nativeRequests[1].text, "พริก");
assert.equal(nativeWorkerInstance.options.type, "module");
assert.match(String(nativeWorkerInstance.url), /fastthaig2p-native-worker\.js$/);
assert.equal(pyodideWorkerInstance, undefined,
  "dictionary-covered input must not create the Pyodide worker");
assert.doesNotMatch(await (await import("node:fs/promises")).readFile(new URL("../src/app.js", import.meta.url), "utf8"), /analyzeText|renderRtgsTokens|renderRtgsUkrainianTokens/);

for (const example of examples) {
  await example.click();
  assert.equal(input.value, example.dataset.example);
  assert.equal(output.hidden, true, "changing the input must invalidate the previous result");
  assert.equal(nativeRequests.length, 2, "choosing an example must not trigger analysis automatically");
}
assert.equal(nativeRequests.length, 2);
assert.equal(element("input-count").textContent, "Знаків: 4");
assert.match(status.textContent, /Приклад додано/);
await analyze.click();
assert.equal(nativeRequests.length, 3);
assert.equal(nativeRequests[2].text, "จริง");
assert.equal(pyodideWorkerInstance, undefined);

let prevented = false;
input.value = "พริก";
await input.listeners.keydown({
  ctrlKey: true, metaKey: false, key: "Enter",
  preventDefault() { prevented = true; }
});
assert.equal(prevented, true);
assert.equal(nativeRequests.length, 4);
assert.equal(pyodideWorkerInstance, undefined);

input.value = "";
await analyze.click();
assert.equal(status.className, "status error");
assert.match(status.textContent, /Введіть тайський текст/);
assert.equal(nativeRequests.length, 4);

input.value = "ทดสอบ";
nextNativeWorkerMessage = {
  type: "error",
  code: "native_dictionary_miss",
  message: "Нативний порт поки не підтримує цей словниковий запис."
};
nextPyodideWorkerMessage = {
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
assert.equal(nativeRequests.length, 5);
assert.equal(pyodideRequests.length, 1, "only a native dictionary miss may initialize the Pyodide fallback");
assert.equal(pyodideRequests[0].type, "analyze");
assert.equal(pyodideRequests[0].text, "ทดสอบ");
assert.match(String(pyodideWorkerInstance.url), /fastthaig2p-worker\.js$/);

// A response for an input that changed while native analysis was running must never render.
nextNativeWorkerMessage = { type: "result", result: response };
input.value = "พริก";
deferNextNativeWorkerMessage = true;
const staleRun = analyze.click();
assert.equal(analyze.disabled, true, "analysis action is locked while the worker is running");
input.value = "กา";
input.listeners.input();
// Native analysis awaits the already-resolved worker-ready promise before posting.
// Flush that microtask so the fake worker has installed its deferred response callback.
await Promise.resolve();
assert.equal(typeof deferredNativeWorkerResponse, "function",
  "the native worker request must be pending before delivering its stale response");
deferredNativeWorkerResponse();
await staleRun;
assert.equal(output.hidden, true, "a stale worker response must not render");
assert.match(status.textContent, /Текст змінився під час аналізу/);
assert.equal(analyze.disabled, false, "analysis action unlocks after the stale response is discarded");

clear.click();
assert.equal(input.value, "");
assert.equal(output.hidden, true);
assert.equal(status.textContent, "");
assert.equal(diagnostics.hidden, true, "editing/clearing input hides stale diagnostics");

console.log("Native-first FastThaiG2P UI contract: dictionary hits avoid Pyodide; only OOV initializes the full fallback worker");
