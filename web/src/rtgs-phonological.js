import { analyzeThaiSyllablesForRomanization } from "./engine.js";
import { romanizeRtgsWord } from "./rtgs-reference.js";

const RTGS_INITIAL = Object.freeze({
  "ก":"k","ข":"kh","ฃ":"kh","ค":"kh","ฅ":"kh","ฆ":"kh","ง":"ng",
  "จ":"ch","ฉ":"ch","ช":"ch","ซ":"s","ฌ":"ch","ญ":"y","ฎ":"d","ฏ":"t",
  "ฐ":"th","ฑ":"th","ฒ":"th","ณ":"n","ด":"d","ต":"t","ถ":"th","ท":"th",
  "ธ":"th","น":"n","บ":"b","ป":"p","ผ":"ph","ฝ":"f","พ":"ph","ฟ":"f",
  "ภ":"ph","ม":"m","ย":"y","ร":"r","ล":"l","ว":"w","ศ":"s","ษ":"s",
  "ส":"s","ห":"h","ฬ":"l","อ":"","ฮ":"h"
});
const RTGS_CODA = Object.freeze({
  "p":"p","t":"t","k":"k","m":"m","n":"n","ŋ":"ng","j":"y","w":"w","ʔ":""
});
const RTGS_VOWEL = Object.freeze({
  "a":"a","i":"i","ɯ":"ue","u":"u","e":"e","ɛ":"ae","ɤ":"oe","o":"o","ɔ":"o",
  "ia":"ia","ɯa":"uea","ua":"ua","aj":"ai","aw":"ao","am":"am","uj":"ui",
  "ɔj":"oi","ɤj":"oei","uaj":"uai","ɯaj":"ueai","iw":"io","ew":"eo",
  "ɛw":"aeo","iaw":"iao"
});
const LEADING_H_SECOND = new Set(["ง","ญ","น","ม","ย","ร","ล","ว"]);

// The official proper-name spelling is a lexical word-boundary decision, not
// a grapheme exception. Keep its source and scope explicit.
const RTGS_PROPER_NAMES = new Map([
  ["กรุงเทพมหานคร", {
    value:"krung thep maha nakhon",
    source:"Royal Society of Thailand official proper-name form",
    url:"https://www.orst.go.th/FILEROOM/CABROYINWEB/DRAWER004/GENERAL/DATA0004/00004233.PDF"
  }]
]);

// A small evidence-backed layer is reserved for readings that the spelling
// alone does not resolve productively (notably ทร and the abbreviation ฯ).
const RTGS_SOURCE_ATTESTED_READINGS = new Map([
  ["ทราย", { value:"sai", source:"BGN/PCGN 2002 Agreement, RTGS example", sourceUrl:"https://assets.publishing.service.gov.uk/media/5ab4e60aed915d78b9a459f5/ROMANIZATION_OF_THAI.pdf" }],
  ["ทรราช", { value:"thorarat", source:"BGN/PCGN 2002 Agreement, RTGS example", sourceUrl:"https://assets.publishing.service.gov.uk/media/5ab4e60aed915d78b9a459f5/ROMANIZATION_OF_THAI.pdf" }],
  ["โปรดเกล้าฯ", { value:"protklao protkramom", source:"BGN/PCGN 2002 Agreement, RTGS abbreviation example", sourceUrl:"https://assets.publishing.service.gov.uk/media/5ab4e60aed915d78b9a459f5/ROMANIZATION_OF_THAI.pdf" }]
]);

function effectiveOnset(onset) {
  if (onset.length === 2 && onset[0] === "ห" && LEADING_H_SECOND.has(onset[1])) {
    return onset.slice(1);
  }
  return onset;
}

function romanizeSyllable(analysis) {
  if (analysis?.status !== "analyzed" || !analysis.vowel) return null;
  const onset = effectiveOnset(analysis.onset || []);
  const initial = onset.map(grapheme => RTGS_INITIAL[grapheme]);
  if (initial.some(value => value === undefined)) return null;
  const vowel = RTGS_VOWEL[String(analysis.vowel).replace(/ː|ˑ/gu, "")];
  if (vowel === undefined) return null;
  const codaKey = analysis.codaIpa || "";
  const coda = RTGS_CODA[codaKey];
  if (coda === undefined) return null;
  return {
    value: initial.join("") + vowel + coda,
    onset: initial.join(""),
    zeroOnset: initial.join("") === "",
    coda: codaKey || null,
    source: "ClippyFirst structural syllable analysis → RTGS positional adapter"
  };
}

function needsHyphen(previous, current) {
  if (!previous || !current) return false;
  if (previous.coda == null && current.zeroOnset) return true;
  if (previous.coda == null && current.onset === "ng") return true;
  if (previous.coda === "ŋ" && current.zeroOnset) return true;
  if (["p","t","k"].includes(previous.coda) && current.onset.startsWith("h")) return true;
  return false;
}

function renderSyllables(syllables) {
  const rendered = [];
  for (const syllable of syllables) {
    const item = romanizeSyllable(syllable);
    if (!item) return null;
    const previous = rendered.at(-1);
    const separator = previous ? (needsHyphen(previous, item) ? "-" : "") : "";
    rendered.push({ ...item, separator });
  }
  return {
    value: rendered.map(item => item.separator + item.value).join(""),
    first: rendered[0] || null,
    last: rendered.at(-1) || null,
    syllables: rendered
  };
}

export function romanizeRtgsThaiToken(input) {
  const word = String(input ?? "").normalize("NFC");
  if (!word) return { status:"unavailable", value:null, source:null };
  if (RTGS_PROPER_NAMES.has(word)) {
    const record = RTGS_PROPER_NAMES.get(word);
    return { status:"transliterated", input:word, value:record.value, source:record.source, sourceUrl:record.url, first:null, last:null, lexicalPhrase:true };
  }
  if (RTGS_SOURCE_ATTESTED_READINGS.has(word)) {
    const record = RTGS_SOURCE_ATTESTED_READINGS.get(word);
    return { status:"transliterated", input:word, value:record.value, source:record.source, sourceUrl:record.sourceUrl, first:null, last:null, lexicalPhrase:true };
  }

  const analysis = analyzeThaiSyllablesForRomanization(word);
  if (analysis.status === "analyzed") {
    const rendered = renderSyllables(analysis.syllables);
    if (rendered) {
      return {
        status:"transliterated", input:word, value:rendered.value,
        source:rendered.syllables.some(item => item.source) ? "ClippyFirst structural syllable analysis → RTGS" : "ClippyFirst structural syllable analysis → RTGS",
        segmentation:analysis.segmentation, first:rendered.first, last:rendered.last,
        syllables:rendered.syllables
      };
    }
  }

  // Retain only reviewed lexical corrections from the legacy RTGS adapter.
  // Do not fall back to its generic grapheme heuristic for an unresolved word.
  const legacy = romanizeRtgsWord(word);
  if (legacy.status === "transliterated" &&
      legacy.source === "PyThaiNLP 5.4.0 royin port + ClippyFirst orthographic correction") {
    return {
      status:"transliterated", input:word, value:legacy.value,
      source:"Reviewed ClippyFirst lexical RTGS correction", first:null, last:null,
      lexicalPhrase:true
    };
  }
  return { status:"unavailable", input:word, value:null, source:null, reason:"unresolved-syllable-or-lexical-reading" };
}

export function romanizeRtgsTokenSequence(tokens) {
  const details = [];
  let previous = null;
  let previousWord = null;
  let output = "";
  let unavailableCount = 0;

  for (const token of tokens || []) {
    if (token.kind !== "thai") {
      const value = token.input;
      details.push({ kind:token.kind, input:token.input, status:"passthrough", value, romanized:null, separatorBefore:"" });
      output += value;
      previous = null;
      previousWord = null;
      continue;
    }

    if (token.input === "ๆ") {
      if (previousWord) {
        details.push({ kind:"thai", input:token.input, status:"transliterated", value:previousWord.value, romanized:previousWord.value, separatorBefore:"", source:"RTGS reduplication-mark rule" });
        output += previousWord.value;
      } else {
        unavailableCount += 1;
        const value = "⟦RTGS НЕ ПЕРЕВІРЕНО: " + token.input + "⟧";
        details.push({ kind:"thai", input:token.input, status:"unavailable", value, romanized:null, separatorBefore:"" });
        output += value;
      }
      previous = null;
      continue;
    }

    const result = romanizeRtgsThaiToken(token.input);
    if (result.status !== "transliterated") {
      unavailableCount += 1;
      const value = "⟦RTGS НЕ ПЕРЕВІРЕНО: " + token.input + "⟧";
      details.push({ kind:"thai", input:token.input, status:"unavailable", value, romanized:null, separatorBefore:"" });
      output += value;
      previous = null;
      previousWord = null;
      continue;
    }

    let separatorBefore = "";
    if (previous && result.first && previous.last && needsHyphen(previous.last, result.first)) {
      separatorBefore = "-";
    } else if (previousWord) {
      separatorBefore = " ";
    }
    const detail = {
      kind:"thai", input:result.input, status:"transliterated",
      value:result.value, romanized:result.value, separatorBefore,
      source:result.source, segmentation:result.segmentation || null
    };
    details.push(detail);
    output += separatorBefore + result.value;
    previous = result;
    previousWord = result;
  }

  return { details, output, unavailableCount };
}
