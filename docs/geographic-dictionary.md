# Пакетний CSV-рушій транскрипції тайського тексту

## Призначення

`scripts/build_geographic_dictionary.py` — історично названа реалізація пакетного CSV-рушія транскрипції тайського тексту. Вона обробляє звичайні слова та фрази в довільній обраній колонці CSV; назва модуля не означає, що вхід обов'язково має бути географічною назвою. Для побудови власного географічного корпусу можна додатково використовувати шаблон `data/geography/geographic-names-template.csv` та відповідні метадані. Для кожного рядка CSV рушій додає чотири незалежно марковані результати:

1. **RTGS** — латинська романізація за PyThaiNLP 5.4.0 (`newmm` для меж слів + `royin` для RTGS), причому `newmm` отримує source-pinned CC0-1.0 словник репозиторію.
2. **Фонемний IPA** — результат внутрішнього ClippyFirst Thai → IPA рушія.
3. **Широкий поверхневий IPA** — окремий типізований шар, якщо він підтриманий.
4. **Український запис з IPA** — результат штатного IPA → Ukrainian адаптера репозиторію.

RTGS не є джерелом українського запису. Він не передає тон і не зберігає всіх відмінностей довготи голосних. Український результат створюється тільки через наявний `PhoneticResult` та `adapt_syllable_to_ukrainian` pipeline.

## Швидкий запуск

Встановити проєкт та додаткову залежність для RTGS:

```bash
python -m pip install -e ".[geography]"
```

Підготувати CSV із заголовком `name_th` (інші колонки можна зберігати як метадані):

```csv
id,name_th,feature_type,source_name,source_url,source_license
```

Запустити:

```bash
python scripts/build_geographic_dictionary.py data/geography/input.csv \
  --thai-column name_th \
  --output build/geographic-dictionary.csv
```

Назву вхідної колонки можна змінити через `--thai-column`. Для TSV можна вказати `--delimiter $'\\t'`; за замовчуванням читається CSV з комою. `--limit 20` дозволяє зробити пробний запуск на перших 20 рядках.

Вихідний CSV записується в UTF-8 з BOM для сумісності з Excel. Усі вхідні колонки, зокрема ідентифікатори, координати, джерела й ліцензії, зберігаються; додаються:

| Колонка | Значення |
|---|---|
| `romanization_rtgs` | RTGS-кандидат PyThaiNLP 5.4.0 |
| `ipa_phonemic` | Фонемний IPA; заповнюється лише за повного підтриманого аналізу |
| `ipa_broad_surface` | Широкий поверхневий IPA |
| `ukrainian_from_ipa` | Українська адаптація через типізований IPA |
| `pipeline_status` | Статус повноти/обмежень |
| `segmentation_method` | Метод меж слів, який повернув рушій |
| `pipeline_warnings` | Попередження та причини утримання результату |
| `romanization_method` | Версія та метод RTGS |

## Статуси та правила утримання

- `COMPLETE_MODEL_OUTPUT_NOT_ADJUDICATED` — технічно повний результат рушія; це **не** означає незалежно перевірену правильність вимови.
- `PARTIAL_OR_UNSUPPORTED_WITHHELD` — принаймні одне слово/склад не має повного підтриманого шляху. IPA та український результат для всього рядка CSV залишаються порожніми; причини вказуються в `pipeline_warnings`.
- `NO_THAI_INPUT` — у вибраній колонці немає тайських символів.

Сегментація слова не доводить його вимову. Скрипт повторно використовує консервативний `analyze_text_with_word_segmentation` і не намагається автоматично вгадувати складову структуру невідомого власного імені. RTGS може бути заповнений, навіть якщо IPA та український результат утримано: це окремі методи з різними обмеженнями.

## Важливо для географічного корпусу

- Не заповнюйте `source_license` припущенням. Записуйте ліцензію, атрибуцію, URL та ідентифікатор вихідного запису лише з перевіреного джерела.
- Не додавайте координати чи українські офіційні екзоніми без окремого авторитетного джерела.
- Зберігайте оригінальне тайське написання та джерельні метадані незмінними.
- Результати моделі — дослідницькі кандидати, а не офіційні назви, не експертне IPA-золото і не юридично затверджена українська форма.
- Для публікації словника потрібна окрема редакторська перевірка власних назв, географічної ідентифікації, IPA, української форми та прав на джерельний набір.

## Архітектура

`Thai CSV field → PyThaiNLP newmm/royin (RTGS side channel)`

`Thai CSV field → ClippyFirst word segmentation → Thai analysis → PhoneticResult IPA → Ukrainian IPA adapter`

RTGS не передається в IPA-адаптер. Невідомі/неповні випадки fail closed. Скрипт не змінює браузерний runtime та не додає зовнішній G2P у production.

## Перевірка

Тести `tests/test_geographic_dictionary.py` перевіряють розділення RTGS і IPA-маршрутів, збереження метаданих CSV, використання `newmm`/ `royin`, та заборону перезаписувати вхідний файл. Для повної перевірки запустити:

```bash
python -m pytest -q
python -m ruff check .
```

PyThaiNLP 5.4.0 є обов'язковою лише для фактичного запуску географічного RTGS-експорту; тести ізольовують її виклик через залежності, що передаються в функції.


## Перевірений стан реалізації — 2026-11-07

PR [#228](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/pull/228) merged as `b7973b03961317abf3c5e2fed67c53c7b450eeee`. Exact-head CI #42303606383 and Pages build #42303606414 passed. Post-merge main CI #42304411797 and Pages build/deploy/live smoke #42304411720 passed, along with Site API, Pyodide compatibility and external G2P smoke. The CI runtime fixture verifies the software pipeline only; geographic proper-name accuracy remains NOT_MEASURED until independent sourced corpus review.
