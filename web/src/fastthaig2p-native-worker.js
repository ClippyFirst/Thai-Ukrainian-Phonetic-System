/**
 * Browser-native FastThaiG2P front-half worker.
 * This worker imports only ClippyFirst JavaScript modules and same-origin data.
 * It does not import Pyodide, Python, wheels, WASM or a remote API.
 */
import {
  createFastThaiG2PNativePipeline,
  loadFastThaiG2PNativeAssets
} from "./fastthaig2p-native.js";

let pipelinePromise;

function getPipeline() {
  if (!pipelinePromise) {
    pipelinePromise = loadFastThaiG2PNativeAssets().then(assets =>
      createFastThaiG2PNativePipeline(assets)
    );
  }
  return pipelinePromise;
}

self.addEventListener("message", async event => {
  const message = event.data || {};
  const { type, id } = message;
  try {
    const pipeline = await getPipeline();
    if (type === "init") {
      self.postMessage({ type: "ready", id, stage: pipeline.stage });
      return;
    }
    if (type === "convert") {
      const result = pipeline.convert(message.text);
      self.postMessage({ type: "result", id, result });
      return;
    }
    self.postMessage({
      type: "error",
      id,
      code: "native_unknown_message",
      message: "Невідома команда браузерного рушія."
    });
  } catch (error) {
    self.postMessage({
      type: "error",
      id,
      code: typeof error?.code === "string" ? error.code : "native_engine_error",
      message: typeof error?.message === "string" ? error.message : "Браузерний рушій не зміг обробити текст."
    });
  }
});
