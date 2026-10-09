/**
 * IPA → Ukrainian practical adaptation.
 * Thai orthography is deliberately absent from this module.
 * IPA remains the source of truth; source contrasts may be neutralized only here.
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
export function adaptIpaToUkrainian(sourceIpa) {
  if (typeof sourceIpa !== "string" || !sourceIpa.trim()) {
    return {status:"withheld", sourceIpa:sourceIpa ?? null, output:null, candidates:[], preservedFeatures:[], neutralizedFeatures:[], rulesApplied:[], warnings:["IPA input is empty."]};
  }
  const ipa = sourceIpa.normalize("NFC");
  const tokens = [];
  for (let i=0;i<ipa.length;) {
    if (/[.\s]/u.test(ipa[i])) { tokens.push({text:ipa[i], out:ipa[i], rule:null}); i++; continue; }
    if (ipa[i] === "ː" || ipa[i] === "̯" || ipa[i] === "̩" || ipa[i] === "̚") {
      tokens.push({text:ipa[i], out:"", rule:"UA-DIACRITIC-NEUTRALIZATION", neutralized:["phonetic detail not represented in Ukrainian practical spelling"]}); i++; continue;
    }
    const key = ORDER.find(k => ipa.startsWith(k,i));
    if (!key) return {status:"withheld", sourceIpa, normalizedIpa:ipa, output:null, candidates:[], preservedFeatures:[], neutralizedFeatures:[], rulesApplied:[], warnings:["Невідомий або непідтримуваний IPA-символ: "+[...ipa.slice(i)][0]+". Український результат не вгадується."]};
    const rule=SEGMENTS.get(key);
    tokens.push({text:key,...rule});
    i += key.length;
  }
  const preservedFeatures=[...new Set(tokens.flatMap(t=>t.preserved||[]))];
  const neutralizedFeatures=[...new Set(tokens.flatMap(t=>t.neutralized||[]))];
  const rulesApplied=[...new Set(tokens.map(t=>t.rule).filter(Boolean))];
  return {status:"adapted", sourceIpa, normalizedIpa:ipa, output:tokens.map(t=>t.out).join(""), candidates:[tokens.map(t=>t.out).join("")], preservedFeatures, neutralizedFeatures, rulesApplied, warnings:[]};
}
