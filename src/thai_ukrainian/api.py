from .parser import parse_syllable
from .tone import determine_tone
from .phonology import phonologize,surface_phoneticize,ONSET_IPA,effective_onset
from .correspondence import rank_ukrainian_candidates as _rank_candidates
from .word import analyze_word
from .ua_orthography import candidates_for_ipa

def analyze_syllable(syllable:str):
    a=parse_syllable(syllable)
    if a.status == "analyzed" and a.tone_class and a.live_dead and a.vowel_length:
        try:
            a.tone=determine_tone(a.tone_class,a.live_dead,a.vowel_length,a.tone_mark)
            a.rules_applied.append(a.tone.rule_id)
        except ValueError as exc:
            # Invalid orthographic tone combinations are data-level findings,
            # not parser crashes. Keep the segmental analysis available.
            a.status="invalid:tone-combination"
            a.warnings.append(str(exc))
    phonologize(a);surface_phoneticize(a)
    if a.phonemic_ipa:
        a.ukrainian_orthography_candidates=candidates_for_ipa(a.phonemic_ipa)
        if a.ukrainian_orthography_candidates:
            a.selected_ukrainian_orthography=a.ukrainian_orthography_candidates[0]
    onset=effective_onset(a)
    if onset:
        first=ONSET_IPA.get(onset[0])
        if first:
            a.ukrainian_candidates=_rank_candidates(first)[:10]
            if a.ukrainian_candidates:a.selected_candidate=a.ukrainian_candidates[0].ipa
    return a

def parse_thai(text:str):
    return [analyze_syllable(x) for x in text.split() if x]

def analyze_word_syllables(syllables:list[str] | tuple[str,...]):
    return analyze_word(syllables)

def phonologize_thai(text:str):
    return [a.as_dict() for a in parse_thai(text)]

def phoneticize_thai(text:str):
    return [{"input":a.input,"ipa":a.phonetic_ipa,"tone":a.tone.tone if a.tone else None,"tone_ipa":a.tone.contour_ipa if a.tone else None,"status":a.status} for a in parse_thai(text)]

def rank_ukrainian_candidates(ipa:str):return [x.__dict__ for x in _rank_candidates(ipa)]

def transliterate_thai(text:str):return [a.as_dict() for a in parse_thai(text)]
