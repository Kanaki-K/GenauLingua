"""ПРИМЕР РАВЕН САМОМУ СЛОВУ — 13 ячеек в 6 рядах.

Пример существует, чтобы показать слово В ДЕЛЕ. Там, где он равен самому
слову, он не показывает ничего, а полный клип произносит слово ДВАЖДЫ:
«Goodbye. Goodbye». Требование владельца к озвучке дословно: «чтобы при
нажатии мы слышали и тратили время на прослушивание ровно того, что надо».

════════════════════════════════════════════════════════════════════════
ЗАМЕР ПО ВЫБРАННОМУ ЗНАЧЕНИЮ, А НЕ ПО ЯЧЕЙКЕ
════════════════════════════════════════════════════════════════════════

Первый прогон приметы дал НОЛЬ попаданий, и это была ошибка проверки, а не
чистая база. Сравнивалась ЯЧЕЙКА перевода:

    ячейка   «goodbye, reunion, meeting again»
    пример   «Goodbye»                          → не равно, пропущено

А код работает с ОДНИМ ВЫБРАННЫМ значением — тем, которое и показано на
карточке, и произнесено в клипе:

    main_meaning   «goodbye»
    пример         «Goodbye»                    → РАВНО

Это восьмой случай одной и той же формы (`ROADMAP.md` §6): проверка
смотрит на одно поле, а код работает с соседним. Правильный замер —
`main_meaning(word, lang)` без артикля, сравнение через `fold` (турецкая
«i» рвёт `.lower()`), концевая точка отброшена.

    судимо 12 902 ряда × 6 языков
    ПРИМЕР РАВЕН ВЫБРАННОМУ ЗНАЧЕНИЮ: 13
    по языкам: en 1, pl 2, ru 3, tr 4, uk 3

Немецкого в списке нет ни одного: там пример всегда прирастает хотя бы
предлогом («Wiedersehen» → «Auf Wiedersehen»).

════════════════════════════════════════════════════════════════════════
ЧТО СТАВИТСЯ ВЗАМЕН
════════════════════════════════════════════════════════════════════════

Правило одно: новый пример ОБЯЗАН содержать то же выбранное значение —
иначе клип снова разойдётся с карточкой, а это уже разобранный дефект
(«Swot» в клипе против «overachiever» в примере). И он держится рядом с
примерами остальных языков того же ряда: база трижды вычитана на
параллельность, и ломать её ради одной ячейки нельзя.

Все шесть рядов — ходовые формулы вежливости и два причастия, поэтому
замена короткая: то же выражение плюс минимальное окружение, в котором оно
действительно звучит.

ВНИМАНИЕ ВЛАДЕЛЬЦУ: восемь из тринадцати ячеек — турецкие, польские и
украинские. Русские и английскую я отвечаю, за остальные прошу взгляда
носителя: смысл и параллельность выдержаны, но за живость языка в чужом
языке ручаться нельзя.

════════════════════════════════════════════════════════════════════════
ПОСЛЕ ПРАВКИ ОБЯЗАТЕЛЕН ДОСИНТЕЗ
════════════════════════════════════════════════════════════════════════

Имя клипа — хеш произносимого текста, поэтому правка примера ОСИРОТИТ
тринадцать полных клипов. Порядок:

    python -m app.scripts.fix_example_equals_word
    python -m app.scripts.fix_example_equals_word --apply
    python -m app.scripts.tts_synthesize
    python -m app.scripts.state_report
"""
from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

WHY = "пример был равен выбранному значению: клип произносил слово дважды"

FIXES: list[tuple[int, str, str, str, str]] = [
    # ряд 982 «verstanden» · de «Ich habe verstanden», ru «Я понял»
    (982, "example_tr", "Anladım", "Tamam, anladım", WHY),

    # ряд 1039 «Wiedersehen» · de «Auf Wiedersehen». Прощание плюс то, что
    # за ним обычно и следует, — так оно и звучит в речи
    (1039, "example_en", "Goodbye", "Goodbye, see you tomorrow", WHY),
    (1039, "example_ru", "До свидания", "До свидания, до завтра", WHY),
    (1039, "example_uk", "До побачення", "До побачення, до завтра", WHY),
    (1039, "example_tr", "Görüşmek üzere", "Görüşmek üzere, iyi günler", WHY),
    (1039, "example_pl", "Do widzenia", "Do widzenia, do zobaczenia jutro", WHY),

    # ряд 1041 «willkommen» · de «Willkommen hier», en «Welcome here».
    # «Добро пожаловать сюда» по-русски не говорят — держим смысл, не слово
    (1041, "example_ru", "Добро пожаловать", "Добро пожаловать к нам", WHY),
    (1041, "example_uk", "Ласкаво просимо", "Ласкаво просимо до нас", WHY),

    # ряд 2726 «portofrei» · en «Delivery is postage-free»
    (2726, "example_tr", "Kargo ücretsiz", "Bu siparişte kargo ücretsiz", WHY),

    # ряд 12526 «angeschossen» · de «Er ist angeschossen», en «He has been shot»
    (12526, "example_tr", "Vurulmuş", "O vurulmuş", WHY),

    # ряд 13968 «Wiederhören» · прощание по телефону, de «Auf Wiederhören»
    (13968, "example_ru", "До связи", "До связи, позвоню вечером", WHY),
    (13968, "example_uk", "До зв'язку", "До зв'язку, подзвоню ввечері", WHY),
    (13968, "example_pl", "Do usłyszenia", "Do usłyszenia, zadzwonię wieczorem", WHY),
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
            current = (cur or "").strip()
            if current == now:
                # Уже применено: скрипт можно гонять сколько угодно
                continue
            if current != was:
                skipped.append((wid, col, cur))
            else:
                ok.append((wid, col, was, now, why))

    print(f"=== правок {len(FIXES)}, совпало {len(ok)}, "
          f"пропущено {len(skipped)}, уже применено "
          f"{len(FIXES) - len(ok) - len(skipped)} ===\n")
    for wid, col in dupes:
        print(f"ВНИМАНИЕ: одна ячейка правится дважды — id={wid} {col}")
    for wid, col, cur in skipped:
        print(f"ПРОПУСК id={wid} {col}: в базе {cur!r}")

    # Новый пример обязан содержать прежний текст: он и был выбранным
    # значением, и клип с карточкой разойдутся, если его потерять
    for wid, col, was, now, _ in ok:
        if was.lower() not in now.lower():
            print(f"ОТКАЗ id={wid} {col}: новый пример не содержит {was!r}")
            return

    if not apply_mode:
        for wid, col, was, now, _ in ok:
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
