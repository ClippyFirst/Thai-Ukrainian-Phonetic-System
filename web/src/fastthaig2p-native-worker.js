/**
 * Browser-native FastThaiG2P front-half worker.
 * This worker imports only ClippyFirst JavaScript modules and same-origin data.
 * It does not import Pyodide, Python, wheels, WASM or a remote API.
 */
import {
  createFastThaiG2PNativePipeline,
  loadFastThaiG2PNativeAssets
} from "./fastthaig2p-native.js";
import { createTltkOovFallback, loadTltkOovData } from "./fastthaig2p-tltk-oov.js";

let pipelinePromise;
let oovFallbackPromise;

function getOovFallback() {
  if (!oovFallbackPromise) {
    oovFallbackPromise = loadTltkOovData().then(createTltkOovFallback);
  }
  return oovFallbackPromise;
}

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
      let result;
      try {
        result = pipeline.convert(message.text);
      } catch (error) {
        if (error?.code !== "native_dictionary_miss") throw error;
        try {
          const oovFallback = await getOovFallback();
          result = pipeline.convert(message.text, { oovFallback: oovFallback.convert });
        } catch (oovError) {
          if (oovError?.code === "native_dictionary_miss") throw oovError;
          // A missing/corrupt/unavailable OOV data pack is a safe fallback
          // condition, not permission to guess a pronunciation.
          self.postMessage({
            type: "error",
            id,
            code: "native_dictionary_miss",
            message: "Нативний OOV-пакет недоступний або не пройшов перевірку; буде використано сумісний резервний рушій."
          });
          return;
        }
      }
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
      message: error?.name === "NativeFastThaiG2PError" && typeof error.message === "string"
        ? error.message
        : "Не вдалося ініціалізувати або виконати браузерну транскрипцію. Спробуйте оновити сторінку."
    });
  }
});
