import assert from "node:assert/strict";
import { readFileSync, readdirSync } from "node:fs";
import { resolve } from "node:path";
import { loadPyodide } from "pyodide";

const wheelDir = resolve(process.argv[2] || "build/pyodide-wheels");
const expectedPath = resolve(process.argv[3] || "build/fastthaig2p-native.json");
const wheelNames = readdirSync(wheelDir).filter(name => name.endsWith(".whl")).sort();
assert.equal(wheelNames.length, 4, `Expected exactly three pinned wheels, found ${wheelNames.length}`);

const indexURL = resolve("node_modules/pyodide") + "/";
let pyodide;
try {
  pyodide = await loadPyodide({ indexURL });
} catch (error) {
  console.error("Pyodide initialisation failed:", error?.stack || error);
  process.exit(1);
}

async function runPython(label, source) {
  try {
    return await pyodide.runPythonAsync(source);
  } catch (error) {
    console.error(`${label} failed:`, error?.stack || error);
    throw error;
  }
}

pyodide.FS.mkdirTree("/wheels");
for (const name of wheelNames) {
  pyodide.FS.writeFile(`/wheels/${name}`, readFileSync(resolve(wheelDir, name)));
}
pyodide.globals.set("WHEEL_NAMES", pyodide.toPy(wheelNames));
await runPython("Pure-Python wheel installation", `
import sysconfig
import zipfile
from pathlib import Path, PurePosixPath

site_packages = Path(sysconfig.get_paths()["purelib"])
for filename in WHEEL_NAMES:
    wheel_path = Path("/wheels") / filename
    with zipfile.ZipFile(wheel_path) as wheel:
        metadata = next(
            (name for name in wheel.namelist() if name.endswith(".dist-info/WHEEL")),
            None,
        )
        assert metadata is not None, filename
        wheel_metadata = wheel.read(metadata).decode("utf-8")
        assert "Root-Is-Purelib: true" in wheel_metadata, filename
        assert "Tag: py3-none-any" in wheel_metadata, filename
        for member_name in wheel.namelist():
            member = PurePosixPath(member_name)
            assert not member.is_absolute() and ".." not in member.parts, member_name
        wheel.extractall(site_packages)
`);

const pythonSource = readFileSync(resolve("scripts/fastthaig2p_pyodide_parity.py"), "utf8");
pyodide.FS.writeFile("/fastthaig2p_pyodide_parity.py", pythonSource);
const actualText = await runPython("FastThaiG2P parity fixture", `
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
assert.equal(garden.result.status_code, 200);
assert.equal(garden.result.body.raw_ipa, "/sua̯n˩˩˦/");
console.log(`Pyodide parity passed: ${actual.cases.length} Thai inputs; upstream ${actual.upstream_commit}`);
