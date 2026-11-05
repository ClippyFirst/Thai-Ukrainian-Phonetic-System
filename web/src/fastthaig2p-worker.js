import { loadPyodide } from "../vendor/pyodide/pyodide.mjs";

const INDEX_URL = new URL("../vendor/pyodide/", import.meta.url).href;
const MANIFEST_URL = new URL("../vendor/bundle-manifest.json", import.meta.url);
const WHEEL_BASE = new URL("../vendor/wheels/", import.meta.url);
const EXPECTED_PACKAGES = new Set([
  "fastthaig2p",
  "pythainlp",
  "thai-ukrainian-phonetic-system",
  "tzdata"
]);

let runtimePromise;

async function fetchManifest() {
  const response = await fetch(MANIFEST_URL, {
    credentials: "same-origin",
    cache: "force-cache"
  });
  if (!response.ok) throw new Error(`Не вдалося завантажити маніфест рушія (${response.status}).`);
  const manifest = await response.json();
  if (manifest.schema_version !== 1 || manifest.pyodide?.version !== "0.29.5") {
    throw new Error("Версія локального Pyodide bundle не відповідає перевіреній конфігурації.");
  }
  if (manifest.purpose === "public-pages" && manifest.redistribution_approved !== true) {
    throw new Error("Публічне розповсюдження компонентів рушія ще не погоджено.");
  }
  if (!Array.isArray(manifest.wheels) ||
      new Set(manifest.wheels.map(item => item.package)).size !== EXPECTED_PACKAGES.size ||
      [...EXPECTED_PACKAGES].some(name => !manifest.wheels.some(item => item.package === name))) {
    throw new Error("Маніфест локального рушія неповний.");
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
    if (!/^[a-zA-Z0-9_.-]+\.whl$/.test(asset.filename)) {
      throw new Error("Маніфест містить неприпустимий шлях до Python wheel.");
    }
    self.postMessage({ type: "progress", requestId, stage: "download", filename: asset.filename });
    const response = await fetch(new URL(asset.filename, WHEEL_BASE), {
      credentials: "same-origin",
      cache: "force-cache"
    });
    if (!response.ok) {
      throw new Error(`Не вдалося завантажити локальний компонент ${asset.filename} (${response.status}).`);
    }
    const buffer = await response.arrayBuffer();
    const digest = await crypto.subtle.digest("SHA-256", buffer);
    const actualHash = [...new Uint8Array(digest)]
      .map(value => value.toString(16).padStart(2, "0"))
      .join("");
    if (actualHash !== asset.sha256) {
      throw new Error(`Контрольна сума локального компонента ${asset.filename} не збігається.`);
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

  try {
    const pyodide = await getRuntime(requestId);
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
      self.postMessage({
        type: "analysis-error",
        requestId,
        message: typeof detail === "string"
          ? detail
          : detail?.message || "Не вдалося обробити тайський текст."
      });
      return;
    }
    self.postMessage({ type: "result", requestId, result: payload.body });
  } catch (error) {
    self.postMessage({
      type: "error",
      requestId,
      message: "Не вдалося запустити локальний рушій FastThaiG2P.",
      diagnostic: String(error?.message || error)
    });
  }
});
