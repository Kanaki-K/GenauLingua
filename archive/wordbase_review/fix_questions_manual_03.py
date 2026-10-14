"""
Потерянная вопросительная форма, партия 3 из списка `scan_question_mark`.

Половина партии — украинские ячейки, где потерян ровно знак: «Можеш
відкрити двері», «Можеш говорити голосніше». Сторож их не тронул
намеренно: славянский вопрос без частицы формально не отличается от
утверждения, и машине доверять такое нельзя. Глазами видно сразу.

Вторая половина — снова другое предложение, и часто во всех языках сразу:

* `rumlaufen` — немецкий «Musst du so im Schlafanzug rumlaufen?», а
  английский, турецкий и украинский рассказывают про того, кто «весь день
  ходит по квартире и ничего не делает».
* `stehenbleiben` — немецкий просит постоять, а переводы сообщают, что
  «часы остановились». Взято другое значение слова.
* `holen` — немецкий просит молоко из подвала, переводы обещают пиво.
* `hierher` — немецкий спрашивает «как ты сюда попал», переводы велят
  «иди сюда».

    python -m app.scripts.fix_questions_manual_03            # показать
    python -m app.scripts.fix_questions_manual_03 --apply    # применить
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
    (2591, "example_tr", "İş unvanın nedir", "İş unvanın nedir?",
     "потерян только знак"),
    (6268, "example_uk", "Це можливо", "Це можливо?", "потерян только знак"),
    (6355, "example_uk", "Можеш відкрити двері", "Можеш відкрити двері?",
     "потерян только знак"),
    (6474, "example_uk", "Можеш говорити голосніше",
     "Можеш говорити голосніше?", "потерян только знак"),
    (6496, "example_tr", "Onun yalan söylediğini fark etmiyor musun",
     "Onun yalan söylediğini fark etmiyor musun?", "потерян только знак"),
    (6510, "example_uk", "Чи вмієш ти рахувати до десяти",
     "Чи вмієш ти рахувати до десяти?", "потерян только знак"),
    (6530, "example_uk", "Чи можна мені ненадовго увійти",
     "Чи можна мені ненадовго увійти?", "потерян только знак"),
    (6592, "example_uk", "Можеш взяти книгу", "Можеш взяти книгу?",
     "потерян только знак"),
    (6596, "example_uk", "Ти можеш записати розмову",
     "Ти можеш записати розмову?", "потерян только знак"),
    (6607, "example_uk", "Можеш вирівняти картину",
     "Можеш вирівняти картину?", "потерян только знак"),
    (6615, "example_tr", "Bu cihazın amacı nedir", "Bu cihazın amacı nedir?",
     "потерян только знак"),
    (6674, "example_uk", "Зайдемо в кафе", "Зайдемо в кафе?",
     "потерян только знак"),
    (6689, "example_uk", "Можеш це підняти", "Можеш це підняти?",
     "потерян только знак"),
    (6718, "example_uk", "Можеш пояснити це точніше",
     "Можеш пояснити це точніше?", "потерян только знак"),
    (6748, "example_uk", "Можеш повернути мені книгу завтра",
     "Можеш повернути мені книгу завтра?", "потерян только знак"),
    (6762, "example_uk", "Можеш подивитися направо",
     "Можеш подивитися направо?", "потерян только знак"),
    (6785, "example_en", "Excuse me, can I interrupt you briefly",
     "Excuse me, can I interrupt you briefly?", "потерян только знак"),
    (6908, "example_uk", "Можеш округлити число до 50",
     "Можеш округлити число до 50?", "потерян только знак"),
    (6938, "example_uk", "Можеш організувати зустріч з нею",
     "Можеш організувати зустріч з нею?", "потерян только знак"),
    (7109, "example_uk", "Ти можеш вгадати загадку",
     "Ти можеш вгадати загадку?", "потерян только знак"),
    (7200, "example_uk", "Ти можеш випустити собаку",
     "Ти можеш випустити собаку?", "потерян только знак"),

    # --- порядок слов и слово не то, плюс знак ---------------------------------
    (6349, "example_uk", "У тебе є подальші питання", "У тебе є ще питання?",
     "«подальші питання» по-украински не говорят"),
    (6661, "example_uk", "Можеш тут повернути", "Можеш тут розвернутися?",
     "wenden — развернуться, а не повернуть"),
    (6923, "example_uk", "Можеш ти їх розрізнити", "Можеш їх розрізнити?",
     "порядок слов и потерянный знак"),
    (6954, "example_uk", "Можеш ти повернути мої речі",
     "Можеш повернути мої речі?", "порядок слов и потерянный знак"),
    (6992, "example_tr", "Ayakkabılarımı bağlar mısın bana",
     "Bana ayakkabılarımı bağlar mısın?",
     "«bana» в конце повисает; и потерян знак"),
    (7042, "example_uk", "Можеш мені достати матеріали",
     "Можеш дістати мені матеріали?",
     "«достати» — русизм, по-украински «дістати»"),

    # --- в немецком «ты», в переводе «Вы» --------------------------------------
    (2275, "example_tr", "Meslek unvanınız nedir", "Meslek unvanın ne?",
     "в немецком «deine» — ты; и потерян знак"),
    (2510, "example_tr", "Maaş beklentiniz nedir", "Maaş beklentin ne?",
     "в немецком «deine» — ты; и потерян знак"),
    (6785, "example_uk", "Вибачте, чи можу я вас ненадовго перервати",
     "Вибач, чи можу я тебе ненадовго перервати?",
     "в немецком «dich» — тебя; и потерян знак"),

    # --- вместо вопроса стоит повеление ----------------------------------------
    (6274, "example_en", "Come here", "How did you get here?",
     "в немецком вопрос «как ты сюда попал», а не приказ"),
    (6274, "example_tr", "Buraya gel", "Buraya nasıl geldin?",
     "в немецком вопрос «как ты сюда попал», а не приказ"),
    (6274, "example_uk", "Іди сюди", "Як ти сюди дістався?",
     "в немецком вопрос «как ты сюда попал», а не приказ"),
    (6344, "example_en", "Take a look at that",
     "Do you want to take a look at that?",
     "в немецком вопрос, а не приказ"),
    (6344, "example_uk", "Подивись на це", "Хочеш на це подивитися?",
     "в немецком вопрос, а не приказ"),
    (7198, "example_pl", "Doczep przyczepę do samochodu",
     "Możesz doczepić przyczepę?", "в немецком вопрос, а не приказ"),
    (7200, "example_pl", "Wypuść psa do ogrodu", "Możesz wypuścić psa?",
     "в немецком вопрос, а не приказ"),

    # --- перевод переводит другое предложение ---------------------------------
    (2300, "example_en", "We meet in the beer garden",
     "Shall we meet in the beer garden?",
     "в немецком это предложение-вопрос"),
    (2300, "example_tr", "Bira bahçesinde buluşuyoruz",
     "Bira bahçesinde buluşalım mı?", "в немецком это предложение-вопрос"),
    (2300, "example_uk", "Ми зустрічаємося в пивному саду",
     "Зустрінемося в пивному саду?", "в немецком это предложение-вопрос"),
    (2586, "example_en", "Someone will help", "Will someone help me?",
     "в немецком вопрос, и «мне» потеряно"),
    (2586, "example_tr", "Biri yardım edecek", "Biri bana yardım eder mi?",
     "в немецком вопрос, и «мне» потеряно"),
    (2586, "example_uk", "Хтось допоможе", "Хтось мені допоможе?",
     "в немецком вопрос, и «мені» потеряно"),
    (6287, "example_en", "I'll get you a beer",
     "Will you get some milk from the cellar, please?",
     "в немецком просят молоко из подвала, а не обещают пиво"),
    (6287, "example_tr", "Sana bir bira getiririm",
     "Lütfen bodrumdan süt getirir misin?",
     "в немецком просят молоко из подвала, а не обещают пиво"),
    (6287, "example_uk", "Я принесу тобі пиво",
     "Принесеш, будь ласка, молоко з підвалу?",
     "в немецком просят молоко из подвала, а не обещают пиво"),
    (6411, "example_uk", "Цих грошей вистачить до кінця місяця",
     "Можу передати тобі сіль?",
     "взято другое значение: «хватит» вместо «передать»"),
    (6511, "example_uk", "Я повертаюся додому о шостій",
     "Коли ти повернешся?", "в немецком вопрос «когда ты вернёшься»"),
    (6621, "example_uk", "Мені потрібна хоч якась допомога",
     "У тебе є якась ідея?", "пример про помощь, а немецкий про идею"),
    (6672, "example_tr", "Polis şüphelinin kimliğini belirledi",
     "Fotoğraftaki adamı tanıyabilir misin?",
     "пример про полицию, а немецкий спрашивает «ты»"),
    (6674, "example_tr", "Kafeye girer miyiz", "Kafeye girelim mi?",
     "в немецком «sollen wir» — предложение, а не возможность"),
    (6735, "example_uk", "Я щоранку спорожняю поштову скриньку",
     "Можеш, будь ласка, винести сміття?",
     "пример про почтовый ящик, а немецкий про мусор"),
    (6753, "example_tr", "Bu ilaç gerçekten işe yaradı",
     "Randevuyla her şey yolunda gitti mi?",
     "пример про лекарство, а немецкий про встречу"),
    (6753, "example_uk", "Мені не вдається відкрити банку",
     "Чи все вийшло із зустріччю?",
     "пример про банку, а немецкий про встречу"),
    (7087, "example_en", "The clock stopped",
     "Can you all stop for a moment?",
     "взято другое значение: часы встали вместо просьбы постоять"),
    (7087, "example_tr", "Saat durdu", "Biraz durabilir misiniz?",
     "взято другое значение: часы встали вместо просьбы постоять"),
    (7087, "example_uk", "Годинник зупинився",
     "Можете на хвилинку зупинитися?",
     "взято другое значение: часы встали вместо просьбы постоять"),
    (7163, "example_en",
     "He walks around the apartment all day and does nothing",
     "Do you have to walk around in your pyjamas like that?",
     "в немецком вопрос «ты» про пижаму"),
    (7163, "example_tr",
     "O, dairenin etrafında dolaşıyor ve hiçbir şey yapmıyor",
     "Böyle pijamayla dolaşmak zorunda mısın?",
     "в немецком вопрос «ты» про пижаму"),
    (7163, "example_uk",
     "Він весь день ходить по квартирі і нічого не робить",
     "Ти мусиш так ходити в піжамі?",
     "в немецком вопрос «ты» про пижаму"),
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
