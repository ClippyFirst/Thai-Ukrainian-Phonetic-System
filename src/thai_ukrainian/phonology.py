from __future__ import annotations
from .models import SyllableAnalysis
from .contextual import surface_ipa_for_consonant, vowel_surface_context
from .inventory import load_consonants

# The Thai consonant registry is the sole source of onset IPA and consonant
# class. Keep these fast lookup views derived rather than maintaining parallel
# hand-written inventories in the phonology layer.
_CONSONANTS = load_consonants()
ONSET_IPA = {
    grapheme: consonant.onset_ipa
    for grapheme, consonant in _CONSONANTS.items()
    if consonant.onset_ipa
}
LOW_SINGLE = {
    grapheme
    for grapheme, consonant in _CONSONANTS.items()
    if consonant.class_ == "low"
}

def effective_onset(a:SyllableAnalysis)->list[str]:
    if len(a.onset)>=2 and a.onset[0]=="ห" and a.onset[1] in LOW_SINGLE:
        a.rules_applied.append("ORTH-H-NAM")
        return [a.onset[1]]
    return a.onset

def phonologize(a:SyllableAnalysis)->SyllableAnalysis:
    onset=effective_onset(a)
    # A parser/status inconsistency or future inventory expansion must not
    # turn an unmapped consonant into a question mark inside apparently valid IPA.
    if any(c not in ONSET_IPA for c in onset):
        a.phonemic_ipa=None
        a.phonetic_ipa=None
        a.status="unresolved:unsupported-onset"
        a.warnings.append("Phonemic IPA withheld because of an unsupported onset consonant.")
        a.rules_applied.append("PHON-UNSUPPORTED-ONSET-WITHHELD")
        return a
    if a.vowel is None or a.status != "analyzed":

        a.phonemic_ipa=None
        a.warnings.append("Phonemic IPA withheld because the vowel is unresolved.")
        a.rules_applied.append("PHON-SEGMENTAL-COMPOSITION-WITHHELD")
        return a
    a.phonemic_ipa="".join(ONSET_IPA.get(c,"?") for c in onset)+(a.vowel)+(a.coda_ipa or "")
    a.rules_applied.append("PHON-SEGMENTAL-COMPOSITION")
    return a

def surface_phoneticize(a:SyllableAnalysis)->SyllableAnalysis:
    if not a.phonemic_ipa:
        a.phonetic_ipa=None
        a.rules_applied.append("PHON-SURFACE-WITHHELD")
        return a

    onset = effective_onset(a)
    inv = load_consonants()
    onset_surface = "".join(
        surface_ipa_for_consonant(inv[c], "onset") for c in onset
    )
    vowel_context = "closed" if a.coda else "open"
    vowel_surface = vowel_surface_context(a.vowel or "", vowel_context)

    coda_surface = ""
    if a.coda:
        coda_surface = surface_ipa_for_consonant(inv[a.coda], "coda")
        if coda_surface != (a.coda_ipa or ""):
            a.rules_applied.append("PHON-SURFACE-FINAL-STOP-UNRELEASED")

    a.phonetic_ipa = onset_surface + vowel_surface + coda_surface
    a.rules_applied.append("PHON-SURFACE-POSITIONAL-IPA")
    return a
