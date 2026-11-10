# Five Immersive Thai–Ukrainian Prototype Directions

## Intent
Create five genuinely different, clickable visual directions for the existing Thai-reading and phonetic-transcription project. The prototypes are for comparison and selection, not production replacement.

## Product truth
- This is a reading/transcription aid, not a translator.
- The conceptual pipeline is Thai orthography → structural analysis → Thai phonology → typed IPA → Ukrainian practical adaptation.
- The Ukrainian line is provisional; accuracy is not independently measured.
- The real browser service processes text locally. Do not imply text is uploaded.
- The prototype may use clearly labeled illustrative demo states; it must never imply that its mock values came from the real engine.

## Five directions
1. X-Ray Archive: cursor spotlight reveals layered annotations and syllable anatomy.
2. Fluid Language: cursor-responsive fluid/mesh field and a staged text-to-structure reveal.
3. Phonetic Universe: spatial constellation of orthography, syllables, tone categories, IPA, and Ukrainian adaptation.
4. Portal Interface: full-screen navigable rooms with distinct section transitions and a persistent way back.
5. Living Atlas: explorable knowledge graph connecting writing, phonology, tone, IPA, adaptation, and uncertainty.

## Interaction requirements
- Each direction must have its own composition, navigation, and signature interaction; do not reuse one hero/card template with recolored skins.
- Each has a working concept switcher, section navigation, Thai input, example chips, and an explicitly labeled illustrative result interaction.
- Pointer effects must degrade to tap/focus behavior on touch devices.
- Keyboard operation and visible focus are required.
- Respect prefers-reduced-motion; do not make essential information depend on animation.
- Keep reading and working surfaces legible; effects must not obscure input or result text.
- No external runtime dependency or network call is needed.

## Non-goals
- Do not replace the production homepage or transcription engine.
- Do not modify main or merge a pull request.
- Do not claim linguistic validation, measured accuracy, or real engine execution in demo panels.

## Acceptance
- Five visibly and behaviorally distinct directions exist in one easy-to-compare prototype page.
- Each direction has a functional input/example/demo-state interaction.
- Responsive layout, reduced motion, keyboard focus, and touch fallback are present.
- The prototype page states that demo outputs are illustrative and not engine results.
