"""Сквозная правка по примете `scan_terminal_punct`.

Класс нашёлся в блоке 5 второго прохода: пять рядов подряд, где
восклицательный знак стоит в одних языках и отсутствует в других.
Примета по всей базе дала 47 рядов по «!» и 2 по «?».

Почему это дефект, а не придирка. Знак — часть того, ЧТО УСЛЫШИТ
ученик: синтезатор читает восклицание иначе, чем ровную фразу. Ряд,
где немецкий эталон спокоен, а русский кричит, учит разной интонации
одной фразы.

ПОЧЕМУ ЭТО НЕЛЬЗЯ ПРАВИТЬ МЕХАНИЧЕСКИ. Первая версия скрипта сводила
всё к правилу «тип фразы задаёт эталон» и получила 100 правок. Среди
них были такие:

    Guten Appetit        ru «Приятного аппетита!» → убрать «!»
    Herzlich willkommen  uk «Сердечно вітаємо вас!» → убрать «!»

То есть правило снимало ВЕРНЫЙ знак, потому что знака не хватало в
самом эталоне: пожелание и приветствие по немецкой орфографии пишутся
с «!» («Guten Appetit!», «Herzlich willkommen!»). Ровно та же ошибка,
что в блоке 3 с усечённым повелительным: вывести правило и применить,
не посмотрев, на какой стороне дефект.

Поэтому направления разделены:

  • эталон С «!», перевод без — правка МЕХАНИЧЕСКАЯ. Тут немецкий
    авторитетен: восклицание есть, перевод его потерял;

  • эталон БЕЗ «!», перевод с ним — каждый ряд РУКАМИ, потому что
    надо решить, кто прав. Таких рядов 21, и они разошлись почти
    пополам: в 10 знак дописан В ЭТАЛОН и во все языки (пожелания,
    приветствия, восклицательное «Was für ein …», междометия боли и
    отвращения — у них «!» не стиль, а орфография), в 11 знак снят с
    перевода (эталон там — спокойное утверждение или обычное
    повелительное, а база пишет повелительные без «!»).

Попутно примета на знак нашла три ПОДМЕНЁННЫХ предложения — то, чего
она не искала:

    tauchen (12156)       en «Let's dive into the pool!»
        эталон «Wir gehen morgen tauchen», остальные четыре языка
        переводят его
    vorbeikommen (2070)   uk «Заходь до нас на чай!»
        эталон «Ich komme morgen vorbei» — это «я зайду», а не
        «приходи к нам»
    runterlassen (7971)   pl «Opuść rolety, jest za jasno»
        эталон спрашивает, польский приказывал

И два ряда по «?» — один класс: эталон состоит из вопроса и отдельного
утверждения, а переводы склеили их запятой и вопрос потеряли.

Ряд `Prost` в улов НЕ попал, и это проверка самой приметы: там «!»
стоит после первого слова («Prost! Auf deine Gesundheit»), и примета
ищет знак во всей фразе, а не только в конце.

    python -m app.scripts.fix_terminal_punct [--apply]
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings
from app.scripts.scan_terminal_punct import LANGS, mark

# ─────────────────────────────────────────────────────────────────────
# ЗНАК ДОПИСАН В ЭТАЛОН: пожелания, приветствия, восклицательное
# «Was für ein …», междометия. У них «!» — орфография, а не стиль.
# ─────────────────────────────────────────────────────────────────────
TO_ETALON: list[tuple[int, str, str, str, str]] = [
    (1153, "example_de", "Guten Appetit", "Guten Appetit!",
     "пожелание: по немецкой орфографии с «!»; ru, uk и pl были правы"),
    (1153, "example_en", "Enjoy your meal", "Enjoy your meal!", "то же"),
    (1153, "example_tr", "Afiyet olsun", "Afiyet olsun!", "то же"),

    (1534, "example_de", "Herzlich willkommen", "Herzlich willkommen!",
     "приветствие: по немецкой орфографии с «!»"),
    (1534, "example_en", "Warm welcome", "A warm welcome!",
     "и «Warm welcome» — не приветствие, а именная группа"),
    (1534, "example_tr", "Hoş geldiniz", "Hoş geldiniz!", "то же"),
    (1534, "example_pl", "Serdecznie witamy", "Serdecznie witamy!", "то же"),

    (6464, "example_de", "Was für ein Zufall", "Was für ein Zufall!",
     "восклицательный тип фразы «Was für ein …!»"),
    (6464, "example_en", "What a coincidence", "What a coincidence!", "то же"),
    (6464, "example_ru", "Какая случайность", "Какая случайность!", "то же"),
    (6464, "example_uk", "Яка випадковість", "Яка випадковість!", "то же"),
    (6464, "example_tr", "Ne tesadüf", "Ne tesadüf!", "то же"),

    (10110, "example_de", "Herzlichen Glückwunsch zum Geburtstag",
     "Herzlichen Glückwunsch zum Geburtstag!",
     "пожелание: по немецкой орфографии с «!»"),
    (10110, "example_en", "Happy birthday!", "Congratulations on your birthday!",
     "и «Happy birthday» теряло слово ряда: карточка показывала congratulations"),
    (10110, "example_uk", "Вітаю з днем народження", "Вітаю з днем народження!", "то же"),
    (10110, "example_tr", "Doğum günün kutlu olsun", "Doğum günün kutlu olsun!", "то же"),
    (10110, "example_pl", "Najlepsze życzenia z okazji urodzin",
     "Najlepsze życzenia z okazji urodzin!", "то же"),

    (361, "example_de", "Guck mal, wie schön der Himmel ist",
     "Guck mal, wie schön der Himmel ist!",
     "восклицательный тип фразы «wie schön …!»"),
    (361, "example_en", "Look how beautiful the sky is",
     "Look how beautiful the sky is!", "то же"),
    (361, "example_tr", "Bak, gökyüzü ne kadar güzel",
     "Bak, gökyüzü ne kadar güzel!", "то же"),
    (361, "example_pl", "Popatrz, jakie piękne jest niebo",
     "Popatrz, jakie piękne jest niebo!", "то же"),

    (6432, "example_de", "Das ist ja Wahnsinn", "Das ist ja Wahnsinn!",
     "частица «ja» делает фразу восклицательной"),
    (6432, "example_en", "That's madness", "That's madness!", "то же"),
    (6432, "example_uk", "Це ж божевілля", "Це ж божевілля!", "то же"),
    (6432, "example_tr", "Bu delilik", "Bu delilik!", "то же"),

    (10667, "example_de", "Das ist ja eine Sauerei hier",
     "Das ist ja eine Sauerei hier!", "частица «ja» делает фразу восклицательной"),
    (10667, "example_en", "What a mess this is", "What a mess this is!", "то же"),
    (10667, "example_tr", "Burası tam bir pislik", "Burası tam bir pislik!", "то же"),

    (13875, "example_de", "Au, das tut weh", "Au, das tut weh!",
     "междометие боли: по орфографии с «!»"),
    (13875, "example_uk", "Ай, боляче", "Ой, боляче!",
     "и «ай» не совпадало с первым переводом «ой»"),
    (13875, "example_tr", "Ah, acıyor", "Ah, acıyor!", "то же"),
    (13875, "example_pl", "Au, to boli", "Au, to boli!", "то же"),

    (14066, "example_de", "Pfui, das ist ja ekelhaft", "Pfui, das ist ja ekelhaft!",
     "междометие отвращения плюс частица «ja»"),
    (14066, "example_en", "Ugh, that's disgusting", "Ugh, that's disgusting!", "то же"),
    (14066, "example_ru", "Фу, это же отвратительно", "Фу, это же отвратительно!", "то же"),
    (14066, "example_uk", "Фу, це ж огидно", "Фу, це ж огидно!", "то же"),
    (14066, "example_pl", "Fuj, ale to obrzydliwe", "Fuj, ale to obrzydliwe!", "то же"),
    (14066, "example_tr", "İyy, şuna bak, ne iğrenç!", "İyy, bu çok iğrenç!",
     "«şuna bak» в эталоне нет"),

    (15537, "example_de", "Donnerwetter, das war knapp", "Donnerwetter, das war knapp!",
     "междометие плюс восклицание"),
    (15537, "example_ru", "Чёрт побери, это было на волосок",
     "Чёрт побери, это было впритык!",
     "«на волосок» по-русски требует продолжения «от чего»"),
    (15537, "example_uk", "Чорт забирай, це було на волосинку",
     "Чорт забирай, це було на межі!", "то же по-украински"),
    (15537, "example_tr", "Vay be, bu çok yakındı", "Vay be, bu çok yakındı!", "то же"),
    (15537, "example_pl", "Do licha, to było blisko", "Do licha, to było blisko!", "то же"),
]

# ─────────────────────────────────────────────────────────────────────
# ЗНАК СНЯТ С ПЕРЕВОДА: эталон — спокойное утверждение или обычное
# повелительное, а повелительные база пишет без «!».
# ─────────────────────────────────────────────────────────────────────
FROM_TRANSLATION: list[tuple[int, str, str, str, str]] = [
    (1770, "example_ru", "Это отлично!", "Это отлично",
     "эталон «Das ist prima» — спокойное утверждение"),
    (1824, "example_pl", "Popatrz tylko!", "Popatrz tylko",
     "эталон «Schau mal» без восклицания"),
    (6585, "example_ru", "Быстро прячься!", "Быстро прячься",
     "эталон «Versteck dich schnell» без восклицания"),
    (6585, "example_uk", "Швидко ховайся!", "Швидко ховайся", "то же"),
    (6695, "example_uk", "Хапай м'яч!", "Хапай м'яч",
     "эталон «Schnapp dir den Ball» без восклицания"),
    (6695, "example_tr", "Topu kap!", "Topu kap", "то же"),
    (7399, "example_uk", "Ну ти й заварив кашу своєю ідеєю!",
     "Ну ти й заварив кашу своєю ідеєю", "эталон без восклицания"),
    (7665, "example_pl", "Niech panuje sprawiedliwość!", "Niech panuje sprawiedliwość",
     "эталон «Lasse die Gerechtigkeit walten» без восклицания"),
    (7760, "example_ru", "Осторожно, ты это сломаешь!", "Осторожно, ты это сломаешь",
     "эталон «Pass auf, du wirst es kaputtmachen» без восклицания"),
    (7760, "example_uk", "Обережно, ти це зламаєш!", "Обережно, ти це зламаєш", "то же"),
    (12506, "example_pl", "Zamknij mordę!", "Zamknij mordę",
     "эталон «Halt die Fresse» без восклицания"),
    (15385, "example_pl", "Stul pysk!", "Stul pysk",
     "эталон «Halt dein Maul» без восклицания"),
]

# ─────────────────────────────────────────────────────────────────────
# НЕ ЗНАК, А ФРАЗА. Нашлось попутно.
# ─────────────────────────────────────────────────────────────────────
WRONG_SENTENCE: list[tuple[int, str, str, str, str]] = [
    (12156, "example_en", "Let's dive into the pool!", "We're going diving tomorrow",
     "подменённое предложение: эталон «Wir gehen morgen tauchen»"),
    (2070, "example_uk", "Заходь до нас на чай!", "Я зайду завтра",
     "подменённое предложение: эталон «Ich komme morgen vorbei» — это «я зайду»"),
    (11806, "example_uk", "Гей, твоя серветка падає!", "Обережно, твоя серветка падає",
     "«Гей» вместо «Pass auf», и восклицания в эталоне нет"),

    (7971, "example_pl", "Opuść rolety, jest za jasno",
     "Możesz opuścić rolety? Jest za jasno",
     "эталон спрашивает, польский приказывал: сменилось наклонение"),
    (7971, "example_en", "Can you lower the blinds, it's too bright",
     "Can you lower the blinds? It's too bright",
     "эталон из вопроса и утверждения, перевод склеил их запятой"),
    (7971, "example_uk", "Можеш опустити жалюзі, занадто світло",
     "Можеш опустити жалюзі? Занадто світло", "то же"),
    (7596, "example_en", "Can you cut the steak for me, it's too thick",
     "Can you cut the steak for me? It's too thick", "то же"),
    (7596, "example_ru", "Ты можешь разрезать мне стейк, он слишком толстый",
     "Ты можешь разрезать мне стейк? Он слишком толстый", "то же"),
    (7596, "example_uk", "Ти можеш розрізати мені стейк, він надто товстий",
     "Ти можеш розрізати мені стейк? Він надто товстий", "то же"),
    (7596, "example_tr", "Bana bifteği kesebilir misin, çok kalın",
     "Bana bifteği kesebilir misin? Çok kalın", "то же"),
    (7596, "example_pl", "Możesz mi przeciąć ten stek, jest za gruby",
     "Możesz mi przeciąć ten stek? Jest za gruby", "то же"),
]

BY_HAND = TO_ETALON + FROM_TRANSLATION + WRONG_SENTENCE
HAND_KEYS = {(wid, col) for wid, col, _, _, _ in BY_HAND}


def planned_auto(conn) -> list[tuple[int, str, str, str, str]]:
    """Механическая половина: в эталоне «!» есть, в переводе нет.

    Только это направление безопасно автоматически — немецкий здесь
    авторитетен. Обратное направление целиком в BY_HAND.
    """
    cols = ", ".join(f"example_{lg}" for lg in LANGS)
    rows = conn.execute(
        text(
            f"SELECT id, example_de, {cols} FROM words "
            "WHERE example_de IS NOT NULL ORDER BY id"
        )
    ).mappings().all()

    out: list[tuple[int, str, str, str, str]] = []
    for r in rows:
        if "!" not in (r["example_de"] or ""):
            continue
        for lg in LANGS:
            col = f"example_{lg}"
            cur = r[col]
            if cur is None or "!" in cur or (r["id"], col) in HAND_KEYS:
                continue
            out.append((r["id"], col, cur, cur.rstrip() + "!",
                        "в эталоне восклицание, в переводе его не было"))
    return out


def main() -> None:
    apply_mode = "--apply" in sys.argv
    engine = create_engine(settings.DATABASE_URL_SYNC)

    ok: list[tuple[int, str, str, str, str]] = []
    skipped: list[tuple[int, str, str | None]] = []
    with engine.connect() as conn:
        for wid, col, was, now, why in BY_HAND:
            cur = conn.execute(
                text(f"SELECT {col} FROM words WHERE id = :i"), {"i": wid}
            ).scalar()
            if (cur or "").strip() != was:
                skipped.append((wid, col, cur))
            else:
                ok.append((wid, col, was, now, why))
        auto = planned_auto(conn)
    ok.extend(auto)

    print(f"=== правок {len(ok)}: руками {len(BY_HAND) - len(skipped)}, "
          f"механически {len(auto)}; пропущено {len(skipped)} ===\n")
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
    print(f"применено: {len(ok)}")

    bad = 0
    with engine.connect() as conn:
        for wid, col, _, now, _ in ok:
            cur = conn.execute(
                text(f"SELECT {col} FROM words WHERE id = :i"), {"i": wid}
            ).scalar()
            if (cur or "").strip() != now.strip():
                bad += 1
                print(f"НЕ ЗАПИСАЛОСЬ id={wid} {col}: {cur!r}")
    print(f"самопроверка: не записалось {bad}")

    with engine.connect() as conn:
        cols = ", ".join(f"example_{lg}" for lg in LANGS)
        rows = conn.execute(
            text(f"SELECT id, example_de, {cols} FROM words WHERE example_de IS NOT NULL")
        ).mappings().all()
    left = sum(
        1 for r in rows
        for lg in LANGS
        if r[f"example_{lg}"] is not None
        and (mark(r[f"example_{lg}"]) == "!") != (mark(r["example_de"]) == "!")
    )
    print(f"самопроверка приметой: ячеек с расхождением по «!» осталось {left}")


if __name__ == "__main__":
    main()
