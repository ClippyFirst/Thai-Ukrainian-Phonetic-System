# Thai output contract

## Strictness

The current Thai service is **Strict-only by default** at the IPA → Ukrainian adapter boundary. The canonical adapter fails closed on an unmapped or ambiguous IPA sequence. The website's FastThaiG2P path is a separately labeled provisional candidate, not a canonical pronunciation result.

- **Strict:** active default; only supported, explicit IPA → Ukrainian correspondences are returned as a final adapter result.
- **Soft:** deferred. The current service does not define a broader, reproducible evidence threshold that would justify promoting more IPA correspondences into a user-facing mode.
- **Super-soft:** deferred. No grapheme-to-Ukrainian fallback is allowed; speculative target output would violate the IPA-first contract.

The optional `allowProvisional` adapter/API path is a research-candidate control, not a general Soft mode. It remains explicitly marked provisional and cannot replace the Strict result.

## Unresolved final output

When the browser has no Ukrainian final/candidate text for an input, it displays `???`. This is a display placeholder only. It does not represent an IPA symbol or a guessed pronunciation.

Python/API responses retain structured semantics: unavailable results use `None`/JSON `null` with `status`, `reason`, and diagnostic metadata. Do not serialize `???` in place of the typed null.

## Confirmed results, candidates and diagnostics

- The FastThaiG2P website result remains labeled as a provisional practical candidate.
- The IPA panel retains the raw/intermediate IPA; tone, vowel length and warnings remain separate.
- The native typed `PhoneticResult` retains phonemic/broad-surface/external IPA distinctions, segment/syllable boundaries, tone, length, provenance and uncertainty.
- The Ukrainian adapter must consume IPA and declared metadata only; it must not infer target letters directly from Thai graphemes, vowel IDs or coda fields.

## Runtime verification boundary

Python and browser checks are separate unless they compare the same typed fixtures. Existing typed-service JSON parity and browser tests remain the required acceptance gate; a UI placeholder test does not prove pronunciation accuracy or Python/browser phonological parity.
