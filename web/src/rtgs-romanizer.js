import { createFastThaiG2PNativeTokenizer } from "./fastthaig2p-tokenizer.js";
import { romanizeRtgsTokenSequence } from "./rtgs-reference.js";
export class RtgsRomanizerError extends Error {
  constructor(code,message){super(message);this.name="RtgsRomanizerError";this.code=code;}
}
export async function createRtgsRomanizer({baseUrl=new URL("../vendor/native/",import.meta.url),fetchImpl=fetch,cryptoImpl=globalThis.crypto}={}){
  const mr=await fetchImpl(new URL("manifest.json",baseUrl),{credentials:"same-origin",cache:"force-cache"});
  if(!mr.ok)throw new RtgsRomanizerError("manifest_unavailable","Не вдалося завантажити локальний маніфест словника.");
  const m=await mr.json();
  if(m?.schema_version!==1||m?.pythainlp_version!=="5.4.0"||m?.pythainlp_wordlist_license!=="CC0-1.0"||!Number.isInteger(m?.pythainlp_wordlist_entries)||!Array.isArray(m?.assets))throw new RtgsRomanizerError("manifest_invalid","Маніфест словника не відповідає закріпленій версії та ліцензії.");
  const a=m.assets.find(x=>x.path==="native/pythainlp-default-words.txt");
  if(!a||!/^[a-f0-9]{64}$/u.test(a.sha256)||!Number.isInteger(a.size_bytes))throw new RtgsRomanizerError("asset_unlisted","У маніфесті немає перевіреного запису для словника сегментації.");
  if(!cryptoImpl?.subtle?.digest)throw new RtgsRomanizerError("integrity_unavailable","Браузер не підтримує SHA-256.");
  const r=await fetchImpl(new URL("pythainlp-default-words.txt",baseUrl),{credentials:"same-origin",cache:"force-cache"});
  if(!r.ok)throw new RtgsRomanizerError("wordlist_unavailable","Не вдалося завантажити локальний тайський словник.");
  const bytes=await r.arrayBuffer();
  if(bytes.byteLength!==a.size_bytes)throw new RtgsRomanizerError("wordlist_size_mismatch","Розмір словника не збігається з маніфестом.");
  const digest=await cryptoImpl.subtle.digest("SHA-256",bytes);
  const hash=[...new Uint8Array(digest)].map(v=>v.toString(16).padStart(2,"0")).join("");
  if(hash!==a.sha256)throw new RtgsRomanizerError("wordlist_hash_mismatch","SHA-256 словника не збігається; обробку зупинено.");
  const words=new TextDecoder().decode(bytes).split(/\r?\n/u).filter(Boolean);
  if(words.length!==m.pythainlp_wordlist_entries)throw new RtgsRomanizerError("wordlist_count_mismatch","Кількість слів не збігається з маніфестом.");
  const tokenizer=createFastThaiG2PNativeTokenizer(words);
  return Object.freeze({engine:"PyThaiNLP 5.4.0 royin / RTGS",segmentation:"PyThaiNLP 5.4.0 newmm",dictionaryEntries:words.length,
    romanize(text){const input=String(text??"");const tokens=tokenizer.tokenize(input).map(value=>({input:value,kind:/[\u0E00-\u0E7F]/u.test(value)?"thai":"other"}));const details=romanizeRtgsTokenSequence(tokens);return {input,output:details.map(x=>x.value).join(""),details,unavailableCount:details.filter(x=>x.status==="unavailable").length,engine:"PyThaiNLP 5.4.0 royin / RTGS",segmentation:"PyThaiNLP 5.4.0 newmm"};}
  });
}
