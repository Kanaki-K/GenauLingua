"""
Седьмой проход по разговорному усечению в немецком эталоне.

Блок 52 показал форму, которой примета не знала: `Morgen **is** der
Todestag ... deshalb **gehn** wir zum Friedhof` — усечение
вспомогательного `ist` до `is` и личного окончания `-en` до `-n`.
Все шесть предыдущих проходов искали проглоченное `-e` у слабого
глагола и приклеенное `es`; `is` не подходило ни под один шаблон.

После расширения примета нашла по базе ещё четыре ряда, все с `is`:
`Der Fahrkartenschalter is dort drüben`, `Das alte Gerät is völlig
unnütz geworden`, `Mein Namensschild is kaputt gegangen`,
`Der Buchhalter hat Millionen unterschlagen und is jetzt flüchtig`.

Счёт проходов: 88, 15, 7, 7, 2, 1, 4.

Седьмая цифра — самая показательная из всех. Класс считался закрытым
шесть раз, и каждый раз «ноль» был честным: примета видела всё, что
умела видеть. Пять рядов она не видела не потому, что плохо написана, а
потому, что усечение в немецком бывает не одного вида, и список видов
растёт только от чтения.

    python -m app.scripts.fix_de_colloquial_7            # показать
    python -m app.scripts.fix_de_colloquial_7 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

FIXES: list[tuple[int, str, str, str, str]] = [
    (1407, "example_de", "Der Fahrkartenschalter is dort drüben",
     "Der Fahrkartenschalter ist dort drüben",
     "«is» вместо «ist»"),
    (8411, "example_de", "Das alte Gerät is völlig unnütz geworden",
     "Das alte Gerät ist völlig unnütz geworden",
     "«is» вместо «ist»"),
    (14256, "example_de", "Mein Namensschild is kaputt gegangen",
     "Mein Namensschild ist kaputt gegangen",
     "«is» вместо «ist»"),
    (16881, "example_de",
     "Der Buchhalter hat Millionen unterschlagen und is jetzt flüchtig",
     "Der Buchhalter hat Millionen unterschlagen und ist jetzt flüchtig",
     "«is» вместо «ist»"),
]


def main() -> None:
    apply_mode = "--apply" in sys.argv
    engine = create_engine(settings.DATABASE_URL_SYNC)

    ok, skipped = [], []
    with engine.connect() as conn:
        for wid, col, was, now, why in FIXES:
            cur = conn.execute(
                text(f"SELECT {col} FROM words WHERE id = :i"), {"i": wid}
            ).scalar()
            if (cur or "").strip() != was:
                skipped.append((wid, col, cur))
            else:
                ok.append((wid, col, was, now, why))

    print(f"=== правок {len(FIXES)}, совпало {len(ok)}, "
          f"пропущено {len(skipped)} ===\n")
    for wid, col, was, now, why in ok:
        print(f"  {wid} {col} — {why}")
        print(f"      было:  {was!r}")
        print(f"      стало: {now!r}")
    for wid, col, cur in skipped:
        print(f"  ПРОПУЩЕНО {wid} {col}: {cur!r}")

    if not apply_mode:
        print("\nэто показ. Для применения — флаг --apply")
        return

    with engine.begin() as conn:
        for wid, col, _, now, _ in ok:
            conn.execute(text(f"UPDATE words SET {col} = :v WHERE id = :i"),
                         {"v": now, "i": wid})
    print(f"\nприменено: {len(ok)}")

    with engine.connect() as conn:
        bad = 0
        for wid, col, _, now, _ in ok:
            cur = conn.execute(text(f"SELECT {col} FROM words WHERE id = :i"),
                               {"i": wid}).scalar()
            if (cur or "").strip() != now:
                print(f"  ТРЕВОГА: {wid} {col} не записалось")
                bad += 1
        print(f"самопроверка: не записалось {bad}")


if __name__ == "__main__":
    main()
