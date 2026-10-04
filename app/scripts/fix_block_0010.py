"""
Сплошная вычитка, блоки 10 и 11: ряды 901–1100 по рангу частотности.

Находки:

* `Eier` — заголовок во множественном числе («die Eier»), а все пять
  переводов в единственном: «яйцо», «egg», «jajko». Примеры при этом
  говорят «три яйца». Переводы приведены к множественному.
* `Maul` — немецкий «Halt dein Maul» это грубое «закрой рот», а английский,
  украинский и турецкий рассказывают, как собака открывает пасть.
* `Fräulein` — немецкий пример объясняет, что так говорили прежде, а три
  языка обращаются к девушке.
* `au` — в английском «Ouch – Ouch, that hurts!»: слово приклеено к фразе
  через тире, след прежней правки.
* `Fleisch` — в английском «He doe's not eat meat»: апостроф внутри «does».
* `Mut` — в украинских значениях «смілвість», опечатка.
* `Reihe` — снова «сидю» вместо «сиджу»: то же, что в ряду `vorne`.
* `Hut`, `darüber` — в немецких примерах разговорные «'nen» и «drüber»,
  тогда как ряд про «einen» и «darüber».

    python -m app.scripts.fix_block_0010            # показать
    python -m app.scripts.fix_block_0010 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# (id, колонка, что стоит сейчас, на что менять, зачем)
FIXES: list[tuple[int, str, str, str, str]] = [

    # --- заголовок во множественном, переводы в единственном ------------------
    (11638, "translation_en", "egg", "eggs",
     "заголовок «die Eier» — множественное число"),
    (11638, "translation_ru", "яйцо", "яйца",
     "заголовок «die Eier» — множественное число"),
    (11638, "translation_uk", "яйце", "яйця",
     "заголовок «die Eier» — множественное число"),
    (11638, "translation_tr", "yumurta", "yumurtalar",
     "заголовок «die Eier» — множественное число"),
    (11638, "translation_pl", "jajko, jajo", "jajka",
     "заголовок «die Eier» — множественное число"),

    # --- русизмы, опечатки, неверные значения ---------------------------------
    (14929, "translation_uk", "чоловік, муж", "чоловік",
     "«муж» — русизм"),
    (801, "translation_uk", "біль, страдання", "біль, страждання",
     "«страдання» — русизм, по-украински «страждання»"),
    (10127, "translation_uk", "смілвість, смілість, мужність, відвага",
     "смiливість, мужність, відвага",
     "«смілвість» — опечатка, «смілість» — не та форма"),
    (14375, "translation_uk", "пісня, піснечка", "пісня, пісенька",
     "«піснечка» — такого слова нет"),
    (6442, "translation_uk", "куля, набій, шарик мороженого",
     "куля, набій, шарик морозива", "«мороженого» — русизм"),
    (15948, "translation_tr", "suç, cinayet", "suç, ağır suç",
     "«cinayet» — убийство, а Verbrechen это преступление вообще"),
    (276, "example_en", "He doe's not eat meat", "He does not eat meat",
     "апостроф внутри «does»"),
    (6427, "example_uk", "Я цим враженний", "Я цим вражений",
     "двойная «н» в «вражений»"),
    (1064, "example_uk", "Я бажаю тобі удачи", "Я бажаю тобі удачі",
     "«удачи» — русское окончание"),
    (2754, "example_uk", "Я сидю в першому ряду",
     "Я сиджу в першому ряду", "«сидю» — такой формы нет"),
    (13875, "example_en", "Ouch – Ouch, that hurts!",
     "Ouch, that hurts!", "слово приклеено к фразе через тире"),

    # --- разговорная форма в немецком эталоне ---------------------------------
    (13626, "example_de", "Er trägt 'nen schwarzen Hut",
     "Er trägt einen schwarzen Hut",
     "«'nen» — разговорное стяжение, ряд про «einen»"),
    (13439, "example_de", "Wir müssen drüber reden",
     "Wir müssen darüber reden",
     "ряд про «darüber», а в примере разговорное «drüber»"),

    # --- пример переводит другую фразу ----------------------------------------
    (801, "example_uk", "Біль сильний", "Біль дуже сильний",
     "потеряно «очень»"),
    (1484, "example_uk", "Вона веде здоровий спосіб життя",
     "Фрукти корисні для здоров'я", "в немецком «фрукты полезны»"),
    (1717, "example_en", "The shop is close to my house",
     "The station is very close", "в немецком вокзал, а не магазин"),
    (17768, "example_tr", "Anlaştık", "Bir anlaşmamız var",
     "в немецком «у нас есть сделка», а не «договорились»"),
    (2585, "example_tr", "Herhangi soruların var mı?",
     "Soruların var mı?", "«herhangi» требует «bir», и так не говорят"),
    (1383, "example_tr", "Nehrin boyunca yürüyoruz",
     "Nehir boyunca yürüyoruz", "«boyunca» не берёт родительный"),
    (915, "example_uk", "Я беру таксі на вокзал",
     "Я беру таксі до вокзалу", "«на вокзал» — неверный предлог"),
    (915, "example_tr", "İstasyona taksi alıyorum",
     "İstasyona taksiyle gidiyorum", "«taksi almak» значит купить такси"),
    (14375, "example_uk", "Заспівай мою улюблену пісню",
     "Ця пісня мені дуже подобається",
     "в немецком «песня мне очень нравится»"),
    (13428, "example_ru", "Это дети, чьи мамы здесь",
     "Это дети, чья мать здесь", "в немецком «deren Mutter» — одна мать"),
    (13428, "example_tr", "Onların evi çok büyük",
     "Bunlar annesi burada olan çocuklar",
     "в немецком про детей и мать, а не про дом"),
    (12103, "example_uk", "Дивись, як він швидко біжить",
     "Діти бігають у парку", "в немецком дети в парке"),
    (15385, "example_en", "The dog opens its mouth", "Shut your mouth",
     "в немецком грубое «закрой рот», а не про собаку"),
    (15385, "example_uk", "Собака відкриває пащу", "Закрий свою пащу",
     "в немецком грубое «закрой рот», а не про собаку"),
    (15385, "example_tr", "Köpek ağzını açıyor", "Çeneni kapa",
     "в немецком грубое «закрой рот», а не про собаку"),
    (90, "example_ru", "Он ранит себе ногу", "Он поранил ногу",
     "«ранит себе ногу» по-русски не говорят"),
    (12104, "example_tr", "Yüksek bir ateş sesi duydum",
     "Yüksek bir silah sesi duydum", "«ateş sesi» — звук огня"),
    (2008, "example_uk", "Ми довго спілкувалися за кавою",
     "Ми добре спілкуємося", "в немецком «мы хорошо общаемся»"),
    (10125, "example_uk", "Це зовсім смішно", "Це просто смішно",
     "«зовсім смішно» по-украински не говорят"),
    (10126, "example_tr", "Ailelerimizi saygıyla anıyoruz",
     "Ailemize saygı gösteriyoruz",
     "«anmak» — поминать умерших, а ehren это чтить"),
    (6413, "example_tr", "Yanlışlıkla kedinin kuyruğuna bastım",
     "Kediye basmak istemiyorum",
     "в немецком «не хочу наступить», а не «наступил»"),
    (1345, "example_uk", "Шафа стоїть у кутку", "Кафе на розі",
     "в немецком кафе на углу, а не шкаф"),
    (13434, "example_tr", "Bu kitap ne hakkında?", "Konu ne hakkında?",
     "в немецком «о чём речь», а не про книгу"),
    (17060, "example_pl", "Przeszliśmy przez stary most",
     "Ten most jest stary", "в немецком «мост старый»"),
    (12105, "example_en", "I was invited", "You are invited",
     "в немецком «тебя приглашают»"),
    (12105, "example_uk", "Я запрошую тебе на каву", "Тебе запрошують",
     "в немецком «тебя приглашают»"),
    (12105, "example_tr", "Davet edildim", "Davet ediliyorsun",
     "в немецком «тебя приглашают»"),
    (2223, "example_tr", "Siparişim hâlâ gelmedi",
     "Yeni bir siparişim var", "в немецком «у меня новый заказ»"),
    (1174, "example_en", "Watch out, the floor is wet!",
     "Look after the child", "в немецком про ребёнка, а не про пол"),
    (1174, "example_uk", "Будь ласка, наглядай за дитиною",
     "Наглядай за дитиною", "«будь ласка» в немецком нет"),
    (1174, "example_tr", "Lütfen çocuğa dikkat et", "Çocuğa dikkat et",
     "«lütfen» в немецком нет"),
    (297, "example_en", "They eat breakfast at eight",
     "We eat breakfast at eight", "в немецком «мы», а не «они»"),
    (297, "example_uk", "Вони снідають о восьмій годині",
     "Ми снідаємо о восьмій", "в немецком «мы», а не «они»"),
    (297, "example_tr", "Saat sekizde kahvaltı yapıyorlar",
     "Saat sekizde kahvaltı yapıyoruz", "в немецком «мы», а не «они»"),
    (6424, "example_uk", "Наш кіт утік із дому",
     "Нам потрібно звідси втекти", "в немецком «нам нужно отсюда убежать»"),
    (10133, "example_tr", "Güzel gülümseyebilir",
     "Çok güzel gülümseyebiliyorsun", "в немецком «ты», а не «он»"),
    (3039, "example_en", "That's the right moment for it",
     "The timing is really badly chosen",
     "в немецком момент выбран плохо, а не правильно"),
    (3039, "example_uk", "Це правильний момент",
     "Момент вибрано зовсім невдало",
     "в немецком момент выбран плохо, а не правильно"),
    (3039, "example_tr", "Bu doğru zaman",
     "Zamanlama gerçekten kötü seçilmiş",
     "в немецком момент выбран плохо, а не правильно"),
    (2696, "example_en", "That is apparently wrong",
     "That is apparently a mistake", "в немецком «это ошибка»"),
    (2696, "example_uk", "Це мабуть помилка", "Це, мабуть, помилка",
     "вводное слово выделяется запятыми"),
    (2696, "example_tr", "Anlaşılan yanlış", "Anlaşılan bu bir hata",
     "фраза без подлежащего"),
    (6437, "example_uk", "Ми піднялися нагору ліфтом",
     "Піднімайся нагору до мене!", "в немецком «поднимайся ко мне»"),
    (15390, "example_uk", "У кота пухнастий хвіст",
     "Собака махає хвостом", "в немецком собака машет хвостом"),
    (18619, "example_ru", "Я недавно его видел в метро",
     "Только что он ещё был здесь", "в немецком «только что он был здесь»"),
    (14934, "example_tr", "Bebeğin poposu kızarmış", "Kıçını kaldır",
     "в немецком «шевели задницей», а не про младенца"),
    (1546, "example_tr", "Yarın hava güzel olur umut ediyorum",
     "Her şeyin yolunda gitmesini umuyorum",
     "в немецком «надеюсь, всё получится»"),
    (14936, "example_en", "Excuse me, miss",
     "People used to call young women Fräulein",
     "в немецком объяснение, а не обращение"),
    (14936, "example_uk", "Вибачте, панна",
     "Раніше молодих жінок називали панною",
     "в немецком объяснение, а не обращение"),
    (14936, "example_tr", "Affedersiniz, bayan",
     "Eskiden genç kadınlara bayan denirdi",
     "в немецком объяснение, а не обращение"),
    (47, "example_uk", "Будь ласка, глибоко дихайте",
     "Будь ласка, глибоко вдихни", "в немецком «Atme» — ты"),
    (47, "example_tr", "Lütfen derin nefes alın",
     "Lütfen derin nefes al", "в немецком «Atme» — ты"),
    (1908, "example_en", "The sun rises at six", "Prices are rising",
     "в немецком про цены, а не про солнце"),
    (2669, "example_uk", "Я почав замислюватися про майбутнє",
     "Мені потрібно подумати", "в немецком «мне нужно подумать»"),
    (6451, "example_uk", "Він мабуть хворий", "Він, мабуть, хворий",
     "вводное слово выделяется запятыми"),
    (6454, "example_tr", "Gezi Hazirana planlanmış",
     "Gezi haziran ayına planlandı",
     "«Hazirana» без апострофа и неверная форма сказуемого"),
    (2853, "example_en", "Please do not disturb",
     "Please don't disturb me", "потеряно «меня»"),
    (2853, "example_uk", "Будь ласка, не заважайте",
     "Будь ласка, не заважай мені", "в немецком «störe» — ты, и «мне»"),
    (2853, "example_tr", "Lütfen rahatsız etmeyin",
     "Lütfen beni rahatsız etme", "в немецком «störe» — ты, и «меня»"),
    (10144, "example_tr", "Annesini alnından öptü",
     "İkisi öpüşmek istiyor", "в немецком «они хотят поцеловаться»"),
    (6457, "example_tr", "Burada sigara içmek izin verilmemiş",
     "Burada sigara içmeye izin verilmiyor", "неграмотная конструкция"),
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
