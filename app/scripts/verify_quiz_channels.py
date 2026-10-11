# -*- coding: utf-8 -*-
"""
ПРИЁМКА ТРЁХ ИГР: прогон вопросов по всем парам, направлениям и каналам.

    python -m app.scripts.verify_quiz_channels
    python -m app.scripts.verify_quiz_channels --per-case 40

ЗАЧЕМ. Владелец дословно: «убедись, что все игры работают как надо, без
поломок... я не в состоянии проверить все языки и остальное». Проверить
руками тут и правда нельзя: шесть изучаемых языков на пять языков значения
дают 30 пар, каждая в двух направлениях, каждая двумя каналами — 120
сочетаний. Нажать их все невозможно, а сломаться может каждое.

Скрипт делает то же, что `verify_wordbase` делает для словарной базы:
гоняет НАСТОЯЩИЙ генератор вопросов и проверяет не «не упало ли», а
содержательные условия.

ЧТО ПРОВЕРЯЕТСЯ В КАЖДОМ ВОПРОСЕ

  общее        ровно четыре варианта; все подписи различны; правильный
               ровно один и это то самое слово; ни одна подпись не пуста
  смысл        ни один неверный вариант не значит того же, что верный —
               иначе правильных ответов два, и выбрать нельзя
  на слух      варианты на ИЗУЧАЕМОМ языке, а не на языке значения;
               самого слова в тексте вопроса НЕТ; примера тоже нет;
               клип существует на диске
  текстом      слово в тексте вопроса ЕСТЬ
  созвучие     у вопроса на слух хотя бы один неверный вариант начинается
               так же, как верный, — иначе слушать не надо

ПОЧЕМУ КЛИП ПРОВЕРЯЕТСЯ ПО ДИСКУ, А НЕ ЧЕРЕЗ `clip_for_user`. Тот при
отсутствии клипа идёт синтезировать по сети. Приёмка должна отвечать на
вопрос «всё ли готово», а не чинить на ходу: синтез замаскировал бы ровно
ту дыру, которую ищем.

Скрипт ТОЛЬКО ЧИТАЕТ: вопросы генерируются, но ответы не засчитываются и
прогресс не меняется.
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

logging.disable(logging.INFO)  # вывод SQL забивает отчёт

from app.database.enums import CEFRLevel, QuizChannel, QuizMode  # noqa: E402
from app.database.models import User  # noqa: E402
from app.database.session import AsyncSessionLocal  # noqa: E402
from app.services import audio_store  # noqa: E402
from app.services.audio_service import (  # noqa: E402
    clip_kind_for_question, spoken_for,
)
from app.services.language_service import (  # noqa: E402
    LEARNABLE_LANGS, LanguagePair, fold, main_meaning, meaning_variants,
    option_label,
)
from app.services.quiz_service import (  # noqa: E402
    OPTIONS_TOTAL, _prefix_len, generate_question,
)
from app.services.tts_voices import default_voice  # noqa: E402

# Отдельный пользователь приёмки: id заведомо не занят живыми людьми, и
# прогресса у него нет — значит правило допуска к слуху всегда даст текст.
# Чтобы проверить и слух, канал ниже навязывается принудительно.
PROBE_USER_ID = -999


def _probe_user(channels: str) -> User:
    user = User(id=PROBE_USER_ID, level=CEFRLevel.B1, quiz_mode=QuizMode.LEVEL)
    user.quiz_channels = channels
    return user


def _check(question: dict, pair: LanguagePair, text: str) -> list[str]:
    """Содержательные проверки одного вопроса. Пустой список — всё верно."""
    problems: list[str] = []
    word = question["correct_word"]
    options = question["options"]
    channel = question["channel"]
    idx = question["correct_answer_index"]

    if len(options) != OPTIONS_TOTAL:
        problems.append(f"вариантов {len(options)}, а должно {OPTIONS_TOTAL}")
        return problems

    labels = [t for _, t in options]
    if any(not t.strip() for t in labels):
        problems.append("есть пустая подпись варианта")
    if len(set(labels)) != len(labels):
        problems.append(f"подписи повторяются: {labels}")
    if options[idx][0] != word.id:
        problems.append("индекс правильного указывает не на то слово")

    # Ни один неверный вариант не должен значить того же, что верный
    answer_lang = pair.learning if channel is QuizChannel.AUDIO else pair.answer_lang
    right = meaning_variants(option_label(word, answer_lang), answer_lang)
    for i, (wid, label) in enumerate(options):
        if i == idx:
            continue
        if right and meaning_variants(label, answer_lang) & right:
            problems.append(f"вариант {label!r} значит то же, что верный")

    shown = option_label(word, pair.learning)
    if channel is QuizChannel.AUDIO:
        if shown not in labels:
            problems.append("на слух варианты не на изучаемом языке")
        if shown and shown in text:
            problems.append("на слух слово напечатано в вопросе — слушать незачем")
        if "📝" in text:
            problems.append("на слух показан пример — он содержит ответ")

        # Созвучие: хотя бы один неверный начинается так же
        bare = main_meaning(word, pair.learning)
        article = (word.article or "").strip()
        if article and article != "-" and bare.lower().startswith(article.lower() + " "):
            bare = bare[len(article) + 1:]
        # СРАВНЕНИЕ ЧЕРЕЗ fold, А НЕ .lower().
        #
        # Первая редакция сравнивала `.lower()` и дала восемь «нарушений»,
        # все турецкие: «İstisna».lower() в Python — это «i» с ОТДЕЛЬНОЙ
        # комбинирующей точкой, и со «istisna» оно не сходится. Данные были
        # безупречны: İstisna · İstifa · İstek · İstiridye. Это уже
        # ЧЕТВЁРТЫЙ случай той же ловушки, поэтому `fold` и вынесена в
        # language_service — чтобы не писать сравнение руками впятый раз.
        head = fold(bare[:_prefix_len(bare)])
        others = [t for i, t in enumerate(labels) if i != idx]
        if head and not any(head in fold(t) for t in others):
            problems.append(f"на слух нет ни одного созвучного варианта к {bare!r}")
    else:
        prompt = option_label(word, pair.prompt_lang)
        if prompt and prompt not in text:
            problems.append("в текстовом вопросе нет самого слова")

    return problems


async def _clip_missing(word, lang: str) -> bool:
    """Нет ли клипа на диске. Через хранилище, а НЕ через clip_for_user."""
    kind = clip_kind_for_question(word, lang)
    spoken = spoken_for(word, lang, kind)
    if not spoken:
        return True
    return audio_store.read(lang, default_voice(lang), kind, spoken) is None


async def run(per_case: int) -> int:
    from app.bot.handlers.quiz.game import _question_text

    cases = [
        (learning, native, reverse)
        for learning in LEARNABLE_LANGS
        for native in LEARNABLE_LANGS
        if learning != native
        for reverse in (False, True)
    ]

    totals = collections.Counter()
    failures: list[str] = []
    no_clip: list[str] = []
    fell_back = collections.Counter()

    async with AsyncSessionLocal() as session:
        for learning, native, reverse in cases:
            pair = LanguagePair(learning=learning, native=native, reverse=reverse)
            arrow = "←" if reverse else "→"
            case = f"{learning}{arrow}{native}"

            for want in (QuizChannel.TEXT, QuizChannel.AUDIO):
                # Канал НАВЯЗЫВАЕТСЯ параметром, а не составом занятия.
                #
                # Первая редакция навязывала составом — и проверка прошла
                # вхолостую: у подопытного нет прогресса, правило допуска к
                # слуху требует одного верного ответа, и все 360 вопросов на
                # слух молча откатились в текст. Отчёт при этом сказал «все
                # игры собираются верно». Ровно тот ложный зелёный, против
                # которого приёмка и ставится.
                user = _probe_user("ta")
                used: list[int] = []

                for _ in range(per_case):
                    question = await generate_question(
                        session, user, exclude_ids=used, pair=pair,
                        recent_channels=[], channel=want,
                    )
                    if question is None:
                        failures.append(f"{case} {want.name}: вопрос не собрался")
                        break

                    word = question["correct_word"]
                    used.append(word.id)
                    got = question["channel"]
                    totals[(case, got.name)] += 1

                    if want is QuizChannel.AUDIO and got is QuizChannel.TEXT:
                        # Законный откат: созвучных соседей не нашлось
                        fell_back[case] += 1
                        continue

                    text = _question_text(
                        word, pair, "ru", 1, per_case, channel=got
                    )
                    for problem in _check(question, pair, text):
                        failures.append(f"{case} {got.name} ряд {word.id}: {problem}")

                    if got is QuizChannel.AUDIO and await _clip_missing(word, learning):
                        no_clip.append(f"{case} ряд {word.id}")

    asked = sum(totals.values())
    print(f"\nсочетаний проверено: {len(cases)} (пар 30 × 2 направления)")
    print(f"вопросов сгенерировано: {asked}")
    print(f"откатов со слуха на текст: {sum(fell_back.values())} "
          f"({100 * sum(fell_back.values()) / max(asked, 1):.1f}%)")

    if fell_back:
        worst = fell_back.most_common(5)
        print("  чаще всего откатывается: " +
              ", ".join(f"{c} ({n})" for c, n in worst))

    if no_clip:
        print(f"\nНЕТ КЛИПА НА ДИСКЕ: {len(no_clip)}")
        for line in no_clip[:10]:
            print(f"   {line}")

    if failures:
        print(f"\nНАРУШЕНИЙ: {len(failures)}")
        for line in failures[:25]:
            print(f"   {line}")
        if len(failures) > 25:
            print(f"   … и ещё {len(failures) - 25}")
        return 1

    if no_clip:
        return 1

    print("\nвсе игры собираются верно на всех парах и в обе стороны")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--per-case", type=int, default=10,
                        help="вопросов на каждое сочетание (по умолчанию 10)")
    args = parser.parse_args()
    return asyncio.run(run(args.per_case))


if __name__ == "__main__":
    raise SystemExit(main())
