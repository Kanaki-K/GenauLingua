"""
Потерянная вопросительная форма, партия 5 из списка `scan_question_mark`.

Та же работа. Повторяющийся вид дефекта в этой партии — **немецкий
обращается к человеку, а переводы рассказывают про третье лицо**:

* `vorbringen` — «Möchtest du noch etwas vorbringen?», а в четырёх языках
  адвокат выдвигает аргументы в суде.
* `ausüben` — немецкий спрашивает, кем ты хочешь работать; переводы хвалят
  того, кто «выполняет работу очень добросовестно».
* `vorlesen` — немецкий просит прочитать письмо, переводы: «мама читает мне
  историю вслух».
* `herumschnüffeln` и `herumlaufen` — немецкий укоряет собеседника, а
  переводы рассказывают про собаку и про детей в парке.

Отдельно: `gewillt` — турецкий пример оборван на условии и повисает: «Bana
yardım etmeye istekliysen» — «если ты готов мне помочь…» и всё.

    python -m app.scripts.fix_questions_manual_05            # показать
    python -m app.scripts.fix_questions_manual_05 --apply    # применить
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
    (8494, "example_uk", "Можеш вставити це речення сюди",
     "Можеш вставити це речення сюди?", "потерян только знак"),
    (9505, "example_tr", "Demek istediğimi anlıyor musun",
     "Demek istediğimi anlıyor musun?", "потерян только знак"),
    (9756, "example_uk", "Якої марки твоя машина", "Якої марки твоя машина?",
     "потерян только знак"),
    (9783, "example_uk", "Я можу позичити твою книгу",
     "Я можу позичити твою книгу?", "потерян только знак"),
    (10118, "example_uk", "Чи можеш ти мене пробачити",
     "Чи можеш ти мене пробачити?", "потерян только знак"),
    (10482, "example_tr", "Senin ihtiyaçların neler",
     "Senin ihtiyaçların neler?", "потерян только знак"),
    (10701, "example_uk", "Ти готовий мені допомогти",
     "Ти готовий мені допомогти?", "потерян только знак"),
    (11318, "example_uk",
     "Можеш мені зробити послугу і принести цукор з кухні",
     "Можеш мені зробити послугу і принести цукор з кухні?",
     "потерян только знак"),
    (11678, "example_tr", "Votka mı bira mı istiyorsun",
     "Votka mı bira mı istiyorsun?", "потерян только знак"),
    (11678, "example_uk", "Хочеш горілку чи пиво", "Хочеш горілку чи пиво?",
     "потерян только знак"),
    (11680, "example_ru", "Можешь купить масло", "Можешь купить масло?",
     "потерян только знак"),
    (11680, "example_uk", "Можеш купити масло", "Можеш купити масло?",
     "потерян только знак"),
    (12318, "example_uk", "Ти вже купив квиток на концерт",
     "Ти вже купив квиток на концерт?", "потерян только знак"),
    (12803, "example_uk", "Можеш помасажувати мені спину",
     "Можеш помасажувати мені спину?", "потерян только знак"),
    (13358, "example_uk", "Це ваша машина", "Це ваша машина?",
     "потерян только знак"),
    (13365, "example_tr", "Kimi arıyorsun", "Kimi arıyorsun?",
     "потерян только знак"),
    (13398, "example_uk", "Для чого ці гроші", "Для чого ці гроші?",
     "потерян только знак"),
    (13423, "example_uk", "Про що ти говориш", "Про що ти говориш?",
     "потерян только знак"),
    (13434, "example_uk", "Про що йдеться", "Про що йдеться?",
     "потерян только знак"),
    (13444, "example_uk", "Хтось дзвонив", "Хтось дзвонив?",
     "потерян только знак"),
    (13507, "example_en", "To what extent did that affect you",
     "To what extent did that affect you?", "потерян только знак"),

    # --- русизм и неверное слово, плюс знак ------------------------------------
    (11841, "example_uk", "Хочеш рюмочку вина", "Хочеш чарку вина?",
     "«рюмочка» — русизм, по-украински «чарка»"),
    (10285, "example_tr", "Bunun için motifin neydi",
     "Bunun için sebebin neydi?",
     "турецкое «motif» — узор, а не побуждение"),
    (10701, "example_tr", "Bana yardım etmeye istekliysen",
     "Bana yardım etmeye istekli misin?",
     "фраза оборвана на условии и повисает"),
    (8465, "example_tr", "Erkek kardeşin partide hazır mıydı",
     "Kardeşin partide miydi?",
     "«hazır» — готов, а zugegen — присутствовал"),

    # --- в переводе лишнее или не то, плюс знак --------------------------------
    (13391, "example_pl", "Po co ci to wszystko", "Po co ci to?",
     "«wszystko» в немецком нет; и потерян знак"),
    (13413, "example_pl", "Na co jeszcze czekasz", "Na co czekasz?",
     "«jeszcze» в немецком нет; и потерян знак"),
    (13434, "example_pl", "O co w tym wszystkim chodzi", "O co chodzi?",
     "«w tym wszystkim» в немецком нет; и потерян знак"),
    (13423, "example_pl", "O czym wy tak rozmawiacie", "O czym ty mówisz?",
     "в немецком «du» — ты, а не «вы»"),
    (13398, "example_pl", "Po co ci tyle pieniędzy",
     "Na co są te pieniądze?",
     "в немецком «для чего эти деньги», а не «зачем тебе столько»"),
    (9014, "example_uk", "Можеш мені допомогти в магазині",
     "Можеш сьогодні ненадовго допомогти мені в магазині?",
     "потеряны «сегодня» и «ненадолго»"),
    (8681, "example_uk", "Знеси валізи вниз, будь ласка",
     "Можеш знести валізи вниз?", "в немецком вопрос, а не приказ"),
    (9797, "example_uk", "У тебе є чек для повернення",
     "У тебе є чек про покупку?",
     "в немецком чек о покупке, а не для возврата"),
    (9915, "example_pl", "Podaj mi swój numer konta",
     "Jaki jest twój numer konta?", "в немецком вопрос, а не приказ"),
    (10482, "example_pl", "Każdy ma inne potrzeby", "Jakie masz potrzeby?",
     "в немецком вопрос «ты», а не общее рассуждение"),
    (13735, "example_pl", "Zapinam koszulę pod szyją",
     "Możesz mi pomóc zapiąć płaszcz?",
     "пример про рубашку, а немецкий просит помочь с пальто"),

    # --- перевод переводит другое предложение ---------------------------------
    (8389, "example_pl", "Adwokat przedstawił nowe argumenty w sądzie",
     "Chcesz jeszcze coś dodać?",
     "в немецком вопрос «ты», а не рассказ про адвоката"),
    (8389, "example_tr", "Avukat mahkemede yeni argümanlar ortaya koydu",
     "Eklemek istediğin bir şey var mı?",
     "в немецком вопрос «ты», а не рассказ про адвоката"),
    (8389, "example_uk", "Адвокат висунув нові аргументи в суді",
     "Хочеш ще щось додати?",
     "в немецком вопрос «ты», а не рассказ про адвоката"),
    (8412, "example_en", "He cut up the meat into small pieces",
     "Can you cut up the paper?",
     "в немецком бумага и вопрос, а не мясо"),
    (8412, "example_tr", "O, eti küçük parçalara ayırdı",
     "Kâğıdı kesebilir misin?",
     "в немецком бумага и вопрос, а не мясо"),
    (8412, "example_uk", "Він нарізав м'ясо на маленькі шматочки",
     "Можеш розрізати папір?",
     "в немецком бумага и вопрос, а не мясо"),
    (8487, "example_en",
     "The dog sniffs around all the time and wants to poke its nose everywhere",
     "Do you have to snoop around in my things?",
     "в немецком упрёк собеседнику, а не рассказ про собаку"),
    (8487, "example_tr", "Köpek her yere burnunu sokuyor",
     "Eşyalarımı karıştırmak zorunda mısın?",
     "в немецком упрёк собеседнику, а не рассказ про собаку"),
    (8487, "example_uk",
     "Собака весь час нюхає й хоче скрізь совати свій ніс",
     "Ти мусиш ритися в моїх речах?",
     "в немецком упрёк собеседнику, а не рассказ про собаку"),
    (8632, "example_en", "He throws in a remark",
     "May I just add something to that?",
     "в немецком вопрос «мне можно», а не рассказ про него"),
    (8632, "example_tr", "Bir yorum arasına sıkıştırıyor",
     "Buna kısaca bir şey ekleyebilir miyim?",
     "в немецком вопрос «мне можно», а не рассказ про него"),
    (8632, "example_uk", "Він вставляє зауваження",
     "Чи можу я коротко щось додати?",
     "в немецком вопрос «мне можно», а не рассказ про него"),
    (8973, "example_en",
     "He practices his profession very conscientiously",
     "What profession would you like to have later?",
     "в немецком вопрос «ты» о будущем"),
    (8973, "example_tr",
     "O, mesleğini çok dikkatli bir şekilde uyguluyor",
     "İleride hangi mesleği yapmak istiyorsun?",
     "в немецком вопрос «ты» о будущем"),
    (8973, "example_uk", "Він здійснює свою роботу дуже сумлінно",
     "Яку професію ти хочеш мати згодом?",
     "в немецком вопрос «ты» о будущем"),
    (9473, "example_en", "Mom reads me a story aloud",
     "Can you read the letter to me?",
     "в немецком просьба-вопрос про письмо"),
    (9473, "example_tr", "Anne bana bir hikaye okuyor",
     "Mektubu bana okuyabilir misin?",
     "в немецком просьба-вопрос про письмо"),
    (9473, "example_uk", "Мама читає мені історію вголос",
     "Можеш прочитати мені листа?",
     "в немецком просьба-вопрос про письмо"),
    (12203, "example_en", "Let's play a game of chess",
     "Shall we play a game of chess?", "в немецком это вопрос"),
    (12203, "example_tr", "Satranç oyunu oynayalım",
     "Bir satranç oyunu oynayalım mı?", "в немецком это вопрос"),
    (12203, "example_uk", "Давай зіграємо партію в шахи",
     "Зіграємо партію в шахи?", "в немецком это вопрос"),
    (12206, "example_en", "The kids run around in the park all day",
     "Do you have to walk around in your pyjamas?",
     "в немецком упрёк собеседнику, а не рассказ про детей"),
    (12206, "example_tr",
     "Çocuklar bütün gün parkta etrafta koşuyorlar",
     "Pijamayla dolaşmak zorunda mısın?",
     "в немецком упрёк собеседнику, а не рассказ про детей"),
    (12206, "example_uk", "Діти бігали по парку весь день",
     "Ти мусиш ходити в піжамі?",
     "в немецком упрёк собеседнику, а не рассказ про детей"),
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
