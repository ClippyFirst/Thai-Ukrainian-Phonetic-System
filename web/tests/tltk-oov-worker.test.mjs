import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";

const root = new URL("../../", import.meta.url);
const fixtures = JSON.parse(await readFile(new URL("build/tltk-oov-reference.json", root), "utf8"));
const messages = [];
const listeners = {};
assert.ok(globalThis.crypto?.subtle, "Node must provide WebCrypto for the native worker integrity check");
globalThis.self = {
  addEventListener(type, callback) { listeners[type] = callback; },
  postMessage(message) { messages.push(message); }
};
globalThis.fetch = async input => {
  const url = input instanceof URL ? input : new URL(input.url || input);
  if (url.protocol !== "file:") return new Response("Unexpected remote request", { status: 500 });
  try {
    return new Response(await readFile(fileURLToPath(url)), { status: 200 });
  } catch {
    return new Response("Not found", { status: 404 });
  }
};

await import("../src/fastthaig2p-native-worker.js?native-tltk-oov-worker-smoke");
assert.equal(typeof listeners.message, "function", "native worker must register its message handler");

await listeners.message({ data: { type: "init", id: "init" } });
assert.equal(messages.at(-1)?.type, "ready");
assert.match(messages.at(-1)?.stage || "", /tltk-oov/u);

for (let index = 0; index < fixtures.cases.length; index += 1) {
  const item = fixtures.cases[index];
  await listeners.message({ data: { type: "convert", id: String(index), text: item.token } });
  const message = messages.at(-1);
  assert.equal(message?.type, "result", "worker must return native result for " + item.token);
  assert.equal(message.result.normalized_input, item.token);
  const { normalized_input, ...serviceResult } = message.result;
  assert.deepEqual(serviceResult, item.response, "worker typed JSON parity for " + item.token);
}

console.log("Native Worker TLTK OOV lazy-load and full Python-service parity: " + fixtures.cases.length + " cases PASS");
