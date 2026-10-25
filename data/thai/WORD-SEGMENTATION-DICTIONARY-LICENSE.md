# Thai word-segmentation dictionary: provenance and license

The word-segmentation dictionary in `words_th_cc0.txt` is derived from the PyThaiNLP project word list.

- Source repository: https://github.com/PyThaiNLP/pythainlp
- Source file: `pythainlp/corpus/words_th.txt`
- Pinned source commit: `8b2b9a6d0f69846364f37e8c16ffc31177f6151c`
- Pinned source blob SHA-1: `093dda8a35646281e71a8a434137cb5fac57882e`
- Source license: CC0-1.0, as explicitly listed for `words_th.txt` in the pinned `pythainlp/corpus/corpus_license.md`.
- Machine-readable manifest: `data/thai/word-segmentation-dictionary-source.json`.

The repository copy is a deterministic transformation: retain only non-empty lines consisting exclusively of Unicode Thai-block code points U+0E00–U+0E7F, preserve source order, and remove exact duplicates. The file is a lexical candidate list, not a pronunciation lexicon, gold segmentation corpus, or claim that every entry is a single orthographic word.

The project segmentation implementation is independently authored; the external data are kept separate from the repository's MIT code license. CC0 permits reuse without attribution requirements, but this notice is retained for provenance and reproducibility.
