import assert from "node:assert/strict";
import { existsSync, readFileSync } from "node:fs";

const notices = readFileSync("web/third-party-notices.html", "utf8");
const homepage = readFileSync("web/index.html", "utf8");
const system = readFileSync("web/system.html", "utf8");
const builder = readFileSync("scripts/build_pyodide_bundle.py", "utf8");
const ccBySa = readFileSync("web/licenses/CC-BY-SA-4.0.txt", "utf8");

assert.match(notices, /<html lang="uk">/);
assert.match(notices, /<a class="skip-link" href="#main-content">/);
assert.match(notices, /<main[^>]*id="main-content"/);
assert.match(notices, /автори Wiktionary/);
assert.match(notices, /Kaikki\.org \/ Wiktextract/);
assert.match(notices, /CC BY-SA 4\.0/);
assert.match(notices, /GNU Free Documentation License 1\.3/);
assert.match(notices, /BSD-3-Clause/);
assert.match(notices, /LGPL-3\.0/);
assert.match(notices, /Apache License 2\.0/);
assert.match(notices, /Mozilla Public License 2\.0/);
assert.match(ccBySa, /Creative Commons Attribution-ShareAlike 4\.0 International/);
assert.ok(ccBySa.length > 10000, "CC BY-SA license file should contain the full legal code");
assert.doesNotMatch(notices, /\\n/);

const requiredNotices = [
  "Apache-2.0-FastThaiG2P.txt",
  "NOTICE-FastThaiG2P.txt",
  "Apache-2.0-PyThaiNLP.txt",
  "PyThaiNLP-corpus-license.md",
  "MPL-2.0-Pyodide.txt",
  "Apache-2.0-tzdata.txt",
  "BSD-3-Clause-TLTK.txt",
  "LGPL-3.0-TLTK-repository-license.txt",
  "CC-BY-SA-4.0.txt",
  "MIT-Project.txt",
];
for (const filename of requiredNotices) {
  assert.ok(existsSync(`web/licenses/${filename}`), `missing notice: ${filename}`);
  assert.ok(notices.includes(`licenses/${filename}`), `notice page does not link: ${filename}`);
}

const datasetPath = "vendor/datasets/fastthaig2p-wiktionary-derived.zip";
assert.ok(notices.includes(datasetPath), "filtered dataset download link is missing");
assert.ok(builder.includes("fastthaig2p-wiktionary-derived.zip"), "bundle builder does not create the linked dataset");
assert.ok(homepage.includes("third-party-notices.html"), "homepage does not link runtime notices");
assert.ok(system.includes("third-party-notices.html"), "system page does not link runtime notices");

console.log("Third-party notices, local license files, dataset link and site navigation passed.");
