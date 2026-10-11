"""
Клавиатуры для бота с поддержкой локализации
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from app.locales import DEFAULT_LOCALE, get_text


def get_answer_keyboard(options: list[tuple[int, str]]) -> InlineKeyboardMarkup:
    """Клавиатура с вариантами ответов (4 кнопки)"""
    buttons = [
        [InlineKeyboardButton(text=text, callback_data=f"answer_{word_id}")]
        for word_id, text in options
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_main_menu_keyboard(lang: str = DEFAULT_LOCALE) -> ReplyKeyboardMarkup:
    """
    Главное меню: ЧЕТЫРЕ кнопки, сетка два на два.

    Рейтинг вынесен отдельной кнопкой. Прежде путь к нему был
    «Статистика → Мой рейтинг → Таблица лидеров» — третий уровень вложенности
    за экраном с чужим названием. Соревнование — главный повод вернуться
    завтра, и прятать его за словом «Статистика» значит лишать себя этого
    повода.

    ПОМОЩЬ ИЗ ГЛАВНОГО МЕНЮ УБРАНА. Владелец о ней дословно: «там вообще
    бесполезная информация... можно сократить, ни на что не влияет».
    Экрану, который сам назван неактуальным, не место среди четырёх
    главных кнопок; остаются команда /help и строка внизу настроек.

    Пять кнопок дали бы ряд «два, два, один» — висящую одиночку, которая
    выглядит как недоделка. Четыре ложатся ровным квадратом.
    """
    buttons = [
        [
            KeyboardButton(text=get_text("btn_learn_words", lang)),
            KeyboardButton(text=get_text("btn_rating", lang))
        ],
        [
            KeyboardButton(text=get_text("btn_stats", lang)),
            KeyboardButton(text=get_text("btn_settings", lang))
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        is_persistent=True,
        input_field_placeholder=get_text("menu_placeholder", lang)
    )