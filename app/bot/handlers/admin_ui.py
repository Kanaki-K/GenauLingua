# -*- coding: utf-8 -*-
"""
Внешность админ-панели: заголовок, пояснение, таблица, кнопки.

ЗАЧЕМ ОТДЕЛЬНЫЙ МОДУЛЬ. В админке было 178 значков пятидесяти видов и 163
рамочных символа (`├ └ │ ─`), и каждый экран собирался своими руками:
где-то `📊 <b>Статистика:</b>`, где-то `🔥 <b>Retention:</b>`, где-то
дерево на три уровня ветвления. Пока правил один экран, остальные ехали в
свою сторону.

Устав внешности — `UI_CONCEPT.md`, пять правил. Для админки из них главные
три: знак либо несёт смысл, которого нет у слова, либо его нет; один экран
— одна работа; у каждого вложенного экрана есть «Назад», и возвращает он
туда, откуда пришли.

ПОЧЕМУ ЧИСЛА В `<pre>`. Админка — это приборная панель: её не читают, в
неё смотрят, и числа должны стоять столбиком. В пропорциональном шрифте
Telegram добивка пробелами НЕ выравнивает — выходит хуже, чем без
выравнивания вовсе. `<pre>` даёт моноширинный блок, и столбец встаёт
ровно. Платим жирным шрифтом внутри блока (Telegram его там не
поддерживает) — для таблицы чисел это невелика потеря.

Ширина блоков ограничена нарочно: на узком телефоне длинная строка в
`<pre>` уезжает за край и тянет горизонтальную прокрутку.
"""
from __future__ import annotations

from html import escape
from typing import Iterable, Optional, Sequence

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Шире этого моноширинная строка не влезает в узкий телефон без прокрутки.
# Проверено на 320 пунктах — там помещается около 34 знаков.
MAX_WIDTH = 32

# Разделитель внутри строки. Из устава: это типографика, а не значок
DOT = "·"


def num(value: Optional[int | float]) -> str:
    """
    Число с разделителем тысяч: 2 320 читается, 2320 — нет.

    Разделитель — узкий неразрывный пробел: обычный пробел Telegram может
    перенести, и число разорвётся на две строки.
    """
    if value is None:
        return "—"
    if isinstance(value, float):
        return f"{value:.1f}".replace(".", ",")
    return f"{value:,}".replace(",", " ")


def pct(part: Optional[int], whole: Optional[int], *, digits: int = 0) -> str:
    """
    Доля в процентах. Пустой знаменатель даёт прочерк, а НЕ ноль.

    Разница важна: ноль означает «посчитали, вышло ноль», прочерк — «не из
    чего считать». Прежде админка показывала 0% там, где данных не было
    вовсе, и это читалось как провал, которого никто не измерял.
    """
    if not whole:
        return "—"
    value = (part or 0) / whole * 100
    return f"{value:.{digits}f}".replace(".", ",") + "%"


def bar(part: Optional[int], whole: Optional[int], cells: int = 10) -> str:
    """Шкала из `▓░`. Из устава: типографика, а не значок."""
    if not whole:
        return "░" * cells
    filled = round((part or 0) / whole * cells)
    return "▓" * max(0, min(cells, filled)) + "░" * max(0, cells - filled)


def table(rows: Sequence[tuple[str, object]], *, width: int = MAX_WIDTH) -> str:
    """
    Таблица «что — сколько» в моноширинном блоке, значения столбиком.

    Подпись слева, значение справа по правому краю: так выравниваются
    разряды, и столбец чисел читается сверху вниз одним взглядом. Слишком
    длинная подпись подрезается, иначе строка уедет за край телефона.
    """
    prepared: list[tuple[str, str]] = []
    for label, value in rows:
        prepared.append((str(label), value if isinstance(value, str) else num(value)))

    if not prepared:
        return ""

    value_width = max(len(value) for _, value in prepared)
    label_width = max(1, width - value_width - 1)

    lines = []
    for label, value in prepared:
        shown = label if len(label) <= label_width else label[: label_width - 1] + "…"
        lines.append(f"{shown:<{label_width}} {value:>{value_width}}")

    return "<pre>" + escape("\n".join(lines)) + "</pre>"


def plural(count: int, one: str, few: str, many: str) -> str:
    """
    Русское склонение числительного: 1 человек, 2 человека, 5 человек.

    Нужно потому, что «233 человек» на экране читается как опечатка, а
    обойти склонение, выбросив существительное, выходит не везде.

    Правило выбора формы — общее с экранами пользователя
    (`app.locales._plural_index`): два списка правил одного языка однажды
    разошлись бы, как разошлись подписи кнопок с фильтрами.
    """
    from app.locales import _plural_index

    return (one, few, many)[_plural_index(count, "ru")]


def people(count: int) -> str:
    """«233 человека», «1 человек», «105 человек»."""
    return f"{num(count)} {plural(count, 'человек', 'человека', 'человек')}"


def columns(rows: Sequence[Sequence[object]], *,
            width: int = MAX_WIDTH) -> str:
    """
    Таблица в несколько столбцов: подпись слева, числа справа столбиками.

    Нужна там, где у строки ДВА числа — например «ответов 19, точность
    32%». Склеенные в одно значение, они читались как одно число: «19 32%»
    невозможно разобрать с первого взгляда.
    """
    if not rows:
        return ""

    prepared = [[cell if isinstance(cell, str) else num(cell) for cell in row]
                for row in rows]
    count = max(len(row) for row in prepared)
    prepared = [list(row) + [""] * (count - len(row)) for row in prepared]

    # Числовые столбцы по правому краю, подпись — по левому
    widths = [max(len(row[index]) for row in prepared) for index in range(count)]
    label_width = max(1, width - sum(widths[1:]) - (count - 1))

    lines = []
    for row in prepared:
        label = row[0]
        if len(label) > label_width:
            label = label[: label_width - 1] + "…"
        cells = [f"{label:<{label_width}}"]
        cells += [f"{row[index]:>{widths[index]}}" for index in range(1, count)]
        lines.append(" ".join(cells))

    return "<pre>" + escape("\n".join(lines)) + "</pre>"


def listing(lines: Iterable[str]) -> str:
    """
    Перечень строк в моноширинном блоке — когда строка не делится на
    «подпись и число» (имена людей, слова, последние занятия).
    """
    rows = [line for line in lines]
    if not rows:
        return ""
    clipped = [row if len(row) <= MAX_WIDTH else row[: MAX_WIDTH - 1] + "…"
               for row in rows]
    return "<pre>" + escape("\n".join(clipped)) + "</pre>"


def screen(title: str, lead: Optional[str] = None,
           blocks: Sequence[Optional[str]] = ()) -> str:
    """
    Экран: заголовок, одна строка пояснения, содержимое.

    Пояснение — курсивом и только там, где без него непонятно; пустые
    блоки отбрасываются, чтобы на экране не оставалось дыр от разделов,
    по которым нет данных.
    """
    parts = [f"<b>{escape(title)}</b>"]
    if lead:
        parts.append(f"<i>{lead}</i>")
    parts.extend(block for block in blocks if block)
    return "\n\n".join(parts)


def section(title: str, body: Optional[str],
            note: Optional[str] = None,
            empty: str = "нет данных") -> str:
    """
    Раздел внутри экрана: название, содержимое, при надобности сноска.

    Пустота ПРОГОВАРИВАЕТСЯ, а не прячется: раздел, который молча исчез,
    выглядит как недоделанная панель, и отличить «данных нет» от «код
    сломался» нельзя.
    """
    head = f"{escape(title)}"
    if not body:
        return f"{head}\n<i>{escape(empty)}</i>"
    out = f"{head}\n{body}"
    if note:
        out += f"\n<i>{note}</i>"
    return out


# ============================================================================
# КНОПКИ
# ============================================================================

def kb(*rows: Sequence[tuple[str, str]], back: Optional[str] = None,
       back_text: str = "Назад") -> InlineKeyboardMarkup:
    """
    Клавиатура из рядов `(подпись, callback_data)` и «Назад» последним.

    `back` — куда возвращает, а не «на уровень выше вообще»: экран обязан
    вернуть туда, откуда пришли, и единственный способ это обеспечить —
    назвать адрес явно.
    """
    keyboard = [
        [InlineKeyboardButton(text=text, callback_data=data) for text, data in row]
        for row in rows if row
    ]
    if back:
        keyboard.append([InlineKeyboardButton(text=back_text, callback_data=back)])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
