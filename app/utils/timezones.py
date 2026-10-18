"""
Утилиты для работы с часовыми поясами
"""

from typing import Dict, Tuple

# Маппинг городов → (names_by_lang, timezone, UTC offset)
# Структура: city_code -> ({"ru"…"cs": "name"}, timezone, offset) — все языки
# интерфейса: без de и pl немецкий и польский экран поясов шёл кириллицей (14.10)
TIMEZONE_CITIES: Dict[str, Tuple[Dict[str, str], str, str]] = {
    # ============================================
    # ПЕРВЫЙ ЭКРАН (4 основных города)
    # ============================================
    "london": (
        {"ru": "🇬🇧 Лондон", "uk": "🇬🇧 Лондон", "en": "🇬🇧 London", "tr": "🇬🇧 Londra", "de": "🇬🇧 London", "pl": "🇬🇧 Londyn", "it": "🇬🇧 Londra", "es": "🇬🇧 Londres", "fr": "🇬🇧 Londres", "cs": "🇬🇧 Londýn"},
        "Europe/London", "+00:00"
    ),
    "berlin": (
        {"ru": "🇩🇪 Берлин", "uk": "🇩🇪 Берлін", "en": "🇩🇪 Berlin", "tr": "🇩🇪 Berlin", "de": "🇩🇪 Berlin", "pl": "🇩🇪 Berlin", "it": "🇩🇪 Berlino", "es": "🇩🇪 Berlín", "fr": "🇩🇪 Berlin", "cs": "🇩🇪 Berlín"},
        "Europe/Berlin", "+01:00"
    ),
    "kyiv": (
        {"ru": "🇺🇦 Киев", "uk": "🇺🇦 Київ", "en": "🇺🇦 Kyiv", "tr": "🇺🇦 Kiev", "de": "🇺🇦 Kyjiw", "pl": "🇺🇦 Kijów", "it": "🇺🇦 Kyiv", "es": "🇺🇦 Kiev", "fr": "🇺🇦 Kyiv", "cs": "🇺🇦 Kyjev"},
        "Europe/Kyiv", "+02:00"
    ),
    "istanbul": (
        {"ru": "🇹🇷 Стамбул", "uk": "🇹🇷 Стамбул", "en": "🇹🇷 Istanbul", "tr": "🇹🇷 İstanbul", "de": "🇹🇷 Istanbul", "pl": "🇹🇷 Stambuł", "it": "🇹🇷 Istanbul", "es": "🇹🇷 Estambul", "fr": "🇹🇷 Istanbul", "cs": "🇹🇷 Istanbul"},
        "Europe/Istanbul", "+03:00"
    ),

    # ============================================
    # ВТОРОЙ ЭКРАН (16 дополнительных городов)
    # ============================================

    # Америка
    "los_angeles": (
        {"ru": "🇺🇸 Лос-Анджелес", "uk": "🇺🇸 Лос-Анджелес", "en": "🇺🇸 Los Angeles", "tr": "🇺🇸 Los Angeles", "de": "🇺🇸 Los Angeles", "pl": "🇺🇸 Los Angeles", "it": "🇺🇸 Los Angeles", "es": "🇺🇸 Los Ángeles", "fr": "🇺🇸 Los Angeles", "cs": "🇺🇸 Los Angeles"},
        "America/Los_Angeles", "-08:00"
    ),
    "chicago": (
        {"ru": "🇺🇸 Чикаго", "uk": "🇺🇸 Чикаго", "en": "🇺🇸 Chicago", "tr": "🇺🇸 Chicago", "de": "🇺🇸 Chicago", "pl": "🇺🇸 Chicago", "it": "🇺🇸 Chicago", "es": "🇺🇸 Chicago", "fr": "🇺🇸 Chicago", "cs": "🇺🇸 Chicago"},
        "America/Chicago", "-06:00"
    ),
    "new_york": (
        {"ru": "🇺🇸 Нью-Йорк", "uk": "🇺🇸 Нью-Йорк", "en": "🇺🇸 New York", "tr": "🇺🇸 New York", "de": "🇺🇸 New York", "pl": "🇺🇸 Nowy Jork", "it": "🇺🇸 New York", "es": "🇺🇸 Nueva York", "fr": "🇺🇸 New York", "cs": "🇺🇸 New York"},
        "America/New_York", "-05:00"
    ),
    "toronto": (
        {"ru": "🇨🇦 Торонто", "uk": "🇨🇦 Торонто", "en": "🇨🇦 Toronto", "tr": "🇨🇦 Toronto", "de": "🇨🇦 Toronto", "pl": "🇨🇦 Toronto", "it": "🇨🇦 Toronto", "es": "🇨🇦 Toronto", "fr": "🇨🇦 Toronto", "cs": "🇨🇦 Toronto"},
        "America/Toronto", "-05:00"
    ),
    "mexico_city": (
        {"ru": "🇲🇽 Мехико", "uk": "🇲🇽 Мехіко", "en": "🇲🇽 Mexico City", "tr": "🇲🇽 Mexico City", "de": "🇲🇽 Mexiko-Stadt", "pl": "🇲🇽 Meksyk", "it": "🇲🇽 Città del Messico", "es": "🇲🇽 Ciudad de México", "fr": "🇲🇽 Mexico", "cs": "🇲🇽 Ciudad de México"},
        "America/Mexico_City", "-06:00"
    ),
    "sao_paulo": (
        {"ru": "🇧🇷 Сан-Паулу", "uk": "🇧🇷 Сан-Паулу", "en": "🇧🇷 São Paulo", "tr": "🇧🇷 São Paulo", "de": "🇧🇷 São Paulo", "pl": "🇧🇷 São Paulo", "it": "🇧🇷 San Paolo", "es": "🇧🇷 São Paulo", "fr": "🇧🇷 São Paulo", "cs": "🇧🇷 São Paulo"},
        "America/Sao_Paulo", "-03:00"
    ),

    # Азия
    "dubai": (
        {"ru": "🇦🇪 Дубай", "uk": "🇦🇪 Дубай", "en": "🇦🇪 Dubai", "tr": "🇦🇪 Dubai", "de": "🇦🇪 Dubai", "pl": "🇦🇪 Dubaj", "it": "🇦🇪 Dubai", "es": "🇦🇪 Dubái", "fr": "🇦🇪 Dubaï", "cs": "🇦🇪 Dubaj"},
        "Asia/Dubai", "+04:00"
    ),
    "almaty": (
        {"ru": "🇰🇿 Алматы", "uk": "🇰🇿 Алмати", "en": "🇰🇿 Almaty", "tr": "🇰🇿 Almatı", "de": "🇰🇿 Almaty", "pl": "🇰🇿 Ałmaty", "it": "🇰🇿 Almaty", "es": "🇰🇿 Almaty", "fr": "🇰🇿 Almaty", "cs": "🇰🇿 Almaty"},
        "Asia/Almaty", "+05:00"
    ),
    "tashkent": (
        {"ru": "🇺🇿 Ташкент", "uk": "🇺🇿 Ташкент", "en": "🇺🇿 Tashkent", "tr": "🇺🇿 Taşkent", "de": "🇺🇿 Taschkent", "pl": "🇺🇿 Taszkent", "it": "🇺🇿 Tashkent", "es": "🇺🇿 Taskent", "fr": "🇺🇿 Tachkent", "cs": "🇺🇿 Taškent"},
        "Asia/Tashkent", "+05:00"
    ),
    "delhi": (
        {"ru": "🇮🇳 Дели", "uk": "🇮🇳 Делі", "en": "🇮🇳 Delhi", "tr": "🇮🇳 Delhi", "de": "🇮🇳 Delhi", "pl": "🇮🇳 Delhi", "it": "🇮🇳 Delhi", "es": "🇮🇳 Delhi", "fr": "🇮🇳 Delhi", "cs": "🇮🇳 Dillí"},
        "Asia/Kolkata", "+05:30"
    ),
    "bangkok": (
        {"ru": "🇹🇭 Бангкок", "uk": "🇹🇭 Бангкок", "en": "🇹🇭 Bangkok", "tr": "🇹🇭 Bangkok", "de": "🇹🇭 Bangkok", "pl": "🇹🇭 Bangkok", "it": "🇹🇭 Bangkok", "es": "🇹🇭 Bangkok", "fr": "🇹🇭 Bangkok", "cs": "🇹🇭 Bangkok"},
        "Asia/Bangkok", "+07:00"
    ),
    "hanoi": (
        {"ru": "🇻🇳 Ханой", "uk": "🇻🇳 Ханой", "en": "🇻🇳 Hanoi", "tr": "🇻🇳 Hanoi", "de": "🇻🇳 Hanoi", "pl": "🇻🇳 Hanoi", "it": "🇻🇳 Hanoi", "es": "🇻🇳 Hanói", "fr": "🇻🇳 Hanoï", "cs": "🇻🇳 Hanoj"},
        "Asia/Ho_Chi_Minh", "+07:00"
    ),
    "beijing": (
        {"ru": "🇨🇳 Пекин", "uk": "🇨🇳 Пекін", "en": "🇨🇳 Beijing", "tr": "🇨🇳 Pekin", "de": "🇨🇳 Peking", "pl": "🇨🇳 Pekin", "it": "🇨🇳 Pechino", "es": "🇨🇳 Pekín", "fr": "🇨🇳 Pékin", "cs": "🇨🇳 Peking"},
        "Asia/Shanghai", "+08:00"
    ),
    "tokyo": (
        {"ru": "🇯🇵 Токио", "uk": "🇯🇵 Токіо", "en": "🇯🇵 Tokyo", "tr": "🇯🇵 Tokyo", "de": "🇯🇵 Tokio", "pl": "🇯🇵 Tokio", "it": "🇯🇵 Tokyo", "es": "🇯🇵 Tokio", "fr": "🇯🇵 Tokyo", "cs": "🇯🇵 Tokio"},
        "Asia/Tokyo", "+09:00"
    ),
    "seoul": (
        {"ru": "🇰🇷 Сеул", "uk": "🇰🇷 Сеул", "en": "🇰🇷 Seoul", "tr": "🇰🇷 Seul", "de": "🇰🇷 Seoul", "pl": "🇰🇷 Seul", "it": "🇰🇷 Seul", "es": "🇰🇷 Seúl", "fr": "🇰🇷 Séoul", "cs": "🇰🇷 Soul"},
        "Asia/Seoul", "+09:00"
    ),
    "sydney": (
        {"ru": "🇦🇺 Сидней", "uk": "🇦🇺 Сідней", "en": "🇦🇺 Sydney", "tr": "🇦🇺 Sidney", "de": "🇦🇺 Sydney", "pl": "🇦🇺 Sydney", "it": "🇦🇺 Sydney", "es": "🇦🇺 Sídney", "fr": "🇦🇺 Sydney", "cs": "🇦🇺 Sydney"},
        "Australia/Sydney", "+11:00"
    ),
}


def get_city_name(city_code: str, lang: str = "ru") -> str:
    """
    Получить название города

    Args:
        city_code: код города (например, "london")
        lang: язык интерфейса (ru, uk, en, tr)

    Returns:
        Название города с флагом на выбранном языке
    """
    if city_code not in TIMEZONE_CITIES:
        unknown_city = {
            "ru": "🌍 Неизвестный город",
            "uk": "🌍 Невідоме місто",
            "en": "🌍 Unknown city",
            "tr": "🌍 Bilinmeyen şehir",
            "it": "🌍 Città sconosciuta",
            "es": "🌍 Ciudad desconocida",
            "fr": "🌍 Ville inconnue",
            "cs": "🌍 Neznámé město",
        }
        return unknown_city.get(lang, unknown_city["ru"])

    city_names = TIMEZONE_CITIES[city_code][0]
    return city_names.get(lang, city_names["ru"])


def get_timezone(city_code: str) -> str:
    """
    Получить timezone по коду города

    Args:
        city_code: код города (например, "london")

    Returns:
        Timezone string (например, "Europe/London")
    """
    if city_code not in TIMEZONE_CITIES:
        return "Europe/Berlin"  # default

    return TIMEZONE_CITIES[city_code][1]


def get_utc_offset(city_code: str) -> str:
    """
    Получить UTC offset по коду города

    Args:
        city_code: код города (например, "london")

    Returns:
        UTC offset string (например, "+00:00")
    """
    if city_code not in TIMEZONE_CITIES:
        return "+01:00"  # default для Берлина

    return TIMEZONE_CITIES[city_code][2]


def get_all_cities() -> Dict[str, Tuple[str, str, str]]:
    """Получить все доступные города"""
    return TIMEZONE_CITIES


def get_main_cities() -> list[str]:
    """Получить коды 4 основных городов"""
    return ["london", "berlin", "kyiv", "istanbul"]


def get_extended_cities() -> list[str]:
    """Получить коды 16 дополнительных городов"""
    main = get_main_cities()
    return [code for code in TIMEZONE_CITIES.keys() if code not in main]