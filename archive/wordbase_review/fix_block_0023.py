"""
Сплошная вычитка, блок 23: ряды 2901–3100 по рангу частотности
(id первого 6925, id последнего 16110).

Находки:

* `Hai` — битый эталон: «ein großer Meerestier». «Meerestier» среднего
  рода, нужно «ein großes». И английский с украинским переводят другую
  фразу: «опасная рыба» вместо «крупное морское животное».
* `sperren` (16084) — немецкий пример дословно совпадал с рядом 3005
  `gesperrt`: «Die Straße ist gesperrt wegen Bauarbeiten». У ряда про
  глагол стоял пример про причастие. Пример заменён во всех шести
  языках.
* `unter` и `Piepen` — эталон со стяжением и без артикля: «Unterm Tisch»,
  «Piepen nervt mich». Слово ряда в примере не видно.
* `Wiederhören` — переводы совпадали с `Wiedersehen` («До свидания»), а
  «Auf Wiederhören» говорят только по телефону. Теперь «До связи», «До
  зв'язку», «Talk to you again soon» — разница видна.
* `Gräfin` — турецкое «Gref»: такого слова нет. `Schneider` —
  «cekenimi». `egoistisch` — «haksızdi». `Verletzung` — «ciddiye değil».
  `naiv` — «Bu senin kısımda saf oldu». `aufstellen` — «Partı».
* `verwandt` — украинское «спорідненні» с двойной «н».
* `Schwachkopf` — «болван» в украинской колонке, `Henker` — «палач»,
  `aufrichtig` и `ausgesprochen` — «з твоєї сторони»: русизмы.
* `Vorstand` — «Правління прийняла»: средний род.
* `Bock`, `beiseite`, `absagen`, `Kanzlei`, `Privatsphäre`, `Klang`,
  `Frost`, `Funkgerät`, `aktivieren`, `ermitteln`, `abbrechen`,
  `ausgesprochen`, `ärgern`, `geregelt` — перевод переводит другую фразу.

    python -m app.scripts.fix_block_0023            # показать
    python -m app.scripts.fix_block_0023 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# (id, колонка, что стоит сейчас, на что менять, зачем)
FIXES: list[tuple[int, str, str, str, str]] = [

    # --- немецкий эталон -------------------------------------------------------
    (15476, "example_de", "Der Hai ist ein großer Meerestier",
     "Der Hai ist ein großes Meerestier",
     "«Meerestier» среднего рода: «ein großes»"),
    (13505, "example_de", "Unterm Tisch sitzt die Katze",
     "Unter dem Tisch sitzt die Katze",
     "«Unterm» — стяжение, и слово ряда «unter» не видно"),
    (13973, "example_de", "Piepen nervt mich", "Das Piepen nervt mich",
     "без артикля фраза не читается"),
    (16084, "example_de", "Die Straße ist gesperrt wegen Bauarbeiten",
     "Die Polizei sperrt die Straße wegen eines Unfalls",
     "пример дословно совпадал с рядом 3005 `gesperrt` и показывал "
     "причастие, а не глагол"),

    # --- `sperren`: пример заменён целиком ------------------------------------
    (16084, "example_ru", "Улица закрыта из-за работ",
     "Полиция перекрывает улицу из-за аварии", "вслед за эталоном"),
    (16084, "example_en", "The street is blocked due to construction",
     "The police are closing the street because of an accident",
     "вслед за эталоном"),
    (16084, "example_uk", "Вулиця заблокована через будівництво",
     "Поліція перекриває вулицю через аварію", "вслед за эталоном"),
    (16084, "example_tr", "Caddede inşaat nedeniyle kapalı",
     "Polis kaza nedeniyle caddeyi kapatıyor", "вслед за эталоном"),
    (16084, "example_pl", "Ulica jest zamknięta z powodu remontu",
     "Policja zamyka ulicę z powodu wypadku", "вслед за эталоном"),

    # --- `Wiederhören`: разводим с `Wiedersehen` ------------------------------
    (13968, "example_ru", "До свидания", "До связи",
     "совпадало с `Wiedersehen`, а «Auf Wiederhören» — только по телефону"),
    (13968, "example_uk", "До побачення", "До зв'язку", "то же"),
    (13968, "example_en", "Goodbye for now", "Talk to you again soon",
     "то же"),

    # --- `Hai`: перевод переводит другую фразу --------------------------------
    (15476, "example_en", "The shark is a dangerous fish",
     "The shark is a large sea animal",
     "в немецком «крупное морское животное»"),
    (15476, "example_uk", "Акула — це небезпечна риба",
     "Акула — велика морська тварина", "то же"),
    (15476, "example_tr", "Köpek balığı tehlikeli bir balıktır",
     "Köpek balığı büyük bir deniz hayvanı", "то же"),

    # --- пример переводит другую фразу ---------------------------------------
    (16080, "example_tr", "Polis hırsızlığı soruşturuyor",
     "Polis bu davayı soruşturuyor",
     "немецкий «Die Polizei ermittelt in diesem Fall»"),
    (8831, "example_en", "He's really enjoying his retirement",
     "My father is retiring next year",
     "немецкий «Mein Vater geht nächstes Jahr in den Ruhestand»"),
    (17519, "example_en", "Can you turn on the washing machine",
     "Activate two-factor authentication",
     "немецкий «Aktiviere die Zwei-Faktor-Authentifizierung»"),
    (17519, "example_tr", "Yeni kartı telefondan etkinleştirdim",
     "İki faktörlü doğrulamayı etkinleştir", "то же"),
    (18183, "example_en", "They live in an old wooden shack",
     "His room is a totally chaotic pad",
     "немецкий «Sein Zimmer ist eine total chaotische Bude»"),
    (18183, "example_ru", "Мы снимали крохотную комнатёнку у вокзала",
     "Его комнатушка — полный бардак", "то же"),
    (16083, "example_ru", "Он нанёс противнику несколько ударов",
     "Он получил побои в наказание",
     "немецкий «Er bekam Schläge als Strafe» — получил, а не нанёс"),
    (14449, "example_tr", "Dışarıdan garip bir ses geliyor",
     "Müziğin sesleri çok güzeldi",
     "немецкий «Die Klänge der Musik waren wunderschön»"),
    (15475, "example_tr", "Gece don var, çiçekleri içeri al",
     "Bu geceki don çok şiddetliydi",
     "немецкий «Der Frost in dieser Nacht war sehr stark»"),
    (17520, "example_tr", "Polis telsizden destek istedi",
     "Telsizim bozuldu", "немецкий «Mein Funkgerät ist kaputt gegangen»"),
    (1165, "example_uk", "Не треба дратуватися через дрібниці",
     "Не сердься", "немецкий «Ärgere dich nicht»"),
    (16090, "example_ru", "Справку выдают в канцелярии школы",
     "Его адвокатская контора в центре",
     "немецкий «Seine Anwaltskanzlei ist im Zentrum»"),
    (16099, "example_ru", "Мне важна приватность в интернете",
     "Я хочу защитить свою личную жизнь",
     "немецкий «Ich möchte meine Privatsphäre schützen»"),
    (13974, "example_tr", "Yemek son derece lezzetliydi",
     "Bu yaptığın son derece haksızca",
     "немецкий «Das ist ausgesprochen unfair von dir»"),
    (6962, "example_uk", "Він стояв осторонь і мовчав",
     "Відклади це вбік, поговоримо про це пізніше",
     "немецкий «Leg das beiseite, wir sprechen später darüber»"),
    (5, "example_uk", "Ми скасовуємо поїздку через дощ",
     "Мені потрібно скасувати зустріч",
     "немецкий «Ich muss den Termin absagen»"),
    (16106, "example_ru", "У него очень упорядоченный распорядок дня",
     "Мой распорядок дня хорошо налажен",
     "немецкий «Mein Alltag ist gut geregelt» — мой, а не его"),
    (16106, "example_uk", "Усі документи впорядковані за датами",
     "Мій розпорядок дня добре налагоджений", "то же"),
    (16106, "example_tr", "Günlük rutinimiz düzenliydi",
     "Günlük rutinim çok düzenli", "то же"),
    (6965, "example_en",
     "The negotiations were broken off because no agreement was reached",
     "Unfortunately we had to cancel the trip",
     "немецкий «Wir mussten die Reise leider abbrechen»"),
    (6965, "example_uk",
     "Переговори були перервані, тому що не було досягнуто згоди",
     "На жаль, нам довелося перервати поїздку", "то же"),
    (6965, "example_tr",
     "Müzakereler kesildi çünkü bir anlaşmaya varılamadı",
     "Maalesef yolculuğu yarıda kesmek zorunda kaldık", "то же"),
    (18698, "example_tr", "Bu sonsuz beklemeden gerçekten bıktım",
     "Onun sonsuz söylenmelerinden gerçekten bıktım",
     "немецкий про вечное нытьё, а не про ожидание"),
    # --- потеряно или добавлено ------------------------------------------------
    (15013, "example_tr", "Biz uzaktan akrabayız", "Biz akrabayız",
     "«uzaktan» в немецком нет"),
    (10381, "example_tr", "Treni iptal olduğu için oldukça sinirli idi",
     "Treni iptal olduğu için oldukça sinirliydi",
     "«sinirli idi» пишется слитно"),
    (16087, "example_ru", "Арест подозреваемого произошёл с утра",
     "Арест подозреваемого произошёл утром", "«с утра» — не «утром»"),
    (16087, "example_uk", "Арешт підозрюваного стався з ранку",
     "Арешт підозрюваного стався вранці", "то же"),
    (17120, "example_ru", "Транспорт товаров занял три дня",
     "Перевозка товаров заняла три дня", "«транспорт товаров» — канцелярит"),
    (12564, "example_uk",
     "Я пішов до відділення невідкладної допомоги з батьком",
     "Мені довелося поїхати з батьком у відділення невідкладної допомоги",
     "потеряно «musste», и порядок слов"),
    (2197, "example_tr", "Bu iş çok zor ve yıpratıcı", "Bu iş çok yorucu",
     "«zor ve» в немецком нет"),
    (6943, "example_uk", "Я вижимаю сік з лимона", "Я вижимаю лимон",
     "сока в немецком нет"),
    (6943, "example_pl", "Wyciskam sok z cytryny", "Wyciskam cytrynę",
     "то же"),
    (2970, "example_en", "I take care of the family",
     "I provide my family with food", "потеряно «mit Essen»"),
    (2970, "example_uk", "Я забезпечую сім'ю",
     "Я забезпечую свою сім'ю їжею", "то же"),
    (2970, "example_tr", "Aileye bakıyorum", "Aileme yemek sağlıyorum",
     "то же"),
    (6958, "example_tr", "Lütfen olabildiğince çabuk gel",
     "Olabildiğince çabuk geri gel",
     "«Lütfen» в немецком нет, зато потеряно «zurück»"),
    (6937, "example_en", "That turned out to be a big mistake",
     "That will turn out to be a mistake",
     "в немецком будущее время и без «большой»"),
    (6937, "example_uk", "Це виявилося великою помилкою",
     "Це виявиться помилкою", "то же"),
    (6937, "example_tr", "Bu büyük bir hata çıktı",
     "Bu bir hata olarak ortaya çıkacak", "то же"),
    (16092, "example_en", "A slave had no freedom",
     "The slave had no freedom", "в немецком определённый артикль"),
    (15474, "example_tr", "Denizde dalgalar bugün çok büyüktü",
     "Denizdeki dalga bugün çok büyüktü", "в немецком единственное число"),

    # --- слова, которых нет в языке, и опечатки -------------------------------
    (16081, "example_tr", "Gref çok zarif giyimli idi",
     "Kontes çok zarif giyinmişti", "«Gref» — такого слова нет"),
    (8836, "example_tr", "Terzi cekenimi onarıyor",
     "Terzi ceketimi onarıyor", "«cekenimi» — опечатка"),
    (10397, "example_tr", "Davranışı bencil ve haksızdi",
     "Davranışı bencil ve haksızdı", "«haksızdi» — опечатка"),
    (12568, "example_tr", "Bacağındaki yaralanma çok ciddiye değil",
     "Bacağındaki yaralanma çok ciddi değil", "«ciddiye değil» — так не говорят"),
    (10392, "example_tr", "Bu senin kısımda saf oldu",
     "Bu senden saflık oldu", "фраза не складывается"),
    (6942, "example_tr", "Partı için masaları kuruyoruz",
     "Parti için masaları kuruyoruz", "«Partı» — опечатка"),
    (15013, "example_uk", "Ми спорідненні", "Ми споріднені",
     "двойная «н» — опечатка"),
    (16088, "example_tr", "Alman bayrağı siyah, kırmızı ve altın renkleridir",
     "Alman bayrağı siyah, kırmızı ve altın renginde",
     "«renkleridir» — фраза не складывается"),
    (16093, "example_uk", "Шахрай вкрав гроші", "Шахрай украв гроші",
     "«вкрав» после согласной — «украв»"),

    # --- русизмы в украинской колонке ----------------------------------------
    (10398, "example_uk", "Такий болван! Це була дурна ідея",
     "Такий бовдур! Це була дурна ідея", "«болван» — русизм"),
    (16108, "translation_uk", "кат, палач", "кат, виконавець вироку",
     "«палач» — русизм"),
    (13974, "example_uk", "Це явно несправедливо з твоєї сторони",
     "Це явно несправедливо з твого боку", "«з твоєї сторони» — русизм"),
    (10392, "example_uk", "Це було наївно з твоєї сторони",
     "Це було наївно з твого боку", "то же"),
    (8836, "example_uk", "Кравець чинить мою куртку",
     "Кравець лагодить мою куртку", "«чинить» — русизм"),
    (6925, "translation_uk", "практично, майже, так би сказати",
     "практично, майже, так би мовити", "«так би сказати» — калька"),

    # --- грамматика целевого языка --------------------------------------------
    (8838, "example_uk", "Правління прийняла рішення",
     "Правління прийняло рішення", "«правління» середнього роду"),
    (13506, "example_ru", "Я не прочитал ни одну из этих книг",
     "Я не прочитал ни одной из этих книг",
     "при отрицании нужен родительный падеж"),
    (13506, "example_uk", "Я не прочитав жодну з цих книг",
     "Я не прочитав жодної з цих книг", "то же"),
    (13505, "example_uk", "Під столом сиділа кішка",
     "Під столом сидить кішка", "в немецком настоящее время"),
    (13505, "example_tr", "Kedi masanın altında oturuyordu",
     "Kedi masanın altında oturuyor", "то же"),
    (10386, "example_tr", "Annem beni her sabah sarılıyor",
     "Annem her sabah bana sarılıyor", "«sarılmak» требует дательного"),
    (6955, "example_tr", "Kuralları uymalısın", "Kurallara uymalısın",
     "«uymak» требует дательного"),
    (10395, "example_tr", "Bunu dayanamam", "Buna dayanamam", "то же"),
    (16092, "example_tr", "Bir köle özgürlüğü yoktu",
     "Kölenin özgürlüğü yoktu", "пропущен родительный падеж"),
    (6944, "example_tr", "Erkek kedim köpek gelince hep tıslatıyor",
     "Erkek kedim köpek gelince hep tıslıyor",
     "«tıslatıyor» — побудительная форма"),
    (6944, "example_uk", "Мій кіт завжди шипить коли приходить собака",
     "Мій кіт завжди шипить, коли приходить собака", "пропущена запятая"),
    (10400, "example_uk", "Дитина була цілком нахабною до своєї матері",
     "Дитина була дуже нахабною зі своєю матір'ю", "неверный предлог"),
    (6966, "example_uk", "Температура підвищена і дуже гарячо",
     "Температура підвищена, і неприємно тепло",
     "«гарячо» — не та форма, и в немецком «unangenehm warm»"),
    (16105, "example_tr", "Toplantı yarın saat 18:00de yapılacak",
     "Toplantı yarın saat 18.00'de yapılacak",
     "в турецком число берёт апостроф"),

    # --- подменённое значение -------------------------------------------------
    (6927, "translation_tr", "yedek, ikame, yerine geçen şey",
     "yedek, ikame, alternatif",
     "«yedek» о напитке не говорят, нужен «alternatif»"),
    (6927, "example_tr", "Kahve çay için iyi bir yedek",
     "Kahve, çayın iyi bir alternatifi", "то же"),
    (6936, "example_tr", "Bu sıkı bir tutamdır", "Bu sıkı bir tutuş",
     "«tutam» — щепотка, а «Griff» это хват"),
    (18184, "example_tr", "Odamı temizlemem gerekiyor",
     "Odamı toplamam gerekiyor",
     "«temizlemek» — мыть; «aufräumen» это убирать"),
    (16101, "example_tr", "Polis binayı bütün gece gözetliyor",
     "Polis binayı bütün gece koruyor",
     "«gözetlemek» — подглядывать; «bewachen» это охранять"),
    (16090, "example_tr", "Avukatlık bürosu şehir merkezindedir",
     "Onun avukatlık bürosu şehir merkezinde",
     "«-dir» канцелярит, и потеряно «его»"),
    (14450, "example_tr", "Vaiz kilisede vaaz verdi",
     "Papaz kilisede vaaz verdi", "в значениях стоит «papaz»"),
    (16097, "example_uk", "Секретна служба стежить за підозрілими особами",
     "Спецслужба стежить за підозрілими особами",
     "в значениях первым стоит «спецслужба»"),
    (15478, "example_uk", "Коні в конюшні і чекають на їжу",
     "Коні в конюшні і чекають на корм", "«Futter» — корм, не еда"),
    (10393, "example_ru", "Мне охота пиццы", "Мне хочется пиццы",
     "«мне охота пиццы» — так не говорят"),
    (10393, "example_uk", "У мене немає охоти сваритися",
     "Мені хочеться піци", "немецкий «Ich habe Bock auf Pizza»"),
    (10393, "example_tr", "Pizza isteği var", "Canım pizza çekiyor",
     "то же, и фраза не складывается"),
    (6933, "example_uk", "Я помічаю, що він нервний",
     "Я помічаю, що він нервує", "«нервний» — черта, а не состояние"),
    (6961, "example_tr", "Sosyal medyadaki durumu çok özeldir",
     "Sosyal medyadaki statüsü çok özel",
     "«durum» — состояние; в значениях «statü»"),
    (13975, "translation_uk", "зрозумілий, ясний, виразний, природний",
     "зрозумілий, ясний, виразний",
     "«природний» не значение слова «verständlich»"),

    # --- говорить по-людски ---------------------------------------------------
    (6925, "example_tr", "Bu hemen hemen bir garantidir",
     "Bu hemen hemen bir garanti", "«-dir» — канцелярит"),
    (10380, "example_tr", "Bu sadece tembel bir bahanedir",
     "Bu sadece boş bir bahane",
     "«tembel bahane» — калька с немецкого «faule Ausrede»"),
    (15472, "example_tr", "Muz artık olgun ve tatlı tadı var",
     "Muzlar artık olgun ve tatlı", "фраза не складывается"),
    (15012, "example_uk", "Громада допомагає одна одній",
     "Спільнота допомагає одне одному", "«одна одній» — не та форма"),
    (10401, "example_uk", "Вчора він був дуже п'яний і міг ледве ходити",
     "Вчора він був дуже п'яний і ледве міг ходити", "порядок слов"),
    (18697, "example_ru", "К настоящему времени я понял, в чём дело",
     "Теперь я понял, в чём дело", "«к настоящему времени» — канцелярит"),
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

    print(f"=== правок {len(ok) + len(skipped)}, совпало {len(ok)}, "
          f"пропущено {len(skipped)} ===\n")
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
