from __future__ import annotations

import unicodedata

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
    "h": ("г", "UA-H"), "ʔ": ("", "UA-GLOTTAL-STOP"),
    "a": ("а", "UA-A"), "i": ("і", "UA-I"), "e": ("е", "UA-E"),
    "ɛ": ("е", "UA-EPSILON"), "ɯ": ("и", "UA-BARRED-I"),
    "ɤ": ("е", "UA-GAMMA"), "u": ("у", "UA-U"), "o": ("о", "UA-O"),
    "ɔ": ("о", "UA-OPEN-O"),
}
ORDER = tuple(sorted(IPA_TO_UA, key=len, reverse=True))
VOWELS = {"a", "i", "e", "ɛ", "ɯ", "ɤ", "u", "o", "ɔ"}
TONE_DIACRITICS = {"\u0300", "\u0301", "\u0302", "\u0304", "\u030c", "\u030b", "\u030f"}  # U+0306 breve can mark extra-shortness; preserve/fail closed.
IPA_MODIFIERS = {"\u031a", "\u032f", "\u0329"}


def _normalize_ipa_input(source_ipa: str) -> tuple[str, list[str], dict[str, bool]]:
    """Normalize presentation conventions while preserving unknown segments."""
    ipa = source_ipa.strip()
    notes = {
        "wrapped": False,
        "tone": False,
        "stress": False,
        "length": False,
        "modifier": False,
    }
    if ((ipa.startswith("[") and ipa.endswith("]"))
            or (ipa.startswith("/") and ipa.endswith("/") and len(ipa) > 1)):
        ipa = ipa[1:-1].strip()
        notes["wrapped"] = True
    ipa = ipa.replace("t\u0361ɕ", "tɕ").replace("t\u035cɕ", "tɕ")
    normalized: list[str] = []
    for char in unicodedata.normalize("NFD", ipa):
        if char in "˥˦˧˨˩" or char in TONE_DIACRITICS:
            notes["tone"] = True
            continue
        if char in {"ˈ", "ˌ"}:
            notes["stress"] = True
            continue
        if char in {"ː", "ˑ"}:
            notes["length"] = True
            normalized.append(char)
            continue
        if char in IPA_MODIFIERS:
            notes["modifier"] = True
        normalized.append(char)
    return unicodedata.normalize("NFC", "".join(normalized)), [
        label for key, label in (
            ("wrapped", "IPA delimiters normalized"),
            ("tone", "tone notation recognized and kept outside segmental Ukrainian spelling"),
            ("stress", "stress notation recognized and not represented in practical Ukrainian spelling"),
            ("length", "vowel length notation recognized"),
            ("modifier", "phonetic modifiers recognized"),
        ) if notes[key]
    ], notes


def adapt_phonetic_result(result: PhoneticResult) -> dict:
    """Adapt only typed phonemic IPA; fail closed on unsupported IPA symbols."""
    source_ipa = result.phonemic_ipa
    if result.status != "SUPPORTED" or not source_ipa:
        return {
            "status": "withheld", "source_ipa": source_ipa, "output": None,
            "rules_applied": [], "input_notes": [],
            "warnings": ["Phonetic result is not supported; Ukrainian output withheld."],
        }

    trimmed_source = source_ipa.strip()
    # A single unmatched/mixed outer delimiter is malformed notation, not IPA.
    if ((trimmed_source.startswith("[") != trimmed_source.endswith("]"))
            or (trimmed_source.startswith("/") != trimmed_source.endswith("/"))
            or (trimmed_source.startswith("[") and trimmed_source.endswith("/"))
            or (trimmed_source.startswith("/") and trimmed_source.endswith("]"))):
        return {
            "status": "withheld", "source_ipa": source_ipa, "output": None,
            "rules_applied": [], "input_notes": [],
            "warnings": ["Mismatched IPA delimiters; Ukrainian output withheld."],
        }

    ipa, input_notes, notation = _normalize_ipa_input(source_ipa)
    if not ipa.strip():
        return {
            "status": "withheld", "source_ipa": source_ipa, "normalized_ipa": ipa,
            "output": None, "rules_applied": [], "input_notes": input_notes,
            "warnings": ["IPA input contains no supported segmental symbols after normalization."],
        }

    output: list[str] = []
    rules: list[str] = []
    neutralized: list[str] = []
    i = 0
    previous_base = ""
    while i < len(ipa):
        if ipa[i].isspace() or ipa[i] == ".":
            output.append(ipa[i])
            i += 1
            previous_base = ""
            continue
        if ipa[i] in {"ː", "ˑ", "\u032f", "\u0329", "\u031a"}:
            if ipa[i] in {"ː", "ˑ"}:
                neutralized.append("vowel length")
            else:
                neutralized.append("phonetic detail not represented in Ukrainian practical spelling")
            i += 1
            continue
        token = next((key for key in ORDER if ipa.startswith(key, i)), None)
        if token is None:
            return {
                "status": "withheld", "source_ipa": source_ipa, "normalized_ipa": ipa,
                "output": None, "rules_applied": rules, "input_notes": input_notes,
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
        if token == "h":
            neutralized.append("glottal place and voicing")
        if token in {"ɛ", "ɯ", "ɤ", "ɔ"}:
            neutralized.append("vowel quality")
        previous_base = token
        i += len(token)

    if notation["tone"]:
        neutralized.append("lexical tone is not encoded in Ukrainian practical spelling")
    if notation["stress"]:
        neutralized.append("stress is not encoded by this project adaptation")
    if notation["length"]:
        neutralized.append("vowel length")
    return {
        "status": "adapted", "source_ipa": source_ipa, "normalized_ipa": ipa,
        "output": "".join(output),
        "rules_applied": list(dict.fromkeys(rules)),
        "neutralized_features": list(dict.fromkeys(neutralized)),
        "input_notes": input_notes,
        "tone_separate": True,
        "warnings": [
            "Project-defined practical adaptation; not an official Ukrainian standard. "
            "Verify lexical reading and target-language convention independently."
        ],
    }


def adapt_syllable_to_ukrainian(result: PhoneticResult) -> str | None:
    """Compatibility helper: returns output from IPA, never from Thai graphemes."""
    adapted = adapt_phonetic_result(result)
    return adapted["output"]
