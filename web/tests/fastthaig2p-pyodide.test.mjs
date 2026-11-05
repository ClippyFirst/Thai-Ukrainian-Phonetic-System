import assert from "node:assert/strict";
import { readFileSync, readdirSync } from "node:fs";
import { resolve } from "node:path";
import { pathToFileURL } from "node:url";
import { loadPyodide } from "pyodide";

const wheelDir = resolve(process.argv[2] || "build/pyodide-wheels");
const expectedPath = resolve(process.argv[3] || "build/fastthaig2p-native.json");
const wheels = readdirSync(wheelDir).filter(name => name.endsWith(".whl"))
  .map(name => pathToFileURL(resolve(wheelDir, name)).href);
assert.equal(wheels.length, 3, `Expected exactly three pinned wheels, found ${wheels.length}`);

const indexURL = pathToFileURL(resolve("node_modules/pyodide") + "/").href;
let pyodide;
try {
  pyodide = await loadPyodide({ indexURL });
} catch (error) {
  console.error("Pyodide initialisation failed:", error?.stack || error);
  process.exit(1);
}
await pyodide.loadPackage("micropip");
pyodide.globals.set("WHEEL_URLS", pyodide.toPy(wheels));
await pyodide.runPythonAsync(`
import micropip
await micropip.install(WHEEL_URLS, deps=False)
`);

const pythonSource = readFileSync(resolve("scripts/fastthaig2p_pyodide_parity.py"), "utf8");
pyodide.FS.writeFile("/fastthaig2p_pyodide_parity.py", pythonSource);
const actualText = await pyodide.runPythonAsync(`
import importlib.util
import json
spec = importlib.util.spec_from_file_location("fastthaig2p_pyodide_parity", "/fastthaig2p_pyodide_parity.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
json.dumps(module.build_payload(), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
`);
const expected = JSON.parse(readFileSync(expectedPath, "utf8"));
const actual = JSON.parse(actualText);
assert.deepEqual(actual, expected, "Pyodide output diverged from the CPython reference");
const garden = actual.cases.find(item => item.input === "สวน");
assert.ok(garden, "สวน regression case must be present");
assert.equal(garden.raw_ipa, "/sua̯n˩˩˦/");
assert.equal(garden.complete_ipa, true);
console.log(`Pyodide parity passed: ${actual.cases.length} Thai inputs; upstream ${actual.upstream_commit}`);
