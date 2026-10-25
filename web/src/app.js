import { analyzeText } from './engine.js';

const esc = value => String(value ?? '').replace(/[&<>"']/g, char => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
}[char]));

const input = document.getElementById('thai-input');
const out = document.getElementById('results');
const status = document.getElementById('status');

const statusLabel = {
  analyzed: 'Проаналізовано',
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
  const ok = analysis.status === 'analyzed';
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

  const unresolved = token.segmentationStatus !== 'lexicon' ||
    (token.syllables || []).some(syllable => syllable.status !== 'analyzed');
  const syllables = (token.syllables || []).map((analysis, syllableIndex) =>
    renderSyllable(analysis, index, syllableIndex)
  ).join('');
  const warnings = (token.warnings || []).map(warning =>
    '<div class="warning">' + esc(warning) + '</div>'
  ).join('');
  return '<article class="result-card" aria-labelledby="' + headingId + '">' +
    '<div class="result-top"><div><h3 class="result-title" id="' + headingId + '">Результат ' +
    (index + 1) + ': ' + esc(token.input) + '</h3><div class="thai" lang="th">' +
    esc(token.input) + '</div><div class="subline">Сегментація: ' +
    esc(token.segmentationStatus) + '</div></div><span class="badge ' +
    (unresolved ? 'warn' : 'ok') + '">' + esc(token.segmentationStatus) +
    '</span></div>' + syllables + warnings + '</article>';
}

function bindCopyButtons() {
  out.querySelectorAll('[data-copy]').forEach(button => button.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(button.dataset.copy);
      const previous = button.textContent;
      button.textContent = 'Скопійовано';
      button.setAttribute('aria-label', 'Скопійовано');
      setTimeout(() => {
        button.textContent = previous;
        button.removeAttribute('aria-label');
      }, 900);
    } catch {
      button.textContent = 'Не вдалося скопіювати';
    }
  }));
}

function run() {
  const text = input.value.trim();
  if (!text) {
    status.className = 'status error';
    status.textContent = 'Введіть тайський текст.';
    out.hidden = true;
    out.innerHTML = '';
    return;
  }

  const tokens = analyzeText(text);
  const thaiTokens = tokens.filter(token => token.kind === 'thai');
  const unresolvedCount = thaiTokens.length === 0 ? 1 : thaiTokens.filter(token =>
    token.segmentationStatus !== 'lexicon' ||
    (token.syllables || []).some(syllable => syllable.status !== 'analyzed')
  ).length;
  status.className = unresolvedCount ? 'status notice' : 'status';
  status.textContent = thaiTokens.length === 0
    ? 'Тайських токенів не знайдено; нетайський текст збережено без фонетичної інтерпретації.'
    : unresolvedCount
      ? 'Проаналізовано ' + tokens.length + ' токен(ів), тайських: ' + thaiTokens.length +
        '; ' + unresolvedCount + ' тайських токен(ів) потребують додаткової перевірки або не мають детермінованого результату.'
      : 'Проаналізовано ' + tokens.length + ' токен(ів), тайських: ' + thaiTokens.length +
        '. Це аналіз написання, а не переклад.';
  out.innerHTML = '<h2 class="results-heading">Результати аналізу</h2>' + tokens.map(card).join('');
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
input.addEventListener('keydown', event => {
  if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
    event.preventDefault();
    run();
  }
});
