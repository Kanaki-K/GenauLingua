"""ТРЕТИЙ ПРОХОД, блок 2 (ряды 201–400): 3 ячейки, из них 1 сквозная.

БЛОК ПОЧТИ ЧИСТ, И ЭТО ГЛАВНЫЙ РЕЗУЛЬТАТ. Ряды 201–400 — это по-прежнему
служебный слой (`andere`, `nehmen`, `darf`, `beide`, `wann`, `je`,
предлоги, местоимения) плюс первая сотня обиходных существительных
(`Arbeit`, `Familie`, `Problem`, `Wasser`, `Schule`). Прочитан целиком,
и дефектов в нём — один ряд. Замеченное глазом в основном растворилось
при замере, и это стоит записать прямо, потому что иначе третий проход
начнёт «исправлять» стиль базы.

ЧТО РАСТВОРИЛОСЬ: ПОЛЬСКОЕ БУДУЩЕЕ ПРИ НЕМЕЦКОМ НАСТОЯЩЕМ.
`andere` (21) pl «POJEDZIEMY inną drogą» при «Wir nehmen einen anderen
Weg». Выглядит как снос времени. Но в этом же блоке:

    später (872)  de «Wir essen später»   tr/uk/pl — будущее, de/ru — настоящее
    holen (1549)  de «Ich hole das Buch»  ru/uk/pl — будущее, de/en/tr — настоящее

Три ряда в одном блоке, разные языки, одно и то же — значит приём, а не
дефект. Это подтверждает замер блока 63 (второй проход), где польское
«zostanie» при немецком пассиве нашлось 14 раз из 14. Славянский
совершенный вид и турецкое «-acak» — штатный перевод немецкого
настоящего, когда речь о будущем действии. **Не править.**

════════════════════════════════════════════════════════════════════════
НАЙДЕННЫЙ КЛАСС: ПОТЕРЯННОЕ «ЕЩЁ РАЗ»
════════════════════════════════════════════════════════════════════════

Повод — `äh` (13829, A1): «Äh, wie heißt du NOCHMAL?» Вся соль фразы в
«nochmal»: человек спрашивает имя ВТОРОЙ раз, потому что забыл. Русский,
украинский и английский это держат («напомни», «нагадай», «again»), а
польский и турецкий потеряли:

    pl «Eee, jak ty się nazywasz?»   ← просто «как тебя зовут»
    tr «Ee, adın ne?»                ← то же

Замер по базе: немецкое «nochmal / noch einmal / wieder / erneut» и
РОВНО ОДИН язык из четырёх (en/ru/uk/pl) без соответствия — 5 попаданий.
Три ложные, и ложные поучительно:

    Lieblingsbuch (9632) pl «czytam ją WCIĄŻ OD NOWA»   — повтор есть,
                                        просто другими словами
    Strolch      (11314) en «played ANOTHER prank»      — «another» и есть
                                        «wieder»
    pardon       (13956) pl «możesz to POWTÓRZYĆ?»      — повтор внутри
                                        глагола, а не отдельным словом

**Вывод о признаке: «ещё раз» бывает спрятано в глаголе или в
определении, и регексп на наречия этого не видит.** Поэтому примету для
этого класса писать НЕЛЬЗЯ — она будет врать в три случая из пяти.
Проверено глазом, исправлено руками, класс закрыт.

Настоящих попаданий два, и оба польские:

    äh      (13829, A1) «Eee, jak ty się nazywasz?»          ← потеряно
    offline (17635, B2) «System jest offline, spróbuj później» ← потеряно

У `offline` расклад самый чистый: четыре языка «ещё раз» держат (en
«again», ru «ещё раз», uk «ще раз», tr «tekrar»), польский один его
обронил. Ряд лежит далеко за границей блока — это сквозная правка, какой
и должен давать проход.

ТУРЕЦКИЙ ПОЧИНЕН СВОИМ СОБСТВЕННЫМ СРЕДСТВОМ, А НЕ КАЛЬКОЙ. По-турецки
«как тебя зовут, напомни» — это не «tekrar» и не «bir daha», а ПРОШЕДШЕЕ
ВРЕМЯ: «adın NEYDİ?», буквально «как твоё имя БЫЛО?». Ровно та же
работа, что делает немецкое «nochmal», и ровно так турок и спросит.
Одно слово вместо вставки наречия.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    (13829, "example_pl",
     "Eee, jak ty się nazywasz?",
     "Eee, przypomnij mi, jak się nazywasz?",
     "потеряно «nochmal» — вся соль фразы; ru «напомни», uk «нагадай», "
     "en «again» его держат"),
    (13829, "example_tr",
     "Ee, adın ne?",
     "Ee, adın neydi?",
     "то же «nochmal»; по-турецки это прошедшее время «neydi», "
     "а не вставное наречие"),
    (17635, "example_pl",
     "System jest offline, spróbuj później",
     "System jest offline, spróbuj ponownie później",
     "сквозная: «nochmal» держат четыре языка, польский один обронил"),
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
