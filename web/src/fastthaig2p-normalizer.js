/**
 * Browser-native port of FastThaiG2P's text normalizer.
 * Data maps are extracted from the pinned upstream normalizer.py at build time.
 * Maiyamok expansion takes the upstream-compatible word tokenizer as an injected dependency.
 */
const REGEX_SPECIAL = new Set(["\\", ".", "*", "+", "?", "^", "$", "{", "}", "(", ")", "|", "[", "]"]);
const escapeRegex = value => [...value].map(char => REGEX_SPECIAL.has(char) ? "\\" + char : char).join("");
const longestFirst = values => [...values].sort((a, b) => b.length - a.length);

function replaceMap(text, map, { flags = "gu", boundaries = false } = {}) {
  const keys = longestFirst(Object.keys(map));
  if (!keys.length) return text;
  const pattern = keys.map(escapeRegex).join("|");
  const expression = boundaries
    ? new RegExp("(^|[^\\p{L}\\p{N}_])(" + pattern + ")(?![\\p{L}\\p{N}_])", flags)
    : new RegExp(pattern, flags);
  return text.replace(expression, (...args) => {
    if (boundaries) return args[1] + map[args[2].toLowerCase()];
    return map[args[0]];
  });
}

function numberGroupToThai(value, digits) {
  let remaining = Number(value);
  if (!remaining) return "";
  const parts = [];
  for (const place of [100000, 10000, 1000, 100, 10, 1]) {
    const digit = Math.floor(remaining / place);
    remaining %= place;
    if (!digit) continue;
    if (place === 1) parts.push(value > 1n && digit === 1 ? "เอ็ด" : digits[String(digit)]);
    else if (place === 10) parts.push(digit === 1 ? "สิบ" : digit === 2 ? "ยี่สิบ" : digits[String(digit)] + "สิบ");
    else if (place === 100) parts.push(digits[String(digit)] + "ร้อย");
    else if (place === 1000) parts.push(digits[String(digit)] + "พัน");
    else if (place === 10000) parts.push(digits[String(digit)] + "หมื่น");
    else if (place === 100000) parts.push(digits[String(digit)] + "แสน");
  }
  return parts.join("");
}

function integerToThai(value, digits) {
  let number = BigInt(value);
  if (number === 0n) return "ศูนย์";
  if (number < 0n) return "ลบ" + integerToThai(-number, digits);
  const parts = [];
  let millionCount = 0;
  while (number > 0n) {
    const group = number % 1000000n;
    number /= 1000000n;
    if (group > 0n) parts.push(numberGroupToThai(group, digits) + "ล้าน".repeat(millionCount));
    millionCount += 1;
  }
  return parts.reverse().join("");
}

function decimalToThai(value, digits) {
  if (value.includes(".")) {
    const [integerPart, decimalPart] = value.split(".", 2);
    return integerToThai(integerPart || "0", digits) + "จุด" +
      [...decimalPart].map(char => digits[char]).join("");
  }
  return integerToThai(value, digits);
}

function digitsToThai(value, digits) {
  return [...value].map(char => digits[char]).join("");
}

function emailToThai(value, data) {
  const separators = { "@": " แอท ", ".": " ดอท ", "-": " ขีด ", "_": " ขีดล่าง " };
  const output = [];
  let token = "";
  const flush = () => {
    if (!token) return;
    const known = data.EMAIL_WORDS[token.toLowerCase()];
    output.push(known || [...token].map(char =>
      /[0-9]/u.test(char) ? data.THAI_DIGITS[char] : data.LETTER_TO_THAI[char.toUpperCase()] || char
    ).join(""));
    token = "";
  };
  for (const char of value) {
    if (Object.hasOwn(separators, char)) {
      flush();
      output.push(separators[char]);
    } else token += char;
  }
  flush();
  return output.join("");
}

function expandMaiyamok(text, wordTokenize) {
  if (!text.includes("ๆ")) return text;
  if (typeof wordTokenize !== "function") {
    throw new Error("Maiyamok expansion requires the pinned Thai word tokenizer");
  }
  const sourceTokens = wordTokenize(text);
  if (!Array.isArray(sourceTokens)) throw new Error("wordTokenize must return an array");
  const tokens = [];
  for (const token of sourceTokens) tokens.push(...String(token).split(/(ๆ)/u).filter(Boolean));
  const output = [];
  let repeatCount = 0;
  for (const token of tokens.reverse()) {
    if (token === "ๆ") repeatCount += 1;
    else if (repeatCount === 0) output.push(token);
    else if (!/^\s+$/u.test(token)) {
      output.push(...Array(repeatCount + 1).fill(token));
      repeatCount = 0;
    }
  }
  return output.reverse().join("");
}

export function normalizeFastThaiG2PText(sourceText, { data, wordTokenize } = {}) {
  if (typeof sourceText !== "string") throw new TypeError("Thai text must be a string");
  if (!data || data.schema_version !== 1 || !data.THAI_DIGITS || !data.ABBREVIATIONS) {
    throw new TypeError("Pinned FastThaiG2P normalizer data is required");
  }
  const digits = data.THAI_DIGITS;
  let text = expandMaiyamok(sourceText, wordTokenize);

  for (const [thai, arabic] of Object.entries(data.THAI_NUMERAL_MAP)) {
    text = text.replaceAll(thai, arabic);
  }

  text = text.replace(/[A-Za-z0-9._-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/gu, match => emailToThai(match, data));
  text = replaceMap(text, data.ENGLISH_ABBREVS, { flags: "giu", boundaries: true });

  const unitKeys = longestFirst(Object.keys(data.UNITS)).map(escapeRegex).join("|");
  text = text.replace(new RegExp("(?<=[0-9])\\s*(" + unitKeys + ")", "gu"), (_match, unit) => data.UNITS[unit]);
  text = replaceMap(text, data.SYMBOLS);

  text = text.replace(
    /(?<![\p{L}\p{N}_])([0-9]{1,2}):([0-9]{2})(?:\s*(?:นาฬิกา|น\.))?/gu,
    (_match, hours, minutes) => {
      const result = integerToThai(hours, digits) + "นาฬิกา";
      return Number(minutes) ? result + integerToThai(minutes, digits) + "นาที" : result;
    }
  );

  text = text.replace(/[0-9]{2,4}[-.][0-9]{3,4}[-.][0-9]{3,4}/gu, match =>
    match.split(/[-.]/u).map(part => digitsToThai(part, digits)).join(" ")
  );

  text = text.replace(
    /[A-Za-z]+-?[0-9]+[-0-9A-Za-z]*|[0-9]+-?[A-Za-z]+[-0-9A-Za-z]*/gu,
    match => [...match].map(char => {
      if (/[0-9]/u.test(char)) return digits[char];
      if (char === "-") return " ";
      return data.LETTER_TO_THAI[char.toUpperCase()] || char;
    }).join("")
  );

  text = text.replace(/-?[0-9]{1,3}(?:,[0-9]{3})+(?:\.[0-9]+)?/gu, match =>
    decimalToThai(match.replaceAll(",", ""), digits)
  );

  text = text.replace(/-?[0-9]+(?:\.[0-9]+)?/gu, match => {
    const raw = match.replace(/^-/, "");
    const negative = match.startsWith("-");
    const integerPart = raw.split(".", 1)[0];
    let result;
    if (integerPart.length >= 7) {
      if (raw.includes(".")) {
        const [intPart, decPart] = raw.split(".", 2);
        result = digitsToThai(intPart, digits) + "จุด" + digitsToThai(decPart, digits);
      } else result = digitsToThai(integerPart, digits);
      if (negative) result = "ลบ" + result;
      return result;
    }
    return decimalToThai(match, digits);
  });

  text = replaceMap(text, data.ABBREVIATIONS);
  text = text.replace(/[A-Za-z]+/gu, match =>
    [...match].map(char => data.LETTER_TO_THAI[char.toUpperCase()]).join("")
  );
  return text.replaceAll("-", " ");
}
