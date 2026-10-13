"""ВТОРОЙ ПРОХОД, блок 56 (ряды 11001–11200): 13 правок.

ГЛАВНОЕ ЗА БЛОК — НЕ ПРАВКИ, А ЛОВУШКА В ДЕВЯТОМ ГЕЙТЕ.

Проверяя блок, я усомнился в ПОЛНОТЕ списка `ADJ_NOUN_STEMS`
(субстантивированные прилагательные, у которых после определённого
определителя нужно слабое «-e»). Замер: ищем заголовки, у которых в базе
есть ОБЕ формы, <основа>e и <основа>er. Выдал 31 кандидата, из них восемь
настоящих и в списке отсутствовавших:

    Angeklagt, Angestellt, Gefangen, Geliebt, Gesandt, Geschworen,
    Gläubig, Verbündet

Я добавил все восемь — и гейт тут же упал:

    СКЛОНЕНИЕ 17836 Gläubiger «Der Gläubiger»: нужно «-e»

**И это был МОЙ промах, а не дефект базы.** «der Gläubiger» значит
КРЕДИТОР и является обычным существительным на -er, а не сильной формой
прилагательного. Верующий — отдельный ряд `Gläubige` (14791). Основа
«Gläubig» из списка убрана с объяснением.

ПРАВИЛО, КОТОРОЕ ИЗ ЭТОГО СЛЕДУЕТ: замер полноты необходим, но
НЕДОСТАТОЧЕН — каждого кандидата надо проверить на ОМОНИМИЧНОЕ имя
деятеля на -er. Остальные семь проверены: у «Angeklagter»,
«Angestellter», «Gefangener», «Geliebter», «Gesandter», «Geschworener»,
«Verbündeter» самостоятельного значения на -er нет.

И отдельно: 23 кандидата из 31 были шумом от неродственных пар
существительных — «Apotheke/Apotheker», «Geige/Geiger»,
«Lehre/Lehrer», «Miete/Mieter», «Wunde/Wunder». Признак «в базе есть обе
формы» класс сам по себе не определяет.

ПРАВКИ БЛОКА — три вида, те же, что в блоках 54 и 55.

ПОДМЕНЫ (не целиком, а одного куска), четыре ряда:

    Schuldner (16886) pl «Dłużnik w końcu ODDAŁ nam pieniądze» вместо
                      «zahlt seine Raten nicht mehr» — смысл перевёрнут:
                      в немецком он НЕ платит, в польском вернул
    Klarinette(14799) pl «MÓJ BRAT gra na klarnecie» вместо «Er spielt
                      Klarinette IM ORCHESTER»
    Probeaufnahme(14790) pl «wyszły świetnie» вместо «waren sehr
                      vielversprechend»
    Diva      (14794) uk «повара» — русизм; по-українськи «кухаря»

СЛОВО НЕ ИЗ СВОЕГО СПИСКА, три ряда:

    seinerzeit(18929) uk «Колись» при «тоді, у той час, свого часу»
    Fehltritt  (8536) uk «помилка» при «промах, хиба, провина»
    Riecher    (8537) tr «koku alma YETENEĞI» (способность) при
                      «koku alma DUYUSU» (чувство) в списке

ВРЕМЯ, ЛИЦО И ПОТЕРЯ, шесть рядов: `begnadigen` (16887) pl прошедшее при
немецком будущем; `angreifbar` (8529) pl настоящее при прошедшем и
потеряно «hatte viele Lücken»; `unterschlagen` (16881) uk «втікає»
(процесс) при «ist flüchtig» (в бегах); `Liedchen` (14792) pl потеряно
«immer» и «nuciła» (напевала) вместо «sang»; `Hörgerät` (13105) pl
потеряно «Mein»; `abwegig` (8526) tr «gerçekçi olmayan görünüyor» —
причастие при «görünmek» рассыпается, нужно «gerçek dışı».
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ подмена куска фразы ════════════════════════════════════
    (16886, "example_pl",
     "Dłużnik w końcu oddał nam pieniądze",
     "Dłużnik przestał płacić swoje raty",
     "смысл перевёрнут: в немецком он НЕ платит, в польском вернул деньги"),
    (14799, "example_pl",
     "Mój brat gra na klarnecie",
     "On gra na klarnecie w orkiestrze",
     "«мой брат» вместо «Er», потерян оркестр"),
    (14790, "example_pl",
     "Zdjęcia próbne do filmu wyszły świetnie",
     "Zdjęcia próbne do filmu były bardzo obiecujące",
     "«вышли отлично» вместо «waren sehr vielversprechend»"),
    (14794, "example_uk",
     "Дива відмовлялася працювати без свого особистого повара",
     "Дива відмовлялася працювати без свого особистого кухаря",
     "«повар» — русизм; по-українськи «кухар»"),

    # ══ слово не из своего списка ══════════════════════════════
    (18929, "example_uk",
     "Колись це було абсолютно нормально, але сьогодні цього ніколи не зробили б",
     "Свого часу це було абсолютно нормально, але сьогодні цього ніколи не зробили б",
     "«Колись» не из списка; «свого часу» в нём третье"),
    (8536, "example_uk",
     "Це була велика помилка з його боку",
     "Це був великий промах з його боку",
     "«помилка» не из списка; «промах» в нём первый"),
    (8537, "example_tr",
     "Köpeklerin iyi bir koku alma yeteneği var",
     "Köpeklerin iyi bir koku alma duyusu var",
     "«yeteneği» (способность) не из списка; «duyusu» (чувство) в нём первое"),

    # ══ время и лицо ═══════════════════════════════════════════
    (16887, "example_pl",
     "Prezydent ułaskawił skazanego",
     "Prezydent ułaskawi skazanego",
     "прошедшее при немецком будущем «wird begnadigen»"),
    (8529, "example_pl",
     "Jego argumenty są łatwo podatne na atak",
     "Jego argumentacja była łatwa do podważenia i miała wiele luk",
     "настоящее при прошедшем, потеряно «hatte viele Lücken»"),
    (16881, "example_uk",
     "Бухгалтер присвоїв мільйони і тепер втікає",
     "Бухгалтер присвоїв мільйони і тепер у бігах",
     "«втікає» (процесс) при «ist flüchtig» (в бегах)"),

    # ══ потеря слова ═══════════════════════════════════════════
    (14792, "example_pl",
     "Babcia nuciła piosenkę przy gotowaniu",
     "Babcia zawsze śpiewała piosenkę, kiedy gotowała",
     "потеряно «immer»; «nuciła» (напевала) вместо «sang»"),
    (13105, "example_pl",
     "Dziadek nosi aparat słuchowy",
     "Mój dziadek nosi aparat słuchowy",
     "потеряно «Mein»"),

    # ══ грамматика турецкого ═══════════════════════════════════
    (8526, "example_tr",
     "Planın tamamen saçma ve gerçekçi olmayan görünüyor",
     "Planın tamamen saçma ve gerçek dışı görünüyor",
     "причастие «olmayan» при «görünmek» рассыпается; нужно «gerçek dışı»"),
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
