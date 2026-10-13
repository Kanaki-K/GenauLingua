"""ВТОРОЙ ПРОХОД, блок 13 (ряды 2401–2600): правки глазами и ОШИБКА В
МОЕЙ ЖЕ ПРИМЕТЕ.

`geradeaus` (329): эталон «Geh bitte geradeaus» — на «ты», а украинский
написал «**йдіть**», турецкий «**gidin**» — оба вежливые. Класс
«обращение в повелительном» был сметён в блоке 8, примета
`scan_imperative_formality` показывала ноль, и ряд всё равно нашёлся
глазами.

ПРИЧИНА — ПОРОГ ДЛИНЫ СЛОВА в самой примете. Было:

    UK_FORMAL       = \\b\\w{4,}(?:йте|іть|ьте|ете|мте)\\b
    TR_FORMAL_MAYBE = \\b\\w{4,}[ıiuü]n\\b

То есть четыре буквы ПЕРЕД окончанием. «йдіть» — пять букв всего,
«gidin» — тоже пять. Короткие формы, то есть самые частые
повелительные, проваливались все. Порог снижен до двух букв.

После правки примета дала по базе:

    украинский: 2 (geradeaus — настоящий, durchgehen — «Давайте», ложное)
    турецкий:  42 в мягком списке, из них НАСТОЯЩИХ ЧЕТЫРЕ

        geradeaus (329)     «Lütfen dümdüz gidin»       → git
        Bankschalter (1216) «Banka gişesine gidin»      → git
        beachten (1224)     «Lütfen uyarıları ... alın» → al
        umgehend (2912)     «Lütfen derhal cevap verin» → ver

И ДВА ИЗ ЧЕТЫРЁХ — `beachten` и `umgehend` — я уже «починил» в блоке 8,
но только с УКРАИНСКОЙ стороны: турецкая тогда не попала в улов из-за
того же порога. Это второй раз за два блока, когда класс был объявлен
сметённым, а сметён в одном языке (первый — польский род в блоке 12).

Остальные 38 турецких попаданий ложные, и ложные они по языку, а не по
порогу: на «-ın»/«-in» в турецком кончаются и второе лицо
ЕДИНСТВЕННОГО у возвратных глаголов («tutun» от tutunmak, «kaçın» от
kaçınmak, «düşün» от düşünmek), и прилагательные («yakın», «derin»),
и притяжательные («e-postanın»). Поэтому примета остаётся мягким
списком: снижение порога подняло улов с 21 до 42, но доля ложных
выросла ровно так же.

Из найденного глазами отдельно:

    kotzen (12546)  de «Das macht mich echt kotzen»
        По-немецки так не говорят: «machen + инфинитив» в этом смысле
        это калька с английского «makes me puke». Правильно «Davon muss
        ich kotzen» или «Das ist zum Kotzen». Все пять переводов
        передают именно это.

    stammen (6821)  ru «из 18 века», uk «з 18 століття»
        Век цифрой. Класс закрыт в первом проходе
        (`fix_roman_centuries`: XIX → девятнадцатом), но там были
        РИМСКИЕ цифры, а арабские остались. Синтезатор читает «18 века»
        как «восемнадцать века». Польский в этом ряду уже написан
        словом.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ── КЛАСС: обращение в повелительном, после правки порога ────
    (329, "example_uk",
     "Будь ласка, йдіть прямо",
     "Будь ласка, йди прямо",
     "эталон «Geh bitte» на «ты»; примета пропускала короткое «йдіть»"),
    (329, "example_tr",
     "Lütfen dümdüz gidin",
     "Lütfen dümdüz git",
     "то же: «gidin» вежливое, единственное — «git»"),
    (1216, "example_tr",
     "Banka gişesine gidin",
     "Banka gişesine git",
     "эталон «Geh zum Bankschalter» на «ты»"),
    (1224, "example_tr",
     "Lütfen uyarıları dikkate alın",
     "Lütfen uyarıları dikkate al",
     "недоделка блока 8: украинский поправил, турецкий не попал в улов"),
    (2912, "example_tr",
     "Lütfen derhal cevap verin",
     "Lütfen derhal cevap ver",
     "то же"),

    # ── эталон: не немецкая конструкция ─────────────────────────
    (12546, "example_de",
     "Das macht mich echt kotzen",
     "Davon muss ich echt kotzen",
     "«machen + инфинитив» в этом смысле калька с английского"),

    # ── век цифрой ──────────────────────────────────────────────
    (6821, "example_ru",
     "Эти старые монеты происходят из 18 века",
     "Эти старые монеты происходят из восемнадцатого века",
     "синтезатор читает «18 века» как «восемнадцать века»; польский уже словом"),
    (6821, "example_uk",
     "Ці старі монети походять з 18 століття",
     "Ці старі монети походять з вісімнадцятого століття",
     "то же"),

    # ── обращение: безличный инфинитив вместо «ты» ──────────────
    (2066, "example_pl",
     "Proszę wypełnić formularz w całości",
     "Wypełnij proszę formularz w całości",
     "эталон «Bitte füll ... aus» на «ты»; в ru, uk, tr и en так и написано"),

    # ── слово не из своего списка ───────────────────────────────
    (17779, "example_tr",
     "Çiftçi her gün hayvanlarıyla ilgileniyor",
     "Çiftçi her gün çiftlik hayvanlarıyla ilgileniyor",
     "карточка показывала «davar» (мелкий скот), пример говорил просто «животные»"),
    (15451, "example_tr",
     "Balık oltaya gelmiyor",
     "Balık yeme gelmiyor",
     "«olta» это удочка, а Köder — приманка"),
    (18683, "example_pl",
     "W tym czasie już zacznę gotować",
     "Tymczasem już zacznę gotować",
     "«w tym czasie» нет в списке переводов, а «tymczasem» есть"),

    # ── порядок и состав списка переводов ───────────────────────
    (10322, "translation_ru",
     "психованный, чудак, дурак, прядильщик",
     "псих, чудак, дурак, прядильщик",
     "пример говорит «псих», и в украинском «псих» стоит первым"),
    (2683, "translation_tr",
     "yan olarak, ayrıca, bu arada",
     "yan olarak, ek olarak, ayrıca, bu arada",
     "пример говорит «ek olarak» — слова не было в списке"),
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
