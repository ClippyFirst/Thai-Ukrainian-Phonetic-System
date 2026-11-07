# Тайська романізація латиницею

## Призначення
Публічний модуль web/romanization.html надає повноцінний окремий інструмент Thai → Latin. На головній сторінці той самий RTGS-рушій доступний як додаткова згорнута відповідь після основного українського результату: користувач сам відкриває секцію, після чого браузер динамічно завантажує RTGS-модуль і ініціалізує його на основі спільного локального словника. До відкриття секції RTGS-модуль не завантажується й романізація не обчислюється. Словник CC0 спільний із нативним браузерним токенізатором основного сервісу, тому він може бути вже в кеші або завантажитися під час основного аналізу; RTGS повторно використовує той самий same-origin ресурс. RTGS залишається окремим методом, а не українською транскрипцією.

## Обраний метод: RTGS / PyThaiNLP royin
Основний метод — **Royal Thai General System of Transcription (RTGS)**, офіційна тайська система транскрипції латиницею, реалізована рушієм royin з PyThaiNLP 5.4.0.
- PyThaiNLP 5.4.0 описує romanize(..., engine="royin") як метод на основі RTGS.
- web/src/rtgs-reference.js уже містив окремий порт royin; інтеграція повторно використовує його.
- Сегментація тексту без пробілів використовує browser-native порт PyThaiNLP newmm (web/src/fastthaig2p-tokenizer.js) і закріплений словник PyThaiNLP 5.4.0.
- Словник перевіряється за SHA-256, розміром, версією й ліцензією локального маніфесту. Дані завантажуються лише з того самого GitHub Pages origin.

Автоматичне розбиття суцільного тайського тексту на слова — окрема задача. Інтерфейс повідомляє, що сегментація здійснюється newmm, а непідтримані лексичні випадки не маскуються під гарантовано правильну форму.

## Відображення на головній сторінці
Українська практична адаптація IPA залишається головним результатом. RTGS показується лише в native disclosure (`details/summary`) з назвою «Показати додатково: романізація латиницею (RTGS)». Це progressive disclosure: додаткова можливість видима, але не конкурує з основним результатом. Відкриття секції запускає dynamic import `rtgs-romanizer.js` і ініціалізацію RTGS через маніфест та спільний CC0-словник із перевіркою SHA-256/розміру/версії; результат прив'язаний до того самого тексту й відкидається, якщо поле змінилося під час завантаження. Непідтримані фрагменти залишаються явно позначеними, без здогадок.

## Перевірені власні назви та лексичні винятки

RTGS — це система передавання вимови, але для офіційних власних назв потрібно зберігати затверджене написання, а не покладатися лише на загальні правила для окремих графем. Тому рушій має окремий шар перевірених лексичних форм із джерелом і тестами.

Перший обов'язковий регресійний запис — **กรุงเทพมหานคร → Krung Thep Maha Nakhon**. Саме таку форму публікує Royal Society of Thailand (สำนักงานราชบัณฑิตยสภา) у своєму офіційному переліку власних назв і довіднику адміністративних одиниць. Окреме офіційне роз'яснення підтверджує, що для назви กรุงเทพมหานคร допустимі обидві форми: *Krung Thep Maha Nakhon* та *Bangkok*. Для RTGS-режиму рушій повертає першу форму; Bangkok є офіційним альтернативним англомовним найменуванням, а не результатом графемної RTGS-конверсії.

- [Royal Society of Thailand — นานาวิสามานยนาม ฉบับราชบัณฑิตยสภา (PDF)](https://www.orst.go.th/FILEROOM/CABROYINWEB/DRAWER004/GENERAL/DATA0004/00004233.PDF), запис กรุงเทพมหานคร.
- [Royal Society of Thailand — офіційне роз'яснення від 16.02.2022](https://orst.go.th/iwfm_list.asp?b=e&i=0020000402001002%2F65BPT1920063&n=g): Krung Thep Maha Nakhon та Bangkok можна використовувати як офіційні латинські назви.

Якщо загальний токенізатор розбиває відому власну назву на кілька сусідніх тайських токенів, рушій може об'єднати їх **лише тоді, коли конкатенація точно збігається з окремим перевіреним лексичним записом**. Об'єднання не перетинає пробіли або пунктуацію і не є загальним правилом склеювання слів. Усі інші послідовності проходять звичайний RTGS-процес або fail-closed перевірку.

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
