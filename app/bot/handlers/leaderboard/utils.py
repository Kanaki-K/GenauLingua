"""
Утилиты для системы рейтингов
Включает функции форматирования, титулов, прогресс-баров
"""


# Порог и ключ названия. Пороги прежние — менять их заодно с видом
# значило бы править два решения одной правкой.
_TITLES = (
    (2000, "rating_title_polyglot"),
    (1000, "rating_title_professor"),
    (500, "rating_title_expert"),
    (100, "rating_title_student"),
)


def get_user_title(win_streak: dict, learned_words: int,
                   lang: str = "ru") -> str:
    """
    Титул человека — по числу выученных слов, словом.

    Прежде титулов было две шкалы: по серии побед (`💎×5`, `👑×3`, `🔥×2`) и
    по словам (`🌍 🧠 🎯 📚`). Первая ушла — три разных знака на одну
    величину, и ни один не говорил, что это победы в месячном зачёте.
    Вторая осталась, но словами: угадать, что глобус дороже книжки, нельзя.

    `win_streak` остался в подписи ради вызывающих, которые его передают;
    значение не используется.
    """
    from app.locales import get_text

    for threshold, key in _TITLES:
        if learned_words >= threshold:
            return get_text(key, lang)
    return ""


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
}


def format_month_name(month: int, lang: str = "ru") -> str:
    """Название месяца на языке человека. Неизвестный язык — номером."""
    names = MONTH_NAMES.get(lang or "")
    if not names or not 1 <= month <= 12:
        return str(month)
    return names[month - 1]


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



def get_leaderboard_keyboard_text(lang: str, current_tab: str) -> dict:
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

    monthly = get_text("rating_tab_month", lang)
    alltime = get_text("rating_tab_alltime", lang)
    if current_tab == "monthly":
        monthly = f"• {monthly} •"
    else:
        alltime = f"• {alltime} •"

    return {
        'monthly': monthly,
        'alltime': alltime
    }


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


