import { UI_TEXT, errorMessage } from "./messages.uk.js";

const esc = value => String(value ?? '').replace(/[&<>"']/g, char => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
}[char]));

const input = document.getElementById('thai-input');
const inputCount = document.getElementById('input-count');
const output = document.getElementById('results');
const status = document.getElementById('status');
const analyzeButton = document.getElementById('analyze');
const diagnostics = document.getElementById('technical-diagnostics');
const diagnosticDetails = document.getElementById('diagnostic-details');

let analysisWorker;
let nextRequestId = 1;
const pendingRequests = new Map();

function updateInputCount() {
  inputCount.textContent = 'Знаків: ' + Array.from(input.value).length;
}

function clearDiagnostics() {
  diagnostics.hidden = true;
  diagnosticDetails.textContent = '';
}

function clearPreviousResult() {
  output.hidden = true;
  output.innerHTML = '';
  status.className = 'status';
  status.textContent = '';
  clearDiagnostics();
}

function getAnalysisWorker() {
  if (analysisWorker) return analysisWorker;
  analysisWorker = new Worker(new URL('./fastthaig2p-worker.js', import.meta.url), { type: 'module' });
  analysisWorker.addEventListener('message', event => {
    const message = event.data || {};
    const pending = pendingRequests.get(message.requestId);
    if (!pending) return;
    if (message.type === 'progress') {
      const labels = {
        runtime: UI_TEXT.starting,
        download: UI_TEXT.downloading,
        analysis: UI_TEXT.analyzing
      };
      status.textContent = labels[message.stage] || UI_TEXT.working;
      return;
    }
    pendingRequests.delete(message.requestId);
    if (message.type === 'result') {
      pending.resolve(message.result);
    } else {
      pending.reject({
        code: message.code || 'analysis_failed',
        diagnostic: message.diagnostic || 'Технічну причину не надано.'
      });
    }
  });
  analysisWorker.addEventListener('error', () => {
    const error = {
      code: 'worker_crashed',
      diagnostic: 'Браузер повідомив про аварійне завершення Web Worker.'
    };
    for (const pending of pendingRequests.values()) pending.reject(error);
    pendingRequests.clear();
    analysisWorker?.terminate();
    analysisWorker = undefined;
  });
  return analysisWorker;
}

function analyzeLocally(text) {
  const requestId = nextRequestId++;
  return new Promise((resolve, reject) => {
    pendingRequests.set(requestId, { resolve, reject });
    try {
      getAnalysisWorker().postMessage({ type: 'analyze', requestId, text });
    } catch (error) {
      pendingRequests.delete(requestId);
      reject({
        code: 'worker_crashed',
        diagnostic: String(error?.message || 'Не вдалося передати запит до Web Worker.')
      });
    }
  });
}

function showError(error) {
  const translated = errorMessage(error?.code);
  status.className = 'status error';
  status.textContent = translated.message;
  diagnosticDetails.textContent = [
    `Код повідомлення: ${translated.id}`,
    `Код помилки: ${error?.code || 'unknown'}`,
    `Технічна причина: ${error?.diagnostic || 'Не надано'}`
  ].join('\\n');
  diagnostics.hidden = false;
}

function localizedWarning(warning) {
  const value = String(warning ?? '');
  if (/PROVISIONAL|not independently adjudicated/i.test(value)) {
    return 'Цей результат попередній: IPA не перевірено незалежними фахівцями.';
  }
  if (/unsupported|not supported|unknown/i.test(value)) {
    return 'Для частини звуків немає підтвердженого правила адаптації.';
  }
  if (/fallback|approximate/i.test(value)) {
    return 'Для частини результату використано наближений спосіб; точність не підтверджена.';
  }
  return 'Для цього результату є додаткове застереження. Перегляньте метод і обмеження сервісу.';
}

function copyButton(label, value) {
  return '<button class="copy" type="button" data-copy="' + esc(value) +
    '" aria-label="Копіювати: ' + esc(label) + '">Копіювати</button>';
}

function renderSyllable(syllable) {
  const warnings = (syllable.warnings || []).map(warning =>
    '<p class="warning">' + esc(localizedWarning(warning)) + '</p>'
  ).join('');
  const toneNames = { mid: 'середній', low: 'низький', falling: 'низхідний', high: 'високий', rising: 'висхідний' };
  const lengthNames = { short: 'короткий', long: 'довгий' };
  const tone = syllable.tone && syllable.tone_ipa
    ? esc(toneNames[syllable.tone] || 'Не визначено') + ' · <span lang="und-fonipa">' + esc(syllable.tone_ipa) + '</span>'
    : 'Не визначено';
  return '<section class="syllable-result">' +
    '<h4 class="result-title">IPA: <span class="ipa-output" lang="und-fonipa">' +
      esc(syllable.raw_ipa) + '</span></h4>' +
    '<div class="data-grid">' +
      '<div class="data"><span class="label">Сегментна IPA</span><div class="value ipa-output" lang="und-fonipa">' +
        esc(syllable.ipa || '—') + '</div>' + (syllable.ipa ? copyButton('IPA', syllable.ipa) : '') + '</div>' +
      '<div class="data"><span class="label">Український кандидат · попередній</span><div class="value">' +
        esc(syllable.ukrainian || '—') + '</div>' + (syllable.ukrainian ? copyButton('український запис', syllable.ukrainian) : '') + '</div>' +
      '<div class="data"><span class="label">Тон</span><div class="value">' + tone + '</div></div>' +
      '<div class="data"><span class="label">Довгота голосного</span><div class="value">' +
        esc(lengthNames[syllable.vowel_length] || 'Не визначено') + '</div></div>' +
    '</div>' + warnings + '</section>';
}

function renderResult(result) {
  const words = (result.words || []).map((word, index) =>
    '<article class="word-card"><h3 class="word-heading">Слово ' + (index + 1) + (word.thai ? ' · <span lang="th">' + esc(word.thai) + '</span>' : '') + '</h3>' +
    '<p class="word-ipa ipa-output" lang="und-fonipa">' + esc(word.fastthaig2p_ipa) + '</p>' +
    '<p class="word-ua">' + esc(word.ukrainian) + '</p>' +
    (word.syllables || []).map(renderSyllable).join('') + '</article>'
  ).join('');
  const warnings = (result.warnings || []).map(warning =>
    '<p class="continuous-output-notice" role="note">' + esc(localizedWarning(warning)) + '</p>'
  ).join('');
  output.innerHTML = '<h2 class="results-heading">Попередній результат FastThaiG2P</h2>' +
    '<p class="results-intro">Рушій побудував IPA; український рядок нижче — попередня практична адаптація.</p>' +
    '<p class="continuous-output-notice" role="note"><strong>Не експертно підтверджено.</strong> Перевіряйте важливі слова за надійним словником або з носієм мови.</p>' +
    warnings +
    '<div class="result-feature-grid">' +
      '<section class="continuous-output ua-continuous" aria-labelledby="result-ua-heading"><div class="continuous-output-head"><div><h3 id="result-ua-heading">Українськими літерами</h3><p>Попередній практичний кандидат</p></div>' +
      copyButton('український запис', result.ukrainian) + '</div><pre class="continuous-output-value">' +
      esc(result.ukrainian) + '</pre></section>' +
      '<section class="continuous-output ipa-continuous" aria-labelledby="result-ipa-heading"><div class="continuous-output-head"><div><h3 id="result-ipa-heading">IPA FastThaiG2P</h3><p>Проміжний фонетичний запис рушія</p></div>' +
      copyButton('IPA', result.raw_ipa) + '</div><pre class="continuous-output-value ipa-output" lang="und-fonipa">' +
      esc(result.raw_ipa) + '</pre></section>' +
    '</div>' +
    '<details class="word-breakdown"><summary>Показати складовий розбір і походження</summary>' +
    '<p>Рушій: <strong>' + esc(result.engine) + '</strong>; upstream commit: <code>' +
    esc(result.upstream_commit) + '</code>.</p>' + words + '</details>';
  output.hidden = false;
  output.querySelectorAll('[data-copy]').forEach(button => button.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(button.dataset.copy);
      button.textContent = UI_TEXT.copied;
    } catch {
      status.className = 'status error';
      status.textContent = UI_TEXT.copyFailed;
    }
  }));
}

async function run() {
  if (analyzeButton.disabled) return;
  const text = input.value;
  if (!text.trim()) {
    status.className = 'status error';
    status.textContent = UI_TEXT.inputRequired;
    output.hidden = true;
    output.innerHTML = '';
    clearDiagnostics();
    return;
  }

  analyzeButton.disabled = true;
  const previousLabel = analyzeButton.textContent;
  analyzeButton.textContent = UI_TEXT.analysisButton;
  status.className = 'status';
  status.textContent = UI_TEXT.starting;
  output.hidden = true;
  clearDiagnostics();
  try {
    const result = await analyzeLocally(text);
    if (input.value !== text) {
      status.className = 'status notice';
      status.textContent = UI_TEXT.changedDuringAnalysis;
      return;
    }
    renderResult(result);
    status.className = 'status notice';
    status.textContent = UI_TEXT.ready;
  } catch (error) {
    output.hidden = true;
    output.innerHTML = '';
    showError(error);
  } finally {
    analyzeButton.disabled = false;
    analyzeButton.textContent = previousLabel;
  }
}

function handleInputChange() {
  updateInputCount();
  clearPreviousResult();
}

input.addEventListener('input', handleInputChange);
document.querySelectorAll('[data-example]').forEach(button => button.addEventListener('click', () => {
  input.value = button.dataset.example;
  handleInputChange();
  status.textContent = UI_TEXT.exampleAdded;
  input.focus();
}));

document.getElementById('clear').addEventListener('click', () => {
  input.value = '';
  handleInputChange();
  input.focus();
});

analyzeButton.addEventListener('click', run);
input.addEventListener('keydown', event => {
  if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
    event.preventDefault();
    return run();
  }
});

updateInputCount();
