# -*- coding: utf-8 -*-
"""
ПРИЁМКА ПОЛНОГО КРУГА: то, что увидит ученик, а не то, что собрал генератор.

    python -m app.scripts.verify_quiz_round
    python -m app.scripts.verify_quiz_round --rounds 20

ЧЕМ ОТЛИЧАЕТСЯ ОТ `verify_quiz_channels`. Та проверяет СБОРКУ вопроса:
варианты, язык, созвучие. Но вопрос собирается верно и при этом остаётся
непоказуемым — ровно так и нашлась самая опасная поломка этого захода:

    Вопрос 4/15 · 🎧
    🔊 Послушай и выбери, что прозвучало:
    [Verspätung] [Verspannung] [Verpflegung] [Versöhnung]

Ни звука, ни слова. Генератор отработал безупречно, приёмка сборки сказала
«верно», а ответить на такое можно только наугад. Клипа не было потому, что
ученик выключил озвучку в настройках — и тогда ПОЛОВИНА круга приходила
вслепую, не изредка, а каждый раз.

Отсюда главное условие, которое здесь держится:

    У КАЖДОГО ВОПРОСА ЕСТЬ ЛИБО СЛОВО НА ЭКРАНЕ, ЛИБО ЗВУК.
    Ни того ни другого — вопрос без вопроса.

Проверяется и остальное, чего сборка не видит: что канал, записанный в
ответ, совпадает с тем, которым вопрос показан; что прогресс по каналам
растёт; что балл считается и растёт вместе с ответами.

ЧТО ЗДЕСЬ ПИШЕТСЯ В БАЗУ. Прогресс и ответы подопытного пользователя —
иначе проверить учёт нечем. Пользователь свой, с отрицательным id, и в
конце удаляется вместе со всеми следами. Живые данные не трогаются.
"""
from __future__ import annotations

import argparse
import asyncio
import collections
import logging
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
os.environ.setdefault("ENV_FILE", ".env.local")

logging.disable(logging.INFO)

from sqlalchemy import delete, select  # noqa: E402

from app.database.enums import CEFRLevel, QuizChannel, QuizMode  # noqa: E402
from app.database.models import User, UserWord  # noqa: E402
from app.database.session import AsyncSessionLocal  # noqa: E402
from app.services.language_service import (  # noqa: E402
    LEARNABLE_LANGS, LanguagePair, example_text, option_label, pair_for_channel,
)
from app.services.quiz_service import (  # noqa: E402
    generate_question, update_word_progress,
)

PROBE_ID = -1001


async def _probe(session, learning: str, native: str, reverse: bool,
                 audio_on: bool, channels: str, onboarded: bool = True) -> User:
    user = await session.get(User, PROBE_ID)
    if user is None:
        user = User(id=PROBE_ID, first_name="приёмка")
        session.add(user)
    user.level = CEFRLevel.B1
    user.quiz_mode = QuizMode.LEVEL
    user.learning_lang = learning
    user.native_lang = native
    user.reverse_mode = reverse
    user.audio_enabled = audio_on
    user.quiz_channels = channels
    user.interface_language = "ru"
    # ПЕРВЫЙ УРОК ПРОЙДЕН. С патча 2.1 (`in_first_lesson`) человек без
    # `onboarded_at` и без законченного занятия получает ТОЛЬКО карточки.
    # Отметку ставит обработчик ответа (7-й ответ) и итог занятия, а приёмка
    # зовёт `update_word_progress` мимо них — и подопытный навсегда оставался
    # на первом уроке: 900 вопросов, все TEXT, «ПРОВЕРКА ПРОШЛА ВХОЛОСТУЮ».
    # Сам первый урок проверяется отдельным случаем (`onboarded=False`)
    from app.core.clock import utcnow

    user.onboarded_at = utcnow() if onboarded else None
    user.quizzes_passed = 1 if onboarded else 0
    await session.commit()
    return user


async def _seed_progress(session, learning: str, words: int = 400) -> None:
    """
    Засеять подопытному прогресс по части слов — иначе слух не проверится.

    Правило допуска к слуху требует одного верного ответа по слову. Но
    отвеченное слово НЕ ВЫПАДАЕТ снова в пределах часа: SRS держит паузу
    (`REPEAT_COOLDOWN`), чтобы не гонять одно и то же подряд. За один прогон
    приёмки час не проходит, и каждое слово оказывается новым.

    Первая редакция на этом и попалась: 360 вопросов, ВСЕ текстовые, и
    отчёт «круг проходится целиком». Второй такой же ложный зелёный за
    сегодня — поэтому сев вынесен в отдельную подписанную функцию, а число
    вопросов по каналам печатается в отчёте всегда.

    `last_seen_at` ставится в прошлое, иначе пауза снова всё срежет.
    """
    from datetime import timedelta

    from app.core.clock import utcnow
    from app.database.models import Word, WordLangGroup

    rows = await session.execute(
        select(Word.id)
        .join(
            WordLangGroup,
            (WordLangGroup.word_id == Word.id)
            & (WordLangGroup.lang == learning)
            & (WordLangGroup.is_canonical.is_(True)),
        )
        .where(Word.level == CEFRLevel.B1)
        .limit(words)
    )
    long_ago = utcnow() - timedelta(days=2)

    # Точность засеваемых слов РАЗНАЯ, и это важно для правдоподобия.
    #
    # Первая редакция ставила всем 2 из 2, то есть 100%. Такие слова SRS
    # почти не показывает: его главная корзина — «трудные», с точностью ниже
    # 70%, и на неё приходится 60% выборки. Стопроцентные попадали в
    # «повторение» (9%) и «выученные» (1%), и вопросов на слух вышло ТРИ на
    # триста шестьдесят. Отчёт при этом снова сказал «ок».
    #
    # Теперь две трети слов идут с точностью 2 из 3 — ровно так выглядит
    # слово, которое человек узнаёт, но ещё путает.
    for n, (word_id,) in enumerate(rows.all()):
        shown, correct = (3, 2) if n % 3 else (2, 2)
        session.add(UserWord(
            user_id=PROBE_ID, word_id=word_id, learning_lang=learning,
            correct_streak=1, times_shown=shown, times_correct=correct,
            last_seen_at=long_ago, learned=False,
        ))
    await session.commit()


async def _cleanup(session) -> None:
    await session.execute(delete(UserWord).where(UserWord.user_id == PROBE_ID))
    await session.execute(delete(User).where(User.id == PROBE_ID))
    await session.commit()


async def play_round(session, user: User, pair: LanguagePair, length: int,
                     problems: list[str], seen: collections.Counter) -> None:
    """Один круг целиком, теми же функциями, что и в обработчике."""
    from app.bot.handlers.quiz.listen import _clip_or_text
    from app.bot.handlers.quiz.question import _question_keyboard, _question_text

    used: list[int] = []
    recent: list[str] = []

    for number in range(1, length + 1):
        question = await generate_question(
            session, user, exclude_ids=used, pair=pair, recent_channels=recent
        )
        if question is None:
            problems.append(f"{pair.learning}->{pair.native}: вопрос {number} не собрался")
            return

        word = question["correct_word"]
        channel = question["channel"]
        options = question["options"]

        # Ровно то же, что делает обработчик перед показом карточки
        clip, channel, options = await _clip_or_text(
            session, user, word, pair, channel, options
        )
        text = _question_text(word, pair, "ru", number, length, channel=channel)

        used.append(word.id)
        recent = (recent + [channel.value])[-2:]
        seen[channel.name] += 1

        # ГЛАВНОЕ УСЛОВИЕ: есть либо слово на экране, либо звук
        # У вопроса ВСЛУХ слово показано на ИЗУЧАЕМОМ языке, а не на языке
        # вопроса: произнести можно только то, что видишь, и произносят его
        # на изучаемом. У остальных — на языке вопроса.
        # Язык вопроса — ПО КАНАЛУ (`pair_for_channel`): у «Вспоминаю» на
        # экране значение, а не слово. Прежде здесь стояла пара снаружи, и
        # проверка молчала только потому, что в её случаях не было «r»:
        # первый же состав с пятой игрой дал 22 ложных «ни слова, ни звука»
        shown_lang = (pair.learning if channel is QuizChannel.SPEECH
                      else pair_for_channel(pair, channel).prompt_lang)
        shown = option_label(word, shown_lang)
        # У сборки на экране не слово, а ФРАЗА на родном — её и собирают
        if channel is QuizChannel.BUILD:
            shown = example_text(word, pair.native)
        word_on_screen = bool(shown) and shown in text
        if not word_on_screen and clip is None:
            problems.append(
                f"{pair.learning}->{pair.native} вопрос {number} ({channel.name}): "
                f"ни слова на экране, ни звука — ответить можно только наугад"
            )

        # У вопроса вслух клавиатура ДРУГАЯ: вариантов нет, ответ приходит
        # голосовым. Проверяется отдельно, потому что 
        # однажды уже оказалась вызываемой, но не определённой — модуль при
        # этом импортировался, а падало бы на первом же вопросе.
        keyboard = _question_keyboard(channel, options, "ru", word.id)
        buttons = [b for row in keyboard.inline_keyboard for b in row]
        if channel is QuizChannel.BUILD:
            # 🧱 Сетка: по кнопке на слово фразы и на каждую ловушку, не
            # больше двенадцати, и ни «⌫», ни «Проверить» — собрано ничего
            from app.services.build_service import MAX_TILES

            tiles = question["build"].tiles
            if len(buttons) != len(tiles) or len(tiles) > MAX_TILES:
                problems.append(
                    f"{pair.learning}->{pair.native} вопрос {number}: "
                    f"у сборки {len(buttons)} кнопок при {len(tiles)} словах"
                )
        elif channel is QuizChannel.SPEECH:
            if len(buttons) != 2:
                problems.append(
                    f"{pair.learning}->{pair.native} вопрос {number}: "
                    f"у вопроса вслух {len(buttons)} кнопок вместо двух"
                )
        elif channel is QuizChannel.AUDIO:
            # Четыре варианта и пятая — «Пропустить»: звук бывает нельзя
            # включить (владелец, 14.10: «может ночью»)
            answers = [b for b in buttons if (b.callback_data or "").startswith("answer_")]
            skips = [b for b in buttons if b.callback_data == "listen_skip"]
            if len(answers) != 4 or len(skips) != 1:
                problems.append(
                    f"{pair.learning}->{pair.native} вопрос {number}: у вопроса на "
                    f"слух {len(answers)} вариантов и {len(skips)} «Пропустить»"
                )
        elif len(buttons) != 4:
            problems.append(
                f"{pair.learning}->{pair.native} вопрос {number}: "
                f"{len(buttons)} кнопок вместо четырёх"
            )

        # Канал, которым вопрос ПОКАЗАН, и которым он будет засчитан, —
        # один и тот же. Разойдись они, прогресс копился бы не в тот навык
        if channel is QuizChannel.AUDIO and clip is None:
            problems.append(
                f"{pair.learning}->{pair.native} вопрос {number}: "
                f"канал остался AUDIO без клипа"
            )

        await update_word_progress(
            user_id=user.id, word_id=word.id, is_correct=(number % 3 != 0),
            session=session, learning_lang=pair.learning, channel=channel,
        )


async def run(rounds: int, length: int, full: bool) -> int:
    problems: list[str] = []
    seen: collections.Counter = collections.Counter()

    # Случаи подобраны так, чтобы каждый ловил свою беду
    cases = [
        ("de", "ru", False, True, "ta", "обычный: текст и слух"),
        ("de", "ru", False, True, "tas", "ВСЕ ТРИ канала вместе"),
        ("de", "ru", False, True, "s", "только речь"),
        ("de", "ru", False, True, "a", "только слух"),
        ("de", "ru", True, True, "ta", "обратное направление"),
        ("de", "ru", False, False, "ta", "ОЗВУЧКА ВЫКЛЮЧЕНА при составе «ta»"),
        ("pl", "uk", False, True, "ta", "пара без немецкого"),
        ("en", "tr", True, True, "ta", "обратное, пара без немецкого"),
        ("tr", "pl", False, True, "t", "только текст"),
        ("de", "ru", False, True, "b", "только сборка"),
        ("de", "ru", False, False, "tb", "сборка при ВЫКЛЮЧЕННОЙ озвучке"),
        ("ru", "de", False, True, "tasrb", "все игры, пара без немецкого изучаемого"),
    ]

    # И СВЕРХ НИХ — ВСЕ 30 ПАР В ОБА НАПРАВЛЕНИЯ, ВСЕМИ ТРЕМЯ КАНАЛАМИ.
    #
    # Девяти подобранных случаев мало, и это стало видно от прямого
    # вопроса владельца: «все игры должны работать во всех направлениях».
    # Полный круг прогонялся на четырёх парах из тридцати, а остальные
    # держались приёмкой СБОРКИ — а она проверяет отдельный вопрос, не
    # проход круга целиком: ни чередования каналов, ни правила «не больше
    # двух подряд», ни того, что у каждого вопроса есть слово или звук.
    #
    # Шестьдесят сочетаний дороже девяти, зато «во всех направлениях»
    # перестаёт быть обещанием.
    if full:
        cases += [
            (learning, native, reverse, True, "tasb",
             f"{learning}{'←' if reverse else '→'}{native} все каналы")
            for learning in LEARNABLE_LANGS
            for native in LEARNABLE_LANGS
            if learning != native
            for reverse in (False, True)
        ]

    async with AsyncSessionLocal() as session:
        try:
            for learning, native, reverse, audio_on, channels, label in cases:
                user = await _probe(session, learning, native, reverse, audio_on, channels)
                await _seed_progress(session, learning)
                pair = LanguagePair(learning=learning, native=native, reverse=reverse)
                before = len(problems)
                for _ in range(rounds):
                    await play_round(session, user, pair, length, problems, seen)
                mark = "ок" if len(problems) == before else f"СБОЙ ({len(problems) - before})"
                print(f"  {label:42s} {mark}")
                await session.execute(
                    delete(UserWord).where(UserWord.user_id == PROBE_ID)
                )
                await session.commit()
            # ПЕРВЫЙ УРОК: все игры включены и открыты по прогрессу, но
            # новичку — только карточки (`in_first_lesson`, патч 2.1)
            user = await _probe(session, "de", "ru", False, True, "tasrb",
                                onboarded=False)
            await _seed_progress(session, "de")
            first: collections.Counter = collections.Counter()
            before = len(problems)
            await play_round(session, user, LanguagePair(learning="de", native="ru", reverse=False),
                             length, problems, first)
            if set(first) != {QuizChannel.TEXT.name}:
                problems.append(f"первый урок: не одни карточки — {dict(first)}")
            mark = "ок" if len(problems) == before else f"СБОЙ ({len(problems) - before})"
            print(f"  {'первый урок: только карточки':42s} {mark}")
        finally:
            await _cleanup(session)

    total = sum(seen.values())
    print(f"\nкругов сыграно: {rounds * len(cases)}, вопросов: {total}")
    print("  по каналам: " + ", ".join(f"{k} {v}" for k, v in sorted(seen.items())))

    # Ложный зелёный: если вопросов какого-то канала не было ВОВСЕ, значит
    # проверять было нечего, и «ок» про него ничего не значит.
    #
    # Проверка нужна на КАЖДЫЙ канал, а не только на слух: добавив речь, я
    # первым же прогоном получил «ок» на случаях «только речь» и «все три
    # вместе», не задав НИ ОДНОГО вопроса вслух — `pick_channel` про третий
    # канал ещё не знал и молча отдавал текст.
    for channel in (QuizChannel.AUDIO, QuizChannel.SPEECH, QuizChannel.BUILD):
        # Звук нужен слуху и речи; сборке — нет
        expected = any((audio_on or channel is QuizChannel.BUILD)
                       and channel.value in channels
                       for _, _, _, audio_on, channels, _ in cases)
        if expected and not seen.get(channel.name):
            print(f"\nПРОВЕРКА ПРОШЛА ВХОЛОСТУЮ: ни одного вопроса канала "
                  f"{channel.name} не задано")
            return 1

    if problems:
        print(f"\nНАРУШЕНИЙ: {len(problems)}")
        for line in problems[:20]:
            print(f"   {line}")
        if len(problems) > 20:
            print(f"   … и ещё {len(problems) - 20}")
        return 1

    print("\nкруг проходится целиком: у каждого вопроса есть слово или звук")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rounds", type=int, default=5)
    parser.add_argument("--length", type=int, default=15)
    parser.add_argument("--full", action="store_true",
                        help="все 30 пар в оба направления всеми каналами")
    args = parser.parse_args()
    return asyncio.run(run(args.rounds, args.length, args.full))


if __name__ == "__main__":
    raise SystemExit(main())
