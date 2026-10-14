"""
Всё, что бот импортирует НА УРОВНЕ МОДУЛЯ, должно быть в requirements.txt.

ЗАЧЕМ ЭТА ПРОВЕРКА СУЩЕСТВУЕТ. Она написана по следам дефекта, который
нельзя было найти чтением и который едва не уронил бота насмерть.

`edge_tts` импортировался строкой 41 в `app/services/audio_service.py` — на
уровне модуля. Этот модуль тянет обработчик игры, обработчик тянут роутеры,
роутеры тянет `app.main`. А в `requirements.txt` библиотеки НЕ БЫЛО: она
стояла в `requirements-dev.txt` с комментарием «боту не нужно».

Следствие: боевой образ не терял синтез — БОТ В НЁМ НЕ ПОДНИМАЛСЯ ВОВСЕ.

    File "/app/app/services/audio_service.py", line 41, in <module>
      import edge_tts
    ModuleNotFoundError: No module named 'edge_tts'

Прод при этом работал: его образ был собран раньше, когда строка ещё стояла
в общем списке. То есть мина лежала и ждала ПЕРВОЙ ЖЕ ПЕРЕСБОРКИ, а
выглядело бы это как «обновились и всё сломалось».

Нашлось не рассуждением, а запуском собранного образа. Эта проверка делает
то же дешевле: сверяет импорты с перечнем зависимостей, не собирая образ.

ЧТО ПРОВЕРЯЕТСЯ И ЧТО НЕТ. Только `app/`, и только импорты верхнего уровня.
`app/scripts` и `app/testing` исключены нарочно: первым можно требовать
dev-зависимости (они не в рантайме бота), второй — обвес проверок.
Импорты ВНУТРИ функций тоже не считаются: это сознательный приём проекта
для необязательных частей — например, декодер mp3 тянет `av` и `numpy`
внутри функции, и их отсутствие не лишает бота озвучки, только обрезки
тишины.
"""

import ast
import pathlib
import sys
from importlib.metadata import packages_distributions

ROOT = pathlib.Path(__file__).resolve().parents[1]

# Эти каталоги внутри app/ не входят в рантайм бота
EXCLUDED = ("app/scripts/", "app/testing/")


def _requirements() -> set[str]:
    """Названия распространяемых пакетов из requirements.txt, в нижнем регистре."""
    text = (ROOT / "requirements.txt").read_text(encoding="utf-8")
    names = set()
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("-"):
            continue
        for sep in ("==", ">=", "<=", "~=", ">", "<", "["):
            if sep in line:
                line = line.split(sep)[0]
        names.add(line.strip().lower().replace("_", "-"))
    return names


def _module_level_imports(path: pathlib.Path) -> set[str]:
    """
    Верхние имена модулей, импортируемые НА УРОВНЕ МОДУЛЯ.

    Считаются и импорты внутри верхнеуровневых `if`/`try`: они тоже
    выполняются при загрузке модуля, а значит тоже валят её.
    """
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    found: set[str] = set()

    def collect(body) -> None:
        for node in body:
            if isinstance(node, ast.Import):
                for alias in node.names:
                    found.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.level == 0 and node.module:
                    found.add(node.module.split(".")[0])
            elif isinstance(node, (ast.If, ast.Try)):
                collect(node.body)
                collect(getattr(node, "orelse", []))
                collect(getattr(node, "finalbody", []))
                for handler in getattr(node, "handlers", []):
                    collect(handler.body)

    collect(tree.body)
    return found


def _runtime_files() -> list[pathlib.Path]:
    out = []
    for path in sorted((ROOT / "app").rglob("*.py")):
        rel = path.relative_to(ROOT).as_posix()
        if any(rel.startswith(skip) for skip in EXCLUDED):
            continue
        out.append(path)
    return out


def test_every_runtime_import_is_declared():
    stdlib = set(sys.stdlib_module_names)
    mapping = packages_distributions()
    declared = _requirements()

    missing: dict[str, list[str]] = {}

    for path in _runtime_files():
        rel = path.relative_to(ROOT).as_posix()
        for module in _module_level_imports(path):
            if module in stdlib or module == "app" or module.startswith("_"):
                continue

            dists = mapping.get(module)
            if not dists:
                # Модуль не установлен даже в разработке — такое поймает
                # обычный импорт, и к перечню зависимостей отношения не имеет
                continue

            names = {d.lower().replace("_", "-") for d in dists}
            if names & declared:
                continue
            missing.setdefault(f"{module} ({'/'.join(sorted(dists))})",
                               []).append(rel)

    assert not missing, (
        "в requirements.txt нет библиотек, которые бот импортирует при "
        "загрузке — боевой образ не поднимется:\n"
        + "\n".join(f"   {name}: {', '.join(files)}"
                    for name, files in sorted(missing.items()))
    )


def test_the_check_itself_would_catch_a_missing_line():
    """
    Проверка проверки: убери строку из перечня — она обязана заметить.

    Без этого легко получить сторожа, который всегда доволен. Проект на
    таком уже горел: метрика «Из напоминаний» искала значение, которого не
    писал никто, и показывала ноль как факт.
    """
    declared = _requirements()
    assert "aiogram" in declared, "перечень читается неверно"

    without = declared - {"edge-tts"}
    mapping = packages_distributions()
    dists = {d.lower().replace("_", "-") for d in mapping.get("edge_tts", [])}

    assert dists, "edge_tts не установлен — проверку не на чем испытать"
    assert not (dists & without), (
        "выброшенная строка всё равно считается объявленной — "
        "сверка названий сломана"
    )
