"""ВТОРОЙ ПРОХОД, блок 32 (ряды 6201–6400): 41 правка.

БЛОК ЗАМЕТНО ЧИЩЕ ПРЕДЫДУЩИХ, и это стоит записать: подмен четыре
против пяти-семи в блоках 27–31, а немецкий эталон ни в одном ряду не
подвёл. Состав блока — существительные ранга 11900–12230, почти все
конкретные и однозначные (`Zange`, `Eiche`, `Aquarium`, `Karussell`), и
это та же зависимость плотности от состава, что отмечена в HANDOVER про
блок 9.

ШЕСТАЯ ПАРА РЯДОВ НА ОДИН ЗАГОЛОВОК, И ВПЕРВЫЕ ЕЁ МОЖНО СНЯТЬ ОДНОЙ
ПРАВКОЙ ЗАГОЛОВКА:

    Vegetarier (2021)   A2, de «Ich bin VegetarierIN»
    Vegetarier (11812)  C1, de «Mein Bruder ist Vegetarier und isst
                            kein Fleisch»

У первого ряда немецкий пример стоит в ЖЕНСКОЙ форме, а заголовок — в
мужской. То есть в одном ряду сошлись сразу два класса: «форма слова
вместо заголовка» и «два ряда на один заголовок».

Правка заголовка 2021 на `Vegetarierin` снимает оба разом: ряд
становится женским по всей строке (а русское «вегетарианка» там уже
стоит и, по решению блока 11, стоит ВЕРНО), и дубль распадается сам.
Это решение владельца — заголовок трогать нельзя, — но впервые в этом
классе видно, КАКАЯ именно правка нужна. Записано в HANDOVER.

ЧЕТЫРЕ ПОДМЕНЫ:

    Lebensgefahr   (12760) pl «RANNY był w stanie zagrożenia życia»
    Stellungnahme  (14138) pl «FIRMA wydała oficjalne oświadczenie»
    Möpse          (15625) tr «KOMŞUNUN MOPSU çok sevimli»
    meilenweit      (7585) pl «DYM było widać na kilometry»

В `meilenweit` подменено одно слово: дым вместо огня. Такие правки
`scan_length_outlier` не видит по устройству — длина та же, — и это
третий случай за проход после `zweieinhalb` (блок 28) и `Zicke`.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ КЛАСС: подменённое предложение ══════════════════════════
    (12760, "example_pl",
     "Ranny był w stanie zagrożenia życia",
     "Pacjent był w zagrożeniu życia i musiał być natychmiast operowany",
     "подмена: раненый вместо пациента, и потеряна вторая половина"),
    (14138, "example_pl",
     "Firma wydała oficjalne oświadczenie w tej sprawie",
     "Rząd wydał oficjalne oświadczenie",
     "подмена: фирма вместо правительства"),
    (15625, "example_tr",
     "Komşunun mopsu çok sevimli",
     "Parktaki mopslar sevimli ve oyuncu",
     "подмена: мопс соседа вместо мопсов в парке"),
    (7585, "example_pl",
     "Dym było widać na kilometry",
     "Ogień było widać na kilometry",
     "подменено слово: дым вместо огня"),

    # ══ формы, которых в языке нет ══════════════════════════════
    (16393, "example_uk",
     "Тільки вповноважені особи можуть входити сюди",
     "Тільки уповноважені особи можуть входити сюди",
     "«вповноважені» не форма: нужно «уповноважені»"),
    (16392, "example_uk",
     "Вони шукають політичний притулок",
     "Вони шукають політичного притулку",
     "«шукати» требует родительного"),
    (7604, "example_tr",
     "Çocuklar yerde birlikte çömeleyip oynuyorlar",
     "Çocuklar yerde çömelip oynuyorlar",
     "«çömeleyip» не форма: «çömelip»; и «birlikte» в эталоне нет"),
    (16399, "example_tr",
     "Asalet, geçmişte toplumda çok büyük gücü vardı",
     "Soylu sınıfın geçmişte toplumda çok büyük gücü vardı",
     "фраза не согласована: нужен родительный при «gücü vardı»"),
    (16401, "example_tr",
     "Kimlik tayin etmek için pasaport ya da kimlik kartı gerekir",
     "Kimlik tespiti için pasaport ya da kimlik kartı gerekir",
     "«kimlik tayin etmek» не оборот; в списке «kimlik tespiti»"),
    (11812, "example_tr",
     "Kardeşim vejeteryen ve et yemiyor",
     "Kardeşim vejetaryen ve et yemiyor",
     "«vejeteryen» описка: в списке «vejetaryen»"),
    (143, "example_tr",
     "Bunu nasıl hecelemek gerekiyor?",
     "Bu nasıl hecelenir?",
     "«nasıl hecelemek gerekiyor» не живой оборот"),

    # ══ существительное подменено глаголом ══════════════════════
    (1975, "example_uk",
     "Мене нудить",
     "У мене нудота",
     "ряд о существительном, а пример давал безличный глагол"),
    (1975, "example_tr",
     "Midem bulanıyor",
     "Mide bulantım var",
     "то же"),

    # ══ слово не из своего списка и не то слово ═════════════════
    (12767, "example_tr",
     "Kaza sonrası harap görünüyordu",
     "Kaza sonrası yıpranmış görünüyordu",
     "«harap» о строениях; о человеке — «yıpranmış», и оно первое"),
    (12251, "example_tr",
     "Büyük konserden önce yapılan ön gösteri çok etkileyiciydi",
     "Büyük konserden önce çalınan prelüd çok etkileyiciydi",
     "«ön gösteri» нет в списке, а «prelüd» стоит первым"),
    (9001, "example_tr",
     "Şirket yeni işçiler alıyor",
     "Şirket yeni işçiler işe alıyor",
     "в списке «işe almak», а пример давал половину"),
    (8998, "example_tr",
     "Katibi önemli belgeler hazırladı",
     "Kâtip önemli belgeyi hazırladı",
     "«katibi» не та форма, и множественное против «das Dokument»"),
    (10849, "example_uk",
     "Це була гарна робота з твого боку",
     "Це була непогана робота з твого боку",
     "«гарний» нет в списке; `brav` здесь «непоганий», и в ru так же"),
    (8996, "example_uk",
     "Пекар кожного ранку готує свіжий хліб",
     "Пекар кожного ранку пече свіжий хліб",
     "хлеб не «готують», а печуть; в ru, tr, en и pl печёт"),
    (15141, "example_uk",
     "Баронеса запросила нас на елегантний вечір",
     "Баронеса запросила нас на елегантний прийом",
     "`Party` это приём; в ru, tr, en и pl приём"),
    (10870, "example_uk",
     "Я хочу відплатити тобі за твою допомогу",
     "Я хочу віддячити тобі за твою допомогу",
     "«відплатити» значит и отомстить; «віддячити» стоит первым"),
    (17606, "example_en",
     "I need to screw a screw into the wall",
     "I need to put a screw into the wall",
     "«screw a screw» — одно слово дважды подряд"),
    (14132, "example_pl",
     "Musimy nazwać rzeczy po imieniu",
     "Musimy nazwać problem po imieniu",
     "«вещи» вместо «das Problem»"),
    (14133, "example_pl",
     "To już taki ograny stereotyp",
     "To taki stereotyp z twojej strony",
     "потеряно «von dir», и «ograny» в эталоне нет"),
    (16397, "example_pl",
     "Żołnierz stanął przed sądem wojennym",
     "Żołnierz musiał stanąć przed sądem wojennym",
     "потеряно «musste gestellt werden»"),
    (7607, "example_pl",
     "Przejdźmy do następnego punktu",
     "Chcemy przejść do następnego punktu",
     "побудительное вместо «Wir wollen übergehen»"),
    (14131, "example_pl",
     "Chcę podkreślić, że to bardzo ważne",
     "Muszę podkreślić, że to bardzo ważne",
     "«хочу» вместо «Ich muss»"),

    # ══ потерянное и добавленное слово ══════════════════════════
    (7602, "example_pl",
     "To jest zupełna bzdura",
     "To zupełna bzdura, co tam mówisz",
     "потеряно «was du da sagst»: в остальных четырёх оно есть"),
    (12761, "example_pl",
     "Po tym jedzeniu dostałem biegunki",
     "Po tym złym jedzeniu dostałem biegunki",
     "потеряно «schlechten»"),
    (10861, "example_en",
     "That was a magical night",
     "That was a really magical night",
     "потеряно «wirklich»: в остальных четырёх оно есть"),
    (10867, "example_ru",
     "Твой сын неблагодарен тебе за всё, что ты для него делаешь",
     "Твой сын неблагодарен тебе за всё, что ты делаешь",
     "«для него» в эталоне «was du tust» нет"),
    (10867, "example_pl",
     "Twój syn jest wobec ciebie niewdzięczny za wszystko, co dla niego robisz",
     "Twój syn jest wobec ciebie niewdzięczny za wszystko, co robisz",
     "то же"),
    (15621, "example_tr",
     "Bahçeye gidip kendim için birkaç elma topluyorum",
     "Bahçeye gidip elma topluyorum",
     "«kendim için» и «birkaç» в эталоне нет"),
    (9851, "example_uk",
     "Я хочу обміняти мою стару машину на нову",
     "Я хочу обміняти свою стару машину на нову",
     "при своём подлежащем нужен «свою»"),
    (143, "example_uk",
     "Як це слово пишеться по літерах?",
     "Як це пишеться по літерах?",
     "«слово» в эталоне «Wie buchstabiert man das?» нет"),
    (14588, "example_tr",
     "Gelecek yazda şehrimizdeki müzik festivaline gideceğiz",
     "Gelecek yaz şehrimizdeki müzik festivaline gideceğiz",
     "«yazda» лишний падеж при «gelecek yaz»"),

    # ══ время глагола ═══════════════════════════════════════════
    (18803, "example_pl",
     "Kupiłem nowy szampon do włosów",
     "Kupuję nowy szampon do włosów",
     "прошедшее против «Ich kaufe»; в остальных четырёх настоящее"),
    (11809, "example_pl",
     "Na kolację zrobię dziś makaron z sosem pomidorowym",
     "Na kolację robię dziś makaron z sosem pomidorowym",
     "будущее против «Ich koche»"),
    (11810, "example_pl",
     "Usiadłem przy kontuarze i zamówiłem piwo",
     "Siadam przy kontuarze i zamawiam piwo",
     "прошедшее против «Ich setze mich ... und bestelle»"),
    (10871, "example_tr",
     "Çocuk gece sessizce inliyordu",
     "Çocuk gece sessizce inliyor",
     "прошедшее длительное против «wimmert»"),
    (9006, "example_pl",
     "Kupiec z powodzeniem prowadzi swój interes od trzydziestu lat",
     "Kupiec z powodzeniem prowadził swój interes od 30 lat",
     "настоящее против «hat geführt», и число словами против цифр"),
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
