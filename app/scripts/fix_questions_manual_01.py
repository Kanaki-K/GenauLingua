"""
Потерянная вопросительная форма, партия 1 из списка `scan_question_mark`.

Эти ячейки сторож намеренно не тронул: там потерян не знак, а само
предложение. Знак бы сделал из неверного утверждения неверный вопрос.

«Wie heißt du?» — «The little dog is called Rex». «Möchtest du noch etwas
Saft?» — «Я п'ю яблучний сік». «Wie soll die neue Küche aussehen?» — «Ти
виглядаєш втомленою», и то же в английском и турецком: ряд `aussehen`
переведён во всех трёх языках не про кухню, а про усталый вид.

Вторая половина партии — вежливая форма. Немецкий спрашивает на «ты»
(«deine Adresse», «dein Beruf»), а турецкий отвечает на «Вы»:
«Adresiniz nedir», «Mesleğiniz nedir». Для анкетных слов это особенно
заметно: там таких рядов подряд десяток.

Ряды 1328 (`du`) в партию не включены: это ряд-дубликат, которому нужно
решение владельца — см. HANDOVER, пункт 1a.

    python -m app.scripts.fix_questions_manual_01            # показать
    python -m app.scripts.fix_questions_manual_01 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# (id, колонка, что стоит сейчас, на что менять, зачем)
FIXES: list[tuple[int, str, str, str, str]] = [

    # --- потерян только знак (форма вопроса без частицы) ----------------------
    (126, "example_uk", "У тебе є олівець", "У тебе є олівець?",
     "вопрос без частицы: потерян только знак"),
    (223, "example_pl", "Przepraszam, gdzie jest toaleta",
     "Przepraszam, gdzie jest toaleta?", "потерян только знак"),
    (239, "example_pl", "Chcesz coś do picia", "Chcesz coś do picia?",
     "потерян только знак"),
    (241, "example_tr", "Adresiniz nedir", "Adresiniz nedir?",
     "потерян только знак; здесь «eure» — множественное, форма верна"),
    (717, "example_uk", "Тут є вільне місце", "Тут є вільне місце?",
     "потерян только знак"),
    (741, "example_uk", "У тебе є гумка", "У тебе є гумка?",
     "потерян только знак"),
    (1035, "example_tr", "Nasılsın", "Nasılsın?", "потерян только знак"),
    (1113, "example_pl", "Możesz mnie podrzucić na dworzec",
     "Możesz mnie podrzucić na dworzec?", "потерян только знак"),
    (1158, "example_uk", "Мені потрібен дозвіл на роботу",
     "Мені потрібен дозвіл на роботу?", "потерян только знак"),
    (1180, "example_uk", "Можеш роздрукувати документ",
     "Можеш роздрукувати документ?", "потерян только знак"),

    # --- в немецком «ты», в переводе «Вы» --------------------------------------
    (8, "example_tr", "Adresiniz nedir", "Adresin ne?",
     "в немецком «deine» — ты; и потерян знак"),
    (96, "example_tr", "Mesleğiniz nedir", "Mesleğin ne?",
     "в немецком «dein» — ты; и потерян знак"),
    (254, "example_tr", "Medeni durumunuz nedir", "Medeni durumun ne?",
     "в немецком «dein» — ты; и потерян знак"),
    (341, "example_uk", "Бажаєте напій", "Хочеш напій?",
     "в немецком «du» — ты; и потерян знак"),
    (636, "example_tr", "Soyadınız nedir", "Soyadın ne?",
     "в немецком «dein» — ты; и потерян знак"),
    (723, "example_tr", "Posta kodu nedir", "Posta kodun ne?",
     "потерян притяжательный аффикс и знак"),
    (921, "example_tr", "Telefon numaranız nedir", "Telefon numaran ne?",
     "в немецком «deine» — ты; и потерян знак"),
    (1054, "example_tr", "İkamet yeriniz neresi", "İkamet yerin neresi?",
     "в немецком «dein» — ты; и потерян знак"),
    (1093, "example_tr", "Hiç yemek istiyor musunuz", "Hiç yemek istiyor musun?",
     "в немецком «du» — ты; и потерян знак"),
    (1215, "example_tr", "Banka kodunuz nedir", "Banka kodun ne?",
     "в немецком «deine» — ты; и потерян знак"),
    (1253, "example_uk", "У якій професійній сфері ви працюєте",
     "У якій професійній сфері ти працюєш?",
     "в немецком «du» — ты; и потерян знак"),
    (1267, "example_tr", "Sipariş numaranız nedir", "Sipariş numaran ne?",
     "в немецком «deine» — ты; и потерян знак"),

    # --- перевод переводит другое предложение ---------------------------------
    (253, "example_pl", "Proszę podać imię i nazwisko",
     "Jakie jest twoje nazwisko?",
     "в немецком вопрос про фамилию, а не просьба заполнить"),
    (254, "example_pl", "W formularzu wpisz swój stan cywilny",
     "Jaki jest twój stan cywilny?",
     "в немецком вопрос, а не указание в формуляре"),
    (394, "example_en", "The little dog is called Rex", "What is your name?",
     "в немецком «как тебя зовут», а не про собаку"),
    (394, "example_tr", 'Bu kelime "su" anlamına geliyor', "Adın ne?",
     "в немецком «как тебя зовут», а не про значение слова"),
    (445, "example_uk", "Назви мені рік", "Який це рік?",
     "в немецком вопрос, а не повеление"),
    (469, "example_en", "We go to the department store",
     "Shall we go to the department store?",
     "в немецком это предложение-вопрос"),
    (469, "example_tr", "Büyük mağazaya gidiyoruz",
     "Büyük mağazaya gidelim mi?", "в немецком это предложение-вопрос"),
    (469, "example_uk", "Ми йдемо до універмагу", "Ідемо до універмагу?",
     "в немецком это предложение-вопрос"),
    (507, "example_tr", "Yeni telefon bana çok pahalıya mal oldu",
     "Bu ne kadar?", "пример про дорогой телефон, а немецкий «сколько это стоит»"),
    (548, "example_en", "She likes to read before bed",
     "Can you read that out loud, please?", "пример про другое"),
    (548, "example_tr", "Bir kitap okuyor",
     "Bunu yüksek sesle okuyabilir misin?", "пример про другое"),
    (548, "example_uk", "Прочитай мені цей лист",
     "Можеш прочитати це вголос?", "в немецком вопрос, а не повеление"),
    (706, "example_uk", "Столик на дві особи, будь ласка",
     "Скільки вас осіб?", "пример про другое"),
    (775, "example_en", "I drink apple juice",
     "Would you like some more juice?", "пример про другое"),
    (775, "example_tr", "Elma suyu içiyorum",
     "Biraz daha meyve suyu ister misin?", "пример про другое"),
    (775, "example_uk", "Я п’ю яблучний сік", "Хочеш ще соку?",
     "пример про другое"),
    (979, "example_uk", "У місті зручний громадський транспорт",
     "Яким транспортом ти їздиш?", "пример про другое"),
    (1054, "example_uk", "Моє місце проживання — місто Львів",
     "Яке твоє місце проживання?", "в немецком вопрос, а не ответ"),
    (1106, "example_en", "The technician reads the meter",
     "Can you read the meter?", "в немецком вопрос «ты», а не про техника"),
    (1106, "example_tr", "Teknisyen sayacı okuyor",
     "Sayacı okuyabilir misin?", "в немецком вопрос «ты», а не про техника"),
    (1106, "example_uk", "Технік зчитує показники лічильника",
     "Можеш зчитати показники лічильника?",
     "в немецком вопрос «ты», а не про техника"),
    (1113, "example_uk", "Батько висаджує мене біля школи",
     "Можеш висадити мене біля вокзалу?",
     "пример про отца и школу, а немецкий про вокзал"),
    (1137, "example_tr", "Üzerinde mavi bir gömlek var",
     "Bu akşam ne giymek istiyorsun?",
     "пример про синюю рубашку, а немецкий спрашивает, что надеть"),
    (1171, "example_en", "Please pick up the trash",
     "Can you pick up the paper?", "в немецком бумага и вопрос, а не мусор"),
    (1171, "example_tr", "Düşen anahtarı yerden aldım",
     "Kâğıdı yerden alabilir misin?", "пример про ключ в прошедшем времени"),
    (1171, "example_uk", "Будь ласка, підніми сміття",
     "Можеш підняти папір?", "в немецком бумага и вопрос, а не мусор"),
    (1172, "example_en", "Stop talking", "Can you please stop that?",
     "в немецком вопрос, и «говорить» там нет"),
    (1172, "example_tr", "Konuşmayı bırak", "Lütfen bunu bırakabilir misin?",
     "в немецком вопрос, и «говорить» там нет"),
    (1172, "example_uk", "Припини говорити", "Можеш, будь ласка, це припинити?",
     "в немецком вопрос, и «говорить» там нет"),
    (1194, "example_en", "You look tired",
     "What should the new kitchen look like?",
     "взято другое значение: «выглядеть усталым» вместо «как должна выглядеть кухня»"),
    (1194, "example_tr", "Sen yorgun görünüyorsun",
     "Yeni mutfak nasıl görünsün?", "то же"),
    (1194, "example_uk", "Ти виглядаєш втомленою",
     "Якою має виглядати нова кухня?", "то же"),
    (1235, "example_uk", "Він завжди обґрунтовує свої рішення",
     "Чи можете Ви це обґрунтувати?",
     "в немецком вопрос на «Вы», а не рассказ о нём"),
    (1294, "example_uk", "Можеш розпиляти дошку",
     "Можеш допомогти мені розпилити дошку?",
     "потеряно «помочь мне»; и знак"),
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
