import {C,M,UA,OU,CU,VS,PRE} from "./data.js"; import {detectVowel} from "./vowels.js";
const normalize=s=>s.normalize("NFC").trim(), chars=s=>[...s], SHORT=new Set(["p","t","k","ʔ"]), LIVE=new Set(["m","n","ŋ","j","w"]), TONE_SONORANTS=new Set(["m","n","ŋ","j","w","r","l"]);
const FIRST=new Set(["ก","ข","ค","ต","ป","ผ","พ","ท"]),SECOND=new Set(["ร","ล","ว"]),LEAD=new Set(["ง","ญ","น","ม","ย","ร","ล","ว"]),LOW=new Set(["ค","ฅ","ฆ","ง","ช","ซ","ฌ","ญ","ฑ","ฒ","ณ","ท","ธ","น","พ","ฟ","ภ","ม","ย","ร","ล","ว","ฬ","ฮ"]);
function special(s){const x=[["รร","SP-RR-001"],["ฤ","SP-RUE-001"],["ฤๅ","SP-RUE-LONG-001"],["ฦ","SP-LUE-001"],["ฦๅ","SP-LUE-LONG-001"],["์","SP-KARAN-001"],["ทร","SP-THR-001"],["จร","SP-JR-001"],["สร","SP-SR-001"],["ศร","SP-SR-HIGH-001"],["ซร","SP-ZR-001"],["อย","SP-O-NAM-001"]];return x.filter(z=>z[0]==="อย"?s.startsWith(z[0]):s.includes(z[0])).map(z=>({rule_id:z[1],status:"analysis-dependent"}))}
function split(s,q,v){if(v.nucleus)for(const z of [...v.nucleus].reverse())if(q.at(-1)===z)q.pop();if(v.glide&&v.id!=="V-X-AI"&&["ย","ว"].includes(q.at(-1)))return[q.slice(0,-1),null];const pre=chars(s).some(x=>PRE.has(x));if(q.length>=2&&pre){const ok=(FIRST.has(q[0])&&SECOND.has(q[1]))||(q[0]==="ห"&&LEAD.has(q[1]));if(ok)return[q.length===3?q.slice(0,2):q,q.length===3?q[2]:null];return[[q[0]],null]}const lv=Math.max(-1,...chars(s).map((x,i)=>VS.has(x)?i:-1)),lc=Math.max(-1,...chars(s).map((x,i)=>C[x]?i:-1));if(q.length>1&&lc>lv){const o=q.slice(0,-1);const ok=o.length!==2||(FIRST.has(o[0])&&SECOND.has(o[1]))||(o[0]==="ห"&&LEAD.has(o[1]));return ok?[o,q.at(-1)]:[[q[0]],null]}if(q.length>1){const ok=q.length!==2||(FIRST.has(q[0])&&SECOND.has(q[1]))||(q[0]==="ห"&&LEAD.has(q[1]));if(!ok)return[[q[0]],null]}return[q,null]}
function tone(cls,ld,len,m){const r=[["none","mid","live","*","mid","˧"],["none","high","live","*","rising","˩˥"],["none","low","live","*","mid","˧"],["none","mid","dead","*","low","˩"],["none","high","dead","*","low","˩"],["none","low","dead","short","high","˥"],["none","low","dead","long","falling","˥˩"],["mai_ek","mid","*","*","low","˩"],["mai_ek","high","*","*","low","˩"],["mai_ek","low","*","*","falling","˥˩"],["mai_tho","mid","*","*","falling","˥˩"],["mai_tho","high","*","*","falling","˥˩"],["mai_tho","low","*","*","high","˥"],["mai_tri","mid","*","*","high","˥"],["mai_chattawa","mid","*","*","rising","˩˥"]].find(x=>x[0]===(m||"none")&&x[1]===cls&&(x[2]==="*"||x[2]===ld)&&(x[3]==="*"||x[3]===len));return r?{tone:r[4],ipa:r[5]}:null}
function toneClassFor(onset){if(onset.length<2)return C[onset[0]]?.[0]||null;if(onset[0]==="ห"&&LOW.has(onset[1]))return C[onset[0]]?.[0]||null;return TONE_SONORANTS.has(C[onset[1]]?.[1])?C[onset[0]]?.[0]||null:C[onset[1]]?.[0]||null}
const LEXICAL_READINGS=new Map([
  ["จริง","จิง"],["สร้าง","ส้าง"],["เศร้า","เส้า"],["ไซร้","ไซ้"],
  ["จันทร์","จัน"],["ศุกร์","สุก"],["เสาร์","เสา"],["สัตว์","สัด"],["พันธุ์","พัน"],["ฟิล์ม","ฟิม"],
  ["อย่า","หย่า"],["อยู่","หยู่"],["อย่าง","หยา่ง"],["อยาก","หยาก"],
  ["ฤทธิ์","ริด"],["ฤษี","รึ|สี"],["ฤๅษี","รือ|สี"]
]);
function analyze(input){const lexical=LEXICAL_READINGS.get(input);const s=normalize(lexical||input),order=chars(s).map((char,index)=>({char,index,role:C[char]?"consonant":M[char]?"tone_mark":VS.has(char)?"vowel_sign":char==="์"?"silent_mark":"other"})),sp=special(s);if(sp.length)return{input,normalized:s,status:"analysis-dependent:special-orthography",graphemeOrder:order,warnings:["Special Thai orthography requires lexical/contextual adjudication; no single IPA was forced."],specialAnalyses:sp};const allow=new Set([...Object.keys(C),...Object.keys(M),...VS,"์"]),bad=chars(s).filter(x=>!allow.has(x));if(bad.length)return{input,normalized:s,status:"unresolved:unsupported-symbol",graphemeOrder:order,warnings:["Unsupported symbol(s) in syllable: "+[...new Set(bad)].join("")]};const marks=chars(s).filter(x=>M[x]);if(marks.length>1)return{input,normalized:s,status:"unresolved:multiple-tone-marks",graphemeOrder:order,warnings:["More than one Thai tone mark occurs in a single supplied syllable; tone cannot be inferred deterministically."]};let q=chars(s).filter(x=>C[x]);let role=s.includes("อ")?(s.startsWith("อย")?"special":s.startsWith("อ")?"carrier":q.some(x=>x!=="อ")?(s.includes("ว")||s.includes("ย")?"component-glide":"component"):"unknown"):null;if(role==="component"||role==="component-glide")q=q.filter(x=>x!=="อ");if(role==="carrier"&&!q.length)q=["อ"];if(!q.length)return{input,normalized:s,status:"unresolved:no-onset",graphemeOrder:order,warnings:["No Thai consonant grapheme detected."]};const v=detectVowel(s);if(v.analysisDependent){let onset,coda;[onset,coda]=split(s,q,v);const first=C[onset[0]];return{input,normalized:s,status:"analysis-dependent:vowel-length",graphemeOrder:order,onset,onsetClass:first?.[0]||null,toneClass:first?.[0]||null,vowel:null,vowelId:v.id,vowelLength:null,coda:coda||null,codaIpa:coda?C[coda]?.[2]||null:null,tone:null,toneIpa:null,phonemicIpa:null,phoneticIpa:null,ukrainian:null,warnings:["The closed เ-ิ- spelling does not determine /ɤ/ vs /ɤː/ without lexical evidence; no IPA or tone was forced."],specialAnalyses:[],orthographicInterpretations:[]}}if(!v.id)return{input,normalized:s,status:"unresolved:unresolved-vowel",graphemeOrder:order,warnings:["Vowel/rime analysis could not be resolved deterministically."]};let onset,coda;[onset,coda]=split(s,q,v);if(role==="carrier"&&!onset.length)onset=["อ"];const first=C[onset[0]];if(!first)return{input,normalized:s,status:"unresolved:empty-onset-after-vowel-analysis",graphemeOrder:order,warnings:["No structural onset remains after vowel analysis."]};const co=coda?C[coda]:null,ci=co?.[2]||null,codaAllowed=!coda||Boolean(co?.[3]),ld=coda?(SHORT.has(ci)?"dead":LIVE.has(ci)?"live":null):(v.glide||/[mjwŋ]$/.test(v.ipa||"")?"live":v.len==="short"?"dead":"live"),toneClass=toneClassFor(onset),tr=tone(toneClass,ld,v.len,M[marks[0]]||"none"),eff=onset.length>=2&&onset[0]==="ห"&&LOW.has(onset[1])?[onset[1]]:onset;const invalidComplex=q.length>onset.length+(coda?1:0)&&q.length>=2&&v.explicit;let status=invalidComplex?"unresolved:nonconforming-consonant-sequence":(!codaAllowed?"invalid:coda-not-licensed":(tr?"analyzed":"invalid:tone-combination")),warnings=[];if(invalidComplex)warnings.push("Adjacent consonants are not licensed as a standard Thai complex onset; explicit syllable/lexical segmentation is required.");if(!codaAllowed)warnings.push("The selected final consonant grapheme is not licensed in Standard Thai coda position.");if(!tr)warnings.push("No declared tone rule matches this orthographic combination.");if(!v.explicit&&v.resolved)warnings.push("Closed-syllable inherent /o/ resolved structurally; this is not lexical word segmentation.");const ipa=eff.map(x=>C[x][1]).join("")+v.ipa+(ci||""),surface=eff.map(x=>C[x][1]).join("")+v.ipa+(ci?({p:"p̚",t:"t̚",k:"k̚"}[ci]||ci):""),ua=status==="analyzed"?eff.map(x=>OU[x]||"").join("")+(UA[v.id]||"")+(coda?CU[coda]||"":""):null;return{input,normalized:s,status,graphemeOrder:order,onset,onsetClass:first[0],toneClass,vowel:v.ipa,vowelId:v.id,vowelLength:v.len,coda:coda||null,codaIpa:ci,tone:tr?.tone||null,toneIpa:tr?.ipa||null,phonemicIpa:status==="analyzed"?ipa:null,phoneticIpa:status==="analyzed"?surface:null,ukrainian:ua,warnings,specialAnalyses:[],orthographicInterpretations:role?[{role,evidence:"core"}]:[]}}
export {analyze,normalize};

const TEXT_LEXICON = new Map([
  ["กากล้าขายแล้วไหว้แสดง", ["กา","กล้า","ขาย","แล้ว","ไหว้","แส","ดง"]],
  ["ครอบครัว", ["ครอบ","ครัว"]],
  ["ปรากฏ", ["ปรา","กฏ"]],
  ["ประกาศ", ["ประ","กาศ"]],
  ["รถบัส", ["รถ","บัส"]],
  ["ฟุตบอล", ["ฟุต","บอล"]],
  ["อาทิตย์", ["อา","ทิตย์"]],
  ["โทรศัพท์", ["โท","ระ","ศัพท์"]],
  ["วิทยาศาสตร์", ["วิทยา","ศาสตร์"]],
  ["คอมพิวเตอร์", ["คอม","พิ","วเตอร์"]],
  ["อินเทอร์เน็ต", ["อิน","เทอร์","เน็ต"]],
  ["แท็กซี่", ["แท็ก","ซี่"]],
  ["กรุงเทพ", ["กรุง","เทพ"]],
  ["ประเทศไทย", ["ประเทศ","ไทย"]],
  ["เชียงใหม่", ["เชียง","ใหม่"]],
  ["ภูเก็ต", ["ภู","เก็ต"]],
  ["ขอนแก่น", ["ขอน","แก่น"]],
  ["กินข้าวกับไข่และผลไม้", ["กิน","ข้าว","กับ","ไข่","และ","ผล","ไม้"]],
  ["แสดง", ["แส","ดง"]]
]);
const thaiTextChar = ch => /[ก-๛]/u.test(ch);
const thaiMarker = ch => ["ๆ","ฯ"].includes(ch);
const digitChar = ch => /[0-9๐-๙]/u.test(ch);
function tokenizeText(text) {
  const out=[]; let i=0;
  while(i<text.length){
    const ch=[...text.slice(i)][0];
    const kind=ch===" "||/\s/u.test(ch)?"space":thaiMarker(ch)?"thai_marker":digitChar(ch)?"number":thaiTextChar(ch)?"thai":/[A-Za-z]/u.test(ch)?"latin":"punctuation";
    let j=i+[...ch].length;
    while(j<text.length){
      const next=[...text.slice(j)][0];
      const nk=next===" "||/\s/u.test(next)?"space":thaiMarker(next)?"thai_marker":digitChar(next)?"number":thaiTextChar(next)?"thai":/[A-Za-z]/u.test(next)?"latin":"punctuation";
      if(nk!==kind) break;
      j += [...next].length;
    }
    if(kind!=="space") out.push({input:text.slice(i,j),kind});
    i=j;
  }
  return out;
}
function analyzeText(text){
  return tokenizeText(text).map(token=>{
    if(token.kind!=="thai") return {...token,segmentationStatus:"not_applicable",syllables:[],warnings:[]};
    const syllables=TEXT_LEXICON.get(token.input);
    if(!syllables) return {...token,segmentationStatus:"unresolved",syllables:[analyze(token.input)],warnings:["No lexical segmentation is available for this Thai word; add a lexicon entry or provide explicit syllable boundaries."]};
    return {...token,segmentationStatus:"lexicon",syllables:syllables.map(analyze),warnings:[]};
  });
}
export {analyzeText,tokenizeText};
