/**
 * IPA → Ukrainian practical adaptation.
 * Thai orthography is deliberately absent from this module.
 * IPA remains the source of truth; source contrasts may be neutralized only here.
 *
 * Accepts common IPA presentation conventions (phonemic /slashes/, phonetic
 * [brackets], Thai tone letters, stress marks and tied affricate notation).
 * It never guesses an unknown segment: unrecognized symbols withhold output.
 */
const SEGMENTS = new Map([
  ["tɕʰ", {out:"ч", rule:"UA-AFFRICATE-ASP", neutralized:["aspiration"]}],
  ["tɕ", {out:"ч", rule:"UA-AFFRICATE", preserved:["place","manner"]}],
  ["kʰ", {out:"к", rule:"UA-K-ASP", neutralized:["aspiration"]}],
  ["pʰ", {out:"п", rule:"UA-P-ASP", neutralized:["aspiration"]}],
  ["tʰ", {out:"т", rule:"UA-T-ASP", neutralized:["aspiration"]}],
  ["k", {out:"к", rule:"UA-K", preserved:["place","manner"]}],
  ["p", {out:"п", rule:"UA-P", preserved:["place","manner"]}],
  ["t", {out:"т", rule:"UA-T", preserved:["place","manner"]}],
  ["d", {out:"д", rule:"UA-D", preserved:["voicing","place","manner"]}],
  ["b", {out:"б", rule:"UA-B", preserved:["voicing","place","manner"]}],
  ["ŋ", {out:"нг", rule:"UA-NG", preserved:["nasal"], neutralized:["velar nasal has no single conventional Ukrainian grapheme"]}],
  ["n", {out:"н", rule:"UA-N", preserved:["nasal"]}],
  ["m", {out:"м", rule:"UA-M", preserved:["nasal"]}],
  ["r", {out:"р", rule:"UA-R", preserved:["rhotic"]}],
  ["l", {out:"л", rule:"UA-L", preserved:["lateral"]}],
  ["j", {out:"й", rule:"UA-J", preserved:["glide"]}],
  ["w", {out:"в", rule:"UA-W", preserved:["glide"], neutralized:["labio-velar glide approximated as Ukrainian в"]}],
  ["s", {out:"с", rule:"UA-S", preserved:["frication"]}],
  ["f", {out:"ф", rule:"UA-F", preserved:["frication","labiodental place"]}],
  ["h", {out:"х", rule:"UA-H", preserved:["frication"], neutralized:["glottal place"]}],
  ["ʔ", {out:"", rule:"UA-GLOTTAL-STOP", neutralized:["glottal stop"]}],
  ["a", {out:"а", rule:"UA-A", preserved:["vowel quality"], neutralized:["length"]}],
  ["i", {out:"і", rule:"UA-I", preserved:["vowel quality"], neutralized:["length"]}],
  ["e", {out:"е", rule:"UA-E", preserved:["vowel quality"], neutralized:["length"]}],
  ["ɛ", {out:"е", rule:"UA-EPSILON", neutralized:["open-mid front vowel quality","length"]}],
  ["ɯ", {out:"и", rule:"UA-BARRED-I", neutralized:["backness","unroundedness","length"]}],
  ["ɤ", {out:"е", rule:"UA-GAMMA", neutralized:["backness","height","length"]}],
  ["u", {out:"у", rule:"UA-U", preserved:["vowel quality"], neutralized:["length"]}],
  ["o", {out:"о", rule:"UA-O", preserved:["vowel quality"], neutralized:["length"]}],
  ["ɔ", {out:"о", rule:"UA-OPEN-O", neutralized:["openness","length"]}]
]);
const ORDER = [...SEGMENTS.keys()].sort((a,b)=>b.length-a.length);
const TONE_DIACRITICS = new Set(["\u0300","\u0301","\u0302","\u0304","\u030c","\u030b","\u030f"]); // U+0306 breve can mark extra-shortness; preserve/fail closed.
const IPA_MODIFIERS = new Set(["\u031a","\u032f","\u0329","\u02d0","\u02d1"]);

function normalizeIpaInput(sourceIpa) {
  let ipa = sourceIpa.trim();
  let wrapped = false;
  if ((ipa.startsWith("[") && ipa.endsWith("]")) ||
      (ipa.startsWith("/") && ipa.endsWith("/") && ipa.length > 1)) {
    ipa = ipa.slice(1, -1).trim();
    wrapped = true;
  }
  // IPA ties are typography, not additional segments. Canonicalize the Thai
  // alveolo-palatal affricate before tokenization.
  ipa = ipa.replace(/t[\u0361\u035c]ɕ/g, "tɕ");
  ipa = ipa.normalize("NFD");
  let toneNotationSeen = false;
  let stressNotationSeen = false;
  let lengthNotationSeen = false;
  let modifierNotationSeen = false;
  let normalized = "";
  for (const char of ipa) {
    if ("˥˦˧˨˩".includes(char)) {
      toneNotationSeen = true;
      continue;
    }
    if (char === "ˈ" || char === "ˌ") {
      stressNotationSeen = true;
      continue;
    }
    if (TONE_DIACRITICS.has(char)) {
      toneNotationSeen = true;
      continue;
    }
    if (char === "ː" || char === "ˑ") {
      lengthNotationSeen = true;
      normalized += char;
      continue;
    }
    if (IPA_MODIFIERS.has(char)) {
      modifierNotationSeen = true;
      normalized += char;
      continue;
    }
    normalized += char;
  }
  return {
    ipa: normalized.normalize("NFC"),
    notes: {
      wrapped,
      toneNotationSeen,
      stressNotationSeen,
      lengthNotationSeen,
      modifierNotationSeen
    }
  };
}

export function adaptIpaToUkrainian(sourceIpa) {
  if (typeof sourceIpa !== "string" || !sourceIpa.trim()) {
    return {status:"withheld", sourceIpa:sourceIpa ?? null, normalizedIpa:null, output:null, candidates:[], preservedFeatures:[], neutralizedFeatures:[], rulesApplied:[], inputNotes:[], warnings:["IPA input is empty."]};
  }
  const normalized = normalizeIpaInput(sourceIpa);
  const ipa = normalized.ipa;
  const inputNotes = [];
  if (normalized.notes.wrapped) inputNotes.push("IPA delimiters normalized");
  if (normalized.notes.toneNotationSeen) inputNotes.push("tone notation recognized and kept outside segmental Ukrainian spelling");
  if (normalized.notes.stressNotationSeen) inputNotes.push("stress notation recognized and not represented in practical Ukrainian spelling");
  if (normalized.notes.lengthNotationSeen) inputNotes.push("vowel length notation recognized");
  if (normalized.notes.modifierNotationSeen) inputNotes.push("phonetic modifiers recognized");
  if (!ipa.trim()) {
    return {status:"withheld", sourceIpa, normalizedIpa:ipa, output:null, candidates:[], preservedFeatures:[], neutralizedFeatures:[], rulesApplied:[], inputNotes, warnings:["IPA input contains no supported segmental symbols after normalization."]};
  }

  const tokens = [];
  for (let i=0;i<ipa.length;) {
    if (/[.\s]/u.test(ipa[i])) { tokens.push({text:ipa[i], out:ipa[i], rule:null}); i++; continue; }
    if (ipa[i] === "ː" || ipa[i] === "ˑ" || ipa[i] === "\u032f" || ipa[i] === "\u0329" || ipa[i] === "\u031a") {
      tokens.push({text:ipa[i], out:"", rule:"UA-DIACRITIC-NEUTRALIZATION", neutralized:[ipa[i] === "ː" || ipa[i] === "ˑ" ? "vowel length" : "phonetic detail not represented in Ukrainian practical spelling"]});
      i++; continue;
    }
    const key = ORDER.find(k => ipa.startsWith(k,i));
    if (!key) return {status:"withheld", sourceIpa, normalizedIpa:ipa, output:null, candidates:[], preservedFeatures:[], neutralizedFeatures:[], rulesApplied:[], inputNotes, warnings:["Невідомий або непідтримуваний IPA-символ: "+[...ipa.slice(i)][0]+". Український результат не вгадується."]};
    const rule=SEGMENTS.get(key);
    tokens.push({text:key,...rule});
    i += key.length;
  }
  for (let i=1;i<tokens.length;i++) {
    if (tokens[i].text === "w" && tokens[i-1].text && /^(?:a|i|e|ɛ|ɯ|ɤ|u|o|ɔ|ː|ˑ)$/u.test(tokens[i-1].text)) {
      tokens[i] = {...tokens[i], out:"у", rule:"UA-W-VOCALIC", neutralized:[...(tokens[i].neutralized||[]),"glide-vowel sequence adapted as Ukrainian vowel spelling"]};
    }
  }
  const preservedFeatures=[...new Set(tokens.flatMap(t=>t.preserved||[]))];
  const neutralizedFeatures=[...new Set(tokens.flatMap(t=>t.neutralized||[]))];
  if (normalized.notes.toneNotationSeen) neutralizedFeatures.push("lexical tone is not encoded in Ukrainian practical spelling");
  if (normalized.notes.stressNotationSeen) neutralizedFeatures.push("stress is not encoded by this project adaptation");
  if (normalized.notes.lengthNotationSeen) neutralizedFeatures.push("vowel length");
  const rulesApplied=[...new Set(tokens.map(t=>t.rule).filter(Boolean))];
  const output=tokens.map(t=>t.out).join("");
  return {status:"adapted", sourceIpa, normalizedIpa:ipa, output, candidates:[output], preservedFeatures, neutralizedFeatures:[...new Set(neutralizedFeatures)], rulesApplied, inputNotes, warnings:["Project-defined practical adaptation; not an official Ukrainian standard. Verify lexical reading and target-language convention independently."]};
}
