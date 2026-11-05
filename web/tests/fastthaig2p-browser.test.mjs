import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { chromium } from "playwright";

const server = spawn("python", [
  "-m", "http.server", "4173", "--bind", "127.0.0.1", "--directory", "web"
], { stdio: "inherit" });

let browser;
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
  await page.waitForFunction(
    () => document.querySelector("#status")?.textContent.includes("Готово"),
    null,
    { timeout: 180000 }
  );

  const firstResult = await page.locator("#results").innerText();
  assert.match(firstResult, /\/sua̯n˩˩˦\//);
  assert.match(firstResult, /Українськими літерами/);
  assert.match(firstResult, /FastThaiG2P/);

  await page.locator("#thai-input").fill("กรุงเทพมหานคร");
  await page.locator("#analyze").click();
  await page.waitForFunction(
    () => document.querySelector("#status")?.textContent.includes("Готово"),
    null,
    { timeout: 30000 }
  );
  const secondResult = await page.locator("#results").innerText();
  assert.match(secondResult, /กรุงเทพมหานคร/);
  assert.match(secondResult, /IPA FastThaiG2P/);

  assert.equal(requests.some(url => url.includes("/api/analyze")), false);
  assert.equal(requests.some(url => url.includes("cdn.jsdelivr.net")), false);
  assert.deepEqual(pageErrors, []);
  console.log("Browser worker passed: same-origin Pyodide, FastThaiG2P IPA regression, warm run and no API/CDN requests");
} finally {
  await browser?.close();
  server.kill("SIGTERM");
}
