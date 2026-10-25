# Text lexicon data provenance and license

The repository's software is licensed separately from source-derived language data. The five rows added to `text_lexicon.tsv` on 2026-10-25 (ไกล, ใกล้, เดิน, กรรม, บรรจุ) are source-attested from the exact Thai Wiktionary revisions recorded in `text_lexicon_sources.csv`.

Those source pages state Creative Commons Attribution-ShareAlike terms; their reused lexical segmentation/reading data is tracked here as **CC BY-SA 4.0**, with attribution to the Thai Wiktionary contributors and links to each exact revision. Keep these rows and their provenance together when copying or adapting the source-derived subset. Do not infer that the repository's MIT software license relicenses the source-derived rows.

This is a small, deliberately curated set, not a bulk Wiktionary import. It supports lexical segmentation/normalization only; it is **not** independently adjudicated IPA gold, not proof that every downstream engine result is correct, and not a representative lexicon-coverage sample.

The word เงิน is enabled only through `data/thai/lexical_ipa_overrides.tsv`, not as an ordinary graphemic syllable entry. Its pinned Thai Wiktionary revision 5759179 records short /ɤ/ in /ŋɤn/. The override preserves source provenance, short-vowel metadata and tone through the typed IPA → Ukrainian adapter boundary. This is dictionary-attested evidence, not independent phonetic gold; it must not be used to claim acoustic correctness or generalize to other words.

Source data reviewed 2026-10-25. See `data/thai/text_lexicon_sources.csv` for exact revision locators.
