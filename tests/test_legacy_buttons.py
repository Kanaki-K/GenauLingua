"""
Нажатие со СТАРОЙ клавиатуры должно доходить.

ЗАЧЕМ. Реплай-клавиатура живёт НА СООБЩЕНИИ и обновляется только когда бот
создаёт новый якорь. Значит у всякого, кто открыл переписку до смены
подписей, в чате остаётся прежняя клавиатура — со значками: `📚 Учить
слова`, `🦾 Настройки`. Нажатие приходит ЕЁ текстом.

А фильтр собирается из нынешних локалей (`app/bot/buttons.py`), и такого
текста он уже не знает. Кнопка молча перестаёт работать: событие приходит,
ни один обработчик не ловит, бот не отвечает. Выбраться человек может
только командой, которую надо знать, — то есть для него бот просто умер.

Это не умозрительная беда: подписи поменялись все четыре сразу, а якорь
пересоздаётся только по нажатию. Поэтому прежние подписи перечислены в
`LEGACY_TEXTS` и остаются в фильтре, нигде не показываясь.
"""

import re
import unicodedata

import pytest

from app.bot.buttons import (
    BTN_HELP, BTN_LEARN_WORDS, BTN_RATING, BTN_SETTINGS, BTN_STATS,
    LEGACY_TEXTS, button_texts, menu_texts,
)
from app.locales import LOCALES

MENU_KEYS = (BTN_LEARN_WORDS, BTN_STATS, BTN_RATING, BTN_SETTINGS)


@pytest.mark.parametrize("key", MENU_KEYS)
def test_the_old_label_is_still_caught(key):
    """
    Каждая прежняя подпись — в фильтре. Иначе у человека со старой
    клавиатурой кнопка не работает, и он этого не понимает: бот молчит.
    """
    caught = button_texts(key)
    for old in LEGACY_TEXTS[key]:
        assert old in caught, f"{old!r} больше не ловится"


@pytest.mark.parametrize("key", MENU_KEYS)
def test_the_new_label_is_caught_too(key):
    """Нынешняя подпись на каждом из шести языков — тоже в фильтре."""
    caught = button_texts(key)
    for lang in LOCALES:
        assert LOCALES[lang][key] in caught, f"{lang}/{key} не ловится"


@pytest.mark.parametrize("key", MENU_KEYS + (BTN_HELP,))
def test_the_shown_label_carries_no_mark(key):
    """
    ПОКАЗЫВАЕТСЯ всегда нынешняя подпись, и в ней знаков нет. Прежние живут
    только в фильтре: попади значок обратно в локаль — вернётся на экран.
    """
    for lang, texts in LOCALES.items():
        value = texts[key]
        marks = [c for c in value
                 if unicodedata.category(c) in ("So", "Sk", "Me", "Mn", "Cf")]
        assert not marks, f"{lang}/{key}: {value!r} несёт знаки {marks}"


def test_the_old_labels_are_the_ones_that_really_were():
    """
    Список прежних подписей описывает ПРОШЛОЕ, и проверить его можно только
    по нему самому: каждая запись обязана нести значок, иначе она не из
    прошлого, а чья-то опечатка.
    """
    for key, labels in LEGACY_TEXTS.items():
        assert labels, f"{key}: список прежних подписей пуст"
        for label in labels:
            has_mark = any(
                unicodedata.category(c) in ("So", "Sk", "Me", "Mn", "Cf")
                for c in label
            )
            assert has_mark, f"{key}: {label!r} без значка — это не прежняя подпись"


def test_menu_texts_protects_the_old_labels_too():
    """
    `menu_texts` защищает нажатия меню от обработчиков, которые ловят любой
    текст. Беда уже случалась: подсказка «ответь голосом» подписалась на
    `F.text`, и во время вопроса кнопки меню переставали работать.

    Если в этот набор не попадут старые подписи, человек со старой
    клавиатурой получит ту же беду обратно.
    """
    protected = menu_texts()
    for key in MENU_KEYS:
        for old in LEGACY_TEXTS[key]:
            assert old in protected, f"{old!r} не защищён от перехвата"


def test_no_locale_value_outside_the_allowed_set_has_marks():
    """
    Сводная проверка по ВСЕМ строкам интерфейса: знаков не осталось, кроме
    разрешённых и типографики.

    Так эта работа и мерится. Было 68 разных знаков в 251 строке из 399;
    правило снятия описано в `app/scripts/strip_marks.py` и работает от
    разрешённого списка, а не от перечня мусора — иначе составные знаки
    вроде `1️⃣` проскакивают.

    РАЗРЕШЁННЫЙ НАБОР БЕРЁТСЯ ИЗ ЧИСТИЛЬЩИКА, а не выписан здесь. Он уже
    был выписан — и разошёлся при первой же правке: владелец попросил по
    своему знаку на каждую игру («чтобы в круге обучения на конкретную
    игру было своё эмодзи»), чистильщик их принял, а тест отверг. Один
    источник, остальные на него смотрят.
    """
    from app.scripts.strip_marks import KEEP

    allowed = KEEP
    offenders = []
    for lang, texts in LOCALES.items():
        for key, value in texts.items():
            for char in value:
                if char in allowed:
                    continue
                if unicodedata.category(char) in ("So", "Sk", "Me", "Mn", "Cf"):
                    offenders.append(f"{lang}/{key}: {char!r} в {value[:40]!r}")
    assert not offenders, (
        f"знаки вернулись в локали ({len(offenders)}):\n"
        + "\n".join(offenders[:20])
    )


def test_no_box_drawing_in_locales():
    """
    Рамочных и чертёжных символов нет: в админке их было 163, в рейтинге
    стояла черта из `━` на всю ширину. Это украшение, а не структура.
    """
    box = re.compile(r"[├└│┌┐┘─━═╔╗╚╝║]")
    offenders = [
        f"{lang}/{key}"
        for lang, texts in LOCALES.items()
        for key, value in texts.items()
        if box.search(value)
    ]
    assert not offenders, "рамки в локалях: " + ", ".join(offenders[:20])
