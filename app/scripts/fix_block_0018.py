"""
Сплошная вычитка, блок 18: ряды 1901–2100 по рангу частотности
(id первого 16008, id последнего 242).

Находки:

* `nichts` — немецкий «Ich habe nichts davon gewusst», а четыре языка из
  пяти говорят «я ничего не делал». Другая фраза во всех сразу.
* `Appetit` — «Guten Appetit» это пожелание за столом, а английский,
  украинский и турецкий рассказывали про аппетит после болезни и у
  ребёнка. Польский желал «Dobrego apetytu» — калька, по-польски
  «Smacznego».
* `versprechen` — немецкий обещает мороженое, английский и украинский
  просят быть осторожным, турецкий тоже.
* `Kopie` — в немецком копия паспорта, в английском «этого документа», у
  украинского и турецкого просто «копия».
* `Atem`, `Reporter`, `umziehen`, `räumen`, `darunter`, `Anzeige`, `mal`,
  `umso`, `Führung`, `Lärm`, `Kette`, `Feier`, `Spielchen`, `schalten`,
  `schieben`, `leihen`, `weitergehen` — то же: перевод переводит другую
  фразу.
* `Bär` — битый эталон: «einen großen Bär» вместо «einen großen Bären».
  Слабое склонение, и карточка учит неверной форме всех шесть языков.
* `bewaffnet` — польское «z bronią» лежит в базе как «z broniÄ…»: utf-8
  прочитан как latin-1. Проверка на диакритику такое не видит. Сплошной
  поиск по всей базе (`scan_mojibake`) показал: такая ячейка одна.
* `Krone` — украинское «Король носити золоту корону»: инфинитив вместо
  формы третьего лица.
* `Haken` — украинское «Повіс пальто» это прошедшее время, а нужен приказ.
* `Teddy` — «плюшевий мишка» в украинском: мишка это мышь. И турецкое
  «Teddy ayı» — немецкое слово в турецкой колонке.
* `Gewicht` — «мой вес слишком высокий» в четырёх языках: вес бывает
  большой, а высоким бывает рост.
* `heutig` — «в сегодняшнее время всё очень быстро»: такого оборота нет.
* `derselbe`, `scheinbar`, `mitmachen`, `Pilot`, `Eile`, `Knarre` —
  русизмы в украинской колонке и ломаный турецкий.
* `Höhe` — турецкое «seyreleşiyor»: такого глагола нет, есть «seyrelmek».

Заголовок `jung` (id 14981) не тронут намеренно: в базе он стоит дважды —
14901 это A1 «молодой», а 14981 все пять языков переводят как «младше»,
то есть это `jünger` с затёртым заголовком. Правка заголовка — решение
владельца, см. HANDOVER.

    python -m app.scripts.fix_block_0018            # показать
    python -m app.scripts.fix_block_0018 --apply    # применить
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
    (3008, "example_uk", "Концерт продовжується ще годину", "Ходімо далі",
     "немецкий «Lass uns weitergehen» — приглашение идти дальше, а не концерт"),
    (1153, "example_en", "All this walking gave me an appetite",
     "Enjoy your meal", "«Guten Appetit» — пожелание за столом"),
    (1153, "example_uk", "У дитини сьогодні чудовий апетит", "Смачного!",
     "то же: пожелание, а не рассказ про ребёнка"),
    (1153, "example_tr", "Hastalıktan sonra iştahım geri geldi",
     "Afiyet olsun", "то же: пожелание, а не аппетит после болезни"),
    (1153, "example_pl", "Dobrego apetytu!", "Smacznego!",
     "«Dobrego apetytu» — калька, по-польски говорят «Smacznego»"),
    (8788, "example_tr", "Fabrikanın yönetimi geçen ay değişti",
     "Şirketin yönetimi önemli",
     "немецкий «Die Führung des Unternehmens ist wichtig», а тут смена руководства"),
    (10260, "example_en", "Promise me that you'll be careful",
     "I promise you an ice cream", "немецкий «Ich verspreche dir ein Eis»"),
    (10260, "example_uk", "Обіцяй мені, що будеш обережний",
     "Я обіцяю тобі мороживо", "то же"),
    (10260, "example_tr", "Dikkatli olacağına dair söz ver",
     "Sana dondurma sözü veriyorum", "то же"),
    (259, "example_pl", "Na uroczystości było mnóstwo gości",
     "Uroczystość była wspaniała",
     "немецкий «Die Feier war toll», а польский про гостей"),
    (2649, "example_tr", "Gürültü çok yüksek", "Birahanedeki gürültü korkunçtu",
     "немецкий про шум в пивной, турецкий — про громкий шум вообще"),
    (13644, "example_pl", "Dostałam na urodziny złoty łańcuszek",
     "Ten łańcuszek jest ze złota",
     "немецкий «Die Kette ist aus Gold», польский — про подарок"),
    (12127, "example_tr", "Bu aptal oyuncağı bırak", "Bu aptal oyunu bırak",
     "«oyuncak» — игрушка, а речь об игре"),
    (760, "example_en", "The reporter works",
     "The reporter writes about politics", "потеряна половина фразы"),
    (760, "example_tr", "Muhabir çalışıyor",
     "Muhabir politika hakkında yazıyor", "то же"),
    (6693, "example_en", "I didn't do anything",
     "I didn't know anything about it",
     "немецкий «Ich habe nichts davon gewusst» — про «не знал»"),
    (6693, "example_uk", "Я нічого не робив", "Я нічого про це не знав",
     "то же"),
    (6693, "example_tr", "Hiçbir şey yapmadım",
     "Bu konuda hiçbir şey bilmiyordum", "то же"),
    (6693, "example_pl", "Nic nie zrobiłem", "Nic o tym nie wiedziałem",
     "то же"),
    (2792, "example_tr", "Anahtarı sağa çevir", "Kanalı değiştiriyorum",
     "немецкий «Ich schalte den Kanal um», турецкий — про поворот ключа"),
    (2624, "example_en", "I need a copy of this document",
     "I need a copy of my passport", "в немецком копия паспорта"),
    (2624, "example_uk", "Мені потрібна копія",
     "Мені потрібна копія мого паспорта", "потеряно, чего именно копия"),
    (2624, "example_tr", "Bir kopya lazım", "Pasaportumun bir kopyası lazım",
     "то же"),
    (6698, "example_en", "The cat is hiding underneath the table",
     "The newspaper is lying underneath",
     "немецкий «Die Zeitung liegt darunter»"),
    (6698, "example_tr", "Anahtar paspasın altında duruyor",
     "Gazete onun altında duruyor", "то же: в немецком газета, а не ключ"),
    (10269, "example_uk", "Не будь нечемним із бабусею",
     "Це було дуже нечемно з твого боку",
     "немецкий «Das war sehr unhöflich von dir»"),
    (13482, "example_en", "None of these books interest me",
     "I haven't read any of these books",
     "немецкий «Ich habe keins dieser Bücher gelesen»"),
    (34, "example_tr", "Televizyonda çok fazla reklam var",
     "İlanlarda daire arıyorum",
     "немецкий «Ich suche eine Wohnung in den Anzeigen»"),
    (1828, "example_tr", "Kapıyı biraz it, açılacak", "El arabasını biraz it",
     "немецкий «Schieb mal den Wagen» — про тележку, а не про дверь"),
    (6705, "example_uk", "Давай сюди", "Підійди-но сюди",
     "«Давай сюди» — это «дай сюда», а немецкий «Komm mal her»"),
    (6705, "example_tr", "Bana bir bardak su ver", "Bir buraya gel",
     "то же: турецкий просил стакан воды"),
    (6705, "example_en", "Come on, come here", "Just come here",
     "«Come on, come here» — одно и то же дважды"),
    (2914, "example_en", "All the better", "All the better that you're coming",
     "потеряно «dass du kommst»"),
    (2914, "example_uk", "Тим більше", "Тим краще, що ти прийдеш",
     "то же, и «тим більше» сбивает смысл"),
    (1997, "example_en", "We move into the new flat tomorrow",
     "We're moving next month", "в немецком «nächsten Monat»"),
    (12525, "example_en", "I'm running out of breath",
     "After the run I was out of breath",
     "немецкий «Nach dem Lauf fehlte mir der Atem»"),
    (12525, "example_uk", "У мене закінчується дихання",
     "Після бігу мені не вистачало дихання", "то же"),
    (12525, "example_tr", "Nefesim kesiliyor",
     "Koşudan sonra nefesim kesildi", "то же"),
    (772, "example_en", "I have to tidy up my room",
     "She's tidying up the room", "в немецком «sie», а не «я»"),
    (772, "example_tr", "Eşyalarını toparla, gidiyoruz", "Odayı topluyor",
     "немецкий «Sie räumt das Zimmer»"),
    (1651, "example_en", "Can I borrow your pen?",
     "Can you lend me some money?",
     "немецкий «Kannst du mir Geld leihen?» — про деньги"),
    (18669, "example_ru", "В сегодняшнее время всё очень быстро",
     "Сегодняшний мир очень быстрый",
     "«в сегодняшнее время» — так не говорят, и потерян «мир»"),
    (18669, "example_uk", "У сьогоднішній час все дуже швидко",
     "Сьогоднішній світ дуже швидкий", "то же"),
    (18669, "example_tr", "Bugünkü zamanda her şey çok hızlı",
     "Bugünkü dünya çok hızlı", "то же"),

    # --- добавлено то, чего в немецком нет -----------------------------------
    (8788, "example_pl", "Kierownictwo firmy jest bardzo ważne",
     "Kierownictwo firmy jest ważne", "«bardzo» в немецком нет"),
    (13918, "example_en", "We're all in agreement, then",
     "We're in agreement", "«all» и «then» в немецком нет"),
    (12526, "example_en", "He's shot but still alive", "He has been shot",
     "«но ещё жив» в немецком нет"),
    (12526, "example_uk", "Він поранений кулею, але живий",
     "Він поранений кулею", "то же"),
    (12526, "example_tr", "Vurulmuş ama hala yaşıyor", "Vurulmuş", "то же"),

    # --- битый немецкий эталон ------------------------------------------------
    (15433, "example_de", "Im Zoo haben wir einen großen Bär gesehen",
     "Im Zoo haben wir einen großen Bären gesehen",
     "«Bär» слабого склонения: в аккузативе «Bären», иначе учится неверная форма"),

    # --- битая кодировка -----------------------------------------------------
    (16022, "translation_pl", "uzbrojony, z broniÄ…", "uzbrojony, z bronią",
     "«ą» прочитана как latin-1; по всей базе такая ячейка одна"),

    # --- слова, которых нет в языке, и опечатки -------------------------------
    (12129, "translation_uk", "ведмедик, плюшевий мишка",
     "ведмедик, плюшевий ведмідь", "«мишка» в украинском — это мышь"),
    (12129, "example_tr", "Teddy ayı yatağın üstünde",
     "Oyuncak ayı yatağın üstünde", "«Teddy» — немецкое слово в турецкой колонке"),
    (6675, "example_tr", "Bu yükseklikte hava seyreleşiyor",
     "Bu yükseklikte hava seyreliyor",
     "«seyreleşmek» — такого глагола нет, есть «seyrelmek»"),
    (8795, "example_tr", "Komisar olayı araştırıyor",
     "Komiser olayı araştırıyor", "«Komisar» — опечатка"),
    (16022, "example_ru", "Вооруженные люди опасны",
     "Вооружённые люди опасны", "пропущена «ё», в значениях стоит «вооружённый»"),
    (6673, "example_tr", "Araba içerde çok temiz", "Araba içeride çok temiz",
     "«içerde» — разговорное стяжение, в значениях стоит «içeride»"),

    # --- русизмы в украинской колонке ----------------------------------------
    (18664, "translation_uk", "поспіх, спішка", "поспіх, спіх",
     "«спішка» — русизм"),
    (16014, "translation_uk", "пушка, пістолет", "пістолет, зброя",
     "«пушка» в значении пистолета — русизм"),
    (8794, "translation_uk", "пілот, летун", "пілот, авіатор",
     "«летун» — русизм"),
    (6687, "example_uk", "Він видимо не вдома", "Його, мабуть, немає вдома",
     "«видимо» — русизм, и вводное слово без запятых"),
    (13481, "example_uk", "Це той же самий чоловік, що й вчора",
     "Це той самий чоловік, що й вчора",
     "«той же самий» — русизм, в значениях стоит «той самий»"),
    (1695, "example_uk", "Я з охотою беру участь", "Я охоче беру участь",
     "«з охотою» — русизм"),

    # --- грамматика целевого языка --------------------------------------------
    (9746, "example_uk", "Король носити золоту корону",
     "Король носить золоту корону", "инфинитив вместо формы третьего лица"),
    (6686, "example_uk", "Повіс пальто на гачок", "Повісь пальто на гачок!",
     "«Повіс» — прошедшее время, а в немецком приказ"),
    (13482, "example_ru", "Я не читал ни одну из этих книг",
     "Я не читал ни одной из этих книг",
     "при отрицании нужен родительный падеж"),
    (13482, "example_uk", "Я не читав жодну з цих книг",
     "Я не читав жодної з цих книг", "то же"),
    (16017, "example_tr", "Bizim cemaat çok küçük",
     "Bizim cemaatimiz çok küçük", "пропущен притяжательный аффикс"),
    (6713, "example_tr", "Top tepeyi aşağı yuvarlanıyor",
     "Top tepeden aşağı yuvarlanıyor", "нужен исходный падеж: «tepeden»"),
    (14405, "example_uk", "Я хочу це знімати", "Я хочу це зняти",
     "вид глагола: в немецком однократное действие"),
    (6690, "example_uk", "Давайте це розглянемо", "Давай це розглянемо",
     "в немецком «lass uns» — на «ты», как и в остальных языках"),
    (6714, "example_ru", "Это возможно слишком дорого для нас",
     "Это, возможно, слишком дорого для нас",
     "вводное слово выделяется запятыми"),
    (6714, "example_uk", "Це можливо занадто дорого для нас",
     "Це, можливо, занадто дорого для нас", "то же"),
    (14408, "translation_uk", "легенда, перекази, умовні позначення на карті",
     "легенда, переказ, умовні позначення на карті",
     "«перекази» — множественное среди единственного"),

    # --- подменённое значение -------------------------------------------------
    (17497, "example_tr", "Teknik harika", "Teknoloji harika",
     "«teknik» — это приём, метод; немецкий про технику-оборудование"),
    (14407, "example_tr", "İncil eski", "Kutsal Kitap eski",
     "«İncil» — Евангелие; Библия целиком это «Kutsal Kitap»"),
    (13644, "example_tr", "Zincir altından yapılmış",
     "Kolye altından yapılmış", "«zincir» — цепь железная, а речь о цепочке"),
    (2052, "example_uk", "У мене є страхування", "У мене є страховка",
     "«страхування» — процесс; у человека на руках страховка"),
    (8796, "example_uk", "Не вигадуй дурниці!", "Не витворяй дурниць!",
     "«вигадувати» — придумывать, а немецкий про «натворить»"),

    # --- говорить по-людски ---------------------------------------------------
    (11664, "example_uk", "Я беру ще один ковток води",
     "Я зроблю ще один ковток води", "«беру ковток» — так не говорят"),
    (18664, "example_ru", "Я спешу, поезд уходит",
     "Я спешу, поезд скоро уходит", "в немецком «bald» — потеряно «скоро»"),
    (18664, "example_uk", "Я поспішаю, поїзд зараз відправляється",
     "Я поспішаю, поїзд скоро від'їжджає",
     "«зараз» вместо «скоро», и «відправляється» — канцелярит"),
    (18664, "example_tr", "Aceleciyim, tren hemen kalkıyor",
     "Acelem var, tren az sonra kalkıyor",
     "«Aceleciyim» — «я человек торопливый», а не «я спешу»"),
    (8788, "example_uk", "Керівництво компанії є важливим",
     "Керівництво компанії важливе", "«є важливим» — калька, по-людски без «є»"),
    (6684, "example_uk", "Я хочу володіти машиною",
     "Я хотів би колись мати власну машину",
     "«володіти машиною» — канцелярит, и потеряно «mal»"),
    (12523, "example_ru", "Мой вес слишком высокий",
     "У меня слишком большой вес",
     "по-русски вес большой, высоким бывает рост"),
    (12523, "example_uk", "Моя вага занадто висока",
     "У мене занадто велика вага", "то же"),
    (12523, "example_tr", "Ağırlığım çok yüksek", "Kilom çok fazla",
     "по-турецки говорят «kilom fazla»"),
    (12523, "example_pl", "Moja waga jest za wysoka",
     "Moja waga jest za duża", "waga bywa duża, nie wysoka"),
    (14408, "example_tr", "Bu benim şehrimden eski bir efsanedir",
     "Bu, şehrimin eski bir efsanesi",
     "«-dir» и «benim şehrimden» — книжно и неловко"),
    (13481, "example_tr", "Bu dünkü aynı adam", "Bu, dünkü adamın aynısı",
     "по-турецки так фразу не строят"),
    (10269, "example_tr", "Bu senin için çok kabaydı",
     "Bu davranışın çok kabaydı",
     "«senin için» — «для тебя»; в немецком «с твоей стороны»"),
    (2914, "example_tr", "O kadar daha iyi ki geldin", "Gelmen daha da iyi",
     "по-турецки так не говорят"),
    (34, "example_uk", "Я шукаю квартиру за оголошенням",
     "Я шукаю квартиру за оголошеннями", "в немецком множественное число"),
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
