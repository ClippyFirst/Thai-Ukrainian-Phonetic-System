import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { spawn } from "node:child_process";
import { chromium } from "playwright";

const oovReference = JSON.parse(await readFile(process.argv[2], "utf8"));
assert(oovReference.input && oovReference.raw_ipa, "A pinned OOV fallback reference is required");

const server = spawn("python", [
  "-m", "http.server", "4173", "--bind", "127.0.0.1", "--directory", "web"
], { stdio: "inherit" });

let browser;
async function waitForAnalysis(page, timeout) {
  await page.waitForFunction(() => {
    const status = document.querySelector("#status");
    return status?.textContent.includes("Готово") || status?.classList.contains("error");
  }, null, { timeout });
  const status = await page.locator("#status").innerText();
  if (!status.includes("Готово")) {
    const diagnostics = await page.locator("#technical-diagnostics").textContent();
    throw new Error(`Browser analysis failed: ${status}\\n${diagnostics || "No technical diagnostics provided"}`);
  }
}

try {
  await new Promise((resolve, reject) => {
    const timeout = setTimeout(() => reject(new Error("Static test server did not start")), 3000);
    server.once("spawn", () => {
      clearTimeout(timeout);
      resolve();
    });
    server.once("error", error => {
      clearTimeout(timeout);
      reject(error);
    });
  });

  browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  const requests = [];
  const pageErrors = [];
  page.on("request", request => requests.push(request.url()));
  page.on("pageerror", error => pageErrors.push(error.message));

  await page.goto("http://127.0.0.1:4173/", { waitUntil: "networkidle" });
  await page.locator("#thai-input").fill("สวน");
  await page.locator("#analyze").click();
  await waitForAnalysis(page, 180000);

  const firstResult = await page.locator("#results").innerText();
  assert.match(firstResult, /\/sua̯n˩˩˦\//);
  assert.match(firstResult, /Українськими літерами/);
  assert.match(firstResult, /FastThaiG2P/);

  await page.locator("#thai-input").fill("กรุงเทพมหานคร");
  await page.locator("#analyze").click();
  await waitForAnalysis(page, 30000);
  const secondResult = await page.locator("#results").innerText();
  assert.match(secondResult, /kruŋ/);
  assert.match(secondResult, /крунгт/);
  assert.match(secondResult, /IPA FastThaiG2P/);

  const pyodideRequestedBeforeOov = requests.some(url =>
    url.includes("/vendor/pyodide/") || url.includes("/vendor/wheels/")
  );
  assert.equal(pyodideRequestedBeforeOov, false,
    "Dictionary-covered inputs must stay on the native JavaScript worker without downloading Python modules");

  await page.locator("#thai-input").fill(oovReference.input);
  await page.locator("#analyze").click();
  await waitForAnalysis(page, 180000);
  const oovResult = await page.locator("#results").innerText();
  assert(oovResult.includes(oovReference.raw_ipa),
    "The lazy Pyodide fallback must return the pinned OOV IPA result");
  assert(requests.some(url => url.includes("/vendor/native-oov/manifest.json")),
    "The native TLTK OOV manifest should load only after a native dictionary miss");
  assert(requests.some(url => url.includes("/vendor/native-oov/tltk-oov-data.json.gz")),
    "The native TLTK OOV data pack should load lazily for a supported OOV token");
  assert.equal(requests.some(url => url.includes("/vendor/pyodide/") || url.includes("/vendor/wheels/")), false,
    "A TLTK-supported OOV token must not download Python or Pyodide modules");

  assert.equal(requests.some(url => url.includes("/api/analyze")), false);
  assert.equal(requests.some(url => url.includes("cdn.jsdelivr.net")), false);
  assert.deepEqual(pageErrors, []);
  console.log("Browser app passed: native JavaScript dictionary and TLTK OOV paths, lazy same-origin OOV data, no Python/Pyodide/API/CDN requests");
} finally {
  await browser?.close();
  server.kill("SIGTERM");
}
