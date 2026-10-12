"""
Сопоставление текста reply-кнопок с действием.

Реплай-кнопки приходят от Telegram обычным текстом, поэтому хендлеры должны
знать все локализованные варианты надписи. Раньше эти списки были вписаны
в каждый хендлер руками (F.text.in_(["📚 Учить слова", "📚 Вчити слова", ...])) —
добавление языка интерфейса требовало правок в нескольких файлах, а расхождение
с локалью молча ломало кнопку.

Теперь варианты берутся из самих локалей: источник истины один.
"""

from aiogram import F

from app.locales import LOCALES, get_text

BTN_LEARN_WORDS = "btn_learn_words"
BTN_STATS = "btn_stats"
BTN_RATING = "btn_rating"
BTN_SETTINGS = "btn_settings"
BTN_HELP = "btn_help"


def button_texts(key: str) -> set[str]:
    """Все локализованные надписи кнопки."""
    return {get_text(key, lang) for lang in LOCALES}


def pressed(key: str):
    """Фильтр aiogram: нажата кнопка с этим ключом на любом языке интерфейса."""
    return F.text.in_(button_texts(key))


def menu_texts() -> set[str]:
    """
    Все надписи кнопок главного меню на всех языках интерфейса.

    Нужно, чтобы обработчики, ловящие ПРОИЗВОЛЬНЫЙ текст, не съедали нажатия
    меню. Беда настоящая и уже случилась: подсказка «ответь голосом»
    подписалась на `F.text` в состоянии ответа, а роутер игры подключён
    раньше настроек и статистики — и во время вопроса эти кнопки переставали
    работать. Молча: обработчик срабатывал, ничего не делал и событие гасил.
    """
    return {
        text
        for key in (BTN_LEARN_WORDS, BTN_STATS, BTN_RATING, BTN_SETTINGS, BTN_HELP)
        for text in button_texts(key)
    }
