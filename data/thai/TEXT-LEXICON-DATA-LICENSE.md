# Text lexicon data provenance and license

The repository's software is licensed separately from source-derived language data. The five rows added to `text_lexicon.tsv` on 2026-10-25 (ไกล, ใกล้, เดิน, กรรม, บรรจุ) are source-attested from the exact Thai Wiktionary revisions recorded in `text_lexicon_sources.csv`.

Those source pages state Creative Commons Attribution-ShareAlike terms; their reused lexical segmentation/reading data is tracked here as **CC BY-SA 4.0**, with attribution to the Thai Wiktionary contributors and links to each exact revision. Keep these rows and their provenance together when copying or adapting the source-derived subset. Do not infer that the repository's MIT software license relicenses the source-derived rows.

This is a small, deliberately curated set, not a bulk Wiktionary import. It supports lexical segmentation/normalization only; it is **not** independently adjudicated IPA gold, not proof that every downstream engine result is correct, and not a representative lexicon-coverage sample.

The candidate เงิน is documented but intentionally excluded from the runtime lexicon. Its source page records short /ɤ/ in /ŋɤn/, while the project evidence register identifies this spelling environment as length-ambiguous without lexical evidence. The text lexicon currently carries syllable strings, not a typed lexical IPA override, so inserting เงิน as an ordinary graphemic syllable could conceal the very distinction that needs resolving. Do not add it until a typed, provenance-bearing lexical-pronunciation adapter and Python/browser parity tests are implemented.

Source data reviewed 2026-10-25. See `data/thai/text_lexicon_sources.csv` for exact revision locators.
