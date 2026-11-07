import { analyze, analyzeThaiSyllablesForRomanization } from "./engine.js";
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

// Source-backed syllable boundaries are data, not direct romanization
// exceptions: every syllable still passes through the shared structural parser
// and the same RTGS onset/vowel/coda adapter.
const RTGS_EXAMPLE_SOURCE = "https://assets.publishing.service.gov.uk/media/5ab4e60aed915d78b9a459f5/ROMANIZATION_OF_THAI.pdf";
const RTGS_SYLLABLE_SEGMENTATIONS = new Map([
  ["สะอาด", ["สะ","อาด"]],
  ["สำอาง", ["สำ","อาง"]],
  ["บังอร", ["บัง","อร"]],
  ["ที่ราบ", ["ที่","ราบ"]],
  ["จริต", ["จะ","ริต"]],
  ["ศักราช", ["ศัก","กะ","ราช"]],
  ["ราชสีห์", ["ราช","ชะ","สี"]],
  ["แขนง", ["ขะ","แนง"]],
  ["เขย่า", ["ขะ","เย่า"]],
  ["เทวา", ["เท","วา"]],
  ["ปรารถนา", ["ปราถ","ถะ","นา"]],
  ["รัตนา", ["รัต","ตะ","นา"]],
  ["อินทรานุ", ["อิน","ทา","นุ"]],
  ["ลักษณ์", ["ลัก"]],
  ["ธาตุ", ["ธาต"]]
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
  const vowelKey = String(analysis.vowel).replace(/ː|ˑ/gu, "");
  let vowel = RTGS_VOWEL[vowelKey];
  if (vowel === undefined) return null;
  let codaKey = analysis.codaIpa || "";
  // Thai off-glides belong to the RTGS vowel spelling, not to a consonantal
  // y/w coda. This keeps /uaj/ as uai, /aj/ as ai, /aw/ as ao, etc.
  const glide = {
    "a:j":"ai","u:j":"ui","ua:j":"uai","ɯa:j":"ueai","ɔ:j":"oi","ɤ:j":"oei",
    "a:w":"ao","i:w":"io","e:w":"eo","ɛ:w":"aeo","ia:w":"iao"
  }[vowelKey + ":" + codaKey];
  if (glide) {
    vowel = glide;
    codaKey = "";
  }
  const coda = RTGS_CODA[codaKey];
  if (coda === undefined) return null;
  return {
    value: initial.join("") + vowel + coda,
    onset: initial.join(""),
    zeroOnset: initial.join("") === "",
    coda: codaKey && codaKey !== "ʔ" ? codaKey : null,
    source: "ClippyFirst structural syllable analysis → RTGS positional adapter"
  };
}

function needsHyphen(previous, current) {
  if (!previous || !current) return false;
  // RTGS hyphenation before vowel-initial syllables, including carrier อ.
  if (current.zeroOnset) return true;
  if (previous.coda == null && current.onset === "ng") return true;
  // Prevent a coda stop + following h from being read as kh/ph/th.
  if (["p","t","k"].includes(previous.coda) && current.onset.startsWith("h")) return true;
  return false;
}

function expandRrOrthography(word) {
  const index = word.indexOf("รร");
  if (index < 0) return null;
  const before = word.slice(0,index);
  const after = word.slice(index + 2);
  // Productive รร patterns: short a + final m before a word-final ม;
  // geminated m+a when ม begins the following syllable; an before a
  // following preposed-vowel syllable (e.g. กรรไกร).
  if (after === "ม") return before + "ัม";
  if (after.startsWith("ม") && after.length > 1) return before + "ัมมะ" + after.slice(1);
  if (/^[เแโใไ]/u.test(after)) return before + "ัน" + after;
  return null;
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

  const rrExpanded = expandRrOrthography(word);
  const lexicalSyllables = RTGS_SYLLABLE_SEGMENTATIONS.get(word);
  const analysis = lexicalSyllables
    ? { status:"analyzed", segmentation:"source-backed-syllable-lexicon", syllables:lexicalSyllables.map(analyze) }
    : analyzeThaiSyllablesForRomanization(rrExpanded || word);
  if (analysis.status === "analyzed" && analysis.syllables.every(item => item.status === "analyzed" && item.phonemicIpa)) {
    const rendered = renderSyllables(analysis.syllables);
    if (rendered) {
      return {
        status:"transliterated", input:word, value:rendered.value,
        source:lexicalSyllables ? "BGN/PCGN source-backed syllable boundaries + structural RTGS adapter" : rrExpanded ? "RTGS รร orthographic rule + structural syllable analysis" : "ClippyFirst structural syllable analysis → RTGS",\n        sourceUrl:lexicalSyllables ? RTGS_EXAMPLE_SOURCE : null,
        segmentation:analysis.segmentation, first:rendered.first, last:rendered.last,
        syllables:rendered.syllables
      };
    }
  }

  // Retain only reviewed lexical corrections from the legacy RTGS adapter.
  // Do not fall back to its generic grapheme heuristic for an unresolved word.
  const legacy = romanizeRtgsWord(word);
  if (legacy.status === "transliterated" &&
      legacy.evidenceStatus === "reviewed_lexical_correction") {
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
