import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";

const html = await readFile(new URL("../index.html", import.meta.url), "utf8");
const systemHtml = await readFile(new URL("../system.html", import.meta.url), "utf8");
const noticesHtml = await readFile(new URL("../third-party-notices.html", import.meta.url), "utf8");
const css = await readFile(new URL("../src/styles.css", import.meta.url), "utf8");
const app = await readFile(new URL("../src/app.js", import.meta.url), "utf8");

// Document language, landmarks, bypass mechanism and page-level navigation.
assert.match(html, /<html lang="uk">/);
assert.match(systemHtml, /<html lang="uk">/);
assert.match(noticesHtml, /<html lang="uk">/);
assert.match(html, /<a class="skip-link" href="#main-content">/);
assert.match(systemHtml, /<a class="skip-link" href="#main-content">/);
assert.match(noticesHtml, /<a class="skip-link" href="#main-content">/);
assert.match(html, /<main[^>]+id="main-content"/);
assert.match(systemHtml, /<main[^>]+id="main-content"/);
assert.match(noticesHtml, /<main[^>]+id="main-content"/);
assert.match(html, /<nav aria-label="Основна навігація">/);
assert.match(systemHtml, /<nav aria-label="Основна навігація">/);
assert.match(noticesHtml, /<nav aria-label="Основна навігація">/);
assert.equal((html.match(/<h1(?:\s|>)/g) || []).length, 1, "service page must have one primary heading");
assert.equal((systemHtml.match(/<h1(?:\s|>)/g) || []).length, 1, "method page must have one primary heading");
assert.equal((noticesHtml.match(/<h1(?:\s|>)/g) || []).length, 1, "notices page must have one primary heading");
assert.match(noticesHtml, /CC BY-SA 4\.0/);
assert.match(noticesHtml, /BSD-3-Clause/);
assert.match(noticesHtml, /Apache License 2\.0/);
assert.match(noticesHtml, /Mozilla Public License 2\.0/);
assert.match(noticesHtml, /MIT License/);

// Every static form control has a programmatic label and its described-by targets exist.
const ids = [...html.matchAll(/\bid="([^"]+)"/g)].map(match => match[1]);
assert.equal(new Set(ids).size, ids.length, "service page IDs must be unique");
const idSet = new Set(ids);
for (const match of html.matchAll(/<label\b[^>]*\bfor="([^"]+)"/g)) {
  assert(idSet.has(match[1]), `label target does not exist: ${match[1]}`);
}
for (const match of html.matchAll(/\baria-describedby="([^"]+)"/g)) {
  for (const id of match[1].split(/\s+/)) assert(idSet.has(id), `described-by target does not exist: ${id}`);
}
for (const id of ["thai-input"]) {
  assert.match(html, new RegExp(`<label[^>]+for="${id}"`), `${id} must have a visible label`);
}
assert.match(html, /<textarea[^>]+lang="th"/);
assert.match(html, /class="hero hero-grid"/);
assert.match(html, /id="input-count"/);
assert.match(html, /aria-describedby="input-hint input-count"/);
assert.match(css, /\.hero-grid\s*\{/);
assert.match(css, /\.input-count\s*\{/);
assert.match(css, /\.examples button\s*\{[^}]*min-height:\s*44px/);
assert.match(html, /<section id="status" class="status" role="status" aria-live="polite"/);
assert.match(html, /<section id="results"[^>]+aria-label="Результати" aria-live="off"/);
assert.match(html, /<details[^>]*>[\s\S]*?<summary>/, "disclosure widgets need a native summary control");
assert.match(systemHtml, /<details[^>]*>[\s\S]*?<summary>/);

// Dynamically generated content retains names, language metadata and safe text insertion.
assert.match(app, /aria-label="Копіювати: /);
assert.match(app, /lang="und-fonipa"/);
assert.match(app, /const esc =/);
assert.match(app, /continuous-output-value/);
assert.match(app, /<h3 class="word-heading">/);
assert.match(app, /<h4 class="result-title">/);
const sampleButtonRule = css.match(/\.examples button\s*\{([^}]*)\}/);
const copyButtonRule = css.match(/\.copy\s*\{[^}]*min-height:\s*44px[^}]*\}/)
assert(sampleButtonRule && /border:\s*1px solid #767676/.test(sampleButtonRule[1]), "sample button boundary must have visible contrast");
assert(copyButtonRule && /border:\s*1px solid #767676/.test(copyButtonRule[1]), "copy button boundary must have visible contrast");

// Keyboard focus must remain visible for all native interactive controls, 
assert.match(css, /:focus-visible\s*\{/);
assert.match(css, /\.skip-link:focus\s*\{/);
assert.match(css, /@media\s*\(prefers-reduced-motion:\s*reduce\)/);

// Check the actual palette pairs used by the stylesheet against WCAG AA's 4.5:1
// normal-text threshold. This is a source-level check, not a browser contrast audit.
function luminance(hex) {
  const raw = hex.replace("#", "");
  const expanded = raw.length === 3 ? [...raw].map(value => value + value).join("") : raw;
  const rgb = expanded.match(/[0-9a-f]{2}/gi).map(value => parseInt(value, 16) / 255);
  const linear = rgb.map(value => value <= 0.04045 ? value / 12.92 : ((value + 0.055) / 1.055) ** 2.4);
  return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2];
}
function contrast(foreground, background) {
  const values = [luminance(foreground), luminance(background)].sort((a, b) => b - a);
  return (values[0] + 0.05) / (values[1] + 0.05);
}

const textareaRule = css.match(/textarea\s*\{([^}]*)\}/i);
assert(textareaRule, "Thai text input must have an active CSS rule");
const textareaBorder = textareaRule[1].match(/\bborder:\s*\d+px\s+solid\s+(#[0-9a-f]{3}(?:[0-9a-f]{3})?)\b/i);
const textareaBackground = textareaRule[1].match(/\bbackground(?:-color)?:\s*(#[0-9a-f]{3}(?:[0-9a-f]{3})?)\b/i);
assert(textareaBorder && textareaBackground, "Thai text input must declare explicit border and background colors");
const textareaBorderContrast = contrast(textareaBorder[1], textareaBackground[1]);
assert(textareaBorderContrast >= 3, `Thai text input border contrast ${textareaBorderContrast.toFixed(2)}:1 is below WCAG 1.4.11's 3:1 threshold`);
const palettePairs = [
  ["#191a22", "#ffffff", "primary text"],
  ["#5e6070", "#ffffff", "muted text on paper"],
  ["#5e6070", "#f5f5fa", "muted text on wash"],
  ["#302d8b", "#ffffff", "blue link/button text"],
  ["#ffffff", "#302d8b", "primary button text"],
  ["#9b263b", "#ffffff", "warning text"],
  ["#9b263b", "#fbf6f6", "warning text on notice"],
  ["#51474b", "#fbf6f6", "notice body text"],
  ["#505360", "#ffffff", "body text"],
  ["#505360", "#f5f5fa", "body text on wash"],
  ["#302d8b", "#f5f6fb", "blue badge text"],
  ["#767676", "#ffffff", "sample and copy button boundaries"],
  ["#ffffff", "#9b263b", "beta label text"],
  ["#9b263b", "#fbf4f5", "warning badge text"]
];
for (const [foreground, background, label] of palettePairs) {
  const ratio = contrast(foreground, background);
  assert(ratio >= 4.5, `${label} contrast ${ratio.toFixed(2)}:1 is below 4.5:1`);
}

console.log(JSON.stringify({
  result: "PASS",
  static_documents: 3,
  unique_service_ids: ids.length,
  wcag_aa_text_contrast_pairs: palettePairs.length,
  minimum_contrast_ratio: Math.min(...palettePairs.map(([foreground, background]) => contrast(foreground, background))),
  checked: [
    "document language and landmarks",
    "third-party notices navigation and license references",
    "skip links and navigation names",
    "visible labels and described-by references",
    "status and result announcements",
    "dynamic output language/name metadata",
    "keyboard focus indicators",
    "reduced-motion preference",
    "selected text-color contrast pairs"
  ],
  limitation: "static source contract only; not manual WCAG 2.2 AA conformance"
}, null, 2));
