// RTGS romanization port based on PyThaiNLP 5.4.0, transliterate/royin.py.
// SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
// SPDX-License-Identifier: Apache-2.0
// Offline browser port; token boundaries remain ClippyFirst's, not PyThaiNLP newmm.
// https://github.com/PyThaiNLP/pythainlp/blob/v5.4.0/pythainlp/transliterate/royin.py

const C = "กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬอฮ";
// Reviewed lexical RTGS corrections, kept separate from the upstream parity port.
const RTGS_UNSUPPORTED_TOKENS = new Set(["ๆ", "ฯ", "ฦ", "สตรีเศรษฐบุตรบำเพ็ญ"]);
const RTGS_LEXICAL_OVERRIDES = new Map([
  ["จริง", "ching"], ["สามารถ", "samat"], ["สวัสดี", "sawatdi"],
  ["สร้าง", "sang"], ["ศรี", "si"], ["เศร้า", "sao"], ["ไซร้", "sai"], ["ทรง", "song"], ["ทราม", "sam"],
  ["พัฒนา", "phatthana"], ["ฤทธิ์", "rit"], ["ฤๅ", "rue"],
  ["รถไฟ", "rotfai"], ["ผลไม้", "phonlamai"], ["ยูเครน", "yukhren"],
  ["ทราบ", "sap"], ["ทรัพย์", "sap"], ["แทรก", "saek"], ["อักษร", "akson"]
]);
const VOWELS = new Set(["a", "e", "i", "o", "u"]);
const CONSONANTS = {
  ก:["k","k"],ข:["kh","k"],ฃ:["kh","k"],ค:["kh","k"],ฅ:["kh","k"],ฆ:["kh","k"],ง:["ng","ng"],
  จ:["ch","t"],ฉ:["ch","t"],ช:["ch","t"],ซ:["s","t"],ฌ:["ch","t"],ญ:["y","n"],ฎ:["d","t"],ฏ:["t","t"],
  ฐ:["th","t"],ฑ:["th","t"],ฒ:["th","t"],ณ:["n","n"],ด:["d","t"],ต:["t","t"],ถ:["th","t"],ท:["th","t"],
  ธ:["th","t"],น:["n","n"],บ:["b","p"],ป:["p","p"],ผ:["ph","p"],ฝ:["f","p"],พ:["ph","p"],ฟ:["f","p"],
  ภ:["ph","p"],ม:["m","m"],ย:["y",""],ร:["r","n"],ฤ:["rue",""],ล:["l","n"],ว:["w",""],
  ศ:["s","t"],ษ:["s","t"],ส:["s","t"],ห:["h",""],ฬ:["l","n"],อ:["",""],ฮ:["h",""]
};
const CLUSTER_SECOND = new Set(["ร","ล","ว"]);
const THAI_CONSONANT = new RegExp("[" + C + "]");
const NORMALIZE = new RegExp("จน์|มณ์|ณฑ์|ทร์|ตร์|[" + C + "]\\u0e4c|[" + C + "][\\u0e30-\\u0e39]\\u0e4c|[\\u0e2f\\u0e46\\u0e48-\\u0e4f\\u0e5a\\u0e5b]", "gu");
const VOWEL_SOURCE = String.raw`เ*ียว,$1iao
แ*็ว,$1aeo
เ*ือย,$1ueai
แ*ว,$1aeo
เ*็ว,$1eo
เ*ว,$1eo
*ิว,$1io
*วย,$1uai
เ*ย,$1oei
*อย,$1oi
โ*ย,$1oi
*ุย,$1ui
*าย,$1ai
ไ*ย,$1ai
*ัย,$1ai
ไ**,$1$2ai
ใ**,$1$2ai
ไ*,$1ai
ใ*,$1ai
*ว*,$1ua$2
*ัวะ,$1ua
*ัว,$1ua
เ*ือะ,$1uea
เ*ือ,$1uea
เ*ียะ,$1ia
เ*ีย,$1ia
เ*อะ,$1oe
เ*อ,$1oe
เ*ิ,$1oe
*อ,$1o
เ*าะ,$1o
*็,$1e
โ*ะ,$1o
โ*,$1o
แ*ะ,$1ae
แ*,$1ae
เ*าะ,$1e
*าว,$1ao
เ*า,$1ao
เ*,$1e
*ู,$1u
*ุ,$1u
*ื,$1ue
*ึ,$1ue
*ี,$1i
*ิ,$1i
*ำ,$1am
*า,$1a
*ั,$1a
*ะ,$1a
#ฤ,$1rue
$ฤ,$1ri`;
const VOWEL_PATTERNS = VOWEL_SOURCE.split("\n").map(line => {
  const i = line.indexOf(",");
  const pattern = line.slice(0, i).replace(/\*/g, () => "(" + "[" + C + "])")
    .replace(/#/g, "([คนพมห])").replace(/\$/g, "([กตทปศส])");
  return [new RegExp(pattern, "gu"), line.slice(i + 1)];
});
const normalize = word => word.replace(NORMALIZE, "");
function replaceVowels(word) {
  for (const [pattern, replacement] of VOWEL_PATTERNS) word = word.replace(pattern, replacement);
  return word;
}
function doubleRoRua(word, i) {
  if (word.slice(i) === "รร") return ["a","n"];
  if (word.slice(i, i + 2) === "รร") return ["a"];
  return null;
}
function initialConsonant(word, i, consonants, j, out) {
  if (!out.some(c => c && !VOWELS.has(c))) {
    const initial = CONSONANTS[consonants[j]][0];
    return { chars: initial ? [initial] : [], vowelSeen: false };
  }
  const cluster = CLUSTER_SECOND.has(word[i]), last = i + 1 >= word.length;
  if (cluster && !last) return { chars:[CONSONANTS[consonants[j]][0]], vowelSeen:false };
  if (!cluster && !last) return { chars:["a", CONSONANTS[consonants[j]][0]].filter(Boolean), vowelSeen:false };
  return { chars:["o", CONSONANTS[consonants[j]][1]], vowelSeen:true };
}
function consonantAfterVowel(word, i, consonants, j) {
  if (i + 1 < word.length && !Object.hasOwn(CONSONANTS, word[i + 1]))
    return { value:CONSONANTS[consonants[j]][0], vowelSeen:false };
  return { value:CONSONANTS[consonants[j]][1], vowelSeen:true };
}
function replaceConsonants(word, consonants) {
  if (!consonants.length) return word;
  const out = []; let skip = false, j = 0, vowelSeen = false;
  for (let i = 0; i < word.length; i++) {
    const ch = word[i];
    if (skip) { skip = false; j++; }
    else if (!Object.hasOwn(CONSONANTS, ch)) { vowelSeen = true; out.push(ch); }
    else if (!out.length && ch === "ห" && consonants.length !== 1) j++;
    else {
      const rr = doubleRoRua(word, i);
      if (rr) { out.push(...rr); skip = true; vowelSeen = true; }
      else if (!vowelSeen) {
        const r = initialConsonant(word, i, consonants, j, out); out.push(...r.chars); vowelSeen = r.vowelSeen;
      } else {
        const r = consonantAfterVowel(word, i, consonants, j); out.push(r.value); vowelSeen = r.vowelSeen;
      }
      j++;
    }
  }
  return out.join("");
}
export function romanizeRtgsWord(input) {
  const original = String(input ?? "").normalize("NFC");
  if (!original || [...original].some(ch => /[^\u0E00-\u0E7F]/u.test(ch)))
    return { status:"unavailable", value:null, source:null };
  if (original === "ห") return { status:"transliterated", value:"", source:"PyThaiNLP 5.4.0 royin port + ClippyFirst orthographic correction" };
  if (RTGS_UNSUPPORTED_TOKENS.has(original)) return { status:"unavailable", value:null, source:null };
  if (RTGS_LEXICAL_OVERRIDES.has(original)) {
    return { status:"transliterated", value:RTGS_LEXICAL_OVERRIDES.get(original), source:"PyThaiNLP 5.4.0 royin port + ClippyFirst orthographic correction" };
  }
  // ทร is lexically variable; do not confidently romanize an unreviewed token by the generic consonant table.
  if (original.startsWith("ทร") || original.startsWith("แทร")) return { status:"unavailable", value:null, source:null };
  const normalized = normalize(original);
  // A leading vowel is written before ห, but in ห นำ clusters it belongs to the following sonorant.
  // Reorder only this orthographic pattern before vowel matching so ใหม่/ไหม become mai, not aim.
  const adjusted = normalized.replace(/^([เแโไใ])ห([งญนมยรลว])/, "ห$1$2");
  let word = replaceVowels(adjusted);
  const consonants = [...word].filter(ch => Object.hasOwn(CONSONANTS, ch));
  if ([...word].length === 2 && consonants.length === 2) {
    const chars = [...word]; chars.splice(1, 0, "o"); word = chars.join("");
  }
  const value = replaceConsonants(word, consonants);
  if (/[^\x00-\x7F]/u.test(value)) return { status:"unavailable", value:null, source:null };
  return { status:"transliterated", value, source:"PyThaiNLP 5.4.0 royin port + ClippyFirst orthographic correction" };
}
function shouldAddSeparator(prevWord, word, prevRomanized) {
  if (!prevRomanized || [...word].length < 2) return false;
  const prevAfterVowels = replaceVowels(normalize(prevWord));
  const prevConsonants = [...prevWord].filter(ch => THAI_CONSONANT.test(ch));
  const hasExplicitVowel = [...prevAfterVowels].length > prevConsonants.length;
  const consonants = [...word].filter(ch => THAI_CONSONANT.test(ch));
  return hasExplicitVowel && consonants.length === 2 && [...word].length - consonants.length === 0 &&
    !VOWELS.has([...prevRomanized].at(-1));
}
export function romanizeRtgsWords(words) {
  const result = [];
  for (let i = 0; i < (words || []).length; i++) {
    const word = String(words[i] ?? ""), item = romanizeRtgsWord(word);
    let value = item.status === "transliterated" ? item.value : word;
    if (i > 0 && item.status === "transliterated" &&
        shouldAddSeparator(String(words[i - 1] ?? ""), word, result[i - 1])) value = "a" + value;
    result.push(value);
  }
  return result.join("");
}
/** Uses the existing analyzer's token boundaries; it does not call PyThaiNLP newmm. */
export function romanizeRtgsTokenSequence(tokens) {
  let previousThai = null, previousRomanized = "";
  return (tokens || []).map(token => {
    if (token.kind !== "thai") {
      previousThai = null;
      previousRomanized = "";
      return { kind: token.kind, input: token.input, status: "passthrough", value: token.input, romanized: null };
    }
    const result = romanizeRtgsWord(token.input);
    if (result.status !== "transliterated") {
      previousThai = null;
      previousRomanized = "";
      return {
        kind: "thai", input: token.input, status: "unavailable",
        value: "⟦RTGS НЕ ПЕРЕВІРЕНО: " + token.input + "⟧", romanized: null
      };
    }
    let value = result.value;
    if (previousThai !== null && value &&
        shouldAddSeparator(previousThai, token.input, previousRomanized)) value = "a" + value;
    previousThai = token.input;
    previousRomanized = value;
    return { kind: "thai", input: token.input, status: "transliterated", value, romanized: value, source: result.source };
  });
}

export function renderRtgsTokens(tokens) {
  return romanizeRtgsTokenSequence(tokens).map(item => item.value).join("");
}
