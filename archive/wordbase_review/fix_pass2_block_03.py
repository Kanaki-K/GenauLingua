"""ВТОРОЙ ПРОХОД, блок 3 (ряды 401–600): правки, найденные глазами.

Главное в блоке — ТРИ ДЕФЕКТА В НЕМЕЦКОМ ЭТАЛОНЕ. За весь первый
проход таких нашлось немного, и каждый важнее десяти правок перевода:
эталон читает ученик, по нему выверяются пять остальных языков, и
ошибка в нём тиражируется.

    sitzen (841)   «Ich sitz auf dem Stuhl»   → sitze
    folgen (1433)  «Folg mir bitte»            → Folge
    ähm (13846)    «wie hießt du noch mal?»    → heißt

`hießt` — это вообще не форма немецкого языка: ни «hieß» (прошедшее),
ни «heißt» (настоящее). Опечатка в эталоне A1-ряда, прожившая первый
проход.

И ЧЕТВЁРТАЯ ДЫРА В `scan_de_colloquial`. Усечение «Ich sitz» примета
не видела, потому что основы `sitz` в её списке не было — хотя `setz`
была. То есть список собирали по найденным примерам, и соседний по
смыслу глагол в него не попал. Основа добавлена, прогон по базе дал
ровно этот один ряд.

«Folg mir bitte» в примету НЕ добавлялось, и это отдельное решение.
Усечённое повелительное — предмет `scan_de_imperative`, а та примета
перечисляет основы, у которых «-e» ОБЯЗАТЕЛЬНО (öffne, arbeite,
beruhige). У «folge» оно по Дудену необязательно, и внести основу туда
значило бы ловить законное. Ряд исправлен руками по правилу базы
«в эталоне усечений нет».

Остальное обычное: выбор дальнего варианта (`Gefühl` ru «плохое
чувство» вместо «предчувствие», и польский с турецким взяли верное),
подменённая фраза в польском (`sobald`), потерянное «bitte» в четырёх
рядах, время глагола.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ── ДЕФЕКТЫ НЕМЕЦКОГО ЭТАЛОНА ────────────────────────────────
    (841, "example_de",
     "Ich sitz auf dem Stuhl",
     "Ich sitze auf dem Stuhl",
     "разговорное усечение в эталоне; основы sitz не было в примете"),
    (1433, "example_de",
     "Folg mir bitte",
     "Folge mir bitte",
     "усечённое повелительное: по правилу базы в эталоне усечений нет"),
    (13846, "example_de",
     "Ähm, wie hießt du noch mal?",
     "Ähm, wie heißt du noch mal?",
     "«hießt» не форма немецкого: ни hieß, ни heißt"),

    # ── дальний вариант вместо нужного ───────────────────────────
    (2505, "example_ru",
     "У меня плохое чувство",
     "У меня плохое предчувствие",
     "«плохое чувство» по-русски не говорят; польский и турецкий взяли предчувствие"),
    (2505, "example_uk",
     "У мене погане почуття",
     "У мене погане передчуття",
     "то же"),
    (1338, "example_uk",
     "Магазин навпроти",
     "Магазин он там",
     "«навпроти» это напротив, а «drüben» — вон там; первый перевод «он там»"),
    (1630, "example_tr",
     "Bu benim arkadaşım",
     "Bu benim ahbabım",
     "«arkadaş» это просто друг; Kumpel разговорное, и в переводе есть «ahbap»"),
    (1685, "example_uk",
     "Там було багато людей",
     "Там була велика кількість людей",
     "потеряно «große Menge»: в остальных языках она есть"),
    (13372, "example_uk",
     "Кожна жінка може це вивчити",
     "Кожна жінка може цьому навчитися",
     "«вивчити» это выучить наизусть; lernen здесь — научиться"),

    # ── подменённая фраза ────────────────────────────────────────
    (13383, "example_pl",
     "Zadzwonię, gdy tylko wrócę do domu",
     "Gdy tylko tam będę, zadzwonię",
     "эталон «Sobald ich da bim»: про возвращение домой там нет"),

    # ── потерянное «bitte» ───────────────────────────────────────
    (6287, "example_pl",
     "Przyniesiesz mleko z piwnicy?",
     "Przyniesiesz proszę mleko z piwnicy?",
     "потеряно «bitte»: в остальных пяти языках оно есть"),
    (1172, "example_pl",
     "Możesz z tym przestać?",
     "Czy możesz z tym przestać, proszę?",
     "то же"),
    (548, "example_uk",
     "Можеш прочитати це вголос?",
     "Можеш прочитати це вголос, будь ласка?",
     "то же"),
    (6289, "example_tr",
     "Buradan kaybolmak istiyorum",
     "Sadece buradan kaybolmak istiyorum",
     "потеряно «einfach»: в остальных четырёх языках оно есть"),

    # ── время глагола ────────────────────────────────────────────
    (790, "example_pl",
     "Wyślę ci to zdjęcie",
     "Wysyłam ci to zdjęcie",
     "будущее против «Ich schicke»; в остальных языках настоящее"),

    # ── добавленное усиление ─────────────────────────────────────
    (1867, "example_en",
     "Safety on the road is very important",
     "Safety on the road is important",
     "«very» в эталоне нет: «ist wichtig»"),
    (1867, "example_uk",
     "Безпека на дорозі дуже важлива",
     "Безпека в дорожньому русі важлива",
     "«дуже» в эталоне нет; и «im Straßenverkehr» это дорожное движение"),
]


def main() -> None:
    apply_mode = "--apply" in sys.argv
    engine = create_engine(settings.DATABASE_URL_SYNC)
    ok: list[tuple[int, str, str, str, str]] = []
    skipped: list[tuple[int, str, str | None]] = []
    with engine.connect() as conn:
        for wid, col, was, now, why in FIXES:
            cur = conn.execute(
                text(f"SELECT {col} FROM words WHERE id = :i"), {"i": wid}
            ).scalar()
            if (cur or "").strip() != was:
                skipped.append((wid, col, cur))
            else:
                ok.append((wid, col, was, now, why))

    print(f"=== правок {len(FIXES)}, совпало {len(ok)}, пропущено {len(skipped)} ===\n")
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
