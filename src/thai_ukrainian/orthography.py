import unicodedata
from .inventory import load_consonants

TONE_MARKS = {"่": "mai_ek", "้": "mai_tho", "๊": "mai_tri", "๋": "mai_chattawa"}
VOWEL_MARKS = set("ะาิีึืุูเแโใไำั็")

def normalize_thai(text):
    return unicodedata.normalize("NFC", text)

def decompose_thai(text):
    inv = load_consonants()
    text = normalize_thai(text)
    rows = []
    for i, ch in enumerate(text):
        role = "consonant" if ch in inv else "tone_mark" if ch in TONE_MARKS else "thai_vowel_or_mark" if ch in VOWEL_MARKS else "other"
        rows.append({"char": ch, "index": i, "unicode": f"U+{ord(ch):04X}", "role": role})
    return rows
