"""
Сплошная вычитка, блок 3: ряды 201–300 по рангу частотности.

Правки руками, без API. Критерии — в REVIEW_CRITERIA.md.

Находки блока:

* `eigentlich` — в украинском «робишь» с мягким знаком по-русски. Такого
  слова в украинском нет, правильно «робиш».
* `töten` — «Вбивати муху нехорошо»: «нехорошо» тоже русское.
* `Art` — в украинском взято другое значение слова: немецкий про «способ
  это сделать», а перевод «з нашого балкона чудовий вид на море».
* `drin` — немецкий спрашивает, что в пакете, а из пяти переводов про пакет
  говорит только русский.
* `Name` — немецкий «Mein Name ist Anna Weber», английский и украинский
  спрашивают «как тебя зовут», турецкий «я забыл твоё имя».
* `eines` — в немецком примере стоит «eins», а ряд про форму «eines».
* `fast` и `leid` — украинский женского рода там, где все остальные языки
  мужского.
* Потерянный вопросительный знак — двадцать ячеек. Немецкий спрашивает,
  перевод выглядит утверждением.

    python -m app.scripts.fix_block_0003            # показать
    python -m app.scripts.fix_block_0003 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# (id, колонка, что стоит сейчас, на что менять, зачем)
FIXES: list[tuple[int, str, str, str, str]] = [

    # --- ошибка в немецком эталоне -------------------------------------------
    (13325, "example_de",
     "Das ist eins meiner Lieblingsbücher",
     "Das ist eines meiner Lieblingsbücher",
     "ряд про форму «eines», а в примере стоит «eins»"),

    # --- русизмы и слова, которых нет в языке ---------------------------------
    (13821, "example_uk",
     "А що ти, власне, робишь?",
     "Що ти, власне, робиш?",
     "«робишь» — русское написание; и «А» в немецком нет"),
    (6226, "example_uk",
     "Вбивати муху нехорошо",
     "Вбивати муху — це недобре",
     "«нехорошо» — русское слово"),
    (191, "example_uk",
     "Ззовні йде дощ, тому ми краще залишаємося вдома",
     "Надворі йде дощ, тому ми краще залишаємося вдома",
     "«ззовні» о погоде по-украински не говорят"),
    (191, "example_ru",
     "Снаружи идёт дождь, поэтому мы лучше остаёмся дома",
     "На улице идёт дождь, поэтому мы лучше остаёмся дома",
     "«снаружи идёт дождь» по-русски не говорят"),
    (10027, "example_uk",
     "Я краще п'ю чай, ніж каву",
     "Я краще питиму чай, ніж каву",
     "«краще п'ю» — незаконченная конструкция"),
    (475, "example_en",
     "I know him for a long time",
     "I have known him for a long time",
     "по-английски здесь нужен перфект"),
    (6226, "example_en",
     "Killing the fly is not good",
     "Killing a fly is not good",
     "в немецком любая муха, а не конкретная"),
    (172, "example_tr",
     "Bunu iyi olduğunu düşünüyorum",
     "Bunun iyi olduğunu düşünüyorum",
     "неверный падеж: нужен родительный"),
    (1311, "example_en",
     "I was in on it",
     "I was there too",
     "«to be in on it» значит быть в сговоре, а «dabei» — присутствовать"),

    # --- род --------------------------------------------------------------------
    (257, "example_uk",
     "Я майже готова",
     "Я майже готовий",
     "женский род, а во всех остальных языках мужской"),

    # --- вежливая форма и лицо --------------------------------------------------
    (1004, "example_tr",
     "Sizi bekliyorum",
     "Seni bekliyorum",
     "в немецком «auf dich» — тебя, а не Вас"),
    (284, "example_uk",
     "У Вас є питання",
     "У тебе є питання?",
     "в немецком «du» — ты; и потерян вопросительный знак"),
    (284, "example_tr",
     "Bir sorunuz var mı",
     "Bir soru var mı?",
     "в немецком «du» — ты; и потерян вопросительный знак"),
    (170, "example_tr",
     "Bununla birlikte ne istersiniz",
     "Bununla ne istersin?",
     "в немецком «du» — ты; и потерян вопросительный знак"),

    # --- потерянный вопросительный знак ----------------------------------------
    (13326, "example_uk",
     "Можна мені тут палити",
     "Можна мені тут палити?",
     "потерян вопросительный знак"),
    (13326, "example_pl",
     "Czy mogę tu palić",
     "Czy mogę tu palić?",
     "потерян вопросительный знак"),
    (1473, "example_en",
     "Do you have enough money",
     "Do you have enough money?",
     "потерян вопросительный знак"),
    (1473, "example_uk",
     "У тебе достатньо грошей",
     "У тебе достатньо грошей?",
     "потерян вопросительный знак"),
    (1473, "example_tr",
     "Yeterince paran var mı",
     "Yeterince paran var mı?",
     "потерян вопросительный знак"),
    (13817, "example_en",
     "Damn, where are my keys",
     "Damn, where are my keys?",
     "потерян вопросительный знак"),
    (1002, "example_tr",
     "Ne zaman geliyorsun",
     "Ne zaman geliyorsun?",
     "потерян вопросительный знак"),
    (13821, "example_en",
     "What are you actually doing",
     "What are you actually doing?",
     "потерян вопросительный знак"),
    (13821, "example_tr",
     "Aslında ne yapıyorsun",
     "Aslında ne yapıyorsun?",
     "потерян вопросительный знак"),
    (13821, "example_pl",
     "Co ty właściwie robisz",
     "Co ty właściwie robisz?",
     "потерян вопросительный знак"),
    (13337, "example_uk",
     "Де ваші книги",
     "Де ваші книги?",
     "потерян вопросительный знак"),
    (13337, "example_tr",
     "Sizin kitaplarınız nerede",
     "Sizin kitaplarınız nerede?",
     "потерян вопросительный знак"),
    (13337, "example_pl",
     "Gdzie są wasze książki",
     "Gdzie są wasze książki?",
     "потерян вопросительный знак"),
    (13343, "example_uk",
     "Ти коли-небудь там був",
     "Ти коли-небудь там був?",
     "потерян вопросительный знак"),
    (13343, "example_tr",
     "Hiç orada bulundun mu",
     "Hiç orada bulundun mu?",
     "потерян вопросительный знак"),
    (13343, "example_pl",
     "Byłeś tam kiedykolwiek",
     "Byłeś tam kiedykolwiek?",
     "потерян вопросительный знак"),

    # --- пример переводит другую фразу ------------------------------------------
    (649, "example_uk",
     "Можеш брати мою машину",
     "Я беру газету",
     "пример про другое"),
    (649, "example_tr",
     "Her sabah otobüse biniyorum",
     "Gazeteyi alıyorum",
     "пример про другое"),

    (13326, "example_tr",
     "Sana yardım edebilirim",
     "Burada sigara içebilir miyim?",
     "пример про другое"),

    (345, "example_tr",
     "Ona hiç inanmıyorum",
     "Sanırım o geliyor",
     "в немецком «думаю, он придёт», а не «я ему не верю»"),

    (1573, "example_tr",
     "Çocuk futbol oynuyor",
     "Oğlan futbol oynuyor",
     "«çocuk» — ребёнок вообще, а Junge — мальчик"),
    (14891, "example_tr",
     "Oğlan bahçede top oynuyor",
     "Oğlanlar futbol oynuyor",
     "в немецком множественное число, и сада там нет"),

    (131, "example_uk",
     "Я потребую твоєї допомоги",
     "Мені потрібне нове пальто",
     "пример про другое"),

    (6212, "example_uk",
     "Я чекав на тебе цілий день",
     "Я чекав увесь час",
     "в немецком «всё время», а не «целый день»"),
    (6212, "example_tr",
     "Bütün gün evde oturduk",
     "Bütün bu süre boyunca bekledim",
     "пример про другое"),

    (608, "example_uk",
     "Зачекай момент, я вже йду",
     "Один момент, будь ласка",
     "пример про другое"),

    (400, "example_en",
     "Excuse me, Mister, you dropped this",
     "Mr Müller is here",
     "пример про другое"),
    (400, "example_tr",
     "Ahmet Bey biraz sonra gelecek",
     "Müller Bey burada",
     "пример про другое"),

    (1729, "example_uk",
     "Ніхто мені так і не подзвонив",
     "Нікого не було вдома",
     "пример про другое"),

    (1311, "example_uk",
     "Візьми парасольку із собою",
     "Я при цьому був",
     "пример про другое"),

    (251, "example_pl",
     "Cała rodzina je razem kolację",
     "Rodzina je razem",
     "«вся» и «ужин» в немецком отсутствуют"),

    (13817, "example_tr",
     "Lanet, anahtarlarım nerede",
     "Kahretsin, anahtarlarım nerede?",
     "«Lanet» отдельным словом не употребляется; и потерян знак"),

    (847, "example_ru",
     "Сын уже большой",
     "Сын высокий",
     "«groß» здесь рост: в остальных языках «высокий»"),
    (847, "example_tr",
     "Oğul büyük",
     "Oğul uzun boylu",
     "то же: рост, а не возраст"),

    (13331, "example_tr",
     "Ben de seninle geliyorum",
     "Doktordayım",
     "пример про другое"),
    (13331, "example_pl",
     "Jestem teraz u lekarza",
     "Jestem u lekarza",
     "«teraz» в немецком нет"),

    (88, "example_uk",
     "Обидві сестри вчаться разом",
     "Обоє дітей граються надворі",
     "в немецком дети играют на улице, а не сёстры учатся"),
    (88, "example_tr",
     "İkisi de dışarıda oynuyor",
     "İki çocuk da dışarıda oynuyor",
     "потеряны «дети»"),

    (330, "example_en",
     "I'll gladly help you with that",
     "I like drinking tea",
     "пример про другое"),

    (6222, "example_tr",
     "Bu cevap doğru mu, emin misin?",
     "Bu doğru",
     "в немецком утверждение «это правда», а не вопрос про ответ"),

    (170, "example_en",
     "I have nothing to add to that",
     "What would you like with it?",
     "в немецком вопрос «что ты хочешь к этому»"),
    (170, "example_uk",
     "Крім того, він завжди запізнюється",
     "Що ти хочеш до цього?",
     "пример про другое"),

    (172, "example_pl",
     "Myślę, że to dobry pomysł",
     "Myślę, że to dobrze",
     "«идея» в немецком отсутствует"),

    (13335, "example_pl",
     "Myślę o tym cały czas",
     "Nie mogę sobie tego przypomnieć",
     "в немецком «не могу вспомнить», а не «думаю об этом»"),

    (163, "example_uk",
     "Щира подяка за допомогу",
     "Дякую тобі",
     "в немецком «Dank dir» — спасибо тебе"),
    (163, "example_tr",
     "Yardım için çok teşekkürler",
     "Sana teşekkürler",
     "в немецком «Dank dir» — спасибо тебе"),

    (284, "example_en",
     "Do you have a question",
     "Do you have a question?",
     "потерян вопросительный знак"),

    (949, "example_en",
     "The clock shows three o'clock",
     "It is three o'clock",
     "в немецком «сейчас три часа», часы ничего не показывают"),
    (949, "example_uk",
     "Це третя година",
     "Зараз третя година",
     "«це третя година» — не о времени, а о предмете"),
    (949, "example_tr",
     "Saat üç gösteriyor",
     "Saat üç",
     "в немецком «сейчас три часа»"),

    (244, "example_uk",
     "Завтра ми їдемо на море",
     "Ми їдемо до Берліна",
     "пример про другое"),
    (244, "example_pl",
     "Jedziemy do Berlina samochodem",
     "Jedziemy do Berlina",
     "«на машине» в немецком нет"),

    (1493, "example_tr",
     "Bol şans",
     "Sana bol şans dilerim",
     "потеряно «желаю тебе»"),

    (74, "example_tr",
     "Yakında eve geliyor",
     "Yakında eve gelecek",
     "настоящее время вместо будущего"),

    (13338, "example_uk",
     "Я чекаю на це",
     "Я з нетерпінням чекаю на це",
     "потеряно «с нетерпением»"),
    (13338, "example_tr",
     "Ona sabırsızlanıyorum",
     "Bunu sabırsızlıkla bekliyorum",
     "по-турецки так не говорят"),

    (2206, "example_en",
     "What kind of music do you like?",
     "That's an interesting way to do it",
     "пример про другое"),
    (2206, "example_uk",
     "З нашого балкона чудовий вид на море",
     "Це цікавий спосіб це зробити",
     "взято другое значение: «вид» вместо «способ»"),
    (2206, "example_tr",
     "Sen ne tür müzik seversin?",
     "Bunu yapmanın ilginç bir yolu",
     "пример про другое"),

    (10035, "example_uk",
     "Чорт, я знову забув ключі",
     "Якого біса ти там робиш",
     "пример про другое"),
    (10035, "example_tr",
     "Şeytan gibi kurnaz bir adam",
     "Ne yapıyorsun orada, şeytan mı dürttü?",
     "пример про хитрого человека, а немецкий — ругательный вопрос"),

    (13342, "example_en",
     "I'll be inside soon",
     "What's in the bag?",
     "пример про другое"),
    (13342, "example_uk",
     "Всередині будинку тепло",
     "А що там усередині пакета?",
     "пример про другое"),
    (13342, "example_tr",
     "Birazdan içerde olacağım",
     "Poşetin içinde ne var?",
     "пример про другое"),
    (13342, "example_pl",
     "W środku było ciepło i cicho",
     "Co jest w środku torby?",
     "пример про другое"),

    (641, "example_en",
     "What is your name?",
     "My name is Anna Weber",
     "в немецком это не вопрос, а ответ"),
    (641, "example_uk",
     "Як твоє ім'я?",
     "Моє ім'я — Анна Вебер",
     "в немецком это не вопрос, а ответ"),
    (641, "example_tr",
     "İsmini unuttum, tekrar söyler misin?",
     "Benim adım Anna Weber",
     "пример про другое"),

    (1319, "example_en",
     "It rained; therefore we stayed home",
     "That's why I am here",
     "пример про другое"),
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
