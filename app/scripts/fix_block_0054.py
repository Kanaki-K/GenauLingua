"""
Правки блока 54 (ряды 9101–9300, ранги 18237–18686).

Классы, которые дал блок:
  · три сломанных эталона: `Der Preis ist mit allen Kosten inbegriffen`
    (перевёрнутая конструкция), `Der Hund war angebunden an einem langen
    Seil` (порядок слов), `Räum dein Zimmer auf!` у ряда `wegräumen`
    (в примере другая приставка, слова ряда в примере нет);
  · перевод другого предложения — больше сорока рядов;
  · перевод-омоним: tr `Yazında sandalet takmayı severim`, где
    `takmak` взято вместо `giymek`, и `ince insanlar` вместо `gurmeler`
    («Feinschmecker» переведено как «тонкие люди»);
  · множественное число в словарной статье при единственном эталоне
    (`der Partisan` → «партизаны, повстанцы»);
  · украинские несуществующие формы: `божевільність`, `передвгадувати`,
    `безшкідлива`, `мотиля`, `плачучу`;
  · турецкие сломанные изафеты и падежи: `Bekçi köpek`, `Şarap tatlı
    bir tadı var`, `cerrahın ameliyat sırasında yardımcı oldu`,
    `Etrafını bakıyor`, `Kertenkele taş üzerine ısınıyor`.

    python -m app.scripts.fix_block_0054            # показать
    python -m app.scripts.fix_block_0054 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

FIXES: list[tuple[int, str, str, str, str]] = [
    # 9101 überschwemmt
    (15747, "example_uk", "Після повені вулиці були повністю залиті",
     "Після повені вулиці були повністю затоплені",
     "перевод слова — «затоплений»"),
    (15747, "example_tr", "Sel sonrası sokaklar tamamen su basmıştı",
     "Sel sonrası sokakları tamamen su basmıştı",
     "«su basmak» требует аккузатива"),
    # 9102 Nagellack
    (13749, "example_pl", "Kupiłam czerwony lakier do paznokci",
     "Właśnie kupiłam sobie czerwony lakier do paznokci",
     "потеряно «gerade» и «mir»"),
    # 9103 Tofu
    (11919, "example_uk", "Я готую сьогодні смажене з тофу замість м'яса",
     "Я готую сьогодні страву з вока з тофу замість м'яса",
     "«смажене» — не страва, и потерян вок"),
    (11919, "example_pl", "Dziś gotuję danie z woka z tofu zamiast z mięsem",
     "Dziś gotuję danie z woka z tofu zamiast mięsa",
     "«zamiast» требует родительного"),
    # 9104 kugelsicher
    (8139, "example_pl", "Ochroniarz ma kuloodporną kamizelkę",
     "Nowy samochód ma kuloodporne szyby",
     "перевод другого предложения"),
    # 9105 potenziell
    (8140, "example_uk", "Ми вже інтерв'ювали потенційних кандидатів",
     "Ми вже провели співбесіди з потенційними кандидатами",
     "«інтерв'ювати» о прессе, а тут собеседование"),
    (8140, "example_tr", "Potansiyel adayları zaten röportaj yaptık",
     "Potansiyel adaylarla zaten görüşme yaptık",
     "сломанное управление и «röportaj» о прессе"),
    (8140, "example_pl", "To nasz potencjalny klient",
     "Już przeprowadziliśmy rozmowy z potencjalnymi kandydatami",
     "перевод другого предложения"),
    # 9106 einfühlsam
    (11263, "example_uk", "Він чуйний друг і завжди вислухає",
     "Вона чуйно поговорила з ним про його проблеми",
     "перевод другого предложения"),
    (11263, "example_pl", "Ona jest bardzo wyrozumiała dla innych",
     "Rozmawiała z nim o jego problemach z empatią",
     "перевод другого предложения"),
    # 9107 systematisch
    (8141, "example_pl", "Uczę się systematycznie każdego dnia",
     "Systematycznie szukamy rozwiązania problemu",
     "перевод другого предложения"),
    # 9108 Sperrgebiet
    (16671, "example_uk", "Військова база — закрита зона",
     "Військова база — заборонена зона",
     "перевод слова — «заборонена зона»"),
    (16671, "example_tr", "Askeri üs kapalı bir alandır",
     "Askeri üs yasak bölgedir",
     "перевод слова — «yasak bölge»"),
    (16671, "example_pl", "Tam nie wolno wchodzić, to strefa zakazana",
     "Teren wojskowy to strefa zakazana",
     "перевод другого предложения"),
    # 9109 Briefmarke
    (14241, "example_uk", "Я повинен наклеїти марку на лист перед відправкою",
     "Мені потрібно ще наклеїти марку на лист, перш ніж я його відправлю",
     "потеряно «noch», и придаточное свёрнуто в предлог"),
    # 9110 Alkoholikerin
    (12955, "example_en",
     "She admitted she's an alcoholic woman and is helping herself now",
     "She admitted that she is an alcoholic and is now helping herself",
     "«alcoholic woman» — не по-английски"),
    # 9112 freudig
    (11264, "example_pl", "Miała radosną minę po dobrej wiadomości",
     "Z radosnym zaskoczeniem otworzyliśmy prezent",
     "перевод другого предложения"),
    # 9113 Gemeinheit
    (11265, "example_uk", "Це була справжня підлість, так з ним поступати",
     "Це була справжня підлість — так з ним чинити",
     "«поступати» — русизм"),
    (11265, "example_tr", "Onu öyle muamele etmek gerçek bir kötülük oldu",
     "Ona öyle davranmak gerçek bir alçaklıktı",
     "«muamele etmek» требует датива"),
    (11265, "example_pl", "To była prawdziwa podłość z jego strony",
     "To była prawdziwa podłość, tak go traktować",
     "перевод другого предложения"),
    # 9114 Vorstadt
    (18394, "example_uk",
     "Ми переїжджаємо в передмістя в наступному місяці, "
     "щоб бути ближче до батьків",
     "Ми переїжджаємо в передмістя наступного місяця, "
     "щоб бути ближче до батьків",
     "«в наступному місяці» — калька"),
    (18394, "example_tr",
     "Ailemime daha yakın olmak için ay sonunda banliyöye taşınıyoruz",
     "Aileme daha yakın olmak için gelecek ay banliyöye taşınıyoruz",
     "«Ailemime» — опечатка, и «ay sonunda» это конец месяца"),
    (18394, "example_pl", "Mieszkamy na przedmieściu, blisko lasu",
     "W przyszłym miesiącu przeprowadzamy się na przedmieście, "
     "żeby być bliżej moich rodziców",
     "перевод другого предложения"),
    # 9115 Egoismus
    (11266, "example_pl", "Jego egoizm wszystkich męczy",
     "Jego egoizm przeszkadza mu zrozumieć innych",
     "перевод другого предложения"),
    # 9117 Syndrom
    (12957, "example_tr", "Down sendromu teşhis edildi",
     "Ona Down sendromu teşhis edildi",
     "потерян «ihm»: кому поставили диагноз"),
    # 9118 Spritzer
    (11920, "translation_uk", "трохи, краплі, брризки",
     "трохи, краплі, бризки",
     "опечатка «брризки»"),
    # 9119 nachfahren
    (17315, "example_uk",
     "Поліцейський буде слідкувати за підозрілим автомобілем",
     "Поліцейський поїде слідом за підозрілим автомобілем",
     "«слідкувати» это наблюдать, а тут ехать следом"),
    # 9120 rütteln
    (8142, "example_uk", "Будь ласка, не штовхай двері, вони заблоковані",
     "Будь ласка, не смикай двері, вони зачинені",
     "«штовхати» это толкать, «abgesperrt» — зачинені"),
    (8142, "example_tr", "Lütfen kapıyı çalkalamayın, kilitli",
     "Lütfen kapıyı sarsmayın, kilitli",
     "«çalkalamak» о жидкости"),
    # 9121 Schiene
    (17316, "example_en",
     "After the accident, his arm wore a splint for protection",
     "After the accident, he wore a splint on his arm",
     "рука не может носить шину"),
    (17316, "example_ru", "После аварии его рука была в шине для защиты",
     "После аварии он носил шину на руке",
     "«для защиты» в эталоне нет"),
    (17316, "example_uk", "Після аварії його рука була в шині для захисту",
     "Після аварії він носив шину на руці",
     "«для захисту» в эталоне нет"),
    (17316, "example_tr", "Kazadan sonra koluna koruma için atel takıldı",
     "Kazadan sonra koluna atel taktı",
     "«koruma için» в эталоне нет"),
    # 9122 Häppchen
    (11921, "example_en",
     "At the party there were small appetizers to snack on",
     "At the party there were delicious little appetizers",
     "потеряно «leckere», добавлено «to snack on»"),
    (11921, "example_uk", "На вечірці були маленькі закуски",
     "На вечірці були смачні маленькі закуски",
     "потеряно «leckere»"),
    (11921, "example_tr",
     "Partide atıştırmak için küçük atıştırmalıklar vardı",
     "Partide lezzetli küçük atıştırmalıklar vardı",
     "«atıştırmak için atıştırmalık» — тавтология"),
    # 9124 Quint
    (14702, "example_pl", "Zagraj czystą kwintę na gitarze",
     "Kwinta to interwał muzyczny pięciu stopni",
     "перевод другого предложения"),
    # 9125 Wohltätigkeit
    (11267, "example_uk",
     "Вона працює в благодійній організації і допомагає людям у потребі",
     "Вона працює в благодійній організації і допомагає нужденним людям",
     "«люди у потребі» — калька"),
    (11267, "example_pl", "Zajmuje się dobroczynnością już od lat",
     "Pracuje w organizacji dobroczynnej i pomaga potrzebującym",
     "перевод другого предложения"),
    # 9126 Faschist
    (16672, "example_ru",
     "Его называли фашистом, потому что он защищал экстремистские идеи",
     "Его называли фашистом, потому что он отстаивал экстремистские идеи",
     "«vertreten» — отстаивать, а не защищать"),
    (16672, "example_tr",
     "Aşırıcı fikirleri desteklediği için faşist olarak adlandırıldı",
     "Aşırı fikirleri desteklediği için faşist olarak adlandırıldı",
     "«aşırıcı» — нет такого слова"),
    (16672, "example_pl", "Nazwali go faszystą za te poglądy",
     "Nazwano go faszystą, bo głosił skrajne poglądy",
     "перевод другого предложения"),
    # 9127 häuten
    (15748, "example_uk", "Змія линяє кожен рік",
     "Змія линяє щоліта",
     "в эталоне «jeden Sommer»"),
    (15748, "example_tr", "Yılan her yaz derisi değiştirir",
     "Yılan her yaz derisini değiştirir",
     "потерян аккузатив"),
    # 9128 Tube
    (8143, "example_pl", "Skończyła mi się tubka pasty do zębów",
     "Tubka pasty do zębów wystarcza mi na trzy miesiące",
     "перевод другого предложения"),
    # 9130 schwerhörig
    (12958, "translation_uk", "слабочуючий, туговухий",
     "глухуватий, туговухий",
     "«слабочуючий» — калька активного дієприкметника"),
    (12958, "example_uk", "Дідусь туговухий, говори голосніше",
     "Мій дідусь туговухий і носить слуховий апарат",
     "перевод другого предложения"),
    (12958, "example_tr", "Dedem işitme engelli ve işitme cihazı takıyor",
     "Dedem ağır işitiyor ve işitme cihazı takıyor",
     "«işitme engelli» это глухой, а «schwerhörig» слабослышащий"),
    # 9131 Lungenkrebs
    (12959, "example_en", "His uncle has been diagnosed with lung cancer",
     "His uncle fell ill with lung cancer",
     "в эталоне «ist erkrankt», а не диагноз"),
    # 9132 Nickel
    (9903, "example_pl", "Mam alergię na nikiel w biżuterii",
     "Nikiel jest często używany w stopach",
     "перевод другого предложения"),
    # 9133 Smalltalk
    (14242, "example_uk", "Ми вели світську розмову про погоду",
     "На конференції ми вели світську бесіду про погоду",
     "потеряна конференция"),
    # 9134 Krempel
    (8144, "translation_pl", "rupiecie, graty, barachło",
     "rupiecie, graty, klamoty",
     "«barachło» — русизм"),
    (8144, "example_tr", "Çekmecede bir sürü ıvır zıvır var",
     "Odası işe yaramaz ıvır zıvırla dolu",
     "перевод другого предложения"),
    # 9136 unerwünscht
    (11268, "example_pl", "Lek może mieć niepożądane skutki",
     "Niepożądani goście wyszli z przyjęcia wcześnie",
     "перевод другого предложения"),
    # 9137 beinhalten
    (8145, "example_pl", "Cena zawiera śniadanie",
     "Paczka zawiera trzy różne produkty",
     "перевод другого предложения"),
    # 9138 Gerichtsgebäude
    (16673, "example_uk", "Нова судова будівля була відкрита минулого року",
     "Нову будівлю суду відкрили минулого року",
     "«судова будівля» — не по-украински"),
    (16673, "example_pl", "Spotkajmy się przed budynkiem sądu",
     "Nowy budynek sądu został otwarty w zeszłym roku",
     "перевод другого предложения"),
    # 9139 Füller
    (9592, "example_uk", "Моя авторучка пуста, мені потрібна нова туш",
     "Моя авторучка порожня, мені потрібне нове чорнило",
     "«туш» это для вій, чернила — «чорнило»"),
    # 9141 kompetent
    (11270, "example_uk", "Він дуже компетентний у своій професії",
     "Він дуже компетентний у своїй професії",
     "опечатка «своій»"),
    (11270, "example_pl", "Sprzedawca był bardzo kompetentny",
     "Jest bardzo kompetentny w swoim zawodzie",
     "перевод другого предложения"),
    # 9142 zusammenpassen
    (8146, "example_tr", "Bu iki renk iyi uyuşuyor",
     "Bu iki renk birbirine iyi uyuyor",
     "«uyuşmak» о людях, не о цветах"),
    # 9143 glühen
    (8147, "example_en", "The lamp glows brightly in the dark night",
     "The lightbulb glows brightly in the dark night",
     "в эталоне «Glühbirne» — лампочка"),
    (8147, "example_uk", "Лампа світиться яскраво в темну ніч",
     "Лампочка яскраво світиться темної ночі",
     "«в темну ніч» — не тот падеж"),
    (8147, "example_tr", "Ampul karanlık gecede parlak ışılıyor",
     "Ampul karanlık gecede parlak parlıyor",
     "«ışılamak» — нет такого глагола"),
    (8147, "example_pl", "Węgle jeszcze żarzą się w kominku",
     "Żarówka jarzy się jasno w ciemną noc",
     "перевод другого предложения"),
    # 9144 ausgebreitet
    (8148, "example_uk", "Ковдра розстелена просто на траві",
     "Ковдра лежала розстелена на ліжку",
     "в эталоне «auf dem Bett»"),
    (8148, "example_pl", "Koc leżał rozłożony na trawie",
     "Koc leżał rozłożony na łóżku",
     "в эталоне «auf dem Bett»"),
    # 9145 unzerstörbar
    (8149, "example_uk", "Його віра в людей незнищенна",
     "Ця каблучка здається незнищенною",
     "перевод другого предложения"),
    (8149, "example_pl", "Ten kubek jest chyba niezniszczalny",
     "Ten pierścień zdaje się niezniszczalny",
     "перевод другого предложения"),
    # 9146 aufdrängen
    (11271, "example_pl", "Nie chcę ci narzucać swojego zdania",
     "Nie chciałem mu narzucać swojego zdania",
     "эталон в прошедшем и про «ihm»"),
    # 9147 bösartig
    (12961, "example_tr", "Tümör kötü niyetli ve çıkarılması gerekiyordu",
     "Tümör kötü huyluydu ve çıkarılması gerekiyordu",
     "«kötü niyetli» о человеке, опухоль — «kötü huylu»"),
    # 9148 Schlaflosigkeit
    (12962, "example_uk",
     "Його безсоння робить його втомленого та дратівливого",
     "Його безсоння робить його втомленим і дратівливим",
     "не тот падеж"),
    # 9149 verirren
    (8150, "example_uk", "Ми постійно заблуджуємося у великому місті",
     "Ми постійно губимося у великому місті",
     "«заблуджуватися» о заблуждении, не о дороге"),
    (8150, "example_pl", "Zgubiliśmy się w lesie",
     "Ciągle gubimy się w wielkim mieście",
     "перевод другого предложения"),
    # 9150 Schuster
    (9171, "example_uk", "Чоботар виправляє мої старі туфлі",
     "Чоботар ремонтує мої старі черевики",
     "«виправляє» это исправляет"),
    (9171, "example_tr", "Ayakkabıcı eski ayakkabılarımı onarıyor",
     "Ayakkabı tamircisi eski ayakkabılarımı onarıyor",
     "перевод слова — «ayakkabı tamircisi»"),
    # 9151 zugetan
    (11272, "example_uk", "Шеф прихильний до нових ідей",
     "Він дуже прив'язаний до своїх дітей",
     "перевод другого предложения"),
    # 9152 schwärmen
    (11273, "example_en", "He's crazy about football",
     "She's crazy about her new teacher",
     "перевод другого предложения"),
    # 9153 minimal
    (8151, "example_tr", "Kayıt için minimum miktar on avro",
     "Kayıt için minimum tutar on avrodur",
     "фраза без связки, и «tutar» о сумме"),
    (8151, "example_pl", "Różnica jest minimalna",
     "Minimalna kwota rejestracji to dziesięć euro",
     "перевод другого предложения"),
    # 9155 freundlicherweise
    (11274, "example_pl", "Sąsiad uprzejmie pożyczył mi parasol",
     "Uprzejmie pożyczył mi swój parasol",
     "«Sąsiad» в эталоне нет"),
    # 9156 Markenzeichen
    (14703, "example_uk", "Його торговельна марка — широка посмішка",
     "Його візитівка — широка усмішка",
     "тут «Markenzeichen» — отличительная черта, не марка"),
    # 9157 vorläufig
    (8152, "example_tr", "Bu sadece sorun için geçici bir çözüm",
     "Bu, sorun için sadece geçici bir çözüm",
     "порядок слов ломает смысл"),
    (8152, "example_pl", "To tylko tymczasowe rozwiązanie",
     "To tylko tymczasowe rozwiązanie problemu",
     "потеряно «für das Problem»"),
    # 9158 Erzählung
    (14704, "example_uk", "Розповідь старика була дуже цікавою",
     "Розповідь старого чоловіка була дуже цікавою",
     "«старик» — русская форма"),
    (14704, "example_pl", "Jego opowiadanie było bardzo ciekawe",
     "Opowiadanie starego człowieka było bardzo ciekawe",
     "в эталоне «des alten Mannes»"),
    # 9159 Vakuum
    (18038, "example_tr", "Bir vakuumda ses dalgaları var olamaz",
     "Vakumda ses dalgaları var olamaz",
     "по-турецки «vakum», и «bir» лишний"),
    # 9160 Willenskraft
    (11275, "example_pl", "Rzucenie palenia wymaga siły woli",
     "Rzucenie palenia wymaga prawdziwej siły woli",
     "потеряно «echte»"),
    # 9161 Aroma
    (11922, "example_uk", "Аромат свіжої кави наповнював всю кухню",
     "Аромат свіжої кави наповнював усю кухню",
     "«всю» после согласной"),
    # 9162 Sinneswandel
    (11276, "example_pl", "Skąd u niego nagła zmiana zdania",
     "Po długiej rozmowie nastąpiła u niego zmiana zdania",
     "перевод другого предложения"),
    # 9163 Intellekt
    (11277, "example_pl", "Imponuje mi jego intelekt",
     "Jego intelekt był imponujący na jego wiek",
     "перевод другого предложения"),
    # 9164 Gezeiten
    (15749, "example_uk", "На припливи й відливи впливає місяць",
     "На припливи й відпливи впливає Місяць",
     "«відливи» — русизм, и Месяц с заглавной как светило"),
    # 9166 geimpft
    (12963, "example_uk", "Всі щеплені люди могли йти на концерт",
     "Усі щеплені люди могли піти на концерт",
     "«могли йти» — калька"),
    # 9167 Assistenzarzt
    (12964, "example_tr",
     "Asistan doktor cerrahın ameliyat sırasında yardımcı oldu",
     "Asistan doktor ameliyat sırasında cerraha yardımcı oldu",
     "«yardımcı olmak» требует датива"),
    # 9168 Wandschrank
    (18395, "example_pl", "Kurtki wiszą w szafie wnękowej",
     "Szafa wnękowa jest za mała na wszystkie moje ubrania",
     "перевод другого предложения"),
    # 9170 wegsperren
    (16674, "example_uk", "Вони хочуть посадити небезпечних злочинців",
     "Вони хочуть посадити небезпечних злочинців за ґрати",
     "потеряно «wegsperren» целиком"),
    (16674, "example_tr", "Tehlikeli suçluları kapatmak istiyorlar",
     "Tehlikeli suçluları kilit altına almak istiyorlar",
     "«kapatmak» без дополнения двусмысленно"),
    (16674, "example_pl", "Takich przestępców trzeba zamykać na długo",
     "Chcą zamknąć niebezpiecznych przestępców",
     "перевод другого предложения"),
    # 9171 Einsen
    (9593, "example_uk", "У нього були тільки одиниці в свідоцтві",
     "У нього в табелі були тільки одиниці",
     "«Zeugnis» это табель, и порядок слов"),
    (9593, "example_tr", "Karne kartında sadece en yüksek notları aldı",
     "Karnesinde sadece en yüksek notları aldı",
     "«karne kartı» — тавтология"),
    # 9172 sensible
    (11278, "example_en", "My skin is very sensitive to the sun",
     "That was a sensitive decision in a difficult situation",
     "перевод другого предложения"),
    (11278, "example_uk", "У мене дуже чутлива шкіра",
     "Це було делікатне рішення у складній ситуації",
     "перевод другого предложения"),
    (11278, "example_tr", "Zor bir durumda akılcı bir karar oldu",
     "Zor bir durumda hassas bir karardı",
     "«akılcı» это разумный, а не чувствительный"),
    (11278, "example_pl", "Ona jest bardzo wrażliwa na krytykę",
     "To była delikatna decyzja w trudnej sytuacji",
     "перевод другого предложения"),
    # 9173 Preisgeld
    (12335, "example_ru",
     "Денежный приз за участие в конкурсе составил 10 000 евро",
     "Денежный приз за конкурс составил 10 000 евро",
     "«за участие» в эталоне нет"),
    (12335, "example_uk", "Премія за конкурс становила 10 000 євро",
     "Грошовий приз конкурсу становив 10 000 євро",
     "перевод слова — «грошовий приз»"),
    # 9174 schwenken
    (8154, "example_uk", "Вони розмахували прапором на честь святкування",
     "Вони розмахують прапором на честь свята",
     "эталон в настоящем времени"),
    (8154, "example_pl", "Kibice wymachiwali flagami",
     "Wymachują flagą na cześć święta",
     "перевод другого предложения"),
    # 9175 Amtszeit
    (16675, "example_ru", "Во время его срока было много реформ",
     "Во время его срока полномочий было много реформ",
     "«срок» без «полномочий» повисает"),
    (16675, "example_uk", "Під час його терміну було багато реформ",
     "Під час його терміну повноважень було багато реформ",
     "«термін» без «повноважень» повисає"),
    (16675, "example_pl", "Jego kadencja kończy się w maju",
     "Podczas jego kadencji było wiele reform",
     "перевод другого предложения"),
    # 9176 Motte
    (15750, "example_uk", "Вночі мотиля літала навколо лампи",
     "Уночі моль літала навколо лампи",
     "«мотиля» — не форма"),
    (15750, "example_tr", "Gece bir güve lambayı dolanıyordu",
     "Gece bir güve lambanın etrafında dolanıyordu",
     "«dolanmak» не берёт аккузатив"),
    (15750, "example_pl", "Ćma krąży wokół lampy",
     "W nocy ćma krążyła wokół lampy",
     "потеряна ночь, и время"),
    # 9177 unschädlich
    (8155, "example_uk", "Ця речовина абсолютно безшкідлива для шкіри",
     "Ця речовина абсолютно нешкідлива для шкіри",
     "«безшкідливий» — нет такого слова"),
    # 9178 Weinkeller
    (18396, "example_en", "The restaurants wine cellar is impressively large",
     "The restaurant's wine cellar is impressively large",
     "потерян апостроф"),
    (18396, "example_pl", "Restauracja ma ogromną piwnicę z winem",
     "Piwnica z winem w restauracji jest imponująco duża",
     "«beeindruckend» потеряно"),
    # 9179 Wirtin
    (9173, "example_uk", "Господиня пивниці знає всіх постійних гостей",
     "Господиня пивнички особисто знає всіх своїх постійних гостей",
     "«пивниця» это погреб, и потеряно «persönlich»"),
    (9173, "example_tr",
     "Meyhane sahibesi tüm düzenli müşterilerini kişisel olarak tanır",
     "Meyhane sahibesi bütün müdavimlerini kişisel olarak tanır",
     "«düzenli müşteri» — калька, по-турецки «müdavim»"),
    # 9180 Partisan — словарная статья во множественном при единственном слове
    (16676, "translation_en", "partisans, guerrillas",
     "partisan, guerrilla",
     "слово ряда единственного числа"),
    (16676, "translation_ru", "партизаны, повстанцы",
     "партизан, повстанец",
     "слово ряда единственного числа"),
    (16676, "translation_uk", "партизани, повстанці",
     "партизан, повстанець",
     "слово ряда единственного числа"),
    (16676, "translation_tr", "partizanlar, gerillalar",
     "partizan, gerilla",
     "слово ряда единственного числа"),
    (16676, "translation_pl", "partyzanci",
     "partyzant",
     "слово ряда единственного числа"),
    (16676, "example_pl", "Partyzanci ukrywali się w lasach",
     "Partyzanci walczyli z okupantami",
     "перевод другого предложения"),
    # 9181 Dickkopf
    (11279, "example_uk",
     "Мій брат такий впертун, він ніколи не слухає інших",
     "Мій брат такий впертюх, він ніколи не слухає інших",
     "перевод слова — «впертюх»"),
    (11279, "example_tr",
     "Kardeşim çok inat çekici, asla başkalarını dinlemez",
     "Kardeşim çok dik kafalı, asla başkalarını dinlemez",
     "«inat çekici» — нет такого выражения"),
    (11279, "example_pl", "Mój brat to straszny uparciuch",
     "Mój brat to taki uparciuch, nigdy nie słucha innych",
     "потеряна вторая половина"),
    # 9182 Mädchenname
    (15241, "example_uk", "Емма — гарне дівоче ім'я",
     "Емма — гарне ім'я для дівчинки",
     "«дівоче ім'я» читается как девичья фамилия"),
    # 9183 Gerichtsdiener
    (16677, "example_uk", "Судовий службовець привів свідка в залу",
     "Судовий пристав привів свідка до зали",
     "перевод слова — «пристав», и «в залу»"),
    # 9184 aufschlussreich
    (8156, "example_tr", "Onunla konuşma çok eğitici oldu",
     "Onunla yaptığım konuşma çok aydınlatıcıydı",
     "«Onunla konuşma» без сказуемого не держится"),
    # 9185 Bestseller
    (14705, "example_tr", "Donna Leonun yeni kitabı bir bestseller",
     "Donna Leon'un yeni kitabı bir bestseller",
     "потерян апостроф в имени"),
    (14705, "example_pl", "Ta książka to prawdziwy bestseller",
     "Nowa książka Donny Leon to bestseller",
     "перевод другого предложения"),
    # 9187 Weihnachtsfeier
    (18875, "example_tr", "Noel kutlaması çok eğlenceliydi",
     "Ofisimizdeki Noel partisi çok eğlenceliydi",
     "потерян офис"),
    # 9188 Pforte
    (18397, "example_pl", "Brama do zamku jest już zamknięta",
     "Brama do zamku jest bardzo stara",
     "перевод другого предложения"),
    # 9189 betreuen
    (15242, "example_uk", "Моя мати доглядає дітей після школи",
     "Моя мати доглядає за дітьми після школи",
     "«доглядати» требует «за»"),
    (15242, "example_pl", "Po szkole opiekuję się młodszym bratem",
     "Moja mama opiekuje się dziećmi po szkole",
     "перевод другого предложения"),
    # 9190 zügig
    (3055, "example_uk", "Будь ласка, працюйте швидко",
     "Будь ласка, працюй швидко",
     "эталон обращается на «ты»"),
    (3055, "example_tr", "Çabuk ol, otobüs kaçıyor!",
     "Lütfen çabuk çalış",
     "перевод другого предложения"),
    # 9191 Schar
    (8158, "example_tr", "Bir kuş sürüsü bize doğru uçtu",
     "Bir kuş sürüsü üzerimizden uçup gitti",
     "«über uns hinweg» — над нами, а не к нам"),
    (8158, "example_pl", "Gromada dzieci biegała po podwórku",
     "Stado ptaków przeleciało nad nami",
     "перевод другого предложения"),
    # 9192 Draufgänger
    (11280, "example_en",
     "He is a real adventurer, always looking for excitement",
     "He is a real daredevil, always out for adventure",
     "перевод слова — «daredevil», и «Abenteuer» это приключение"),
    (11280, "example_pl", "Z niego jest prawdziwy śmiałek",
     "To prawdziwy śmiałek, zawsze szuka przygód",
     "потеряна вторая половина"),
    # 9194 Doktortitel
    (9594, "example_tr", "Felsefe doktora derecesi aldı",
     "Felsefe alanında doktora derecesini aldı",
     "фраза без падежей не держится"),
    # 9195 unbewusst
    (11281, "example_pl", "To był nieświadomy odruch",
     "To było nieświadome, nie myślałem o tym",
     "перевод другого предложения"),
    # 9196 Privatbesitz
    (16678, "example_uk", "Дім — приватна власність і не відкритий для публіки",
     "Будинок — приватна власність і не відкритий для публіки",
     "«дім» это домашний очаг, строение — «будинок»"),
    (16678, "example_pl",
     "To jest własność prywatna i nie wolno tu wchodzić",
     "Dom jest własnością prywatną i nie jest dostępny dla publiczności",
     "вторая половина переводит другое"),
    # 9201 schockieren
    (11282, "example_tr", "Haber onu şoka sokar",
     "Haber onu şoke edecek",
     "эталон в будущем"),
    # 9202 zehnte
    (8160, "example_pl", "To już dziesiąty raz w tym tygodniu",
     "To już dziesiąte ostrzeżenie",
     "перевод другого предложения"),
    # 9203 festgebunden
    (8161, "example_uk", "Пакет був міцно пов'язаний",
     "Пакет був міцно зав'язаний",
     "«пов'язаний» это связанный по смыслу"),
    (8161, "example_tr", "Paket sıkı bağlı idi",
     "Paket sıkıca bağlanmıştı",
     "«idi» отдельно"),
    # 9204 Selbstmörder
    (12966, "example_en", "The suicide victim left a note",
     "The man who killed himself left a farewell letter",
     "«suicide victim» это жертва чужого, и «Abschiedsbrief»"),
    (12966, "example_uk", "Самогубець залишив записку",
     "Самогубець залишив прощальну записку",
     "потеряно «Abschieds-»"),
    (12966, "example_tr", "İntihar eden bir not bıraktı",
     "İntihar eden kişi bir veda mektubu bıraktı",
     "потеряно «kişi» и «veda»"),
    # 9205 vornehme
    (8162, "example_uk", "Вона з аристократичної сім'ї",
     "Вона походить зі знатної родини",
     "перевод слова — «знатний», и потеряно «stammt»"),
    # 9206 kommend
    (18876, "example_uk", "На майбутньому тижні буде свято",
     "Наступного тижня буде свято",
     "«на майбутньому тижні» — калька"),
    (18876, "example_tr", "Gelecek hafta bir festival var",
     "Gelecek hafta bir kutlama var",
     "«Fest» это праздник, не фестиваль"),
    # 9207 publik — ru и pl прочли «Affäre» как любовный роман
    (14243, "example_ru", "Роман стал публичным достоянием",
     "Скандал стал публичным",
     "«Affäre» здесь скандал, а не роман"),
    (14243, "example_tr", "Skandal herkese açık hale geldi",
     "Skandal herkesçe bilinir hale geldi",
     "«herkese açık» это открытый для входа"),
    (14243, "example_pl", "Romans stał się publiczny",
     "Skandal stał się publiczny",
     "«Affäre» здесь скандал, а не роман"),
    # 9208 Pflegerin
    (12967, "example_uk", "Медсестра зробила мені укол",
     "Доглядальниця піклується про пацієнта",
     "перевод другого предложения"),
    # 9209 entschädigen
    (16679, "example_en", "The insurance will compensate him",
     "The insurance will compensate him for the damage",
     "потеряно «für den Schaden»"),
    (16679, "example_ru", "Страховка его компенсирует",
     "Страховка возместит ему ущерб",
     "«компенсировать кого» — не то управление"),
    (16679, "example_uk", "Страховка його компенсує",
     "Страховка відшкодує йому збитки",
     "«компенсувати когось» — не то управление"),
    (16679, "example_tr", "Sigorta onu tazmin edecek",
     "Sigorta zararını tazmin edecek",
     "возмещают ущерб, а не человека"),
    (16679, "example_pl", "Ubezpieczenie zrekompensuje nam straty po burzy",
     "Ubezpieczenie zrekompensuje mu szkodę",
     "перевод другого предложения"),
    # 9210 lieblich
    (11283, "example_uk", "Вино має солодкий смак",
     "Вино має солодкуватий смак",
     "«lieblich» о вине — солодкуватий"),
    (11283, "example_tr", "Şarap tatlı bir tadı var",
     "Şarabın tatlı bir tadı var",
     "потерян родительный, фраза не держится"),
    # 9211 inbegriffen — эталон перевёрнут
    (8163, "example_de", "Der Preis ist mit allen Kosten inbegriffen",
     "Alle Kosten sind im Preis inbegriffen",
     "включают расходы в цену, а не цену в расходы"),
    # 9213 fürsorglich
    (11284, "example_uk", "Вона дуже турботлива до своїх дітей",
     "Вона дуже турботлива зі своїми дітьми",
     "«турботливий до» — не то управление"),
    # 9214 zahlreich
    (8164, "translation_pl", "liczny, wielu, liczne",
     "liczny, wielu, mnogi",
     "«liczne» это та же статья в другом роде"),
    (8164, "example_pl", "Na spotkanie przyszli liczni goście",
     "Jest wiele powodów do tego",
     "перевод другого предложения"),
    # 9215 fortführen
    (8165, "example_pl", "Chcemy kontynuować ten projekt",
     "Będziemy kontynuować ten projekt",
     "эталон в будущем, а не «хотим»"),
    # 9216 ergreifend
    (11285, "example_tr", "Çok duygulandırıcı bir hikâye idi",
     "Çok duygulandırıcı bir hikâyeydi",
     "«idi» отдельно"),
    # 9217 Verrücktheit
    (11286, "example_uk", "Його божевільність відома",
     "Його божевілля відоме",
     "«божевільність» — нет такого слова"),
    (11286, "example_pl", "Jego szaleństwo znają tu wszyscy",
     "Jego szaleństwo jest znane",
     "перевод другого предложения"),
    # 9220 zurückdrehen
    (8167, "example_uk",
     "Я зменшив гучність музики, вона занадто гучна",
     "Я зменшую гучність музики, вона для мене занадто гучна",
     "эталон в настоящем, и потеряно «mir»"),
    (8167, "example_pl", "Nie da się cofnąć czasu",
     "Przykręcam muzykę, jest dla mnie za głośna",
     "перевод другого предложения"),
    # 9222 Vorgarten
    (18398, "example_uk", "У передньому саду ростуть гарні квіти",
     "У палісаднику ростуть гарні квіти",
     "перевод слова — «палісадник»"),
    (18398, "example_pl", "W ogródku przed domem rosną róże",
     "W ogródku przed domem rosną piękne kwiaty",
     "в эталоне «schöne Blumen», а не розы"),
    # 9223 bekleiden
    (13750, "example_pl", "Był lekko ubrany na taki mróz",
     "Był lekko ubrany na tę zimną porę roku",
     "«taki mróz» в эталоне нет"),
    # 9224 Modul
    (17674, "example_uk",
     "Новий модуль в курсі присвячений управлінню проектами",
     "Новий модуль у курсі присвячений управлінню проектами",
     "«в» перед согласной"),
    (17674, "example_tr", "Kursdaki yeni modül proje yönetimine odaklanıyor",
     "Kurstaki yeni modül proje yönetimini ele alıyor",
     "«Kursdaki» без согласования, и «behandeln» это разбирать"),
    (17674, "example_pl", "W tym semestrze mamy nowy moduł",
     "Nowy moduł w kursie dotyczy zarządzania projektami",
     "перевод другого предложения"),
    # 9225 zusammentreffen
    (8168, "example_pl", "Jutro obaj szefowie spotkają się",
     "Jutro obaj szefowie się spotkają",
     "«się» в конце звучит оборванно"),
    # 9226 Ignoranz
    (11288, "example_ru", "Его невежество по отношению к ситуации удручает",
     "Его игнорирование ситуации удручает",
     "«невежество по отношению к» — не по-русски"),
    (11288, "example_pl", "Jego ignorancja naprawdę mnie denerwuje",
     "Jego ignorancja wobec tej sytuacji jest frustrująca",
     "потеряно «gegenüber der Situation»"),
    # 9227 Sandale
    (13751, "example_tr", "Yazında sandalet takmayı severim",
     "Yazın sandalet giymeyi severim",
     "«Yazında» не форма, и обувь не «takmak», а «giymek»"),
    # 9228 Wettstreit
    (12338, "example_en",
     "There's fierce competition between the two companies",
     "There's a great rivalry between the two companies",
     "в эталоне «großen», а не «ожесточённое»"),
    (12338, "example_pl",
     "Między tymi dwiema firmami trwa ostra rywalizacja",
     "Między tymi dwiema firmami trwa wielka rywalizacja",
     "в эталоне «großen», а не «острое»"),
    # 9229 besänftigen
    (11289, "example_en", "This tea soothes a sore throat",
     "She tried to calm the crying child",
     "перевод совершенно другого предложения"),
    (11289, "example_uk", "Вона намагалася заспокоїти плачучу дитину",
     "Вона намагалася заспокоїти дитину, що плакала",
     "«плачучий» — калька активного дієприкметника"),
    # 9230 Knirps
    (15243, "example_uk", "Малюк весь час нарікав",
     "Малюк весь час скиглив",
     "«нарікати» это жаловаться вслух, «jammern» — скиглити"),
    (15243, "example_tr", "Ufaklık bütün gün sızlandı",
     "Ufaklık sürekli sızlandı",
     "«die ganze Zeit» это всё время, а не весь день"),
    (15243, "example_pl", "Ten brzdąc ciągle biega po domu",
     "Ten mały brzdąc marudził cały czas",
     "перевод другого предложения"),
    # 9231 Petition
    (16681, "example_ru", "Мы начали петицию против нового правила",
     "Мы запустили петицию против нового правила",
     "петицию запускают, а не начинают"),
    (16681, "example_uk", "Ми розпочали петицію проти нового правила",
     "Ми започаткували петицію проти нового правила",
     "петицію започатковують"),
    (16681, "example_tr", "Yeni kuralın karşısında bir dilekçe başlattık",
     "Yeni kurala karşı bir dilekçe başlattık",
     "«karşısında» это физически напротив"),
    (16681, "example_pl", "Podpisałem petycję przeciwko wycince drzew",
     "Rozpoczęliśmy petycję przeciwko nowej zasadzie",
     "перевод другого предложения"),
    # 9232 Praktikantin
    (9174, "example_tr",
     "Stajyer kız bütün gün basit görevlere yardım ediyor",
     "Stajyer kız bütün gün basit işlerde yardım ediyor",
     "«görevlere yardım» — не то управление"),
    # 9233 Hausfriedensbruch
    (16682, "example_tr",
     "Şüpheliyle eve tecavüz suçundan sorgulandı",
     "Eve giren kişi haneye tecavüz suçundan şikâyet edildi",
     "«Şüpheliyle» ломает фразу, и термин «haneye tecavüz»"),
    (16682, "example_pl",
     "Sąsiad zgłosił na policji naruszenie miru domowego",
     "Intruz został zgłoszony za naruszenie miru domowego",
     "перевод другого предложения"),
    # 9234 statistisch
    (18042, "example_ru", "Статистически люди толстеют меньше, чем раньше",
     "Статистически меньше людей страдают избыточным весом, чем раньше",
     "в эталоне не «толстеют меньше», а «меньше людей»"),
    (18042, "example_tr", "İstatistiksel olarak daha az insan fazla kilolu",
     "İstatistiksel olarak eskisinden daha az insan fazla kilolu",
     "потеряно «als früher»"),
    # 9235 Bombenleger
    (16683, "example_ru", "Полиция ищет террориста",
     "Полиция ищет подрывника",
     "перевод слова — «подрывник»"),
    (16683, "example_uk", "Поліція шукає терориста",
     "Поліція шукає підривника",
     "перевод слова — «підривник»"),
    (16683, "example_tr", "Polis bomba atıcısını arıyor",
     "Polis bombacıyı arıyor",
     "«bomba atıcısı» — не по-турецки"),
    (16683, "example_pl", "Policja od tygodnia szuka zamachowca",
     "Policja szuka zamachowca",
     "«od tygodnia» в эталоне нет"),
    # 9236 Sozialismus
    (16684, "example_pl", "Moi dziadkowie żyli jeszcze w socjalizmie",
     "Socjalizm to ideologia polityczna XX wieku",
     "перевод другого предложения"),
    # 9237 angebunden — эталон с ломаным порядком слов
    (8169, "example_de", "Der Hund war angebunden an einem langen Seil",
     "Der Hund war an einem langen Seil angebunden",
     "причастие должно стоять в конце"),
    (8169, "example_uk", "Собака була прив'язана довгою мотузкою",
     "Собака була прив'язана на довгій мотузці",
     "привязывают не мотузкой, а на мотузці"),
    (8169, "example_pl", "Pies był przywiązany do drzewa",
     "Pies był przywiązany na długiej linie",
     "перевод другого предложения"),
    # 9238 verbitten
    (11290, "example_en", "I won't tolerate such insults",
     "I will not tolerate this insult",
     "эталон о одном конкретном оскорблении"),
    (11290, "example_uk", "Я не допущу такого образи",
     "Я не допущу такої образи",
     "рассогласование рода"),
    (11290, "example_tr", "Patron gecikmelerden hiç hoşnut olmadı",
     "Bu hakareti kesinlikle kabul etmiyorum",
     "перевод совершенно другого предложения"),
    # 9239 Kruste
    (11923, "example_tr", "Ekmeğin çıtır altın-kahverengi kabuğu var",
     "Ekmeğin çıtır çıtır altın kahverengi bir kabuğu var",
     "«çıtır» одиночное и дефис не по-турецки"),
    # 9240 saftig
    (11924, "translation_tr", "sulu, etli, tuzlu",
     "sulu, etli, dolgun",
     "«tuzlu» это солёный, а «saftig» в третьем значении — солидный"),
    (11924, "translation_pl", "soczysty, wilgotny, słony",
     "soczysty, wilgotny, pokaźny",
     "«słony» это солёный, а «saftig» в третьем значении — солидный"),
    # 9241 Wachhund
    (18399, "example_tr", "Bekçi köpek bütün alanı koruyor",
     "Bekçi köpeği bütün alanı koruyor",
     "потерян изафет"),
    (18399, "example_pl", "Nasz pies obronny pilnuje całego podwórka",
     "Pies obronny pilnuje całego terenu",
     "«Nasz» в эталоне нет, «Gelände» это территория"),
    # 9242 Liebesbrief — «Freund» здесь парень, а не друг
    (11291, "example_en", "She received a romantic love letter from her friend",
     "She received a romantic love letter from her boyfriend",
     "любовное письмо от «друга» меняет смысл"),
    (11291, "example_ru",
     "Она получила романтическое любовное письмо от своего друга",
     "Она получила романтическое любовное письмо от своего парня",
     "«Freund» здесь парень"),
    (11291, "example_uk",
     "Вона отримала романтичний любовний лист від свого друга",
     "Вона отримала романтичний любовний лист від свого хлопця",
     "«Freund» здесь хлопець"),
    (11291, "example_tr", "Arkadaşından romantik bir aşk mektubu aldı",
     "Erkek arkadaşından romantik bir aşk mektubu aldı",
     "«arkadaş» это товарищ"),
    (11291, "example_pl", "Napisał jej długi list miłosny",
     "Dostała romantyczny list miłosny od swojego chłopaka",
     "перевод другого предложения"),
    # 9243 Inszenierung
    (14706, "example_tr", "Oyunun sahne tasarımı etkileyiciydi",
     "Oyunun sahnelenmesi etkileyiciydi",
     "«sahne tasarımı» это декорации, а не постановка"),
    (14706, "example_pl", "Inscenizacja tej sztuki była świetna",
     "Inscenizacja tej sztuki teatralnej była imponująca",
     "«beeindruckend» — впечатляющая"),
    # 9244 vorhersehen
    (8170, "translation_uk", "передбачати, передвгадувати",
     "передбачати, передчувати",
     "«передвгадувати» — нет такого слова"),
    (8170, "example_pl", "Nikt nie mógł tego przewidzieć",
     "Nie mogłem przewidzieć tego problemu",
     "перевод другого предложения"),
    # 9246 Visite
    (12969, "example_tr", "Doktor hastane odalarında tur yapıyor",
     "Doktor hasta odalarında vizite yapıyor",
     "«hastane odası» это палата больницы вообще, и «vizite»"),
    # 9247 Ensemble
    (14707, "example_ru", "Ансамбль сыграл чудесное представление",
     "Ансамбль дал чудесное представление",
     "представление дают, а не играют"),
    (14707, "example_uk", "Ансамбль зіграв чудесне представлення",
     "Ансамбль дав чудову виставу",
     "«чудесне представлення» — русизм"),
    (14707, "example_pl", "Zespół zagrał wspaniały koncert",
     "Zespół dał wspaniałe przedstawienie",
     "«Aufführung» это спектакль, не концерт"),
    # 9249 verzehren
    (11925, "example_uk", "Ця робота поглинає весь мій час",
     "Голод поволі виснажує його",
     "перевод другого предложения"),
    (11925, "example_tr", "Pişmanlık onun içini kemiriyor",
     "Açlık onu yavaş yavaş tüketiyor",
     "перевод другого предложения"),
    # 9250 miterleben
    (8171, "example_uk", "Я бачив ту аварію на власні очі",
     "Мені довелося побачити цей концерт на власні очі, "
     "і це було фантастично",
     "перевод другого предложения"),
    (8171, "example_tr", "Konseri yaşamak şansı buldum ve harika oldu",
     "Konseri bizzat yaşama şansı buldum ve harikaydı",
     "«yaşamak şansı» без изафета не держится"),
    (8171, "example_pl", "Mogłem na własne oczy przeżyć ten koncert",
     "Mogłem przeżyć ten koncert na własne oczy i był fantastyczny",
     "потеряна вторая половина"),
    # 9252 Mobiltelefon
    (17675, "example_pl", "Zostawiłem telefon komórkowy w domu",
     "Mój telefon komórkowy jest zepsuty, muszę kupić nowy",
     "перевод другого предложения"),
    # 9254 gebar
    (15244, "example_pl", "Urodziła zdrowego chłopca w szpitalu",
     "Po długiej chorobie urodziła zdrowe dziecko",
     "перевод другого предложения"),
    # 9256 Schäfchen
    (15751, "example_uk", "Маленьке ягня слідує за своєю матір'ю скрізь",
     "Маленька овечка скрізь іде за своєю матір'ю",
     "перевод слова — «овечка», и «слідує» канцелярит"),
    (15751, "example_pl", "Na łące pasie się mała owieczka",
     "Mała owieczka chodzi za swoją matką wszędzie",
     "перевод другого предложения"),
    # 9257 ausfahren
    (17317, "example_en",
     "The ambulance driver had to head out quickly to save the patient",
     "Tomorrow we deliver the parcels",
     "перевод совершенно другого предложения"),
    (17317, "example_ru",
     "Водитель скорой должен был быстро выехать, чтобы спасти пациента",
     "Завтра мы развозим посылки",
     "перевод совершенно другого предложения"),
    (17317, "example_uk",
     "Водій швидкої мав швидко виїхати, щоб врятувати пацієнта",
     "Завтра ми розвозимо посилки",
     "перевод совершенно другого предложения"),
    (17317, "example_tr",
     "Ambulans şoförü hastayı kurtarmak için hızlı çıkmak zorunda kaldı",
     "Yarın paketleri dağıtıyoruz",
     "перевод совершенно другого предложения"),
    # 9260 Schlich
    (11295, "example_tr", "Polis onun hileleri fark etti ve onu tutukladı",
     "Polis onun hilelerini fark etti ve onu tutukladı",
     "потерян аккузатив"),
    (11295, "example_pl", "Policja przejrzała jego sztuczki",
     "Policja przejrzała jego sztuczki i go aresztowała",
     "потеряна вторая половина"),
    # 9261 Pose
    (8173, "example_tr", "Ayna önünde özgüvenli bir poz veriyordu",
     "Aynanın önünde özgüvenli bir pozda duruyordu",
     "в эталоне «stand», а не «позировал», и потерян изафет"),
    (8173, "example_pl", "Ustawił się w śmiesznej pozie do zdjęcia",
     "Stał przed lustrem w pewnej siebie pozie",
     "перевод другого предложения"),
    # 9262 wurscht
    (11296, "example_en", "Pizza or pasta, it's all the same to me",
     "I don't care what you do, do what you want",
     "перевод другого предложения"),
    (11296, "example_uk", "Мені байдуже, що ти робиш, робити що хочеш",
     "Мені байдуже, що ти робиш, роби що хочеш",
     "«робити» вместо повелительного"),
    # 9263 durchgeknallte
    (11297, "example_uk", "Його божевільний брат піднімав галас у вітальні",
     "Його схибнутий брат зчинив галас у вітальні",
     "перевод слова — «схибнутий», и «піднімав галас»"),
    # 9264 befriedigend
    (1233, "example_tr", "Notu yeterli derecede iyi",
     "Notu yeterli",
     "«yeterli derecede iyi» это уже другая оценка"),
    # 9266 wegräumen — слова ряда в примере нет: там «aufräumen»
    (3004, "example_de", "Räum dein Zimmer auf!",
     "Räum deine Sachen weg!",
     "в примере «aufräumen», а ряд про «wegräumen»"),
    (3004, "example_en", "Tidy your room",
     "Put your things away",
     "вслед за эталоном"),
    (3004, "example_ru", "Убери свою комнату!",
     "Убери свои вещи!",
     "вслед за эталоном"),
    (3004, "example_uk", "Прибери свою кімнату",
     "Прибери свої речі",
     "вслед за эталоном"),
    (3004, "example_tr", "Odanı topla ve kaldır",
     "Eşyalarını yerine kaldır",
     "вслед за эталоном"),
    (3004, "example_pl", "Sprzątnij swój pokój!",
     "Odłóż swoje rzeczy na miejsce!",
     "вслед за эталоном"),
    # 9267 schwängern
    (12970, "example_uk",
     "Він не хотів залишити її вагітною, це була помилка",
     "Він не хотів зробити її вагітною, це була випадковість",
     "«залишити вагітною» — не то слово, и «Missgeschick»"),
    (12970, "example_tr",
     "Onu hamile bırakmak istemiyordu, bu bir kaza idi",
     "Onu hamile bırakmak istemiyordu, bu bir kazaydı",
     "«idi» отдельно"),
    # 9269 Staatssekretär
    (16685, "example_pl", "Sekretarz stanu zastąpił ministra na spotkaniu",
     "Sekretarz stanu reprezentuje ministra na ważnych spotkaniach",
     "эталон в настоящем и о регулярном представительстве"),
    # 9270 Abschleppwagen
    (17318, "example_tr", "Çekici aracı yoldan çekip aldı",
     "Çekici, arabayı yoldan aldı",
     "«Çekici aracı» читается как один предмет"),
    # 9271 Flegel
    (11299, "example_uk", "Цей грубіян поводить себе жахливо за столом",
     "Цей грубіян поводиться жахливо за столом",
     "«поводить себе» — русизм"),
    # 9272 auseinandernehmen
    (8174, "example_pl", "Musiałem rozebrać silnik na części",
     "Muszę rozebrać silnik na części, żeby go naprawić",
     "эталон в настоящем, и потеряна цель"),
    # 9273 kulturell
    (14708, "example_pl", "To było ciekawe wydarzenie kulturalne",
     "Wydarzenie kulturalne było naprawdę imponujące",
     "«ciekawe» вместо «beeindruckend»"),
    # 9275 Sozialversicherungsnummer
    (16686, "example_tr", "Başvuru için sosyal güvenlik numaranız gerekli",
     "Başvuru için sosyal güvenlik numaran gerekli",
     "эталон обращается на «ты»"),
    # 9276 Schwätzer
    (11301, "example_uk", "Цей балабол говорить без упину",
     "Цей балабол ніколи не може тримати язик за зубами",
     "перевод другого предложения"),
    (11301, "example_tr", "O geveze hiç ağzını kapatamiyor",
     "O geveze hiç ağzını kapatamıyor",
     "латинская «i» вместо «ı»"),
    # 9278 Leckerbissen
    (11926, "example_tr", "Bu, ince insanlar için gerçek bir lezzetti",
     "Bu, gurmeler için gerçek bir lezzetti",
     "«Feinschmecker» переведено как «тонкие люди»"),
    # 9282 Sägewerk
    (9177, "example_tr", "Şehirdeki eski testere fabrikası yenilendi",
     "Şehirdeki eski kereste fabrikası yenilendi",
     "«testere fabrikası» это завод пил"),
    # 9283 Todesopfer
    (16687, "example_tr", "Kaza birkaç ölüm kurbanına neden oldu",
     "Kazada birkaç can kaybı oldu",
     "«ölüm kurbanı» — тавтология"),
    (16687, "example_pl", "W wypadku były trzy ofiary śmiertelne",
     "W wypadku było kilka ofiar śmiertelnych",
     "«trzy» в эталоне нет"),
    # 9284 gleich
    (8175, "example_pl", "Chcę to samo co ty",
     "Chce tego samego co jego brat",
     "перевод другого предложения"),
    # 9285 Frust
    (2490, "example_en", "I'm very frustrated",
     "I'm very frustrated because the project failed",
     "потеряна вторая половина"),
    (2490, "example_uk", "У мене сильна фрустрація",
     "У мене сильне розчарування, бо проект провалився",
     "потеряна вторая половина"),
    (2490, "example_tr", "Çok bıkkınım",
     "Proje başarısız olduğu için büyük bir hayal kırıklığı içindeyim",
     "потеряна вторая половина"),
    # 9287 dampfen
    (8176, "example_ru", "Еда ещё дымит, она слишком горячая",
     "От еды ещё идёт пар, она слишком горячая",
     "еда не дымит, от неё идёт пар"),
    (8176, "example_uk", "Пічка димить на всю кімнату",
     "Від їжі ще йде пара, вона занадто гаряча",
     "перевод другого предложения"),
    # 9289 abrupt
    (8178, "example_uk", "Це була дуже різка зміна погоди",
     "Історія закінчується різко, без пояснення",
     "перевод другого предложения"),
    (8178, "example_pl", "To był bardzo nagły koniec rozmowy",
     "Historia kończy się nagle, bez wyjaśnienia",
     "перевод другого предложения"),
    # 9291 dichten
    (14709, "example_pl", "Wieczorami lubi pisać wiersze",
     "Poeta pisał wspaniałe wiersze",
     "перевод другого предложения"),
    # 9293 Eidechse
    (15753, "example_uk", "Ящірка грілася на камені",
     "Ящірка гріється на камені",
     "эталон в настоящем времени"),
    (15753, "example_tr", "Kertenkele taş üzerine ısınıyor",
     "Kertenkele taşın üzerinde güneşleniyor",
     "не тот падеж, и «sich sonnen» — греться на солнце"),
    # 9294 andersherum
    (8179, "example_pl", "Nie tak — przekręć to na odwrót",
     "Nie tak, na odwrót, proszę",
     "перевод другого предложения"),
    # 9295 Käsekuchen
    (11927, "example_uk", "Моя бабуся завжди пече смачні сирники",
     "Моя бабуся завжди пече смачний сирник",
     "«сирники» это оладки, а ряд про пиріг"),
    # 9296 Strafverfolgung
    (16688, "example_pl", "Sprawca uniknął ścigania karnego",
     "Ściganie karne tego przestępstwa nie było proste",
     "перевод другого предложения"),
    # 9297 unterliegen
    (8180, "example_uk", "Цей товар обміну не підлягає",
     "План підлягає суворим правилам",
     "перевод другого предложения"),
    (8180, "example_pl", "Wszyscy podlegają tym samym zasadom",
     "Plan podlega surowym zasadom",
     "перевод другого предложения"),
    # 9300 umschauen
    (8181, "example_tr", "Etrafını bakıyor ve şehri görüyor",
     "Etrafına bakıyor ve şehri görüyor",
     "«bakmak» требует датива"),
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

    print(f"=== правок {len(FIXES)}, совпало {len(ok)}, "
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
