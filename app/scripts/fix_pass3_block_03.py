"""ТРЕТИЙ ПРОХОД, блок 3 (ряды 401–600): 3 ячейки.

БЛОК НАШЁЛ БЛИЗНЕЦА ТОГО РЯДА, КОТОРЫЙ ПРАВИЛСЯ В БЛОКЕ 2, И ПОКАЗАЛ, ЧТО
МОЙ ЖЕ ЗАМЕР ЕГО ПРОПУСТИЛ.

В блоке 2 исправлен `äh` (13829, A1) «Äh, wie heißt du NOCHMAL?» — там
«nochmal» потеряли польский и турецкий. Замер тогда искал ряды, где
соответствия нет РОВНО В ОДНОМ языке из четырёх, и дал 5 попаданий.

В блоке 3 стоит `ähm` (13846, A1) — та же фраза, тот же уровень:

    de  Ähm, wie heißt du noch mal?
    en  Um, what WAS your name?        ← держит (прошедшим временем)
    ru  Эм, как тебя зовут, НАПОМНИ?   ← держит
    tr  Şey, adın NEYDİ?               ← держит (прошедшим временем)
    uk  Ем, як тебе звати?             ← ПОТЕРЯНО
    pl  Yyy, jak ty się nazywasz?      ← ПОТЕРЯНО

Потеряли ДВА языка, а не один, — и условие «ровно один» его отсекло.
Правило 1p в чистом виде: **условие, написанное для подавления шума,
надо мерить по тому, сколько сигнала оно подавляет.**

Перемер с условием «хотя бы один язык» и по всем пяти языкам: 12
попаданий вместо 5. И это окончательно закрывает вопрос о примете.

════════════════════════════════════════════════════════════════════════
ПОЧЕМУ ПРИМЕТУ НА ЭТОТ КЛАСС ПИСАТЬ НЕЛЬЗЯ: 9 ЛОЖНЫХ ИЗ 12
════════════════════════════════════════════════════════════════════════

«Ещё раз» прячется ЧЕТЫРЬМЯ разными способами, и ни один регексп на
наречия их не поймает:

  внутри глагола     `wiederkommen` (1038) ru «ВЕРНЁШЬСЯ», uk «ПОВЕРНЕШСЯ»
  в отрицании        `vergeben`    (10168) ru «БОЛЬШЕ так не делай»
                     `Abschaum`    (10347) pl «JUŻ NIGDY nie chcę widzieć»
                     `Gelübde`     (10778) uk «НІКОЛИ БІЛЬШЕ не брехати»
                     `gelobte`     (14294) ru «БОЛЬШЕ НИКОГДА не лгать»
  в количестве       `Lieblingsbuch` (9632) tr «DEFALARCA okurum» (много раз)
                     `überarbeiten`  (9282) tr «BİR KEZ DAHA» (ещё один раз)
  внутри лексемы     `gutmachen`   (10596) «wieder gutmachen» — это цельный
                     глагол «загладить», и все ПЯТЬ языков верно дали
                     «исправить / make amends / telafi etmek»

Плюс `adieu` (13995): «Wir sehen uns bald wieder» все четыре языка дали
как «скоро увидимся» — и это верно, потому что «увидимся» уже содержит
повторную встречу.

**Итог: 1 настоящее попадание, 2 пограничных, 9 ложных.** Это второй
замер того же класса, и второй раз он говорит одно: мерить нечем,
править глазом. Класс закрыт окончательно.

Пограничные, оставленные как есть:
  `Klassentreffen` (9543) — «endlich WIEDER so toll» потеряли три языка
      согласно, значит это не выброс одного, а общее решение
  `befinden` (12749) tr — «wieder gesund» без «yeniden»; турецкий один,
      но «sağlıklı olduğuna karar verdi» и так означает выздоровление

════════════════════════════════════════════════════════════════════════
ТРЕТЬЯ ПРАВКА: ЗАГОЛОВОК И ПРИМЕР ПИШУТ ОДНО СЛОВО ПО-РАЗНОМУ
════════════════════════════════════════════════════════════════════════

`nochmal` (657, A1) — заголовок написан СЛИТНО, а пример раздельно:
«Sag das NOCH MAL». Оба написания в немецком законны, но ряд учит
слитному, а показывает раздельное: на карточке человек видит сверху
«nochmal», а во фразе «noch mal».

База сама себе противоречит и в соседних рядах: `äh` (13829) «Äh, wie
heißt du NOCHMAL?» — слитно, `ähm` (13846) «Ähm, wie heißt du NOCH MAL?»
— раздельно. Но там заголовки другие (`äh`, `ähm`), и написание ни на
что не указывает. А в ряду 657 заголовок и есть это слово, поэтому
пример обязан его повторить.

Проверено: ряд 657 в остатке `scan_word_in_example` (49) НЕ лежит —
примета сопоставляет «nochmal» и «noch mal» по основе. Значит правка её
остаток не меняет.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    (13846, "example_uk",
     "Ем, як тебе звати?",
     "Ем, як тебе звати, нагадай?",
     "потеряно «noch mal»; ru «напомни», en «was», tr «neydi» держат, "
     "и близнец `äh` (13829) uk тоже говорит «нагадай»"),
    (13846, "example_pl",
     "Yyy, jak ty się nazywasz?",
     "Yyy, przypomnij mi, jak się nazywasz?",
     "то же «noch mal»; так же исправлен близнец `äh` (13829)"),
    (657, "example_de",
     "Sag das noch mal",
     "Sag das nochmal",
     "заголовок ряда написан слитно, а пример раздельно; ряд учит "
     "именно этому слову, значит пример обязан его повторить"),
]


def main() -> None:
    apply_mode = "--apply" in sys.argv
    engine = create_engine(settings.DATABASE_URL_SYNC)
    ok: list[tuple[int, str, str, str, str]] = []
    skipped: list[tuple[int, str, str | None]] = []
    seen: set[tuple[int, str]] = set()
    dupes: list[tuple[int, str]] = []
    with engine.connect() as conn:
        for wid, col, was, now, why in FIXES:
            if (wid, col) in seen:
                dupes.append((wid, col))
            seen.add((wid, col))
            cur = conn.execute(
                text(f"SELECT {col} FROM words WHERE id = :i"), {"i": wid}
            ).scalar()
            if (cur or "").strip() != was:
                skipped.append((wid, col, cur))
            else:
                ok.append((wid, col, was, now, why))

    print(f"=== правок {len(FIXES)}, совпало {len(ok)}, пропущено {len(skipped)} ===\n")
    for wid, col in dupes:
        print(f"ВНИМАНИЕ: одна ячейка правится дважды — id={wid} {col}")
    for wid, col, cur in skipped:
        print(f"ПРОПУСК id={wid} {col}: в базе {cur!r}")

    if not apply_mode:
        for wid, col, was, now, why in ok:
            print(f"id={wid} {col}")
            print(f"  было:  {was}")
            print(f"  стало: {now}")
        print("\nсухой прогон. применить: --apply")
        return

    with engine.begin() as conn:
        for wid, col, _, now, _ in ok:
            conn.execute(
                text(f"UPDATE words SET {col} = :v WHERE id = :i"),
                {"v": now, "i": wid},
            )
    print(f"\nприменено: {len(ok)}")

    bad = 0
    with engine.connect() as conn:
        for wid, col, _, now, _ in ok:
            cur = conn.execute(
                text(f"SELECT {col} FROM words WHERE id = :i"), {"i": wid}
            ).scalar()
            if (cur or "").strip() != now:
                bad += 1
                print(f"НЕ ЗАПИСАЛОСЬ id={wid} {col}: {cur!r}")
    print(f"самопроверка: не записалось {bad}")


if __name__ == "__main__":
    main()
