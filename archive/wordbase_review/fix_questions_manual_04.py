"""
Потерянная вопросительная форма, партия 4 из списка `scan_question_mark`.

Здесь особенно много рядов, где **все** переводы ушли от немецкого в одну и
ту же сторону: немецкий просит о чём-то вопросом, а переводы приводят
посторонний пример на то же слово.

* `abladen` — «Kannst du mir die Kisten abladen helfen?», а в английском,
  турецком и украинском грузовик разгружает товар на складе.
* `wegbleiben` — немецкий спрашивает, почему ты вчера не пришёл; польский,
  турецкий и украинский советуют остаться дома, если болеешь.
* `Beleg` — немецкий спрашивает про чек из магазина, четыре языка велят
  сохранить чек для налоговой.
* `nah` — немецкий просит подробностей, три языка рассуждают о «ближайшем
  будущем». Взято другое значение слова.

Попутно две опечатки: украинское «скланку» вместо «склянку» и
«прогулюємся» вместо «прогуляємося».

    python -m app.scripts.fix_questions_manual_04            # показать
    python -m app.scripts.fix_questions_manual_04 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# (id, колонка, что стоит сейчас, на что менять, зачем)
FIXES: list[tuple[int, str, str, str, str]] = [

    # --- потерян только знак ---------------------------------------------------
    (7258, "example_uk", "Ти можеш винести мішки зі сміттям",
     "Ти можеш винести мішки зі сміттям?", "потерян только знак"),
    (7424, "example_tr", "Aşağı gidebilir miyiz", "Aşağı gidebilir miyiz?",
     "потерян только знак"),
    (7512, "example_pl", "Chcesz uczestniczyć w naszym projekcie",
     "Chcesz uczestniczyć w naszym projekcie?", "потерян только знак"),
    (7526, "example_ru", "Можешь смазать петли двери маслом",
     "Можешь смазать петли двери маслом?", "потерян только знак"),
    (7528, "example_uk", "Можеш позначити важливі місця в тексті",
     "Можеш позначити важливі місця в тексті?", "потерян только знак"),
    (7885, "example_uk", "Можеш підтвердити запрошення",
     "Можеш підтвердити запрошення?", "потерян только знак"),

    # --- порядок слов, опечатки, грамматика ------------------------------------
    (7512, "example_uk", "Хочеш ти брати участь у нашому проекті",
     "Хочеш брати участь у нашому проекті?",
     "порядок слов и потерянный знак"),
    (7829, "example_uk", "Можеш ти дізнатися, хто це зробив",
     "Можеш дізнатися, хто це зробив?", "порядок слов и потерянный знак"),
    (7986, "example_uk", "Можеш наповнити скланку, будь ласка",
     "Можеш наповнити склянку, будь ласка?",
     "«скланку» — опечатка, нужно «склянку»; и потерян знак"),
    (8083, "example_uk", "Давайте вийдемо та прогулюємся",
     "Може, вийдемо прогулятися?",
     "«прогулюємся» — такой формы нет; и потерян знак"),
    (7526, "example_tr", "Kapı menteşelerini yağla mısın?",
     "Kapı menteşelerini yağlar mısın?",
     "«yağla mısın» — неверная форма, нужно «yağlar mısın»"),

    # --- вместо вопроса стоит повеление ----------------------------------------
    (7526, "example_pl", "Posmaruj kanapkę masłem",
     "Możesz naoliwić zawiasy drzwi?",
     "пример про бутерброд, а немецкий про петли, и это вопрос"),
    (7528, "example_pl", "Zaznacz ważne zdania w tekście",
     "Możesz zaznaczyć ważne miejsca w tekście?",
     "в немецком вопрос, а не приказ"),
    (7986, "example_pl", "Napełnij szklankę do pełna",
     "Możesz napełnić szklankę?", "в немецком вопрос, а не приказ"),
    (8049, "example_en",
     "Put your phone away and concentrate on your homework",
     "Can you put the phone away, please?",
     "в немецком вежливый вопрос, и домашней работы там нет"),
    (8049, "example_tr",
     "Telefonunu bir tarafa koy ve ödevine konsantre ol",
     "Lütfen telefonu bir kenara koyar mısın?",
     "в немецком вежливый вопрос, и домашней работы там нет"),
    (8049, "example_uk",
     "Відклади телефон і сконцентруйся на домашній роботі",
     "Можеш, будь ласка, відкласти телефон?",
     "в немецком вежливый вопрос, и домашней работы там нет"),
    (8081, "example_pl", "Podaj mi konkretny przykład",
     "Możesz podać mi konkretny przykład, nie tak ogólnie?",
     "в немецком вопрос и «не так расплывчато»"),
    (8334, "example_pl", "Uzupełnij brakujące słowa w zdaniu",
     "Możesz uzupełnić moje zdanie?",
     "в немецком вопрос про «моё предложение», а не приказ"),
    (8079, "example_pl", "Zajrzyj do garnka, czy zupa gotowa",
     "Możesz zajrzeć, czy jedzenie gotowe?",
     "в немецком вопрос, и суп там не упомянут"),

    # --- перевод переводит другое предложение ---------------------------------
    (7240, "example_en", "She portrays a young nurse",
     "What is this picture supposed to show?",
     "взято другое значение: «играть роль» вместо «изображать»"),
    (7240, "example_tr", "Filmde bir polis rolü oynuyor",
     "Bu resim neyi gösteriyor?",
     "взято другое значение: «играть роль» вместо «изображать»"),
    (7240, "example_uk", "Він грає роль поліцейського у фільмі",
     "Що має зображати ця картина?",
     "взято другое значение: «играть роль» вместо «изображать»"),
    (7339, "example_en", "I have to leave in ten minutes",
     "Do you have to leave again already?",
     "в немецком вопрос «ты», а не «мне через десять минут»"),
    (7339, "example_tr", "Akşamları sık sık dışarı çıkıyor",
     "Yine gitmek zorunda mısın?", "пример про другое"),
    (7339, "example_uk", "Вона часто виходить вечором",
     "Ти вже знову мусиш іти?", "пример про другое"),
    (7424, "example_uk", "Починаймо спускатися з гори",
     "Можемо спуститися?", "в немецком вопрос, и горы там нет"),
    (7548, "example_en", "I skipped the boring parts of the movie",
     "Can we skip this chapter?",
     "в немецком вопрос про главу, а не рассказ про фильм"),
    (7548, "example_tr", "Filmin sıkıcı kısımlarını atladım",
     "Bu bölümü atlayabilir miyiz?",
     "в немецком вопрос про главу, а не рассказ про фильм"),
    (7548, "example_uk", "Я пропустив нудні частини фільму",
     "Можемо пропустити цей розділ?",
     "в немецком вопрос про главу, а не рассказ про фильм"),
    (7778, "example_en", "We need to assemble a team for the project",
     "Can you put the shelf back together?",
     "в немецком полка, а не команда для проекта"),
    (7778, "example_pl", "Pomóż mi złożyć tę półkę z powrotem",
     "Możesz złożyć tę półkę z powrotem?",
     "в немецком вопрос, а не просьба помочь"),
    (7778, "example_tr", "Proje için bir takım oluşturmalıyız",
     "Rafı tekrar birleştirebilir misin?",
     "в немецком полка, а не команда для проекта"),
    (7778, "example_uk", "Ми повинні скласти команду для проекту",
     "Можеш знову скласти полицю?",
     "в немецком полка, а не команда для проекта"),
    (7833, "example_en", "He stayed away from the meeting again",
     "Why did you stay away yesterday?",
     "в немецком вопрос «ты» про вчера"),
    (7833, "example_pl", "Jeśli jesteś chory, nie przychodź do pracy",
     "Dlaczego cię wczoraj nie było?", "пример про другое"),
    (7833, "example_tr", "Hasta isen evde kalmalısın",
     "Dün neden gelmedin?", "пример про другое"),
    (7833, "example_uk", "Якщо ти хворий, ти повинен залишатися вдома",
     "Чому тебе вчора не було?", "пример про другое"),
    (7857, "example_pl", "Trudno ocenić, ile to potrwa",
     "Czy potrafisz właściwie ocenić sytuację?",
     "в немецком вопрос «ты», а не рассуждение"),
    (7913, "example_en",
     "The truck unloaded the goods at the warehouse",
     "Can you help me unload the boxes?",
     "в немецком просьба-вопрос, а не рассказ про грузовик"),
    (7913, "example_pl", "Pomóż mi wyładować zakupy z auta",
     "Możesz mi pomóc wyładować skrzynki?",
     "в немецком ящики и вопрос, а не покупки и приказ"),
    (7913, "example_tr", "Kamyon depodan malları boşalttı",
     "Kutuları boşaltmama yardım eder misin?",
     "в немецком просьба-вопрос, а не рассказ про грузовик"),
    (7913, "example_uk", "Вантажівка розвантажувала товари на складі",
     "Можеш допомогти мені розвантажити ящики?",
     "в немецком просьба-вопрос, а не рассказ про грузовик"),
    (8019, "example_en",
     "The near future will show whether this works",
     "Can you give me more detailed information?",
     "взято другое значение: «близкое будущее» вместо «подробнее»"),
    (8019, "example_tr",
     "Yakın gelecek bunun işe yarayıp yaramayacağını gösterecek",
     "Bana daha ayrıntılı bilgi verebilir misiniz?",
     "взято другое значение: «близкое будущее» вместо «подробнее»"),
    (8019, "example_uk",
     "Найближче майбутнє покаже, чи це працюватиме",
     "Чи можете Ви дати мені докладнішу інформацію?",
     "взято другое значение: «близкое будущее» вместо «подробнее»"),
    (8079, "example_uk", "Зазирни до нас увечері на чай",
     "Можеш зазирнути, чи їжа готова?",
     "пример про чай, а немецкий про готовность еды"),
    (8081, "example_tr",
     "Bana somut bir örnek verebilir misin, bu kadar muğlak değil",
     "Bu kadar muğlak değil de bana somut bir örnek verebilir misin?",
     "вторая половина оборвана и повисает"),
    (8083, "example_pl", "Wyjdźmy na chwilę na dwór",
     "Wyjdziemy na spacer?", "в немецком вопрос, и это про прогулку"),
    (8125, "example_pl", "Zastaliśmy w domu straszny bałagan",
     "Co tam zastaniemy?",
     "в немецком вопрос о будущем, а не рассказ о прошлом"),
    (8125, "example_tr", "Eve geldiğimde boş bir ev buldum",
     "Orada neyle karşılaşacağız acaba?",
     "в немецком вопрос о будущем, а не рассказ о прошлом"),
    (8177, "example_en", "Keep the receipt for your tax return",
     "Do you still have the receipt from the supermarket?",
     "в немецком вопрос про чек из магазина, а не совет про налоги"),
    (8177, "example_pl", "Zachowaj paragon ze sklepu",
     "Masz jeszcze paragon z supermarketu?",
     "в немецком вопрос, а не приказ"),
    (8177, "example_tr", "Vergi beyannamesi için makbuzu sakla",
     "Süpermarket fişi hâlâ sende mi?",
     "в немецком вопрос про чек из магазина, а не совет про налоги"),
    (8177, "example_uk", "Збережи квитанцію для податкової декларації",
     "У тебе ще є чек із супермаркету?",
     "в немецком вопрос про чек из магазина, а не совет про налоги"),
    (8249, "example_pl", "Zostaw mi wolny piątek wieczorem",
     "Możesz zarezerwować dla mnie przyszły piątek?",
     "в немецком следующая пятница и вопрос, а не вечер и приказ"),
    (8249, "example_uk", "Залиш, будь ласка, це місце вільним",
     "Можеш звільнити для мене наступну п'ятницю?",
     "пример про место, а немецкий про пятницу"),
    (8294, "example_en", "The driver couldn't give me change",
     "Can you give change for fifty euros?",
     "в немецком вопрос, а не рассказ про водителя"),
    (8294, "example_tr", "Kasiyer para üstü vermeyi unuttu",
     "Elli euroyu bozabilir misiniz?",
     "в немецком вопрос, а не рассказ про кассира"),
    (8294, "example_uk", "Продавець забув дати мені решту",
     "Чи можете Ви дати решту з п'ятдесяти євро?",
     "в немецком вопрос, а не рассказ про продавца"),
    (8389, "example_en",
     "The lawyer put forward new arguments in court",
     "Would you like to add anything?",
     "в немецком вопрос «ты», а не рассказ про адвоката"),
]


def main() -> None:
    apply_mode = "--apply" in sys.argv
    engine = create_engine(settings.DATABASE_URL_SYNC)

    ok, skipped = [], []
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
    for wid, col, was, now, why in ok:
        print(f"  {wid} {col} — {why}")
        print(f"      было:  {was!r}")
        print(f"      стало: {now!r}")
    for wid, col, cur in skipped:
        print(f"  ПРОПУЩЕНО {wid} {col}: {cur!r}")

    if not apply_mode:
        print("\nэто показ. Для применения — флаг --apply")
        return

    with engine.begin() as conn:
        for wid, col, _, now, _ in ok:
            conn.execute(text(f"UPDATE words SET {col} = :v WHERE id = :i"),
                         {"v": now, "i": wid})
    print(f"\nприменено: {len(ok)}")

    with engine.connect() as conn:
        bad = 0
        for wid, col, _, now, _ in ok:
            cur = conn.execute(text(f"SELECT {col} FROM words WHERE id = :i"),
                               {"i": wid}).scalar()
            if (cur or "").strip() != now:
                print(f"  ТРЕВОГА: {wid} {col} не записалось")
                bad += 1
        print(f"самопроверка: не записалось {bad}")


if __name__ == "__main__":
    main()
