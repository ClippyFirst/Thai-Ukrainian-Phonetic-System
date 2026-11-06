import assert from "node:assert/strict";
import { createServer } from "node:http";
import { readFile } from "node:fs/promises";
import { extname, resolve, sep } from "node:path";
import { chromium } from "playwright";

const root = resolve("web");
const reference = JSON.parse(await readFile(process.argv[2], "utf8"));
assert(reference.cases.length > 0, "Native browser smoke requires reference cases");
const mime = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".txt": "text/plain; charset=utf-8",
  ".css": "text/css; charset=utf-8"
};
const server = createServer(async (request, response) => {
  try {
    const pathname = decodeURIComponent(new URL(request.url, "http://localhost").pathname);
    const file = resolve(root, "." + pathname);
    if (file !== root && !file.startsWith(root + sep)) {
      response.writeHead(403).end();
      return;
    }
    const body = await readFile(file);
    response.writeHead(200, { "content-type": mime[extname(file)] || "application/octet-stream" });
    response.end(body);
  } catch {
    response.writeHead(404).end("not found");
  }
});
await new Promise(resolveListen => server.listen(0, "127.0.0.1", resolveListen));
const address = server.address();
const browser = await chromium.launch({ headless: true });
try {
  const page = await browser.newPage();
  const requests = [];
  page.on("request", request => requests.push(request.url()));
  await page.goto("http://127.0.0.1:" + address.port + "/tests/native-worker-smoke.html");
  const actual = await page.evaluate(async cases => {
    const worker = new Worker("/src/fastthaig2p-native-worker.js", { type: "module" });
    const pending = new Map();
    let sequence = 0;
    worker.onmessage = event => {
      const message = event.data || {};
      const waiter = pending.get(message.id);
      if (!waiter) return;
      pending.delete(message.id);
      clearTimeout(waiter.timer);
      if (message.type === "error") {
        waiter.reject(new Error(message.code + ": " + message.message));
      } else {
        waiter.resolve(message);
      }
    };
    worker.onerror = event => {
      for (const waiter of pending.values()) {
        clearTimeout(waiter.timer);
        waiter.reject(new Error(event.message || "Native worker failed"));
      }
      pending.clear();
    };
    const send = (type, payload = {}) => new Promise((resolve, reject) => {
      const id = "native-" + (++sequence);
      const timer = setTimeout(() => {
        pending.delete(id);
        reject(new Error("Native worker request timed out: " + type));
      }, 30000);
      pending.set(id, { resolve, reject, timer });
      worker.postMessage({ type, id, ...payload });
    });
    try {
      const ready = await send("init");
      const results = [];
      for (const item of cases) {
        const message = await send("convert", { text: item.input });
        results.push(message.result);
      }
      let oov;
      try {
        await send("convert", { text: "🤖" });
        oov = { unexpectedly_succeeded: true };
      } catch (error) {
        oov = { message: error.message };
      }
      return { stage: ready.stage, results, oov };
    } finally {
      worker.terminate();
    }
  }, reference.cases);
  assert.equal(actual.results.length, reference.cases.length);
  for (const [index, expected] of reference.cases.entries()) {
    const result = actual.results[index];
    assert.equal(result.normalized_input, expected.normalized, "normalized input case " + index);
    assert.deepEqual(result.words.map(word => word.thai), expected.tokens, "tokens case " + index);
    assert.equal(result.raw_ipa, expected.expected_ipa, "raw IPA case " + index);
  }
  assert.equal(actual.oov.unexpectedly_succeeded, undefined);
  assert.match(actual.oov.message, /^native_dictionary_miss: /u);
  assert.match(actual.oov.message, /Нативний порт поки не підтримує/u);

  const forbidden = requests.filter(url =>
    /pyodide|\/wheels\/|\.whl(?:$|\?)|pyodide\.mjs|https?:\/\/(?!127\.0\.0\.1)/iu.test(url)
  );
  assert.deepEqual(forbidden, [], "Native worker requested a Python/Pyodide/wheel or remote asset");
  assert(requests.some(url => url.includes("/vendor/native/fastthaig2p-ipa.json")));
  assert(requests.some(url => url.includes("/vendor/native/fastthaig2p-normalizer.json")));
  assert(requests.some(url => url.includes("/vendor/native/pythainlp-default-words.txt")));
  console.log("Native FastThaiG2P Worker passed Chromium smoke for " + reference.cases.length +
    " CPython cases and fail-closed OOV without Pyodide, Python, wheels or remote requests");
} finally {
  await browser.close();
  await new Promise(resolveClose => server.close(resolveClose));
}
