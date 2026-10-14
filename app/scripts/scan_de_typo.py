"""
ПРИМЕТА НЕ РАБОТАЕТ. Оставлена как записанный отрицательный результат:
она показывает, где приём «словарь из самой базы» перестаёт годиться.
Гейтом быть не может, в проверки не ставить.

Что она должна была искать: ОПЕЧАТКУ в немецком слове эталона.

Зачем. Блок 57 дал `Ich esse gerne eine Waffel mit Schoklade` —
пропущена буква в `Schokolade`. Это не стиль и не вариант написания,
а опечатка, и ученик списывает её вместе с фразой.

Почему не вышло. Две предыдущие приметы со словарём из базы
(scan_de_lowercase_noun, scan_de_separable) задавали базе вопрос
«ВЫВОДИТСЯ ли эта форма от известного заголовка?» — и база отвечала
точно. Здесь вопрос другой: «СУЩЕСТВУЕТ ли это слово в немецком?»
На него 12483 заголовка ответить не могут: примеры используют слов
гораздо больше, чем есть в базе.

А немецкий вдобавок плотен: от любого слова на расстоянии одной
правки почти всегда стоит другое настоящее слово. После трёх раундов
сужения примета дала 108 попаданий, и все 108 — настоящие слова:
`Schloss` (одна правка до `schließen`), `Materialien` (до `Material`),
`Risiken` (до `Risiko`), `Vergiss` (до `vergessen`), `Fiction`
(до `Fiktion`). Ни одной опечатки сверх той, что нашлась глазами.

Вывод: класс опечаток в эталоне проверяется только настоящим словарём
немецкого, которого у проекта нет. Глазами — ловится, приметой — нет.

Как ищется. Опять словарём служит база: 12902 заголовка и все формы,
которые от них выводятся. Если слово из примера базе НЕ известно, а на
расстоянии одной правки от него стоит известное — это подозрение на
опечатку. `Schoklade` базе неизвестно, `Schokolade` известно, между
ними одна вставка.

Расстояние считается без перебора словаря. Для каждого известного слова
в указатель кладётся и само слово, и все его варианты с одной
выброшенной буквой. Тогда замена, вставка и выпадение буквы — это
пересечение указателей слова и кандидата, и проверка занимает
постоянное время, а не 12902 сравнения.

Границы приметы, и они жёсткие:
  · смотрим только слова С ЗАГЛАВНОЙ и не короче семи букв. В коротких
    словах немецкий полон пар, отличающихся одной буквой (`Stadt` и
    `statt`, `Meer` и `mehr`), и примета захлебнулась бы;
  · база знает 12902 слова, а примеры используют гораздо больше. Слово,
    неизвестное базе, чаще всего просто отсутствует в ней, а не
    написано с ошибкой. Поэтому примета НЕ ЧИНИТ, а сужает базу до
    списка, который читается глазами;
  · немецкие составные слова (`Blutkörperchen`, `Wassermoleküle`)
    в базе есть лишь частью, и расстояние до них ничего не значит.

Самопроверка идёт на выдуманном словаре: проверяется логика, а не
содержимое базы.

    python -m app.scripts.scan_de_typo
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

WORD = re.compile(r"[A-Za-zÄÖÜäöüß]+")
MIN_LEN = 7

# Окончания, которыми база сама образует формы от своих заголовков.
SUFFIXES = ("", "e", "en", "er", "es", "em", "n", "s", "ern", "se",
            # женский род занятий: Grafiker → Grafikerin
            "in", "innen",
            # личные и повелительные формы глагола
            "t", "st", "te", "ten", "test", "end", "et", "est")

# Умлаутное множественное: Blatt → Blätter, Strumpf → Strümpfe,
# Fahrgast → Fahrgäste, Bundesland → Bundesländer. Это правило, а не
# список: достаточно переставить гласную в основе.
UMLAUT = (("au", "äu"), ("a", "ä"), ("o", "ö"), ("u", "ü"))

# Имена собственные: вывести их из базы нельзя, а расстояние до
# заголовков у них случайное. Список ведётся руками.
NAMES = {
    "münchen", "spanien", "berlin", "deutschland", "österreich",
    "italien", "frankreich", "polen", "russland", "europa", "afrika",
    "amerika", "asien", "brasilien", "japan", "china", "indien",
    "schweiz", "türkei", "ukraine", "england", "london", "paris",
    "hamburg", "köln", "dresden", "leipzig", "bayern", "rom", "wien",
}


def del1(w: str) -> set[str]:
    """Все варианты слова с одной выброшенной буквой."""
    return {w[:i] + w[i + 1:] for i in range(len(w))}


def umlauts(w: str) -> set[str]:
    """Варианты основы с переставленной на умлаут гласной."""
    out = {w}
    for a, b in UMLAUT:
        i = w.rfind(a)
        if i >= 0:
            out.add(w[:i] + b + w[i + len(a):])
    return out


ALPHABET = "abcdefghijklmnopqrstuvwxyzäöüß"


def build_known(words: set[str]) -> set[str]:
    """Все формы, которые база выводит от своих заголовков."""
    known = set()
    for w in words:
        stems = umlauts(w)
        if w.endswith("en"):
            stems |= umlauts(w[:-2])    # основа глагола
        for stem in stems:
            for s in SUFFIXES:
                known.add(stem + s)
    return known


def neighbours(w: str) -> set[str]:
    """Все слова на расстоянии одной правки от w.

    Перебираем правки САМОГО СЛОВА, а не словаря: их около 600 на
    слово, а словарь после вывода форм — больше двух миллионов.
    Первая версия приметы строила указатель выбрасываний по всему
    словарю и не укладывалась в две минуты."""
    out = set(del1(w))
    for i in range(len(w) + 1):
        for c in ALPHABET:
            out.add(w[:i] + c + w[i:])          # вставка
            if i < len(w):
                out.add(w[:i] + c + w[i + 1:])  # замена
    # перестановка соседних букв: `Banhhof` вместо `Bahnhof`. По
    # Левенштейну это две правки, но на клавиатуре — одна, и это самая
    # частая опечатка вообще. Самопроверка на `Banhhof` и поймала, что
    # без этого правила примета класс не видит.
    for i in range(len(w) - 1):
        out.add(w[:i] + w[i + 1] + w[i] + w[i + 2:])
    out.discard(w)
    return out


def suspects(example: str, known: set[str]) -> list[str]:
    out = []
    for m in WORD.finditer(example):
        t = m.group()
        if len(t) < MIN_LEN or not t[0].isupper():
            continue
        low = t.lower()
        if low in known or low in NAMES:
            continue
        if neighbours(low) & known:
            out.append(t)
    return out


FAKE = {"schokolade", "erdbeere", "bahnhof", "wohnung", "fahrgast",
        "grafiker", "beachten"}
GOOD = [
    "Ich esse gerne eine Waffel mit Schokolade",
    # слово короче семи букв примета не смотрит
    "Das ist ein Haus",
    # слово, которого в базе просто нет, и до известных далеко
    "Der Mikroprozessor arbeitet schnell",
    # законная форма от заголовка
    "Ich mag Erdbeeren sehr",
    # умлаутное множественное
    "Die Fahrgäste steigen aus dem Zug aus",
    # женский род занятия
    "Sie arbeitet als Grafikerin im Verlag",
    # повелительное от глагола
    "Beachte bitte die Hinweise genau",
    # имя собственное
    "Sie ist in München aufgewachsen",
]
BAD = [
    "Ich esse gerne eine Waffel mit Schoklade",
    "Wir treffen uns am Banhhof",
    "Meine Wohnnung ist klein",
]


def selfcheck() -> None:
    known = build_known(FAKE)
    for s in GOOD:
        if suspects(s, known):
            print(f"САМОПРОВЕРКА УПАЛА: ложное срабатывание на {s!r}")
            sys.exit(1)
    for s in BAD:
        if not suspects(s, known):
            print(f"САМОПРОВЕРКА УПАЛА: пропущено {s!r}")
            sys.exit(1)
    print(f"самопроверка: {len(GOOD)} правильных и {len(BAD)} "
          f"испорченных строк разобраны верно\n")


def main() -> None:
    selfcheck()
    engine = create_engine(settings.DATABASE_URL_SYNC)
    with engine.connect() as conn:
        heads = {r[0].lower() for r in conn.execute(text(
            "SELECT word_de FROM words WHERE word_de IS NOT NULL")).all()}
        rows = conn.execute(text(
            "SELECT id, word_de, example_de FROM words "
            "WHERE example_de IS NOT NULL ORDER BY id")).all()

    known = build_known(heads)
    print(f"заголовков в базе: {len(heads)}")
    print(f"выведенных форм: {len(known)}")
    print(f"прочитано немецких примеров: {len(rows)}")

    found = [(i, w, e, s) for i, w, e in rows
             if (s := suspects(e, known))]
    print(f"слов на расстоянии одной правки от известного: {len(found)}\n")
    for i, w, e, s in found:
        print(f"  {i:>6}  {w:<22} [{', '.join(s)}]  {e}")


if __name__ == "__main__":
    main()
