"""ВТОРОЙ ПРОХОД, блок 41 (ряды 8001–8200): 16 правок.

САМЫЙ ЧИСТЫЙ БЛОК ЗА ПРОХОД — 16 правок на 200 рядов, 8%. Для сравнения:
блоки 36–38 давали по 35–44. Причина видна: правка матчера в блоке 39
закрыла целый класс, который прежде давал по 3–5 правок в каждом блоке, а
польская полоса здесь впервые за шесть блоков оборвалась.

ОДНА ОШИБКА В СПИСКЕ, КОТОРУЮ ГЕЙТ НЕ ВИДИТ: `Freiwilliger` (11130)
держал в русском «добровол**ь**ец» — с мягким знаком, которого в
именительном падеже нет. В примере того же ряда стоит верное
«Доброволец».

ЗАМЕР ПО ЭТОМУ СЛЕДУ ОТМЕНЁН, И ПРИЧИНА ТОЧНАЯ. Украинский агентивный
суффикс «-ець» против русского «-ец» выглядел пригодным признаком:
правило «русская ячейка со следом -ець/-ьец/-ьц-» дало 41 попадание. Но
из 41 законны 40:

    пальца, пальцем, пальцы, кольцо, Кольцо, тельце, тельца,
    пыльцы, пыльцу, жильцы, владельца, добровольцы

Дело в русском чередовании «-лец → -льца»: «постоялец» → «постояльца»,
«кормилец» → «кормильца», «доброволец» → «добровольц**ы**». Мягкий знак
в косвенных падежах и в множественном числе — НОРМА, и ровно поэтому
`Freiwillige` (2480) с «добровольцы» верен, а `Freiwilliger` с
«добровольец» нет. Отличить их может только падеж, а его регулярное
выражение не видит.

Это десятый отменённый замер за проход, и причина та же, что у гибридов и
польского «sama»: прежде чем считать улов дефектами, надо спросить, не
норма ли это языка. Один дефект найден глазами и исправлен здесь.

ВИД КАРТОЧКИ — ВСЕГО ШЕСТЬ СЛУЧАЕВ, И ВСЕ МЕЛКИЕ. После правки матчера
класс сузился до того, что и должно было остаться: пример написан словом,
которого в списке нет вовсе.

    vielerlei   (7952) tr «pek çok farklı» при списке «çeşitli…»
    statuieren (16585) tr «ibret verdi» при «ibret olsun diye
                       cezalandırmak» — опознать мешала длина оборота
    umstellen   (7972) uk «переоснастити» при «перебудувати»
    Söhnchen   (15199) tr потерян сам уменьшительный смысл
    Bürschchen (15196) en «boy» при списке «little lad»
    Habgier    (11121) tr «hırs» при «açgözlülük»

КАЛЬКА С НЕМЕЦКОГО, ПОВТОРИВШАЯСЯ В ДВУХ ЯЗЫКАХ СРАЗУ: `aufrufen` (1175)
— «вызовут твоё имя» и «викличуть твоє ім'я». По-русски и по-украински
имя не вызывают, вызывают человека; в списке так и записано — «вызывать
по имени».
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ ошибка в самом списке ═══════════════════════════════════
    (11130, "translation_ru",
     "добровольец, волонтёр",
     "доброволец, волонтёр",
     "в именительном мягкого знака нет: «доброволец», но «добровольцы»"),

    # ══ вид карточки: слово не из своего списка ═════════════════
    (7952, "example_tr",
     "Pazarda pek çok farklı meyve vardı",
     "Pazarda çeşitli meyveler vardı",
     "«pek çok farklı» не из списка; «çeşitli» стоит в нём первым"),
    (16585, "example_tr",
     "Mahkeme bu cezayla ibret verdi",
     "Mahkeme bu kararla ibret olsun diye cezalandırdı",
     "оборот списка «ibret olsun diye cezalandırmak» опознаётся по "
     "«cezalandır-», а в примере его не было"),
    (7972, "example_uk",
     "Ми повинні повністю переоснастити виробництво",
     "Ми повинні повністю перебудувати виробництво",
     "«переоснастити» не из списка; «перебудувати» в нём есть"),
    (15199, "example_tr",
     "Bu benim sevgili oğlum, henüz üç yaşında",
     "Bu benim sevgili küçük oğlum, henüz üç yaşında",
     "потерян уменьшительный смысл `Söhnchen`; «küçük oğul» в списке есть"),
    (15196, "example_en",
     "The little boy was playing in the yard",
     "The little lad was playing in the yard",
     "«boy» не из списка; в нём «little lad»"),
    (11121, "example_tr",
     "Onun hırsı sınırı yok, hep daha fazla para istiyor",
     "Açgözlülüğünün sınırı yok, hep daha fazla para istiyor",
     "«hırsı sınırı yok» не согласовано, и «hırs» не из списка"),

    # ══ калька с немецкого в двух языках сразу ══════════════════
    (1175, "example_ru",
     "Сейчас вызовут твоё имя",
     "Сейчас вызовут тебя по имени",
     "имя не вызывают; в списке «вызывать по имени»"),
    (1175, "example_uk",
     "Зараз викличуть твоє ім'я",
     "Зараз викличуть тебе за іменем",
     "то же; в списке «викликати за іменем»"),

    # ══ форма, которой в языке нет ══════════════════════════════
    (11123, "example_uk",
     "Дитина не зважала на дощ і грала на вулиці",
     "Дитина не зважала на дощ і гралася на вулиці",
     "дитина «грається», а «грала» — про гру на інструменті"),
    (2303, "example_ru",
     "Этот материал биологически разлагаемый",
     "Этот материал биоразлагаемый",
     "«биологически разлагаемый» не по-людски; «биоразлагаемый» в списке"),

    # ══ потерянное и добавленное слово ══════════════════════════
    (11121, "example_pl",
     "Jego chciwość nie zna granic",
     "Jego chciwość nie zna granic, zawsze chce więcej pieniędzy",
     "потеряна вторая половина эталона «er will immer mehr Geld»"),
    (7955, "example_pl",
     "Muszę nadrobić zaległości z matematyki",
     "Jestem w tyle z matematyki, muszę to nadrobić",
     "потеряно «Ich bin hinterher»: в остальных четырёх оно есть"),
    (11131, "example_pl",
     "Jasno oświetlony pokój wyglądał przytulnie",
     "Oświetlony pokój wyglądał bardzo przytulnie",
     "«jasno» в эталоне нет, а «sehr» потеряно"),
    (17278, "example_pl",
     "Ruch przekierowano na inną ulicę",
     "Ruch przekierowano z powodu budowy",
     "«na inną ulicę» в эталоне нет, а «wegen der Baustelle» потеряно"),

    # ══ не тот термин ═══════════════════════════════════════════
    (16569, "example_uk",
     "Підозрюваного було взято під запобіжний арешт",
     "Підозрюваного було взято під захисний арешт",
     "«запобіжний арешт» другой юридический термин; в списке «захисний»"),
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
