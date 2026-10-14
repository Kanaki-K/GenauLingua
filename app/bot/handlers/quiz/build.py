"""
🧱 «Собираю» — сборка фразы из кнопок-слов: экран, нажатия, разбор.

Логика (годность примера, ловушки, сравнение) — в `app/services/
build_service.py`; здесь только то, что видит и нажимает человек. В
`question.py` и `lesson.py` — лишь точки встраивания: вопрос этой игрой задаёт круг, а
ответ записывается общим `_record_answer`, как у всех игр.

УСТРОЙСТВО ЭКРАНА. Одно сообщение, правится на месте — как карточка и
доска. Озвучки в вопросе нет (решение владельца).

    3 / 15 · 🧱

    После еды мы идём гулять

    nach dem ▢ ▢ ▢

    [ gehen ] [ den   ]
    [ wir   ] [ Essen ]
    [ raus  ] [ ihr   ]
    [ ⌫ ]

СОБРАННОЕ — СТРОКОЙ В ТЕКСТЕ, ВНИЗУ — ТОЛЬКО НЕИСПОЛЬЗОВАННОЕ, В ДВЕ
КОЛОНКИ, НЕ БОЛЬШЕ ДЕСЯТИ. Так решил владелец после двух живых тестов
14.10. Первый вид оставлял нажатое слово в сетке точкой «·», а лишние
слова висели и после сборки: «висят как бесполезные». Второй ставил
собранное кнопками-местами ▢ над словами: «половина из них — пустые
клетки… перенагружает и делает этот вид игры "душным". Было хорошо, когда
заполнялся текст на экране». Нажатое слово уходит из сетки, «⌫» убирает
последнее, а когда места заняты, сетки нет — одна «Проверить».

ДВОЙНЫЕ И УСТАРЕВШИЕ НАЖАТИЯ. Как у доски: в `callback_data` — номер
слова и ВЕРСИЯ сетки, нажатия идут под замком чата (`lesson_state._claim_lock`).
Номер слова отличает сетку нынешнего вопроса от сетки прошлого, версия —
нынешнее состояние от того, что человек видел до своего же прошлого
нажатия. «Проверить» занимает вопрос (`S_ANSWERED`) под тем же замком,
что и ответы остальных игр: двойная проверка не запишет двух ответов, а
нажатие по сетке после проверки не перерисует разбор обратно в сетку.
"""

from __future__ import annotations

import html
import logging
from typing import Optional

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.clock import utcnow
from app.database.enums import QuizChannel
from app.database.models import User, Word
from app.locales import DEFAULT_LOCALE, get_text
from app.services.build_service import (
    GRID_COLUMNS, Puzzle, Verdict, judge, sentence_tokens,
)
from app.services.language_service import (
    LanguagePair, example_text, pair_from_user,
)

logger = logging.getLogger(__name__)

router = Router()

# Ключи состояния сетки
S_WORD = "build_word"                # id слова: сетка какого вопроса
S_TILES = "build_tiles"              # кнопки в порядке на экране
S_TARGET = "build_target"            # слова фразы — эталон
S_PICKED = "build_picked"            # номера нажатых кнопок по порядку
S_VERSION = "build_version"          # защита от устаревших нажатий
S_SENTENCE = "build_sentence"        # фраза на изучаемом, с пунктуацией
S_TRANSLATION = "build_translation"  # она же на родном — задание

SLOT = "▢"


def initial_state(puzzle: Puzzle, word_id: int) -> dict:
    """Состояние новой сетки — его кладёт в FSM круг, задав вопрос."""
    return {
        S_WORD: word_id,
        S_TILES: list(puzzle.tiles),
        S_TARGET: list(puzzle.target),
        S_PICKED: [],
        S_VERSION: 0,
        S_SENTENCE: puzzle.sentence,
        S_TRANSLATION: puzzle.translation,
    }


# ============================================================================
# ЭКРАН
# ============================================================================

def render_text(lang: str, current: int, total: int, translation: str,
                picked_words: list[str], slots: int) -> str:
    """
    Текст вопроса: номер, фраза на родном, собранное и пропуски.

    Собранное и пропуски — одной строкой, пропусков ровно столько, сколько
    слов ещё не хватает: длина фразы видна сразу, и человек не гадает,
    сколько нажимать. Владелец: «было хорошо, когда заполнялся текст на
    экране».
    """
    from app.bot.handlers.quiz.question import channel_mark

    number = get_text("quiz_question_number", lang, current=current, total=total)
    built = [html.escape(w, quote=False) for w in picked_words]
    built += [SLOT] * max(0, slots - len(picked_words))
    return (
        f"{number} · {channel_mark(QuizChannel.BUILD)}\n\n"
        f"<b>{html.escape(translation, quote=False)}</b>\n\n"
        f"{' '.join(built)}\n\n"
        f"<i>{get_text('build_hint', lang)}</i>"
    )


def question_text_for(word: Word, pair: LanguagePair, lang: str,
                      current: int, total: int) -> str:
    """Экран только что заданного вопроса — ничего ещё не собрано."""
    target = sentence_tokens(word, pair) or []
    return render_text(lang, current, total,
                       example_text(word, pair.native), [], len(target))


def grid_keyboard(tiles: list[str], picked: list[int], word_id: int,
                  version: int, lang: str, slots: int = 0) -> InlineKeyboardMarkup:
    """
    Неиспользованные слова в две колонки и ряд управления под ними.

    Нажатое слово УХОДИТ из сетки — собранное видно строкой в тексте, и
    кнопка-точка на его месте была бы шумом. Номер в `bd:t:<номер>` — номер
    слова в исходной сетке, он не меняется от сдвига кнопок, поэтому
    нажатие по прежней раскладке ставит то самое слово. КОГДА МЕСТА ЗАНЯТЫ,
    сетки нет: лишние слова больше не нужны, остаются «⌫» и «Проверить».

    Одинаковые слова («die … die») — разные кнопки: у каждой свой номер.
    """
    rows: list[list] = []
    full = bool(slots) and len(picked) >= slots
    if not full:
        pool = [
            InlineKeyboardButton(text=tile, callback_data=f"bd:t:{index}:{word_id}:{version}")
            for index, tile in enumerate(tiles) if index not in picked
        ]
        rows += [pool[i:i + GRID_COLUMNS] for i in range(0, len(pool), GRID_COLUMNS)]

    controls = []
    if picked:
        controls.append(InlineKeyboardButton(
            text="⌫", callback_data=f"bd:back:{word_id}:{version}",
        ))
    if full:
        controls.append(InlineKeyboardButton(
            text=get_text("build_btn_check", lang),
            callback_data=f"bd:check:{word_id}:{version}",
        ))
    if controls:
        rows.append(controls)
    return InlineKeyboardMarkup(inline_keyboard=rows)


def _sentence_block(sentence: str, translation: str) -> str:
    """Эталон с пунктуацией — полужирным, перевод — курсивом через строку."""
    out = f"<b>{html.escape(sentence, quote=False)}</b>"
    if translation:
        out += f"\n\n<i>{html.escape(translation, quote=False)}</i>"
    return out


def result_text(verdict: Verdict, answer: list[str], sentence: str,
                translation: str, lang: str) -> str:
    """
    Разбор сборки. Три исхода, и у каждого свой экран:

        верно             «✓ Верно», эталон, перевод
        слова не те       фраза человека с ✓/✗ у каждого слова, что лишнее,
                          чего не хватило, и эталон
        порядок другой    мягкая формулировка: в немецком часто верны два
                          порядка, а бот знает один — человек мог быть прав.
                          Засчитывается всё равно НЕверным: проверить второй
                          порядок боту нечем, а засчитать любой порядок
                          значило бы не проверять порядок вовсе
    """
    reference = _sentence_block(sentence, translation)
    if verdict.correct:
        return f"{get_text('quiz_correct', lang)}\n\n{reference}"

    yours = get_text("build_yours", lang)
    label = get_text("build_reference", lang)
    if verdict.same_words:
        plain = html.escape(" ".join(answer), quote=False)
        return (f"{get_text('build_order_only', lang)}\n\n"
                f"{yours} {plain}\n\n{label}\n{reference}")

    marked = " ".join(
        f"{html.escape(word, quote=False)}✓" if ok else f"<u>{html.escape(word, quote=False)}</u>✗"
        for word, ok in zip(answer, verdict.marks)
    )
    lines = [get_text("quiz_wrong", lang), "", f"{yours} {marked}"]
    if verdict.extra:
        extra = html.escape(", ".join(verdict.extra), quote=False)
        lines.append(get_text("build_extra", lang, words=extra))
    if verdict.missing:
        missing = html.escape(", ".join(verdict.missing), quote=False)
        lines.append(get_text("build_missing", lang, words=missing))
    lines += ["", label, reference]
    return "\n".join(lines)


# ============================================================================
# НАЖАТИЯ
# ============================================================================

def _parse(data: str) -> Optional[tuple[str, int, int, int]]:
    """
    `bd:t:<кнопка>:<слово>:<версия>` — поставить слово,
    `bd:u:<место>:<слово>:<версия>` — вернуть слово с места вниз,
    `bd:back:<слово>:<версия>` — убрать последнее (кнопка прежней сетки,
    живёт в переписке), `bd:check:<слово>:<версия>`
    → (действие, кнопка или место, слово, версия).

    Всё прочее — None. Не исключение: в переписке живут кнопки прошлых
    версий бота, а обход экранов нажимает шаблоны вроде `bd:t:X`, и ни то,
    ни другое не должно ронять обработчик.
    """
    parts = data.split(":")
    try:
        if len(parts) == 5 and parts[1] in ("t", "u"):
            return parts[1], int(parts[2]), int(parts[3]), int(parts[4])
        if len(parts) == 4 and parts[1] in ("back", "check"):
            return parts[1], -1, int(parts[2]), int(parts[3])
    except ValueError:
        return None
    return None


def _live(data: dict, word_id: int, version: int) -> bool:
    """Нажатие относится к НЫНЕШНЕЙ сетке и вопрос ещё не отвечен."""
    from app.bot.handlers.quiz.lesson_state import S_ANSWERED

    return (
        data.get("channel") == QuizChannel.BUILD.value
        and int(data.get(S_WORD) or 0) == word_id
        and int(data.get(S_VERSION) or 0) == version
        and data.get(S_ANSWERED) != data.get("current_question")
    )


@router.callback_query(F.data.startswith("bd:"))
async def press(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    """Нажатие по сетке: слово, возврат слова с места, «⌫» или «Проверить»."""
    parsed = _parse(callback.data or "")
    if parsed is None:
        await callback.answer()
        return
    action, index, word_id, version = parsed
    if action == "check":
        await _check(callback, state, session, word_id, version)
        return

    from app.bot.handlers.quiz.lesson_state import _claim_lock

    # ЦЕЛИКОМ ПОД ЗАМКОМ ЧАТА, как нажатие по доске: проверка версии и её
    # увеличение разделены несколькими `await`, а aiogram ведёт нажатия
    # параллельно — двойной тык поставил бы одно слово дважды
    async with _claim_lock(callback.message.chat.id):
        await _tap(callback, state, session, action, index, word_id, version)


async def _tap(callback: CallbackQuery, state: FSMContext, session: AsyncSession,
               action: str, index: int, word_id: int, version: int) -> None:
    data = await state.get_data()
    if not _live(data, word_id, version):
        # Устаревшее нажатие или сетка прошлого вопроса — молча гасим: это
        # не ошибка человека, он нажал быстрее, чем пришёл ответ
        await callback.answer()
        return

    tiles: list[str] = list(data.get(S_TILES) or [])
    target: list[str] = list(data.get(S_TARGET) or [])
    picked: list[int] = list(data.get(S_PICKED) or [])

    user = await session.get(User, callback.from_user.id)
    lang = (user.interface_language if user else None) or DEFAULT_LOCALE

    if action == "t":
        if not 0 <= index < len(tiles) or index in picked:
            await callback.answer()
            return
        if len(picked) >= len(target):
            # Пропуски кончились: слово ставить некуда. Подсказать, а не
            # промолчать — иначе нажатие выглядело бы сломанным
            await callback.answer(get_text("build_full", lang), show_alert=True)
            return
        picked.append(index)
    elif action == "u":                     # слово с места — обратно вниз
        if not 0 <= index < len(picked):
            await callback.answer()
            return
        picked.pop(index)
    else:                                   # «⌫» прежней сетки
        if not picked:
            await callback.answer()
            return
        picked.pop()

    version += 1
    await state.update_data(**{S_PICKED: picked, S_VERSION: version})
    await callback.answer()

    words = [tiles[i] for i in picked]
    try:
        await callback.message.edit_text(
            render_text(lang, int(data.get("current_question") or 1),
                        int(data.get("total_questions") or 1),
                        data.get(S_TRANSLATION) or "", words, len(target)),
            reply_markup=grid_keyboard(tiles, picked, word_id, version, lang,
                                       slots=len(target)),
        )
    except Exception:
        # Правка не удалась — сетка всё равно в состоянии, следующее
        # нажатие её перерисует
        logger.debug("правка сетки не удалась", exc_info=True)


async def _claim_check(state: FSMContext, chat_id: int, word_id: int,
                       version: int) -> Optional[dict]:
    """
    Занять вопрос проверкой РОВНО ОДИН РАЗ — и только по нынешней, полной
    сетке. Возвращает состояние, по которому проверять, или None.

    Сверка и отметка «ответ принят» — под одним замком, тем же, что у
    ответов остальных игр (`lesson_state._claim_answer`). Раздельно они пропустили
    бы двойное «Проверить» (две строки ответа, балл дважды) и «⌫»,
    пришедший между проверкой версии и записью.
    """
    from app.bot.handlers.quiz.lesson_state import S_ANSWERED, _claim_lock

    async with _claim_lock(chat_id):
        data = await state.get_data()
        if not _live(data, word_id, version):
            return None
        if len(data.get(S_PICKED) or []) != len(data.get(S_TARGET) or []):
            return None
        await state.update_data(**{S_ANSWERED: data.get("current_question")})
        return data


async def _check(callback: CallbackQuery, state: FSMContext, session: AsyncSession,
                 word_id: int, version: int) -> None:
    """«Проверить»: сравнить, записать ответ общим путём, показать разбор."""
    from app.bot.handlers.quiz.lesson import _record_answer

    data = await _claim_check(state, callback.message.chat.id, word_id, version)
    if data is None:
        await callback.answer()
        return

    user = await session.get(User, callback.from_user.id)
    word = await session.get(Word, word_id)
    if not user or not word:
        await callback.answer("Error", show_alert=True)
        return

    lang = user.interface_language or DEFAULT_LOCALE
    pair = pair_from_user(user)
    tiles: list[str] = list(data.get(S_TILES) or [])
    answer = [tiles[i] for i in data.get(S_PICKED) or []]
    verdict = judge(list(data.get(S_TARGET) or []), answer, pair.learning)
    breakdown = result_text(verdict, answer, data.get(S_SENTENCE) or "",
                            data.get(S_TRANSLATION) or "", lang)

    asked_at = data.get("asked_at")
    response_seconds = (
        max(0, int(utcnow().timestamp() - float(asked_at))) if asked_at else None
    )

    # Запись — ОБЩИМ ПУТЁМ, как у любой игры: строка ответа с каналом «b»,
    # счётчики занятия, прогресс слова (`shown_build`/`correct_build`),
    # ошибка круга для «Повторить ошибки» и звук полного клипа на разборе,
    # если озвучка включена. Своей записи у сборки нет нарочно — она
    # разошлась бы с остальными при первой же правке учёта
    await _record_answer(
        bot=callback.bot, chat_id=callback.message.chat.id, state=state,
        session=session, user=user, pair=pair, lang=lang,
        correct_word=word, is_correct=verdict.correct,
        channel=QuizChannel.BUILD,
        # Что собрал человек — то и в строке ответа: по ней видно, какие
        # ловушки притягивают
        answer_text=" ".join(answer),
        card_message=callback.message,
        session_id=data["session_id"],
        correct_answers=data.get("correct_answers", 0),
        errors=list(data.get("errors") or []),
        response_seconds=response_seconds,
        breakdown=breakdown,
    )
    await callback.answer()
