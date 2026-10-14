"""ВТОРОЙ ПРОХОД, блок 6 (ряды 1001–1200): правки, найденные глазами.

Самое важное:

    deutsch (1122/6467)  tr «ALMAN dilbilgisi öğreniyorum»
        «Alman» это немец, народ; язык — «Almanca». «Alman
        dilbilgisi» значит «грамматика немцев». Ряд как раз про то,
        чем ученик занят, и перевод в нём неверен.

    Fräulein (1053/14936)  uk «...називали ПАННОЮ»
        Орудний однини там, где нужен множественный: «молодих жінок
        називали ПАННАМИ». Ошибка числа, а не выбора слова.

    Mistkerl (1079/10142)  pl список переводов «drań, łajdak, skurwysyn»
        Регистр: «Mistkerl» это мерзавец, а «skurwysyn» — мат. Список
        переводов виден на карточке целиком, то есть база учит слову,
        которое грубее исходного на два порядка. Заменено на «podlec».

    wünschen (1007/1064)  ru «Я желаю тебе СЧАСТЬЯ»
        «Ich wünsche dir Glück» — это пожелание удачи, и так его
        поняли английский, украинский и турецкий. Немецкое «Glück»
        двусмысленно (счастье и удача), и русский выбрал дальнее.

Остальное обычное: потерянные и добавленные слова, время глагола,
выбор дальнего варианта, карточка против примера.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ── ошибки языка ─────────────────────────────────────────────
    (6467, "example_tr",
     "Alman dilbilgisi öğreniyorum",
     "Almanca dilbilgisi öğreniyorum",
     "«Alman» это немец, язык — «Almanca»"),
    (14936, "example_uk",
     "Раніше молодих жінок називали панною",
     "Раніше молодих жінок називали паннами",
     "орудний однини там, где нужен множественный"),
    (10156, "example_uk",
     "У мене є в цьому сумнів",
     "У мене є сумніви щодо цього",
     "порядок слов и число: в эталоне «Zweifel» во множественном"),

    # ── регистр перевода ─────────────────────────────────────────
    (10142, "translation_pl",
     "drań, łajdak, skurwysyn",
     "drań, łajdak, podlec",
     "«Mistkerl» это мерзавец, а «skurwysyn» мат: список виден на карточке целиком"),

    # ── выбор дальнего варианта ──────────────────────────────────
    (1064, "example_ru",
     "Я желаю тебе счастья",
     "Я желаю тебе удачи",
     "«Glück» здесь удача, как в en, uk и tr"),
    (15388, "example_pl",
     "Kot chce gonić ptaka",
     "Kot chce polować na ptaka",
     "«gonić» это гнаться, а четыре языка выбрали охоту"),
    (6438, "example_uk",
     "Насильство не вихід",
     "Насильство не рішення",
     "«вихід» нет в списке переводов, эталон говорит «keine Lösung»"),
    (14378, "example_uk",
     "Це була незручна сцена",
     "Це була ганебна сцена",
     "«незручна» это неудобная; peinlich — про стыд, как в en, tr и pl"),
    (15394, "example_uk",
     "Пташка співає на дереві",
     "Птах співає на дереві",
     "карточка показывала «птах», пример говорил «пташка»"),
    (18619, "example_uk",
     "Недавно він ще був тут",
     "Щойно він ще був тут",
     "«vorhin» это только что; «щойно» стоит первым в переводе"),
    (14937, "example_uk",
     "Мамо, де ти?",
     "Мамусю, де ти?",
     "ряд про уменьшительное «Mami», а пример давал обычное «мама»"),
    (14937, "example_tr",
     "Anne, neredesin?",
     "Anneciğim, neredesin?",
     "то же: «Mami» уменьшительное, и «anneciğim» есть в переводе"),
    (6427, "example_tr",
     "Bundan etkilenmiş durumdayım",
     "Bundan etkilendim",
     "«etkilenmiş durumdayım» по-турецки не говорят"),

    # ── потерянное слово ─────────────────────────────────────────
    (10133, "example_uk",
     "Ти можеш гарно посміхатися",
     "Ти можеш так гарно посміхатися",
     "потеряно «so»: в ru, tr и pl оно есть"),
    (10133, "example_en",
     "You can smile beautifully",
     "You can smile so beautifully",
     "то же"),
    (1546, "example_uk",
     "Я сподіваюся, що вийде",
     "Я сподіваюся, що все вийде",
     "потеряно «alles»: в ru, tr и pl оно есть"),
    (1546, "example_en",
     "I hope it works",
     "I hope everything works",
     "то же"),
    (10145, "example_uk",
     "Мені це здається знайомим",
     "Це відчуття здається мені знайомим",
     "потеряно «Gefühl»: в ru и pl оно есть"),
    (10145, "example_en",
     "That seems familiar to me",
     "That feeling seems familiar to me",
     "то же"),
    (10145, "example_tr",
     "Bu bana tanıdık geliyor",
     "Bu duygu bana tanıdık geliyor",
     "то же"),
    (2610, "example_uk",
     "Це було дуже розумно",
     "Це було дуже розумно з твого боку",
     "потеряно «von dir»: в ru и pl оно есть"),
    (2610, "example_en",
     "That was very clever",
     "That was very clever of you",
     "то же"),
    (10144, "example_uk",
     "Вони хочуть поцілуватися",
     "Ці двоє хочуть поцілуватися",
     "потеряно «die beiden»: в ru, tr и pl оно есть"),
    (274, "example_uk",
     "Я люблю рибу",
     "Я люблю їсти рибу",
     "потеряно «esse»: в ru, en, tr и pl оно есть"),
    (6452, "example_ru",
     "Мне нужно проверить почту",
     "Мне нужно проверить электронную почту",
     "«почта» по-русски и бумажная; в эталоне E-Mails"),
    (182, "example_tr",
     "Polis teşkilatında çalışıyor",
     "Polis hizmetinde çalışıyor",
     "потеряно «Dienst» — слово ряда"),
    (507, "example_tr",
     "Bu ne kadar?",
     "Bunun fiyatı ne kadar?",
     "потеряно «kostet» — слово ряда"),
    (710, "example_tr",
     "Bu on sterlin",
     "Bu on sterlin tutuyor",
     "потеряно «kostet»"),
    (6482, "example_uk",
     "Я сьогодні слабкий",
     "Я почуваюся сьогодні слабким",
     "потеряно «fühle mich»: в ru и pl оно есть"),

    # ── добавленное слово ────────────────────────────────────────
    (10139, "example_pl",
     "Mówię to całkiem poważnie",
     "Mówię to poważnie",
     "«całkiem» в эталоне нет: «Ich meine das ernsthaft»"),
    (6482, "example_tr",
     "Kendimi bugün çok güçsüz hissediyorum",
     "Kendimi bugün güçsüz hissediyorum",
     "«çok» в эталоне нет"),
    (52, "example_uk",
     "Я встаю о сьомій ранку",
     "Я встаю о сьомій",
     "«ранку» в эталоне нет: «um sieben»"),
    (2111, "example_ru",
     "У меня есть одно желание",
     "У меня есть желание",
     "«einen» здесь артикль, а не числительное"),

    # ── подменённое слово ────────────────────────────────────────
    (1694, "example_en",
     "Are you coming with me?",
     "Are you coming with us?",
     "в ru, uk и pl «с нами»; эталон «Kommst du mit» без лица"),
    (3039, "example_ru",
     "Момент выбран совсем неудачно",
     "Момент выбран действительно неудачно",
     "«echt» это действительно, как в en, tr и pl"),
    (3039, "example_uk",
     "Момент вибрано зовсім невдало",
     "Момент вибрано справді невдало",
     "то же"),

    # ── время глагола ────────────────────────────────────────────
    (15391, "example_pl",
     "Podaruję ci różę",
     "Daruję ci różę",
     "будущее против «Ich schenke»; в ru, uk, en и tr настоящее"),
    (15953, "example_pl",
     "Burmistrz przyjedzie dzisiaj",
     "Burmistrz przychodzi dzisiaj",
     "будущее против «kommt heute»; в остальных четырёх настоящее"),
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
