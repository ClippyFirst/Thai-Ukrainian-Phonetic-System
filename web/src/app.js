const esc = value => String(value ?? '').replace(/[&<>"']/g, char => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
}[char]));

const input = document.getElementById('thai-input');
const output = document.getElementById('results');
const status = document.getElementById('status');
const analyzeButton = document.getElementById('analyze');

function copyButton(label, value) {
  return '<button class="copy" type="button" data-copy="' + esc(value) +
    '" aria-label="Копіювати: ' + esc(label) + '">Копіювати</button>';
}

function renderSyllable(syllable) {
  const warnings = (syllable.warnings || []).map(warning =>
    '<p class="warning">' + esc(warning) + '</p>'
  ).join('');
  const toneNames = { mid: 'середній', low: 'низький', falling: 'низхідний', high: 'високий', rising: 'висхідний' };
  const lengthNames = { short: 'короткий', long: 'довгий' };
  const tone = syllable.tone && syllable.tone_ipa
    ? esc(toneNames[syllable.tone] || syllable.tone) + ' · <span lang="und-fonipa">' + esc(syllable.tone_ipa) + '</span>'
    : 'Не визначено';
  return '<section class="syllable-result">' +
    '<div class="result-title">IPA: <span class="ipa-output" lang="und-fonipa">' +
      esc(syllable.raw_ipa) + '</span></div>' +
    '<div class="data-grid">' +
      '<div class="data"><span class="label">Сегментна IPA</span><div class="value ipa-output" lang="und-fonipa">' +
        esc(syllable.ipa || '—') + '</div>' + (syllable.ipa ? copyButton('IPA', syllable.ipa) : '') + '</div>' +
      '<div class="data"><span class="label">Український кандидат · попередній</span><div class="value">' +
        esc(syllable.ukrainian || '—') + '</div>' + (syllable.ukrainian ? copyButton('український запис', syllable.ukrainian) : '') + '</div>' +
      '<div class="data"><span class="label">Тон</span><div class="value">' + tone + '</div></div>' +
      '<div class="data"><span class="label">Довгота голосного</span><div class="value">' +
        esc(lengthNames[syllable.vowel_length] || syllable.vowel_length || 'Не визначено') + '</div></div>' +
    '</div>' + warnings + '</section>';
}

function renderResult(result) {
  const words = (result.words || []).map((word, index) =>
    '<article class="result-card"><h3 class="result-title">Слово ' + (index + 1) + (word.thai ? ' · <span lang="th">' + esc(word.thai) + '</span>' : '') + '</h3>' +
    '<div class="value ipa-output" lang="und-fonipa">' + esc(word.fastthaig2p_ipa) + '</div>' +
    '<div class="value">' + esc(word.ukrainian) + '</div>' +
    (word.syllables || []).map(renderSyllable).join('') + '</article>'
  ).join('');
  const warnings = (result.warnings || []).map(warning =>
    '<p class="continuous-output-notice" role="note">' + esc(warning) + '</p>'
  ).join('');
  output.innerHTML = '<h2 class="results-heading">Попередній результат FastThaiG2P</h2>' +
    '<p class="continuous-output-notice" role="note"><strong>Не експертно підтверджено.</strong> ' +
    'Український запис — практична адаптація зовнішньої IPA; перевіряйте важливі слова.</p>' +
    warnings +
    '<section class="continuous-output ua-continuous"><div class="continuous-output-head"><h3>Українськими літерами</h3>' +
    copyButton('український запис', result.ukrainian) + '</div><pre class="continuous-output-value">' +
    esc(result.ukrainian) + '</pre></section>' +
    '<section class="continuous-output ipa-continuous"><div class="continuous-output-head"><h3>IPA FastThaiG2P</h3>' +
    copyButton('IPA', result.raw_ipa) + '</div><pre class="continuous-output-value ipa-output" lang="und-fonipa">' +
    esc(result.raw_ipa) + '</pre></section>' +
    '<details class="analysis-details"><summary>Показати складовий розбір і походження</summary>' +
    '<p>Рушій: <strong>' + esc(result.engine) + '</strong>; upstream commit: <code>' +
    esc(result.upstream_commit) + '</code>.</p>' + words + '</details>';
  output.hidden = false;
  output.querySelectorAll('[data-copy]').forEach(button => button.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(button.dataset.copy);
      const previous = button.textContent;
      button.textContent = 'Скопійовано';
      window.setTimeout(() => { button.textContent = previous; }, 1200);
    } catch {
      button.textContent = 'Не вдалося скопіювати';
    }
  }));
}

async function run() {
  const text = input.value;
  if (!text.trim()) {
    status.className = 'status error';
    status.textContent = 'Введіть тайський текст.';
    output.hidden = true;
    output.innerHTML = '';
    return;
  }

  analyzeButton.disabled = true;
  status.className = 'status';
  status.textContent = 'FastThaiG2P аналізує текст…';
  output.hidden = true;
  try {
    const response = await fetch('/api/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });
    const payload = await response.json();
    if (!response.ok) {
      const detail = payload.detail;
      throw new Error(typeof detail === 'string' ? detail : detail?.message || 'Не вдалося обробити текст.');
    }
    renderResult(payload);
    status.className = 'status notice';
    status.textContent = 'Готово. Український запис попередній і потребує перевірки.';
  } catch (error) {
    status.className = 'status error';
    status.textContent = error instanceof Error ? error.message : 'Помилка API FastThaiG2P.';
    output.hidden = true;
    output.innerHTML = '';
  } finally {
    analyzeButton.disabled = false;
  }
}

document.querySelectorAll('[data-example]').forEach(button => button.addEventListener('click', () => {
  input.value = button.dataset.example;
  input.focus();
  return run();
}));

document.getElementById('clear').addEventListener('click', () => {
  input.value = '';
  output.hidden = true;
  output.innerHTML = '';
  status.className = 'status';
  status.textContent = '';
  input.focus();
});

analyzeButton.addEventListener('click', run);
input.addEventListener('keydown', event => {
  if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
    event.preventDefault();
    return run();
  }
});
