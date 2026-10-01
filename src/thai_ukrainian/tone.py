from .models import ToneResult

TONE_IPA = {"mid": "˧", "low": "˩", "falling": "˥˩", "high": "˥", "rising": "˩˥"}

def classify_live_dead(vowel_length, coda_ipa, open_syllable=True):
    if coda_ipa in {"p", "t", "k", "ʔ"}:
        return "dead"
    if open_syllable and vowel_length == "short":
        return "dead"
    return "live"

def determine_tone(consonant_class, live_dead, vowel_length, tone_mark=None):
    mark = tone_mark or "none"
    if mark == "mai_tri":
        if consonant_class != "mid":
            raise ValueError("mai tri is restricted to mid-class spellings in the standard rule system")
        tone, rule = "high", "T-MID-TRI"
    elif mark == "mai_chattawa":
        if consonant_class != "mid":
            raise ValueError("mai chattawa is restricted to mid-class spellings in the standard rule system")
        tone, rule = "rising", "T-MID-CHATTAWA"
    elif mark == "mai_ek":
        tone, rule = {"mid": "low", "high": "low", "low": "falling"}[consonant_class], f"T-{consonant_class.upper()}-EK"
    elif mark == "mai_tho":
        tone, rule = {"mid": "falling", "high": "falling", "low": "high"}[consonant_class], f"T-{consonant_class.upper()}-THO"
    elif live_dead == "live":
        tone, rule = {"mid": "mid", "high": "rising", "low": "mid"}[consonant_class], f"T-{consonant_class.upper()}-LIVE-NONE"
    elif consonant_class in {"mid", "high"}:
        tone, rule = "low", f"T-{consonant_class.upper()}-DEAD-NONE"
    elif vowel_length == "short":
        tone, rule = "high", "T-LOW-DEAD-SHORT"
    else:
        tone, rule = "falling", "T-LOW-DEAD-LONG"
    return ToneResult(tone, TONE_IPA[tone], rule)
