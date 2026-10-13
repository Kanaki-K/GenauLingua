"""
Класс: латинская буква-двойник внутри кириллического слова.

«смiливість» — третья буква латинская «i». «личнo» — последняя латинская
«o». «rеlіgіозный» — вообще мешанина: латинские r, l, i и кириллические
е, о, з, н, ы, й в одном слове. Глазом это не видно никак: буквы
выглядят одинаково. Проверка на диакритику их не берёт, словарь тоже —
для него это просто незнакомые слова.

Почему это дорого. Поиск по слову их не находит: «сміливість» и
«смiливість» для базы разные строки. Синтез читает латинскую букву как
латинскую, то есть слово звучит неправильно. А главное — ученик видит на
карточке слово, которого нет.

КЛАСС БЫЛ ИЗВЕСТЕН И НИКОГДА НЕ ПРОВЕРЯЛСЯ. В REVIEW_CRITERIA, раздел 3,
записано: «чужой алфавит внутри слова: „коноtа“, „діш kürü“». Нашли
глазами в первом круге, исправили те строки — и не прогнали поиском.

Поиск шёл в два приёма. Сначала соседство букв двух алфавитов — дало
три находки. Потом строже: любое слово с латиницей внутри русской или
украинской ячейки, кроме законных сокращений. Второй приём дал 21
попадание, из них законных 17: «PIN-код», «ID-картка», «HR-директор»,
«VIP-гостя», «BIC-код», «Speedy» (прозвище), «The Beatles», «Felis»
(латинское название рода). Настоящих четыре.

Четвёртое — не двойник, а целое английское слово, оставшееся в русских
значениях: `Gefährtin` → «спутница, подруга, companion».

ПОЧЕМУ «было» ЗДЕСЬ ПРОВЕРЯЕТСЯ ШАБЛОНОМ, А НЕ СТРОКОЙ. Как и в
`fix_uk_apostrophe_char`: «смiливість» и «сміливість» в исходнике
выглядят одинаково, и ошибку в литерале не увидел бы никто. Поэтому id
перечислены поимённо, ячейка обязана содержать латинскую букву, а новое
значение записано целиком и потом сверяется чтением обратно.

    python -m app.scripts.fix_homoglyph            # показать
    python -m app.scripts.fix_homoglyph --apply    # применить
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

LATIN = re.compile(r"[A-Za-z]")

# (id, колонка, на что менять, зачем). «было» проверяется наличием латиницы.
FIXES: list[tuple[int, str, str, str]] = [
    (10127, "translation_uk", "сміливість, мужність, відвага",
     "«сміливість» было написано с латинской «i»"),
    (11016, "translation_ru", "верующий, религиозный",
     "«религиозный» было написано вперемешку латиницей и кириллицей"),
    (14103, "example_ru", "Запись в дневнике написана очень лично",
     "«лично» заканчивалось латинской «o»"),
    (15198, "translation_ru", "спутница, подруга, компаньонка",
     "«companion» — английское слово в русских значениях"),
]


def main() -> None:
    apply_mode = "--apply" in sys.argv
    engine = create_engine(settings.DATABASE_URL_SYNC)

    plan, skipped = [], []
    with engine.connect() as conn:
        for wid, col, now, why in FIXES:
            cur = conn.execute(
                text(f"SELECT {col} FROM words WHERE id = :i"), {"i": wid}
            ).scalar()
            if not cur or not LATIN.search(cur):
                skipped.append((wid, col, cur))
                continue
            plan.append((wid, col, cur, now, why))

    print(f"=== ячеек {len(FIXES)}, с латиницей {len(plan)}, "
          f"пропущено {len(skipped)} ===\n")
    for wid, col, was, now, why in plan:
        print(f"  {wid} {col} — {why}")
        print(f"      было:  {was!r}")
        print(f"      стало: {now!r}")
    for wid, col, cur in skipped:
        print(f"  ПРОПУЩЕНО {wid} {col}: {cur!r}")

    if not apply_mode:
        print("\nэто показ. Для применения — флаг --apply")
        return

    with engine.begin() as conn:
        for wid, col, _, now, _ in plan:
            conn.execute(text(f"UPDATE words SET {col} = :v WHERE id = :i"),
                         {"v": now, "i": wid})
    print(f"\nприменено: {len(plan)}")

    with engine.connect() as conn:
        bad = 0
        for wid, col, _, now, _ in plan:
            cur = conn.execute(text(f"SELECT {col} FROM words WHERE id = :i"),
                               {"i": wid}).scalar()
            if cur != now:
                print(f"  ТРЕВОГА: {wid} {col} не записалось")
                bad += 1
        print(f"самопроверка: не записалось {bad}")


if __name__ == "__main__":
    main()
