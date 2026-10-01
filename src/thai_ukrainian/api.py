from .orthography import decompose_thai
from .parser import parse_syllable
from .tone import determine_tone
from .correspondence import rank_ukrainian_candidates as _rank

def analyze_syllable(syllable):
    a = parse_syllable(syllable)
    if a.onset_class and a.live_dead and a.vowel_length:
        a.tone = determine_tone(a.onset_class, a.live_dead, a.vowel_length, a.tone_mark)
        a.rules_applied.append(a.tone.rule_id)
    return a

def parse_thai(text):
    return [analyze_syllable(x) for x in text.split() if x]

def phonologize_thai(text):
    return parse_thai(text)

def phoneticize_thai(text):
    return [{"input": a.input, "tone": a.tone.tone if a.tone else None, "tone_ipa": a.tone.contour_ipa if a.tone else None, "status": a.status} for a in parse_thai(text)]

def rank_ukrainian_candidates(ipa):
    return _rank(ipa)

def transliterate_thai(text):
    return [a.__dict__ for a in parse_thai(text)]
