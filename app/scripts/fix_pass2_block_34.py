"""ВТОРОЙ ПРОХОД, блок 34 (ряды 6601–6800): 24 правки.

ГЛАВНОЕ В БЛОКЕ — НЕ ПРАВКИ, А ЗАМЕР. В блоке попались сразу две пары
рядов на один заголовок: `anstrengen` (7383 B2 и 7668 C1) и `eisern`
(7482 B2 и 7678 C1). Это уже седьмая и восьмая за семь блоков, и такая
частота заставила проверить класс прямо.

**375 заголовков встречаются в базе больше одного раза.** Класс, который
я собирал по одной паре за блок, оказался на два порядка больше — и это
теперь примета `scan_same_headword.py` с разобранным уловом:

    8 пар  — полный дубль (совпадает и немецкий пример). Это ровно тот
             список из блока 24; правило воспроизводится в точности.
    35 пар — разные части речи. Законно.
    23 пары — списки переводов не пересекаются: разные значения.
    339 пар — та же часть речи И списки пересекаются: учат ОДНОМУ.
    175 из них — пересечение почти полное.

Как это выглядит: `Sohn` (847 A1 «Der Sohn ist groß» / 14973 A2 «Er hat
zwei Söhne»), `Student`, `Patient`, `Firma`. У `Junge` одна фраза дана в
единственном (1573, A2) и множественном (14891, A1) числе — и
множественное отнесено к уровню НИЖЕ.

Похоже, база собиралась слоями: ядро A1/A2 и позднее расширение по
частотности, и слои наложились. Ряды НЕ ТРОНУТЫ — удаление меняет размер
базы и связи `user_words`, это решение владельца. Подробности и список в
самой примете.

ЕДИНСТВЕННАЯ ПОДМЕНА ЦЕЛИКОМ, И ОНА В АНГЛИЙСКОМ:

    unser (13562)  de «Das ist unsere Entscheidung, nicht deine»
                   en «That little house is ours now»

Прочие четыре языка верны. Английский подменяет редко — за весь проход
это восьмой случай против девятнадцати польских.

ПОДМЕНА, УШЕДШАЯ ПАРОЙ ru+uk:

    Faktor (17986)  de «Das ist ein wichtiger Faktor bei der Entscheidung»
        ru «ОПЫТ — важный фактор при ВЫБОРЕ РАБОТЫ»
        uk «ДОСВІД — важливий фактор при ВИБОРІ РОБОТИ»

en, tr и pl верны. Пара ru+uk встречается реже тройки en+uk+tr, но это
уже не первый раз.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ КЛАСС: подменённое предложение ══════════════════════════
    (13562, "example_en",
     "That little house is ours now",
     "That is our decision, not yours",
     "подмена: эталон «Das ist unsere Entscheidung, nicht deine»"),
    (17986, "example_ru",
     "Опыт — важный фактор при выборе работы",
     "Это важный фактор при принятии решения",
     "подмена: эталон «ein wichtiger Faktor bei der Entscheidung»"),
    (17986, "example_uk",
     "Досвід — важливий фактор при виборі роботи",
     "Це важливий фактор при ухваленні рішення",
     "то же; en, tr и pl верны"),
    (14147, "example_pl",
     "Zostawił list pożegnalny na stole",
     "Napisał list pożegnalny, zanim odszedł",
     "подмена: оставил на столе вместо «geschrieben, bevor er gegangen ist»"),
    (7668, "example_tr",
     "Gerçekten zorlayan bir hafta geçirdim",
     "Zorlanmış görünüyordu",
     "подмена: «у меня была тяжёлая неделя» вместо «Er sah angestrengt aus»"),

    # ══ слово не из своего списка и не то слово ═════════════════
    (10932, "example_tr",
     "Kaza hakkında duyunca çok endişeli oldu",
     "Kazayı duyunca şoke oldu",
     "«endişeli» это встревоженный; `bestürzt` — «şoke olmuş», и оно первое"),
    (10936, "example_tr",
     "Sosyal durumlarda gergin ve emin olmayan görünüyor",
     "Sosyal durumlarda gergin ve özgüvensiz görünüyor",
     "«emin olmayan» не оборот; неуверенный в себе — «özgüvensiz»"),
    (14612, "example_tr",
     "Bu, tam bir fars davasıydı",
     "Bu dava tam bir farstı",
     "«fars davası» не оборот: фарсом был процесс, а не наоборот"),
    (16444, "translation_pl",
     "rabuś bankowy, napastnik",
     "rabuś bankowy, bandyta",
     "«napastnik» это нападающий в футболе, а не грабитель"),
    (10922, "example_pl",
     "Jakiś fanatyk zniszczył pomnik",
     "Jakiś fanatyk uszkodził pomnik",
     "«zniszczyć» это уничтожить; `beschädigen` — повредить"),
    (14148, "example_uk",
     "Я повинен помітити, що це неправильно",
     "Я повинен зауважити, що це неправильно",
     "«помітити» это заметить глазами; в списке «зауважити» первым"),
    (7667, "example_uk",
     "Я засновую приз для конкурсу",
     "Я жертвую приз для конкурсу",
     "приз не «засновують»; в списке «пожертвувати» первым"),
    (17613, "example_ru",
     "Смайлик в конце твоего сообщения классный",
     "Смайлик в конце твоего сообщения милый",
     "`niedlich` это милый; в uk, en, tr и pl милый"),

    # ══ калька с немецкого ══════════════════════════════════════
    (14610, "example_ru",
     "Я довольно охотно играю на виолончели",
     "Мне нравится играть на виолончели",
     "«довольно охотно» калька с «ganz gerne»"),
    (14610, "example_uk",
     "Я досить охоче граю на віолончелі",
     "Мені подобається грати на віолончелі",
     "то же"),
    (16457, "example_ru",
     "Исторически людей сжигали на костре",
     "В прошлом людей сжигали на костре",
     "«исторически» калька с «historisch» в начале фразы"),
    (16457, "example_uk",
     "Історично людей спалювали на вогнищах",
     "У минулому людей спалювали на вогнищі",
     "то же, и множественное против «auf dem Scheiterhaufen»"),
    (13713, "example_uk",
     "Вона одягається елегантно на галу",
     "Вона елегантно одягається на гала-вечір",
     "«на галу» не форма: «на гала-вечір»"),

    # ══ потерянное и добавленное слово ══════════════════════════
    (15641, "example_uk",
     "У мене вдома росте пальма на балконі",
     "У мене на балконі росте пальма",
     "«вдома» в эталоне нет"),
    (18806, "example_tr",
     "Bir çeyrek saat daha bekle, o zaman hazır olurum",
     "Çeyrek saat daha bekle, o zaman hazır olurum",
     "«bir» перед «çeyrek» лишний"),
    (16446, "example_pl",
     "Trybunał wydał wyrok w tej sprawie",
     "Trybunał wydał wyrok",
     "«w tej sprawie» в эталоне нет"),
    (9026, "example_ru",
     "В день зарплаты я трачу весь свой оклад",
     "В день зарплаты я трачу свой оклад",
     "«весь» в эталоне «gebe ich mein Gehalt aus» нет"),
    (9026, "example_pl",
     "W dzień wypłaty wydaję całą pensję",
     "W dzień wypłaty wydaję pensję",
     "то же"),
    (11832, "example_pl",
     "W niedzielę idziemy na brunch",
     "W niedzielę chętnie idziemy na brunch",
     "потеряно «gerne»: в остальных четырёх оно есть"),
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
