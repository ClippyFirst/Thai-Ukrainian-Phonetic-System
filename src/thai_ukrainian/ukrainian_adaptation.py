from __future__ import annotations

from .models import SyllableAnalysis
from .phonology import effective_onset


# Thai grapheme → Ukrainian orthographic adaptation.
# These are project rules, not an official Ukrainian transliteration standard.
ONSET_UA = {
    "ก": "к", "ข": "к", "ฃ": "к", "ค": "к", "ฅ": "к", "ฆ": "к",
    "ง": "нг", "จ": "ч", "ฉ": "ч", "ช": "ч", "ซ": "с", "ฌ": "ч",
    "ญ": "й", "ฎ": "д", "ฏ": "т", "ฐ": "т", "ฑ": "т", "ฒ": "т",
    "ณ": "н", "ด": "д", "ต": "т", "ถ": "т", "ท": "т", "ธ": "т", "น": "н",
    "บ": "б", "ป": "п", "ผ": "п", "ฝ": "ф", "พ": "п", "ฟ": "ф", "ภ": "п",
    "ม": "м", "ย": "й", "ร": "р", "ล": "л", "ว": "в", "ศ": "с", "ษ": "с",
    "ส": "с", "ห": "г", "ฬ": "л", "ฮ": "г", "อ": "",
}

CODA_UA = {
    "ง": "нг",
    "จ": "т", "ช": "т", "ซ": "т", "ฎ": "т", "ฏ": "т",
    "ฐ": "т", "ฑ": "т", "ฒ": "т", "ถ": "т", "ท": "т", "ธ": "т",
    "ด": "т", "ต": "т", "ศ": "т", "ษ": "т", "ส": "т",
    "บ": "п", "ป": "п", "ผ": "п", "พ": "п", "ฟ": "п", "ภ": "п",
    "ม": "м", "ณ": "н", "น": "н", "ญ": "н", "ร": "н", "ล": "н", "ฬ": "н",
    "ย": "й", "ว": "в",
}

CODA_IPA_UA = {
    "p": "п", "t": "т", "k": "к", "ʔ": "",
    "m": "м", "n": "н", "ŋ": "нг", "j": "й", "w": "в",
}

VOWEL_UA = {
    "V-01": "і", "V-02": "і", "V-03": "е", "V-04": "е",
    "V-05": "е", "V-06": "е", "V-07": "и", "V-08": "и",
    "V-09": "е", "V-10": "е", "V-11": "а", "V-12": "а",
    "V-13": "у", "V-14": "у", "V-15": "о", "V-16": "о",
    "V-17": "о", "V-18": "о", "V-19": "іа", "V-20": "іа",
    "V-21": "иа", "V-22": "иа", "V-23": "уа", "V-24": "уа",
    "V-X-AI": "ай", "V-X-AM": "ам", "V-X-AJ": "ай", "V-X-AW": "ав",
    "V-X-IW": "ів", "V-X-UJ": "уй", "V-X-EW": "ев", "V-X-EW-L": "ев",
    "V-X-EAW": "ев", "V-X-EY": "ей", "V-X-OY": "ой", "V-X-OJ": "ой",
    "V-X-AW-S": "ав", "V-X-IAW": "іав", "V-X-UAJ": "уай", "V-X-UEY": "иай", "V-X-UA": "уа", "IV-INHERENT-O": "о",
}


def adapt_syllable_to_ukrainian(a: SyllableAnalysis) -> str | None:
    """Render Ukrainian output from structured Thai analysis, not from IPA."""
    if a.status != "analyzed" or not a.vowel_id:
        return None

    onset = effective_onset(a)
    onset_text = "".join(ONSET_UA.get(c, "") for c in onset)
    vowel_text = VOWEL_UA.get(a.vowel_id)
    if vowel_text is None:
        return None

    coda_text = CODA_IPA_UA.get(a.coda_ipa or "", "") if a.coda else ""
    return onset_text + vowel_text + coda_text
