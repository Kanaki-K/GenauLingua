"""
Утилиты для системы рейтингов
Включает функции форматирования, титулов, прогресс-баров
"""


# ЗВАНИЙ В ТАБЛИЦЕ БОЛЬШЕ НЕТ. Прежде после имени стояло «ученик»,
# «эксперт», «профессор», «полиглот» — по выученным словам, без пояснения,
# и читалось как часть имени: «DYET ученик — 812 баллов». Владелец, 14.10:
# «убрать длинные дуратские названия». Чем хвастаться вместо них — лиги в
# духе Duolingo — решается отдельно (NEXT_SESSION.md).


# Названия месяцев по языкам. ТАБЛИЦЕЙ, а не цепочкой условий.
#
# Прежде выбор был такой: `months_uk if lang == "uk" else months_en if
# lang == "en" else months_tr if lang == "tr" else months_ru`. Немецкий и
# польский в цепочку не попали, и человек, читающий бота по-немецки,
# видел «Октябрь» русскими буквами. Два языка из шести.
#
# Таблица эту ошибку делает невозможной: новый язык либо есть в ней, либо
# его отсутствие видно сразу — по запасному значению.
MONTH_NAMES = {
    "ru": ("Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
           "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"),
    "uk": ("Січень", "Лютий", "Березень", "Квітень", "Травень", "Червень",
           "Липень", "Серпень", "Вересень", "Жовтень", "Листопад", "Грудень"),
    "en": ("January", "February", "March", "April", "May", "June",
           "July", "August", "September", "October", "November", "December"),
    "de": ("Januar", "Februar", "März", "April", "Mai", "Juni",
           "Juli", "August", "September", "Oktober", "November", "Dezember"),
    "pl": ("Styczeń", "Luty", "Marzec", "Kwiecień", "Maj", "Czerwiec",
           "Lipiec", "Sierpień", "Wrzesień", "Październik", "Listopad", "Grudzień"),
    "tr": ("Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
           "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"),
    "it": ("Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno",
           "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"),
    "es": ("Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
           "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"),
    "fr": ("Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
           "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"),
    "cs": ("Leden", "Únor", "Březen", "Duben", "Květen", "Červen",
           "Červenec", "Srpen", "Září", "Říjen", "Listopad", "Prosinec"),
}


def format_month_name(month: int, lang: str = "ru", *, inline: bool = False) -> str:
    """
    Название месяца на языке человека. Неизвестный язык — номером.

    `inline` — месяц ВНУТРИ фразы: «Вы в зачёте за октябрь». По-русски и
    по-украински он тогда со строчной; с заглавной — только в заголовке
    («Таблица лидеров — Октябрь 2026»). Прежде везде стояла заглавная, и
    выходило «за Октябрь». В английском и немецком месяц всегда с
    заглавной — их не трогаем.
    """
    names = MONTH_NAMES.get(lang or "")
    if not names or not 1 <= month <= 12:
        return str(month)
    name = names[month - 1]
    # В итальянском, испанском, французском и чешском месяц внутри фразы
    # тоже со строчной
    if inline and lang in ("ru", "uk", "it", "es", "fr", "cs"):
        return name[:1].lower() + name[1:]
    return name


def create_progress_bar(current: int, target: int, length: int = 10) -> str:
    """
    Создать визуальный прогресс-бар

    Args:
        current: текущее значение
        target: целевое значение
        length: длина прогресс-бара в символах

    Returns:
        Строка с прогресс-баром и процентом
    """
    if target <= current:
        return "▓" * length + " ✓"

    percentage = min(100, int((current / target) * 100))
    filled = int((current / target) * length)
    empty = length - filled

    bar = "▓" * filled + "░" * empty
    return f"{bar} {percentage}%"



def get_leaderboard_keyboard_text(lang: str, current_tab: str,
                                  learning: "str | None" = None) -> dict:
    """
    Получить тексты кнопок для клавиатуры рейтинга

    Args:
        lang: язык интерфейса
        current_tab: текущая вкладка ('monthly' или 'alltime')

    Returns:
        Словарь с текстами кнопок
    """
    # ПОДПИСИ ИЗ ЛОКАЛИ. Здесь стоял тернарник на четыре языка, а языков
    # шесть: немец и поляк видели вкладки по-турецки — «Ay», «Tüm
    # Zamanlar». Найдено аудитом 14 октября; та же ошибка «список вместо
    # правила», что и с надписями нижних кнопок.
    from app.locales import get_text

    # ТРИ ВКЛАДКИ (владелец, 17.10): месяц и всё время — со всеми, третья —
    # месяц среди учащих тот же язык; подписана названием языка
    texts = {
        'monthly': get_text("rating_tab_month", lang),
        'alltime': get_text("rating_tab_alltime", lang),
        'lang': get_text(f"langname_{learning}", lang) if learning else "",
    }
    if current_tab in texts:
        texts[current_tab] = f"• {texts[current_tab]} •"
    return texts


# Вкладка → нажатие. Литералы, а не f-строки: приёмка `verify_buttons`
# сверяет с обработчиками именно их
RATING_TABS = {"monthly": "rating_monthly", "alltime": "rating_alltime", "lang": "rating_lang"}
TABLE_TABS = {"monthly": "table_monthly", "alltime": "table_alltime", "lang": "table_lang"}
OPEN_TABLE = {"monthly": "leaderboard_table_monthly", "alltime": "leaderboard_table_alltime",
              "lang": "leaderboard_table_lang"}


def tabs_row(lang: str, current_tab: str, learning: str, actions: dict) -> list:
    from aiogram.types import InlineKeyboardButton

    texts = get_leaderboard_keyboard_text(lang, current_tab, learning)
    return [InlineKeyboardButton(text=texts[tab], callback_data=actions[tab])
            for tab in ("monthly", "alltime", "lang")]


def lang_suffix(lang: str, learning: str) -> str:
    """Приписка к заголовку вкладки языка: « · Немецкий»."""
    from app.locales import get_text

    return f" · {get_text(f'langname_{learning}', lang)}"


async def edit_screen(callback, text: str, reply_markup) -> None:
    """
    Перерисовать экран рейтинга, не падая на повторном нажатии.

    Нажатие на уже открытую вкладку присылает тот же текст, и Telegram
    отвечает «message is not modified» — в журнал это шло ошибкой
    обработчика, хотя ничего не сломано: экран уже такой, какой просили.
    """
    from aiogram.exceptions import TelegramBadRequest

    try:
        await callback.message.edit_text(text, reply_markup=reply_markup)
    except TelegramBadRequest as error:
        if "not modified" not in str(error):
            raise


