"""
Доска сопоставления: тыкнуть слово с одной стороны и его пару с другой.

УСТРОЙСТВО ЭКРАНА. Инлайн-клавиатура Telegram с двумя кнопками в ряд — это
и есть две колонки, другого способа нарисовать их в Telegram нет и не
нужно. Пять рядов, одно сообщение, правится на месте — так же, как
карточка.

    [ Verspätung ]   [ привычка  ]
    [ Gewohnheit ]   [ черновик  ]
    [ Entwurf    ]   [ опоздание ]
    [ Sorge      ]   [ забота    ]
    [ Vorteil    ]   [ выгода    ]

ТЫКАТЬ МОЖНО С ЛЮБОЙ СТОРОНЫ. Требование владельца: первое нажатие
выбирает — слева или справа, безразлично, — второе с ПРОТИВОПОЛОЖНОЙ
стороны решает пару. Нажатие по той же стороне переносит выбор, а не
считается промахом: человек передумал, а не ошибся.

ТРИ СОСТОЯНИЯ ЯЧЕЙКИ, и значки выбраны не наугад:

    не тронуто   Verspätung
    выбрано    ▸ Verspätung
    сошлось    ✓ Verspätung

Галочка с крестиком из экрана напоминаний здесь НЕ ГОДЯТСЯ: там они значат
«включено/выключено», а на доске означали бы «верно/неверно». Один значок
на два смысла — уже разобранный дефект, повторять его осознанно незачем.

СОШЕДШАЯСЯ ПАРА ОСТАЁТСЯ НА ДОСКЕ. Убрать её нельзя: левая и правая
половины лежат в РАЗНЫХ рядах, и удаление поломало бы решётку. Галочка
взамен даже лучше: видно накопленное, а оставшееся — то, что без неё.

ПРОМАХ — ВСПЛЫВАШКОЙ, без правки сообщения. Правка ради мигания стоит
лишнего вызова, а Telegram на неизменившейся разметке ещё и отвечает
ошибкой «message is not modified».
"""

from __future__ import annotations

import logging
import random

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.enums import QuizChannel
from app.database.models import User, Word
from app.locales import DEFAULT_LOCALE, get_text
from app.services.language_service import option_label, pair_from_user
from app.services.match_service import (
    BOARD_SIZE, deranged_order, pick_words, scored_pairs,
)
from app.services.quiz_service import update_word_progress

logger = logging.getLogger(__name__)

router = Router()

# Ключи состояния доски
S_WORDS = "match_words"          # id слов, порядок = левая колонка
S_RIGHT = "match_right"          # перестановка для правой колонки
S_MATCHED = "match_matched"      # индексы сошедшихся, в порядке схождения
S_SELECTED = "match_selected"    # «l:2» / «r:4» или пусто
S_ERRORS = "match_errors"        # промахов всего
S_MISSED = "match_missed"        # индексы, по которым промахивались
S_VERSION = "match_version"      # защита от устаревших нажатий

# Номер вопроса круга, на котором доска встала. Пусто — доска открыта сама
# по себе, с домашнего экрана или командой. По нему же доска и возвращает
# круг: занимает она РОВНО ОДИН вопрос, и счётчик остаётся на нём.
S_ROUND_AT = "match_round_at"

MARK_PICKED = "▸ "
MARK_DONE = "✓ "

# Пустышка для сошедшейся кнопки. Нажатие по ней всё равно приходит —
# Telegram не умеет «неактивных» кнопок, — и его надо тихо погасить.
CB_SPENT = "mt:done"


def _cell(data: str, version: int) -> str:
    """
    `callback_data` с НОМЕРОМ ВЕРСИИ доски.

    Версия защищает от устаревших нажатий. Человек может тыкнуть дважды
    быстрее, чем придёт ответ, и оба нажатия приедут с одинаковыми
    данными — вторым обработается уже изменившаяся доска. Виден такой
    дефект был бы редко и выглядел бы как «кнопка сработала сама».

    Шестидесяти четырёх байт, которыми Telegram ограничивает callback_data,
    хватает с избытком: здесь уходит около десяти.
    """
    return f"mt:{data}:{version}"


def board_keyboard(
    left: list[str], right_labels: list[str], right_order: list[int],
    matched: list[int], selected: str, version: int,
) -> InlineKeyboardMarkup:
    """
    Сетка из двух колонок. `right_order[i]` — какая пара стоит в ряду i
    справа.
    """
    rows = []
    for row in range(len(left)):
        right_index = right_order[row]

        left_done = row in matched
        right_done = right_index in matched

        left_mark = MARK_DONE if left_done else (
            MARK_PICKED if selected == f"l:{row}" else ""
        )
        right_mark = MARK_DONE if right_done else (
            MARK_PICKED if selected == f"r:{row}" else ""
        )

        rows.append([
            InlineKeyboardButton(
                text=left_mark + left[row],
                callback_data=CB_SPENT if left_done else _cell(f"l:{row}", version),
            ),
            InlineKeyboardButton(
                text=right_mark + right_labels[right_index],
                callback_data=CB_SPENT if right_done else _cell(f"r:{row}", version),
            ),
        ])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def _board_text(lang: str, matched: int, total: int, errors: int) -> str:
    head = get_text("match_title", lang)
    line = get_text("match_progress", lang, matched=matched, total=total)
    if errors:
        line += " · " + get_text("match_errors", lang, count=errors)
    return f"{head}\n\n{line}\n\n<i>{get_text('match_hint', lang)}</i>"


# ============================================================================
# ЗАПУСК
# ============================================================================

async def start_board(
    message: Message, state: FSMContext, session: AsyncSession, user: User
) -> bool:
    """
    Собрать и показать доску. Возвращает False, если собирать было не из чего.

    Отказ — это НЕ ошибка: на доску идут только знакомые слова с короткими
    подписями, и у новичка их попросту нет. Честный ответ «ещё рано» лучше
    доски из двух пар, где обе бесплатны.
    """
    lang = user.interface_language or DEFAULT_LOCALE
    pair = pair_from_user(user)

    # УЖЕ ЗАДАННЫЕ В КРУГЕ СЛОВА ДОСКА НЕ БЕРЁТ.
    #
    # Список читается из состояния, а не передаётся параметром: доска
    # открывается ТРЕМЯ путями — командой, кнопкой с домашнего экрана и
    # внутри круга, — и у первых двух круга нет, значит и списка. Один
    # источник, и у каждого пути он верный сам собой.
    #
    # Прежде списка не было вовсе, и приёмка круга поймала это на первом же
    # сочетании: доска повторяла слово, спрошенное несколькими вопросами
    # раньше. Прогресс по такому слову двигался в одном круге дважды.
    data = await state.get_data()
    used = list(data.get("used_word_ids") or [])

    # Уровень и режим НЕ передаются: `pick_words` берёт их сама, тем же
    # фильтром, которым отбирает слова сам круг. Передай их отдельно — и
    # появится второе место, решающее «какие слова учит этот человек».
    words = await pick_words(user, session, pair, exclude_ids=used)
    if len(words) < BOARD_SIZE:
        await message.answer(
            get_text("match_not_ready", lang, need=BOARD_SIZE, have=len(words))
        )
        return False

    # НАПРАВЛЕНИЕ СОБЛЮДАЕТСЯ: слева язык ВОПРОСА, справа язык ОТВЕТА.
    #
    # Первая редакция ставила изучаемый язык слева жёстко, и в обратном
    # режиме доска выглядела ровно так же, как в прямом, — то есть
    # направление не соблюдалось вовсе. Беда тихая: доска собиралась,
    # решалась и ничем не выдавала, что человек просил обратный порядок.
    left = [option_label(w, pair.prompt_lang) for w in words]
    right_labels = [option_label(w, pair.answer_lang) for w in words]
    order = deranged_order(len(words), random)

    await state.update_data(**{
        S_WORDS: [w.id for w in words],
        S_RIGHT: order,
        S_MATCHED: [],
        S_SELECTED: "",
        S_ERRORS: 0,
        S_MISSED: [],
        S_VERSION: 0,
    })

    await message.answer(
        _board_text(lang, 0, len(words), 0),
        reply_markup=board_keyboard(left, right_labels, order, [], "", 0),
    )
    return True


@router.message(Command("match"))
async def cmd_match(message: Message, state: FSMContext, session: AsyncSession):
    user = await session.get(User, message.from_user.id)
    try:
        await message.delete()
    except Exception:
        logger.debug("сообщение человека не удалилось", exc_info=True)

    if not user or not user.level:
        lang = (user.interface_language if user else None) or DEFAULT_LOCALE
        await message.answer(get_text("quiz_no_level", lang))
        return

    await start_board(message, state, session, user)


@router.callback_query(F.data == "match_start")
async def match_from_button(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
):
    """
    Доска с кнопки — с домашнего экрана или с итога прошлой доски.

    Прежний экран удаляется, а не остаётся выше: иначе после третьей доски
    в переписке висят три решённых, и найти текущую трудно.
    """
    await callback.answer()
    user = await session.get(User, callback.from_user.id)
    if not user or not user.level:
        return

    message = callback.message
    try:
        await message.delete()
    except Exception:
        logger.debug("прежний экран не удалился", exc_info=True)

    await start_board(message, state, session, user)


@router.callback_query(F.data == CB_SPENT)
async def spent_cell(callback: CallbackQuery):
    """
    Нажатие по уже сошедшейся паре.

    Telegram не умеет неактивных кнопок: нажатие придёт всё равно, и если
    его не погасить, у человека будет крутиться часик ожидания.
    """
    await callback.answer()


# ============================================================================
# НАЖАТИЕ ПО ЯЧЕЙКЕ
# ============================================================================

@router.callback_query(F.data.startswith("mt:l:"))
@router.callback_query(F.data.startswith("mt:r:"))
async def tap(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    """Одно нажатие по доске: выбрать, перенести выбор или решить пару."""
    _, side, index_raw, version_raw = callback.data.split(":")
    data = await state.get_data()

    word_ids: list[int] = data.get(S_WORDS) or []
    if not word_ids:
        await callback.answer()
        return

    version = int(data.get(S_VERSION) or 0)
    if int(version_raw) != version:
        # Устаревшее нажатие: доска успела измениться. Молча гасим — это не
        # ошибка человека, он просто нажал быстрее, чем пришёл ответ
        await callback.answer()
        return

    user = await session.get(User, callback.from_user.id)
    if not user:
        await callback.answer("❌ Error", show_alert=True)
        return

    lang = user.interface_language or DEFAULT_LOCALE
    pair = pair_from_user(user)
    words = [await session.get(Word, wid) for wid in word_ids]
    left = [option_label(w, pair.prompt_lang) for w in words]
    right_labels = [option_label(w, pair.answer_lang) for w in words]

    order: list[int] = list(data.get(S_RIGHT) or [])
    matched: list[int] = list(data.get(S_MATCHED) or [])
    missed: list[int] = list(data.get(S_MISSED) or [])
    errors = int(data.get(S_ERRORS) or 0)
    selected: str = data.get(S_SELECTED) or ""

    row = int(index_raw)
    # Какую ПАРУ задевает нажатие: слева это номер ряда, справа — то, что
    # стоит в этом ряду по перестановке
    pair_index = row if side == "l" else order[row]
    if pair_index in matched:
        await callback.answer()
        return

    here = f"{side}:{row}"
    alert: str | None = None

    if not selected:
        selected = here
    elif selected == here:
        selected = ""                      # повторное нажатие снимает выбор
    elif selected[0] == side:
        selected = here                    # та же сторона — перенос, не промах
    else:
        other_side, other_row = selected.split(":")
        other_pair = int(other_row) if other_side == "l" else order[int(other_row)]
        if other_pair == pair_index:
            # Сошлась. С первой попытки или нет — скажет `missed`, который
            # ведётся на промахах; здесь добавлять нечего
            matched.append(pair_index)
        else:
            errors += 1
            # Промах помечает ОБА задетых слова: ни одно из них больше не
            # считается узнанным с первой попытки
            for idx in (pair_index, other_pair):
                if idx not in missed:
                    missed.append(idx)
            alert = get_text("match_wrong", lang)
        selected = ""

    version += 1
    await state.update_data(**{
        S_MATCHED: matched,
        S_SELECTED: selected,
        S_ERRORS: errors,
        S_MISSED: missed,
        S_VERSION: version,
    })

    done = len(matched) == len(word_ids)
    if done:
        await _finish(callback, state, session, user, lang, words, matched, missed, errors)
        await callback.answer()
        return

    await callback.answer(alert or None)
    try:
        await callback.message.edit_text(
            _board_text(lang, len(matched), len(word_ids), errors),
            reply_markup=board_keyboard(
                left, right_labels, order, matched, selected, version
            ),
        )
    except Exception:
        # Правка не удалась — доска всё равно в состоянии, следующее
        # нажатие её перерисует
        logger.debug("правка доски не удалась", exc_info=True)


async def _finish(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession,
    user: User, lang: str, words: list[Word], matched: list[int],
    missed: list[int], errors: int,
) -> None:
    """
    Итог доски и запись прогресса.

    В прогресс идут ТОЛЬКО пары, сошедшиеся с первой попытки, и никогда
    последняя: разбор — в `match_service`. Канал — текстовый, потому что
    сопоставление проверяет узнавание написанного, тот же навык, что
    карточка. Отдельного канала у него нет нарочно: это не четвёртый
    навык, а более лёгкое упражнение на тот же.
    """
    pair = pair_from_user(user)
    first_try = {i for i in matched if i not in missed}
    counted = scored_pairs(first_try, matched)

    # КАЖДАЯ ПАРА — ПОДВОПРОС, И ЗАПИСЫВАЕТСЯ КАК ОБЫЧНЫЙ ОТВЕТ КРУГА.
    #
    # Сошлась с первой попытки — верный, после промаха — неверный. Ровно
    # так же считается карточка, и это не прихоть симметрии: промах должен
    # СТОИТЬ балла, иначе доску выгодно перебирать наугад, а перебор
    # ничему не учит.
    #
    # Внутри круга запись идёт через `record_board_answers`: там и строки
    # `quiz_questions` (от них зависят баллы, точность, разбор и репорт), и
    # ошибки круга для «повторить ошибки». Открытая сама по себе доска
    # круга не имеет, и тогда двигается только прогресс по словам.
    from app.bot.handlers.quiz.game import record_board_answers

    in_round = await record_board_answers(
        state, session, user, pair, words, matched, counted
    )
    if not in_round:
        for index in matched:
            await update_word_progress(
                user_id=user.id, word_id=words[index].id,
                is_correct=index in counted,
                session=session, learning_lang=pair.learning,
                channel=QuizChannel.TEXT,
            )
        await session.commit()

    # Числа считаются ДО вызова: test_format_parameters_match разбирает
    # get_text регулярным выражением, и вложенный вызов внутри аргумента
    # рвёт разбор — проверка перестаёт видеть остальные параметры. Третий
    # раз за день попадаюсь на одном и том же.
    counted_total = len(counted)
    pairs_total = len(words)
    text = (
        f"{get_text('match_done', lang)}\n\n"
        f"{get_text('match_done_counted', lang, counted=counted_total, total=pairs_total)}"
    )
    if errors:
        text += "\n" + get_text("match_errors", lang, count=errors)

    # ДОСКА ВНУТРИ КРУГА ВОЗВРАЩАЕТ КРУГ, а не предлагает себя снова.
    data = await state.get_data()
    round_at = data.get(S_ROUND_AT)
    if round_at:
        # Доска заняла РОВНО ОДИН вопрос, и счётчик остаётся на нём:
        # `show_next_question` сам прибавит единицу и даст следующий по
        # порядку. Прежняя редакция перепрыгивала пять, и человек видел
        # счёт 5 → 11.
        await state.update_data(**{
            "current_question": int(round_at),
            S_ROUND_AT: None,
        })
        text += "\n\n" + get_text("match_back_to_round", lang)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(
                text=get_text("quiz_btn_next", lang), callback_data="next_question"
            )
        ]])
        try:
            await callback.message.edit_text(text, reply_markup=keyboard)
        except Exception:
            await callback.message.answer(text, reply_markup=keyboard)
        return

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=get_text("match_btn_again", lang), callback_data="match_start"
        )],
        [InlineKeyboardButton(
            text=get_text("home_btn_learn", lang, count=user.quiz_word_count or 15),
            # С итога отдельно открытой доски
            callback_data="learn_now:board",
        )],
    ])
    try:
        await callback.message.edit_text(text, reply_markup=keyboard)
    except Exception:
        await callback.message.answer(text, reply_markup=keyboard)
