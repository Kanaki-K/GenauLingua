"""
Примета: знак в конце примера расходится между языками ряда.

Зачем. Блок 5 второго прохода дал пять таких рядов подряд:
`Glückwunsch` (en и ru с «!», остальные без), `guck` (de, ru, pl с «!»,
uk, tr, en без), `Maul` (только pl с «!»), `beeilen` (de, ru, pl с «!»,
остальные без), `au` (en и ru с «!», остальные без). Пять рядов в
одном блоке — это класс, а класс надо смотреть по всей базе.

Почему это дефект, а не придирка. Знак в конце — часть того, ЧТО
слышит ученик: клип читается синтезатором, и восклицание он произносит
иначе, чем ровную фразу. Ряд, где немецкий эталон спокоен, а русский
кричит, учит разной интонации одной и той же фразы.

Правило простое: тип фразы задаёт ЭТАЛОН. Если немецкий пример
кончается на «!», то и перевод должен; если нет — не должен.

Чего примета НЕ решает сама. Вопросительный знак бывает законно
расходится: немецкое утверждение с частицей (`Das ist gut, ne?`)
переводится вопросом, а немецкий вопрос — утверждением
(`Möchtest du einen Drink?` → «Хочешь напиток?» всё-таки вопрос, но
бывает и иначе). Поэтому «?» выводится ОТДЕЛЬНЫМ списком и гейтом не
является — там нужны глаза.

Самопроверка обязательна: заведомо согласованные ряды молчат,
заведомо расходящиеся ловятся.

    python -m app.scripts.scan_terminal_punct
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

LANGS = ("en", "ru", "uk", "tr", "pl")


def mark(sentence: str | None) -> str:
    """Тип фразы по знаку: «!», «?» или пусто.

    Знак ищется ВО ВСЕЙ фразе, а не только в конце. Иначе ряд `Prost`
    («Prost! Auf deine Gesundheit» — восклицание стоит после первого
    слова) считался бы спокойным, и примета потребовала бы убрать «!»
    из русского, где он на месте.
    """
    s = sentence or ""
    if "!" in s:
        return "!"
    if "?" in s:
        return "?"
    return ""


def selfcheck() -> None:
    cases = [
        # (эталон, переводы, ждём ли расхождения по «!»)
        ("Komm bitte herein!", ["Please come in!", "Заходи, пожалуйста!"], False),
        ("Das ist gut", ["That is good", "Это хорошо"], False),
        ("Guck mal hier!", ["Look here", "Смотри-ка сюда!"], True),
        ("Das tut weh", ["Ouch, that hurts!", "Ой, больно"], True),
        ("Halt dein Maul", ["Shut your mouth", "Stul pysk!"], True),
        ("Worum geht es denn?", ["What's it about?", "О чём речь?"], False),
    ]
    errs = []
    for de, others, expect in cases:
        # ровно та же проверка, что в main: ПОЯЗЫКОВО, а не «хоть один»
        got = any((mark(o) == "!") != (mark(de) == "!") for o in others)
        if got != expect:
            errs.append(f"{de!r}: ждали расхождение={expect}, получили {got}")
    if errs:
        print("САМОПРОВЕРКА НЕ ПРОШЛА:")
        for e in errs:
            print("   ", e)
        sys.exit(1)
    print(f"самопроверка: {len(cases)} случаев разобраны верно")


def main() -> None:
    selfcheck()
    engine = create_engine(settings.DATABASE_URL_SYNC)
    cols = ", ".join(f"example_{lg}" for lg in LANGS)
    with engine.connect() as conn:
        rows = conn.execute(
            text(
                f"SELECT id, word_de, example_de, {cols} FROM words "
                "WHERE example_de IS NOT NULL ORDER BY id"
            )
        ).mappings().all()

    bang: list[tuple[int, str, str, list[str]]] = []
    quest: list[tuple[int, str, str, list[str]]] = []
    for r in rows:
        de_mark = mark(r["example_de"])
        off_bang, off_quest = [], []
        for lg in LANGS:
            m = mark(r[f"example_{lg}"])
            if (m == "!") != (de_mark == "!"):
                off_bang.append(f"{lg}{'+' if m == '!' else '-'}")
            if (m == "?") != (de_mark == "?"):
                off_quest.append(f"{lg}{'+' if m == '?' else '-'}")
        if off_bang:
            bang.append((r["id"], r["word_de"], r["example_de"], off_bang))
        if off_quest:
            quest.append((r["id"], r["word_de"], r["example_de"], off_quest))

    print(f"\nпрочитано рядов: {len(rows)}")
    print(f"расхождение по «!»: {len(bang)}")
    print(f"расхождение по «?»: {len(quest)}  (отдельный список, нужны глаза)")

    print("\n── «!» ────────────────────────────────────────────────────")
    for wid, word, ex, off in bang:
        print(f"  {wid:>6}  {word:<22} {' '.join(off):<22} {ex}")

    print("\n── «?» ────────────────────────────────────────────────────")
    for wid, word, ex, off in quest:
        print(f"  {wid:>6}  {word:<22} {' '.join(off):<22} {ex}")


if __name__ == "__main__":
    main()
