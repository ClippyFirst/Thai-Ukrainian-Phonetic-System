import { analyze } from './engine.js';

const esc = x => String(x ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
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

function card(a, index) {
  const ok = a.status === 'analyzed';
  const title = a.input || 'Елемент ' + (index + 1);
  const heading = 'Результат ' + (index + 1) + ': ' + title;
  const fields = [
    ['ФОНОЛОГІЧНА IPA', a.phonemicIpa],
    ['ПОВЕРХНЕВА IPA', a.phoneticIpa],
    ['ТОН', a.tone && a.toneIpa ? a.tone + ' · ' + a.toneIpa : '—'],
    ['УКРАЇНСЬКИЙ ПРАКТИЧНИЙ КАНДИДАТ', a.ukrainian || '—']
  ];
  const explanation = (a.warnings || []).map(w => '<div class="warning">' + esc(w) + '</div>').join('');
  const data = fields.map(([label, value]) => '<div class="data"><span class="label">' + esc(label) + '</span><div class="value">' + esc(value) + '</div>' + ((label.includes('КАНДИДАТ') || label.includes('IPA')) && value ? '<button class="copy" type="button" data-copy="' + esc(value) + '">Копіювати</button>' : '') + '</div>').join('');
  return '<article class="result-card" aria-labelledby="result-' + index + '"><div class="result-top"><div><h3 class="result-title" id="result-' + index + '">' + esc(heading) + '</h3><div class="thai" lang="th">' + esc(title) + '</div><div class="subline">' + esc(statusLabel[a.status] || a.status) + '</div></div><span class="badge ' + (ok ? 'ok' : 'warn') + '">' + esc(a.status) + '</span></div>' + (ok ? '<div class="data-grid">' + data + '</div>' : '<div class="result-explanation"><strong>' + esc(statusLabel[a.status] || 'Статус аналізу') + '</strong>' + explanation + '</div>') + (ok ? explanation : '') + '</article>';
}

function render(analyses) {
  out.innerHTML = '<h2 class="results-heading">Результати аналізу</h2>' + analyses.map(card).join('');
  out.hidden = false;
  out.querySelectorAll('[data-copy]').forEach(button => button.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(button.dataset.copy);
      const old = button.textContent;
      button.textContent = 'Скопійовано';
      button.setAttribute('aria-label', 'Скопійовано');
      setTimeout(() => { button.textContent = old; button.removeAttribute('aria-label'); }, 900);
    } catch { button.textContent = 'Не вдалося скопіювати'; }
  }));
}

function run() {
  const text = input.value.trim();
  if (!text) {
    status.className = 'status error';
    status.textContent = 'Введіть тайський склад або слово. Для кількох складів розділіть їх пробілами.';
    out.hidden = true;
    return;
  }
  const analyses = text.split(/\s+/).map(analyze);
  const unresolved = analyses.filter(a => a.status !== 'analyzed').length;
  status.className = unresolved ? 'status notice' : 'status';
  status.textContent = unresolved ? 'Проаналізовано ' + analyses.length + ' елемент(ів); ' + unresolved + ' потребують додаткової перевірки або не мають детермінованого результату.' : 'Проаналізовано ' + analyses.length + ' елемент(ів). Це аналіз написання, а не переклад.';
  render(analyses);
}

document.querySelectorAll('[data-example]').forEach(button => button.addEventListener('click', () => { input.value = button.dataset.example; input.focus(); run(); }));
document.getElementById('clear').addEventListener('click', () => { input.value = ''; out.hidden = true; status.className = 'status'; status.textContent = ''; input.focus(); });
input.addEventListener('keydown', event => { if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') { event.preventDefault(); run(); } });
document.getElementById('analyze').addEventListener('click', run);