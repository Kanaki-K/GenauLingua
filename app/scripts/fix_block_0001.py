"""
Сплошная вычитка, блок 1: ряды 1–100 по рангу частотности (id 422…13287).

Это сотня самых частых слов базы — их видит каждый ученик на каждом уровне.
Вычитаны руками, без API. Критерии — в REVIEW_CRITERIA.md.

ЧТО ЗДЕСЬ ОКАЗАЛОСЬ. Служебные слова, похоже, никогда не вычитывались: из
ста рядов замечания в шестидесяти, и почти все одного вида — **перевод
примера переводит другую фразу**. Немецкий «Ich bin in der Stadt», а
английский «The milk is in the fridge»; немецкий «Ich gebe dem Kind das
Buch», а турецкий «Утром я рано иду в школу». Слово в примере стоит
правильное, поэтому формальные проверки проходят мимо: example_quality
смотрит, есть ли слово, а не о том ли фраза.

Отдельные находки, которые стоит знать:

* `sich` — ошибка в немецком эталоне: «Sie wascht sich» вместо «wäscht».
  Эталон для пяти языков, и неверен он во всех сразу.
* `euch` — немецкий «Ich sage euch was?» с вопросительным знаком, хотя это
  утверждение, и все пять переводов — утверждения.
* `den` — в украинском вместо примера заметка про английский язык:
  «В англійській є означений артикль the».
* `mir` и `uns` — турецкие примеры «Bu benim», «Bu bizim» ставят родительный
  там, где всё слово про дательный. Форма учится не та, которой ряд посвящён.
* `hast` — «Ти маєш удачу»: по-украински так не говорят, нужно «Тобі щастить».
* `da` — языки разошлись: по-русски «Он здесь», по-украински «Він там».
  Один и тот же немецкий ряд.

    python -m app.scripts.fix_block_0001            # показать
    python -m app.scripts.fix_block_0001 --apply    # применить
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
    (836, "example_de",
     "Sie wascht sich",
     "Sie wäscht sich",
     "пропущен умлаут: «wascht» вместо «wäscht»"),
    (240, "example_de",
     "Ich sage euch was?",
     "Ich sage euch was",
     "это утверждение, вопросительный знак лишний"),

    # --- не пример, а заметка -------------------------------------------------
    (13227, "example_uk",
     "В англійській є означений артикль the",
     "Я бачу того чоловіка",
     "это не пример, а заметка про английский язык"),

    # --- учится не та грамматическая форма -----------------------------------
    (596, "example_tr",
     "Bu benim",
     "Bu bana ait",
     "«benim» — родительный, а весь ряд про дательный «mir»"),
    (962, "example_tr",
     "Bu bizim",
     "Bu bize ait",
     "«bizim» — родительный, а весь ряд про дательный «uns»"),

    # --- языки разошлись между собой -----------------------------------------
    (160, "example_en",
     "He is there",
     "He is here",
     "«da» здесь значит «на месте»; в русском «здесь», в украинском «там»"),
    (160, "example_uk",
     "Він там",
     "Він тут",
     "то же: немецкий ряд один, а языки переведены по-разному"),
    (160, "example_tr",
     "O orada",
     "O burada",
     "то же"),

    # --- пример переводит другую фразу ----------------------------------------
    (839, "example_en",
     "They come tomorrow",
     "They're coming by tomorrow",
     "по-английски так не говорят, и потеряно «зайдут»"),
    (839, "example_tr",
     "Onlar yarın geliyor",
     "Onlar yarın uğrayacak",
     "в немецком «зайдут» (vorbeikommen), а не просто «придут»"),

    (13213, "example_uk",
     "Я хочу бути лікарем",
     "Це моя машина",
     "пример про другое"),
    (13213, "example_tr",
     "Yarın hava güzel olur",
     "Bu benim arabam",
     "пример про другое"),

    (195, "example_en",
     "How are you",
     "Are you coming along tonight?",
     "пример про другое"),
    (195, "example_uk",
     "Ти йдеш зі мною?",
     "Ти йдеш з нами сьогодні ввечері?",
     "в немецком «с нами сегодня вечером»"),
    (195, "example_tr",
     "Sen nerede oturuyorsun?",
     "Bu akşam bizimle geliyor musun?",
     "пример про другое"),

    (180, "example_uk",
     "Ця сукня мені завелика",
     "Ця жінка мила",
     "пример про другое"),
    (180, "example_tr",
     "Bu çok güzel bir fikir",
     "Bu kadın çok hoş",
     "пример про другое"),

    (237, "example_en",
     "It's raining again outside",
     "It is cold outside",
     "в немецком холодно, а не дождь"),
    (237, "example_uk",
     "Це не моя парасолька",
     "На вулиці холодно",
     "пример про другое"),
    (237, "example_tr",
     "O bugün işe gelmedi",
     "Dışarıda hava soğuk",
     "пример про другое"),
    (237, "example_pl",
     "To jest mój nowy telefon",
     "Na dworze jest zimno",
     "пример про другое"),

    (174, "example_en",
     "I'll take that one, please",
     "The man is tall",
     "пример про другое"),
    (174, "example_uk",
     "Подай мені он той ніж",
     "Той чоловік високий",
     "пример про другое"),
    (174, "example_tr",
     "O benim en yakın arkadaşım",
     "O adam uzun boylu",
     "пример про другое"),

    (1077, "example_en",
     "This coffee is too hot",
     "I am going to the shop",
     "взято другое значение, чем в немецком примере"),
    (1077, "example_tr",
     "Bugün çok fazla kahve içtim",
     "Dükkâna gidiyorum",
     "взято другое значение, чем в немецком примере"),

    (13223, "example_en",
     "I bought a new phone today",
     "I have a book",
     "пример про другое"),
    (13223, "example_uk",
     "Мені потрібен один квиток, будь ласка",
     "У мене є одна книга",
     "пример про другое"),
    (13223, "example_pl",
     "Mam jeden bilet więcej",
     "Mam jedną książkę",
     "пример про другое"),

    (431, "example_en",
     "The milk is in the fridge",
     "I am in the city",
     "пример про другое"),
    (431, "example_uk",
     "Поклади молоко в холодильник",
     "Я в місті",
     "пример про другое"),
    (431, "example_tr",
     "Süt buzdolabının içinde",
     "Ben şehirdeyim",
     "пример про другое"),

    (597, "example_tr",
     "Ailem ile tatile gidiyoruz",
     "Seninle gidiyorum",
     "в немецком «с тобой»"),

    (13227, "example_tr",
     "Kapıyı kapat lütfen",
     "O adamı görüyorum",
     "пример про другое"),
    (13227, "example_pl",
     "Tego pana nie znam",
     "Widzę tego mężczyznę",
     "пример про другое"),

    (1320, "example_tr",
     "Geldiğini kimseye söylemedim",
     "Senin geleceğini biliyorum",
     "в немецком «я знаю, что ты придёшь»"),

    (13233, "example_uk",
     "Одна дівчина питала про тебе",
     "Це якась кішка",
     "пример про другое"),

    (13235, "example_en",
     "He has hunger",
     "He is hungry",
     "по-английски так не говорят"),
    (13235, "example_uk",
     "Він має нову машину",
     "Він голодний",
     "пример про другое"),
    (13235, "example_tr",
     "Küçük bir eve sahip olmak istiyorum",
     "O aç",
     "пример про другое"),
    (13235, "example_pl",
     "On ma nowy samochód",
     "On jest głodny",
     "пример про другое"),

    (366, "example_uk",
     "Ти маєш гроші з собою?",
     "У мене є питання",
     "пример про другое"),

    (13238, "example_uk",
     "У мене є старший брат",
     "Ми втомилися",
     "пример про другое"),
    (13238, "example_tr",
     "Onlar sonunda çok mutlu oldular",
     "Biz yorgunuz",
     "пример про другое"),

    (991, "example_tr",
     "Bu film hakkında ne düşünüyorsun?",
     "Bu benden",
     "пример про другое"),

    (1026, "example_tr",
     "Eğer istersen sana yardım ederim",
     "Yağmur yağarsa evde kalırım",
     "пример про другое"),

    (13248, "example_uk",
     "Я хочу бути лікарем",
     "Я Анна",
     "пример про другое"),
    (13248, "example_tr",
     "Ben bugün çok mutluyum",
     "Ben Anna'yım",
     "пример про другое"),
    (13248, "example_pl",
     "Jestem Anna i mieszkam tutaj",
     "Jestem Anna",
     "добавлено «и живу здесь», чего в немецком нет"),

    (664, "example_uk",
     "У мене тільки п'ять хвилин",
     "Я вчу тільки німецьку",
     "пример про другое"),

    (13251, "example_pl",
     "Mam jednego brata",
     "Kupuję jedno jabłko",
     "пример про другое"),

    (836, "example_en",
     "He cut himself while shaving",
     "She washes herself",
     "пример про другое"),
    (836, "example_uk",
     "Подивись на себе у дзеркало",
     "Вона миється",
     "пример про другое"),

    (13254, "example_en",
     "I have two brothers",
     "You are lucky",
     "пример про другое"),
    (13254, "example_tr",
     "Benim bir kedim var",
     "Şanslısın",
     "пример про другое"),

    (13255, "example_uk",
     "Передай це тому чоловікові біля вікна",
     "Я даю дитині книгу",
     "пример про другое"),
    (13255, "example_tr",
     "Sabah erken okula gidiyorum",
     "Çocuğa kitabı veriyorum",
     "пример про другое"),
    (13255, "example_pl",
     "Daj to temu chłopcu",
     "Daję dziecku książkę",
     "пример про другое"),

    (13256, "example_tr",
     "Bunu tek başına yapabilir misin?",
     "Yüzebilirim",
     "пример про другое"),

    (362, "example_en",
     "That is good",
     "That tastes good",
     "в немецком «на вкус» — это другое значение"),
    (362, "example_uk",
     "Це добре",
     "Це смачно",
     "в немецком «на вкус»"),
    (362, "example_tr",
     "Bu iyi",
     "Bu lezzetli",
     "в немецком «на вкус»"),

    (827, "example_en",
     "I want to be a doctor",
     "I want to be on time tomorrow",
     "пример про другое"),
    (827, "example_uk",
     "Я хочу бути лікарем",
     "Я хочу завтра бути пунктуальним",
     "пример про другое"),
    (827, "example_tr",
     "Büyüyünce doktor olmak istiyorum",
     "Yarın tam zamanında olmak istiyorum",
     "пример про другое"),

    (13, "example_tr",
     "Çocukken bu bahçede oynardık",
     "Ben kardeşimden büyüğüm",
     "взято другое значение, чем в немецком примере"),

    (13262, "example_en",
     "Just wait a minute, please",
     "Come here a moment",
     "пример про другое"),
    (13262, "example_tr",
     "Bana bir bardak su ver",
     "Hele buraya gel",
     "пример про другое"),

    (165, "example_tr",
     "Önce yemek yiyelim, sonra gideriz",
     "O zaman üçe doğru gelirim",
     "пример про другое"),

    (13265, "example_pl",
     "Jesteśmy w domu",
     "Jestem w domu",
     "в немецком «я», а не «мы»"),

    (13266, "example_en",
     "It becomes dark early in winter",
     "It will be cold tomorrow",
     "пример про другое"),
    (13266, "example_uk",
     "На вулиці вже стає темно",
     "Завтра буде холодно",
     "пример про другое"),
    (13266, "example_pl",
     "Na dworze staje się ciemno",
     "Jutro będzie zimno",
     "пример про другое"),

    (13269, "example_pl",
     "Nie mam na to żadnej ochoty",
     "Nie mam czasu",
     "пример про другое"),

    (669, "example_uk",
     "Тобі чай або каву?",
     "Кава або чай",
     "пример про другое"),

    (567, "example_en",
     "One never knows what might happen",
     "You can park here",
     "пример про другое"),
    (567, "example_tr",
     "O çok iyi bir insan",
     "Burada park edilebilir",
     "взято другое значение: «человек» вместо безличного «можно»"),

    (1028, "example_en",
     "She wants to become a doctor",
     "I will soon be a father",
     "пример про другое"),
    (1028, "example_uk",
     "Стає темно",
     "Я скоро стану батьком",
     "пример про другое"),
    (1028, "example_tr",
     "Hava kararıyor",
     "Yakında baba olacağım",
     "пример про другое"),

    (527, "example_en",
     "I can cook well",
     "We can eat together tomorrow",
     "пример про другое"),
    (527, "example_uk",
     "Я можу тобі допомогти",
     "Ми можемо завтра поїсти разом",
     "пример про другое"),
    (527, "example_tr",
     "İyi yemek yapabilirim",
     "Yarın birlikte yemek yiyebiliriz",
     "пример про другое"),

    (1123, "example_tr",
     "Pastanın hepsini yemiş",
     "Herkes burada",
     "взято другое значение: «весь торт» вместо «все здесь»"),

    (319, "example_uk",
     "Мені треба йти додому",
     "Я йду гуляти",
     "пример про другое"),

    (13286, "example_uk",
     "Я допоміг одному хлопцю з валізою",
     "Я говорю з одним другом",
     "пример про другое"),

    # --- неестественно сказано ------------------------------------------------
    (49, "translation_ru",
     "на, в, на тему о",
     "на, в, на тему",
     "«на тему о» — неграмотно"),
    (836, "example_ru",
     "Она моет себя",
     "Она моется",
     "«моет себя» — калька, по-русски так не говорят"),
    (13254, "example_ru",
     "Тебе везёт, удача у тебя есть",
     "Тебе везёт",
     "вторая половина — пересказ первой"),
    (13254, "example_uk",
     "Ти маєш удачу",
     "Тобі щастить",
     "«мати удачу» по-украински не говорят"),
    (13269, "example_ru",
     "У меня нет никакого времени",
     "У меня нет времени",
     "«никакого» здесь лишнее"),

    # --- потеряно или добавлено против немецкого -------------------------------
    (13254, "example_pl",
     "Masz szczęście do ludzi",
     "Masz szczęście",
     "«do ludzi» в немецком нет"),
    (13256, "example_pl",
     "Umiem pływać od dziecka",
     "Umiem pływać",
     "«od dziecka» в немецком нет"),
    (13258, "example_pl",
     "Znam go od dawna",
     "Znam go dobrze",
     "в немецком «хорошо», а не «давно»"),
    (173, "example_uk",
     "Я вдома, тому що йде дощ",
     "Я залишаюся вдома, тому що йде дощ",
     "потерян глагол «залишаюся»"),
    (987, "example_en",
     "Maybe we will come",
     "Maybe we will come tomorrow",
     "потеряно «завтра»"),
    (987, "example_uk",
     "Можливо, ми прийдемо",
     "Можливо, ми прийдемо завтра",
     "потеряно «завтра»"),
    (987, "example_tr",
     "Belki geliriz",
     "Belki yarın geliriz",
     "потеряно «завтра»"),
    (6168, "example_uk",
     "Приходь швидко!",
     "Заходь швидше!",
     "в немецком «herein» — внутрь"),
    (6168, "example_tr",
     "Çabuk gel",
     "Çabuk içeri gel!",
     "потеряно «внутрь» и восклицательный знак"),

    # --- время и вид глагола ---------------------------------------------------
    (564, "example_uk",
     "Я це зроблю",
     "Я це роблю",
     "в немецком настоящее время"),

    # --- «ты» вместо «Вы» и потерянный вопросительный знак --------------------
    (1035, "example_uk",
     "Як Ви почуваєтесь",
     "Як ти почуваєшся",
     "в немецком «dir» — ты, а не Вы"),
    (1035, "example_tr",
     "Nasılsınız",
     "Nasılsın",
     "в немецком «dir» — ты, а не Вы"),
    (239, "example_uk",
     "Бажаєте щось випити",
     "Хочеш щось випити?",
     "в немецком «du» — ты; и потерян вопросительный знак"),
    (239, "example_tr",
     "Bir şey içmek ister misiniz",
     "Bir şey içmek ister misin?",
     "в немецком «du» — ты; и потерян вопросительный знак"),
    (946, "example_en",
     "What do we do",
     "What do we do here?",
     "потеряно «тут» и вопросительный знак"),
    (946, "example_uk",
     "Що ми робимо",
     "Що ми тут робимо?",
     "потеряно «тут» и вопросительный знак"),
    (946, "example_tr",
     "Ne yapıyoruz",
     "Burada ne yapıyoruz?",
     "потеряно «тут» и вопросительный знак"),
    (1027, "example_en",
     "Who is that",
     "Who is that?",
     "потерян вопросительный знак"),
    (1027, "example_uk",
     "Хто це",
     "Хто це?",
     "потерян вопросительный знак"),
    (1027, "example_tr",
     "Bu kim",
     "Bu kim?",
     "потерян вопросительный знак"),
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
