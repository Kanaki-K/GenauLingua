# -*- coding: utf-8 -*-
"""
ПРИЁМКА ВСЕХ ИГР: прогон вопросов по всем парам языков и всем каналам.

    python -m app.scripts.verify_quiz_channels
    python -m app.scripts.verify_quiz_channels --per-case 40

ЗАЧЕМ. Владелец дословно: «убедись, что все игры работают как надо, без
поломок... я не в состоянии проверить все языки и остальное». Проверить
руками тут и правда нельзя: шесть изучаемых языков на пять языков значения
дают 30 пар, и каждая проверяется ЧЕТЫРЬМЯ каналами: карточка,
припоминание, слух, речь. Сто двадцать сочетаний — нажать их все
невозможно, а сломаться может каждое.

НАПРАВЛЕНИЯ В СЛУЧАЯХ НЕТ НАРОЧНО. Оно было настройкой на весь круг и
стало ПЯТОЙ ИГРОЙ, то есть каналом (`QuizChannel.REVERSE`). Прежний цикл
по `reverse` после этого проверял бы прямую сторону дважды — и приёмка
осталась бы зелёной, потеряв половину покрытия.

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
from app.services.language_service import (
    pair_for_channel,  # noqa: E402
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


def _check_build(question: dict, pair: LanguagePair, text: str) -> list[str]:
    """
    🧱 Сборка: вариантов нет, есть кнопки-слова. Проверяется то, без чего
    вопрос нельзя решить или можно решить, не зная языка:

        эталон      3–10 слов, все они есть среди кнопок (с повторами)
        кнопок      не больше двенадцати, ловушек от двух до четырёх
        ловушки     ни одна не совпадает со словом фразы — иначе две
                    одинаковые кнопки и неоднозначная проверка
        порядок     кнопки стоят НЕ в порядке фразы — иначе ответ готов
        экран       перевод на родном показан, фраза на изучаемом — НЕТ
    """
    import collections

    from app.services.build_service import (
        MAX_TILES, MAX_WORDS, MIN_DISTRACTORS, MIN_WORDS,
    )

    problems: list[str] = []
    puzzle = question.get("build")
    if puzzle is None:
        return ["сборка без задачи"]
    target, tiles = puzzle.target, puzzle.tiles
    if not MIN_WORDS <= len(target) <= MAX_WORDS:
        problems.append(f"в эталоне {len(target)} слов")
    if len(tiles) > MAX_TILES:
        problems.append(f"кнопок {len(tiles)} — больше {MAX_TILES}")
    if collections.Counter(target) - collections.Counter(tiles):
        problems.append("не все слова эталона есть среди кнопок")
    if len(puzzle.distractors) < MIN_DISTRACTORS:
        problems.append(f"ловушек {len(puzzle.distractors)}")
    if {fold(d) for d in puzzle.distractors} & {fold(t) for t in target}:
        problems.append(f"ловушка совпадает со словом фразы: {puzzle.distractors}")
    if tiles[:len(target)] == target:
        problems.append("кнопки стоят в порядке фразы — ответ готов")
    # Экран — в HTML, и фраза в нём экранирована так же, как её экранирует
    # сам экран (`build.py`): сверка сырой строки дала 11 ложных нарушений
    # на фразах с апострофом
    import html

    if puzzle.translation and html.escape(puzzle.translation, quote=False) not in text:
        problems.append("на экране нет фразы на родном — собирать нечего")
    if puzzle.sentence and html.escape(puzzle.sentence, quote=False) in text:
        problems.append("на экране эталон — собирать незачем")
    return problems


def _check(question: dict, pair: LanguagePair, text: str) -> list[str]:
    """Содержательные проверки одного вопроса. Пустой список — всё верно."""
    problems: list[str] = []
    word = question["correct_word"]
    options = question["options"]
    channel = question["channel"]
    idx = question["correct_answer_index"]

    if channel is QuizChannel.BUILD:
        return _check_build(question, pair, text)

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

    # Ни один неверный вариант не должен значить того же, что верный.
    #
    # Язык ответа берётся ПО КАНАЛУ: направление стало свойством игры, и
    # пара, пришедшая снаружи, всегда прямая. Пятая игра ждёт ответа на
    # изучаемом языке, как и слух, — но по другой причине: там спрашивают
    # значением
    channel_pair = pair_for_channel(pair, channel)
    answer_lang = (
        pair.learning if channel is QuizChannel.AUDIO
        else channel_pair.answer_lang
    )
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
    elif channel is QuizChannel.SPEECH:
        # ВСЛУХ СЛОВО ПОКАЗАНО, И ВСЕГДА НА ИЗУЧАЕМОМ ЯЗЫКЕ — в обоих
        # направлениях. Произнести можно только то, что видишь, а
        # произносят здесь изучаемый язык; обратного порядка у речи не
        # существует, как и у слушания.
        #
        # Отсюда и отличие от текстового вопроса: там слово стоит на языке
        # ВОПРОСА (`prompt_lang`), и при обратном направлении это язык
        # значения. Сверь речь тем же полем — и в обратном направлении
        # получишь ложное нарушение на совершенно верных данных.
        shown = option_label(word, pair.learning)
        if shown and shown not in text:
            problems.append("вслух слова на экране нет — произносить нечего")
        if "📝" in text:
            problems.append("вслух показан пример — он подталкивает прочесть фразу")
    else:
        # Язык ВОПРОСА — по каналу, как и в коде. Прежде здесь стояло
        # `pair.prompt_lang` от пары, пришедшей снаружи, и для пятой игры
        # это давало 175 ложных нарушений: проверка искала в карточке
        # немецкое слово, а карточка показывает значение. Ожидание обязано
        # следовать тому же правилу, по которому вопрос собран, — иначе
        # приёмка ругается на верный код и прячет настоящие дефекты в шуме.
        prompt = option_label(word, channel_pair.prompt_lang)
        if prompt and prompt not in text:
            problems.append(
                f"в вопросе каналом {channel.value} нет самого задания"
            )

    return problems


def _voices_in_use(lang: str) -> list[str]:
    """
    Все голоса, которыми база РЕАЛЬНО озвучена, а не весь список движка.

    У движка их по шесть на немецкий, и пять из них базе неизвестны. Голос
    считается рабочим по доле покрытия — тем же способом, что в
    `verify_voices`, и по той же причине: у неиспользуемого голоса бывает
    горстка случайных клипов, и проверка «есть ли хоть один» их не отличает.
    """
    from app.services.tts_voices import voices_for

    root = pathlib.Path("tts") / lang
    if not root.exists():
        return [default_voice(lang)]

    counted = []
    for voice in voices_for(lang):
        folder = root / voice.name
        if folder.exists():
            counted.append((voice.name, sum(1 for _ in folder.rglob("*.mp3"))))
    if not counted:
        return [default_voice(lang)]

    biggest = max(n for _, n in counted)
    # Половина от самого полного — с запасом в обе стороны: озвученные
    # голоса идут наравне, случайные пробы отстают на порядки
    return [name for name, n in counted if n >= biggest * 0.5] or [default_voice(lang)]


async def _clips_missing(word, lang: str) -> list[str]:
    """
    Голоса, у которых НЕТ клипа для этого вопроса.

    Проверяется КАЖДЫЙ рабочий голос, а не только основной. Прежде здесь
    стоял `default_voice`, то есть вопрос «есть ли чем озвучить» задавался
    про женский голос — а человек выбирает голос сам, и мужские
    синтезировались отдельным прогоном. Полнота по ним проверена
    (`verify_voices`), но здесь важно другое: что клип найдётся по тому же
    пути, которым его ищет вопрос, — вид клипа и произносимый текст зависят
    от слова, а не от голоса, и ошибка в них ударила бы по всем голосам
    сразу.

    Через хранилище, а НЕ через `clip_for_user`: тот при отсутствии клипа
    идёт синтезировать по сети и замаскировал бы ровно ту дыру, которую ищем.
    """
    kind = clip_kind_for_question(word, lang)
    spoken = spoken_for(word, lang, kind)
    if not spoken:
        return _voices_in_use(lang)
    return [
        voice for voice in _voices_in_use(lang)
        if audio_store.read(lang, voice, kind, spoken) is None
    ]


async def run(per_case: int) -> int:
    from app.bot.handlers.quiz.question import _question_text

    # НАПРАВЛЕНИЯ В СЛУЧАЯХ БОЛЬШЕ НЕТ. Оно было прежней настройкой на весь
    # круг и на сборку вопроса не влияет: обратная сторона стала ПЯТОЙ
    # ИГРОЙ, то есть каналом, и проверяется перечислением каналов ниже.
    # Оставь его здесь — и обратная половина тридцати пар проверяла бы ровно
    # то же, что прямая, а приёмка осталась бы зелёной, потеряв половину.
    cases = [
        (learning, native)
        for learning in LEARNABLE_LANGS
        for native in LEARNABLE_LANGS
        if learning != native
    ]

    totals = collections.Counter()
    failures: list[str] = []
    no_clip: list[str] = []
    fell_back = collections.Counter()
    build_fell_back = collections.Counter()

    async with AsyncSessionLocal() as session:
        for learning, native in cases:
            pair = LanguagePair(learning=learning, native=native)
            case = f"{learning}→{native}"

            # ВСЕ КАНАЛЫ ИЗ ПЕРЕЧИСЛЕНИЯ, а не список руками.
            #
            # Прежде речи здесь не было вовсе: она появилась позже и в
            # перечисление не попала. Выходило, что третья игра на 30 парах
            # не проверялась НИКОГДА — её держала только приёмка круга, а та
            # идёт по десятку подобранных случаев. Пятая игра повторила бы
            # эту историю, поэтому список берётся из `QuizChannel`.
            for want in QuizChannel:
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
                    if want is QuizChannel.BUILD and got is QuizChannel.TEXT:
                        # Законный откат: пример короче трёх слов или длиннее
                        # десяти. Канал навязан мимо подбора, а подбор такие
                        # слова сборкой не задаёт (`channel_fits`)
                        build_fell_back[case] += 1
                        continue

                    text = _question_text(
                        word, pair, "ru", 1, per_case, channel=got
                    )
                    for problem in _check(question, pair, text):
                        failures.append(f"{case} {got.name} ряд {word.id}: {problem}")

                    # ЗВУК НУЖЕН ДВУМ КАНАЛАМ ИЗ ТРЁХ, и по разным причинам.
                    #
                    # На слух клип — это и есть вопрос: слова на экране нет.
                    # Вслух слово показано, но клип нужен не меньше — им
                    # человек слушает ЭТАЛОН, чтобы сравнить себя. Без
                    # эталона упражнение превращается в «скажи что-то, я
                    # угадаю», и половина пользы теряется.
                    if got in (QuizChannel.AUDIO, QuizChannel.SPEECH):
                        missing_voices = await _clips_missing(word, learning)
                        for voice in missing_voices:
                            no_clip.append(f"{case} {got.name} ряд {word.id} — {voice}")

    asked = sum(totals.values())
    by_channel = collections.Counter()
    for (_, channel_name), count in totals.items():
        by_channel[channel_name] += count

    print(f"\nпар проверено: {len(cases)}, каналов у каждой: {len(QuizChannel)}")
    print(f"вопросов сгенерировано: {asked}")
    print("  по каналам: " + ", ".join(
        f"{name} {count}" for name, count in sorted(by_channel.items())
    ))
    print(f"откатов со слуха на текст: {sum(fell_back.values())} "
          f"({100 * sum(fell_back.values()) / max(asked, 1):.1f}%)")

    print(f"откатов со сборки на текст (пример не годится): "
          f"{sum(build_fell_back.values())}")

    if fell_back:
        worst = fell_back.most_common(5)
        print("  чаще всего откатывается: " +
              ", ".join(f"{c} ({n})" for c, n in worst))

    # ЛОЖНЫЙ ЗЕЛЁНЫЙ: канала не было вовсе, и «ок» про него ничего не значит.
    #
    # Проверка нужна на каждый канал, и дважды уже была нужна: первая
    # редакция этой приёмки отрапортовала «все игры собираются верно», не
    # собрав НИ ОДНОГО вопроса на слух (канал навязывался составом, а не
    # параметром). Речь добавлена в перечисление позже, и ровно та же
    # ловушка ждала её.
    empty = [c.name for c in QuizChannel
             if not by_channel.get(c.name)]
    if empty:
        print(f"\nКАНАЛОВ БЕЗ ЕДИНОГО ВОПРОСА: {', '.join(empty)} — "
              f"проверять было нечего, это неудача")
        return 1

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

    print("\nвсе игры собираются верно на всех парах и всеми каналами")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--per-case", type=int, default=10,
                        help="вопросов на каждое сочетание (по умолчанию 10)")
    args = parser.parse_args()
    return asyncio.run(run(args.per_case))


if __name__ == "__main__":
    raise SystemExit(main())
