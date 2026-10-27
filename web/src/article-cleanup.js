const ENTITY_MAP = new Map([
  ["amp", "&"], ["lt", "<"], ["gt", ">"], ["quot", '"'],
  ["apos", "'"], ["nbsp", " "], ["ensp", " "], ["emsp", " "],
  ["thinsp", " "], ["ndash", "–"], ["mdash", "—"], ["hellip", "…"]
]);

function decodeEntity(entity) {
  if (entity[1] === "#") {
    const hex = entity[2]?.toLowerCase() === "x";
    const digits = entity.slice(hex ? 3 : 2, -1);
    const codePoint = Number.parseInt(digits, hex ? 16 : 10);
    if (Number.isInteger(codePoint) && codePoint >= 0 && codePoint <= 0x10ffff &&
        !(codePoint >= 0xd800 && codePoint <= 0xdfff)) {
      return String.fromCodePoint(codePoint);
    }
    return " ";
  }
  return ENTITY_MAP.get(entity.slice(1, -1).toLowerCase()) ?? entity;
}

function replaceMarkdownLinks(source) {
  let output = "";
  let cursor = 0;
  while (cursor < source.length) {
    const open = source.indexOf("[", cursor);
    if (open < 0) return output + source.slice(cursor);
    output += source.slice(cursor, open);
    let close = open + 1;
    let depth = 1;
    for (; close < source.length && depth; close++) {
      if (source[close] === "\\" && close + 1 < source.length) { close++; continue; }
      if (source[close] === "[") depth++;
      if (source[close] === "]") depth--;
    }
    if (depth) {
      output += source.slice(open, open + 1);
      cursor = open + 1;
      continue;
    }
    const labelEnd = close - 1;
    if (source[labelEnd + 1] !== "(") {
      output += source.slice(open, close);
      cursor = close;
      continue;
    }
    let parenDepth = 1;
    let end = labelEnd + 2;
    for (; end < source.length && parenDepth; end++) {
      if (source[end] === "\\" && end + 1 < source.length) { end++; continue; }
      if (source[end] === "(") parenDepth++;
      if (source[end] === ")") parenDepth--;
    }
    if (parenDepth) {
      output += source.slice(open, close);
      cursor = close;
      continue;
    }
    const label = source.slice(open + 1, labelEnd).replace(/\\([\\[\]])/g, "$1");
    output += /^[ⓘ🔗]$/.test(label) ? " " : label;
    cursor = end;
  }
  return output;
}

/**
 * Prepare pasted wiki/Markdown article content while keeping visible link labels.
 * This is deliberately not a general-purpose HTML parser or a translation step.
 */
function preprocessArticleText(input) {
  const original = String(input ?? "");
  const looksMarkedUp = /<ref\b|<[^>]+>|\[[^\]]+\]\([^)]*\)|\[\[|&(?:#(?:x[0-9a-f]+|[0-9]+)|[a-z][a-z0-9]+);|'{2,5}|\*{1,3}[^*]+\*{1,3}/i.test(original);
  if (!looksMarkedUp) return { text: original, changed: false };

  let text = original
    .replace(/<ref\b[^>]*>[\s\S]*?<\/ref\s*>/gi, " ")
    .replace(/<ref\b[^>]*\/>/gi, " ")
    .replace(/<[^>]*>/g, " ")
    .replace(/\[\[([^\]|]+)\|([^\]]+)\]\]/g, "$2")
    .replace(/\[\[([^\]]+)\]\]/g, "$1");
  text = replaceMarkdownLinks(text);
  text = text
    .replace(/\\([\[\]{}|])/g, "$1")
    .replace(/\[(?:[a-z]|[0-9]{1,4})\]/gi, " ")
    .replace(/&(?:#(?:x[0-9a-f]+|[0-9]+)|[a-z][a-z0-9]+);/gi, decodeEntity)
    .replace(/(?:https?:\/\/|www\.)[^\s<>]+/gi, " ")
    .replace(/'{2,5}/g, "")
    .replace(/\*{1,3}([^*\n]+)\*{1,3}/g, "$1")
    .replace(/_{2,}/g, "")
    .replace(/[ \t]+([,.;:!?])/g, "$1")
    .replace(/[ \t]{2,}/g, " ")
    .replace(/[ \t]*\n[ \t]*/g, "\n");
  return { text, changed: text !== original };
}

export { preprocessArticleText };
