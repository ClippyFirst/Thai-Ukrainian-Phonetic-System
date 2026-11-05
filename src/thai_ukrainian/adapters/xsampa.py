"""Strict X-SAMPA → IPA conversion for text-only phonetic annotations."""
from __future__ import annotations
import re
import unicodedata
from dataclasses import dataclass

class XSampaConversionError(ValueError):
    """Raised when a label contains notation not covered by the declared map."""

# General X-SAMPA subset; actual CCOST symbol coverage must be inspected.
XSAMPA_TO_IPA = {
    "p":"p","b":"b","t":"t","d":"d","k":"k","g":"ɡ","c":"c","J\\":"ɟ",
    "q":"q","G\\":"ɢ","?":"ʔ","m":"m","F":"ɱ","n":"n","J":"ɲ","N":"ŋ","N\\":"ɴ",
    "f":"f","v":"v","T":"θ","D":"ð","s":"s","z":"z","S":"ʃ","Z":"ʒ",
    "s\\":"ɕ","z\\":"ʑ","B":"β","C":"ç","j\\":"ʝ","x":"x","G":"ɣ","X":"χ",
    "R":"ʁ","X\\":"ħ","?\\":"ʕ","h":"h","h\\":"ɦ","v\\":"ʋ","r\\":"ɹ",
    "j":"j","M\\":"ɰ","l":"l","L":"ʎ","L\\":"ʟ","4":"ɾ","r":"r","R\\":"ʀ",
    "K":"ɬ","K\\":"ɮ","x\\":"ɧ","H":"ɥ","W":"ʍ","w":"w","5":"ɫ",
    "i":"i","y":"y","1":"ɨ","}":"ʉ","M":"ɯ","u":"u","I":"ɪ","Y":"ʏ","U":"ʊ",
    "e":"e","2":"ø","@\\":"ɘ","8":"ɵ","7":"ɤ","o":"o","@":"ə","E":"ɛ","9":"œ",
    "3":"ɜ","3\\":"ɞ","V":"ʌ","O":"ɔ","{":"æ","6":"ɐ","a":"a","&":"ɶ","A":"ɑ","Q":"ɒ",
    "B\\":"ʙ","O\\":"ʘ","!\\":"ǃ","=\\":"ǂ","|\\":"ǀ",
}
# Retroflex spellings use a backtick in X-SAMPA; construct those keys explicitly.
XSAMPA_TO_IPA.update({"s"+chr(96):"ʂ","z"+chr(96):"ʐ","n"+chr(96):"ɳ",
                      "t"+chr(96):"ʈ","d"+chr(96):"ɖ","r"+chr(96):"ɽ","l"+chr(96):"ɭ"})
DIACRITICS = {
    "_h":"ʰ","_n":"ⁿ","_}":"̚","_j":"ʲ","_w":"ʷ","_~":"̃","_^":"̯","_=":"̩",
    "_>":"ʼ","_d":"̪","_a":"̺","_m":"̻","_+":"̟","_-":"̠",'_"':"̈",
    "_r":"̝","_t":"̤","_k":"̰","_G":"ˠ","_?\\":"ˤ","_O":"̹","_c":"̜",
}
# CCOST paper maps five Thai toneme labels (_1.._5). BAS MAUS syntax is broader
# and permits numeric tone suffixes _1.._9; this adapter deliberately maps only
# the CCOST-published five and fails closed for the others.
_TONES={"1":"mid","2":"low","3":"falling","4":"high","5":"rising"}
_SYMBOLS=tuple(sorted(XSAMPA_TO_IPA,key=lambda x:(-len(x),x)))
_DIACRITICS=tuple(sorted(DIACRITICS,key=lambda x:(-len(x),x)))
_TONE_RE=re.compile(r"_(?P<tone>[1-5])")

@dataclass(frozen=True)
class XSampaSyllable:
    xsampa: str
    ipa: str
    tone_number: str | None
    tone_category: str | None

@dataclass(frozen=True)
class XSampaLabel:
    raw: str
    syllables: tuple[XSampaSyllable,...]
    notation: str="X-SAMPA"
    tone_scheme: str="CCOST paper mapping (_1.._5); generic MAUS syntax _1.._9"
    @property
    def ipa(self)->str:
        return ".".join(item.ipa for item in self.syllables)
    @property
    def tone_categories(self)->tuple[str|None,...]:
        return tuple(item.tone_category for item in self.syllables)

def _convert_segmental(value:str)->str:
    if not value: raise XSampaConversionError("empty segmental syllable")
    if not value.isascii(): raise XSampaConversionError(f"expected ASCII X-SAMPA, found {value!r}")
    output=[]; index=0; has_segment=False
    while index<len(value):
        if value[index].isspace(): index+=1; continue
        if value.startswith("::",index):
            if not has_segment: raise XSampaConversionError("length mark has no preceding segment")
            output.append("ːː"); index+=2; continue
        if value.startswith(":\\",index):
            if not has_segment: raise XSampaConversionError("half-length mark has no preceding segment")
            output.append("ˑ"); index+=2; continue
        if value[index]==":":
            if not has_segment: raise XSampaConversionError("length mark has no preceding segment")
            output.append("ː"); index+=1; continue
        if value[index] in {'"',"%"}:
            output.append("ˈ" if value[index]=='"' else "ˌ"); index+=1; has_segment=False; continue
        if value[index]=="'":
            if not has_segment: raise XSampaConversionError("palatalization mark has no preceding segment")
            output.append("ʲ"); index+=1; continue
        diacritic=next((token for token in _DIACRITICS if value.startswith(token,index)),None)
        if diacritic is not None:
            if not has_segment: raise XSampaConversionError(f"diacritic {diacritic!r} has no preceding segment")
            output.append(DIACRITICS[diacritic]); index+=len(diacritic); continue
        symbol=next((token for token in _SYMBOLS if value.startswith(token,index)),None)
        if symbol is None:
            raise XSampaConversionError(f"unsupported X-SAMPA sequence at offset {index}: {value[index:]!r}")
        output.append(XSAMPA_TO_IPA[symbol]); index+=len(symbol); has_segment=True
    return unicodedata.normalize("NFD","".join(output))

def convert_xsampa_label(label:str)->XSampaLabel:
    """Convert a CCOST label; numeric tone suffixes close the current syllable."""
    if not isinstance(label,str): raise TypeError("X-SAMPA label must be a string")
    if not label.strip(): raise XSampaConversionError("empty X-SAMPA label")
    syllables=[]; current=[]
    def finish(tone:str|None=None):
        raw="".join(current)
        if not raw: raise XSampaConversionError("tone or syllable boundary without segmental content")
        syllables.append(XSampaSyllable(raw,_convert_segmental(raw),tone,_TONES.get(tone or "")))
        current.clear()
    for token in re.findall(r"\.|[^\s.]+",label.strip()):
        if token==".":
            if current: finish()
            elif not syllables: raise XSampaConversionError("leading syllable boundary")
            continue
        cursor=0
        for match in _TONE_RE.finditer(token):
            current.append(token[cursor:match.start()])
            if not any(current): raise XSampaConversionError("tone suffix without segmental content")
            finish(match.group("tone")); cursor=match.end()
        remainder=token[cursor:]
        if remainder: current.append(remainder)
    if current: finish()
    if not syllables: raise XSampaConversionError("label contains no syllables")
    return XSampaLabel(label,tuple(syllables))
