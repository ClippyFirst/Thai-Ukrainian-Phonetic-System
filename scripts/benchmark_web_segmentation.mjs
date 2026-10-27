#!/usr/bin/env node
/**
 * Reproducible, non-gating latency diagnostic for the browser Thai text path.
 * Timings are environment-specific and are not accuracy or release claims.
 * Run after scripts/generate_web_word_dictionary.py.
 */
import { writeFileSync } from "node:fs";
import { performance } from "node:perf_hooks";
import { analyzeText } from "../web/src/engine.js";

const OUTPUT = process.env.THAI_SEGMENTATION_BENCHMARK_OUTPUT || "/tmp/thai-browser-segmentation-benchmark.json";
const WARMUP = 5;
const ITERATIONS = 30;
const SIZES = [100, 250, 500];
const SEED = "กินข้าวกับไข่และผลไม้ข่าวข้าวเข้เข่าเขาเงินเดินกาแฟทดสอบเชียงใหม่ประเทศไทย";
const points = [...SEED];

function inputOfLength(target) {
  const chars = [];
  while (chars.length < target) chars.push(...points);
  return chars.slice(0, target).join("");
}
function percentile(values, p) {
  const sorted = [...values].sort((a, b) => a - b);
  return sorted[Math.min(sorted.length - 1, Math.ceil(p * sorted.length) - 1)];
}
function summarize(text) {
  const result = analyzeText(text);
  return {
    tokens: result.length,
    thaiSpans: result.filter(x => x.kind === "thai").length,
    unresolvedSpans: result.filter(x => x.kind === "thai" && x.segmentationStatus === "unresolved").length,
  };
}

const cases = [];
for (const size of SIZES) {
  const input = inputOfLength(size);
  for (let i = 0; i < WARMUP; i++) analyzeText(input);
  const samplesMs = [];
  let outputSummary;
  for (let i = 0; i < ITERATIONS; i++) {
    const start = performance.now();
    const result = analyzeText(input);
    samplesMs.push(performance.now() - start);
    outputSummary = {
      tokens: result.length,
      thaiSpans: result.filter(x => x.kind === "thai").length,
      unresolvedSpans: result.filter(x => x.kind === "thai" && x.segmentationStatus === "unresolved").length,
    };
  }
  cases.push({
    inputCodePoints: [...input].length,
    warmupIterations: WARMUP,
    measuredIterations: ITERATIONS,
    medianMs: Number(percentile(samplesMs, 0.5).toFixed(3)),
    p95Ms: Number(percentile(samplesMs, 0.95).toFixed(3)),
    minMs: Number(Math.min(...samplesMs).toFixed(3)),
    maxMs: Number(Math.max(...samplesMs).toFixed(3)),
    output: outputSummary,
  });
}
const report = {
  reportType: "BROWSER_SEGMENTATION_LATENCY_DIAGNOSTIC_NOT_ACCURACY_BENCHMARK",
  runtime: process.version,
  dictionary: "pinned CC0 Thai word list; boundary evidence only",
  warmupIterations: WARMUP,
  measuredIterations: ITERATIONS,
  cases,
  caveats: [
    "Wall-clock timings vary by runner, runtime, load and JIT state; compare only like-for-like runs.",
    "This diagnostic does not measure linguistic accuracy, word-boundary correctness, IPA quality or Ukrainian adaptation quality.",
    "No latency threshold is enforced; results are diagnostic and do not authorize guessed pronunciation.",
  ],
};
writeFileSync(OUTPUT, JSON.stringify(report, null, 2) + "\n", "utf8");
console.log(JSON.stringify(report, null, 2));
