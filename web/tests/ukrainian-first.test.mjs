import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { ERROR_MESSAGES, UI_TEXT, errorMessage } from "../src/messages.uk.js";

const ukrainian = /[А-Яа-яІіЇїЄєҐґ]/u;
for (const [key, value] of Object.entries(UI_TEXT)) {
  assert.equal(typeof value, "string", `UI text ${key} must be a string`);
  assert(ukrainian.test(value), `UI text ${key} must be Ukrainian`);
}
const ids = new Set();
for (const [code, value] of Object.entries(ERROR_MESSAGES)) {
  assert(ukrainian.test(value.message), `Error ${code} must have Ukrainian user copy`);
  assert.match(value.id, /^UA-[A-Z]+-\d{3}$/u);
  assert(!ids.has(value.id), `Duplicate user-facing error ID: ${value.id}`);
  ids.add(value.id);
}
assert.match(errorMessage("unregistered_error").message, /Сталася непередбачена помилка/);
assert.match(errorMessage("incomplete_ipa").message, /не підмінятиме/);

const app = await readFile(new URL("../src/app.js", import.meta.url), "utf8");
const worker = await readFile(new URL("../src/fastthaig2p-worker.js", import.meta.url), "utf8");
const html = await readFile(new URL("../index.html", import.meta.url), "utf8");
const feedback = await readFile(new URL("../../.github/ISSUE_TEMPLATE/beta-feedback.yml", import.meta.url), "utf8");
assert.match(app, /errorMessage\(error\?\.code\)/);
assert.doesNotMatch(app, /status\.textContent\s*=\s*error\.message/);
assert.match(app, /diagnosticDetails\.textContent/);
assert.match(worker, /type: "error"[\s\S]*?code,/);
assert.doesNotMatch(worker, /message: typeof detail/);
assert.doesNotMatch(worker, /detail\?\.message/);
assert.match(html, /id="technical-diagnostics"/);
assert.match(html, /Ці дані допоможуть повідомити про помилку/);
assert.match(feedback, /name: Відгук про бета-версію/);
assert.match(feedback, /label: Категорія відгуку/);
assert.match(feedback, /label: Що сталося/);
assert.match(feedback, /label: Браузер і версія/);
assert.match(feedback, /"Неочікуваний результат: тайський текст → IPA → український запис"/);
assert.match(feedback, /placeholder: "Наприклад: Firefox 132"/);
assert.match(feedback, /placeholder: "Наприклад: Android 16, Windows 11"/);
assert.match(feedback, /Підтверджую, що не додаю особистої/);
assert.doesNotMatch(feedback, /Feedback category|What happened|Browser and version|Privacy confirmation/);

console.log(JSON.stringify({
  result: "PASS",
  localized_ui_strings: Object.keys(UI_TEXT).length,
  localized_error_codes: ERROR_MESSAGES && Object.keys(ERROR_MESSAGES).length,
  unique_error_ids: ids.size,
  checks: ["Ukrainian user copy", "stable error identifiers", "generic unknown-error fallback", "raw upstream messages not forwarded", "optional diagnostics disclosure"]
}, null, 2));
