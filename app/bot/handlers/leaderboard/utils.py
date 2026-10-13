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


def format_month_name(month: int, lang: str = "ru") -> str:
    """
    Форматировать название месяца

    Args:
        month: номер месяца (1-12)
        lang: язык интерфейса

    Returns:
        Название месяца на выбранном языке
    """
    months_ru = {
        1: "Январь", 2: "Февраль", 3: "Март", 4: "Апрель",
        5: "Май", 6: "Июнь", 7: "Июль", 8: "Август",
        9: "Сентябрь", 10: "Октябрь", 11: "Ноябрь", 12: "Декабрь"
    }
    months_uk = {
        1: "Січень", 2: "Лютий", 3: "Березень", 4: "Квітень",
        5: "Травень", 6: "Червень", 7: "Липень", 8: "Серпень",
        9: "Вересень", 10: "Жовтень", 11: "Листопад", 12: "Грудень"
    }
    months_en = {
        1: "January", 2: "February", 3: "March", 4: "April",
        5: "May", 6: "June", 7: "July", 8: "August",
        9: "September", 10: "October", 11: "November", 12: "December"
    }
    months_tr = {
        1: "Ocak", 2: "Şubat", 3: "Mart", 4: "Nisan",
        5: "Mayıs", 6: "Haziran", 7: "Temmuz", 8: "Ağustos",
        9: "Eylül", 10: "Ekim", 11: "Kasım", 12: "Aralık"
    }

    months = months_uk if lang == "uk" else months_en if lang == "en" else months_tr if lang == "tr" else months_ru
    return months.get(month, str(month))


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
    if current_tab == "monthly":
        monthly_text = "• Месяц •" if lang == "ru" else "• Місяць •" if lang == "uk" else "• Month •" if lang == "en" else "• Ay •"
        alltime_text = "За всё время" if lang == "ru" else "За весь час" if lang == "uk" else "All-Time" if lang == "en" else "Tüm Zamanlar"
    else:
        monthly_text = "Месяц" if lang == "ru" else "Місяць" if lang == "uk" else "Month" if lang == "en" else "Ay"
        alltime_text = "• За всё время •" if lang == "ru" else "• За весь час •" if lang == "uk" else "• All-Time •" if lang == "en" else "• Tüm Zamanlar •"

    return {
        'monthly': monthly_text,
        'alltime': alltime_text
    }


