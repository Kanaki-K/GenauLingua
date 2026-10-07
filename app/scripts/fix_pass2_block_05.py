"""ВТОРОЙ ПРОХОД, блок 5 (ряды 801–1000): правки, найденные глазами.

Блок дал КЛАСС, который ушёл в отдельный сквозной проход: пять рядов
подряд, где восклицательный знак стоит в одних языках и отсутствует в
других (`Glückwunsch`, `guck`, `Maul`, `beeilen`, `au`). По всей базе
таких оказалось 47 рядов, и правит их `fix_terminal_punct`. Здесь
только то, что знака не касается.

Самое важное из найденного глазами:

    verzeihen (10118)  uk «Чи можеш ти МЕНЕ пробачити?»
        «пробачати» в украинском требует давального: пробачити КОМУСЬ.
        Винительный — ошибка управления, а не выбор слова. В русском
        рядом стоит верное «простить меня» (там как раз винительный),
        и калька прошла незамеченной весь первый проход.

    überrascht (10107)  de «Ich bin MEGA überrascht»
        В эталоне молодёжное усиление, которого нет ни в одном из пяти
        переводов — все пишут «очень». Ряд A1.

    Position (894/719)  ru «Это хорошая ДОЛЖНОСТЬ»
        Тот же класс, что `Karte` в блоке 4: немецкое слово
        двусмысленно, и языки разошлись по значениям. Русский учил
        должности, остальные четыре — позиции.

    Aha (986/13873)  tr «Aha, şimdi anladım»
        Карточка показывала «anladım» (понял) как перевод «Aha»:
        первый вариант «ha» короче четырёх букв и совпадением не
        считается, поэтому выбиралось второе слово из списка. Эталон
        приведён к «Ha», и карточка снова про междометие.

Остальное обычное: выбор дальнего варианта, время глагола, потерянные
и добавленные слова, два случая «по-людски» («Это ничего особенного»
по-русски не говорят).
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ── ошибка управления ────────────────────────────────────────
    (10118, "example_uk",
     "Чи можеш ти мене пробачити?",
     "Чи можеш ти мені пробачити?",
     "«пробачати» требует давального: пробачити комусь, а не когось"),

    # ── эталон ───────────────────────────────────────────────────
    (10107, "example_de",
     "Ich bin mega überrascht",
     "Ich bin sehr überrascht",
     "«mega» — молодёжное усиление, которого нет ни в одном из пяти переводов"),

    # ── подменённый смысл ────────────────────────────────────────
    (719, "example_ru",
     "Это хорошая должность",
     "Это хорошая позиция",
     "«Position» двусмысленно, и четыре языка выбрали позицию"),
    (17057, "example_tr",
     "Geminin bordasındayız",
     "Geminin güvertesindeyiz",
     "«borda» это борт как бок судна, а «an Bord» — на борту"),
    (1684, "example_uk",
     "Я кажу, що захворів",
     "Я повідомляю, що захворів",
     "«кажу» это говорю; «sich krank melden» — сообщать о болезни"),
    (6418, "example_uk",
     "Я не можу це зрозуміти",
     "Я не можу цього усвідомити",
     "«зрозуміти» нет в списке переводов, а «усвідомити» есть"),
    (10109, "example_uk",
     "Я турбуюся за тебе",
     "Я за тебе занепокоєний",
     "глагол вместо прилагательного: карточка показывала «стурбований»"),
    (6410, "example_uk",
     "Там діра в стіні",
     "Там дірка в стіні",
     "карточка показывала «дірка», пример говорил «діра»"),
    (13873, "example_tr",
     "Aha, şimdi anladım",
     "Ha, şimdi anladım",
     "карточка показывала «anladım» вместо междометия: «ha» короче четырёх букв"),
    (10126, "example_tr",
     "Ailemize saygı gösteriyoruz",
     "Anne babamıza saygı gösteriyoruz",
     "«aile» это семья, а в эталоне «unsere Eltern» — родители"),
    (2160, "example_uk",
     "Це таки правда",
     "Це, щоправда, так",
     "«таки» нет в списке переводов, а «щоправда» есть"),
    (2160, "example_tr",
     "Bu gerçekten doğru",
     "Bu gerçi doğru",
     "«gerçekten» это действительно; «gerçi» есть в списке переводов"),
    (10104, "example_pl",
     "Taki już mój los",
     "To mój los",
     "переформулировано: эталон «Das ist mein Schicksal»"),
    (12105, "example_pl",
     "Zapraszamy cię",
     "Jesteś zaproszony",
     "эталон в страдательном («Du wirst eingeladen»), польский был в действительном"),
    (13432, "example_pl",
     "To ten pan, którego samochód jest czerwony",
     "Mężczyzna, którego samochód jest czerwony",
     "«Der Mann» это мужчина, и «To ten» в эталоне нет"),
    (12098, "example_ru",
     "Мне это доставляет удовольствие",
     "Это для меня удовольствие",
     "эталон — формула вежливости «Es ist mir ein Vergnügen», а не рассказ о себе"),
    (12098, "example_uk",
     "Мені це доставляє задоволення",
     "Це для мене задоволення",
     "то же"),

    # ── по-людски ────────────────────────────────────────────────
    (6416, "example_ru",
     "Это ничего особенного",
     "Ничего особенного",
     "«это ничего особенного» по-русски не говорят"),
    (6416, "example_uk",
     "Це нічого особливого",
     "Нічого особливого",
     "то же по-украински"),
    (1530, "example_ru",
     "Заходи, пожалуйста, внутрь!",
     "Заходи, пожалуйста!",
     "«заходи внутрь» по-русски тавтология"),
    (1530, "example_uk",
     "Заходь, будь ласка, усередину!",
     "Заходь, будь ласка!",
     "то же по-украински"),

    # ── потерянное слово ─────────────────────────────────────────
    (6377, "example_ru",
     "Мы должны выжить",
     "Мы должны это пережить",
     "потеряно «das»: в en, uk, tr и pl оно есть"),
    (50, "example_uk",
     "Завдання не складне",
     "Це завдання не складне",
     "потеряно «Diese»: в ru, en и pl оно есть"),
    (50, "example_tr",
     "Görev zor değil",
     "Bu görev zor değil",
     "то же"),
    (801, "example_en",
     "The pain is strong",
     "The pain is very strong",
     "потеряно «sehr»: в ru, uk и pl оно есть"),
    (801, "example_tr",
     "Ağrı şiddetli",
     "Ağrı çok şiddetli",
     "то же"),
    (2971, "example_ru",
     "Я тебе обещаю",
     "Я тебе это обещаю",
     "потеряно «das»: в uk, en и pl оно есть"),
    (13431, "example_uk",
     "Такого я ще не бачив",
     "Такого я ще ніколи не бачив",
     "потеряно «nie»: в ru, en и tr оно есть"),
    (13433, "example_uk",
     "Я нікому не скажу",
     "Я нікому цього не скажу",
     "потеряно «es»: в ru и pl оно есть"),
    (2585, "example_tr",
     "Soruların var mı?",
     "Herhangi bir soru var mı?",
     "потеряно «irgendwelche» — слово ряда"),
    (129, "example_en",
     "That was a stupid joke",
     "That was a stupid joke of yours",
     "потеряно «von dir»: в ru и pl оно есть"),
    (129, "example_uk",
     "Це був дурний жарт",
     "Це був дурний жарт з твого боку",
     "то же"),
    (129, "example_tr",
     "Bu saçma bir şakaydı",
     "Bu senin saçma bir şakandı",
     "то же"),
    (6388, "example_uk",
     "Дивись сюди!",
     "Дивись-но сюди!",
     "потеряна частица «mal»: в ru «-ка», в pl «no»"),
    (6388, "example_tr",
     "Buraya bak!",
     "Buraya bir bak!",
     "то же"),

    # ── добавленное слово ────────────────────────────────────────
    (702, "example_tr",
     "Bu ayakkabılar ayağıma tam uyuyor",
     "Ayakkabılar iyi uyuyor",
     "«ayağıma tam» в эталоне нет: «Die Schuhe passen gut»"),
    (6383, "example_ru",
     "Там ещё остался торт",
     "Ещё остался торт",
     "«там» в эталоне нет: «Es ist noch Kuchen übrig»"),
    (6383, "example_pl",
     "Pozostało jeszcze trochę ciasta",
     "Pozostało jeszcze ciasto",
     "«trochę» в эталоне нет"),
    (6397, "example_pl",
     "Już się zdecydowałem",
     "Zdecydowałem się",
     "«już» в эталоне нет: «Ich habe mich entschieden»"),
    (11635, "example_uk",
     "Вечеря вже готова",
     "Вечеря готова",
     "«вже» в эталоне нет: «Das Abendessen ist fertig»"),
    (6398, "example_en",
     "These numbers just don't add up",
     "These numbers don't add up",
     "«just» в эталоне нет: «Die Zahlen stimmen nicht»"),
    (169, "example_uk",
     "Це триває одну годину",
     "Це триває годину",
     "«eine» здесь артикль, а не числительное: в ru и pl числа нет"),

    # ── предлог и время глагола ──────────────────────────────────
    (76, "example_uk",
     "М'яч котиться по вулиці",
     "М'яч котиться через вулицю",
     "«über die Straße» это через дорогу, а не по ней"),
    (76, "example_tr",
     "Top sokakta yuvarlanıyor",
     "Top yolun karşısına yuvarlanıyor",
     "то же: «sokakta» это на улице"),
    (915, "example_pl",
     "Wezmę taksówkę na dworzec",
     "Biorę taksówkę na dworzec",
     "будущее против «Ich nehme»; в ru, uk, en и tr настоящее"),
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
