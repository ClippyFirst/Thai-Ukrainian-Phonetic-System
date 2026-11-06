import assert from "node:assert/strict";
import { createServer } from "node:http";
import { readFile } from "node:fs/promises";
import { extname, resolve, sep } from "node:path";
import { chromium } from "playwright";

const root = resolve("web");
const reference = JSON.parse(await readFile(process.argv[2], "utf8"));
const expected = reference.cases[0];
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
  const actual = await page.evaluate(async input => {
    const worker = new Worker("/src/fastthaig2p-native-worker.js", { type: "module" });
    return await new Promise((resolve, reject) => {
      const initId = "native-init";
      const convertId = "native-convert";
      const timeout = setTimeout(() => {
        worker.terminate();
        reject(new Error("Native worker smoke timed out"));
      }, 30000);
      worker.onerror = event => {
        clearTimeout(timeout);
        worker.terminate();
        reject(new Error(event.message || "Native worker failed"));
      };
      worker.onmessage = event => {
        const message = event.data || {};
        if (message.id === initId && message.type === "ready") {
          worker.postMessage({ type: "convert", id: convertId, text: input });
        } else if (message.id === convertId && message.type === "result") {
          clearTimeout(timeout);
          worker.terminate();
          resolve(message.result);
        } else if (message.type === "error") {
          clearTimeout(timeout);
          worker.terminate();
          reject(new Error(message.code + ": " + message.message));
        }
      };
      worker.postMessage({ type: "init", id: initId });
    });
  }, expected.input);
  assert.equal(actual.normalized_input, expected.normalized);
  assert.deepEqual(actual.words.map(word => word.thai), expected.tokens);
  assert.equal(actual.raw_ipa, expected.expected_ipa);

  const forbidden = requests.filter(url =>
    /pyodide|\/wheels\/|\.whl(?:$|\?)|pyodide\.mjs|https?:\/\/(?!127\.0\.0\.1)/iu.test(url)
  );
  assert.deepEqual(forbidden, [], "Native worker requested a Python/Pyodide/wheel or remote asset");
  assert(requests.some(url => url.includes("/vendor/native/fastthaig2p-ipa.json")));
  assert(requests.some(url => url.includes("/vendor/native/fastthaig2p-normalizer.json")));
  assert(requests.some(url => url.includes("/vendor/native/pythainlp-default-words.txt")));
  console.log("Native FastThaiG2P worker passed Chromium smoke without Pyodide, Python, wheels or remote requests");
} finally {
  await browser.close();
  await new Promise(resolveClose => server.close(resolveClose));
}
