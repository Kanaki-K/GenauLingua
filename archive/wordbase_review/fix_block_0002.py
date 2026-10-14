"""
Сплошная вычитка, блок 2: ряды 101–200 по рангу частотности.

Правки руками, без API. Критерии — в REVIEW_CRITERIA.md.

Картина та же, что в блоке 1: главный дефект — перевод примера переводит
другую фразу. Немецкий «Ich hab keinen Hunger mehr», а английский «There's
no milk left in the fridge»; немецкий «Wir gehen ins Theater», а турецкий
«Брось сахар в чай».

Отдельные находки:

* `wirst` — немецкий «Du wirst das schon schaffen», а украинский «Ти будеш
  каву чи чай?». Из пяти переводов в этом ряду верных не было ни одного.
* `des` — к русскому примеру приклеено пояснение: «Машина этого мужчины
  красная — здесь нужен артикль родительного падежа». Сплошной поиск этого
  не видел: его шаблон ищет тире в начале строки.
* `wegen` — «З-за дощу»: русизм, в украинском «через».
* `leid` — в украинском женский род («спізнилася»), во всех остальных
  языках мужской.
* `dieser` — в английском «Were going» без апострофа.
* `Na`, `Ach` — в самих немецких примерах пропущен апостроф: «gehts»,
  «versteh ichs».
* `ob` — в украинском значении стоит «якби». Это «если бы», а «ob» — «чи».

    python -m app.scripts.fix_block_0002            # показать
    python -m app.scripts.fix_block_0002 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# (id, колонка, что стоит сейчас, на что менять, зачем)
FIXES: list[tuple[int, str, str, str, str]] = [

    # --- ошибки в самом немецком эталоне -------------------------------------
    (13810, "example_de",
     "Na, wie gehts dir denn",
     "Na, wie geht's dir denn",
     "пропущен апостроф: «gehts» вместо «geht's»"),
    (13815, "example_de",
     "Ach so, jetzt versteh ichs!",
     "Ach so, jetzt versteh ich's!",
     "пропущен апостроф: «ichs» вместо «ich's»"),
    (13295, "example_de",
     "Ist das dein Handy",
     "Ist das dein Handy?",
     "это вопрос, знак потерян — и он есть во всех переводах, кроме польского"),
    (663, "example_de",
     "Was machen wir nun",
     "Was machen wir nun?",
     "это вопрос, знак потерян"),

    # --- пояснение, приклеенное к примеру ------------------------------------
    (13292, "example_ru",
     "Машина этого мужчины красная — здесь нужен артикль родительного падежа",
     "Машина этого мужчины красная",
     "к примеру приклеено пояснение через тире"),

    # --- слово, которого нет в языке, и русизмы ------------------------------
    (2089, "example_uk",
     "З-за дощу я залишаюсь дома",
     "Через дощ я залишаюся вдома",
     "«з-за» — русизм, по-украински «через»; и «дома» вместо «вдома»"),
    (1738, "translation_uk",
     "чи, якби",
     "чи",
     "«якби» — это «если бы», а «ob» — «чи»"),
    (486, "example_tr",
     "Bu bana net",
     "Bu benim için açık",
     "по-турецки так не говорят"),
    (13314, "example_tr",
     "Hediye babadan",
     "Bu hediye babamdan",
     "фраза без подлежащего и связки"),
    (1666, "example_tr",
     "Kız çocuk bahçede oynuyor",
     "Kız bahçede oynuyor",
     "«kız çocuk» без аффикса — неграмотно"),
    (13320, "example_tr",
     "Çok insan pizzayı sever",
     "Birçok insan pizzayı sever",
     "«çok insan» вместо «birçok insan»"),

    # --- род, лицо и вежливая форма -------------------------------------------
    (10022, "example_uk",
     "Мені шкода, що я спізнилася",
     "Мені шкода, що я спізнився",
     "женский род, а во всех остальных языках мужской"),
    (539, "example_uk",
     "Будь ласка, залиште це",
     "Залиш це, будь ласка",
     "в немецком «Lass» — ты, а не Вы"),
    (539, "example_tr",
     "Onu bırakın, lütfen",
     "Onu bırak, lütfen",
     "в немецком «Lass» — ты, а не Вы"),
    (395, "example_uk",
     "Можу Вам допомогти",
     "Чи можу я тобі допомогти?",
     "в немецком «dir» — ты; и потерян вопросительный знак"),
    (395, "example_tr",
     "Size yardım edebilir miyim",
     "Sana yardım edebilir miyim?",
     "в немецком «dir» — ты; и потерян вопросительный знак"),
    (1857, "example_tr",
     "Ne zamandan beri burada yaşıyorsunuz",
     "Ne zamandan beri burada yaşıyorsun?",
     "в немецком «du» — ты; и потерян вопросительный знак"),
    (13319, "example_en",
     "We should go to sleep earlier",
     "You should go to sleep earlier",
     "в немецком «du», а не «мы»"),
    (13319, "example_uk",
     "Ми повинні лягати спати раніше",
     "Тобі слід лягати спати раніше",
     "в немецком «du», а не «мы»"),
    (663, "example_uk",
     "Що ти тепер робиш?",
     "Що ми тепер робимо?",
     "в немецком «мы», а не «ты»"),

    # --- потерянный вопросительный знак ---------------------------------------
    (13294, "example_uk",
     "Що ти хочеш їсти",
     "Що ти хочеш їсти?",
     "потерян вопросительный знак"),
    (13294, "example_pl",
     "Co chcesz dzisiaj zjeść",
     "Co chcesz zjeść?",
     "потерян знак, и «dzisiaj» в немецком нет"),
    (13295, "example_pl",
     "Czy to twój telefon",
     "Czy to twój telefon?",
     "потерян вопросительный знак"),
    (663, "example_en",
     "What do we do now",
     "What do we do now?",
     "потерян вопросительный знак"),
    (663, "example_tr",
     "Şimdi ne yapıyoruz",
     "Şimdi ne yapıyoruz?",
     "потерян вопросительный знак"),
    (13300, "example_en",
     "What do you mean by that",
     "What do you mean by that?",
     "потерян вопросительный знак"),
    (13300, "example_pl",
     "Co masz na myśli",
     "Co masz na myśli?",
     "потерян вопросительный знак"),
    (370, "example_en",
     "Hello, how are you",
     "Hello, how are you?",
     "потерян вопросительный знак"),
    (18564, "example_ru",
     "Как долго ты уже ждешь",
     "Как долго ты уже ждёшь?",
     "потерян вопросительный знак и буква «ё»"),
    (18564, "example_uk",
     "Як довго ти вже чекаєш",
     "Як довго ти вже чекаєш?",
     "потерян вопросительный знак"),
    (13317, "example_en",
     "Were going on vacation with this car",
     "We're going on vacation with this car",
     "«Were» без апострофа — другое слово"),

    # --- пример переводит другую фразу ----------------------------------------
    (1046, "example_en",
     "I do not know that",
     "You must know that",
     "в немецком «ты же должен это знать»"),
    (1046, "example_uk",
     "Я цього не знаю",
     "Ти ж мусиш це знати",
     "в немецком «ты же должен это знать»"),
    (1046, "example_tr",
     "Bunu bilmiyorum",
     "Bunu bilmen gerekir",
     "в немецком «ты же должен это знать»"),

    (629, "example_uk",
     "Мушу завтра рано вставати",
     "Мушу працювати",
     "в немецком «я должен работать»"),

    (655, "example_tr",
     "Onu asla affetmeyeceğim",
     "Oraya hiç gitmedim",
     "пример про другое"),

    (1014, "example_en",
     "Which way to the station?",
     "The way to the beach is short",
     "пример про другое"),
    (1014, "example_uk",
     "Дорога до школи займає десять хвилин",
     "Дорога до пляжу коротка",
     "пример про другое"),
    (1014, "example_tr",
     "Bu yol doğruca sahile çıkıyor",
     "Sahile giden yol kısa",
     "в немецком дорога короткая, а не «ведёт прямо»"),

    (541, "example_en",
     "She lives in Berlin",
     "We like living in this city",
     "пример про другое"),
    (541, "example_uk",
     "Я живу в цьому місті",
     "Нам подобається жити в цьому місті",
     "в немецком «мы охотно живём»"),
    (541, "example_tr",
     "Berlin’de yaşıyor",
     "Bu şehirde yaşamayı seviyoruz",
     "пример про другое"),

    (13293, "example_tr",
     "Çantam sandalyenin yanında duruyor",
     "Ben gardayım",
     "пример про другое"),
    (13293, "example_pl",
     "Czekam na dworcu",
     "Jestem na dworcu",
     "в немецком «я на вокзале», а не «жду»"),

    (1059, "example_en",
     "I want to eat",
     "We want to go swimming tomorrow",
     "пример про другое"),
    (1059, "example_uk",
     "Я хочу морозива",
     "Ми хочемо завтра піти плавати",
     "пример про другое"),
    (1059, "example_tr",
     "Yemek istiyorum",
     "Yarın yüzmeye gitmek istiyoruz",
     "пример про другое"),

    (305, "example_tr",
     "Saat tam üçte buluşalım",
     "Bu gayet iyi",
     "пример про другое"),

    (13810, "example_tr",
     "Hadi, acele et biraz!",
     "Ee, nasılsın",
     "пример про другое"),

    (13811, "example_uk",
     "Моя бабуся щиро вірить у Бога",
     "Ах Боже, я ж про це забув",
     "пример про другое"),

    (13300, "example_uk",
     "Що ти маєш на увазі?",
     "Що ти про це думаєш?",
     "потеряно «об этом»"),

    (13302, "example_uk",
     "Мені потрібні два квитки",
     "Мені потрібні дві булочки, будь ласка",
     "в немецком булочки, а не билеты"),
    (13302, "example_pl",
     "Kupiłem dwie bułki",
     "Potrzebuję dwie bułki, proszę",
     "в немецком «мне нужны», а не «я купил»"),

    (13303, "example_pl",
     "Codziennie idę do szkoły",
     "Idę do szkoły",
     "«codziennie» в немецком нет"),

    (749, "example_en",
     "We talk about it",
     "We talk about the problem",
     "потеряна «проблема»"),
    (749, "example_uk",
     "Ми про це розмовляємо",
     "Ми розмовляємо про цю проблему",
     "потеряна «проблема»"),
    (749, "example_tr",
     "Bunun hakkında konuşuyoruz",
     "Bu problem hakkında konuşuyoruz",
     "потеряна «проблема»"),
    (1091, "example_uk",
     "Ми говоримо про це",
     "Ми говоримо про цю проблему",
     "потеряна «проблема»"),
    (1091, "example_tr",
     "Bunun hakkında konuşuyoruz",
     "Bu problem hakkında konuşuyoruz",
     "потеряна «проблема»"),

    (6186, "example_en",
     "Get out of my room!",
     "Come on, let's go outside",
     "в немецком «пойдём выйдем», а не «вон из комнаты»"),
    (6186, "example_uk",
     "Вийдемо назовні, тут душно",
     "Ходімо, вийдемо назовні",
     "«тут душно» в немецком нет"),

    (13306, "example_en",
     "There's no milk left in the fridge",
     "I'm not hungry any more",
     "пример про другое"),
    (13306, "example_ru",
     "Я больше не голоден, никакого аппетита",
     "Я больше не голоден",
     "вторая половина — пересказ первой"),
    (13306, "example_uk",
     "Я не маю ніякого бажання йти",
     "Я більше не голодний",
     "пример про другое"),
    (13306, "example_tr",
     "Hiçbir fikrim yok",
     "Artık hiç aç değilim",
     "пример про другое"),
    (13306, "example_pl",
     "Nie mam żadnego pomysłu",
     "Nie jestem już głodny",
     "пример про другое"),

    (1738, "example_tr",
     "Acaba yarın gelir mi?",
     "Onun gelip gelmeyeceğini bilmiyorum",
     "в немецком «я не знаю, придёт ли он»"),

    (1860, "example_en",
     "Don't help me, I'll do it myself",
     "I'll do it myself",
     "первая половина в немецком отсутствует"),
    (1860, "example_tr",
     "Odamı kendim temizledim",
     "Bunu kendim yapıyorum",
     "пример про другое"),

    (1040, "example_tr",
     "Neden bugün okula gelmedin?",
     "Neden gelmiyorsun?",
     "школы в немецком нет"),

    (671, "example_tr",
     "Çayı şeker olmadan içerim",
     "Kahveyi şekersiz içerim",
     "в немецком кофе, а не чай"),

    (13309, "example_uk",
     "Інші вже там",
     "Інші вже тут",
     "«schon da» — уже здесь; в русском «здесь», в украинском было «там»"),
    (13309, "example_pl",
     "Inne dzieci już poszły do domu",
     "Inni są już tutaj",
     "пример про другое"),

    (637, "example_uk",
     "Ніч була тиха й тепла",
     "Вночі ми спимо",
     "пример про другое"),

    (13310, "example_en",
     "You will manage it, don't worry",
     "You will manage it",
     "«не волнуйся» в немецком нет"),
    (13310, "example_ru",
     "Ты обязательно справишься, всё станет хорошо",
     "Ты обязательно справишься",
     "вторая половина в немецком отсутствует"),
    (13310, "example_uk",
     "Ти будеш каву чи чай?",
     "Ти обов'язково справишся",
     "пример про другое"),
    (13310, "example_tr",
     "Yarın çok sıcak olacak",
     "Bunu başaracaksın",
     "пример про другое"),
    (13310, "example_pl",
     "Z czasem staniesz się lepszy",
     "Dasz sobie radę",
     "пример про другое"),

    (271, "example_uk",
     "Я ніколи не знаходжу свої окуляри",
     "Я не можу знайти ключ",
     "пример про другое"),

    (18564, "example_tr",
     "Saçların çok uzun olmuş",
     "Ne zamandır bekliyorsun?",
     "пример про длинные волосы, а немецкий про «как долго ждёшь»"),

    (13311, "example_uk",
     "Це подарунок моєму братові",
     "Це друг мого брата",
     "пример про другое"),
    (13311, "example_pl",
     "To prezent dla mojego brata",
     "To kolega mojego brata",
     "пример про другое"),

    (13313, "example_tr",
     "Şekeri çayın içine at",
     "Tiyatroya gidiyoruz",
     "пример про другое"),

    (13815, "example_uk",
     "Ах, тепер розумію!",
     "Ах ось як, тепер я розумію!",
     "потеряно «вот оно что»"),

    (310, "example_en",
     "Give me the newspaper",
     "Can you give me some water?",
     "в немецком вопрос про воду"),
    (310, "example_uk",
     "Мама любить давати поради",
     "Можеш дати мені води?",
     "пример про другое"),
    (310, "example_tr",
     "Bana gazeteyi ver",
     "Bana su verebilir misin?",
     "в немецком вопрос про воду"),
    (310, "example_pl",
     "Daj mi szklankę wody",
     "Możesz mi dać wody?",
     "в немецком это вопрос, а не просьба"),

    (13315, "example_pl",
     "Zjadłem z tego połowę",
     "Kupiłem pizzę i zjadłem już z niej połowę",
     "потеряна первая половина фразы"),

    (161, "example_tr",
     "Bunun için özür dilerim",
     "Ben bundan yanayım",
     "в немецком «я за это», а не «извините за это»"),

    (13317, "example_uk",
     "Цей хліб ще свіжий",
     "Цією машиною ми поїдемо у відпустку",
     "пример про другое"),

    (13319, "example_tr",
     "Daha çok çalışmalısın",
     "Daha erken yatmalısın",
     "в немецком про сон, а не про работу"),

    (382, "example_uk",
     "Наш будинок стоїть біля парку",
     "Я вдома",
     "пример про другое"),
    (382, "example_tr",
     "Yeni bir ev arıyoruz",
     "Ben evdeyim",
     "пример про другое"),

    (1136, "example_en",
     "She has a real fear of heights",
     "I am afraid of spiders",
     "в немецком пауки и «я», а не высота и «она»"),
    (1136, "example_uk",
     "У мене страх висоти",
     "Я боюся павуків",
     "в немецком пауки, а не высота"),

    (238, "example_uk",
     "Діти їдять суп на обід",
     "Ми їмо о дванадцятій",
     "пример про другое"),
    (238, "example_pl",
     "Jem śniadanie o ósmej",
     "Jemy o dwunastej",
     "пример про другое"),

    (6206, "example_uk",
     "Заходь всередину, тут тепло",
     "Заходь всередину, на вулиці холодно",
     "в немецком «на улице холодно», а не «тут тепло»"),
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
