"""
Сплошная вычитка, блок 19: ряды 2101–2300 по рангу частотности
(id первого 248, id последнего 15445).

Находки:

* `kehren` — английский «We return home tomorrow» и турецкий «Yarın eve
  dönüyoruz» при немецком «Ich kehre das Zimmer». Взято другое значение
  слова: подметать и возвращаться.
* `blasen` — немецкий про ветер, украинский про ребёнка и суп, турецкий
  про свечи и желание.
* `Versehen` — турецкий «Şirket bize ücretsiz yemek sağlıyor»: компания
  кормит бесплатно, а в немецком «это была моя оплошность».
* `Wirkung` — украинское «Це була дуже смілива дія» при немецком «Die
  Medizin zeigt keine Wirkung».
* `entgegen`, `existieren`, `amüsieren`, `proben`, `gefälligst`,
  `schmecken`, `eingehen`, `erheben`, `herzlich`, `pinkeln` — то же:
  перевод переводит другую фразу.
* `heulen` — в русских значениях «вытьвоить». Такого слова нет.
* `verärgert` — украинское «образений» вместо «ображений».
* `Segen` — турецкое «berekettti» с тремя «t».
* `verlobt` — английское «Were engaged» без апострофа.
* `Camp` — турецкое «bu yaz yaz kampına»: слово дважды. И украинское
  «у літній табір цього літа» — про лето дважды.
* `Bursche` — турецкое «genç delikanlı»: «delikanlı» и есть юноша.
* `Kanone` — «hala» без циркумфлекса читается как «тётя».
* `Block` — «мы живём в жилом блоке» в русском и украинском: так не
  говорят, а в значениях уже стоит «жилой дом».
* `schmecken`, `widerlich` — турецкое «tadıyor»: вкус по-турецки не
  «пробуют», а «есть».
* `vertragen` — польское «nie znoszę mleka» это «не люблю молоко», а
  немецкий про непереносимость.
* `Wächter` — английское «controls the entrances»: ложный друг, «kontrollieren»
  это проверять.
* `Raumschiff` — в немецком и польском корабль сел посреди Берлина, в
  остальных трёх — в центре города. Ряд приведён к эталону.

Отдельная оговорка про `herzlich` (id 1534). «Herzlich willkommen» —
приветствие, и естественные равенства ему в турецком («Hoş geldiniz») и
украинском не содержат самого слова «сердечный». Выбрано приветствие:
владелец требует, чтобы переводы были естественными и отвечали друг
другу, а это важнее, чем видеть заголовок внутри примера.

    python -m app.scripts.fix_block_0019            # показать
    python -m app.scripts.fix_block_0019 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# (id, колонка, что стоит сейчас, на что менять, зачем)
FIXES: list[tuple[int, str, str, str, str]] = [

    # --- пример переводит другую фразу ---------------------------------------
    (248, "example_pl", "Jadę do pracy rowerem", "Jedzie na rowerze",
     "немецкий «Er fährt mit dem Fahrrad» — он, а не «я на работу»"),
    (1534, "example_uk", "Сердечно дякую тобі за допомогу",
     "Сердечно вітаємо вас!",
     "немецкий «Herzlich willkommen» — приветствие, а не благодарность"),
    (1534, "example_tr", "Komşumuz çok samimi bir insan", "Hoş geldiniz",
     "то же: турецкий рассказывал про соседа"),
    (2379, "example_uk", "Гроші надходять на рахунок завтра",
     "Заявка надійшла", "немецкий «Die Bewerbung ist eingegangen»"),
    (6728, "example_tr", "Hayaletlerin var olduğuna inanmıyorum",
     "Bu tür problemler her yerde var",
     "немецкий «Solche Probleme existieren überall», турецкий — про привидений"),
    (12135, "example_uk", "Клоун розважає дітей на святі",
     "Це мене дуже забавляє", "немецкий «Das amüsiert mich sehr»"),
    (6738, "example_uk", "Це була дуже смілива дія",
     "Ліки не мають жодної дії",
     "немецкий «Die Medizin zeigt keine Wirkung», украинский — про поступок"),
    (6740, "example_tr", "Sokağın karşısında küçük bir market var",
     "Bana doğru geldi",
     "немецкий «Er kam mir entgegen», турецкий — про магазин напротив"),
    (6741, "example_tr", "Şirket bize ücretsiz yemek sağlıyor",
     "Bu benim yanlışlığımdı",
     "немецкий «Das war ein Versehen von mir», турецкий — про бесплатную еду"),
    (6742, "example_uk", "Ми піднімаємося сходами на третій поверх",
     "Ми підводимося зі стільця", "немецкий «Wir erheben uns vom Stuhl»"),
    (14418, "example_en", "We still need to rehearse for the concert",
     "We're rehearsing the play tonight",
     "немецкий «Wir proben heute Abend das Theaterstück»"),
    (14418, "example_uk", "Нам ще потрібно репетирувати для концерту",
     "Сьогодні ввечері ми репетируємо виставу", "то же"),
    (14418, "example_tr", "Konser için hala prova yapmamız gerekiyor",
     "Bu akşam oyunun provasını yapıyoruz", "то же"),
    (800, "example_uk", "Мені дуже смакує цей борщ", "Це смачно",
     "немецкий «Das schmeckt gut» — без борща"),
    (12531, "example_uk", "Мамо, я хочу пісяти",
     "Мені треба швиденько попісяти",
     "немецкий «Ich muss kurz pinkeln» — без обращения к маме"),
    (6764, "example_en", "We return home tomorrow", "I sweep the room",
     "немецкий «Ich kehre das Zimmer» — подметаю, а не возвращаюсь"),
    (6764, "example_tr", "Yarın eve dönüyoruz", "Odayı süpürüyorum", "то же"),
    (6769, "example_uk", "Дитина дує на гарячий суп",
     "Сьогодні сильно дує вітер", "немецкий «Der Wind bläst heute stark»"),
    (6769, "example_tr", "Mumları üfle ve dilek tut",
     "Bugün rüzgâr çok şiddetli esiyor", "то же: турецкий про свечи"),
    (13934, "example_uk", "Передай мені сіль, будь ласка",
     "Припини це, будь ласкавий",
     "немецкий «Hör gefälligst auf damit» — требование прекратить"),
    (1021, "example_uk", "Дід Мороз приніс дітям подарунки",
     "Дід Мороз приносить подарунки",
     "в немецком настоящее время, и детей там нет"),
    (2718, "example_uk", "Зараз у нас важка фаза", "Це важка фаза",
     "немецкий «Das ist eine schwierige Phase»"),

    # --- потеряно или добавлено --------------------------------------------
    (18670, "example_ru", "Можешь разбудить меня завтра рано?",
     "Можешь разбудить меня завтра утром?", "«morgen früh» — завтра утром"),
    (18670, "example_pl", "Możesz mnie obudzić wcześnie rano?",
     "Możesz mnie obudzić jutro rano?", "потеряно «завтра»"),
    (11668, "example_uk", "Мене мучить страшна спрага",
     "Мене справді мучить спрага",
     "«страшна» в немецком нет, зато потеряно «richtig»"),
    (6741, "example_en", "That was by mistake", "That was my mistake",
     "потеряно «von mir»"),
    (14986, "example_en", "Were engaged", "We're engaged to each other",
     "потерян апостроф, и «miteinander» не переведено"),
    (2709, "example_uk", "Це справжній рай", "Це рай",
     "«справжній» в немецком нет"),
    (235, "example_pl", "Ten film jest tylko dla dorosłych",
     "Tylko dla dorosłych", "«Ten film» в немецком нет"),
    (12136, "example_en", "The kids are going to summer camp",
     "The kids are going to camp this summer", "в немецком «diesen Sommer»"),
    (1359, "example_en", "Please get in the car", "Please get in",
     "машины в немецком нет"),
    (2972, "example_uk", "Я це розумію", "Я ставлюся до цього з розумінням",
     "«Verständnis haben für» — относиться с пониманием"),
    (13934, "example_en", "Stop that right now", "Kindly stop that",
     "«gefälligst» — «будь любезен», это и есть слово ряда"),
    (17504, "example_en", "The spaceship landed in the middle of the city",
     "The spaceship landed in the middle of Berlin", "в немецком Берлин"),
    (17504, "example_ru", "Космический корабль приземлился в центре города",
     "Космический корабль приземлился посреди Берлина", "то же"),
    (17504, "example_uk", "Космічний корабель приземлився посеред міста",
     "Космічний корабель приземлився посеред Берліна", "то же"),
    (17504, "example_tr", "Uzay gemisi şehrin ortasına indi",
     "Uzay gemisi Berlin'in ortasına indi", "то же"),
    (12529, "example_uk", "Мені ще треба швидко під душ",
     "Мені ще треба швидко прийняти душ", "пропущен глагол"),

    # --- слова, которых нет в языке, и опечатки -------------------------------
    (10281, "translation_ru", "рыдать, плакать, вытьвоить",
     "рыдать, плакать, выть", "«вытьвоить» — такого слова нет"),
    (2937, "translation_uk", "розлючений, роздратований, образений",
     "розлючений, роздратований, ображений", "«образений» — опечатка"),
    (14412, "example_tr", "Yağmur bitkiler için bir berekettti",
     "Yağmur bitkiler için bir bereketti", "опечатка: три «t»"),
    (16026, "example_tr", "Eski top hala müzede duruyor",
     "Eski top hâlâ müzede duruyor",
     "без циркумфлекса «hala» — это тётя, а не «до сих пор»"),
    (16027, "example_ru", "Король сидел на своем золотом троне",
     "Король сидел на своём золотом троне", "пропущена «ё»"),
    (12136, "example_tr", "Çocuklar bu yaz yaz kampına gidiyorlar",
     "Çocuklar bu yaz kampa gidiyorlar", "«yaz yaz» — слово дважды"),
    (12136, "example_uk", "Діти їдуть у літній табір цього літа",
     "Діти цього літа їдуть у табір", "про лето сказано дважды"),
    (14989, "example_tr", "Genç delikanlı çok yardımsever",
     "Delikanlı çok yardımsever",
     "«delikanlı» и есть юноша: «genç delikanlı» — дважды одно и то же"),
    (15443, "translation_ru", "курица, кура", "курица",
     "«кура» — просторечие"),

    # --- русизмы в украинской колонке ----------------------------------------
    (15437, "translation_uk", "спека, жара, жар", "спека, жарота, жар",
     "«жара» — русизм"),
    (6747, "example_uk", "Він тихо відкрив двері",
     "Він тихо відчинив двері", "двері відчиняють; «відкрив» — русизм"),
    (13490, "example_uk", "Я знову зробив ту ж саму помилку",
     "Я знову зробив ту саму помилку",
     "«ту ж саму» — русизм, в значениях стоит «та сама»"),

    # --- грамматика целевого языка --------------------------------------------
    (17087, "example_tr", "Kamyonun ağır bir yükü vardır",
     "Kamyonun ağır bir yükü var", "«-dır» — канцелярит"),
    (13489, "example_tr", "Bana yardım eden o kişi",
     "Bana yardım eden kişi o", "пропущена связка, фраза не складывается"),
    (2569, "example_tr", "Tepeden yürüyoruz", "Tepenin üzerinden yürüyoruz",
     "«tepeden» — с холма; в немецком через холм"),
    (2588, "example_tr", "Yıllarca onun için bekledim",
     "Yıllarca onu bekledim", "«onun için» — для него; в немецком ждал его"),
    (10296, "example_tr", "Bunu başarmaya iradem var",
     "Bunu başarmak için iradem var", "«başarmaya iradem» — неверное управление"),
    (13647, "example_uk", "Ця куртка зроблена з справжньої вовни",
     "Ця куртка зроблена зі справжньої вовни", "перед «сп» нужно «зі»"),
    (1359, "example_tr", "Lütfen binin", "Lütfen bin",
     "в немецком «ты», а «binin» — «вы»"),

    # --- подменённое значение -------------------------------------------------
    (15437, "example_tr", "Bu sıcaklıkta içeride kalmayı tercih ederim",
     "Bu sıcakta içeride kalmayı tercih ederim",
     "«sıcaklık» — температура, а «Hitze» это жара"),
    (8800, "example_en", "The secretary takes the appointments",
     "The secretary writes down the appointments",
     "«schreibt auf» — записывает, а не принимает"),
    (8800, "example_tr", "Sekreter randevuları alıyor",
     "Sekreter randevuları kaydediyor", "то же"),
    (9460, "example_tr", "Bana bir kalem verir misin?",
     "Benim için bir kalemin var mı?",
     "немецкий спрашивает, есть ли ручка, а не просит дать"),
    (17503, "example_ru", "Можешь найти мой телефон?",
     "Можешь определить, где мой телефон?",
     "«orten» — определить местоположение, а не найти вещь"),
    (17503, "example_uk", "Можеш знайти мій телефон?",
     "Можеш визначити, де мій телефон?", "то же"),
    (14417, "example_pl", "Cały ten dramat z moim byłym mnie męczy",
     "Cały ten dramat z moim byłym mnie denerwuje",
     "«nervt» — раздражает, а не утомляет"),
    (13647, "example_pl", "Ten sweter jest z prawdziwej wełny",
     "Ta kurtka jest z prawdziwej wełny", "в немецком куртка, а не свитер"),
    (324, "example_tr", "Kafe çok samimi", "Kafe çok rahat",
     "«samimi» — искренний о людях; «gemütlich» это уютный"),
    (10306, "example_tr", "Veda etmek bizim için zordu",
     "Veda bizim için zordu", "в немецком существительное, а не глагол"),
    (2976, "example_pl", "Nie znoszę mleka", "Nie toleruję mleka",
     "«nie znoszę» — не люблю; немецкий про непереносимость"),
    (8803, "example_en", "The guard controls the entrances",
     "The guard checks the entrances",
     "«kontrollieren» — проверять; «control» здесь ложный друг"),
    (2972, "example_en", "I have understanding for that",
     "I have sympathy for that", "«have understanding for» — не по-английски"),
    (1359, "example_uk", "Заходь у машину, будь ласка", "Сідай, будь ласка",
     "в транспорт сідають, а не заходять; и машины в немецком нет"),

    # --- говорить по-людски ---------------------------------------------------
    (10290, "example_tr", "Bu onun tarafından acımasızca",
     "Onun yaptığı çok acımasızdı", "по-турецки так фразу не строят"),
    (6741, "example_uk", "Це було по помилці", "Це була моя помилка",
     "«по помилці» — калька, и потеряно «von mir»"),
    (6743, "example_uk", "Тримай, будь ласка, відстань метр від мене",
     "Тримайся, будь ласка, на відстані метра від мене",
     "«тримай відстань метр» — так не говорят"),
    (57, "example_uk", "Вона проходить професійне навчання кухаря",
     "Вона проходить навчання на кухарку",
     "«навчання кухаря» читается как учёба повара, а она учится на повара"),
    (800, "example_tr", "Bu güzel tadıyor", "Bunun tadı güzel",
     "«tadıyor» — так по-турецки не говорят"),
    (10295, "example_tr", "Yemek gerçekten iğrenç tadıyor",
     "Yemeğin tadı gerçekten iğrenç", "то же"),
    (14989, "example_uk", "Молодий хлопець дуже відгукливий",
     "Молодий хлопець завжди готовий допомогти",
     "«відгукливий» — так не говорят; «hilfsbereit» это готовый помочь"),
    (18158, "example_ru", "Мы живём в большом жилом блоке",
     "Мы живём в большом жилом доме",
     "«жилой блок» — так не говорят, в значениях стоит «жилой дом»"),
    (18158, "example_uk", "Ми живемо у великому житловому блоці",
     "Ми живемо у великому житловому будинку", "то же"),
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
