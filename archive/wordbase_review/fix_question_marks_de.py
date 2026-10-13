"""
Немецкие примеры-вопросы без вопросительного знака — 41 ряд.

Нашлось сплошным поиском `scan_question_mark` после того, как вычитка
наткнулась на это в трёх блоках подряд. Немецкий ряд — эталон для пяти
языков: «Kannst du Butter kaufen» без знака читается как утверждение, и
переводы за ним идут утверждениями. Поэтому правится эталон.

ПОЧЕМУ ЗДЕСЬ СПИСОК id, А НЕ ПАР «БЫЛО → СТАЛО». У остальных правок
записано точное прежнее значение: перевод я пишу сам, и ошибиться строкой
легко. Здесь правка механическая — приписать знак, — и переписывать руками
41 немецкую фразу значило бы добавить ровно тот риск опечатки, от которого
«было» и защищает. Вместо этого каждый id проверяется тем же шаблоном, что
его нашёл: если в базе уже не вопрос-без-знака, ряд пропускается. Смысл
гарантии тот же — вслепую не пишем.

Все 41 просмотрены глазами по одному. Восемь ложных срабатываний первого
прогона в список не попали и учтены в самом шаблоне: оборот «Was die
Bezahlung anbelangt», восклицание «Was für ein Zufall» и шесть фраз, где
знак уже стоит внутри: «Wo ist der Feuerlöscher? Ich kann ihn nicht finden».

Две фразы знаком не исправить — в них вопрос склеен с утверждением запятой,
и правка другая:

    Kannst du mir das Steak durchschneiden, es ist zu dick
    Kannst du die Jalousien runterlassen, es ist zu hell

    python -m app.scripts.fix_question_marks_de            # показать
    python -m app.scripts.fix_question_marks_de --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402
from app.scripts.scan_question_mark import looks_like_question  # noqa: E402

# Ряды, где достаточно приписать знак. Просмотрены по одному.
APPEND_MARK = [
    8, 302, 462, 706, 717, 1035, 1113, 1318, 1615, 1709, 2103, 2585,
    6268, 6621, 6689, 6692, 6735, 6762, 7042, 7258, 8079, 8334,
    9756, 10035, 10278, 10285, 10482, 11318, 11680, 12255,
    13438, 13899, 13920, 13933, 13944, 13982, 14198, 16035, 18283,
]

# Ряды, где вопрос склеен с утверждением запятой: (id, было, стало)
SPLIT_SENTENCE = [
    (7596,
     "Kannst du mir das Steak durchschneiden, es ist zu dick",
     "Kannst du mir das Steak durchschneiden? Es ist zu dick"),
    (7971,
     "Kannst du die Jalousien runterlassen, es ist zu hell",
     "Kannst du die Jalousien runterlassen? Es ist zu hell"),
]


def main() -> None:
    apply_mode = "--apply" in sys.argv
    engine = create_engine(settings.DATABASE_URL_SYNC)

    planned: list[tuple[int, str, str, str]] = []
    skipped: list[tuple[int, str]] = []

    with engine.connect() as conn:
        for wid in APPEND_MARK:
            cur = (conn.execute(
                text("SELECT example_de FROM words WHERE id = :i"), {"i": wid}
            ).scalar() or "").strip()
            if not cur or not looks_like_question(cur):
                skipped.append((wid, cur))
                continue
            planned.append((wid, cur, cur + "?", "вопрос без знака"))

        for wid, was, now in SPLIT_SENTENCE:
            cur = (conn.execute(
                text("SELECT example_de FROM words WHERE id = :i"), {"i": wid}
            ).scalar() or "").strip()
            if cur != was:
                skipped.append((wid, cur))
                continue
            planned.append((wid, was, now, "вопрос склеен с утверждением запятой"))

    total = len(APPEND_MARK) + len(SPLIT_SENTENCE)
    print(f"=== рядов {total}, к правке {len(planned)}, пропущено {len(skipped)} ===\n")
    for wid, was, now, why in planned:
        print(f"  {wid} example_de — {why}")
        print(f"      было:  {was!r}")
        print(f"      стало: {now!r}")
    for wid, cur in skipped:
        print(f"  ПРОПУЩЕНО {wid}: {cur!r}")

    if not apply_mode:
        print("\nэто показ. Для применения — флаг --apply")
        return

    with engine.begin() as conn:
        for wid, _, now, _ in planned:
            conn.execute(text("UPDATE words SET example_de = :v WHERE id = :i"),
                         {"v": now, "i": wid})
    print(f"\nприменено: {len(planned)}")

    with engine.connect() as conn:
        bad = 0
        for wid, _, now, _ in planned:
            cur = (conn.execute(
                text("SELECT example_de FROM words WHERE id = :i"), {"i": wid}
            ).scalar() or "").strip()
            if cur != now:
                print(f"  ТРЕВОГА: {wid} не записалось")
                bad += 1
        print(f"самопроверка: не записалось {bad}")


if __name__ == "__main__":
    main()
