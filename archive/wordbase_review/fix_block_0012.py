"""
Сплошная вычитка, блоки 12 и 13: ряды 1101–1300 по рангу частотности.

Правки сделаны уже с новым прицелом — говорить по-людски (REVIEW_CRITERIA,
пункт 0). Находки:

* `Mond` — в украинских значениях «луна». По-украински «луна» это эхо, а
  луна на небе — «місяць». Человек выучил бы не то слово.
* `gebraucht` — в русских значениях «подержанный, б, у, использованный»:
  сокращение «б/у» рассыпалось на две буквы, когда из базы убирали слеши.
* `langweilig`, `erlauben`, `schweigen`, `unschuldig`, `blind` — русизмы и
  опечатки в списках значений: «скучний», «позволяти», «молчати»,
  «невиновний», польское «slepy» без диакритики.
* `rauchen`, `Scherz` — английские «He doe's not smoke» и «That wa's just a
  joke»: апостроф внутри слова, третий случай той же порчи.
* `Regen`, `verflucht`, `enden` — примеры обрублены или про другое:
  «Насувається дощ» вместо «под дождём мы промокли».
* `selben` — в немецком «den selben» раздельно, правильно «denselben».
* `Star` — «Mein Lieblings-Star» через дефис, по-немецки «Lieblingsstar».

    python -m app.scripts.fix_block_0012            # показать
    python -m app.scripts.fix_block_0012 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# (id, колонка, что стоит сейчас, на что менять, зачем)
FIXES: list[tuple[int, str, str, str, str]] = [

    # --- неверное слово в списке значений -------------------------------------
    (611, "translation_uk", "місяць, луна, супутник", "місяць, супутник",
     "«луна» по-украински значит «эхо», а не небесное тело"),
    (1452, "translation_ru", "подержанный, б, у, использованный",
     "подержанный, бывший в употреблении, использованный",
     "«б/у» рассыпалось на две буквы при уборке слешей"),
    (538, "translation_uk", "нудний, скучний", "нудний",
     "«скучний» — русизм"),
    (1395, "translation_uk", "дозволяти, позволяти", "дозволяти",
     "«позволяти» — русизм"),
    (13887, "translation_uk", "молчати, мовчати, замовкнути",
     "мовчати, замовкнути", "«молчати» — русизм"),
    (15958, "translation_uk", "невинний, невиновний, безневинний",
     "невинний, безневинний", "«невиновний» — русизм"),
    (12488, "translation_pl", "niewidomy, slepy, bezkrytyczny",
     "niewidomy, ślepy, bezkrytyczny", "«slepy» без диакритики"),
    (1907, "translation_uk", "крати, красти, вкрасти", "красти, вкрасти",
     "«крати» — опечатка"),

    # --- апостроф внутри слова -------------------------------------------------
    (745, "example_en", "He doe's not smoke", "He does not smoke",
     "апостроф внутри «does»"),
    (13881, "example_en", "That wa's just a joke", "That was just a joke",
     "апостроф внутри «was»"),
    (13452, "example_en", "Despite the rain, were going for a walk",
     "Despite the rain, we're going for a walk",
     "«were» без апострофа — другое слово"),
    (6519, "example_en", "Were looking for cover from the rain",
     "We're looking for cover from the rain",
     "«Were» без апострофа — другое слово"),

    # --- ошибки в немецком эталоне -------------------------------------------
    (13455, "example_de", "Wir haben den selben Geschmack",
     "Wir haben denselben Geschmack", "«denselben» пишется одним словом"),
    (14382, "example_de", "Mein Lieblings-Star singt heute",
     "Mein Lieblingsstar singt heute", "дефис здесь не нужен"),

    # --- пример переводит другую фразу ----------------------------------------
    (10146, "example_en", "You need to calm down",
     "Calm down, everything will be fine",
     "в немецком «успокойся, всё будет хорошо»"),
    (10146, "example_uk", "Ти маєш заспокоїтися",
     "Заспокойся, все буде добре", "в немецком «успокойся, всё будет хорошо»"),
    (10146, "example_tr", "Sakinleşmen gerek",
     "Sakin ol, her şey yoluna girecek",
     "в немецком «успокойся, всё будет хорошо»"),
    (1731, "example_en", "I normally get up at seven", "I normally walk",
     "в немецком «обычно я хожу пешком»"),
    (6465, "example_en", "She lives far from here",
     "The place is too far away", "в немецком «это место слишком далеко»"),
    (6465, "example_uk", "Вона живе далеко звідси",
     "Це місце занадто далеко", "в немецком «это место слишком далеко»"),
    (6465, "example_tr", "Buradan çok uzakta yaşıyor", "Bu yer çok uzak",
     "в немецком «это место слишком далеко»"),
    (1946, "example_en", "We're writing a test",
     "We're writing a test tomorrow", "потеряно «завтра»"),
    (1946, "example_uk", "Ми пишемо тест", "Ми пишемо тест завтра",
     "потеряно «завтра»"),
    (1946, "example_tr", "Bir test yapıyoruz", "Yarın bir test yapıyoruz",
     "потеряно «завтра»"),
    (925, "example_uk", "Мій прийом у лікаря в понеділок",
     "Моя зустріч у понеділок", "врача в немецком нет"),
    (8758, "example_uk", "Вона мріє про кар'єру лікарки",
     "Моя кар'єра для мене важлива",
     "в немецком «моя карьера важна для меня»"),
    (9723, "example_uk", "Я заборгував тобі сто гривень",
     "Я ще винен тобі гроші", "гривень в немецком нет"),
    (9723, "example_ru", "Я тебе ещё денег должен",
     "Я тебе ещё должен денег", "порядок слов"),
    (6478, "example_uk", "Рукоятка ножа зламалася", "Ручка зламана",
     "ножа в немецком нет"),
    (710, "example_tr", "Cebimde sadece on sterlin var", "Bu on sterlin",
     "в немецком «это стоит десять фунтов»"),
    (6484, "example_uk", "Пошукай цю книжку в іншому місці",
     "Давай підемо кудись інде", "в немецком «давай пойдём в другое место»"),
    (1102, "example_tr", "Çocukları okuldan almaya gidiyorum",
     "Seni saat 8'de almaya geleceğim",
     "в немецком «я заберу тебя в восемь»"),
    (10160, "example_en", "What a disgrace, he lied to us",
     "That's a disgrace", "вторая половина в немецком отсутствует"),
    (1790, "example_en", "It is raining",
     "We got completely wet in the rain",
     "в немецком «под дождём мы промокли»"),
    (1790, "example_uk", "Насувається дощ", "Під дощем ми зовсім промокли",
     "в немецком «под дождём мы промокли»"),
    (1790, "example_tr", "Yağmur geliyor", "Yağmurda tamamen ıslandık",
     "в немецком «под дождём мы промокли»"),
    (14939, "example_uk", "Дай мені поцілунок на прощання",
     "Вона подарувала йому поцілунок",
     "в немецком «она дала ему поцелуй»"),
    (2808, "example_tr", "Bu tabii ki", "Bu çok doğal",
     "фраза оборвана на середине"),
    (1003, "example_uk", "Одягни теплий светр, надворі вітер",
     "Вода тепла", "в немецком «вода тёплая»"),
    (10161, "example_uk", "Цей проклятий комп'ютер",
     "Цей проклятий комп'ютер просто не працює",
     "потеряна вторая половина фразы"),
    (10161, "example_tr", "Bu lanet bilgisayar",
     "Bu lanet bilgisayar bir türlü çalışmıyor",
     "потеряна вторая половина фразы"),
    (6491, "example_en", "There's nowhere to sit here",
     "I can't find it anywhere", "в немецком «я нигде его не нахожу»"),
    (2403, "example_uk", "Молоко в холодильнику закінчується",
     "Фільм закінчується о 22:00", "в немецком про фильм, а не про молоко"),
    (133, "example_uk", "Наречена в білому платті",
     "Наречена в білій сукні", "«платті» — русизм, по-украински «сукня»"),
    (6497, "example_ru", "Сделай музыку потише, покрути ручку",
     "Сделай музыку потише", "вторая половина приписана"),
    (6497, "example_uk", "Зроби музику потихше", "Зроби музику тихіше",
     "«потихше» — такой формы нет"),
    (6499, "example_uk", "Цей метод знайшов широке застосування",
     "Пожежники на виїзді", "в немецком пожарные на выезде"),
    (6499, "example_tr", "Bu ilacın kullanımı çok kolay",
     "İtfaiye görevde", "в немецком пожарные на выезде"),
    (6501, "example_uk", "Виходить, ти був правий",
     "Для мене це не має сенсу", "в немецком «для меня это бессмысленно»"),
    (6501, "example_tr", "Bu benim için anlam çıkarmıyor",
     "Bu bana hiç anlamlı gelmiyor", "по-турецки так не говорят"),
    (2364, "example_en", "I'm coming as well", "I think likewise",
     "в немецком «я думаю так же»"),
    (10168, "example_en", "I forgive you",
     "I forgive you, don't do it again", "потеряна вторая половина"),
    (10168, "example_uk", "Пробач мені, я забув подзвонити",
     "Я пробачаю тобі, тільки більше так не роби",
     "в немецком прощает говорящий, а не просит прощения"),
    (10168, "example_tr", "Seni çoktan affettim",
     "Seni affediyorum, bir daha yapma", "потеряна вторая половина"),
    (309, "example_uk", "До нас прийшов гість", "У нас гості",
     "в немецком гости во множественном числе"),
    (6506, "example_uk", "Це було багато зусиль даремно",
     "Стільки зусиль — і все даремно", "фраза спотыкается"),
    (6506, "example_tr", "Bu boşuna çok çaba oldu",
     "Bunca çaba boşunaydı", "по-турецки так не говорят"),
    (1395, "example_tr", "Annem dışarı çıkmama izin verdi",
     "Burada sigara içmek yasak", "в немецком про курение, а не про мать"),
    (6509, "example_en", "Let's begin with the easy questions",
     "The movie began at eight", "в немецком «фильм начался в восемь»"),
    (1062, "example_tr", "Vitrindeki en güzel elbiseyi seçtim",
     "Yeni bir cumhurbaşkanı seçiyoruz",
     "в немецком выбирают президента, а не платье"),
    (12108, "example_en", "Tonight we're going out",
     "I'm going out tonight", "в немецком «я», а не «мы»"),
    (12108, "example_uk", "Я виходжу увечері на вулицю",
     "Я йду сьогодні ввечері в місто",
     "«выйти на улицу» и «выйти в город» — разное"),
    (12108, "example_tr", "Bu akşam dışarı çıkıyoruz",
     "Bu akşam dışarı çıkıyorum", "в немецком «я», а не «мы»"),
    (1472, "example_uk", "Я насолоджуюся тишею вранці",
     "Я насолоджуюся тишею", "«вранці» в немецком нет"),
    (672, "example_ru", "Он поранил себе ухо", "Он поранил ухо",
     "«себе» здесь лишнее"),
    (245, "example_pl", "Kierowca już czeka przed domem",
     "Kierowca czeka na ciebie", "в немецком «ждёт тебя», дома там нет"),
    (13455, "example_uk", "Це той самий фільм, що вчора",
     "У нас однаковий смак", "в немецком про вкус, а не про фильм"),
    (15961, "example_tr", "Majesteleri konuşmasına yeni başladı",
     "Hazretleri çok nazik", "в немецком «его высочество очень любезен»"),
    (14945, "example_uk", "Він розлучений уже два роки",
     "Ми живемо окремо вже багато років",
     "в немецком «мы живём раздельно много лет»"),

    # --- неестественно и книжно -------------------------------------------------
    (6474, "example_tr", "Daha sesli konuşabilir misin?",
     "Daha yüksek sesle konuşabilir misin?",
     "«sesli» значит «со звуком», громче — «yüksek sesle»"),
    (10148, "example_tr", "Bu inanılmaz derecede zor idi",
     "Bu inanılmaz derecede zordu", "«idi» отдельно — книжно"),
    (767, "example_pl", "Światło na sygnalizacji jest czerwone",
     "Światło jest czerwone", "лишние слова"),
    (256, "example_pl", "Jaki kolor najbardziej lubisz?",
     "Jaki kolor lubisz?", "«najbardziej» в немецком нет"),
    (17065, "example_pl", "Przeszliśmy wiele mil pieszo",
     "Przeszliśmy wiele mil", "«pieszo» в немецком нет"),
    (10157, "example_uk", "Це був захоплюючий фільм",
     "Це був захопливий фільм",
     "«захоплюючий» — калька, по-украински «захопливий»"),
    (10157, "example_pl", "To był naprawdę wciągający film",
     "To był wciągający film", "«naprawdę» в немецком нет"),
    (10152, "example_uk", "Речі лежали безладно на підлозі",
     "Усе геть переплуталося", "в немецком «всё перепуталось»"),
    (6496, "example_uk", "Ти не помічаєш, що він брешеш?",
     "Ти не помічаєш, що він бреше?", "неверное лицо глагола"),
    (1612, "example_tr", "Lütfen faturayı kontrol edin",
     "Lütfen faturayı kontrol et", "в немецком «kontrollier» — ты"),
    (895, "example_tr", "Sandalyeye oturun", "Sandalyeye otur",
     "в немецком «Setz dich» — ты"),
    (291, "example_uk", "Вона дуже привітна", "Ти дуже привітний",
     "в немецком «du» — ты"),
    (291, "example_tr", "O çok canayakın", "Sen çok cana yakınsın",
     "«cana yakın» пишется раздельно; и в немецком «du»"),
    (1907, "example_en", "Someone tried to steal my phone",
     "He wanted to steal my money", "в немецком «он хотел украсть деньги»"),
    (1907, "example_uk", "Хтось украв мій велосипед",
     "Він хотів украсти мої гроші", "в немецком «он хотел украсть деньги»"),
    (1907, "example_tr", "Biri bisikletimi çaldı",
     "Paramı çalmak istedi", "в немецком «он хотел украсть деньги»"),
    (182, "example_uk", "Він працює на службі",
     "Він працює на службі в поліції", "потеряна полиция"),
    (182, "example_tr", "Görevde çalışıyor",
     "Polis teşkilatında çalışıyor", "потеряна полиция"),
    (611, "example_tr", "Ay parlak görünüyor", "Ay pırıl pırıl parlıyor",
     "в немецком луна светит, а не «выглядит яркой»"),
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
