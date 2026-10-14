"""ВТОРОЙ ПРОХОД, блок 14 (ряды 2601–2800): 24 правки.

Блок дал класс, какого раньше в таком количестве не попадалось:
**ПОДМЕНЁННОЕ ПРЕДЛОЖЕНИЕ** — перевод говорит не то, что эталон, а
что-то своё. Пять рядов:

    auftreten (14438)   de «Die Band tritt heute Abend auf»
        en «Problems can occur at any time»
        uk «Проблеми можуть виникнути в будь-який момент»
        tr «Sorunlar her zaman ortaya çıkabilir»
        Три языка перевели ДРУГОЕ значение слова (возникать), и притом
        все три одинаково — то есть ошибка пришла из одного источника.
        Русский и польский написаны верно.

    vergangen (18688)   de «Die vergangene Woche war echt stressig»
        en «Let's just forget the past» — вообще про другое

    Ausland (1188)      de «Ich reise gern ins Ausland»
        uk «Закордон мене завжди вабив» — «заграница меня всегда
        манила», другая фраза

    umgeben (6879)      de «Bäume umgeben das Haus»
        tr «Bahçeyi yüksek bir duvar çevreliyor» — «сад окружает
        высокая стена»

    locken (10356)      de «Das Angebot soll Kunden locken»
        uk «Реклама повинна приваблювати покупців» — подлежащее
        подменено: реклама вместо предложения

ЗАМЕР, КОТОРЫЙ ЗАКРЫЛ ВОПРОС. Напрашивался формальный признак: если в
переводе нет НИ ОДНОГО слова из его же списка переводов, значит перевод
ушёл от ряда. Проверено по базе через настоящую `main_meaning` и
`_stem_in`, а не по догадке.

**7 попаданий, и все семь — артефакты.** Это предлоги (`bei`, `in`,
`um`, `mit`, `im`, `beim`, `plus`), где английский и турецкий дают
слово короче четырёх букв («at», «with», «ile»), а `_STEM_MIN` в
`language_service` равен четырём. То есть строгая форма класса по базе
ЧИСТА, а найденные глазами ряды — слабее: там выбран не тот вариант, а
не ни один. Формального признака у этого нет.

Ещё в блоке:

    Werkzeug (3014)  tr «Bu iş için ALETA ihtiyacım var»
        «aleta» не форма турецкого: датив от «alet» — «alete».

    Nacken (12554)  uk «У мене болить шия ПІСЛЯ СНУ»
        В эталоне никакого сна нет, и «шия» это Hals, а Nacken —
        потилиця, то есть первый вариант перевода.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ── КЛАСС: подменённое предложение ──────────────────────────
    (14438, "example_en",
     "Problems can occur at any time",
     "The band is performing tonight",
     "перевод про другое значение (возникать); ru и pl написаны верно"),
    (14438, "example_uk",
     "Проблеми можуть виникнути в будь-який момент",
     "Гурт виступає сьогодні ввечері",
     "то же"),
    (14438, "example_tr",
     "Sorunlar her zaman ortaya çıkabilir",
     "Grup bu akşam sahneye çıkıyor",
     "то же"),
    (18688, "example_en",
     "Let's just forget the past",
     "Last week was really stressful",
     "перевод вообще про другое: эталон про прошлую неделю"),
    (1188, "example_uk",
     "Закордон мене завжди вабив",
     "Я люблю їздити за кордон",
     "другая фраза: эталон «Ich reise gern ins Ausland»"),
    (6879, "example_tr",
     "Bahçeyi yüksek bir duvar çevreliyor",
     "Ağaçlar evi çevreliyor",
     "другая фраза: эталон «Bäume umgeben das Haus»"),
    (10356, "example_uk",
     "Реклама повинна приваблювати покупців",
     "Ця пропозиція має приваблювати клієнтів",
     "подлежащее подменено: реклама вместо предложения"),

    # ── форма, которой в языке нет ──────────────────────────────
    (3014, "example_tr",
     "Bu iş için aleta ihtiyacım var",
     "Bu iş için doğru alete ihtiyacım var",
     "«aleta» не форма турецкого: датив от «alet» — «alete»; и потеряно «richtige»"),

    # ── выдуманное обстоятельство и дальний вариант ─────────────
    (12554, "example_uk",
     "У мене болить шия після сну",
     "У мене болить потилиця",
     "«після сну» в эталоне нет, и «шия» это Hals, а Nacken — потилиця"),
    (18172, "example_pl",
     "W parku stoi stara studnia",
     "W parku stoi stara fontanna",
     "в парке это фонтан, и так в остальных четырёх языках"),
    (18174, "example_uk",
     "Сіно лежить у старій коморі",
     "Сіно лежить у старій клуні",
     "«комора» это кладовка; «клуня» стоит первым в переводе"),
    (10352, "example_uk",
     "Після голу почалася велика радість",
     "Після голу почалися радісні вигуки",
     "«радість» слабее, чем Jubel: там именно крики"),
    (6890, "example_tr",
     "Bu şarkıyı hiç bilmiyorum",
     "Bu şarkı bana tamamen yabancı",
     "перевод превратил прилагательное в глагол; «yabancı» есть в списке"),
    (10343, "example_uk",
     "Мені дуже полегшало",
     "Я відчуваю велике полегшення",
     "безличное вместо прилагательного ряда"),
    (1710, "example_tr",
     "Mahalle dostça",
     "Mahalle dostane",
     "«dostça» это наречие, нужно прилагательное"),
    (13500, "example_ru",
     "В том доме напротив живёт мой друг",
     "В том доме вон там живёт мой друг",
     "«da drüben» это вон там, а не напротив"),
    (13500, "example_uk",
     "У тому будинку навпроти живе мій друг",
     "У тому будинку он там живе мій друг",
     "то же"),

    # ── потерянное слово ────────────────────────────────────────
    (12551, "example_uk",
     "Аварія була смертельною",
     "На жаль, аварія була смертельною",
     "потеряно «leider»: в ru, en, tr и pl оно есть"),
    (2345, "example_en",
     "There was a theft",
     "There was a theft in our shop yesterday",
     "потеряно «Gestern ... in unserem Geschäft»: в ru, uk и pl оно есть"),
    (2345, "example_tr",
     "Bir hırsızlık oldu",
     "Dün mağazamızda bir hırsızlık oldu",
     "то же"),
    (2345, "example_uk",
     "Вчора в магазині сталася крадіжка",
     "Вчора в нашому магазині сталася крадіжка",
     "потеряно «unserem»"),

    # ── добавленная обязанность и время глагола ─────────────────
    (6872, "example_uk",
     "Нам потрібно знову поставити намет",
     "Ми знову ставимо намет",
     "в эталоне нет модального: «Wir bauen das Zelt wieder auf»"),
    (6872, "example_en",
     "We need to set up the tent again",
     "We set up the tent again",
     "то же"),
    (8818, "example_uk",
     "Офіціант принесе нам рахунок",
     "Офіціант несе нам рахунок",
     "будущее против «bringt»; в ru, tr, en и pl настоящее"),
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
