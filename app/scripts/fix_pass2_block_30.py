"""ВТОРОЙ ПРОХОД, блок 30 (ряды 5801–6000): 39 правок.

НЕМЕЦКИЙ ЭТАЛОН, ПРОТИВОРЕЧАЩИЙ САМОМУ СЕБЕ:

    verfehlen (7519)  de «Der Schuss verfehlte die Zielscheibe KNAPP
                          und flog WEIT VORBEI»

Промахнулся чуть-чуть и улетел далеко — одновременно. Такого не бывает,
и видно, что сделали переводы: каждый выбрал одну половину и дописал
своё.

    en «narrowly missed the target and flew far past» — повторил оба
    ru «чуть не попал в мишень и ушёл далеко в сторону» — повторил оба
    uk «Я промахнувся, м'яч пішов вище» — ПОДМЕНА целиком, про мяч
    tr «Atış hedefi kaçırdı ve çok ötesine uçtu» — потерял «knapp»
    pl «Strzelił, ale chybił celu o centymetr» — потерял «weit vorbei»

Это четвёртый ряд за проход с неверным немецким эталоном после `Arche`,
`Güte` и `Zünder`, и первый, где эталон не ошибается в слове, а
противоречит себе внутри одной фразы. Ряд переписан целиком: оставлено
«промахнулся чуть-чуть», потому что именно это значит `knapp verfehlen`.

ЧЕТЫРЕ ПОДМЕНЫ, И ВСЕ В РАЗНЫХ ЯЗЫКАХ:

    Beihilfe  (16375)  ru «ФЕРМЕРЫ получают дотации от государства»
    abseits    (7520)  pl «ICH DOM stoi na uboczu wsi»
    Pelz      (15596)  tr «Kışın annem KÜRK MANTOSUNU giyer»
    abwesend  (18789)  tr «YOKLUĞUNDA seni çok özledik»
    verfehlen  (7519)  uk «Я промахнувся, М'ЯЧ пішов вище»

Прежде подмены шли полосами по одному языку: девять польских в блоке 21,
семь в блоке 27. Здесь по одной в каждом, и это, похоже, другой случай —
не общий источник, а разрозненные промахи.

ЕЩЁ ОДНА ПАРА РЯДОВ НА ОДНО СЛОВО. `unterbringen` стоит в базе дважды:
18268 (B2, «Die Gäste sind gut untergebracht») и 18283 (C1, «Kannst du
meine Cousine für ein paar Nächte unterbringen?»). Первый я правил в
блоке 28, второй попался здесь. Примеры разные, уровни разные — в
строгий список дублей не попадает, как и `Ehepartner`. Записано в
HANDOVER к решению владельца.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ эталон противоречит самому себе ═════════════════════════
    (7519, "example_de",
     "Der Schuss verfehlte die Zielscheibe knapp und flog weit vorbei",
     "Der Schuss verfehlte die Zielscheibe knapp",
     "«knapp» и «weit vorbei» в одной фразе исключают друг друга"),
    (7519, "example_en",
     "The shot narrowly missed the target and flew far past",
     "The shot narrowly missed the target",
     "то же"),
    (7519, "example_ru",
     "Выстрел чуть не попал в мишень и ушёл далеко в сторону",
     "Выстрел едва не попал в мишень",
     "то же"),
    (7519, "example_uk",
     "Я промахнувся, м'яч пішов вище",
     "Вистріл трохи не влучив у мішень",
     "подмена целиком: мяч вместо выстрела и мишени"),
    (7519, "example_tr",
     "Atış hedefi kaçırdı ve çok ötesine uçtu",
     "Atış hedefi az farkla kaçırdı",
     "то же, и потеряно «knapp»"),
    (7519, "example_pl",
     "Strzelił, ale chybił celu o centymetr",
     "Strzał nieznacznie chybił celu",
     "то же, и подлежащим стал стрелок вместо выстрела"),

    # ══ КЛАСС: подменённое предложение ══════════════════════════
    (16375, "example_ru",
     "Фермеры получают дотации от государства",
     "Государство предоставляет пособие нуждающимся семьям",
     "подмена: эталон «Die Regierung gewährt Beihilfe für bedürftige Familien»"),
    (7520, "example_pl",
     "Ich dom stoi na uboczu wsi",
     "Zawsze siedzi na uboczu i nie chce grać z innymi",
     "подмена: дом на окраине вместо человека, сидящего в стороне"),
    (15596, "example_tr",
     "Kışın annem kürk mantosunu giyer",
     "Tilkinin kürkü çok güzel ve sıcak",
     "подмена: шуба матери вместо лисьего меха"),
    (18789, "example_tr",
     "Yokluğunda seni çok özledik",
     "Patron bugün yoktu ve yarın dönecek",
     "подмена: эталон «Der Chef war heute abwesend und kommt morgen zurück»"),

    # ══ слово не из своего списка и не то слово ═════════════════
    (15593, "translation_uk",
     "сходити, підніматися, відкриватися, прокидатися",
     "сходити, підніматися, відкриватися, проростати",
     "`aufgehen` не значит «прокидатися»; в ru на этом месте «всходить»"),
    (14115, "example_en",
     "I'm giving you a warning",
     "I'm giving you advance warning",
     "ни одного слова списка; `Vorwarnung` это предупреждение ЗАРАНЕЕ"),
    (18791, "example_en",
     "This is a good vintage from 2015",
     "This wine is a good vintage from 2015",
     "потеряно «Dieser Wein»"),
    (18791, "example_tr",
     "Bu şarap 2015'in iyi bir ürünü",
     "Bu şarap iyi bir 2015 mahsulü",
     "«ürün» нет в списке, а «mahsul yılı» есть"),
    (2739, "example_tr",
     "Lor yemeyi severim",
     "Lor peyniri yemeyi severim",
     "в списке «lor peyniri», а пример давал половину"),
    (7509, "example_tr",
     "Hiç kimseye acı çektirmek istemiyorum",
     "Hiç kimseye acı vermek istemiyorum",
     "«acı çektirmek» это заставлять страдать; в списке «acı vermek»"),
    (7509, "example_pl",
     "Nie chcę nikomu wyrządzić krzywdy",
     "Nie chcę nikomu zadawać bólu",
     "`Schmerz` это боль, а не обида"),
    (7516, "example_tr",
     "Senin oyunlarını gördüm, daha aptal yapma",
     "Numaralarını çözdüm, kendini daha aptal gösterme",
     "«daha aptal yapma» не фраза; и «gördüm» теряет смысл «раскусил»"),
    (12749, "example_tr",
     "Doktor hastanın sağlıklı olduğunu tespit etti",
     "Doktor hastanın sağlıklı olduğuna karar verdi",
     "«tespit etmek» нет в списке, а «karar vermek» есть"),
    (10804, "example_tr",
     "Bütün bu zaman bana dik dik baktı ve ben gerginleştim",
     "Sürekli bana dik dik baktı ve ben gerginleştim",
     "«bütün bu zaman» калька; по-турецки «sürekli»"),
    (18277, "example_ru",
     "Мы переехали в новое поселение",
     "Мы переехали в новый жилой массив",
     "`Siedlung` здесь жилой массив; «поселение» это другое значение"),
    (18277, "example_uk",
     "Ми переїхали в нове селище",
     "Ми переїхали в новий житловий масив",
     "то же"),
    (1757, "example_en",
     "A penny is an old coin",
     "A pfennig is an old coin",
     "«pfennig» стоит в списке первым, и ряд именно о нём"),
    (1757, "example_tr",
     "Pfennig eski bir madeni paradır",
     "Fenik eski bir madeni paradır",
     "немецкое слово вместо турецкого «fenik» из списка"),
    (9840, "example_uk",
     "Мій гаманець пустий",
     "Мій гаманець порожній",
     "«пустий» о вещи разговорно; по-украински «порожній»"),

    # ══ управление и сочетаемость ═══════════════════════════════
    (17210, "example_tr",
     "Yat limanda demirli",
     "Yat limanda demirlemiş",
     "без сказуемого фраза не передаёт действия «ankert»"),
    (12746, "example_pl",
     "Pracuje na oddziale chirurgii",
     "Pracuje jako specjalista w chirurgii",
     "потеряно «als Spezialist»"),
    (14557, "example_uk",
     "Я ходжу на богослужіння у неділю",
     "Я ходжу на богослужіння щонеділі",
     "«sonntags» это по воскресеньям, а не в одно воскресенье"),
    (17598, "example_ru",
     "Симуляция полёта очень реалистична",
     "Симуляция поведения самолёта в полёте очень реалистична",
     "потеряно «Flugverhalten»: в остальных четырёх оно есть"),

    # ══ потерянное слово ════════════════════════════════════════
    (10789, "example_tr",
     "Çok sinirliyim",
     "Sana çok sinirliyim",
     "потеряно «auf dich»: в остальных четырёх адресат есть"),
    (14112, "example_uk",
     "Мої привітання з днем народження",
     "Щирі привітання з днем народження",
     "«herzliche» это сердечные, а не «мої»"),
    (10790, "example_tr",
     "Mükemmellik için çaba gösteriyor",
     "O, mükemmellik için çaba gösteriyor",
     "потеряно подлежащее «Sie»"),
    (14558, "example_ru",
     "Дедушка подарил мне талисман",
     "Мой дедушка подарил мне талисман",
     "потеряно «Mein»: в en, uk и tr оно есть"),
    (14558, "example_pl",
     "Dziadek podarował mi talizman",
     "Mój dziadek podarował mi talizman",
     "то же"),

    # ══ добавленное слово ═══════════════════════════════════════
    (15125, "example_tr",
     "Bütün özenini çocuklara adıyor",
     "Özenini çocuklara adıyor",
     "«bütün» в эталоне нет"),
    (1757, "example_uk",
     "Пфеніг — це стара німецька монета",
     "Пфеніг — це стара монета",
     "«німецька» в эталоне нет"),
    (13553, "example_ru",
     "Подлежащее в предложении очень важно",
     "Подлежащее предложения важно",
     "«очень» в эталоне нет, и «des Satzes» это родительный"),
    (14111, "example_pl",
     "Gwizdem przywołał psa do siebie",
     "Gwizdem przywołał psa",
     "«do siebie» в эталоне нет"),
    (18788, "example_pl",
     "Zegar tyka bardzo głośno",
     "Zegar tyka głośno",
     "«bardzo» в эталоне нет"),
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
