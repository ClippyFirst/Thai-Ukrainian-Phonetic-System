import { analyzeText } from './engine.js';
import { preprocessArticleText } from './article-cleanup.js';
import { renderRtgsTokens } from './rtgs-reference.js';

const esc = value => String(value ?? '').replace(/[&<>"']/g, char => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
}[char]));

const input = document.getElementById('thai-input');
const out = document.getElementById('results');
const status = document.getElementById('status');
const modeInput = document.getElementById('engine-mode');
const modeHint = document.getElementById('mode-hint');

function updateModeHint() {
  if (!modeHint) return;
  const hints = {
    strict: 'Строгий режим: невідомі фрагменти залишаються невизначеними замість вгадування.',
    soft: 'М’який режим: можливі структурні припущення; читання й межі слів потребують перевірки.',
    'super-soft': 'Суперм’який режим: невідомі фрагменти отримують приблизний кандидат, який може бути помилковим.'
  };
  modeHint.textContent = hints[modeInput?.value] || hints.strict;
}

const statusLabel = {
  analyzed: 'Проаналізовано',
  'approximate:orthographic-fallback': 'Приблизний резервний результат',
  'analysis-dependent:special-orthography': 'Потрібна лексична перевірка',
  'analysis-dependent:vowel-length': 'Потрібна лексична перевірка',
  'unresolved:unsupported-symbol': 'Невизначений вхід',
  'unresolved:multiple-tone-marks': 'Невизначений вхід',
  'unresolved:unresolved-vowel': 'Невизначений вхід',
  'unresolved:no-onset': 'Невизначений вхід',
  'unresolved:empty-onset-after-vowel-analysis': 'Невизначений вхід',
  'unresolved:nonconforming-consonant-sequence': 'Потрібна сегментація',
  'invalid:coda-not-licensed': 'Неприпустимий склад',
  'invalid:tone-combination': 'Неприпустима тонова комбінація'
};

function copyButton(label, value) {
  if (!value) return '';
  return '<button class="copy" type="button" data-copy="' + esc(value) +
    '" aria-label="Копіювати: ' + esc(label) + '">Копіювати</button>';
}

function renderField(label, value, isIpa = false) {
  const present = value !== null && value !== undefined && value !== '' && value !== '—';
  const shown = present ? value : '—';
  return '<div class="data"><span class="label">' + esc(label) +
    '</span><div class="value' + (isIpa ? ' ipa-output' : '') + '"' +
    (isIpa ? ' lang="und-fonipa"' : '') + '>' + esc(shown) + '</div>' +
    (present ? copyButton(label, value) : '') + '</div>';
}

function renderSyllable(analysis, tokenIndex, syllableIndex) {
  const ok = analysis.status === 'analyzed' || analysis.status === 'approximate:orthographic-fallback';
  const headingId = 'syllable-' + tokenIndex + '-' + syllableIndex;
  const warnings = (analysis.warnings || []).map(warning =>
    '<div class="warning">' + esc(warning) + '</div>'
  ).join('');
  const fields = [
    ['ФОНОЛОГІЧНА IPA', analysis.phonemicIpa, true],
    ['ПОВЕРХНЕВА IPA', analysis.phoneticIpa, true],
    ['ТОН', analysis.tone && analysis.toneIpa ? analysis.tone + ' · ' + analysis.toneIpa : '—', false],
    ['УКРАЇНСЬКИЙ ПРАКТИЧНИЙ КАНДИДАТ', analysis.ukrainian || '—', false]
  ];
  const data = fields.map(([label, value, isIpa]) => renderField(label, value, isIpa)).join('');
  const explanation = '<div class="result-explanation"><strong>' +
    esc(statusLabel[analysis.status] || 'Статус аналізу') + '</strong>' +
    (warnings || '<p>Для цього складу немає детермінованого фонетичного результату.</p>') + '</div>';
  const adaptation = analysis.ukrainianAdaptation
    ? '<div class="adaptation-audit"><div class="label">АУДИТ IPA → УКРАЇНСЬКА</div><p>Застосовані правила: ' +
      esc((analysis.ukrainianAdaptation.rulesApplied || []).join(', ') || '—') +
      '</p><p>Нейтралізовані ознаки: ' +
      esc((analysis.ukrainianAdaptation.neutralizedFeatures || []).join('; ') || '—') +
      '</p></div>'
    : '';
  return '<section class="syllable-result" aria-labelledby="' + headingId + '">' +
    '<h4 class="result-title" id="' + headingId + '">Склад: ' + esc(analysis.input) + '</h4>' +
    '<div class="subline">' + esc(statusLabel[analysis.status] || analysis.status) +
    ' · <code>' + esc(analysis.status) + '</code></div>' +
    (ok ? '<div class="data-grid">' + data + '</div>' + adaptation + warnings : explanation) +
    '</section>';
}

function card(token, index) {
  const headingId = 'result-' + index;
  if (token.kind !== 'thai') {
    return '<article class="result-card" aria-labelledby="' + headingId + '">' +
      '<div class="result-top"><div><h3 class="result-title" id="' + headingId + '">Токен ' +
      (index + 1) + ': ' + esc(token.kind) + '</h3><div class="thai">' + esc(token.input) +
      '</div><div class="subline">Збережено без фонетичної інтерпретації</div></div></div></article>';
  }

  const unresolved = !['lexicon', 'lexical_ipa_override', 'soft-orthographic-clusters'].includes(token.segmentationStatus) ||
    (token.syllables || []).some(syllable => syllable.status !== 'analyzed');
  const syllables = (token.syllables || []).map((analysis, syllableIndex) =>
    renderSyllable(analysis, index, syllableIndex)
  ).join('');
  const warnings = (token.warnings || []).map(warning =>
    '<div class="warning">' + esc(warning) + '</div>'
  ).join('');
  const tokenStatusLabel = {
    lexicon: 'Словниковий запис',
    lexical_ipa_override: 'Словникове читання з IPA',
    'soft-orthographic-clusters': 'Попередній структурний розбір',
    'super-soft-approximate': 'Приблизне резервне читання'
  }[token.segmentationStatus] ||
    (token.segmentationStatus.startsWith('analysis-dependent:')
      ? 'Потрібне лексичне або контекстне рішення'
      : token.segmentationStatus.startsWith('unresolved:')
        ? 'Розбір не встановлено'
        : token.segmentationStatus.startsWith('invalid:')
          ? 'Комбінація не підтримується моделлю'
          : 'Потребує перевірки');
  return '<article class="result-card" aria-labelledby="' + headingId + '">' +
    '<div class="result-top"><div><h3 class="result-title" id="' + headingId + '">Результат ' +
    (index + 1) + ': ' + esc(token.input) + '</h3><div class="thai" lang="th">' +
    esc(token.input) + '</div><div class="subline">Статус: ' + esc(tokenStatusLabel) +
    ' · технічний код: <code>' + esc(token.segmentationStatus) +
    '</code></div></div><span class="badge ' +
    (unresolved ? 'warn' : 'ok') + '">' + esc(tokenStatusLabel) +
    '</span></div>' + syllables + warnings + '</article>';
}


// Explicit project-defined word grouping for the curated phrase; other entries
// retain their source lexicon contract and are never split by guessed boundaries.
const REVIEWED_WORD_GROUPS = new Map([['กินข้าวกับไข่และผลไม้', [1, 1, 1, 1, 1, 2]]]);

function continuousToken(token, mode) {
  if (token.kind !== 'thai') return token.input;
  const known = ['lexicon', 'lexical_ipa_override', 'soft-orthographic-clusters', 'super-soft-approximate'].includes(token.segmentationStatus);
  if (!known || !(token.syllables || []).length) return mode === 'ua'
    ? '⟦НЕВИЗНАЧЕНО: ' + token.input + '⟧'
    : '⟦UNRESOLVED: ' + token.input + '⟧';
  if (mode === 'ua') {
    const renderSyllable = s => ['analyzed', 'approximate:orthographic-fallback'].includes(s.status) && s.ukrainian
      ? s.ukrainian : (token.segmentationStatus === 'super-soft-approximate' ? 'а' : '⟦НЕВИЗНАЧЕНО: ' + s.input + '⟧');
    const groups = REVIEWED_WORD_GROUPS.get(token.input);
    if (!groups) return token.syllables.map(renderSyllable).join('');
    let offset = 0;
    const words = groups.map(size => {
      const word = token.syllables.slice(offset, offset + size).map(renderSyllable).join('');
      offset += size;
      return word;
    });
    return offset === token.syllables.length ? words.join(' ') : token.syllables.map(renderSyllable).join('');
  }
  return token.syllables.map(s =>
    ['analyzed', 'approximate:orthographic-fallback'].includes(s.status) && s.phonemicIpa ? s.phonemicIpa + (s.toneIpa || '') : (token.segmentationStatus === 'super-soft-approximate' ? 'a' : '⟦UNRESOLVED: ' + s.input + '⟧')
  ).join(' ');
}

function assembleOutput(source, tokens, mode) {
  let cursor = 0, result = '', previous = null;
  for (const token of tokens) {
    const start = source.indexOf(token.input, cursor);
    if (start < 0) { result += continuousToken(token, mode); continue; }
    const gap = source.slice(cursor, start);
    result += gap;
    if (!gap && previous && previous.kind === 'thai' && token.kind === 'thai') result += ' ';
    result += continuousToken(token, mode);
    cursor = start + token.input.length;
    previous = token;
  }
  return result + source.slice(cursor);
}

function continuousPanel(title, value, hint, extraClass = '') {
  return '<section class="continuous-output ' + extraClass + '"><div class="continuous-output-head"><div><h3>' +
    esc(title) + '</h3><p>' + esc(hint) + '</p></div>' + copyButton(title, value) +
    '</div><pre class="continuous-output-value">' + esc(value) + '</pre></section>';
}

async function copyText(value) {
  if (globalThis.navigator?.clipboard?.writeText) {
    try {
      await globalThis.navigator.clipboard.writeText(value);
      return;
    } catch {
      // Fall through to the local selection-based fallback when clipboard
      // permissions are denied or unavailable.
    }
  }
  if (!document.createElement || !document.body || !document.execCommand) {
    throw new Error('Clipboard API is unavailable');
  }
  const fallback = document.createElement('textarea');
  fallback.value = value;
  fallback.setAttribute('readonly', '');
  fallback.setAttribute('aria-hidden', 'true');
  fallback.style.position = 'fixed';
  fallback.style.opacity = '0';
  fallback.style.pointerEvents = 'none';
  document.body.appendChild(fallback);
  fallback.select();
  const copied = document.execCommand('copy');
  fallback.remove();
  if (!copied) throw new Error('Copy command was rejected');
}

function bindCopyButtons() {
  out.querySelectorAll('[data-copy]').forEach(button => button.addEventListener('click', async () => {
    const previous = button.textContent;
    const previousLabel = button.getAttribute('aria-label');
    try {
      await copyText(button.dataset.copy);
      button.textContent = 'Скопійовано';
      button.setAttribute('aria-label', 'Скопійовано');
      button.setAttribute('aria-live', 'polite');
      setTimeout(() => {
        button.textContent = previous;
        if (previousLabel) button.setAttribute('aria-label', previousLabel);
        else button.removeAttribute('aria-label');
        button.removeAttribute('aria-live');
      }, 1400);
    } catch {
      button.textContent = 'Не вдалося скопіювати';
      button.setAttribute('aria-live', 'polite');
      setTimeout(() => {
        button.textContent = previous;
        if (previousLabel) button.setAttribute('aria-label', previousLabel);
        else button.removeAttribute('aria-label');
        button.removeAttribute('aria-live');
      }, 2200);
    }
  }));
}

function run() {
  const text = input.value;
  if (!text.trim()) {
    status.className = 'status error';
    status.textContent = 'Введіть тайський текст.';
    out.hidden = true;
    out.innerHTML = '';
    return;
  }

  const mode = ['soft', 'super-soft'].includes(modeInput?.value) ? modeInput.value : 'strict';
  const prepared = preprocessArticleText(text);
  const analysisText = prepared.text;
  const tokens = analyzeText(analysisText, { mode });
  const thaiTokens = tokens.filter(token => token.kind === 'thai');
  const unresolvedCount = thaiTokens.length === 0 ? 1 : thaiTokens.filter(token =>
    !['lexicon', 'lexical_ipa_override', ...(mode === 'soft' ? ['soft-orthographic-clusters'] : []), ...(mode === 'super-soft' ? ['soft-orthographic-clusters', 'super-soft-approximate'] : [])].includes(token.segmentationStatus) ||
    (token.syllables || []).some(syllable => syllable.status !== 'analyzed')
  ).length;
  status.className = unresolvedCount || mode === 'soft' || mode === 'super-soft' ? 'status notice' : 'status';
  status.textContent = thaiTokens.length === 0
    ? 'Тайських токенів не знайдено; нетайський текст збережено без фонетичної інтерпретації.'
    : unresolvedCount
      ? 'Режим «' + (mode === 'super-soft' ? 'Суперм’який' : mode === 'soft' ? 'М’який' : 'Строгий') + '». Проаналізовано ' + tokens.length + ' токен(ів), тайських: ' + thaiTokens.length +
        '; ' + unresolvedCount + (mode === 'super-soft' ? ' фрагмент(ів) мають приблизне читання або потребують перевірки.' : ' фрагмент(ів) потребують перевірки або залишилися невизначеними.')
      : 'Режим «' + (mode === 'super-soft' ? 'Суперм’який' : mode === 'soft' ? 'М’який' : 'Строгий') + '». Проаналізовано ' + tokens.length + ' токен(ів), тайських: ' + thaiTokens.length +
        '. Це фонетичний кандидат, а не переклад.';
  const uaOutput = assembleOutput(analysisText, tokens, 'ua');
  const ipaOutput = assembleOutput(analysisText, tokens, 'ipa');
  const rtgsOutput = renderRtgsTokens(tokens);
  const unresolved = (uaOutput.match(/⟦НЕВИЗНАЧЕНО:/g) || []).length;
  const notice = thaiTokens.length === 0
    ? '<p class="continuous-output-notice" role="note">Тайського тексту для фонетичного перетворення не знайдено; нетайські фрагменти збережено без інтерпретації.</p>'
    : mode === 'super-soft'
      ? '<p class="continuous-output-notice" role="note"><strong>Суперм’який режим — повне покриття, приблизна вимова.</strong> Український вихід формується для кожного тайського фрагмента. Непідтверджені місця отримують резервну IPA-оцінку, яку обробляє IPA → українська; вона може бути помилковою, а тон і межі слів не гарантовані.</p>'
      : mode === 'soft'
      ? '<p class="continuous-output-notice" role="note"><strong>М’який режим — попередній результат.</strong> Невідомі фрагменти додатково розкладаються на структурно можливі склади. Межі слів і такі читання не підтверджені лексикографічно; невирішені фрагменти позначаються, а не вгадуються.</p>'
      : unresolved
        ? '<p class="continuous-output-notice" role="note">Строгий режим: є ' + unresolved +
          ' невизначених фрагментів. Їх навмисно позначено замість вигадування вимови.</p>'
        : '<p class="continuous-output-notice">Строгий режим: цілісний дослідницький кандидат. Перед використанням перевірте правильність вимови.</p>';
  const cleanupNotice = prepared.changed
    ? '<p class="continuous-output-notice" role="note">Перед аналізом очищено вікі-/Markdown-розмітку: адреси посилань, HTML-теги та службові виноски прибрано; видимі підписи посилань збережено. Аналізується очищений текст, а не початкова розмітка.</p>'
    : '';
  out.innerHTML = '<h2 class="results-heading">Результати · 3 представлення</h2>' + cleanupNotice + notice +
    continuousPanel('01 · RTGS — латинська романізація (не IPA)', rtgsOutput,
      'Довідкова романізація латиницею. Це окреме представлення, не IPA і не джерело українського кандидата. RTGS не позначає тон і не зберігає надійно довготу голосних; ph/th/kh позначають придихові приголосні.', 'rtgs-continuous') +
    continuousPanel('02 · IPA — фонетичне представлення', ipaOutput,
      mode === 'super-soft' ? 'Приблизний IPA для повного покриття; резервні читання не підтверджені.' : mode === 'soft' ? 'Попередній IPA-проміжний результат; перевірте сегментацію та читання.' : 'Фонетична основа, яку використовує адаптація до української графіки.', 'ipa-continuous') +
    continuousPanel('03 · Український фонетичний кандидат', uaOutput,
      mode === 'super-soft' ? 'Повний приблизний український кандидат; неперевірені звукові відповідності можуть бути неточними.' : mode === 'soft' ? 'Попередній український кандидат; неперевірені структурні сегменти можуть бути неточними.' : 'Український запис, адаптований із IPA. Один суцільний текст для читання та копіювання; межі слів відокремлено.', 'ua-continuous') +
    '<details class="analysis-details"><summary>Детальний аналіз сегментів і складів</summary>' +
    tokens.map(card).join('') + '</details>';
  out.hidden = false;
  bindCopyButtons();
}

document.querySelectorAll('[data-example]').forEach(button => button.addEventListener('click', () => {
  input.value = button.dataset.example;
  input.focus();
  run();
}));

document.getElementById('clear').addEventListener('click', () => {
  input.value = '';
  out.hidden = true;
  out.innerHTML = '';
  status.className = 'status';
  status.textContent = '';
  input.focus();
});

document.getElementById('analyze').addEventListener('click', run);
modeInput?.addEventListener('change', updateModeHint);
updateModeHint();
input.addEventListener('keydown', event => {
  if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
    event.preventDefault();
    run();
  }
});

