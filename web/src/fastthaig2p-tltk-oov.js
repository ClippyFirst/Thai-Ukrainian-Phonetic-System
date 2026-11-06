/**
 * Browser-native port of FastThaiG2P's pinned TLTK 1.3.8 OOV path.
 * Source: awslabs/fastthaig2p _th2ipa.py @ 4e82a291b4cf2876326744c6580121e9986ad354.
 * Data: extracted from TLTK 1.9.1 BSD-3-Clause package assets; JSON only.
 */
import { NativeFastThaiG2PError } from "./fastthaig2p-native.js";

const TONES = {"0":"˧","1":"˨˩","2":"˥˩","3":"˦˥","4":"˩˩˦"};
const CONSONANTS = [["kh","kʰ"],["ph","pʰ"],["th","tʰ"],["ch","t͡ɕʰ"],["c","t͡ɕ"],["N","ŋ"],["?","ʔ"]];
const VOWELS = [["UUa","ɯa̯"],["Ua","ɯa̯"],["iia","ia̯"],["ia","ia̯"],["uua","ua̯"],["ua","ua̯"],["aa","aː"],["ii","iː"],["uu","uː"],["xx","ɛː"],["ee","eː"],["oo","oː"],["OO","ɔː"],["@@","ɤː"],["UU","ɯː"],["a","a"],["i","i"],["u","u"],["x","ɛ"],["e","e"],["o","o"],["O","ɔ"],["@","ɤ"],["U","ɯ"]];
const ALIASES = {A:"X",K:"X",C:"X",R:"X",G:"X",E:"X",D:"Y",Z:"Y",H:"Y",F:"Y"};
const TOKENS = {
 X:"([ก-ฮ])", C:"([กขคจดตทบปผพฟสศซ])", Y:"([ก-ฬฮ])", R:"([รลว])",
 K:"([ก-ฮ])", A:"([กจฆดตบปอขฉฐถผฝศษสหคชพภทธมยรลวนณซญฑฏฌ])",
 Z:"([กงดนมบรลฎฏจตณถพศทสชคภปญ])", D:"([กงดนมบวยต])", W:"[ก-ฮ]"
};
const SPECIAL = new Set([".", "*", "+", "?", "^", "$", "{", "}", "(", ")", "|", "[", "]", "\\"]);
const escapeRegex = value => [...value].map(ch => SPECIAL.has(ch) ? "\\" + ch : ch).join("");
const length = value => Array.from(value).length;
const tuple = (...values) => JSON.stringify(values);
const get = (map,key) => map.get(key) ?? 0;
const replaceAllLiteral = (value, from, to) => value.split(from).join(to);

function compilePattern(record) {
 let pattern=record.pattern;
 for(const [token,replacement] of Object.entries(TOKENS)) pattern=pattern.replaceAll(token,replacement);
 pattern=pattern.replaceAll(".","[.]").replaceAll("T",record.tone_flag==="T"?"[่้๊๋]":"[่้๊๋]*");
 try{return new RegExp("^(?:"+pattern+")","u");}
 catch(error){throw new NativeFastThaiG2PError("native_oov_pattern_invalid","TLTK OOV pattern is invalid: "+String(error?.message||error));}
}
function addPron(map,form,phone){const values=map.get(form)||[];values.push(phone);map.set(form,values);}
function deadSyllable(phone){
 const value=phone.replaceAll("ch","C").replace(/[0-4]/gu,"");
 if(/[mnwjlN]8?$/u.test(value))return "L";
 if(/[pktfscC]8?$/u.test(value))return "D";
 return /([aeiouxOU@])\1/u.test(value)?"L":"D";
}
function replaceSound(phone,code,charmatch,stable){
 let output=phone;const chars=charmatch.split(" ");
 for(let i=0;i<length(code);i++){
  const symbol=Array.from(code)[i], base=ALIASES[symbol]||symbol, sound=stable[base]?.[chars[i]];
  if(typeof sound!=="string")throw new NativeFastThaiG2PError("native_oov_stable_missing","TLTK stable consonant mapping is missing.");
  output=replaceAllLiteral(output,symbol,sound);
 }
 return output+"8";
}
function toneAssign(form,phone,code,charmatch){
 if(!phone)return [phone,"9"];
 let lead="",init="",final="";
 if(/[0-4]8/u.test(phone))return [phone.replace(/([0-4])8/gu,"$1"),""];
 if(code.includes("X")||code==="GH"||code==="EF"){const c=charmatch.split(" ");init=c[0]||"";final=c[1]||"";}
 else if(/AK|CR/u.test(code)){const c=charmatch.split(" ");lead=c[0]||"";if(c.length>2){init=c[1];final=c[2];}else init=c[1]||"";}
 const dead=deadSyllable(phone), has=m=>form.includes(m);
 if(phone.includes("+'"))phone=phone.replaceAll("+",("ผฝถขสหฉศษ".includes(lead)||"กจดตบปอ".includes(lead))?"1":"3");
 if("กจดตฎฏบปอ".includes(init))return [phone,dead==="L"?(has("่")?"1":has("้")?"2":has("๊")?"3":has("๋")?"4":"0"):(has("่")?"9":has("้")?"2":has("๊")?"3":has("๋")?"4":"1")];
 if("ขฃฉฐถผฝสศษห".includes(init))return [phone,dead==="L"?(has("่")?"1":has("้")?"2":has("๊")||has("๋")?"9":"4"):(has("่")?"9":has("้")?"2":has("๊")||has("๋")?"9":"1")];
 if("งญณนมยรลวฬ".includes(init)&&lead&&"ขฃฉฐถผฝสศษห".includes(lead))return [phone,dead==="L"?(has("่")?"1":has("้")?"2":"4"):(has("่")?"9":has("้")?"2":"1")];
 if("งญณนมยรลวฬ".includes(init)&&lead&&"กจดตฎฏบปอ".includes(lead))return [phone,dead==="L"?(has("่")?"1":has("้")?"2":has("๊")?"3":has("๋")?"4":"0"):(has("่")?"9":has("้")?"2":has("๊")?"3":has("๋")?"4":"1")];
 if("คฅฆชฌซฑฒทธพภฟฮงญณนมยรลวฬฤฦ".includes(init)){
  if(dead==="L")return [phone,has("่")?"2":has("้")?"3":has("๊")||has("๋")?"9":"0"];
  if(/[aeiouxOU@][aeiouxOU@]+/u.test(phone))return [phone,has("่")?"9":has("้")?"3":has("๊")?"9":has("๋")?"4":"2"];
  return [phone,has("่")?"2":has("้")?"9":has("๊")?"9":has("๋")?"4":"3"];
 }
 return [phone,"9"];
}
function transformSyllable(form,phone){
 if(/xx[nmN][12]/u.test(phone))phone=phone.replace("xx","x");
 else if(/ee[nmN][12]/u.test(phone))phone=phone.replace("ee","e");
 else if(/@@[nmN][12]/u.test(phone))phone=phone.replace("@@","@");
 if(/^(อย่า|อยู่|อย่าง|อยาก)$/u.test(form)&&phone.includes("'"))phone=phone.split("'").at(-1);
 else if(form.includes("ห")&&phone.includes("ha1")&&!/หนุ$|หก|หท|หพ|หฤ|หโ/u.test(form))phone=phone.split("'").at(-1);
 else if(/[จซศส]ร/u.test(form)&&/[cs]r/u.test(phone)&&/[^']/u.test(phone))phone=phone.replaceAll("r","");
 return [form,phone];
}
function allowedPronunciation(code,charmatch,form,phone,allowed){
 if(form.includes("."))return true;
 if(code.includes("CR")&&/^(?:ผ ร|ด ล|ต ล|ท ล|ด ว|ต ว|ท ว|บ ว|ป ว|พ ว|ฟ ว|ผ ว|ส ล|ส ว|ร ร|ศ ล|ศ ว)/u.test(charmatch))return false;
 if(code.includes("AK")){const c=charmatch.split(" ");if(!(allowed[c[0]]||"").includes(c[1]||""))return false;}
 if(/\u0E31[่้๊๋]?ว/u.test(form)&&phone.includes("aw"))return false;
 if(/[ก-ฮ] ข/u.test(charmatch)&&!/[ุัเ]/u.test(form))return false;
 if(/[ก-ฮ] ร$/u.test(charmatch)&&/.an/u.test(phone))return false;
 return true;
}
function mergeKaran(forms,pron){
 const out=[];let pending=null;const mergedSeen=new Set();
 for(const form of [...forms].reverse()){
  if(/(.+)[ิุ]์/u.test(form)||(/(.+)์/u.test(form)&&length(form)<4)){pending=form;continue;}
  if(pending!==null){for(const phone of pron.get(form)||[]){const key=tuple(form+pending,phone);if(!mergedSeen.has(key)){addPron(pron,form+pending,phone);mergedSeen.add(key);}}out.push(form+pending);pending=null;}
  else out.push(form);
 }
 return out.reverse();
}
function makeSyllableStats(records){
 const tri=new Map(),bi=new Map(),biType=new Map(),counts=new Map(),types=new Map();let totalWord=0,totalLex=0;
 for(const [a,b,c,n] of records){tri.set(tuple(a,b,c),n);const k=tuple(a,b);bi.set(k,get(bi,k)+n);biType.set(k,get(biType,k)+1);counts.set(b,get(counts,b)+n);}
 for(const key of bi.keys()){const [first]=JSON.parse(key);types.set(first,get(types,first)+1);}
 for(const n of counts.values()){totalLex++;totalWord+=n;}
 const score=forms=>{let p1="|",p2="|",sum=0;for(const word of forms){const t=get(tri,tuple(p2,p1,word)),b=get(bi,tuple(p2,p1)),bt=get(biType,tuple(p2,p1)),b2=get(bi,tuple(p1,word)),c=get(counts,p1),ty=get(types,p1),cw=get(counts,word);const p=0.8*(t>0?t/(b+bt):0)+0.15*(b2>0?b2/(c+ty):0)+0.04*(cw>0?cw/(totalWord+totalLex):0)+1/((totalWord+totalLex)**2);sum+=Math.log(p);p2=p1;p1=word;}return sum;};
 const collocation=(a,b)=>{const k=tuple(a,b);let n=get(bi,k),ca=get(counts,a),cb=get(counts,b);if(n<1||ca<1||cb<1){bi.set(k,n+1);counts.set(a,ca+1);counts.set(b,cb+1);totalWord+=2;n=get(bi,k);ca=get(counts,a);cb=get(counts,b);}return Math.abs(Math.log2((n*totalWord)/(ca*cb)));};
 return {score,collocation};
}
function makePhoneScorer(records){
 const tri=new Map(),triF=new Map(),bi=new Map(),biF=new Map(),uni=new Map(),uniF=new Map(),abs=new Map(),absF=new Map();
 const add=(m,k,n)=>m.set(k,get(m,k)+n);
 for(const [a,b,c,p,n] of records){
  add(tri,tuple(a,b,c,p),n);add(triF,tuple(a,b,c),n);add(bi,tuple(a,b,p),n);add(biF,tuple(a,b),n);
  add(bi,tuple(b,c,p),n);add(biF,tuple(b,c),n);add(uni,tuple(b,p),n);add(uniF,b,n);
  const af=b.replace(/[่้๊๋]/gu,"").replace(/[ก-ฮ]/gu,"C"),ap=p.replace(/[0-9]/gu,"").replace(/[^aeio@OuxU]/gu,"C");
  add(abs,tuple(af,ap),n);add(absF,af,n);
 }
 return (p,pw,w,nw)=>{let p3=0,p2=0,p1=0,p0=0,c=get(tri,tuple(pw,w,nw,p));if(c>0)p3=(1+Math.log(c))/(1+Math.log(get(triF,tuple(pw,w,nw))));
 c=get(bi,tuple(pw,w,p));if(c>0)p2+=(1+Math.log(c))/(1+Math.log(get(biF,tuple(pw,w))))*0.25;
 c=get(bi,tuple(w,nw,p));if(c>0)p2+=(1+Math.log(c))/(1+Math.log(get(biF,tuple(w,nw))))*0.75;
 c=get(uni,tuple(w,p));if(c>0)p1=(1+Math.log(c))/(1+Math.log(get(uniF,w)));
 const af=w.replace(/[่้๊๋]/gu,"").replace(/[ก-ฮ]/gu,"C"),ap=p.replace(/[0-9]/gu,"").replace(/[^aeio@OuxU]/gu,"C");c=get(abs,tuple(af,ap));if(c>0)p0=(1+Math.log(c))/(1+Math.log(get(absF,af)));
 return 0.8*p3+0.16*p2+0.03*p1+0.00001*p0+1e-11;};
}
function phonesToIpa(raw){
 const output=[];
 for(const part of raw.split(/[|~^]/u))for(const piece of part.split("'")){
  let s=piece.trim();if(!s)continue;
  const tone=/[0-4]$/u.test(s)?s.at(-1):"0";if(/[0-4]$/u.test(s))s=s.slice(0,-1);
  for(const [from,to] of CONSONANTS)s=replaceAllLiteral(s,from,to);
  for(const [from,to] of VOWELS)s=replaceAllLiteral(s,from,to);
  if(s&&"ktp".includes(s.at(-1))&&/[aeiouɔɛɯɤː̯]/u.test(s.slice(0,-1)))s=s.slice(0,-1)+s.at(-1)+"̚";
  output.push(s+TONES[tone]);
 }
 return output.length?"/"+output.join(".")+"/":null;
}

export function createTltkOovFallback(data){
 if(data?.schema_version!==1||data?.tltk_package_license!=="BSD-3-Clause"||
 !Array.isArray(data.syllable_patterns)||!Array.isArray(data.syllable_dictionary)||
 !Array.isArray(data.phone_trigrams)||!Array.isArray(data.syllable_trigrams)||
 !Array.isArray(data.word_dictionary)||!data.parser_constants?.stable_base||!data.parser_constants?.allowed_clusters)
  throw new TypeError("Pinned TLTK OOV data schema is incomplete");
 const constants=data.parser_constants;
 const stable={...constants.stable_base,...Object.fromEntries(Object.entries(constants.stable_aliases).map(([key,base])=>[key,constants.stable_base[base]]))};
 const basePron=new Map();for(const [form,phone] of data.syllable_dictionary)addPron(basePron,form,phone);
 const patterns=data.syllable_patterns.map(record=>({...record,expression:compilePattern(record)}));
 const sylStats=makeSyllableStats(data.syllable_trigrams),phoneScore=makePhoneScorer(data.phone_trigrams),dictionary=new Set(data.word_dictionary);
 function parseSyllables(input, pron){
  const chars=Array.from(input),n=chars.length,chart=new Map();
  const set=(i,j,forms)=>{if(!chart.has(i))chart.set(i,new Map());chart.get(i).set(j,forms);};
  for(const {pronunciation,expression} of patterns)for(let i=0;i<n;i++){
   const match=expression.exec(chars.slice(i).join(""));if(!match)continue;
   const form=match[0];
   const groupCount=match.length-1;
   const groups=groupCount>=3?match.slice(1,4):groupCount===2?match.slice(1,3):groupCount===1?match.slice(1,2):[];
   const end=i+length(form);set(i,end,[form]);
   if(!groups.length){addPron(pron,form,pronunciation);continue;}
   if(groups.some(value=>value===undefined))continue;
   const charmatch=groups.join(" ");
   const code=pronunciation.replace(/[^AKYDZCRX]/gu,"");if(!code)continue;
   let phone;
   try { phone=replaceSound(pronunciation,code,charmatch,stable); }
   catch(error) { if(error?.code==="native_oov_stable_missing")continue; throw error; }
   if(allowedPronunciation(code,charmatch,form,phone,constants.allowed_clusters)){
    const [assigned,tone]=toneAssign(form,phone,code,charmatch);phone=assigned;
    if(tone<"5")phone=phone.replaceAll("8",tone);
    [,phone]=transformSyllable(form,phone);
   }
   addPron(pron,form,phone);
   if(/^ทร/u.test(form)&&/^thr/u.test(phone))addPron(pron,form,phone.replace("thr","s"));
  }
  for(let j=0;j<n;j++){
   const fromZero=chart.get(0),atJ=chart.get(j);if(!fromZero?.has(j)||!atJ)continue;
   for(const [end,forms] of [...atJ.entries()]){
    const merged=mergeKaran([...fromZero.get(j),...forms],pron);
    if(!fromZero.has(end)||sylStats.score(merged)>sylStats.score(fromZero.get(end)))set(0,end,merged);
   }
  }
  return chart.get(0)?.get(n)||null;
 }
 function parseWords(syllables){
  const n=syllables.length,edges=new Map(),scores=new Map();
  const set=(i,j,forms,score)=>{if(!edges.has(i))edges.set(i,new Map());edges.get(i).set(j,forms);scores.set(tuple(i,j),score);};
  for(let i=0;i<n;i++)set(i,i+1,[syllables[i]],0);
  for(let i=0;i<n;i++)for(let j=i+1;j<=n;j++){
   const word=syllables.slice(i,j).join("");if(!dictionary.has(word))continue;
   let score=0;for(let k=i;k<j-1;k++)score+=sylStats.collocation(syllables[k],syllables[k+1]);
   set(i,j,[syllables.slice(i,j).join("~")],score);
  }
  const best=new Array(n+1).fill(null);best[0]={score:0,words:[]};
  for(let i=0;i<n;i++){if(!best[i])continue;for(const [end,forms] of edges.get(i)||[]){
   const candidate={score:best[i].score+get(scores,tuple(i,end)),words:[...best[i].words,...forms]};
   if(!best[end]||candidate.score>best[end].score)best[end]=candidate;
  }}
  return best[n]?.words||null;
 }
 function selectPhones(forms, pron){
  const padded=["|",...forms,"|"];
  return forms.map((form,i)=>{const candidates=pron.get(form)||[];if(candidates.length===1)return candidates[0];
   let chosen="",best=0;for(const phone of candidates){const score=phoneScore(phone,padded[i],form,padded[i+2]);
    if(score>best||(score===best&&phone.includes("'")&&length(phone)>length(chosen))){chosen=phone;best=score;}}
   return chosen;
  });
 }
 function convert(word){
  if(typeof word!=="string"||!word)return null;
  if(/^[^ก-์]+/u.test(word))return null;
  const pron=new Map([...basePron.entries()].map(([form,phones])=>[form,[...phones]]));
  const normalized=word.replaceAll("เเ","แ").replaceAll("ํา","ำ").replaceAll("ฤา","ฤๅ").replaceAll("ฦา","ฦๅ");
  const syllables=parseSyllables(normalized,pron);if(!syllables)return null;
  const words=parseWords(syllables);if(!words)return null;
  const raw=words.map(w=>selectPhones(w.split("~"),pron).join("~")).join("|");
  return phonesToIpa(raw);
 }
 return Object.freeze({sourceCommit:data.fastthaig2p_commit,tltkCommit:data.tltk_source_commit,packageVersion:data.tltk_package_version,convert});
}

export async function loadTltkOovData({
 baseUrl=new URL("../vendor/native-oov/",import.meta.url),fetchImpl=fetch,
 cryptoImpl=globalThis.crypto,DecompressionStreamImpl=globalThis.DecompressionStream
}={}){
 const mr=await fetchImpl(new URL("manifest.json",baseUrl),{credentials:"same-origin",cache:"force-cache"});
 if(!mr.ok)throw new NativeFastThaiG2PError("native_oov_unavailable","Не вдалося завантажити TLTK OOV-дані.");
 const manifest=await mr.json();
 if(manifest?.schema_version!==1||manifest?.license!=="BSD-3-Clause"||manifest?.tltk_package_version!=="1.9.1"||
 manifest?.fastthaig2p_commit!=="4e82a291b4cf2876326744c6580121e9986ad354"||
 manifest?.path!=="tltk-oov-data.json.gz"||!/^[a-f0-9]{64}$/u.test(manifest?.compressed_sha256||"")||
 !/^[a-f0-9]{64}$/u.test(manifest?.uncompressed_sha256||""))
  throw new NativeFastThaiG2PError("native_oov_manifest_invalid","Маніфест TLTK OOV не відповідає закріпленій версії.");
 if(!cryptoImpl?.subtle?.digest||typeof DecompressionStreamImpl!=="function")
  throw new NativeFastThaiG2PError("native_oov_integrity_unavailable","Браузер не підтримує перевірку цілісності або gzip-декомпресію TLTK OOV.");
 const response=await fetchImpl(new URL(manifest.path,baseUrl),{credentials:"same-origin",cache:"force-cache"});
 if(!response.ok)throw new NativeFastThaiG2PError("native_oov_asset_unavailable","Не вдалося завантажити TLTK OOV-дані.");
 const compressed=await response.arrayBuffer();
 const hash=async bytes=>{const d=await cryptoImpl.subtle.digest("SHA-256",bytes);return [...new Uint8Array(d)].map(x=>x.toString(16).padStart(2,"0")).join("");};
 if(compressed.byteLength!==manifest.compressed_size_bytes||await hash(compressed)!==manifest.compressed_sha256)
  throw new NativeFastThaiG2PError("native_oov_asset_corrupt","Стиснений TLTK OOV-пакет не пройшов SHA-256.");
 const stream=new Blob([compressed]).stream().pipeThrough(new DecompressionStreamImpl("gzip"));
 const payload=await new Response(stream).arrayBuffer();
 if(payload.byteLength!==manifest.uncompressed_size_bytes||await hash(payload)!==manifest.uncompressed_sha256)
  throw new NativeFastThaiG2PError("native_oov_asset_corrupt","Розпакований TLTK OOV-пакет не пройшов SHA-256.");
 let data;try{data=JSON.parse(new TextDecoder().decode(payload));}catch{throw new NativeFastThaiG2PError("native_oov_asset_invalid","JSON TLTK OOV-пакета пошкоджений.");}
 if(data?.schema_version!==1||data?.tltk_package_license!=="BSD-3-Clause"||data?.fastthaig2p_commit!==manifest.fastthaig2p_commit||data?.tltk_source_commit!==manifest.tltk_source_commit)
  throw new NativeFastThaiG2PError("native_oov_asset_invalid","Версія TLTK OOV-даних не збігається з маніфестом.");
 return data;
}
