"""
Звук вопроса и откат «Слышу» на «Читаю», когда звука нет.

Вынесено из `game.py` переносом, без правок поведения.
"""

import logging

from aiogram.fsm.context import FSMContext

from app.bot.handlers.quiz.question import _question_keyboard, _question_text
from app.database.enums import QuizChannel
from app.database.models import User, Word
from app.services.audio_service import (
    KIND_BLIND,
    KIND_FULL,
    warm_clip,
    clip_for_user,
    clip_kind_for_question,
)
from app.services.language_service import LanguagePair, pair_for_channel
from app.services.quiz_service import OPTIONS_TOTAL, build_options, get_distractors

logger = logging.getLogger(__name__)


# ============================================================================
# ОТОБРАЖЕНИЕ ВОПРОСА И ОТВЕТА
# ============================================================================

async def _question_clip(
    session, user: User, word: Word, pair: LanguagePair,
    channel: QuizChannel = QuizChannel.TEXT,
):
    """
    Озвучка для вопроса.

    НА СЛУХ КЛИП — ЭТО И ЕСТЬ ВОПРОС, и направление на него не влияет.
    Обратного порядка у слушания не существует: звучит изучаемый язык, из
    него и выбирают.

    У ПЯТОЙ ИГРЫ ЗВУКА НЕТ, И ЭТО НЕ МЕЛОЧЬ. Она спрашивает значением —
    «металл по-немецки?» — а произнести при этом само слово означало бы
    назвать ответ голосом. Проверка эта была и прежде, но смотрела на
    `pair.reverse`, то есть на НАСТРОЙКУ человека; направление стало
    свойством игры, и смотреть надо на канал. Иначе озвучка выдавала бы
    ответ в каждом обратном вопросе — а их теперь получают все.

    В прямом направлении звучит слово. Исключение — гетероним: произнесённый
    отдельно, он читается наугад («modern», «umfahren» имеют по два чтения),
    и управлять этим нельзя, SSML движку недоступен. Такому слову ставится
    клип с примером, где контекст задаёт чтение однозначно.
    """
    # Звук разбора (слово с примером) начинает готовиться уже сейчас, пока
    # человек думает: после ответа он берётся с диска, а не синтезируется.
    # Язык — изучаемый из настроек, как у разбора, до разворота по игре
    await warm_clip(session, user, word, pair.learning, KIND_FULL)
    pair = pair_for_channel(pair, channel)

    # 🧱 У СБОРКИ ЗВУКА В ВОПРОСЕ НЕТ — решение владельца: «на экране
    # вопроса озвучка не нужна». Клип слова с примером назвал бы ответ
    # голосом, а клип одного слова — подсказал бы, какое из него собирать.
    # Звук — на разборе, как у остальных игр
    if channel is QuizChannel.BUILD:
        return None

    if channel is QuizChannel.AUDIO:
        # ВСЕГДА ОДНО СЛОВО, даже для гетеронима.
        #
        # Карточке клип с примером нужен: там слово видно, и прочитанное
        # наугад («live» как /lɪv/ или /laɪv/) учило бы неверному
        # произношению. На слух этой беды нет — оба чтения ПИШУТСЯ
        # одинаково, а спрашивают тут именно написание.
        #
        # Зато вред от примера настоящий: 109 рядов проигрывали бы целое
        # предложение — «to live … We like living in this city» — при
        # вариантах из одного слова. Это другая задача, заметно более
        # лёгкая, и соседние вопросы круга оказывались бы разной трудности
        # без всякой причины.
        #
        # И ВСЛЕПУЮ: у клипа слова название — само слово, и плеер Telegram
        # показывал ответ прямо над вариантами (`KIND_BLIND`).
        return await clip_for_user(session, user, word, pair.learning, KIND_BLIND)
    if pair.reverse:
        return None
    return await clip_for_user(
        session, user, word, pair.learning, clip_kind_for_question(word, pair.learning)
    )


async def _clip_or_text(
    session, user: User, word: Word, pair: LanguagePair, channel: QuizChannel,
    options: list,
):
    """
    Клип для вопроса, а если его нет — ПЕРЕСОБРАТЬ вопрос текстом.

    Вопрос на слух держится на звуке: самого слова на экране нет, его
    заменяет клип. Если клип не пришёл, на экране остаётся «Послушай и
    выбери» и четыре варианта — вопрос без вопроса, на который можно только
    ткнуть наугад.

    Клип не приходит по трём причинам, и все три настоящие: ученик выключил
    озвучку (это уже отсекается составом занятия), клипа нет на диске для
    выбранного голоса, синтез не ответил. Последние две предсказать нельзя:
    на неосновных голосах синтез срывается примерно в одном случае из
    десяти, а голос ученик выбирает сам.

    Поэтому решение принимается ЗДЕСЬ, после попытки получить звук, а не
    при сборке вопроса: только здесь известно, есть он или нет.

    Возвращает (клип, канал, варианты). Канал в ответе может отличаться от
    запрошенного — тогда и засчитан ответ будет текстовым, что верно: на
    слух ученик его не давал.
    """
    clip = await _question_clip(session, user, word, pair, channel)
    if channel is not QuizChannel.AUDIO or clip is not None:
        return clip, channel, options

    logger.info(
        "клип для вопроса на слух не получен (ряд %s, %s) — спрашиваю текстом",
        word.id, pair.learning,
    )
    distractors = await get_distractors(word, session, pair, user=user)
    if len(distractors) < OPTIONS_TOTAL - 1:
        # Текстом тоже не собрать — отдаём как есть, звука не будет.
        # Случай крайний: четырёх различимых вариантов не нашлось ни так, ни так
        return clip, channel, options

    text_options, _ = build_options(word, distractors, pair)
    fallback_clip = await _question_clip(session, user, word, pair, QuizChannel.TEXT)
    return fallback_clip, QuizChannel.TEXT, text_options


def _as_text_question(
    session, user: User, word: Word, pair: LanguagePair, state: FSMContext,
    lang: str, current: int, total: int, channel: QuizChannel,
):
    """
    Пересборка вопроса на слух в «Читаю», если звук пропал ПРИ ОТПРАВКЕ.

    `_clip_or_text` решает то же при сборке, но file_id может умереть уже в
    Telegram: тогда клип отвергается на отправке, и вопрос уходил текстом
    «Послушай и выбери» без слова. Канал в состоянии меняется на текст —
    засчитан ответ будет так, как его давали.
    """
    if channel is not QuizChannel.AUDIO:
        return None

    async def rebuild():
        distractors = await get_distractors(word, session, pair, user=user)
        if len(distractors) < OPTIONS_TOTAL - 1:
            return None
        options, _ = build_options(word, distractors, pair)
        await state.update_data(channel=QuizChannel.TEXT.value)
        return (
            _question_text(word, pair, lang, current, total,
                           channel=QuizChannel.TEXT),
            _question_keyboard(QuizChannel.TEXT, options, lang),
        )

    return rebuild
