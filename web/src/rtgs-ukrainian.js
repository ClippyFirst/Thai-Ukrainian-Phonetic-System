import { romanizeRtgsTokenSequence } from "./rtgs-reference.js";

// Project-defined rendering of RTGS letter sequences in Ukrainian script.
// Digraph h is retained as х (kh/ph/th → кх/пх/тх); this is not IPA adaptation.
const DIGRAPHS = Object.freeze({
  kh: "кх",
  ph: "пх",
  th: "тх",
  ch: "ч",
  ng: "нг"
});
// RTGS rimes are adapted as syllabic units, not letter by letter.
// Values follow the phonetic distinctions retained by the RTGS vowel table.
const Y_ONSET_SEQUENCES = Object.freeze({
  ya: "я", ye: "є", yi: "ї", yo: "йо", yu: "ю"
});
const RIME_SEQUENCES = Object.freeze({
  ueai: "иай", iao: "іо", aeo: "еу", oei: "ей",
  uai: "уай", uea: "иа",
  ai: "ай", am: "ам", ao: "ау", io: "іу", ui: "уй",
  eo: "еу", oi: "ой", ia: "іа", ue: "и", oe: "е",
  ae: "е", ua: "уа"
});
const LETTERS = Object.freeze({
  a: "а", b: "б", d: "д", e: "е", f: "ф", h: "х", i: "і",
  k: "к", l: "л", m: "м", n: "н", o: "о", p: "п", r: "р",
  s: "с", t: "т", u: "у", w: "в", y: "й"
});

export function adaptRtgsToUkrainian(romanized) {
  if (typeof romanized !== "string") {
    return { status: "unavailable", input: romanized, output: null, rulesApplied: [], warning: "RTGS input must be a string." };
  }
  const output = [];
  const rulesApplied = [];
  let i = 0;
  while (i < romanized.length) {
    const lower = romanized.slice(i).toLowerCase();
    const yOnset = romanized[i].toLowerCase() === "y"
      ? Object.keys(Y_ONSET_SEQUENCES).find(sequence => lower.startsWith(sequence))
      : null;
    if (yOnset) {
      output.push(Y_ONSET_SEQUENCES[yOnset]);
      rulesApplied.push("RTGS-ONSET-" + yOnset.toUpperCase());
      i += yOnset.length;
      continue;
    }
    const rime = Object.keys(RIME_SEQUENCES).find(sequence => lower.startsWith(sequence));
    if (rime) {
      output.push(RIME_SEQUENCES[rime]);
      rulesApplied.push("RTGS-RIME-" + rime.toUpperCase());
      i += rime.length;
      continue;
    }
    const pair = romanized.slice(i, i + 2).toLowerCase();
    if (Object.hasOwn(DIGRAPHS, pair)) {
      output.push(DIGRAPHS[pair]);
      rulesApplied.push("RTGS-" + pair.toUpperCase());
      i += 2;
      continue;
    }
    const char = romanized[i];
    if (/[A-Za-z]/u.test(char)) {
      const mapped = LETTERS[char.toLowerCase()];
      if (!mapped) {
        return {
          status: "unavailable", input: romanized, output: null,
          rulesApplied, warning: "Unsupported RTGS letter " + JSON.stringify(char) + "; Ukrainian output withheld."
        };
      }
      output.push(mapped);
      rulesApplied.push("RTGS-" + char.toLowerCase());
      i += 1;
      continue;
    }
    // Keep separators, punctuation and digits exactly as RTGS supplied them.
    output.push(char);
    i += 1;
  }
  return {
    status: "adapted", input: romanized, output: output.join(""),
    rulesApplied: [...new Set(rulesApplied)], warning: null
  };
}

export function renderRtgsUkrainianTokens(tokens) {
  return romanizeRtgsTokenSequence(tokens).map(item => {
    if (item.kind !== "thai" || item.status !== "transliterated") return item.value;
    const adapted = adaptRtgsToUkrainian(item.romanized);
    return adapted.status === "adapted"
      ? adapted.output
      : "⟦RTGS НЕ ПЕРЕВІРЕНО: " + item.input + "⟧";
  }).join("");
}
