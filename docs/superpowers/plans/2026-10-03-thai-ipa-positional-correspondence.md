# Thai → IPA → Ukrainian Positional Correspondence Implementation Plan

> For agentic workers: use the superpowers execution workflow. Steps use checkbox syntax.

Goal: Make IPA a first-class audit layer in the Thai correspondence tables and expose position-sensitive consonant realizations while keeping unsupported vowel allophony explicitly unforced.

Architecture: Add a small contextual-phonology module between phonological composition and surface IPA. Extend the exhaustive master generator to emit component-level phonemic/surface IPA and Ukrainian output derived from IPA, plus separate consonant and vowel correspondence tables. Keep word-position metadata distinct from syllable-internal onset/coda position.

Tech Stack: Python 3.14, dataclasses, CSV registries, unittest, deterministic generated CSV/JSON artifacts, GitHub Actions.

Global constraints:
- IPA is the mandatory intermediate representation.
- Phonemic IPA and surface IPA remain separate.
- Final consonant neutralization/release behavior is modeled only where declared evidence supports it.
- No vowel-quality allophony is invented without a declared rule and evidence.
- Word initial/medial/final position is metadata and does not automatically alter IPA.
- Structural generation remains distinct from lexical/corpus attestation.

Review focus:
- voiced Thai obstruents in coda position must not retain onset IPA;
- final p/t/k must remain identifiable as unreleased surface stops;
- vowel tables must not claim unsupported positional vowel-quality changes;
- Ukrainian candidates must be traceable to IPA;
- structural cardinality must remain 343200.

Tasks:
1. Add contextual.py and failing positional tests.
2. Integrate surface IPA into phonology.py without changing phonemic IPA.
3. Extend generate_master_table.py with component IPA columns and separate consonant/vowel artifacts.
4. Update README and documentation.
5. Run all generators and the complete unittest suite.