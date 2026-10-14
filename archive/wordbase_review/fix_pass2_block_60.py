"""ВТОРОЙ ПРОХОД, блок 60 (ряды 11801–12000): 11 правок.

ПЛОТНОСТЬ 5.5% — участок, начавшийся в блоке 57, кончился окончательно:
ни одной подмены целиком, ни одной сочинённой фразы. Первая половина
блока дала три правки на сто рядов.

ТУРЕЦКИЙ — ПЯТЬ РЯДОВ ИЗ ОДИННАДЦАТИ, и он остаётся самым слабым языком
базы в последних блоках:

    Antiquität (14838) «Mobilya 18. yüzyıldan gerçek bir antika» —
                       потеряна связка «-dır» и указание «Bu».
    Aufgebot   (16974) «polis KONUŞLANDIRMASI» (развёртывание) не из
                       списка «güç, sevk edilen kuvvet, kadro».
    Übertreibung(14329) «senin AÇINDAN» — опечатка, нужно «açısından».
    unverschämt(11601) «utanmazCA bir yalandı» — наречие на месте
                       определения; нужно «utanmaz bir yalan».
    Beerdigungsinstitut(15337) «ANIT MERASİM» — так не говорят,
                       поминальная церемония это «anma töreni»; плюс
                       «Cenaze işleri şirketi» вместо «cenaze şirketi»
                       из списка.

ПРИТЯЖАТЕЛЬНОЕ, КОТОРОЕ МЕНЯЕТ СМЫСЛ, два ряда:

    Zeichner (9292) ru «Художник сделал МОЙ фантастический портрет»
                    uk «Художник зробив МІЙ фантастичний портрет»
                    de «hat ein fantastisches Porträt VON MIR gemacht»

«Мой портрет» по-русски и по-украински читается как «портрет,
принадлежащий мне», а немецкое «von mir» значит «изображающий меня».
Разница невелика на вид, но меняет, кто на картине. Правильно «портрет
с меня».

ПОТЕРЯ «zu» (слишком), два ряда: `Formulierung` (14330) en «The wording
is unclear» и uk «Формулювання неясне» при немецком «ist ZU unklar» —
русский и польский «слишком» держат. Без него фраза говорит, что
формулировка просто неясна, а не что она неясна ЧЕРЕСЧУР.

Плюс `leichtgläubig` (11595) pl «o wiele za BARDZO łatwowierny» —
двойное усиление, по-польски хватает «o wiele za»; и `Krematorium`
(15336) pl будущее время при немецком настоящем.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ турецкий ═══════════════════════════════════════════════
    (14838, "example_tr",
     "Mobilya 18. yüzyıldan gerçek bir antika",
     "Bu mobilya 18. yüzyıldan kalma gerçek bir antikadır",
     "потеряна связка «-dır» и указание «Bu»"),
    (16974, "example_tr",
     "Geniş polis konuşlandırması etkileyiciydi",
     "Geniş polis gücü etkileyiciydi",
     "«konuşlandırması» не из списка; «güç» в нём первое"),
    (14329, "example_tr",
     "Bu senin açından oldukça büyük bir abartıydı",
     "Bu, senin açısından oldukça büyük bir abartıydı",
     "опечатка: «açından» → «açısından»"),
    (11601, "example_tr",
     "Bu ondan utanmazca bir yalandı",
     "Bu, ondan utanmaz bir yalandı",
     "наречие «utanmazca» на месте определения"),
    (15337, "example_tr",
     "Cenaze işleri şirketi anıt merasim için tüm düzenlemeleri yaptı",
     "Cenaze şirketi anma töreni için tüm düzenlemeleri yaptı",
     "«anıt merasim» так не говорят — «anma töreni»; и «cenaze şirketi» из списка"),

    # ══ притяжательное, меняющее смысл ═════════════════════════
    (9292, "example_ru",
     "Художник сделал мой фантастический портрет",
     "Художник сделал фантастический портрет с меня",
     "«мой портрет» читается как принадлежащий мне; «von mir» — изображающий меня"),
    (9292, "example_uk",
     "Художник зробив мій фантастичний портрет",
     "Художник зробив фантастичний портрет з мене",
     "то же в украинском"),

    # ══ потеря «zu» (слишком) ══════════════════════════════════
    (14330, "example_en",
     "The wording is unclear",
     "The wording is too unclear",
     "потеряно «zu»; ru и pl «слишком» держат"),
    (14330, "example_uk",
     "Формулювання неясне",
     "Формулювання занадто неясне",
     "то же в украинском"),

    # ══ двойное усиление и время ═══════════════════════════════
    (11595, "example_pl",
     "Jest o wiele za bardzo łatwowierny i nabiera się na każdą sztuczkę",
     "Jest o wiele za łatwowierny i nabiera się na każdą sztuczkę",
     "«o wiele za bardzo» — двойное усиление"),
    (15336, "example_pl",
     "Ciało zostanie przewiezione do krematorium",
     "Ciało przewozi się do krematorium",
     "будущее при немецком настоящем «wird gebracht»"),
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
