import { loadPyodide } from "../vendor/pyodide/pyodide.mjs";

const INDEX_URL = new URL("../vendor/pyodide/", import.meta.url).href;
const MANIFEST_URL = new URL("../vendor/bundle-manifest.json", import.meta.url);
const WHEEL_BASE = new URL("../vendor/wheels/", import.meta.url);
const EXPECTED_VERSIONS = {
  fastthaig2p: "0.1.0",
  pythainlp: "5.4.0",
  "thai-ukrainian-phonetic-system": "0.6.1",
  tzdata: "2026.6"
};

let runtimePromise;

function failure(code, diagnostic) {
  const error = new Error(code);
  error.code = code;
  error.diagnostic = diagnostic;
  return error;
}

async function fetchManifest() {
  const response = await fetch(MANIFEST_URL, {
    credentials: "same-origin",
    cache: "force-cache"
  });
  if (!response.ok) {
    throw failure("bundle_unavailable", `Маніфест рушія: HTTP ${response.status}`);
  }
  const manifest = await response.json();
  if (manifest.schema_version !== 1 || manifest.pyodide?.version !== "0.29.5") {
    throw failure("bundle_invalid", "Версія або схема маніфесту не відповідає перевіреній конфігурації.");
  }
  if (manifest.purpose === "public-pages" && manifest.redistribution_approved !== true) {
    throw failure("bundle_invalid", "Публічне розповсюдження компонентів рушія не погоджено.");
  }
  if (!Array.isArray(manifest.wheels) ||
      manifest.wheels.length !== Object.keys(EXPECTED_VERSIONS).length ||
      Object.entries(EXPECTED_VERSIONS).some(([name, version]) =>
        !manifest.wheels.some(item => item.package === name && item.version === version))) {
    throw failure("bundle_invalid", "Маніфест рушія неповний або містить неочікувані версії.");
  }
  return manifest;
}

async function initializeRuntime(requestId) {
  self.postMessage({ type: "progress", requestId, stage: "runtime" });
  const pyodide = await loadPyodide({ indexURL: INDEX_URL });
  const manifest = await fetchManifest();
  pyodide.FS.mkdirTree("/wheels");
  const wheelNames = [];

  for (const asset of manifest.wheels) {
    if (!/^[a-zA-Z0-9_.-]+\\.whl$/.test(asset.filename)) {
      throw failure("bundle_invalid", "Маніфест містить неприпустиму назву Python-компонента.");
    }
    self.postMessage({ type: "progress", requestId, stage: "download", filename: asset.filename });
    const response = await fetch(new URL(asset.filename, WHEEL_BASE), {
      credentials: "same-origin",
      cache: "force-cache"
    });
    if (!response.ok) {
      throw failure("bundle_unavailable", `Компонент ${asset.filename}: HTTP ${response.status}`);
    }
    const buffer = await response.arrayBuffer();
    if (buffer.byteLength !== asset.size_bytes) {
      throw failure("bundle_corrupt", `Розмір ${asset.filename} не збігається з маніфестом.`);
    }
    const digest = await crypto.subtle.digest("SHA-256", buffer);
    const actualHash = [...new Uint8Array(digest)]
      .map(value => value.toString(16).padStart(2, "0"))
      .join("");
    if (actualHash !== asset.sha256) {
      throw failure("bundle_corrupt", `Контрольна сума ${asset.filename} не збігається.`);
    }
    pyodide.FS.writeFile(`/wheels/${asset.filename}`, new Uint8Array(buffer));
    wheelNames.push(asset.filename);
  }

  pyodide.globals.set("WHEEL_NAMES", pyodide.toPy(wheelNames));
  await pyodide.runPythonAsync(`
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
        assert any(line.startswith("Tag: py3-none-any") or line.startswith("Tag: py2.py3-none-any")
                   for line in wheel_metadata.splitlines()), filename
        for member_name in wheel.namelist():
            member = PurePosixPath(member_name)
            assert not member.is_absolute() and ".." not in member.parts, member_name
        wheel.extractall(site_packages)
`);

  return pyodide;
}

function getRuntime(requestId) {
  if (!runtimePromise) {
    runtimePromise = initializeRuntime(requestId).catch(error => {
      runtimePromise = undefined;
      throw error;
    });
  }
  return runtimePromise;
}

self.addEventListener("message", async event => {
  const { type, requestId, text } = event.data || {};
  if (type !== "analyze") return;

  let phase = "runtime";
  try {
    const pyodide = await getRuntime(requestId);
    phase = "analysis";
    self.postMessage({ type: "progress", requestId, stage: "analysis" });
    pyodide.globals.set("INPUT_TEXT", String(text ?? ""));
    const responseText = await pyodide.runPythonAsync(`
import json
from thai_ukrainian.fastthaig2p_service import (
    FastThaiG2PAnalysisError,
    analyze_with_fastthaig2p,
)
try:
    payload = {"status_code": 200, "body": analyze_with_fastthaig2p(INPUT_TEXT)}
except FastThaiG2PAnalysisError as exc:
    payload = {"status_code": exc.status_code, "detail": exc.detail}
json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
`);
    const payload = JSON.parse(responseText);
    if (payload.status_code !== 200) {
      const detail = payload.detail;
      const code = payload.status_code === 422 && detail?.code === "incomplete_ipa"
        ? "incomplete_ipa"
        : payload.status_code === 502
          ? "engine_inconsistent"
          : "analysis_failed";
      self.postMessage({
        type: "error",
        requestId,
        code,
        diagnostic: `Відмова рушія: HTTP ${payload.status_code}; код: ${detail?.code || "не вказано"}.`
      });
      return;
    }
    self.postMessage({ type: "result", requestId, result: payload.body });
  } catch (error) {
    self.postMessage({
      type: "error",
      requestId,
      code: error?.code || (phase === "runtime" ? "runtime_failed" : "analysis_failed"),
      diagnostic: String(error?.diagnostic || error?.message || "Невідома технічна причина.")
    });
  }
});
