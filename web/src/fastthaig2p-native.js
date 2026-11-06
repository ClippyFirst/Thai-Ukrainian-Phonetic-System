/**
 * Incremental browser-native FastThaiG2P port.
 *
 * This first slice ports the dictionary lookup/result adapter only. It is
 * intentionally NOT wired into the public UI: normalization, PyThaiNLP newmm
 * segmentation and the TLTK OOV fallback are still required for parity.
 */
import { adaptIpaToUkrainian } from "./ipa-ua.js";
import { normalizeFastThaiG2PText } from "./fastthaig2p-normalizer.js";
import { createFastThaiG2PNativeTokenizer } from "./fastthaig2p-tokenizer.js";

export const FASTTHAIG2P_UPSTREAM_COMMIT = "4e82a291b4cf2876326744c6580121e9986ad354";
export const NATIVE_PORT_STAGE = "dictionary-adapter-only";

const TONE_CATEGORIES = Object.freeze({
  "˧": "mid",
  "˨˩": "low",
  "˥˩": "falling",
  "˦˥": "high",
  "˩˩˦": "rising"
});

const TONE_SUFFIX = /([˥˦˧˨˩]+)$/u;

export class NativeFastThaiG2PError extends Error {
  constructor(code, message) {
    super(message);
    this.name = "NativeFastThaiG2PError";
    this.code = code;
  }
}

/**
 * Parse the upstream slash-delimited output without normalizing or guessing.
 * @param {string} raw
 * @returns {{wordGroups: string[], syllables: string[], passthrough: string}}
 */
export function parseFastThaiG2POutput(raw) {
  if (typeof raw !== "string") {
    throw new TypeError("FastThaiG2P output must be a string");
  }
  const wordGroups = [...raw.matchAll(/\/([^/]+)\//gu)].map(match => match[1].trim());
  const syllables = wordGroups.flatMap(group => group.split(".").filter(Boolean));
  const passthrough = raw.replace(/\/([^/]+)\//gu, "").trim();
  return { wordGroups, syllables, passthrough };
}

function syllableResult(rawIpa) {
  const toneMatch = TONE_SUFFIX.exec(rawIpa);
  const toneIpa = toneMatch?.[1] ?? null;
  const segmentalIpa = toneMatch ? rawIpa.slice(0, toneMatch.index) : rawIpa;
  const adaptation = adaptIpaToUkrainian(segmentalIpa);
  const warnings = [
    "FastThaiG2P output is not independently adjudicated phonetic gold.",
    "Its phonemic-versus-broad-surface status is not established; external IPA remains separate.",
    "Ukrainian output is a provisional practical adaptation, not an expert-validated transcription."
  ];
  if (toneIpa && !TONE_CATEGORIES[toneIpa]) {
    warnings.push("Unrecognized Chao tone contour retained without category mapping.");
  }
  if (!toneIpa) warnings.push("No terminal Chao tone contour was present in this syllable.");
  return {
    ipa: segmentalIpa,
    raw_ipa: rawIpa,
    tone: TONE_CATEGORIES[toneIpa] ?? null,
    tone_ipa: toneIpa,
    vowel_length: segmentalIpa.includes("ː") ? "long" : null,
    ukrainian: adaptation.output,
    adaptation_status: adaptation.status,
    rules_applied: adaptation.rulesApplied ?? [],
    neutralized_features: adaptation.neutralizedFeatures ?? [],
    provenance: [`FastThaiG2P@${FASTTHAIG2P_UPSTREAM_COMMIT}`],
    warnings: [...warnings, ...(adaptation.warnings ?? [])]
  };
}

/**
 * Construct a dictionary-only engine around the filtered, source-attributed
 * IPA map. A tokenizer is injected so the later newmm port can replace the
 * temporary whitespace tokenizer without changing the result contract.
 *
 * @param {{dictionary: Record<string,string>, tokenize?: (text:string)=>string[]}} options
 */
export function createFastThaiG2PNativeEngine({
  dictionary,
  tokenize = text => text.split(/\s+/u).filter(Boolean),
  normalize = text => text.normalize("NFC").trim()
}) {
  if (!dictionary || typeof dictionary !== "object" || Array.isArray(dictionary)) {
    throw new TypeError("A FastThaiG2P IPA dictionary object is required");
  }
  for (const [word, ipa] of Object.entries(dictionary)) {
    if (!word || typeof ipa !== "string" || !/^\/[^/]+\/$/u.test(ipa)) {
      throw new TypeError(`Invalid source-attributed IPA dictionary entry: ${word}`);
    }
  }

  return Object.freeze({
    stage: NATIVE_PORT_STAGE,
    upstreamCommit: FASTTHAIG2P_UPSTREAM_COMMIT,
    convert(text) {
      if (typeof text !== "string" || !text.trim()) {
        throw new NativeFastThaiG2PError("empty_input", "Введіть тайський текст.");
      }
      const normalized = normalize(text);
      if (typeof normalized !== "string") {
        throw new NativeFastThaiG2PError("normalization_failed", "Нормалізатор повернув не текст.");
      }
      const tokens = tokenize(normalized);
      if (!Array.isArray(tokens) || !tokens.length || tokens.some(token => typeof token !== "string" || !token)) {
        throw new NativeFastThaiG2PError("tokenization_failed", "Не вдалося сегментувати текст.");
      }

      const wordGroups = [];
      for (const token of tokens) {
        const ipa = dictionary[token];
        if (!ipa) {
          throw new NativeFastThaiG2PError(
            "native_dictionary_miss",
            `Нативний порт поки не підтримує токенізацію або OOV-обробку для фрагмента довжиною ${[...token].length}.`
          );
        }
        wordGroups.push(ipa.slice(1, -1));
      }

      const rawIpa = wordGroups.map(group => `/${group}/`).join(" ");
      const parsed = parseFastThaiG2POutput(rawIpa);
      if (parsed.passthrough || parsed.wordGroups.length !== tokens.length) {
        throw new NativeFastThaiG2PError("native_output_inconsistent", "Нативний адаптер отримав неузгоджений IPA-вихід.");
      }

      const words = tokens.map((token, index) => {
        const rawGroup = parsed.wordGroups[index];
        const syllables = rawGroup.split(".").filter(Boolean).map(syllableResult);
        const ukrainian = syllables.map(item =>
          item.ukrainian == null ? `⟦НЕВИЗНАЧЕНО: ${item.raw_ipa}⟧` : item.ukrainian
        ).join("");
        return {
          thai: token,
          fastthaig2p_ipa: `/${rawGroup}/`,
          ukrainian,
          syllables
        };
      });

      return {
        input: text,
        normalized_input: normalized,
        engine: "FastThaiG2P",
        upstream_commit: FASTTHAIG2P_UPSTREAM_COMMIT,
        status: "provisional",
        raw_ipa: rawIpa,
        ukrainian: words.map(word => word.ukrainian).join(" "),
        words,
        coverage: { dictionary_tokens: tokens.length, rule_fallback_tokens: 0 },
        warnings: [
          "Це експериментальний нативний JavaScript-порт: нормалізація, newmm сегментація та словниковий IPA-пошук реалізовані окремими модулями.",
          "TLTK OOV fallback ще не портований; невідомі токени відхиляються без здогадок, тому це поки не повна заміна FastThaiG2P.",
          "Український запис є попередньою практичною адаптацією IPA, не підтвердженою незалежними фахівцями."
        ]
      };
    }
  });
}

/**
 * Load and verify the generated source-filtered dictionary on demand. The
 * dictionary is a data asset; this loader never loads Python, Pyodide or wheels.
 */
export async function loadFastThaiG2PNativeDictionary({
  url = new URL("../vendor/native/fastthaig2p-ipa.json", import.meta.url),
  manifestUrl = new URL("../vendor/native/manifest.json", import.meta.url),
  fetchImpl = fetch,
  cryptoImpl = globalThis.crypto
} = {}) {
  const manifestResponse = await fetchImpl(manifestUrl, {
    credentials: "same-origin",
    cache: "force-cache"
  });
  if (!manifestResponse.ok) {
    throw new NativeFastThaiG2PError("native_manifest_unavailable", `HTTP ${manifestResponse.status}`);
  }
  const manifest = await manifestResponse.json();
  if (
    manifest?.schema_version !== 1 ||
    manifest?.upstream_commit !== FASTTHAIG2P_UPSTREAM_COMMIT ||
    manifest?.stage !== "dictionary-normalizer-and-default-wordlist-data-only; not a complete runtime" ||
    manifest?.dictionary_license !== "CC-BY-SA-4.0" ||
    manifest?.normalizer_license !== "Apache-2.0" ||
    manifest?.pythainlp_version !== "5.4.0" ||
    manifest?.pythainlp_wordlist_license !== "CC0-1.0" ||
    !Number.isInteger(manifest?.pythainlp_wordlist_entries) ||
    !Number.isInteger(manifest?.dictionary_entries)
  ) {
    throw new NativeFastThaiG2PError("native_manifest_invalid", "Native dictionary manifest does not match the reviewed source contract");
  }
  const asset = manifest.assets?.find(item => item.path === "native/fastthaig2p-ipa.json");
  if (!asset || !/^[a-f0-9]{64}$/u.test(asset.sha256) || !Number.isInteger(asset.size_bytes)) {
    throw new NativeFastThaiG2PError("native_manifest_invalid", "Native dictionary integrity record is missing");
  }

  const response = await fetchImpl(url, {
    credentials: "same-origin",
    cache: "force-cache"
  });
  if (!response.ok) {
    throw new NativeFastThaiG2PError("native_dictionary_unavailable", `HTTP ${response.status}`);
  }
  const buffer = await response.arrayBuffer();
  if (buffer.byteLength !== asset.size_bytes) {
    throw new NativeFastThaiG2PError("native_dictionary_corrupt", "Native IPA dictionary size does not match its manifest");
  }
  if (!cryptoImpl?.subtle?.digest) {
    throw new NativeFastThaiG2PError("native_integrity_unavailable", "Web Crypto SHA-256 is required to verify the native dictionary");
  }
  const digest = await cryptoImpl.subtle.digest("SHA-256", buffer);
  const actualHash = [...new Uint8Array(digest)]
    .map(value => value.toString(16).padStart(2, "0"))
    .join("");
  if (actualHash !== asset.sha256) {
    throw new NativeFastThaiG2PError("native_dictionary_corrupt", "Native IPA dictionary SHA-256 does not match its manifest");
  }

  let dictionary;
  try {
    dictionary = JSON.parse(new TextDecoder().decode(buffer));
  } catch {
    throw new NativeFastThaiG2PError("native_dictionary_invalid", "Native IPA dictionary is not valid UTF-8 JSON");
  }
  if (
    !dictionary ||
    typeof dictionary !== "object" ||
    Array.isArray(dictionary) ||
    Object.keys(dictionary).length !== manifest.dictionary_entries
  ) {
    throw new NativeFastThaiG2PError("native_dictionary_invalid", "Native IPA dictionary entry count does not match its manifest");
  }
  return dictionary;
}

/**
 * Compose the native normalization, PyThaiNLP default newmm tokenizer,
 * FastThaiG2P custom newmm tokenizer and filtered IPA dictionary. OOV words
 * fail closed until a licensed, parity-tested fallback port is available.
 */
export function createFastThaiG2PNativePipeline({ dictionary, normalizerData, defaultWords }) {
  if (!normalizerData || !Array.isArray(defaultWords) || !defaultWords.length) {
    throw new TypeError("Native normalizer data and the pinned PyThaiNLP default wordlist are required");
  }
  const defaultTokenizer = createFastThaiG2PNativeTokenizer(defaultWords);
  const customTokenizer = createFastThaiG2PNativeTokenizer(Object.keys(dictionary));
  const adapter = createFastThaiG2PNativeEngine({
    dictionary,
    normalize: text => normalizeFastThaiG2PText(text, {
      data: normalizerData,
      wordTokenize: value => defaultTokenizer.tokenize(value)
    }),
    tokenize: text => customTokenizer.tokenize(text).filter(token => token.trim() !== "")
  });
  return Object.freeze({
    ...adapter,
    stage: "normalizer+default-newmm+custom-newmm+wiktionary-dictionary; no-oov-fallback"
  });
}
