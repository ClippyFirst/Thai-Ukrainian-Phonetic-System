/**
 * Browser-native port of PyThaiNLP 5.4.0 newmm segmentation used by
 * FastThaiG2P's Tokenizer. The custom dictionary is the exact filtered
 * FastThaiG2P IPA-key set. Algorithm source: PyThaiNLP, Apache-2.0.
 */
const MAX_GRAPH_SIZE = 50;
const PAT_THAI_TWOCHARS = /^[ก-ฮ]{0,2}$/u;
const PAT_NONTHAI = new RegExp(
  "^(?:[-a-zA-Z]+|[0-9]+(?:[,\\.][0-9]+)*|[ \\t]+|\\r?\\n|[^\\u0E00-\\u0E7F \\t\\r\\n]+)",
  "u"
);
const TCC_RULES = [
  "เc็ck", "เcctาะk", "เccีtยะk", "เccีtย(?=[เ-ไก-ฮ]|$)k",
  "เcc็ck", "เcิc์ck", "เcิtck", "เcีtยะ?k", "เcืtอะ?k",
  "เc[ิีุู]tย(?=[เ-ไก-ฮ]|$)k", "เctา?ะ?k", "cัtวะk",
  "c[ัื]tc[ุิะ]?k", "c[ิุู]์", "c[ะ-ู]tk", "cรรc์", "c็",
  "ct[ะาำ]?k", "ck", "แc็c", "แcc์", "แctะ", "แcc็c",
  "แccc์", "โctะ", "[เ-ไ]ct", "ก็", "อึ", "หึ"
].map(rule =>
  rule
    .replaceAll("k", "(cc?[dิ]?[์])?")
    .replaceAll("c", "[ก-ฮ]")
    .replaceAll("t", "[่-๋]?")
    .replaceAll("d", "ูุ")
);
const PAT_TCC = new RegExp("^(?:" + TCC_RULES.join("|") + ")", "u");

function buildTrie(words) {
  const root = { children: new Map(), end: false };
  let count = 0;
  for (const word of new Set(words)) {
    if (typeof word !== "string" || !word) continue;
    let node = root;
    for (const char of Array.from(word)) {
      if (!node.children.has(char)) node.children.set(char, { children: new Map(), end: false });
      node = node.children.get(char);
    }
    if (!node.end) {
      node.end = true;
      count += 1;
    }
  }
  return { root, count };
}

function prefixes(trie, chars, start) {
  const result = [];
  let node = trie.root;
  for (let index = start; index < chars.length; index += 1) {
    node = node.children.get(chars[index]);
    if (!node) break;
    if (node.end) result.push(chars.slice(start, index + 1).join(""));
  }
  return result;
}

function tccPositions(chars) {
  const valid = new Uint8Array(chars.length + 1);
  let position = 0;
  while (position < chars.length) {
    const match = PAT_TCC.exec(chars.slice(position).join(""));
    position += match ? Array.from(match[0]).length : 1;
    valid[position] = 1;
  }
  return valid;
}

function nonThaiEnd(chars, begin) {
  const match = PAT_NONTHAI.exec(chars.slice(begin).join(""));
  return match ? begin + Array.from(match[0]).length : null;
}

function bfsPath(graph, start, goal) {
  const visited = new Set([start]);
  const queue = [[start, [start]]];
  let cursor = 0;
  while (cursor < queue.length) {
    const [vertex, path] = queue[cursor++];
    for (const position of graph.get(vertex) || []) {
      if (position === goal) return [...path, position];
      if (!visited.has(position)) {
        visited.add(position);
        queue.push([position, [...path, position]]);
      }
    }
  }
  return null;
}

function extendGraph(graph, positions, chars, begin, valid, trie, graphSize) {
  for (const word of prefixes(trie, chars, begin)) {
    const end = begin + Array.from(word).length;
    if (valid[end]) {
      if (!graph.has(begin)) graph.set(begin, []);
      graph.get(begin).push(end);
      graphSize += 1;
      if (!positions.includes(end)) positions.push(end);
      if (graphSize > MAX_GRAPH_SIZE) break;
    }
  }
  return graphSize;
}

function findSkipEnd(chars, begin, valid, trie) {
  const length = chars.length;
  const nonThai = nonThaiEnd(chars, begin);
  if (nonThai !== null) return nonThai;

  for (let position = begin + 1; position < length; position += 1) {
    if (!valid[position]) continue;
    const words = prefixes(trie, chars, position).filter(word => {
      const end = position + Array.from(word).length;
      return Boolean(valid[end]) && !PAT_THAI_TWOCHARS.test(word);
    });
    if (words.length) return position;
    if (nonThaiEnd(chars, position) !== null) return position;
  }
  return length;
}

function onecut(chars, trie) {
  if (!chars.length) return [];
  const graph = new Map();
  let graphSize = 0;
  const valid = tccPositions(chars);
  const positions = [0];
  let endPosition = 0;
  const output = [];

  while (positions.length) {
    positions.sort((a, b) => a - b);
    if (positions[0] >= chars.length) break;
    const begin = positions.shift();
    graphSize = extendGraph(graph, positions, chars, begin, valid, trie, graphSize);

    if (positions.length === 1) {
      const path = bfsPath(graph, endPosition, positions[0]);
      if (!path) throw new Error("newmm graph lost a reachable path");
      graphSize = 0;
      graph.clear();
      for (const position of path.slice(1)) {
        output.push(chars.slice(endPosition, position).join(""));
        endPosition = position;
      }
    } else if (positions.length === 0) {
      endPosition = findSkipEnd(chars, begin, valid, trie);
      graphSize = 0;
      graph.clear();
      output.push(chars.slice(begin, endPosition).join(""));
      positions.push(endPosition);
    }
  }
  return output;
}

function codePointLength(value) {
  return Array.from(value).length;
}

function rejoinFormattedNumbers(segments) {
  const original = segments.join("");
  const matches = [...original.matchAll(/([0-9]+[.,:])+[0-9]+/gu)].map(match => {
    const start = codePointLength(original.slice(0, match.index));
    return { start, end: start + codePointLength(match[0]) };
  });
  if (!matches.length) return segments;

  const output = [];
  let position = 0;
  let segmentIndex = 0;
  let matchIndex = 0;
  while (segmentIndex < segments.length && matchIndex < matches.length) {
    const match = matches[matchIndex];
    const token = segments[segmentIndex];
    if (position >= match.start) {
      let connected = "";
      while (position < match.end && segmentIndex < segments.length) {
        connected += segments[segmentIndex];
        position += codePointLength(segments[segmentIndex]);
        segmentIndex += 1;
      }
      if (connected) output.push(connected);
      matchIndex += 1;
    } else {
      output.push(token);
      segmentIndex += 1;
      position += codePointLength(token);
    }
  }
  output.push(...segments.slice(segmentIndex));
  return output;
}

export function createFastThaiG2PNativeTokenizer(dictionaryWords) {
  if (!Array.isArray(dictionaryWords) || !dictionaryWords.length) {
    throw new TypeError("The filtered FastThaiG2P tokenizer dictionary is required");
  }
  const trie = buildTrie(dictionaryWords);
  return Object.freeze({
    dictionarySize: trie.count,
    tokenize(text) {
      if (typeof text !== "string" || !text) return [];
      return rejoinFormattedNumbers(onecut(Array.from(text), trie));
    }
  });
}
