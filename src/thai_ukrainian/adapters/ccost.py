"""Text-only CCOST TextGrid reader and typed X-SAMPA adapter."""
from __future__ import annotations
import re
from dataclasses import dataclass
from .phonetic_result import PhoneticResult, _segment_ipa
from .xsampa import XSampaLabel, convert_xsampa_label

CCOST_DOI="10.5281/zenodo.17366698"
CCOST_SOURCE=f"CCOST@{CCOST_DOI}"
CCOST_PHONETIC_TIERS=frozenset({"KAN","KAS","MAU","MAS"})
CCOST_PHONEMIC_TIERS=frozenset({"KAN","KAS","MAS"})
CCOST_TIER_DESCRIPTIONS={"ORT":"orthographic word","KAN":"canonical word pronunciation",
"KAS":"canonical syllabified pronunciation","MAU":"phonetic segment","MAS":"phonemic syllable",
"TRN":"orthographic utterance transcript"}

class TextGridFormatError(ValueError):
    """Raised when a Praat long-text TextGrid cannot be parsed safely."""

@dataclass(frozen=True)
class TextGridInterval:
    xmin:float
    xmax:float
    text:str

@dataclass(frozen=True)
class TextGridPoint:
    number:float
    mark:str

@dataclass(frozen=True)
class TextGridTier:
    name:str
    kind:str
    xmin:float
    xmax:float
    intervals:tuple[TextGridInterval,...]=()
    points:tuple[TextGridPoint,...]=()

@dataclass(frozen=True)
class TextGrid:
    xmin:float
    xmax:float
    tiers:tuple[TextGridTier,...]
    def tier(self,name:str)->TextGridTier:
        matches=[tier for tier in self.tiers if tier.name==name]
        if len(matches)!=1: raise KeyError(f"expected exactly one tier named {name!r}; found {len(matches)}")
        return matches[0]

@dataclass(frozen=True)
class CCOSTAnnotation:
    tier:str
    xmin:float
    xmax:float
    converted:XSampaLabel
    @property
    def ipa(self)->str: return self.converted.ipa
    def to_phonetic_results(self)->tuple[PhoneticResult,...]:
        """Return one typed result for this interval; never fabricate per-syllable times."""
        provenance=(CCOST_SOURCE,f"Praat TextGrid tier {self.tier}",
                    "X-SAMPA symbol mapping: Wells (1995; revised 2000)",
                    "CCOST tone suffix convention: _1.._5")
        segments=tuple(_segment_ipa(self.converted.ipa,provenance))
        boundaries=[0]
        offset=0
        for syllable in self.converted.syllables:
            offset+=len(_segment_ipa(syllable.ipa,provenance))
            boundaries.append(offset)
        tone_category=(self.converted.syllables[0].tone_category
                       if len(self.converted.syllables)==1 else None)
        common={
            "segments":segments,
            "syllable_boundaries":tuple(boundaries),
            "vowel_length":"long" if "ː" in self.converted.ipa else None,
            "tone_category":tone_category,
            "provenance":provenance,
        }
        if self.tier in CCOST_PHONEMIC_TIERS:
            return (PhoneticResult(
                phonemic_ipa=self.converted.ipa,broad_surface_ipa=None,
                status="PROVISIONAL",uncertainty=(
                    "CCOST source annotation; not independently adjudicated gold.",
                    "Per-syllable tone labels remain in CCOSTAnnotation.converted; the scalar PhoneticResult tone is omitted for multisyllabic labels.",
                    "Actual released TextGrid conformance has not yet been independently reviewed.",
                ),external_ipa=self.converted.ipa,**common),)
        return (PhoneticResult(
            phonemic_ipa=None,broad_surface_ipa=self.converted.ipa,
            status="UNSUPPORTED",uncertainty=(
                "MAU is a phone-level surface tier; aggregate and align it with syllable context before adaptation.",
                "Surface phone labels are not phonemic syllable labels.",
            ),external_ipa=None,**common),)

def _quoted_field(block:str,field:str)->str:
    match=re.search(rf'(?m)^\s*{re.escape(field)}\s*=\s*"(.*)"\s*$',block)
    if match is None: raise TextGridFormatError(f"missing quoted TextGrid field {field!r}")
    return match.group(1).replace('""','"')

def _number_field(block:str,field:str)->float:
    match=re.search(rf"(?m)^\s*{re.escape(field)}\s*=\s*([-+0-9.eE]+)\s*$",block)
    if match is None: raise TextGridFormatError(f"missing numeric TextGrid field {field!r}")
    try: return float(match.group(1))
    except ValueError as exc: raise TextGridFormatError(f"invalid numeric TextGrid field {field!r}") from exc

def _indexed_blocks(block:str,prefix:str)->list[str]:
    starts=list(re.finditer(rf"(?m)^\s*{re.escape(prefix)}\s*\[\d+\]\s*:\s*$",block))
    return [block[start.start():starts[i+1].start() if i+1<len(starts) else len(block)]
            for i,start in enumerate(starts)]

def parse_textgrid_long(text:str)->TextGrid:
    """Parse Praat long-text TextGrid without touching paired audio."""
    if not isinstance(text,str): raise TypeError("TextGrid content must be text")
    if 'Object class = "TextGrid"' not in text or "item []:" not in text:
        raise TextGridFormatError("only Praat long-text TextGrid files are supported; short/binary formats are not guessed")
    xmin,xmax=_number_field(text,"xmin"),_number_field(text,"xmax")
    item_blocks=_indexed_blocks(text,"item")
    if not item_blocks: raise TextGridFormatError("TextGrid contains no item tiers")
    tiers=[]
    for block in item_blocks:
        kind,name=_quoted_field(block,"class"),_quoted_field(block,"name")
        tier_xmin,tier_xmax=_number_field(block,"xmin"),_number_field(block,"xmax")
        if kind=="IntervalTier":
            intervals=tuple(TextGridInterval(_number_field(part,"xmin"),_number_field(part,"xmax"),
                _quoted_field(part,"text")) for part in _indexed_blocks(block,"intervals"))
            if any(item.xmax<item.xmin for item in intervals):
                raise TextGridFormatError(f"negative interval duration in tier {name!r}")
            tiers.append(TextGridTier(name,kind,tier_xmin,tier_xmax,intervals=intervals))
        elif kind=="TextTier":
            points=tuple(TextGridPoint(_number_field(part,"number"),_quoted_field(part,"mark"))
                for part in _indexed_blocks(block,"points"))
            tiers.append(TextGridTier(name,kind,tier_xmin,tier_xmax,points=points))
        else: raise TextGridFormatError(f"unsupported TextGrid tier class {kind!r}")
    names=[tier.name for tier in tiers]
    if len(names)!=len(set(names)): raise TextGridFormatError("duplicate TextGrid tier names")
    return TextGrid(xmin,xmax,tuple(tiers))

def convert_ccost_tier(textgrid:TextGrid,tier_name:str)->tuple[CCOSTAnnotation,...]:
    """Convert non-empty X-SAMPA labels from one published CCOST pronunciation tier."""
    if tier_name not in CCOST_PHONETIC_TIERS:
        raise ValueError(f"tier {tier_name!r} is not a declared CCOST pronunciation tier; expected one of {', '.join(sorted(CCOST_PHONETIC_TIERS))}")
    tier=textgrid.tier(tier_name)
    if tier.kind!="IntervalTier":
        raise TextGridFormatError(f"CCOST pronunciation tier {tier_name!r} must be an IntervalTier")
    converted=[]
    for interval in tier.intervals:
        label=interval.text.strip()
        if not label or label in {"<p :>","<usb>"}: continue
        converted.append(CCOSTAnnotation(tier_name,interval.xmin,interval.xmax,convert_xsampa_label(label)))
    return tuple(converted)
