"""
Сплошная вычитка, блоки 8 и 9: ряды 701–900 по рангу частотности.

Находки:

* `Willen` — из пяти переводов к немецкому «Das war gegen meinen Willen» не
  подходил ни один: английский про силу воли и курение, украинский про
  голосование, турецкий про мать, польский про упорство.
* `Güte` — немецкий «Ach du meine Güte» это возглас, а украинский,
  турецкий и польский благодарят за доброту. Взято другое значение.
* `Nase` — немецкий «у клоуна красный нос», а три языка жалуются на
  кровь из носа.
* `singen`, `fernsehen`, `melden` — то же: немецкий говорит о себе, а
  переводы о детях, о вечерах и о полиции.
* `vorne` — украинское «сидю» вместо «сиджу».
* `nahe` — немецкий пример «Das Geschäft in Berlin ist ganz nahe» странен
  сам: близко к чему? Берлин убран, и переводы приведены к одному виду.
* `Tante` — в украинских значениях «тьотя», такого слова нет.
* `sauer` — в украинских значениях «образився», это глагол среди
  прилагательных.

    python -m app.scripts.fix_block_0008            # показать
    python -m app.scripts.fix_block_0008 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# (id, колонка, что стоит сейчас, на что менять, зачем)
FIXES: list[tuple[int, str, str, str, str]] = [

    # --- слова, которых нет в языке, и опечатки -------------------------------
    (14923, "translation_uk", "тітка, тьотя", "тітка",
     "«тьотя» — такого слова в украинском нет"),
    (10095, "translation_uk", "кислий, злий, образився",
     "кислий, злий, ображений",
     "«образився» — глагол среди прилагательных"),
    (15938, "translation_uk", "армія, війско", "армія, військо",
     "«війско» — опечатка"),
    (998, "example_uk", "Я сидю попереду", "Я сиджу попереду",
     "«сидю» — такой формы нет, нужно «сиджу»"),
    (10101, "example_tr", "Hala umudım var", "Hâlâ umudum var",
     "«umudım» — опечатка; и «hâlâ» с циркумфлексом"),
    (15946, "example_tr", "Hakim çok sert", "Hâkim çok sert",
     "без циркумфлекса «hakim» читается иначе"),

    # --- немецкий пример странен сам ------------------------------------------
    (6387, "example_de", "Das Geschäft in Berlin ist ganz nahe",
     "Das Geschäft ist ganz nahe",
     "«магазин в Берлине совсем близко» — близко к чему?"),
    (6387, "example_ru", "Магазин в Берлине совсем близко",
     "Магазин совсем близко", "вслед за немецким"),
    (6387, "example_pl", "Sklep w Berlinie jest całkiem blisko",
     "Sklep jest całkiem blisko", "вслед за немецким"),

    # --- пример переводит другую фразу ----------------------------------------
    (17055, "example_pl", "Popłyniemy łódką po jeziorze", "Płyniemy łódką",
     "«по озеру» в немецком нет, и время настоящее"),
    (773, "example_uk", "Мені болить спина", "У мене болить спина",
     "по-украински «у мене болить»"),
    (416, "example_tr", "Açlıktan midem ağrıyor", "Açım",
     "в немецком просто «я голоден»"),
    (6355, "example_tr", "Pencereyi açmak ister misin?",
     "Kapıyı açabilir misin?", "в немецком дверь, а не окно"),
    (10088, "example_pl", "Podobno w tym domu mieszka duch",
     "Nie wierzę w duchy", "в немецком «я не верю в духов»"),
    (13403, "example_en", "Its at least warm here",
     "It's at least warm here", "«Its» без апострофа"),
    (13403, "example_pl", "Przynajmniej nie pada deszcz",
     "Przynajmniej jest tu ciepło", "в немецком «по крайней мере, тепло»"),
    (14917, "example_uk", "Я тут народжений", "Я тут народився",
     "«я тут народжений» по-украински не говорят"),
    (6359, "example_ru", "Я это доказать могу", "Я могу это доказать",
     "порядок слов"),
    (15938, "example_ru", "Армия марширует",
     "Армия марширует по Берлину", "потеряно «через Берлин»"),
    (15938, "example_uk", "Армія марширує",
     "Армія марширує Берліном", "потеряно «через Берлин»"),
    (15938, "example_tr", "Ordu yürüyor",
     "Ordu Berlin'de yürüyüş yapıyor", "потеряно «через Берлин»"),
    (1400, "example_tr", "Bir telefon çağrısı bekliyorum",
     "Bir telefon bekliyorum", "«telefon çağrısı» по-турецки не говорят"),
    (10091, "example_pl", "Chyba jestem w niej zakochany",
     "Jestem zakochany", "«chyba» и «в неё» в немецком нет"),
    (1398, "example_uk", "Як я можу з вами зв'язатися?",
     "Як я можу з тобою зв'язатися?", "в немецком «dich» — тобой"),
    (10092, "example_pl", "Policja szuka zaginionego chłopca",
     "Mój pies zaginął", "в немецком пропала собака, а не мальчик"),
    (6364, "example_uk", "Наша команда набрала три очки",
     "Цей пункт важливий", "в немецком «этот пункт важен»"),
    (1755, "example_uk", "Це моя особиста справа", "Я зайду особисто",
     "в немецком «я зайду лично»"),
    (1755, "example_tr", "Bunu sana şahsen söylemek istedim",
     "Şahsen uğrayacağım", "в немецком «я зайду лично»"),
    (642, "example_en", "My nose is bleeding",
     "The clown has a red nose", "в немецком про нос клоуна"),
    (642, "example_uk", "У мене кровоточить ніс", "У клоуна червоний ніс",
     "в немецком про нос клоуна"),
    (642, "example_tr", "Burnum kanıyor",
     "Palyaçonun kırmızı bir burnu var", "в немецком про нос клоуна"),
    (14922, "example_en", "Our relationship is broken",
     "We have a good relationship",
     "в немецком отношения хорошие, а не разрушенные"),
    (14922, "example_tr", "İlişkimiz bitti", "İyi bir ilişkimiz var",
     "в немецком отношения хорошие, а не кончились"),
    (10095, "example_pl", "Te jabłka są bardzo kwaśne",
     "Ten chleb jest dla mnie za kwaśny",
     "в немецком хлеб, а не яблоки"),
    (784, "example_en", "What a pity you can't come!", "That's a pity",
     "в немецком просто «это жаль»"),
    (784, "example_tr", "Bu yazık", "Çok yazık",
     "«bu yazık» по-турецки не говорят"),
    (10097, "example_uk", "Твоя доброта мене дуже зворушила",
     "Ах ти Боже мій!",
     "в немецком это возглас, а не благодарность за доброту"),
    (10097, "example_tr", "İyiliğini asla unutmayacağım", "Aman Tanrım",
     "в немецком это возглас, а не благодарность"),
    (10097, "example_pl", "Dziękuję ci za twoją dobroć", "O mój Boże",
     "в немецком это возглас, а не благодарность"),
    (10098, "example_en", "It takes willpower to quit smoking",
     "That was against my will", "в немецком «это было против моей воли»"),
    (10098, "example_uk", "Я голосую за цю пропозицію",
     "Це було проти моєї волі", "в немецком «это было против моей воли»"),
    (10098, "example_tr", "Annemin hatırı için sustum",
     "Bu benim isteğim dışındaydı", "в немецком «против моей воли»"),
    (10098, "example_pl", "Ma silną wolę i nigdy się nie poddaje",
     "To było wbrew mojej woli", "в немецком «против моей воли»"),
    (840, "example_en", "Let's sing a song together", "I like to sing",
     "в немецком «я люблю петь»"),
    (840, "example_uk", "Діти співають", "Я люблю співати",
     "в немецком «я люблю петь»"),
    (840, "example_tr", "Çocuklar şarkı söylüyor",
     "Şarkı söylemeyi severim", "в немецком «я люблю петь»"),
    (1720, "example_en", "One thing is missing, namely money",
     "I can't, you see I'm sick", "в немецком «я не могу, ведь я болен»"),
    (10100, "example_pl", "Nie zdradzę twojej tajemnicy",
     "To moja tajemnica", "в немецком «это моя тайна»"),
    (10101, "example_pl", "Mam jeszcze nadzieję, że się uda",
     "Mam jeszcze nadzieję", "вторая половина в немецком отсутствует"),
    (501, "example_uk", "Будь ласка, встановіть контакт",
     "Будь ласка, встанови контакт", "в немецком «nimm» — ты"),
    (501, "example_tr", "Lütfen iletişime geçin", "Lütfen iletişime geç",
     "в немецком «nimm» — ты"),
    (318, "example_uk", "Він сидить навпроти мене",
     "Кафе розташоване навпроти мене", "в немецком про кафе, а не про него"),
    (318, "example_tr", "Kafe karşısında", "Kafe karşımda",
     "потеряно «напротив меня»"),
    (1396, "example_uk", "Мені ще потрібно дещо виконати",
     "Мені потрібно ще швидко дещо зробити", "потеряно «быстро»"),
    (6370, "example_uk", "Вона, очевидно, вже не прийде",
     "Це очевидно неправильно", "в немецком «это очевидно неправильно»"),
    (1906, "example_uk", "Встав ключ у замок", "Встав вилку в розетку",
     "в немецком вилка и розетка, а не ключ и замок"),
    (1906, "example_en", "Plug it in", "Put the plug in the socket",
     "потеряны вилка и розетка"),
    (6377, "example_tr", "Bunu hayatta kalmalıyız", "Bunu atlatmalıyız",
     "«hayatta kalmak» не принимает дополнения"),
    (13409, "example_pl", "Albo idziemy teraz, albo wcale",
     "Albo przyjdziesz, albo ja idę",
     "в немецком «либо ты придёшь, либо я уйду»"),
    (1053, "example_uk", "Я живу в Мюнхені", "Я живу в місті",
     "в немецком «в городе», Мюнхена там нет"),
    (1053, "example_tr", "Münih'te oturuyorum", "Şehirde oturuyorum",
     "в немецком «в городе», Мюнхена там нет"),
    (2573, "example_uk", "Ми впоралися шляхом того, що працювали разом",
     "Я допомагаю тим, що беру участь у роботі",
     "в немецком «я помогаю тем, что участвую»"),
    (17057, "example_pl", "Wszyscy pasażerowie są już na pokładzie",
     "Jesteśmy na pokładzie statku", "в немецком «мы на борту корабля»"),
    (12098, "example_tr", "Bu benim zevkim", "Benim için bir zevk",
     "«bu benim zevkim» значит «это мой вкус»"),
    (13412, "example_pl", "Rozmawiajmy ze sobą spokojnie",
     "Rozmawiamy ze sobą", "в немецком утверждение, а не призыв"),
    (1726, "example_uk", "Я нервовий", "Я знервований",
     "«я нервовий» — о характере, а в немецком о состоянии"),
    (10107, "example_pl", "Jestem zdziwiony tą wiadomością",
     "Jestem bardzo zdziwiony", "«этой новостью» в немецком нет"),
    (2830, "example_uk", "Наскільки я знаю",
     "Наскільки я знаю, він прийде завтра",
     "потеряна вторая половина фразы"),
    (2160, "example_en", "That's correct, however I didn't see him",
     "That's correct, though", "вторая половина в немецком отсутствует"),
    (2160, "example_uk", "Це правда, утім я його не бачив",
     "Це таки правда", "вторая половина в немецком отсутствует"),
    (2160, "example_tr", "Bu doğru, ancak", "Bu gerçekten doğru",
     "фраза оборвана на союзе"),
    (13416, "example_en", "Nobody was home when I arrived",
     "I'm not telling anybody anything",
     "в немецком «я никому ничего не говорю»"),
    (13416, "example_uk", "Я нікому нічого не скажу",
     "Я нікому нічого не кажу", "в немецком настоящее время"),
    (13416, "example_tr", "Kimseye hiçbir şey söylemeyeceğim",
     "Kimseye hiçbir şey söylemiyorum", "в немецком настоящее время"),
    (1530, "example_uk", "Заходь усередину, там тепло",
     "Заходь, будь ласка, усередину!", "«там тепло» в немецком нет"),
    (1530, "example_tr", "Lütfen içeri gelin!", "Lütfen içeri gel!",
     "в немецком «Komm» — ты"),
    (10110, "example_en", "Congratulations, you passed the exam!",
     "Happy birthday!", "в немецком поздравление с днём рождения"),
    (10110, "example_tr", "Tebrik kartını çok beğendim",
     "Doğum günün kutlu olsun", "в немецком поздравление с днём рождения"),
    (261, "example_pl", "W sobotę świętujemy urodziny taty",
     "W sobotę świętujemy", "«день рождения папы» в немецком нет"),
    (15381, "example_tr", "Buranın bölgesi güzel", "Buradaki bölge güzel",
     "по-турецки так не говорят"),
    (2429, "example_uk", "Я тебе не розпізнаю", "Я тебе не впізнаю",
     "«розпізнавати» о людях не говорят"),
    (2358, "example_tr", "Dışarısı soğuk, içeride kal",
     "İçeride kal, yağmur yağıyor", "в немецком дождь, а не холод"),
    (6389, "example_tr", "İlk defa uçağa biniyorum",
     "Bu benim burada ilk günüm", "в немецком «мой первый день здесь»"),
    (1684, "example_en", "Please report the accident to the police",
     "I'm reporting in sick", "в немецком «я сообщаю, что болен»"),
    (1684, "example_uk", "Повідом мені, коли приїдеш",
     "Я повідомляю, що захворів", "в немецком «я сообщаю, что болен»"),
    (1684, "example_tr", "Adres değişikliğini belediyeye bildirdim",
     "Hasta olduğumu bildiriyorum", "в немецком «я сообщаю, что болен»"),
    (10113, "example_tr", "Midem kötü", "Midem bulanıyor",
     "«midem kötü» по-турецки не говорят"),
    (10113, "example_uk", "Мене нудить від цього запаху", "Мене нудить",
     "«от этого запаха» в немецком нет"),
    (18613, "example_en", "She previously worked at our office",
     "I have never seen that before",
     "в немецком «этого я прежде не видел»"),
    (265, "example_en", "I watch TV in the evening",
     "I just want to watch TV now",
     "в немецком «хочу сейчас только смотреть телевизор»"),
    (265, "example_uk", "Я дивлюся телевізор увечері",
     "Я хочу зараз тільки дивитися телевізор",
     "в немецком «хочу сейчас только смотреть телевизор»"),
    (265, "example_tr", "Akşamları televizyon izliyorum",
     "Şimdi sadece televizyon izlemek istiyorum",
     "в немецком «хочу сейчас только смотреть телевизор»"),
    (1337, "example_uk", "Мені пора повертатися додому", "Обернись",
     "в немецком «обернись», а не «пора домой»"),
    (1337, "example_tr", "Anahtarı sağa çevir", "Arkanı dön",
     "в немецком «обернись», а не «поверни ключ»"),
    (2482, "example_tr", "Gözlerinde büyük bir sevinç vardı",
     "Bu bana büyük sevinç veriyor",
     "в немецком «это доставляет мне радость»"),
    (13422, "example_uk", "Перед цим я подзвоню мамі", "Я цього боюся",
     "в немецком «я этого боюсь»"),
    (13422, "example_pl", "Bardzo się tego boję", "Boję się tego",
     "«bardzo» в немецком нет"),

    # --- запятые и вежливая форма ----------------------------------------------
    (18609, "example_ru", "Он вероятно опоздает", "Он, вероятно, опоздает",
     "вводное слово выделяется запятыми"),
    (18609, "example_uk", "Він ймовірно спізниться",
     "Він, імовірно, спізниться",
     "вводное слово выделяется запятыми; и «імовірно»"),
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
