"""
Админка держится устава внешности: знаки, «Назад», ширина, склонение.

ЗАЧЕМ. В админке было 178 значков пятидесяти видов и 163 рамочных символа.
Убрать их один раз — работа на вечер; НЕ ДАТЬ ИМ ВЕРНУТЬСЯ — работа теста.
Иначе следующий раздел напишется по образцу памяти, а не устава, и через
месяц в панели снова будет `📊 <b>Статистика:</b>`.

Разрешены ровно четыре знака (`UI_CONCEPT.md`, §3), и в админке из них
встречаются два: `✓` и `✗` в решении по жалобе. Остальное — слова и
типографика.

Проверки здесь про ФОРМУ, а не про числа: что показывает каждый раздел —
дело `audit_admin`, который вызывает их на живых данных.
"""

import ast
import pathlib
import re

import pytest

from app.bot.handlers import admin, admin_ui

ADMIN_PATH = pathlib.Path(admin.__file__)
UI_PATH = pathlib.Path(admin_ui.__file__)

# Знаки из устава, разрешённые в админке
ALLOWED_MARKS = {"✓", "✗", "▓", "░", "·", "→", "…", "—", "–"}

EMOJI = re.compile(
    r"[\U0001F000-\U0001FAFF←-⇿☀-➿⬀-⯿️]"
)
BOX_DRAWING = re.compile(r"[├└│┌┐┘─╔╗╚╝║═]")


def _source_of(source: str, tree: ast.Module, name: str) -> str:
    """Исходник функции по имени — чтобы заглянуть в сборщик, который зовёт экран."""
    for node in tree.body:
        if (isinstance(node, (ast.AsyncFunctionDef, ast.FunctionDef))
                and node.name == name):
            return ast.get_source_segment(source, node) or ""
    return ""


def _strings_in(path: pathlib.Path) -> list[tuple[int, str]]:
    """
    Все строковые значения из кода — без описаний и комментариев.

    Разбор, а не чтение построчно: в описаниях обработчиков разрешено
    называть знаки («исключение — `✓` и `✗`»), и поиск по тексту файла
    спотыкался бы об это.
    """
    tree = ast.parse(path.read_text(encoding="utf-8"))
    docstrings = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef,
                             ast.FunctionDef, ast.AsyncFunctionDef)):
            first = node.body[0] if node.body else None
            if (isinstance(first, ast.Expr)
                    and isinstance(first.value, ast.Constant)
                    and isinstance(first.value.value, str)):
                docstrings.add(id(first.value))

    found = []
    for node in ast.walk(tree):
        if (isinstance(node, ast.Constant) and isinstance(node.value, str)
                and id(node) not in docstrings):
            found.append((node.lineno, node.value))
    return found


# ============================================================================
# ЗНАКИ
# ============================================================================

@pytest.mark.parametrize("path", [ADMIN_PATH, UI_PATH], ids=["admin", "admin_ui"])
def test_no_decorative_marks_on_admin_screens(path):
    """
    Ни одного знака вне разрешённых четырёх.

    Было 178 штук пятидесяти видов: `📊 📈 🔥 🏆 👻 🚪 🎙 🥈 🥉 📍` и так
    далее. Значок-пуля запрещён уставом: если у каждой строки свой значок —
    значков нет, есть рябь.
    """
    offenders = []
    for line, value in _strings_in(path):
        for char in EMOJI.findall(value):
            if char not in ALLOWED_MARKS:
                offenders.append(f"{path.name}:{line} {char!r} в {value[:40]!r}")

    assert not offenders, "лишние знаки на экранах админки:\n" + "\n".join(offenders)


@pytest.mark.parametrize("path", [ADMIN_PATH, UI_PATH], ids=["admin", "admin_ui"])
def test_no_box_drawing(path):
    """
    Рамочных символов нет: их было 163.

    Дерево из `├ └ │` изображало вложенность, которой в данных не было —
    на экране когорт ветвление уходило на три уровня ради двух чисел.
    Вместо него моноширинная таблица, где числа стоят столбиком.
    """
    offenders = [
        f"{path.name}:{line} {value[:50]!r}"
        for line, value in _strings_in(path)
        if BOX_DRAWING.search(value)
    ]
    assert not offenders, "рамочные символы вернулись:\n" + "\n".join(offenders)


# ============================================================================
# ВОЗВРАТ
# ============================================================================

def test_every_screen_has_a_way_back():
    """
    У каждого вложенного экрана есть «Назад», и он назван адресом.

    Правило устава: тупиков нет, и возвращает «Назад» туда, откуда пришли.
    Единственный способ это обеспечить — указать адрес явно; «на уровень
    выше вообще» в плоском списке обработчиков не существует.
    """
    source = ADMIN_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)

    # Экраны, которым «Назад» не нужен: главная (она и есть верх) и
    # действия, которые не рисуют экран
    no_back = {
        "admin:back",               # сама главная
        "admin:export_users",       # отдаёт файл и удаляет экран
        "admin:export_quizzes",
        "admin:broadcast_cancel",   # гасит экран подтверждения
        "admin:broadcast_confirm",
    }

    missing = []
    for node in tree.body:
        if not isinstance(node, (ast.AsyncFunctionDef, ast.FunctionDef)):
            continue
        data = None
        for decorator in node.decorator_list:
            if not isinstance(decorator, ast.Call) or not decorator.args:
                continue
            target = decorator.args[0]
            if (isinstance(target, ast.Compare)
                    and isinstance(target.comparators[0], ast.Constant)):
                data = target.comparators[0].value
        if not data or not data.startswith("admin:") or data in no_back:
            continue

        body = ast.get_source_segment(source, node) or ""
        # Экран может собирать клавиатуру в отдельном сборщике — так делают
        # жалобы, у которых кнопок столько, сколько слов в очереди. Тогда
        # «Назад» ищется и в сборщике: правило, а не исключение по имени
        for builder in re.findall(r"\b(_build_\w+)\(", body):
            body += _source_of(source, tree, builder)
        if "back=" not in body and 'callback_data="admin:back"' not in body:
            missing.append(data)

    assert not missing, (
        "экраны без «Назад» — из них нельзя выйти: " + ", ".join(sorted(missing))
    )


def test_back_goes_where_you_came_from():
    """
    Вложенный экран возвращает к СВОЕЙ группе, а не на главную.

    «Приход» и «Отток» открываются из «Людей» — значит и возвращать должны
    в «Людей». Прежде все разделы висели на главной и возвращали на неё;
    с появлением групп такой «Назад» уводил бы на уровень выше нужного.
    """
    source = ADMIN_PATH.read_text(encoding="utf-8")
    expected = {
        "admin:cohorts": "admin:people",
        "admin:churn": "admin:people",
        "admin:top_users": "admin:people",
        "admin:person_help": "admin:people",
        "admin:games": "admin:lessons",
        "admin:retention": "admin:lessons",
        "admin:attention": "admin:lessons",
    }

    tree = ast.parse(source)
    wrong = []
    for node in tree.body:
        if not isinstance(node, (ast.AsyncFunctionDef, ast.FunctionDef)):
            continue
        for decorator in node.decorator_list:
            if not isinstance(decorator, ast.Call) or not decorator.args:
                continue
            target = decorator.args[0]
            if not (isinstance(target, ast.Compare)
                    and isinstance(target.comparators[0], ast.Constant)):
                continue
            data = target.comparators[0].value
            if data not in expected:
                continue
            body = ast.get_source_segment(source, node) or ""
            if f'back="{expected[data]}"' not in body:
                wrong.append(f"{data} должен возвращать в {expected[data]}")

    assert not wrong, "«Назад» уводит не туда:\n" + "\n".join(wrong)


def test_every_button_on_the_main_screen_has_a_handler():
    """Кнопка в пустоту — это тупик, который видно только нажатием."""
    source = ADMIN_PATH.read_text(encoding="utf-8")
    handled = set(re.findall(r'F\.data == "(admin:[a-z_]+)"', source))

    drawn = {
        button.callback_data
        for row in admin.get_admin_keyboard().inline_keyboard
        for button in row
        if button.callback_data
    }
    assert drawn <= handled, (
        "кнопки главной ведут в пустоту: " + ", ".join(sorted(drawn - handled))
    )


# ============================================================================
# ШИРИНА И ЧИСЛА
# ============================================================================

def test_tables_fit_a_narrow_phone():
    """
    Моноширинная строка шире 32 знаков тянет горизонтальную прокрутку.

    Проверяется сам сборщик: он обязан подрезать подпись, а не позволять
    строке уехать за край. Проверено на 320 пунктах ширины.
    """
    wide = admin_ui.table([
        ("Очень длинная подпись, которая никуда не влезет", 123456),
        ("Коротко", 1),
    ])
    for line in wide.replace("<pre>", "").replace("</pre>", "").split("\n"):
        assert len(line) <= admin_ui.MAX_WIDTH, f"{len(line)} знаков: {line!r}"


def test_columns_fit_a_narrow_phone():
    wide = admin_ui.columns([
        ("Имя человека подлиннее некуда", 198, 288, 42),
        ("Кратко", 1, 2, 3),
    ])
    for line in wide.replace("<pre>", "").replace("</pre>", "").split("\n"):
        assert len(line) <= admin_ui.MAX_WIDTH, f"{len(line)} знаков: {line!r}"


def test_empty_denominator_gives_a_dash_not_a_zero():
    """
    Ноль и прочерк значат разное: ноль — «посчитали, вышло ноль», прочерк —
    «не из чего считать». Админка показывала 0% там, где данных не было
    вовсе, и это читалось как провал, которого никто не измерял.
    """
    assert admin_ui.pct(0, 0) == "—"
    assert admin_ui.pct(5, 0) == "—"
    assert admin_ui.pct(0, 10) == "0%"


def test_thousands_are_separated_without_breaking():
    """
    Разделитель — узкий НЕРАЗРЫВНЫЙ пробел (U+202F), а не обычный: обычный
    Telegram переносит, и «2 320» разрывается на две строки.
    """
    assert admin_ui.num(2320) == "2 320"
    assert admin_ui.num(12902) == "12 902"
    assert " " not in admin_ui.num(2320), "обычный пробел перенесётся"
    assert admin_ui.num(7) == "7"
    assert admin_ui.num(None) == "—"


def test_numbers_agree_with_the_noun():
    """«233 человек» читается как опечатка."""
    assert admin_ui.people(1) == "1 человек"
    assert admin_ui.people(2) == "2 человека"
    assert admin_ui.people(5) == "5 человек"
    assert admin_ui.people(11) == "11 человек"
    assert admin_ui.people(21) == "21 человек"
    assert admin_ui.people(233) == "233 человека"


def test_html_in_values_is_escaped():
    """
    Имя человека попадает на экран как есть. Имя с `<` Telegram считает
    началом тега и отклоняет ВСЁ сообщение — админка осталась бы без
    экрана, а причина была бы не видна.
    """
    built = admin_ui.listing(["<script> & Co"])
    assert "&lt;script&gt;" in built and "&amp;" in built


def test_an_empty_section_says_so_instead_of_vanishing():
    """
    Раздел без данных ПРОГОВАРИВАЕТСЯ. Молча исчезнувший раздел выглядит
    как недоделанная панель, и отличить «данных нет» от «код сломался»
    нельзя — на этом панель полгода выглядела наполовину пустой.
    """
    built = admin_ui.section("Скорость ответа", None, empty="замеров нет")
    assert "Скорость ответа" in built
    assert "замеров нет" in built
