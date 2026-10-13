"""ВТОРОЙ ПРОХОД, блок 24 (ряды 4601–4800): 24 правки.

ЗАМЕР, КОТОРЫЙ ДАЛ ВЛАДЕЛЬЦУ ТОЧНЫЙ СПИСОК. Блок показал две пары
рядов на одно слово: `Beamter` (8921) рядом с `Beamte` (8855 и 8892), и
`Vorgesetzter` (8926) рядом с `Vorgesetzte` (8837 и 9178). Это повод
замерить дубли по всей базе.

Сравнение основы заголовка и части речи даёт 446 групп, и почти все
ЗАКОННЫ: `dunkel` в «Es wird dunkel» и в «dunkle Schokolade» — разные
значения; `keine`/`keinen`/`keiner` — разные формы, которым учат
отдельно; `Apotheke`/`Apotheker` — разные слова. По основе дубль не
ищется.

А вот строгая проверка — ТО ЖЕ СЛОВО И ТОТ ЖЕ НЕМЕЦКИЙ ПРИМЕР — даёт
ровно **восемь групп**, и каждая это две карточки, учащие одному:

    bestimmt     103 и 1269    «Er kommt bestimmt»
    du           195 и 1328    «Kommst du heute Abend mit?»
    intern      2582 и 7388    «Das ist eine interne Angelegenheit»
    mal         6705 и 13262   «Komm mal her»
    Dunkelheit  6716 и 15414   «In der Dunkelheit kann ich nichts sehen»
    grob        7005 и 7629    «Das war eine grobe Beleidigung»
    platzen     7115 и 7195    «Der Ballon ist geplatzt»
    aufrichtig 10384 и 11525   «Das war eine aufrichtige Entschuldigung»

**Эти ряды НЕ ТРОНУТЫ.** Удалить ряд или развести примеры — решение
владельца: удаление меняет размер базы, числа целостности и связи
`user_words`. Список записан в HANDOVER точными id.

Отдельно подтверждено решение первого прохода про ОДИНАКОВЫЙ ПРИМЕР У
РАЗНЫХ СЛОВ: таких групп 26, и это почти всегда не дефект. «Das Bild
hängt an der Wand» служит рядам `an`, `hängen` и `Wand` — одна
естественная фраза на три слова, и это скорее хорошо.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ подмена ═════════════════════════════════════════════════
    (12209, "example_pl",
     "Cały dzień obijamy się w domu",
     "Dzisiaj chcemy tylko obijać się w domu",
     "подмена: эталон «Wir wollen heute nur zu Hause rumhängen»"),
    (13528, "example_pl",
     "Masz niezliczone możliwości rozwoju kariery",
     "Istnieją niezliczone możliwości dla twojej kariery",
     "подмена подлежащего: эталон «Es gibt»"),

    # ══ слова ряда в примере не было ════════════════════════════
    (16272, "example_en",
     "The product is defective and won't be sold",
     "The product is a reject and won't be sold",
     "ни одного слова из списка в примере не было; «reject» есть"),
    (10609, "example_uk",
     "Новий дизайн дійсно привабливий та сучасний",
     "Новий дизайн дійсно приємний та сучасний",
     "«привабливий» нет в списке, а «приємний» стоит первым"),
    (12666, "example_tr",
     "Adli tıp doktoru cesedi inceledi",
     "Adli tıp uzmanı cesedi inceledi",
     "в списке «adli tıp uzmanı», а не «doktoru»"),
    (16282, "example_ru",
     "Агент следит за объектом",
     "Агент следит за объектом наблюдения",
     "карточка показывает «объект наблюдения», пример давал половину"),
    (7290, "example_tr",
     "Zamanın varsa sinemaya gidebiliriz",
     "Zamanın olması şartıyla sinemaya gidebiliriz",
     "слова ряда в примере не было: vorausgesetzt это «şartıyla»"),
    (1570, "example_uk",
     "Заняття відбуваються кожного понеділка",
     "Заняття відбуваються щоразу в понеділок",
     "слова ряда в примере не было: jeweils это «щоразу»"),

    # ══ формы и управление ══════════════════════════════════════
    (10603, "example_uk",
     "Ніхто не може тобі цього докорити",
     "Ніхто не може тобі цього закинути",
     "«докоряти» не берёт винительного; «закидати» есть в списке"),
    (14055, "example_uk",
     "Я сповіщу тебе, як тільки прийду",
     "Я сповіщу тебе, як тільки приїду",
     "«ankommen» это прибыть, а «прийду» — прийти пешком"),
    (1378, "example_uk",
     "Я залучаюся до захисту довкілля",
     "Я активно долучаюся до захисту довкілля",
     "«залучаюся» страдательное; в списке «активно долучатися»"),
    (8921, "example_uk",
     "Чиновник у ратуші був дуже корисним",
     "Чиновник у ратуші дуже мені допоміг",
     "«корисний» о человеке не говорят; в ru «очень мне помог»"),
    (10613, "example_tr",
     "Olguları çarpıttı ve şimdi herkes kafası karışık",
     "Olguları çarpıttı ve şimdi herkesin kafası karışık",
     "нужен родительный: «herkesin kafası»"),
    (10614, "example_tr",
     "Savaş insanlara çok felaket getiriyor",
     "Savaş insanlara büyük felaketler getiriyor",
     "«çok felaket» не согласовано"),
    (2046, "example_tr",
     "Ajans dairelere aracılık ediyor",
     "Ajans daire bulmada aracılık ediyor",
     "«dairelere aracılık» не то управление"),
    (18749, "example_tr",
     "Bu geçici olarak en iyi çözüm, ama daha sonra geliştirilebilir",
     "Bu geçici olarak en iyi çözüm, ama daha sonra geliştirebiliriz",
     "пассив вместо «wir können sie verbessern»"),
    (18749, "translation_tr",
     "şimdilik, geçici olarak, ön olarak",
     "şimdilik, geçici olarak, geçici süreyle",
     "«ön olarak» не турецкий оборот"),

    # ══ время глагола ═══════════════════════════════════════════
    (10598, "example_pl",
     "Dziecko szlochało po upadku",
     "Dziecko szlocha po upadku",
     "прошедшее против «schluchzt»; в остальных четырёх настоящее"),

    # ══ потерянное слово ════════════════════════════════════════
    (11748, "example_ru",
     "Бабушка каждый год печёт вкусное печенье на Рождество",
     "Моя бабушка каждый год печёт вкусное печенье на Рождество",
     "потеряно «Meine»: в остальных четырёх оно есть"),
    (10599, "example_pl",
     "Robi się sentymentalna przy starych zdjęciach",
     "Zawsze robi się sentymentalna, kiedy patrzy na stare zdjęcia",
     "потеряно «immer» и подчинённая фраза"),
    (10600, "example_pl",
     "Razem to jakoś przetrwamy",
     "Jestem pewien, że razem to przetrwamy",
     "потеряно «Ich bin sicher, dass»"),
    (12667, "example_pl",
     "Lekarz podał mi surowicę",
     "Lekarz podał mi zastrzyk z surowicy",
     "потеряна «Injektion»"),

    # ══ добавленное слово ═══════════════════════════════════════
    (10621, "example_pl",
     "Był bardzo wzruszony tą muzyką",
     "Był wzruszony tą muzyką",
     "«bardzo» в эталоне «Er war ergriffen» нет"),
    (10577, "example_pl",
     "Byłem bardzo wzruszony tą historią",
     "Byłem wzruszony tą historią",
     "то же, ряд-близнец"),
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
