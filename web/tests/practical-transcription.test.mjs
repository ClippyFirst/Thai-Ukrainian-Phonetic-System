import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const page = readFileSync(new URL('../transcription.html', import.meta.url), 'utf8');
const home = readFileSync(new URL('../index.html', import.meta.url), 'utf8');
const system = readFileSync(new URL('../system.html', import.meta.url), 'utf8');
const styles = readFileSync(new URL('../src/styles.css', import.meta.url), 'utf8');

assert.match(page, /<html lang="uk">/);
assert.match(page, /<main[^>]+id="main-content"/);
assert.match(page, /class="skip-link"/);
assert.match(page, /Практична система/);
assert.match(page, /Тайсько-українська практична транскрипція/);
assert.match(page, /структурний аналіз[\s\S]*типізований IPA/);
assert.match(page, /<table>[\s\S]*<thead>[\s\S]*<th scope="col">/);
assert.equal((page.match(/<table>/g) || []).length, 6);
for (const [ipa, ua] of [['/ja/', 'я'], ['/je/', 'є'], ['/jɛ/', 'є'], ['/ji/', 'ї'], ['/jo/', 'йо'], ['/jɔ/', 'йо'], ['/ju/', 'ю']]) {
  assert.ok(page.includes(ipa) && page.includes(ua), `Missing practical onset mapping ${ipa} → ${ua}`);
}
assert.match(page, /\/[e, ɛ]+\/[\s\S]*«е»/);
assert.match(page, /не є затвердженим національним стандартом|не затверджений національний стандарт/);
assert.match(page, /незалежн/);
assert.match(page, /third-party-notices\.html/);
assert.match(page, /docs\/thai-ukrainian-practical-transcription\.md/);
assert.match(home, /href="transcription\.html"/);
assert.match(system, /href="transcription\.html"/);
assert.match(system, /64\/64/);
assert.doesNotMatch(system, /TLTK OOV-алгоритм ще не портований/);
assert.match(styles, /\.system \.evidence table/);
assert.match(styles, /@media \(max-width: 640px\)/);
console.log('Practical transcription page contract: PASS');
