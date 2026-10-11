# -*- coding: utf-8 -*-
"""
ГЕЙТ: название клипа совпадает с тем, что на карточке и что звучит.

    python -m app.scripts.scan_clip_title

ПОЧЕМУ ГЕЙТ, А НЕ ПРИМЕТА. Законных исключений нет: если на карточке стоит
«Zapomnienie», то и в названии клипа обязано стоять «Zapomnienie», и голос
обязан произнести его же. Любое расхождение — дефект.

ЧТО ЭТО ЗА ТРИ ВЕЩИ

    показано   option_label(word, lang)      — слово на карточке и на кнопке
    звучит     spoken_for(word, lang, kind)  — текст, отданный синтезу
    названо    audio_title(...)              — заголовок аудиофайла в Telegram

Для клипа со словом все три совпадают буква в букву. Для клипа с примером
название длиннее: «слово — начало примера», — поэтому сверяется начало.

ОТКУДА ВЗЯЛСЯ ГЕЙТ. Владелец прислал снимок карточки: слово «Zapomnienie»,
а в заголовке аудиофайла «zapomnienie, niepamięć» — вся ячейка перевода.
Звучало при этом одно слово и звучало верно.

Код на тот момент был УЖЕ ПРАВИЛЬНЫЙ: `audio_title(option_label(...))`.
Неверным был кэш. Название впечатывается в клип при ЗАГРУЗКЕ в Telegram, а
при отправке по file_id параметр title игнорируется — показываются
метаданные первой загрузки. Проверка годности кэша сверяла произносимый
текст и бота, но не название; при правке правила названия произносимый
текст не менялся, запись считалась годной, и карточка молча показывала
старый заголовок.

Поэтому гейт проверяет ДВЕ разные вещи, и обе нужны:

    1. ПРАВИЛО — что построит код для каждого ряда и языка. Ловит ошибку в
       самом правиле (так были пойманы «вся ячейка вместо одного значения»
       и «автобус вместо Автобус»).
    2. КЭШ — что записано в word_audio рядом с file_id. Ловит клипы,
       загруженные по старому правилу: правило уже верное, а в Telegram
       лежит прежнее название.

Проверять только первое — ровно та дыра, из-за которой дефект дожил до
снимка: правило чинили, а загруженные клипы оставались как были.

ПОЧЕМУ ПУСТОЙ КЭШ — ЭТО НОРМА. word_audio заполняется лениво, при первом
показе слова. Ноль записей означает «ещё никто не играл», а не поломку.

Скрипт ТОЛЬКО ЧИТАЕТ.
"""
from __future__ import annotations

import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
os.environ.setdefault("ENV_FILE", ".env.local")

from sqlalchemy import create_engine, text  # noqa: E402
from sqlalchemy.orm import Session  # noqa: E402

from app.config import settings  # noqa: E402
from app.database.models import Word, WordAudio  # noqa: E402
from app.services.audio_service import (  # noqa: E402
    KIND_FULL, KIND_WORD, audio_title, spoken_for,
)
from app.services.language_service import (  # noqa: E402
    SUPPORTED_LANGS, example_text, get_language, main_meaning, option_label,
    upper_first,
)

SHOW = 12  # сколько расхождений печатать подробно


def check_rule(session: Session) -> list[str]:
    """Что построит КОД — для каждого ряда, языка и вида клипа."""
    bad: list[str] = []
    ids = session.execute(text("SELECT id FROM words ORDER BY id")).scalars().all()
    pairs = 0
    for i in ids:
        w = session.get(Word, i)
        for lang in SUPPORTED_LANGS:
            shown = option_label(w, lang)
            if not shown:
                continue
            pairs += 1
            for kind in (KIND_WORD, KIND_FULL):
                spoken = spoken_for(w, lang, kind)
                if not spoken:
                    continue
                example = example_text(w, lang) if kind == KIND_FULL else None
                title = audio_title(shown, example)

                # названо начинается с показанного
                if not title.startswith(shown):
                    bad.append(f"ряд {i} {lang} {kind}: показано {shown!r}, "
                               f"названо {title!r}")
                # названо и звучит — одно слово, различие только в регистре
                #
                # СРАВНИВАТЬ ЧЕРЕЗ .lower() ЗДЕСЬ НЕЛЬЗЯ. Турецкая «İ».lower()
                # даёт в Python «i» с ОТДЕЛЬНОЙ комбинирующей точкой, а не
                # «i», и сравнение расходится на всех 1256 турецких рядах с
                # начальной «i» — при полностью верных данных. Поэтому
                # регистр наводится той же функцией, что и в боте.
                chosen = main_meaning(w, lang)
                want = (chosen if get_language(lang).uses_article
                        else upper_first(chosen, lang))
                if shown != want:
                    bad.append(f"ряд {i} {lang} {kind}: звучит {chosen!r}, "
                               f"показано {shown!r}, ожидалось {want!r}")
                # в названии клипа со словом нет списка
                if kind == KIND_WORD and "," in title:
                    bad.append(f"ряд {i} {lang} {kind}: в названии список — "
                               f"{title!r}")
    print(f"правило: проверено пар «ряд × язык» {pairs}, расхождений {len(bad)}")
    return bad


def check_cache(session: Session) -> list[str]:
    """Что РЕАЛЬНО записано рядом с загруженными в Telegram file_id."""
    bad: list[str] = []
    rows = session.execute(
        text("SELECT * FROM word_audio ORDER BY id")
    ).mappings().all()
    for r in rows:
        w = session.get(Word, r["word_id"])
        if w is None:
            continue
        lang, kind = r["lang"], r["kind"]
        shown = option_label(w, lang)
        example = example_text(w, lang) if kind == KIND_FULL else None
        want = audio_title(shown, example)
        if r["title"] is None:
            bad.append(f"запись {r['id']} (ряд {r['word_id']} {lang} {kind}): "
                       f"название не сохранено — клип грузили до миграции")
        elif r["title"] != want:
            bad.append(f"запись {r['id']} (ряд {r['word_id']} {lang} {kind}): "
                       f"в Telegram {r['title']!r}, надо {want!r}")
    note = " (пусто — ещё никто не играл, это норма)" if not rows else ""
    print(f"кэш: записей {len(rows)}{note}, расхождений {len(bad)}")
    return bad


def main() -> int:
    engine = create_engine(settings.DATABASE_URL_SYNC)
    with Session(engine) as session:
        bad = check_rule(session) + check_cache(session)

    for line in bad[:SHOW]:
        print(f"  {line}")
    if len(bad) > SHOW:
        print(f"  … и ещё {len(bad) - SHOW}")

    if bad:
        print(f"\nВСЕГО РАСХОЖДЕНИЙ: {len(bad)}")
        print("Если расходится КЭШ, а правило чисто — клипы загружены по "
              "старому правилу. Лечится: DELETE FROM word_audio;")
        return 1
    print("\nназвание, показанное слово и звучащее слово совпадают везде")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
