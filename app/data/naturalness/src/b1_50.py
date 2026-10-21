"""B1, блок 50: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    8853: ("«Er ist Ingenieur» — пусто", {**all_x(
        "Ingenieure werden überall gesucht", "Инженеров ищут везде", "Інженерів шукають усюди",
        "Engineers are in demand everywhere", "Mühendisler her yerde aranıyor", "Inżynierów szuka się wszędzie",
        "Gli ingegneri sono richiesti ovunque", "Se buscan ingenieros en todas partes", "On cherche des ingénieurs partout",
        "Inženýři jsou žádaní všude")}),
    18193: ("«Er holte die Axt …» — претерит, шаблон hacken", {**all_x(
        "Mit der Axt kann man sich leicht verletzen", "Топором легко пораниться", "Сокирою легко поранитися",
        "It's easy to hurt yourself with an axe", "Baltayla kolayca yaralanabilirsin", "Siekierą łatwo się zranić",
        "Con l'ascia è facile farsi male", "Con el hacha es fácil hacerse daño", "On se blesse facilement avec une hache",
        "Se sekerou se člověk snadno zraní")}),
    18706: ("«Sie arbeitet stundenlang» — пусто", {**all_x(
        "Sie telefoniert stundenlang mit ihrer Freundin", "Она часами болтает по телефону с подругой",
        "Вона годинами розмовляє телефоном із подругою", "She talks on the phone to her friend for hours",
        "Arkadaşıyla saatlerce telefonda konuşuyor", "Godzinami gada przez telefon z przyjaciółką",
        "Sta al telefono per ore con la sua amica", "Habla por teléfono durante horas con su amiga",
        "Elle passe des heures au téléphone avec son amie", "Celé hodiny telefonuje s kamarádkou")}),
    2975: (EN + "; " + LIST, {"t_ru": "нарушать, отвергнуть", "t_uk": "порушувати, відштовхнути",
                             "t_en": "to break (rules), to disown", "t_tr": "ihlal etmek, reddetmek",
                             "t_pl": "naruszać, wyrzec się", "x_en": "You're breaking the rules"}),
    10439: ("ru «Ты должен продержаться» — калька", {"x_ru": "Надо продержаться, даже если станет трудно",
                                                    "x_en": "You've got to hang in there, even when it gets tough"}),
    7041: ("ru «Мы должны обеспечить» — калька; " + LIST, {
        "t_ru": "обеспечить, изъять", "t_uk": "забезпечити, вилучити", "t_en": "to ensure, to confiscate",
        "t_tr": "sağlamak, el koymak", "t_pl": "zapewnić, zabezpieczyć", "t_it": "assicurarsi, sequestrare",
        "t_es": "asegurarse, incautar", "t_fr": "s'assurer, saisir", "t_cs": "zajistit, zabavit",
        "x_ru": "Надо обеспечить, чтобы всё пришло вовремя"}),
    17129: ("«Das Päckchen ist per Post angekommen» — шаблон Paket («Das Paket ist heute angekommen»)", {
        "t_ru": "посылка, пачка", "t_uk": "посилка, пачка", "t_en": "small parcel, packet", "t_tr": "küçük paket",
        "t_pl": "paczuszka, paczka", "t_it": "il pacchetto", "t_es": "el paquete", "t_fr": "le petit colis, le paquet",
        "t_cs": "balíček",
        **all_x("Ein Päckchen Taschentücher, bitte", "Пачку салфеток, пожалуйста", "Пачку серветок, будь ласка",
                "A packet of tissues, please", "Bir paket mendil, lütfen", "Paczkę chusteczek poproszę",
                "Un pacchetto di fazzoletti, per favore", "Un paquete de pañuelos, por favor",
                "Un paquet de mouchoirs, s'il vous plaît", "Jeden balíček kapesníků, prosím")}),
    10441: ("«Er stand hilflos vor dem Problem» — претерит", {**all_x(
        "Ich fühle mich so hilflos", "Я чувствую себя таким беспомощным", "Я почуваюся таким безпорадним",
        "I feel so helpless", "Kendimi çok çaresiz hissediyorum", "Czuję się taki bezradny", "Mi sento così impotente",
        "Me siento tan impotente", "Je me sens tellement impuissant", "Cítím se tak bezmocný")}),
    10442: ("«… von mir» — шаблон «Das war ein Versehen von mir»", {"t_en": "stupidity, stupid thing", **all_x(
        "Das war die größte Dummheit meines Lebens", "Это была самая большая глупость в моей жизни",
        "Це була найбільша дурість у моєму житті", "That was the most stupid thing of my life",
        "Hayatımın en büyük aptallığıydı", "To była największa głupota w moim życiu",
        "È stata la più grande stupidaggine della mia vita", "Fue la mayor tontería de mi vida",
        "C'était la plus grosse bêtise de ma vie", "To byla největší hloupost mého života")}),
    15027: ("ru «должен был продолжать жить» — калька", {"x_ru": "После несчастья ему пришлось жить дальше"}),
    16129: ("«Er versteckte einen Dolch …» — претерит", {**all_x(
        "Im Museum sieht man einen alten Dolch", "В музее можно увидеть старинный кинжал", "У музеї можна побачити старовинний кинджал",
        "You can see an old dagger in the museum", "Müzede eski bir hançer görebilirsin", "W muzeum można zobaczyć stary sztylet",
        "Al museo si vede un vecchio pugnale", "En el museo se puede ver un puñal antiguo",
        "Au musée, on peut voir un vieux poignard", "V muzeu je k vidění stará dýka")}),
    13992: ("«Wir plauderten gemütlich …» — претерит", {**all_x(
        "Komm, wir plaudern ein bisschen", "Давай немного поболтаем", "Давай трохи побалакаємо",
        "Come on, let's have a little chat", "Hadi biraz sohbet edelim", "Chodź, pogawędzimy trochę",
        "Dai, chiacchieriamo un po'", "Venga, charlamos un rato", "Viens, on bavarde un peu", "Pojď, trochu si popovídáme")}),
    7043: ("убрать пометки (colloq.)/(coloq.)/(fam.)/(hovor.)", {
        "t_it": "fantastico, figo", "t_es": "genial, guay", "t_fr": "génial, cool", "t_cs": "skvělý, super"}),
    7044: ("«Er streifte ihre Hand ganz leicht» — претерит", {**all_x(
        "Der Ball hat nur den Pfosten gestreift", "Мяч только задел штангу", "М'яч лише зачепив штангу",
        "The ball only grazed the post", "Top sadece direği sıyırdı", "Piłka tylko musnęła słupek",
        "Il pallone ha solo sfiorato il palo", "El balón solo rozó el poste", "Le ballon a juste effleuré le poteau",
        "Míč jen zavadil o tyč")}),
    2174: ("«Die Anerkennung ihrer Arbeit war …» — претерит", {**all_x(
        "Du verdienst Anerkennung für deine Arbeit", "Ты заслуживаешь признания за свою работу",
        "Ти заслуговуєш на визнання за свою роботу", "You deserve recognition for your work",
        "Emeğin için takdiri hak ediyorsun", "Zasługujesz na uznanie za swoją pracę",
        "Meriti riconoscimento per il tuo lavoro", "Mereces reconocimiento por tu trabajo",
        "Tu mérites de la reconnaissance pour ton travail", "Zasloužíš si uznání za svou práci")}),
    10445: ("«Igitt, das ist ja ekelhaft!» — шаблон eklig («Igitt, ist das eklig!»)", {**all_x(
        "Igitt, da ist eine Spinne!", "Фу, там паук!", "Фу, там павук!", "Ugh, there's a spider!", "Iyy, orada bir örümcek var!",
        "Fuj, tam jest pająk!", "Bleah, c'è un ragno!", "¡Puaj, hay una araña!", "Beurk, il y a une araignée!",
        "Fuj, tam je pavouk!")}),
    15028: ("в живой речи Muschi — грубое слово; «кошечка» — устаревшее/детское → C2", {"level": "C2"}),
    10446: ("«Er hatte einen Anfall von Wut …» — претерит", {**all_x(
        "Er bekommt gleich wieder einen Anfall", "У него сейчас опять будет припадок", "У нього зараз знову буде напад",
        "He's about to have another fit", "Birazdan yine kriz geçirecek", "Zaraz znowu dostanie ataku",
        "Tra poco gli viene un'altra crisi", "Ahora le va a dar otro ataque", "Il va encore faire une crise",
        "Za chvíli zase dostane záchvat")}),
    7045: ("пример многословный; " + LIST, {
        "t_ru": "рог, гудок", "t_uk": "ріг, гудок", "t_en": "horn", "t_tr": "boynuz, korna", "t_pl": "róg, klakson",
        "t_it": "il corno, il clacson", "t_es": "el cuerno, la bocina", "t_fr": "la corne, le klaxon", "t_cs": "roh, klakson",
        **all_x("Der Stier hat spitze Hörner", "У быка острые рога", "У бика гострі роги", "The bull has sharp horns",
                "Boğanın sivri boynuzları var", "Byk ma ostre rogi", "Il toro ha le corna appuntite",
                "El toro tiene los cuernos afilados", "Le taureau a des cornes pointues", "Býk má ostré rohy")}),
    8856: (EN + " («airplane» — американское); " + LIST, {
        "t_ru": "экипаж, оккупация", "t_uk": "екіпаж, окупація", "t_en": "crew, occupation", "t_tr": "mürettebat, işgal",
        "t_pl": "załoga, okupacja", "x_en": "The cabin crew are very friendly and helpful"}),
    7046: ("снова армия; " + LIST, {
        "t_ru": "снимать, вычитать", "t_uk": "знімати, відраховувати", "t_en": "to pull off, to deduct",
        "t_tr": "çıkarmak, düşmek", "t_pl": "zdjąć, odjąć", "t_it": "togliere, sottrarre", "t_es": "quitar, restar",
        "t_fr": "retirer, déduire", "t_cs": "stáhnout, odečíst",
        **all_x("Zieh bitte die Bettwäsche ab", "Сними, пожалуйста, постельное бельё", "Зніми, будь ласка, постільну білизну",
                "Please pull off the bedding", "Lütfen nevresimleri çıkar", "Zdejmij, proszę, pościel",
                "Togli le lenzuola, per favore", "Quita las sábanas, por favor", "Retire les draps, s'il te plaît",
                "Stáhni prosím povlečení")}),
    14455: (EN + " («vacation»)", {"x_en": "I'll bring you back a souvenir from my holiday"}),
    13993: ("снова Projekt", {**all_x(
        "Ohne deine Zustimmung mache ich nichts", "Без твоего согласия я ничего не сделаю", "Без твоєї згоди я нічого не зроблю",
        "I won't do anything without your consent", "Senin onayın olmadan hiçbir şey yapmam", "Bez twojej zgody nic nie zrobię",
        "Senza il tuo consenso non faccio niente", "Sin tu consentimiento no hago nada", "Sans ton accord, je ne fais rien",
        "Bez tvého souhlasu nic neudělám")}),
    16130: ("«Der Gefangene wurde freigelassen …» — претерит, хроника", {**all_x(
        "Lass den Vogel frei!", "Отпусти птицу на волю!", "Відпусти пташку на волю!", "Set the bird free!",
        "Kuşu serbest bırak!", "Wypuść ptaka na wolność!", "Libera l'uccellino!", "¡Libera al pájaro!", "Libère l'oiseau!",
        "Osvoboď toho ptáka!")}),
    10447: ("«… fühlte er sich deprimiert» — претерит", {**all_x(
        "Seit der Trennung ist er total deprimiert", "После расставания он совсем подавлен", "Після розставання він зовсім пригнічений",
        "He's been really depressed since the break-up", "Ayrılıktan beri çok moralsiz", "Od rozstania jest totalnie przygnębiony",
        "Dalla separazione è proprio depresso", "Desde la separación está muy deprimido",
        "Depuis la rupture, il est complètement déprimé", "Od rozchodu je úplně deprimovaný")}),
}

REPLACE = [
    {"id": 9476, "by": 735, "lang": "de", "why": "geprüft — причастие от prüfen"},
    {"id": 7048, "by": 805, "lang": "de", "why": "rasch — книжный вариант schnell"},
]

SPLIT_LATER = {}
