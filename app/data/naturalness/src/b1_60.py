"""B1, блок 60: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    17169: ("«Die Eisenbahn war früher …» — претерит, учебник", {**all_x(
        "Mit der Eisenbahn dauert die Fahrt sechs Stunden", "На поезде поездка займёт шесть часов",
        "Поїздом подорож триває шість годин", "By train the journey takes six hours", "Trenle yolculuk altı saat sürüyor",
        "Pociągiem podróż trwa sześć godzin", "In treno il viaggio dura sei ore", "En tren el viaje dura seis horas",
        "En train, le trajet dure six heures", "Vlakem trvá cesta šest hodin")}),
    3035: ("«Ich kann zaubern» — пусто", {**all_x(
        "Sie hat in zehn Minuten ein tolles Essen gezaubert",
        "Она за десять минут сотворила отличный ужин", "За десять хвилин вона як за помахом чарівної палички приготувала чудову вечерю",
        "She conjured up a great meal in ten minutes", "On dakikada harika bir yemek ortaya çıkardı",
        "W dziesięć minut wyczarowała świetny obiad", "In dieci minuti ha fatto una magia: una cena fantastica",
        "En diez minutos hizo magia y preparó una comida estupenda",
        "En dix minutes, elle a fait de la magie et préparé un super repas", "Za deset minut vykouzlila skvělé jídlo")}),
    1226: (LIST, {"t_ru": "обрабатывать, редактировать", "t_uk": "опрацьовувати, редагувати", "t_en": "to process, to edit",
                  "t_tr": "işlemek, düzenlemek", "t_pl": "opracowywać, edytować"}),
    1429: ("убрать пометки (coloq.)/(fam.)", {"t_es": "coquetear, ligar", "t_fr": "flirter, draguer"}),
    736: ("«Der Pudding ist süß» — пусто", {**all_x(
        "Ich koche den Pudding mit Milch", "Я варю пудинг на молоке", "Я варю пудинг на молоці",
        "I make the pudding with milk", "Pudingi sütle pişiriyorum", "Gotuję budyń na mleku",
        "Preparo il budino con il latte", "Hago el pudin con leche", "Je fais la crème dessert avec du lait",
        "Vařím pudink s mlékem")}),
    2330: ("«Der Container ist voll» — пусто", {**all_x(
        "Wirf die Flaschen in den Container", "Брось бутылки в контейнер", "Викинь пляшки в контейнер",
        "Put the bottles in the container", "Şişeleri konteynere at", "Wrzuć butelki do kontenera",
        "Butta le bottiglie nel cassonetto", "Tira las botellas al contenedor", "Jette les bouteilles dans le conteneur",
        "Hoď lahve do kontejneru")}),
    231: ("«Sie hat eine Erkältung» — пусто", {**all_x(
        "Ich glaube, ich bekomme eine Erkältung", "Кажется, у меня начинается простуда", "Здається, у мене починається застуда",
        "I think I'm coming down with a cold", "Sanırım soğuk algınlığına yakalanıyorum", "Chyba łapie mnie przeziębienie",
        "Credo di prendermi il raffreddore", "Creo que estoy cogiendo un resfriado", "Je crois que j'attrape un rhume",
        "Asi na mě leze nachlazení")}),
    1134: ("ru «ты должен указать» — калька; анкета; " + LIST + "; убрать пометки", {
        "t_ru": "указывать, хвастаться", "t_uk": "зазначати, вихвалятися", "t_en": "to state, to show off",
        "t_tr": "belirtmek, hava atmak", "t_pl": "podawać, przechwalać się", "t_it": "indicare, vantarsi",
        "t_es": "indicar, presumir", "t_fr": "indiquer, frimer", "t_cs": "uvést, vytahovat se",
        **all_x("Gib doch nicht so an!", "Не хвастайся так!", "Не вихваляйся так!", "Stop showing off!",
                "Bu kadar hava atma!", "Nie przechwalaj się tak!", "Non vantarti così!", "¡No presumas tanto!",
                "Arrête de frimer!", "Nevytahuj se tak!")}),
    16264: ("ru «одобрила» / de «genehmigt» — время не совпадает; канцелярит", {**all_x(
        "Wende dich bitte an die Verwaltung", "Обратись, пожалуйста, в администрацию", "Звернися, будь ласка, до адміністрації",
        "Please contact the administration", "Lütfen yönetime başvur", "Zwróć się, proszę, do administracji",
        "Rivolgiti all'amministrazione, per favore", "Dirígete a la administración, por favor",
        "Adresse-toi à l'administration, s'il te plaît", "Obrať se prosím na správu")}),
    2382: (LIST, {"t_ru": "вставлять, делать (перерыв)", "t_uk": "вставляти, робити (перерву)", "t_en": "to insert, to take (a break)",
                  "t_tr": "yerleştirmek, ara vermek", "t_pl": "wkładać, robić (przerwę)", "t_it": "inserire, fare (una pausa)",
                  "t_es": "introducir, hacer (una pausa)", "t_fr": "insérer, faire (une pause)", "t_cs": "vložit, udělat si (přestávku)"}),
    1557: ("«Wir gehen in die Innenstadt» — шаблон «gehen»", {**all_x(
        "In der Innenstadt findet man nie einen Parkplatz", "В центре города никогда не найдёшь парковку",
        "У центрі міста ніколи не знайдеш паркування", "You can never find a parking space in the city centre",
        "Şehir merkezinde hiç park yeri bulunmaz", "W centrum miasta nigdy nie można znaleźć miejsca parkingowego",
        "In centro non si trova mai parcheggio", "En el centro nunca se encuentra aparcamiento",
        "Au centre-ville, on ne trouve jamais de place", "V centru nikdy nenajdeš parkovací místo")}),
    377: ("«Ich trage Handschuhe» — шаблон одежды", {**all_x(
        "Ich habe einen Handschuh im Bus verloren", "Я потерял перчатку в автобусе", "Я загубив рукавичку в автобусі",
        "I lost a glove on the bus", "Otobüste bir eldivenimi kaybettim", "Zgubiłem rękawiczkę w autobusie",
        "Ho perso un guanto sull'autobus", "He perdido un guante en el autobús", "J'ai perdu un gant dans le bus",
        "Ztratil jsem rukavici v autobuse")}),
    2046: ("«Die Agentur vermittelt Wohnungen» — шаблон Agentur; " + LIST + " (было шесть значений)", {
        "t_ru": "передавать, помогать найти", "t_uk": "передавати, допомагати знайти", "t_en": "to convey, to find for someone",
        "t_tr": "aktarmak, bulmak", "t_pl": "przekazywać, pomagać znaleźć", "t_it": "trasmettere, procurare",
        "t_es": "transmitir, conseguir", "t_fr": "transmettre, trouver", "t_cs": "předávat, zprostředkovat",
        **all_x("Sie hat mir einen Job vermittelt", "Она помогла мне найти работу", "Вона допомогла мені знайти роботу",
                "She found me a job", "Bana iş buldu", "Pomogła mi znaleźć pracę", "Mi ha procurato un lavoro",
                "Me consiguió un trabajo", "Elle m'a trouvé un boulot", "Zprostředkovala mi práci")}),
    1500: ("«Der Grill ist heiß» — пусто", {**all_x(
        "Wirf schon mal den Grill an!", "Разжигай уже гриль!", "Розпалюй уже мангал!", "Get the barbecue going!",
        "Mangalı yakmaya başla!", "Odpal już grilla!", "Accendi pure il barbecue!", "¡Ve encendiendo la barbacoa!",
        "Allume déjà le barbecue!", "Rozpal už gril!")}),
    1781: ("«Das ist ein guter Ratschlag» — пусто", {**all_x(
        "Ich brauche keinen Ratschlag, ich will nur reden", "Мне не нужен совет, я просто хочу поговорить",
        "Мені не потрібна порада, я просто хочу поговорити", "I don't need advice, I just want to talk",
        "Öğüde ihtiyacım yok, sadece konuşmak istiyorum", "Nie potrzebuję rady, chcę tylko pogadać",
        "Non mi serve un consiglio, voglio solo parlare", "No necesito un consejo, solo quiero hablar",
        "Je n'ai pas besoin de conseil, je veux juste parler", "Nepotřebuju radu, chci si jen promluvit")}),
    3009: ("«Kann ich dir weiterhelfen?» — шаблон behilflich", {**all_x(
        "Tut mir leid, da kann ich Ihnen nicht weiterhelfen", "Извините, тут я вам помочь не могу",
        "Вибачте, тут я вам допомогти не можу", "Sorry, I can't help you with that",
        "Üzgünüm, bu konuda size yardımcı olamam", "Przepraszam, w tym nie mogę pomóc",
        "Mi dispiace, non posso aiutarla", "Lo siento, en eso no puedo ayudarle", "Désolé, là je ne peux pas vous aider",
        "Promiňte, s tím vám nepomůžu")}),
    1927: ("«Wir tanzen Tango» — пусто", {**all_x(
        "Zum Tango gehören immer zwei", "Для танго нужны двое", "Для танго потрібні двоє", "It takes two to tango",
        "Tango iki kişiyle yapılır", "Do tanga trzeba dwojga", "Per ballare il tango bisogna essere in due",
        "Para bailar tango hacen falta dos", "Il faut être deux pour danser le tango", "K tangu jsou potřeba dva")}),
    2289: ("«Der Betrag ist 100 Euro» — пусто", {**all_x(
        "Bitte überweisen Sie den Betrag bis Freitag", "Пожалуйста, переведите сумму до пятницы", "Будь ласка, перекажіть суму до п'ятниці",
        "Please transfer the amount by Friday", "Lütfen tutarı cumaya kadar havale edin", "Proszę przelać kwotę do piątku",
        "La preghiamo di bonificare l'importo entro venerdì", "Por favor, transfiera el importe antes del viernes",
        "Veuillez virer le montant d'ici vendredi", "Prosím převeďte částku do pátku")}),
    10607: ("«Das ist ein ungerechter Vorwurf» — шаблон ungerecht", {**all_x(
        "Ich mache dir keinen Vorwurf", "Я тебя не упрекаю", "Я тобі не дорікаю", "I'm not blaming you",
        "Seni suçlamıyorum", "Nie robię ci wyrzutów", "Non ti sto rimproverando", "No te lo reprocho",
        "Je ne te fais pas de reproche", "Nevyčítám ti to")}),
    12661: ("«Ich putze mir die Zähne mit meiner Zahnbürste» — масло масляное", {**all_x(
        "Ich habe meine Zahnbürste vergessen", "Я забыл зубную щётку", "Я забув зубну щітку", "I've forgotten my toothbrush",
        "Diş fırçamı unuttum", "Zapomniałem szczoteczki do zębów", "Ho dimenticato lo spazzolino",
        "Me he olvidado el cepillo de dientes", "J'ai oublié ma brosse à dents", "Zapomněl jsem si zubní kartáček")}),
    3044: ("«Die Vase wurde zerschlagen» — претерит", {**all_x(
        "Unsere Pläne haben sich zerschlagen", "Наши планы сорвались", "Наші плани зірвалися", "Our plans fell through",
        "Planlarımız suya düştü", "Nasze plany się rozsypały", "I nostri piani sono andati a monte",
        "Nuestros planes fracasaron", "Nos projets ont échoué", "Naše plány zkrachovaly")}),
    1325: ("«Der Computer ist defekt» — шаблон «ist kaputt»", {**all_x(
        "Die Ampel ist schon seit Tagen defekt", "Светофор уже несколько дней неисправен", "Світлофор уже кілька днів несправний",
        "The traffic light has been broken for days", "Trafik ışığı günlerdir arızalı", "Sygnalizacja jest zepsuta od kilku dni",
        "Il semaforo è guasto da giorni", "El semáforo lleva días averiado", "Le feu est en panne depuis des jours",
        "Semafor je už několik dní porouchaný")}),
}

SPLIT_LATER = {}
