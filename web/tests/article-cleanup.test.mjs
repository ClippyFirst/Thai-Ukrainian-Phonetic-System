import assert from "node:assert/strict";
import { preprocessArticleText } from "../src/article-cleanup.js";

const source = '**ยูเครน** ([อังกฤษ](https://th.wikipedia.org/wiki/ภาษาอังกฤษ "ภาษาอังกฤษ"): *Ukraine*; [ยูเครน](https://th.wikipedia.org/wiki/ภาษายูเครน "ภาษายูเครน"): Украї́на, ออกเสียง: [[ʊkrɐˈjinɐ]](https://en.wikipedia.org/wiki/Help:IPA/Ukrainian "en:Help:IPA/Ukrainian") [ⓘ](https://th.wikipedia.org/wiki/file.oga "title")) เป็นประเทศหนึ่ง [\\[a\\]](https://example.org/note) &#x20;';

const cleaned = preprocessArticleText(source);
assert.equal(cleaned.changed, true);
assert.match(cleaned.text, /ยูเครน/);
assert.match(cleaned.text, /อังกฤษ: Ukraine/);
assert.match(cleaned.text, /Украї́на/);
assert.match(cleaned.text, /\[ʊkrɐˈjinɐ\]/);
assert.match(cleaned.text, /เป็นประเทศหนึ่ง/);
assert.doesNotMatch(cleaned.text, /wikipedia\.org|example\.org|\\\[a\\\]|\[a\]|&#x20;|ⓘ/i);

const html = preprocessArticleText('ข้อความ<ref name="x">แหล่งอ้างอิง</ref> ต่อ');
assert.doesNotMatch(html.text, /<ref|แหล่งอ้างอิง/);
assert.match(html.text, /ข้อความ/);
assert.match(html.text, /ต่อ/);

const plain = "  กินข้าวกับไข่และผลไม้  \\n";
const untouched = preprocessArticleText(plain);
assert.deepEqual(untouched, { text: plain, changed: false });

console.log("Article cleanup contract passed.");
