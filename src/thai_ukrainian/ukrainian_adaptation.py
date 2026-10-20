from __future__ import annotations

from .phonetic_result import PhoneticResult

# IPA → Ukrainian practical adaptation. Thai graphemes and Thai vowel IDs are
# deliberately absent: the typed phonetic result is the sole input boundary.
# This is a project convention, not an official Ukrainian transliteration standard.
IPA_TO_UA = {
    "tɕʰ": ("ч", "UA-AFFRICATE-ASP"),
    "tɕ": ("ч", "UA-AFFRICATE"),
    "kʰ": ("к", "UA-K-ASP"),
    "pʰ": ("п", "UA-P-ASP"),
    "tʰ": ("т", "UA-T-ASP"),
    "k": ("к", "UA-K"), "p": ("п", "UA-P"), "t": ("т", "UA-T"),
    "d": ("д", "UA-D"), "b": ("б", "UA-B"),
    "ŋ": ("нг", "UA-NG"), "n": ("н", "UA-N"), "m": ("м", "UA-M"),
    "r": ("р", "UA-R"), "l": ("л", "UA-L"), "j": ("й", "UA-J"),
    "w": ("в", "UA-W"), "s": ("с", "UA-S"), "f": ("ф", "UA-F"),
    "h": ("х", "UA-H"), "ʔ": ("", "UA-GLOTTAL-STOP"),
    "a": ("а", "UA-A"), "i": ("і", "UA-I"), "e": ("е", "UA-E"),
    "ɛ": ("е", "UA-EPSILON"), "ɯ": ("и", "UA-BARRED-I"),
    "ɤ": ("е", "UA-GAMMA"), "u": ("у", "UA-U"), "o": ("о", "UA-O"),
    "ɔ": ("о", "UA-OPEN-O"),
}
ORDER = tuple(sorted(IPA_TO_UA, key=len, reverse=True))
VOWELS = {"a", "i", "e", "ɛ", "ɯ", "ɤ", "u", "o", "ɔ"}


def adapt_phonetic_result(result: PhoneticResult) -> dict:
    """Adapt only the phonemic IPA in a typed result; fail closed on unknown IPA."""
    ipa = result.phonemic_ipa
    if result.status != "SUPPORTED" or not ipa:
        return {
            "status": "withheld", "source_ipa": ipa, "output": None,
            "rules_applied": [], "warnings": ["Phonetic result is not supported; Ukrainian output withheld."],
        }

    output: list[str] = []
    rules: list[str] = []
    neutralized: list[str] = []
    i = 0
    previous_base = ""
    while i < len(ipa):
        if ipa[i] in ". ":
            output.append(ipa[i])
            i += 1
            previous_base = ""
            continue
        if ipa[i] == "ː":
            neutralized.append("vowel length")
            i += 1
            continue
        token = next((key for key in ORDER if ipa.startswith(key, i)), None)
        if token is None:
            return {
                "status": "withheld", "source_ipa": ipa, "output": None,
                "rules_applied": rules,
                "warnings": [f"Unsupported IPA symbol {ipa[i]!r}; Ukrainian output withheld."],
            }
        rendered, rule = IPA_TO_UA[token]
        # In licensed vowel+glide sequences, Thai /w/ is conventionally rendered
        # as Ukrainian у to preserve the rime rather than introducing в.
        if token == "w" and previous_base in VOWELS:
            rendered, rule = "у", "UA-W-VOCALIC"
            neutralized.append("glide-vowel sequence represented by Ukrainian vowel spelling")
        output.append(rendered)
        rules.append(rule)
        if token in {"kʰ", "pʰ", "tʰ", "tɕʰ"}:
            neutralized.append("aspiration")
        if token in {"ɛ", "ɯ", "ɤ", "ɔ"}:
            neutralized.append("vowel quality")
        previous_base = token
        i += len(token)

    return {
        "status": "adapted", "source_ipa": ipa, "output": "".join(output),
        "rules_applied": list(dict.fromkeys(rules)),
        "neutralized_features": list(dict.fromkeys(neutralized)),
        "tone_separate": True,
        "warnings": ["Project-defined practical adaptation; not an official Ukrainian standard."],
    }


def adapt_syllable_to_ukrainian(result: PhoneticResult) -> str | None:
    """Compatibility helper: returns output from IPA, never from Thai graphemes."""
    adapted = adapt_phonetic_result(result)
    return adapted["output"]
