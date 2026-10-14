"""
Немецкий глагол, переведённый причастием — во всех пяти языках сразу.

КАК НАШЛОСЬ. Вычитка дала один случай: у `pflücken` заголовок инфинитив,
а переводы причастия. Сплошной поиск по признаку «первое значение не
глагол» дал ещё двадцать таких слов.

ПОЧЕМУ ТАК ВЫШЛО. Переводили не заголовок, а причастие из примера:

    bezwingen   «Er hat den Berg endlich bezwungen»   → «покорённый»
    erringen    «Der errungene Sieg war das Ergebnis» → «завоёванный»
    speichern   «Die Datei ist gespeichert»           → «сохранённый»

В примерах стоит перфект, пассив или определение, и перевод пошёл за ними.
Человек учит «покорённый» там, где немецкое слово значит «покорять».

ПОЧЕМУ ЭТО ХУЖЕ ОБЫЧНОЙ ОПЕЧАТКИ. Ошибка одинакова во всех пяти языках, то
есть сверка языков между собой её не поймает. И карточка выглядит
безупречно: слово есть, диакритика на месте, пример содержит слово.

ЧЕГО ЗДЕСЬ НЕТ. Модальные и формы глагола «быть» — `soll`, `sollen`,
`sollten`, `seid`, `wären` — проверка тоже пометила, но там «должен» и
«should» это правильный перевод, а не причастие. Их не трогаю.

    python -m app.scripts.fix_verb_participles            # показать
    python -m app.scripts.fix_verb_participles --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# id: {колонка: (было, стало)}
FIXES: dict[int, dict[str, tuple[str, str]]] = {
    7202: {  # involvieren
        "translation_en": ("involved, engaged, implicated",
                           "to involve, to engage, to implicate"),
        "translation_ru": ("вовлечённый, причастный, задействованный",
                           "вовлекать, привлекать, задействовать"),
        "translation_uk": ("залучений, причетний, задіяний",
                           "залучати, втягувати, задіювати"),
        "translation_tr": ("dahil, karışmış, işin içinde",
                           "dahil etmek, katmak, işin içine sokmak"),
        "translation_pl": ("zaangażowany, wmieszany, zamieszany",
                           "angażować, wciągać, wplątywać"),
    },
    7195: {  # platzen
        "translation_en": ("burst, popped, cracked",
                           "to burst, to pop, to crack"),
        "translation_ru": ("лопнувший, треснувший, сорвавшийся",
                           "лопаться, трескаться, срываться"),
        "translation_uk": ("лопнутий, тріснутий, зірваний",
                           "лопатися, тріскатися, зриватися"),
        "translation_tr": ("patlamış, çatlamış, suya düşmüş",
                           "patlamak, çatlamak, suya düşmek"),
        "translation_pl": ("pęknięty, przebity",
                           "pękać, przebijać się"),
    },
    8208: {  # nageln
        "translation_en": ("nailed, nailed shut", "to nail, to nail shut"),
        "translation_ru": ("прибитый гвоздями, забитый гвоздями",
                           "прибивать гвоздями, заколачивать"),
        "translation_uk": ("прибитий цвяхами, забитий цвяхами",
                           "прибивати цвяхами, забивати"),
        "translation_tr": ("çivilenmiş, çivili", "çivilemek, çakmak"),
        "translation_pl": ("przybity gwoździami, zabity gwoździami",
                           "przybijać gwoździami, zabijać gwoździami"),
    },
    14209: {  # flüstern
        "translation_en": ("whispering, in a whisper", "to whisper, to murmur"),
        "translation_ru": ("шёпотом, шепча", "шептать, шептаться"),
        "translation_uk": ("шепотом, шепочучи", "шепотіти, шептатися"),
        "translation_tr": ("fısıldayarak", "fısıldamak"),
        "translation_pl": ("szeptem, szepcząc", "szeptać, szepnąć"),
    },
    17284: {  # stranden
        "translation_en": ("stranded, run aground, stuck",
                           "to run aground, to be stranded, to get stuck"),
        "translation_ru": ("севший на мель, выброшенный на берег, застрявший",
                           "садиться на мель, выбрасываться на берег, застревать"),
        "translation_uk": ("що сів на мілину, викинутий на берег, застряглий",
                           "сідати на мілину, викидатися на берег, застрягати"),
        "translation_tr": ("karaya oturmuş, mahsur kalmış",
                           "karaya oturmak, mahsur kalmak"),
        "translation_pl": ("osiadły na mieliźnie, wyrzucony na brzeg, utknięty",
                           "osiadać na mieliźnie, zostać wyrzuconym na brzeg, utknąć"),
    },
    8207: {  # kennzeichnen
        "translation_en": ("marked, labelled, characterized",
                           "to mark, to label, to characterize"),
        "translation_ru": ("отмеченный, обозначенный, помеченный",
                           "отмечать, обозначать, характеризовать"),
        "translation_uk": ("позначений, відмічений",
                           "позначати, маркувати"),
        "translation_tr": ("işaretlenmiş, belirtilmiş",
                           "işaretlemek, belirtmek"),
        "translation_pl": ("oznaczony, oznakowany",
                           "oznaczać, znakować"),
    },
    8367: {  # bezwingen
        "translation_en": ("conquered, defeated, overcome",
                           "to conquer, to defeat, to overcome"),
        "translation_ru": ("покорённый, побеждённый, преодолённый",
                           "покорять, побеждать, преодолевать"),
        "translation_uk": ("підкорений, переможений, подоланий",
                           "підкоряти, перемагати, долати"),
        "translation_tr": ("fethedilmiş, yenilmiş, aşılmış",
                           "fethetmek, yenmek, aşmak"),
        "translation_pl": ("pokonany, zdobyty, przezwyciężony",
                           "pokonywać, zdobywać, przezwyciężać"),
    },
    8295: {  # erringen
        "translation_en": ("achieved, won, gained",
                           "to achieve, to win, to gain"),
        "translation_ru": ("завоёванный, добытый, достигнутый",
                           "завоёвывать, добывать, достигать"),
        "translation_uk": ("здобутий, завойований, досягнутий",
                           "здобувати, завойовувати, досягати"),
        "translation_tr": ("kazanılmış, elde edilmiş, erişilmiş",
                           "kazanmak, elde etmek, erişmek"),
        "translation_pl": ("zdobyty, wywalczony, osiągnięty",
                           "zdobywać, wywalczyć, osiągać"),
    },
    8347: {  # schrumpfen
        "translation_en": ("shrunk, shrunken, reduced",
                           "to shrink, to contract, to diminish"),
        "translation_ru": ("уменьшившийся, сжавшийся, севший",
                           "уменьшаться, сжиматься, садиться"),
        "translation_uk": ("зменшений, зсілий, стиснутий",
                           "зменшуватися, стискатися, сідати"),
        "translation_tr": ("küçülmüş, daralmış, çekmiş",
                           "küçülmek, daralmak, çekmek"),
        "translation_pl": ("skurczony, zmniejszony",
                           "kurczyć się, zmniejszać się"),
    },
    13034: {  # verunglücken
        "translation_en": ("crashed, involved in an accident",
                           "to have an accident, to crash"),
        "translation_ru": ("попавший в аварию, разбившийся, пострадавший в аварии",
                           "попадать в аварию, разбиваться, гибнуть в аварии"),
        "translation_uk": ("потерпілий в аварії, розбитий",
                           "потрапляти в аварію, розбиватися"),
        "translation_tr": ("kaza geçirmiş, düşmüş", "kaza geçirmek, düşmek"),
        "translation_pl": ("rozbity, poszkodowany w wypadku",
                           "ulec wypadkowi, rozbić się"),
    },
    11368: {  # verhöhnen
        "translation_en": ("mocked, ridiculed, jeered at",
                           "to mock, to ridicule, to jeer at"),
        "translation_ru": ("высмеянный, осмеянный, поруганный",
                           "высмеивать, осмеивать, глумиться"),
        "translation_uk": ("висміяний, осміяний, зневажений",
                           "висміювати, глузувати, зневажати"),
        "translation_tr": ("alay edilen, küçümsenen, dalga geçilen",
                           "alay etmek, küçümsemek, dalga geçmek"),
        "translation_pl": ("wyśmiany, wyszydzony, wykpiony",
                           "wyśmiewać, wyszydzać, kpić"),
    },
    12750: {  # verheilen
        "translation_en": ("healed, closed up", "to heal, to close up"),
        "translation_ru": ("заживший, зарубцевавшийся",
                           "заживать, зарубцовываться"),
        "translation_uk": ("загоєний, зарубцьований",
                           "загоюватися, рубцюватися"),
        "translation_tr": ("iyileşmiş, kapanmış", "iyileşmek, kapanmak"),
        "translation_pl": ("zagojony, zabliźniony", "goić się, zabliźniać się"),
    },
    16525: {  # beschatten
        "translation_en": ("shadowed, under surveillance, shaded",
                           "to shadow, to tail, to shade"),
        "translation_ru": ("под наблюдением, затенённый",
                           "вести слежку, следить, затенять"),
        "translation_uk": ("під наглядом, затінений",
                           "стежити, вести стеження, затінювати"),
        "translation_tr": ("izlenen, gözetim altında, gölgeli",
                           "izlemek, takip etmek, gölgelemek"),
        "translation_pl": ("śledzony, zacieniony",
                           "śledzić, obserwować, zacieniać"),
    },
    8018: {  # einteilen
        "translation_en": ("divided, assigned, scheduled",
                           "to divide, to assign, to schedule"),
        "translation_ru": ("разделённый, распределённый, расписанный",
                           "разделять, распределять, расписывать"),
        "translation_uk": ("розподілений, поділений, розписаний",
                           "розподіляти, ділити, розписувати"),
        "translation_tr": ("bölünmüş, ayrılmış, görevlendirilmiş",
                           "bölmek, ayırmak, görevlendirmek"),
        "translation_pl": ("podzielony, przydzielony, rozplanowany",
                           "dzielić, przydzielać, rozplanowywać"),
    },
    8034: {  # heimsuchen
        "translation_en": ("afflicted, stricken, haunted",
                           "to afflict, to strike, to haunt"),
        "translation_ru": ("поражённый, пострадавший, измученный",
                           "поражать, обрушиваться, преследовать"),
        "translation_uk": ("уражений, потерпілий, змучений",
                           "уражати, навідуватися, переслідувати"),
        "translation_tr": ("musibete uğramış, felakete uğramış, perili",
                           "musallat olmak, felakete uğratmak, dadanmak"),
        "translation_pl": ("nawiedzony, dotknięty, udręczony",
                           "nawiedzać, dotykać, dręczyć"),
    },
    13750: {  # bekleiden
        "translation_en": ("dressed, clothed", "to clothe, to dress"),
        "translation_ru": ("одетый, облачённый", "одевать, облачать"),
        "translation_uk": ("одягнений, вбраний", "одягати, вбирати"),
        "translation_tr": ("giyinmiş, giydirilmiş", "giydirmek, giyinmek"),
        "translation_pl": ("ubrany, odziany", "ubierać, odziewać"),
    },
    12714: {  # aufschlitzen
        "translation_en": ("slashed, slit open, cut open",
                           "to slash, to slit open, to cut open"),
        "translation_ru": ("разрезанный, вспоротый, порезанный",
                           "разрезать, вспарывать, распарывать"),
        "translation_uk": ("розрізаний, розпанаханий, порізаний",
                           "розрізати, розпорювати, розтинати"),
        "translation_tr": ("yarılmış, kesilmiş, deşilmiş",
                           "yarmak, kesmek, deşmek"),
        "translation_pl": ("rozcięty, rozpruty", "rozcinać, rozpruwać"),
    },
    17595: {  # speichern
        "translation_en": ("saved, stored", "to save, to store"),
        "translation_ru": ("сохранённый, записанный", "сохранять, записывать"),
        "translation_uk": ("збережений, записаний", "зберігати, записувати"),
        "translation_tr": ("kaydedilmiş, saklanmış", "kaydetmek, saklamak"),
        "translation_pl": ("zapisany, zachowany", "zapisywać, przechowywać"),
    },
    10810: {  # vernachlässigen
        "translation_en": ("neglected, run-down, uncared-for",
                           "to neglect, to disregard, to let go"),
        "translation_ru": ("запущенный, заброшенный, неухоженный",
                           "запускать, забрасывать, пренебрегать"),
        "translation_uk": ("занедбаний, закинутий, недоглянутий",
                           "занедбувати, закидати, нехтувати"),
        "translation_tr": ("ihmal edilmiş, bakımsız", "ihmal etmek, savsaklamak"),
        "translation_pl": ("zaniedbany, niedbały", "zaniedbywać, lekceważyć"),
    },
    18018: {  # neutralisieren
        "translation_en": ("neutralized, rendered harmless",
                           "to neutralize, to render harmless"),
        "translation_ru": ("нейтрализованный, обезвреженный",
                           "нейтрализовать, обезвреживать"),
        "translation_uk": ("нейтралізований, знешкоджений",
                           "нейтралізувати, знешкоджувати"),
        "translation_tr": ("etkisiz hâle getirilmiş, nötrleştirilmiş",
                           "nötrleştirmek, etkisiz hâle getirmek"),
        "translation_pl": ("zneutralizowany, unieszkodliwiony",
                           "neutralizować, unieszkodliwiać"),
    },
}


def main() -> None:
    apply_mode = "--apply" in sys.argv
    engine = create_engine(settings.DATABASE_URL_SYNC)

    ok, skipped = [], []
    with engine.connect() as conn:
        for wid, cols in FIXES.items():
            de = conn.execute(text("SELECT word_de FROM words WHERE id = :i"),
                              {"i": wid}).scalar()
            for col, (was, now) in cols.items():
                cur = conn.execute(
                    text(f"SELECT {col} FROM words WHERE id = :i"), {"i": wid}
                ).scalar()
                if (cur or "").strip() != was:
                    skipped.append((wid, de, col, cur))
                else:
                    ok.append((wid, de, col, was, now))

    print(f"=== слов {len(FIXES)}, ячеек {len(ok) + len(skipped)}, "
          f"совпало {len(ok)}, пропущено {len(skipped)} ===\n")
    last = None
    for wid, de, col, was, now in ok:
        if wid != last:
            print(f"  {wid} {de}")
            last = wid
        print(f"      {col[-2:]}: {was!r}")
        print(f"      {'':2}  → {now!r}")
    for wid, de, col, cur in skipped:
        print(f"  ПРОПУЩЕНО {wid} {de} {col}: {cur!r}")

    if not apply_mode:
        print("\nэто показ. Для применения — флаг --apply")
        return

    with engine.begin() as conn:
        for wid, _, col, _, now in ok:
            conn.execute(text(f"UPDATE words SET {col} = :v WHERE id = :i"),
                         {"v": now, "i": wid})
    print(f"\nприменено ячеек: {len(ok)}")
    print("Переводы изменились — нужна пересборка групп и пересинтез озвучки")

    with engine.connect() as conn:
        bad = 0
        for wid, _, col, _, now in ok:
            cur = conn.execute(text(f"SELECT {col} FROM words WHERE id = :i"),
                               {"i": wid}).scalar()
            if (cur or "").strip() != now:
                print(f"  ТРЕВОГА: {wid} {col} не записалось")
                bad += 1
        print(f"самопроверка: не записалось {bad}")


if __name__ == "__main__":
    main()
