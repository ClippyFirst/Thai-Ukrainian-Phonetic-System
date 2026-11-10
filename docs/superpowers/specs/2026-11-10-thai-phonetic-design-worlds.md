# Five distinct visual worlds for the Thai–Ukrainian phonetic service

## Intent
Replace the first, generic five-way prototype gallery with five genuinely different art directions that make the product's distinctive mechanism visible: Thai orthography is structurally analyzed, interpreted phonologically, represented in IPA, then adapted into a provisional Ukrainian practical form. The site is a reading/transcription instrument, not a translator.

## Audience and primary job
A Ukrainian-speaking reader/researcher enters Thai text and wants to inspect how the system derives a phonetic reading and a Ukrainian candidate. The first screen should make the subject memorable; the workbench must remain immediately understandable and usable.

## Approved directions
1. **Living Glyphs** — Thai letterforms as spatial, layered objects; iridescent enamel, liquid-light edges and dimensional glyph composition. Signature: a large Thai syllable whose orthographic components separate into spatial layers.
2. **Tone Observatory** — deep atmospheric field and five distinct luminous pitch-contour ribbons. Signature: five tone paths that illuminate as a conceptual legend; explicitly illustrative, not measured audio.
3. **Phonetic Prism** — an optical transformation story from Thai script through IPA to Ukrainian adaptation. Signature: spectral refraction and translucent prism planes, with IPA visibly retained as the intermediate layer.
4. **Type Foundry** — experimental Thai/Ukrainian type specimen culture, editorial scale shifts, glyph anatomy and looped/loopless form comparisons. Signature: typographic specimen wall and precise annotations.
5. **Living Phonetic Instrument** — the richest synthesis: living Thai glyphs, tone paths, and the Thai → IPA → Ukrainian sequence. Signature: a staged instrument-like composition where structural layers reveal causal steps.

## Goals
- Five independent visual concepts with visibly different compositions, material languages, type hierarchy and motion signatures.
- A common prototype switcher for side-by-side evaluation.
- Each concept contains a clear workbench with Thai input, example loading, an explicit demo-only result, and an honest boundary between visual prototype and actual engine.
- Responsive behavior, keyboard focus, reduced-motion support, readable contrast and no external runtime dependencies.
- Preserve the existing separate branch; do not modify main, merge, or open a PR without a later instruction.

## Non-goals
- Do not connect or alter the transcription engine.
- Do not claim linguistic accuracy, validation, or measured audio.
- Do not redesign the production pages in this task.
- Do not add dependencies, tracking, network calls, or send Thai input anywhere.

## Product truth and constraints
- The browser service processes Thai text locally; never imply input is uploaded.
- Ukrainian output is a provisional candidate, not expert-validated transcription.
- The intermediate IPA is essential; do not depict direct Thai-grapheme-to-Ukrainian substitution.
- Accuracy remains NOT_MEASURED against an independent IPA gold set.
- Visual demo output is illustrative placeholder content and must be labelled as such.
- Keep the workbench calm enough for reading; reserve strong spectacle for hero and the analysis explanation.

## Interaction and motion
- Concept switcher changes the visible prototype without navigation.
- Example controls fill the textarea; Analyze only reveals the labelled illustrative state and never pretends to call the engine.
- The signature sequence is explanatory and can be replayed; it must not delay access to the input or controls.
- Motion uses CSS transforms/opacity, short UI feedback, and one explanatory hero/sequence moment per concept. Respect prefers-reduced-motion and pointer capability.

## Acceptance
- All five concepts are available from one page and are not merely palette swaps.
- Each has a unique hero composition and signature visual.
- No invented metrics, real-time audio claims, or fabricated engine results.
- Mobile layout works at narrow widths; all controls are keyboard reachable with visible focus.
- Main branch remains untouched; changes stay on the design branch.
