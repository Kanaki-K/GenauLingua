"""
Сплошная вычитка, блок 17: ряды 1701–1900 по рангу частотности.

Находки:

* `kurz` — немецкий про короткие волосы, а четыре перевода из пяти про
  недавний переезд. Самый большой разъезд в блоке.
* `berichten`, `rosa`, `prüfen`, `die Tasse`, `die Dusche`, `das Weib`,
  `der Junior`, `die Sicht`, `rausholen` — примеры переводят другое
  предложение, причём обычно сразу в трёх языках.
* `das Weib` — в английском «mug» прочли как кружку в предыдущем блоке, а
  здесь пример вообще про учительницу.
* `klauen` — в украинском значении «крати» вместо «красти».
* `der Roman` — в польском «roman», которого в этом значении нет.
* `eng`, `die Verteidigung` — в списке значений пояснение, а не слово:
  «o przyjaźni», «defence in sport», «защита в спорте».
* `mutig` — в украинском и «смілий», и «сміливий»: одно слово дважды.
* `amerikanisch`, `leiten` — английские следы: «Were» вместо «We're»,
  «I lead/manage the project» со слэшем.
* `der Hauptmann`, `der Staatsanwalt` — «задает» и «отдает» без ё.

    python -m app.scripts.fix_block_0017            # показать
    python -m app.scripts.fix_block_0017 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# (id, колонка, что стоит сейчас, на что менять, зачем)
FIXES: list[tuple[int, str, str, str, str]] = [

    # --- kurz: немецкий про волосы, переводы про переезд ---------------------
    (18662, "example_en", "I moved here recently", "My hair is now very short",
     "немецкий пример про короткие волосы"),
    (18662, "example_ru", "Недавно я сюда переехал",
     "Мои волосы теперь совсем короткие",
     "немецкий пример про короткие волосы"),
    (18662, "example_uk", "Нещодавно я сюди переїхав",
     "Моє волосся тепер зовсім коротке",
     "немецкий пример про короткие волосы"),
    (18662, "example_tr", "Kısa süre önce buraya taşındım",
     "Saçlarım şimdi çok kısa",
     "немецкий пример про короткие волосы"),

    # --- примеры переводят другое предложение --------------------------------
    (95, "example_en", "She reported the accident to the police",
     "I'm telling you about my trip",
     "немецкий — «я рассказываю тебе о своей поездке»"),
    (95, "example_uk", "Вона розповідає про подорож",
     "Я розповідаю тобі про свою подорож",
     "немецкий в первом лице и с «тебе»"),
    (95, "example_tr", "Yolculuk hakkında anlatıyor",
     "Sana yolculuğumu anlatıyorum",
     "немецкий в первом лице и с «тебе»"),
    (95, "example_pl", "Opowiem ci o mojej podróży",
     "Opowiadam ci o mojej podróży",
     "немецкий в настоящем времени"),

    (6634, "example_en", "I love your pink jacket",
     "I bought myself a pink dress",
     "немецкий — «я купила себе розовое платье»"),
    (6634, "example_uk", "Вона купила рожеву сукню",
     "Я купила собі рожеву сукню",
     "немецкий в первом лице"),
    (6634, "example_tr", "Pembe bir elbise giyiyor",
     "Kendime pembe bir elbise aldım",
     "немецкий — купила, а не носит"),

    (735, "example_en", "Let me check the time", "You check the documents",
     "немецкий — «ты проверяешь документы»"),
    (735, "example_uk", "Перевір, чи двері зачинені", "Ти перевіряєш документи",
     "немецкий — «ты проверяешь документы»"),
    (735, "example_tr", "Ödevimi bir daha kontrol ettim",
     "Belgeleri kontrol ediyorsun",
     "немецкий — «ты проверяешь документы»"),

    (914, "example_en", "She drinks from a cup", "I drink my coffee from a cup",
     "немецкий — «я пью свой кофе из чашки»"),
    (914, "example_uk", "Вона п'є з чашки", "Я п'ю каву з чашки",
     "немецкий в первом лице, и кофе потерялся"),
    (914, "example_tr", "Bir fincandan içiyor", "Kahvemi fincandan içiyorum",
     "немецкий в первом лице, и кофе потерялся"),

    (199, "example_en", "He takes a quick shower", "I take a quick shower",
     "немецкий в первом лице"),
    (199, "example_uk", "Він приймає короткий душ", "Я приймаю короткий душ",
     "немецкий в первом лице"),
    (199, "example_tr", "Kısa bir duş alıyor", "Kısa bir duş alıyorum",
     "немецкий в первом лице"),

    (14968, "example_en", "That woman over there is my teacher",
     "Now that's a clever woman!",
     "немецкий — «вот это умная баба!»"),
    (14968, "example_uk", "Моя жінка готує вечерю", "Ото розумна баба!",
     "перевод переводил другое предложение"),
    (14968, "example_tr", "Karım işten yeni geldi", "Ne akıllı kadın!",
     "перевод переводил другое предложение"),

    (14970, "example_en", "Our junior team won again yesterday",
     "He plays as a junior on the team",
     "немецкий — «он играет в команде как юниор»"),
    (14970, "example_uk", "Мій молодший брат ходить у школу",
     "Він грає в команді як юніор",
     "перевод переводил другое предложение"),

    (6637, "example_en", "Visibility is really bad in this fog",
     "From here you have a good view",
     "немецкий — «отсюда у тебя хороший вид»"),
    (6637, "example_uk", "Через туман погана видимість",
     "Звідси у тебе гарний вид",
     "перевод переводил другое предложение"),
    (6637, "example_tr", "Buradan şehrin güzel bir görüşü var",
     "Buradan görüş çok iyi",
     "«şehrin görüşü» — калька, город взялся из ниоткуда"),

    (6665, "example_en", "I need to get the car out of the garage",
     "I'm getting the car out of the garage",
     "немецкий о происходящем, а не о надобности"),
    (6665, "example_uk", "Мені потрібно витягти машину з гаража",
     "Я витягаю машину з гаража",
     "немецкий о происходящем, а не о надобности"),
    (6665, "example_tr", "Arabayı çıkarmam gerekiyor",
     "Arabayı garajdan çıkarıyorum",
     "немецкий о происходящем, и гараж потерялся"),

    (17773, "example_ru", "С ним трудно договариваться",
     "Мы можем договориться о цене",
     "немецкий — «мы можем договориться о цене»"),
    (17773, "example_uk", "З ним важко домовлятися",
     "Ми можемо домовитися про ціну",
     "немецкий — «мы можем договориться о цене»"),

    (10236, "example_uk", "Це був відчайдушний крик про допомогу",
     "Вона у повному відчаї",
     "перевод переводил другое предложение"),
    (10236, "example_tr", "Tamamen umutsuz", "O tamamen umutsuz",
     "без подлежащего фраза висит"),

    (10247, "example_en", "That noise at night is really creepy",
     "The house is incredibly dark",
     "немецкий — «дом жутко тёмный»"),

    (10255, "example_en", "I'm so glad you came!", "Merry Christmas",
     "немецкий — «Frohe Weihnachten», как и остальные четыре языка"),

    (2270, "example_en", "We're running low on fuel",
     "I have to fill up with petrol",
     "немецкий — «мне нужно заправиться»"),
    (2270, "example_uk", "Мені потрібно заправити бензин",
     "Мені треба заправитися бензином",
     "«заправити бензин» так не кажуть"),

    (6632, "example_en", "I tell you the following: Come on time",
     "I tell you the following: come on time",
     "после двоеточия строчная"),
    (6632, "example_uk", "Я кажу тобі наступне: Приходь вчасно",
     "Я кажу тобі наступне: приходь вчасно",
     "после двоеточия строчная"),

    (13476, "example_tr", "Sınıfta yüz öğrenci var", "Kitap yüz euro",
     "пример был про учеников, немецкий — про цену книги"),
    (15429, "example_tr", "Masaldaki ejder ateş püskürüyor",
     "Uçurtma gökyüzünde uçuyor",
     "пример был про дракона, немецкий — про воздушного змея"),
    (13914, "example_tr", "Radyo çalışmıyor", "Telsiz çalışmıyor",
     "«Funk» здесь рация, а не радиоприёмник"),
    (1198, "example_tr", "Otobüsten inmek için düğmeye bas",
     "Bir sonraki durakta iniyorum",
     "пример был про кнопку, немецкий — про следующую остановку"),
    (6645, "example_tr", "Bu merkezi soru", "Ana soru bu",
     "«merkezi soru» — калька, по-турецки так не говорят"),
    (15996, "example_tr", "Yalan söylediği şüphem var",
     "Yalan söylediğinden şüphem var",
     "фраза не стоит без падежа"),
    (1976, "example_tr", "Bugün hâlâ piyano çalışmam gerekiyor",
     "Bugün bir de piyano çalışmam gerekiyor",
     "«hâlâ» — ещё до сих пор, а немецкое «noch» здесь «ещё и»"),
    (8780, "example_tr", "Kralın çok hizmetkarı var",
     "Kralın birçok hizmetkârı var",
     "«çok hizmetkarı» — нужна форма «birçok», и буква â"),
    (2401, "example_tr", "Karşılama çok sıcakkanlıydı", "Karşılama çok sıcaktı",
     "«sıcakkanlı» — о человеке, а не о приёме"),
    (739, "example_tr", "Tren dakik geliyor", "Tren tam zamanında geliyor",
     "«dakik» — о человеке, а не о поезде"),
    (12521, "example_tr", "Yara hala acıyor", "Yara hâlâ acıyor",
     "«hala» — тётя, нужно «hâlâ»"),

    (1563, "example_uk", "Я в інтернеті", "Я сиджу в інтернеті",
     "немецкий — «ich sitze im Internet»"),
    (6628, "example_en", "I cut bread", "I'm cutting the bread right now",
     "в немецком «gerade» — прямо сейчас"),
    (6628, "example_uk", "Цим ножем важко різати хліб", "Я саме ріжу хліб",
     "перевод переводил другое предложение"),
    (6628, "example_tr", "Ekmek kesiyorum", "Şu anda ekmek kesiyorum",
     "в немецком «gerade» — прямо сейчас"),
    (8778, "example_uk", "На письмовому столі повний безлад",
     "Мій комп'ютер стоїть на письмовому столі",
     "перевод переводил другое предложение"),
    (2071, "example_uk", "Мені треба готуватися до іспиту",
     "Я готуюся до іспиту",
     "немецкий — «я готовлюсь», а не «мне надо»"),
    (10233, "example_uk", "Я боюся темряви", "Я боюся грози",
     "в немецком гроза, а не темнота"),
    (485, "example_uk", "Я прибираю одяг", "Я прибираю свої шмотки",
     "в ряду слово «шмотки», и «свої» потерялось"),
    (485, "example_tr", "Kıyafetleri topluyor", "Kıyafetlerimi topluyorum",
     "немецкий в первом лице и со «своими»"),
    (12517, "example_uk", "Я спалила пиріг у печі",
     "Обережно, ти можеш обпектися",
     "перевод переводил другое предложение"),
    (988, "example_uk", "Я чекаю вже чверть години", "Зараз чверть на четверту",
     "перевод переводил другое предложение"),
    (6652, "example_uk", "Він обернувся й помахав мені рукою", "Обернись!",
     "немецкий — повеление «Dreh dich um!»"),
    (6636, "example_uk", "Він завжди з'являється останнім",
     "Ти мусиш з'явитися вчасно",
     "перевод переводил другое предложение"),
    (10243, "example_uk", "Вона жертвує свій час дітям",
     "Я жертвую своїм вільним часом заради роботи",
     "перевод переводил другое предложение"),
    (10242, "example_uk", "Вона відчула співчуття до бездомного пса",
     "Я відчуваю до нього співчуття",
     "перевод переводил другое предложение"),
    (16003, "example_ru", "Командир отдал приказ выступать",
     "Командир ведёт солдат",
     "перевод переводил другое предложение"),
    (16003, "example_uk", "Наш командир суворий, але справедливий",
     "Командир веде солдатів",
     "перевод переводил другое предложение"),
    (17919, "example_ru", "Учёный проводит опыты в лаборатории",
     "Учёный проводит опыты",
     "лаборатории в немецком нет"),
    (1200, "example_uk", "Покажіть, будь ласка, посвідчення",
     "Покажи, будь ласка, своє посвідчення",
     "немецкий на «ты», а здесь на «вы»"),
    (1200, "example_tr", "Lütfen kimliğinizi gösterin",
     "Lütfen kimliğini göster",
     "немецкий на «ты», а здесь на «вы»"),
    (1200, "example_ru", "Покажи мне, пожалуйста, своё удостоверение личности",
     "Покажи мне, пожалуйста, своё удостоверение",
     "«удостоверение личности» в живой речи сокращают"),

    # --- ошибки в словах -----------------------------------------------------
    (16007, "translation_uk", "вкрасти, стягнути, крати",
     "вкрасти, стягнути, красти",
     "«крати» — опечатка, нужно «красти»"),
    (14403, "translation_pl", "powieść, roman", "powieść",
     "«roman» в этом значении по-польски не говорят"),
    (10241, "translation_uk", "смілий, сміливий, відважний",
     "сміливий, відважний, мужній",
     "«смілий» і «сміливий» — одне слово двічі"),
    (6665, "translation_uk", "витягати, дістати, вижати максимум",
     "витягати, дістати, вичавити максимум",
     "«вижати» — русизм, українською «вичавити»"),
    (14972, "translation_uk", "особа, ідентичність, самобутність",
     "особистість, ідентичність, самобутність",
     "у прикладі «особистість», і так точніше"),
    (16000, "example_ru", "Капитан отдает приказы", "Капитан отдаёт приказы",
     "пропущена ё"),
    (16006, "example_ru", "Прокурор задает вопросы", "Прокурор задаёт вопросы",
     "пропущена ё"),
    (965, "example_uk", "Урок починається о дев'ять",
     "Урок починається о дев'ятій",
     "о дев'ятій годині — потрібен порядковий"),
    (269, "example_uk", "У неї лихоманка", "У неї температура",
     "«Fieber haben» — це температура, а лихоманка це хвороба"),
    (1829, "example_uk", "Знак великий", "Табличка велика",
     "у ряді перше значення «табличка», як і в російському"),
    (15429, "example_uk", "Повітряний змій летить в небі",
     "Повітряний змій летить у небі",
     "перед «н» потрібне «у»"),
    (14402, "example_uk", "Чарівник робить чари", "Чарівник творить чари",
     "«робить чари» так не кажуть"),
    (10240, "example_uk", "Я хочу виконати свою мрію",
     "Я хочу здійснити свою мрію",
     "мрію здійснюють, а не виконують"),
    (2290, "example_uk", "Ти не можеш входити в кімнату",
     "Тобі не можна входити в кімнату",
     "немецкое «darfst nicht» — запрет, а не неспособность"),
    (10232, "example_uk", "Це зовсім дурно", "Це зовсім дурне",
     "«дурно» — це про недобре самопочуття"),

    # --- в списке значений пояснение вместо слова ----------------------------
    (15998, "translation_en", "defense, defence in sport", "defense, defence",
     "в списке значений стояло пояснение"),
    (15998, "translation_ru", "защита, оборона, защита в спорте",
     "защита, оборона",
     "в списке значений стояло пояснение"),
    (222, "translation_pl", "wąski, ciasny, bliski, o przyjaźni",
     "wąski, ciasny, bliski",
     "«o przyjaźni» — пояснение, а не слово"),

    # --- по-людски: книжно и калькой там, где немецкий сказал просто ---------
    (789, "example_en", "I give you a book", "I'm giving you a book as a present",
     "«schenken» — дарить, а «I give you» этого не передаёт"),
    (789, "example_pl", "Podaruję ci książkę", "Daję ci książkę w prezencie",
     "немецкий в настоящем времени"),
    (6627, "example_en", "Were watching an American movie",
     "We're watching an American movie",
     "«Were» вместо «We're»"),
    (2657, "example_en", "I lead/manage the project", "I manage the project",
     "слэш в примере — след черновика"),
    (1266, "example_en", "I would like to order water", "I'm ordering a water",
     "немецкий — «я заказываю», а не «я хотел бы»"),
    (1266, "example_uk", "Я хочу замовити воду", "Я замовляю воду",
     "немецкий — «я заказываю», а не «я хочу»"),
    (1266, "example_tr", "Bir su sipariş etmek istiyorum",
     "Bir su sipariş ediyorum",
     "немецкий — «я заказываю», а не «я хочу»"),
    (14397, "example_ru", "Публика разражается аплодисментами",
     "Публика аплодирует",
     "«разражается аплодисментами» — книжно"),
    (14397, "example_pl", "Publiczność nagradza występ oklaskami",
     "Publiczność bije oklaski",
     "«nagradza występ» — книжно, немецкий сказал коротко"),
    (2024, "example_en", "He left without saying goodbye", "I'm saying goodbye",
     "немецкий — «я прощаюсь»"),
    (2024, "example_tr", "Gitmeden önce herkese veda ettim", "Veda ediyorum",
     "немецкий — «я прощаюсь», коротко и в настоящем"),
    (2024, "example_pl", "Pożegnam się", "Żegnam się",
     "немецкий в настоящем времени"),
    (1658, "example_en", "They deliver groceries to our door",
     "We deliver groceries to your home",
     "немецкий — «мы доставляем», а не «они»"),
    (1658, "example_uk", "Магазин доставляє продукти додому безкоштовно",
     "Ми доставляємо продукти додому",
     "немецкий в первом лице, и «безкоштовно» взялось из ниоткуда"),
    (1658, "example_tr", "Siparişi kapıya teslim ettiler",
     "Yiyecekleri eve teslim ediyoruz",
     "немецкий в первом лице и в настоящем времени"),
    (10238, "example_ru", "Он имеет большое влияние на меня",
     "У него на меня большое влияние",
     "«имеет влияние» — канцелярит"),
    (2081, "example_ru", "Это имеет много преимуществ",
     "У этого много преимуществ",
     "«имеет много преимуществ» — канцелярит"),
    (17075, "example_ru", "Мы делаем тур по городу",
     "Мы едем на экскурсию по городу",
     "«делаем тур» — калька с немецкого"),
    (17075, "example_uk", "Ми робимо тур по місту",
     "Ми їдемо на екскурсію по місту",
     "«робимо тур» — калька з німецької"),
    (6656, "example_uk", "Погода сьогодні екстремально спекотна",
     "Погода сьогодні надзвичайно спекотна",
     "«екстремально спекотна» так не кажуть"),
    (18657, "example_en", "I waited an eternity for the bus",
     "I've been waiting an eternity for you",
     "немецкий — «я жду тебя», и до сих пор жду"),
    (557, "example_ru", "Какую линию ты берёшь?", "Какой линией ты едешь?",
     "«брать линию» — калька с немецкого"),
    (557, "example_tr", "Hangi hattı alıyorsun?", "Hangi hatla gidiyorsun?",
     "«hattı almak» — калька с немецкого"),
    (222, "example_pl", "Te spodnie są za wąskie", "Te spodnie są za ciasne",
     "о штанах по-польски говорят «ciasne»"),
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
