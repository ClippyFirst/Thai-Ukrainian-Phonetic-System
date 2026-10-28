// RTGS reference prototype for a small provisional fixture list only.
// This deliberately does not guess romanization for arbitrary Thai strings.
// Planned reference for parity work: PyThaiNLP's Apache-2.0-licensed "royin" implementation.
// These fixtures are provisional and have not been checked against that implementation.
// See docs/research/thai-romanization-integration.md for provenance and limits.

const RTGS_FIXTURES = new Map([
  ["กา", "ka"],
  ["พริก", "phrik"],
  ["มา", "ma"],
  ["ไฟ", "fai"],
  ["หมา", "ma"],
  ["ใหม่", "mai"],
]);

/**
 * Return a provisional RTGS fixture for an exact lexical token.
 * RTGS is a lossy Latin transcription, not IPA and not English G2P.
 * Unknown tokens are explicitly unavailable rather than guessed.
 */
export function lookupRtgsToken(token) {
  const value = RTGS_FIXTURES.get(String(token ?? "").normalize("NFC"));
  return value
    ? { status: "fixture", value, source: "provisional-fixture" }
    : { status: "unavailable", value: null, source: null };
}

/**
 * Format token-level RTGS references without inventing segmentation.
 * Caller must supply the existing analyser's token boundaries.
 */
export function renderRtgsTokens(tokens) {
  return (tokens || []).map(token => {
    if (token.kind !== "thai") return token.input;
    const result = lookupRtgsToken(token.input);
    return result.status === "fixture" ? result.value : "⟦RTGS НЕ ПЕРЕВІРЕНО: " + token.input + "⟧";
  }).join("");
}
