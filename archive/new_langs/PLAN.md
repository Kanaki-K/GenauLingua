# Новые языки it / es / fr / cs — что сделано и что осталось

Ветка `feature/new-langs-it-es-fr-cs`. Языки описаны, но ЗАКРЫТЫ: кодов нет в
`LEARNABLE_LANGS`, ученики их не видят. Порядок шагов — HANDOVER §12.
Старые языки (ru/uk/en/pl/tr) не правились: утверждены, на проде.

## Сделано (17.10.2026)

- [x] Колонки `translation_/example_ it/es/fr/cs` — миграция `a1c3e5f7b9d2`
      (применена только к dev-базе); поля в `Word`; реестр `LANGUAGES`,
      `SUPPORTED_LANGS`; снятие артикля «l'» при схлопывании.
- [x] Словарь: 12 902 слова × 4 языка — `archive/new_langs/out/*.jsonl`.
      Правила — `GUIDE.md`, решения по спорным словам — `DECISIONS.md`.
- [x] Проверки качества (цифры — в отчётах сессии):
      перевод+самопроверка; вычитка (549 правок); точечный круг (476);
      аудит 100×100 случайных рядов (ошибки 0,57% → исправлены);
      обратный перевод вслепую A1–A2 (6 548 пар, 15 ошибок);
      сверка пар — все 10 языков показывают один смысл (123 правки);
      сленг по правилу 2.1 — нейтральное первым, разговорное с пометкой,
      грубое убрано (1 516 правок, 39 грубых значений удалено).
      Инструменты: `app/scripts/new_langs_{check,audit,backtrans,crosscheck,show,consistency,apply}.py`.
- [x] Записано в dev-базу (`new_langs_apply --apply`), пересчитаны группы
      (`rebuild_word_groups --langs it es fr cs --no-remap`), частоты,
      уровни (`fill_word_levels`: новые языки в `LANGS`, артикль снимается).
      Отпечаток старых языков и прогресса учеников — без изменений.
- [x] Голоса (только одноязычные): it Elsa/Isabella/Diego, es Elvira/Ximena/
      Alvaro, fr Denise/Eloise/Henri, cs Vlasta/Antonin; фразы прослушивания;
      коды распознавания `ASR_LANG`.
- [~] Синтез озвучки ЗАПУЩЕН (женский основной голос, затем мужской):
      `tts_synthesize --lang es|it|fr|cs`, затем `tts_synthesize_male`.
      Клипы — `tts/<lang>/<голос>/...` (в .gitignore). Прерывать можно:
      повторный запуск доделывает только недостающее.

- [x] Интерфейс `app/locales/{it,es,fr,cs}.py` (464 ключа, только вежливая
      форма) — подключён в `LOCALES`, но выбрать нельзя: нет в `INTERFACE_LANGS`.
      `langname_*`/`lang_*` новых языков добавлены во все локали (старые строки
      не тронуты); `_plural_index` для cs/fr; месяцы, города, «Собираю».
- [x] 16 примет `scan_*` понимают новые языки (20 полей исправлено).
- [x] `verify_quiz_channels` при открытых 10 языках (обёртка, без правки кода):
      90 пар, 4 500 вопросов, единственная находка — нет чешских клипов.
- [x] `verify_quiz_round --full` при 10 открытых языках: 192 сочетания «ок»,
      14 400 вопросов (AUDIO 3 527, SPEECH 2 668, BUILD 645). Приёмка шла
      вхолостую из-за правила 2.1 «первое занятие — только карточки» —
      подопытный теперь проходит первое занятие.
- [x] Аудит оставшихся 2 902 рядов — аудитом покрыта вся база (12 902).
- [x] Озвучка it/es/fr: оба голоса, не хватает 0 (по коду, не по счёту файлов).
- [x] Распознавание it/es/fr (все клипы с примером, ASR_DEVICE=cuda):
      it 9 551 / es 9 369 / fr 9 412; 106 несовпадений перепроверены моделью
      medium — настоящих ошибок 0 (числа цифрами, омофоны fr, повторы).
- [x] `tts_scan_duration` по всем 190 тыс. клипам: 6 обрубленных (1 it, 5 cs)
      — it пересинтезирован, cs убраны (лежат в archive/new_langs/truncated/).
- [~] Чешский: сервис Microsoft по cs-CZ отвечает урывками (сервер принимает
      запрос и рвёт соединение, код 1006; Vlasta 6/30, Antonin 3/30 при sk/it
      30/30). Повтор — scratchpad cs_retry.sh; Antonin — tts_synthesize_male.
      ПОСЛЕ: missing.py cs = 0, `tts_scan_duration` (обрывы!), распознавание cs.

## Осталось — по порядку

1. **Довести синтез.** Повторять, пока не останется сорвавшихся:
   `python -m app.scripts.tts_synthesize --lang XX` (и `tts_synthesize_male`).
   Счёт: `python -m app.scripts.tts_synthesize --stats`.
2. **Проверка озвучки распознаванием** по всем клипам:
   `python -m app.scripts.tts_asr_check --lang XX --all --workers 4`
   (и `--voice` мужского). Разобрать расхождения; на пробе cs было 1/10 —
   похоже на слабость распознавателя, проверить.
3. **Подписи аудиокарточек** — посмотреть `app/services/audio_service.py`
   (title/performer клипа) для новых языков; сравнить со старыми.
4. **Интерфейс бота** `app/locales/{it,es,fr,cs}.py` — все 460 ключей
   (`test_all_locales_have_identical_key_sets`), только на «Вы» (it Lei, es
   usted, fr vous, cs Vy), «занятие» = lezione/lección/leçon/lekce, вид
   уведомлений по тесту `test_every_outgoing_message_has_the_same_look`.
5. **Множественное число** `_plural_index` (`app/locales/__init__.py`):
   cs как pl (1 / 2–4 / 5+); fr — 0 и 1 единственное; it, es — как en.
6. **«Собираю»** `app/services/build_service.py` — ловушки: it/es/fr артикли
   и формы глагола, cs падежи.
7. **Приметы `scan_*`** с языковыми списками (`scan_formality`,
   `scan_alien_letter`, `scan_pos`, `example_number_mismatch`, `scan_artifacts`).
8. `INTERFACE_LANGS` (порядок — решение владельца), города
   `app/utils/timezones.py`, справка `help_how_to_use_text`.
9. **Открытие** — коды в `LEARNABLE_LANGS`; перед этим `verify_quiz_channels`,
   `verify_quiz_round`, полный `pytest`. Сначала на тест-бот @gentestling_bot.
10. **Прод** (только по слову владельца): миграция → `wordbase_transfer load`
    (НЕ дамп) → пересчёты (шаг 7 §12, `--no-remap`) → `release_snapshot
    --compare` → клипы `tts/` по SFTP → `file_id` боевым ботом
    (`tts_pregenerate`) — клипы тестового бота не годятся.

## Решения владельца, ждут ответа

- Старые языки: исправить ли найденное — `OLD_COMMA_SPLIT.txt` (43 значения
  с запятой внутри — бот режет), `OLD_PAIRS.txt` (297 расхождений смысла в
  парах), `OLD_LANGS_NOTES.md` (~130 замечаний), остаток сленга в ru/uk
  (Bulle «мент», Weib «баба», Fresse «морда», bumsen…).
