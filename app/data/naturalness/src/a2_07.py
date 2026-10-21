"""A2, блок 7: слова 241–280 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
SKEL = "пример-скелет («X ist alt/dunkel») — так о вещи не говорят"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    801: (SKEL + "; " + LIST, {
        "t_ru": "боль", "t_uk": "біль", "t_en": "pain, ache", "t_tr": "ağrı, acı", "t_pl": "ból",
        **all_x("Ich habe Schmerzen im Knie", "У меня боль в колене", "У мене біль у коліні",
                "I've got pain in my knee", "Dizimde ağrı var", "Czuję ból w kolanie", "Ho un dolore al ginocchio",
                "Tengo dolor en la rodilla", "J'ai une douleur au genou", "Mám bolesti v koleni")}),
    1484: (LIST, {"t_en": "healthy", "t_tr": "sağlıklı", "t_pl": "zdrowy"}),
    639: ("«Nachts ist es dunkel» — детская книжка", {
        "t_en": "at night", "t_tr": "geceleri", "t_pl": "w nocy, nocą",
        **all_x("Ich arbeite oft nachts", "Я часто работаю по ночам", "Я часто працюю ночами",
                "I often work at night", "Sık sık geceleri çalışıyorum", "Często pracuję w nocy",
                "Lavoro spesso di notte", "A menudo trabajo de noche", "Je travaille souvent la nuit",
                "Často pracuji v noci")}),
    8752: (LIST + "; «результат» — другое слово", {"t_ru": "успех, удача", "t_uk": "успіх", "t_en": "success",
                                                   "t_tr": "başarı", "t_pl": "sukces, powodzenie"}),
    6401: (LIST, {"t_ru": "быть похожим, походить", "t_uk": "бути схожим", "t_en": "to resemble, to be like",
                  "t_tr": "benzemek", "t_pl": "być podobnym, przypominać", "t_it": "somigliare",
                  "t_es": "parecerse", "t_cs": "podobat se"}),
    419: ("«зависеть» — это abhängen; " + LIST, {"t_ru": "висеть, вешать", "t_en": "to hang",
                                                 "t_fr": "être accroché, accrocher"}),
    81: (LIST, {"t_ru": "строить, собирать", "t_uk": "будувати", "t_en": "to build",
                "t_tr": "inşa etmek, yapmak", "t_pl": "budować"}),
    814: (LIST, {"t_tr": "hamile", "t_pl": "w ciąży"}),
    1834: (LIST + "; «я это сделал» — калька", {
        "t_ru": "в конце концов, ведь", "t_uk": "зрештою, адже", "t_en": "in the end, after all",
        "t_tr": "sonunda, ne de olsa", "t_pl": "w końcu, przecież", "t_it": "alla fine, dopotutto",
        "t_es": "al final, después de todo", "t_fr": "finalement, après tout", "t_cs": "nakonec, přece",
        "x_ru": "В конце концов у меня получилось", "x_uk": "Зрештою в мене вийшло"}),
    1855: (SKEL + "; " + LIST, {
        "t_ru": "сложный, трудный", "t_uk": "складний, важкий", "t_en": "difficult, hard", "t_tr": "zor",
        "t_pl": "trudny",
        **all_x("Die Prüfung war ziemlich schwierig", "Экзамен был довольно сложный", "Іспит був досить складний",
                "The exam was pretty difficult", "Sınav oldukça zordu", "Egzamin był dość trudny",
                "L'esame era piuttosto difficile", "El examen fue bastante difícil", "L'examen était assez difficile",
                "Zkouška byla docela těžká")}),
    13430: ("en «therefore» в разговоре не говорят; fr «c'est pourquoi» — книжно", {
        "t_en": "that's why, so", "t_tr": "bu yüzden", "t_pl": "dlatego",
        "x_en": "It's raining, that's why I'm staying home", "x_fr": "Il pleut, donc je reste à la maison"}),
    588: ("ru/uk «Стол длиной два метра» — обрывок", {"t_en": "metre",
                                                     "x_ru": "Стол два метра в длину", "x_uk": "Стіл завдовжки два метри"}),
    1414: (LIST + "; «был фантастическим» — книжно", {
        "t_ru": "потрясающий, фантастический", "t_uk": "фантастичний, чудовий", "t_en": "fantastic, amazing",
        "t_tr": "harika, muhteşem", "t_pl": "fantastyczny, świetny", "x_ru": "Фильм был потрясающий"}),
    2928: ("«Das Unternehmen wächst» — язык новостей; «затея» — другое слово", {
        "t_ru": "компания, фирма", "t_uk": "компанія, підприємство", "t_en": "company, business", "t_tr": "şirket",
        "t_pl": "firma, przedsiębiorstwo",
        **all_x("Ich arbeite in einem kleinen Unternehmen", "Я работаю в небольшой компании",
                "Я працюю в невеликій компанії", "I work for a small company", "Küçük bir şirkette çalışıyorum",
                "Pracuję w małej firmie", "Lavoro in una piccola azienda", "Trabajo en una empresa pequeña",
                "Je travaille dans une petite entreprise", "Pracuji v malé firmě")}),
    2008: ("«содержать» — другое значение; en «We are chatting well» — так не говорят", {
        "t_ru": "разговаривать, развлекать", "t_uk": "розмовляти, розважати", "t_en": "to chat, to entertain",
        "t_tr": "sohbet etmek, eğlendirmek", "t_pl": "rozmawiać, zabawiać", "t_it": "chiacchierare, intrattenere",
        "t_es": "charlar, entretener", "t_fr": "discuter, divertir", "t_cs": "bavit se, povídat si",
        **all_x("Wir haben uns lange unterhalten", "Мы долго разговаривали", "Ми довго розмовляли",
                "We chatted for a long time", "Uzun uzun sohbet ettik", "Długo rozmawialiśmy",
                "Abbiamo chiacchierato a lungo", "Estuvimos charlando mucho rato", "On a discuté longtemps",
                "Dlouho jsme si povídali")}),
    1232: (LIST + "; «о 17-й годині», «a las 17» — так время не называют", {
        "t_ru": "заканчивать, завершать", "t_uk": "закінчувати, завершувати", "t_en": "to finish, to end",
        "t_tr": "bitirmek", "t_pl": "kończyć, zakończyć", "t_it": "finire, terminare", "t_es": "terminar, acabar",
        "t_fr": "finir, terminer", "t_cs": "končit, ukončit",
        "x_uk": "Я закінчую роботу о п'ятій", "x_en": "I finish work at five", "x_it": "Finisco di lavorare alle cinque",
        "x_es": "Termino de trabajar a las cinco"}),
    698: (SKEL + " («Wir gehen in den Park» — как Wald)", {**all_x(
        "Der Park ist gleich um die Ecke", "Парк прямо за углом", "Парк одразу за рогом",
        "The park is just around the corner", "Park hemen köşede", "Park jest tuż za rogiem",
        "Il parco è proprio dietro l'angolo", "El parque está a la vuelta de la esquina",
        "Le parc est juste au coin de la rue", "Park je hned za rohem")}),
    13432: ("пример — обрывок, не предложение", {**all_x(
        "Das ist der Mann, dessen Auto hier steht", "Это тот мужчина, чья машина тут стоит",
        "Це той чоловік, чия машина тут стоїть", "That's the man whose car is parked here",
        "Arabası burada duran adam bu", "To ten pan, którego samochód tu stoi",
        "È l'uomo la cui macchina è parcheggiata qui", "Es el hombre cuyo coche está aparcado aquí",
        "C'est l'homme dont la voiture est garée ici", "To je ten muž, jehož auto tu stojí")}),
    13435: ("«нет» — другое слово (nee); «Das ist gut, ne?» — пусто", {
        "t_ru": "да?, правда?", "t_uk": "так?, правда?", "t_en": "right?", "t_tr": "değil mi?",
        "t_pl": "prawda?, no nie?", "t_fr": "non?, hein?",
        **all_x("Du kommst doch mit, ne?", "Ты же пойдёшь с нами, да?", "Ти ж підеш з нами, так?",
                "You're coming along, right?", "Sen de geliyorsun, değil mi?", "Idziesz z nami, no nie?",
                "Vieni anche tu, no?", "Vienes con nosotros, ¿no?", "Tu viens avec nous, hein?", "Půjdeš s námi, ne?")}),
    17060: (SKEL + "; " + LIST, {
        "t_ru": "мост", "t_uk": "міст", "t_pl": "most",
        **all_x("Nach der Brücke biegen Sie links ab", "После моста поверните налево", "Після мосту поверніть ліворуч",
                "After the bridge, turn left", "Köprüden sonra sola dönün", "Za mostem proszę skręcić w lewo",
                "Dopo il ponte giri a sinistra", "Después del puente, gire a la izquierda",
                "Après le pont, tournez à gauche", "Za mostem odbočte doleva")}),
    10128: (LIST + "; «Это же безумно» — так не говорят", {
        "t_ru": "сумасшедший, потрясающий", "t_uk": "божевільний, неймовірний", "t_en": "crazy, amazing",
        "t_tr": "çılgın, inanılmaz", "t_pl": "szalony, obłędny",
        "x_ru": "Это же безумие", "x_uk": "Це ж божевілля", "x_pl": "To jakieś szaleństwo"}),
    6421: ("«Geh vorwärts» — команда из учебника", {
        "t_en": "forward", "t_tr": "ileri", "t_pl": "do przodu", "t_it": "avanti", "t_fr": "en avant",
        **all_x("Fahr noch ein Stück vorwärts", "Проедь ещё немного вперёд", "Проїдь ще трохи вперед",
                "Move forward a bit more", "Biraz daha ileri git", "Podjedź jeszcze trochę do przodu",
                "Vai ancora un po' avanti", "Avanza un poco más", "Avance encore un peu", "Popojeď ještě kousek dopředu")}),
    10129: ("«У меня нет интереса», «Nie mam żadnego zainteresowania» — так не говорят", {
        "t_ru": "интерес", "t_uk": "інтерес, зацікавленість", "t_en": "interest", "t_tr": "ilgi",
        "t_pl": "zainteresowanie",
        **all_x("Ich habe kein Interesse an Fußball", "Футбол меня не интересует", "Футбол мене не цікавить",
                "I'm not interested in football", "Futbola ilgim yok", "Nie interesuję się piłką nożną",
                "Il calcio non mi interessa", "No me interesa el fútbol", "Le foot ne m'intéresse pas",
                "Fotbal mě nezajímá")}),
    1174: (LIST + "; pl «Uważaj na dziecko» — «берегись ребёнка»", {
        "t_ru": "присматривать, быть осторожным", "t_uk": "наглядати, бути обережним",
        "t_en": "to watch out, to look after", "t_pl": "uważać, pilnować", "t_it": "stare attento, badare",
        "t_es": "tener cuidado, cuidar", "t_fr": "faire attention, surveiller",
        "x_pl": "Popilnuj dziecka", "x_tr": "Çocuğa göz kulak ol"}),
    129: (LIST + "; «шутка с твоей стороны» — калька", {
        "t_ru": "глупый, дурацкий", "t_uk": "дурний, дурнуватий", "t_en": "stupid, silly", "t_tr": "aptal, saçma",
        "t_pl": "głupi",
        **all_x("Das war ein blöder Witz", "Это была дурацкая шутка", "Це був дурний жарт", "That was a silly joke",
                "Bu aptalca bir şakaydı", "To był głupi żart", "È stata una battuta stupida", "Qué chiste más tonto",
                "C'était une blague bête", "To byl hloupý vtip")}),
    6425: ("«Geh hinaus ins Freie» — книжно", {
        "t_ru": "наружу, на улицу", "t_uk": "назовні, надвір", "t_en": "out, outside", "t_tr": "dışarı",
        "t_pl": "na zewnątrz, na dwór", "t_it": "fuori", "t_es": "fuera, afuera", "t_cs": "ven",
        **all_x("Ich gehe kurz hinaus, frische Luft schnappen", "Я ненадолго выйду на улицу подышать",
                "Я ненадовго вийду надвір подихати", "I'm just going outside for some fresh air",
                "Biraz temiz hava almak için dışarı çıkıyorum", "Wyjdę na chwilę na dwór odetchnąć",
                "Esco un attimo fuori a prendere aria", "Salgo un momento fuera a tomar el aire",
                "Je vais dehors prendre l'air un moment", "Jdu na chvíli ven na vzduch")}),
    6426: (LIST, {"t_ru": "пустой, разряженный", "t_uk": "порожній, розряджений", "t_en": "empty, flat",
                  "t_tr": "boş", "t_pl": "pusty, rozładowany"}),
    1064: ("«Я желаю тебе» — лишнее «я»", {"t_en": "to wish, to want", "t_pl": "życzyć, chcieć",
                                         "x_ru": "Желаю тебе удачи", "x_uk": "Бажаю тобі удачі"}),
    10134: (LIST, {"t_ru": "плакать", "t_uk": "плакати"}),
    289: (LIST, {
        "t_ru": "радоваться", "t_uk": "радіти", "t_en": "to be glad, to look forward to",
        "t_tr": "sevinmek, memnun olmak", "t_pl": "cieszyć się", "t_it": "essere contento, non vedere l'ora",
        "t_es": "alegrarse", "t_fr": "se réjouir, être content",
        "x_uk": "Я дуже радий", "x_en": "I'm really pleased"}),
    6430: (LIST, {"t_ru": "система", "t_uk": "система", "t_en": "system", "t_tr": "sistem", "t_pl": "system"}),
    1737: (LIST, {"t_ru": "пользоваться, использовать", "t_uk": "користуватися, використовувати",
                  "t_en": "to use, to make use of", "t_tr": "kullanmak, yararlanmak", "t_pl": "korzystać, używać",
                  "t_it": "usare, sfruttare", "t_es": "usar, aprovechar", "t_cs": "používat, využívat"}),
    473: (SKEL, {**all_x(
        "Die Fahrräder stehen im Keller", "Велосипеды стоят в подвале", "Велосипеди стоять у підвалі",
        "The bikes are in the basement", "Bisikletler bodrumda", "Rowery stoją w piwnicy", "Le bici sono in cantina",
        "Las bicis están en el sótano", "Les vélos sont à la cave", "Kola jsou ve sklepě")}),
    1952: (LIST, {"t_en": "animal"}),
    15391: ("en «I give you a rose» — так не говорят", {**all_x(
        "Er hat ihr rote Rosen geschenkt", "Он подарил ей красные розы", "Він подарував їй червоні троянди",
        "He gave her red roses", "Ona kırmızı güller hediye etti", "Podarował jej czerwone róże",
        "Le ha regalato delle rose rosse", "Le regaló rosas rojas", "Il lui a offert des roses rouges",
        "Daroval jí červené růže")}),
    1546: (EN, {"x_en": "I hope everything works out"}),
    2467: ("«авиабилет» — другое слово; «Der Flug war angenehm» — язык анкет", {
        "t_ru": "полёт, рейс", "t_en": "flight", "t_tr": "uçuş", "t_pl": "lot",
        **all_x("Mein Flug hat Verspätung", "Мой рейс задерживается", "Мій рейс затримується", "My flight is delayed",
                "Uçuşum rötarlı", "Mój lot jest opóźniony", "Il mio volo è in ritardo", "Mi vuelo tiene retraso",
                "Mon vol a du retard", "Můj let má zpoždění")}),
    13438: ("en «What are you making from it?» — так не говорят", {
        "t_ru": "из этого", "t_uk": "з цього", "t_en": "out of it, from it", "t_tr": "bundan", "t_pl": "z tego",
        "t_es": "de eso",
        **all_x("Daraus wird nichts", "Из этого ничего не выйдет", "З цього нічого не вийде",
                "Nothing will come of it", "Bundan bir şey çıkmaz", "Nic z tego nie będzie",
                "Non ne verrà fuori niente", "De eso no saldrá nada", "Il n'en sortira rien", "Z toho nic nebude")}),
}

SPLIT_LATER = {}
