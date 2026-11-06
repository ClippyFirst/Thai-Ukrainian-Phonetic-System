# Тайська романізація латиницею

## Призначення
Публічний модуль web/romanization.html перетворює тайський текст на латинський запис окремо від основного Thai → IPA → Ukrainian сервісу. Це допоміжний режим для читання й пошуку тайських назв; він не є українською транскрипцією.

## Обраний метод: RTGS / PyThaiNLP royin
Основний метод — **Royal Thai General System of Transcription (RTGS)**, офіційна тайська система транскрипції латиницею, реалізована рушієм royin з PyThaiNLP 5.4.0.
- PyThaiNLP 5.4.0 описує romanize(..., engine="royin") як метод на основі RTGS.
- web/src/rtgs-reference.js уже містив окремий порт royin; інтеграція повторно використовує його.
- Сегментація тексту без пробілів використовує browser-native порт PyThaiNLP newmm (web/src/fastthaig2p-tokenizer.js) і закріплений словник PyThaiNLP 5.4.0.
- Словник перевіряється за SHA-256, розміром, версією й ліцензією локального маніфесту. Дані завантажуються лише з того самого GitHub Pages origin.

Автоматичне розбиття суцільного тайського тексту на слова — окрема задача. Інтерфейс повідомляє, що сегментація здійснюється newmm, а непідтримані лексичні випадки не маскуються під гарантовано правильну форму.

## Чому не Thai2Rom або ISO 11940
PyThaiNLP також документує thai2rom і thai2rom_onnx — нейромережеві рушії романізації. Вони дають інший, model-based результат і не є RTGS. Їх не вбудовано: це потребувало б окремої моделі/рантайму, перевірки розміру завантаження, прав на модель та незалежного порівняння точності.
**ISO 11940** — транслітерація тайського письма латиницею, не тотожна запису вимови. IPA/G2P — фонетичний формат, а не романізація.

## Обмеження
- RTGS не позначає лексичний тон і не зберігає повністю довготу голосних.
- Сегментація тексту без пробілів може мати альтернативні межі.
- Існуючі lexical overrides і fail-closed правила rtgs-reference.js залишаються чинними.
- Непідтримані фрагменти показуються як RTGS НЕ ПЕРЕВІРЕНО, а не підміняються здогадкою.
- Не використовуйте результат для офіційної транслітерації паспортних чи юридичних даних без перевірки.

## Джерела та ліцензії
- [PyThaiNLP 5.4.0 royin source](https://github.com/PyThaiNLP/pythainlp/blob/v5.4.0/pythainlp/transliterate/royin.py), Apache-2.0.
- [PyThaiNLP 5.4.0 API](https://pythainlp.org/docs/5.4.0/api/transliterate.html).
- PyThaiNLP-derived newmm tokenizer port: fastthaig2p-tokenizer.js, Apache-2.0.
- PyThaiNLP default word list: CC0-1.0 per existing browser asset manifest. Existing third-party notices remain in force; no external model or remote service is loaded.

## Verification
- rtgs-romanizer.test.mjs: manifest, SHA-256/size guard, known RTGS example, punctuation passthrough and unsupported-token abstention.
- romanization-page.test.mjs: page contract, navigation, method limitations and same-origin implementation.
- Existing rtgs-reference.test.mjs and scripts/test_rtgs_parity.py remain the underlying RTGS renderer and pinned PyThaiNLP parity gates.
- Pages post-deploy smoke requests the page and browser module. Engineering parity is not independent Thai linguistic review or a claim of perfect lexical romanization.
