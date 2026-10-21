"""B1, блок 15: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    6593: ("«Er ist angeblich krank» — шаблон anscheinend («Er ist anscheinend krank»)", {**all_x(
        "Angeblich hat er im Lotto gewonnen", "Он якобы выиграл в лотерею", "Він нібито виграв у лотерею",
        "He supposedly won the lottery", "Güya piyangoyu kazanmış", "Podobno wygrał w lotto",
        "A quanto pare ha vinto alla lotteria", "Supuestamente le ha tocado la lotería",
        "Il aurait soi-disant gagné au loto", "Prý vyhrál v loterii")}),
    6594: (LIST, {"t_ru": "выглядеть, действовать", "t_uk": "виглядати, діяти", "t_en": "to seem, to have an effect",
                  "t_tr": "görünmek, etki etmek", "t_pl": "wydawać się, działać", "t_it": "sembrare, fare effetto",
                  "t_es": "parecer, hacer efecto", "t_fr": "sembler, faire effet", "t_cs": "působit, účinkovat"}),
    2841: ("«Der Staat hilft» — пусто", {**all_x(
        "Der Staat zahlt einen Teil der Kosten", "Государство оплачивает часть расходов", "Держава оплачує частину витрат",
        "The state pays part of the costs", "Masrafların bir kısmını devlet ödüyor", "Państwo pokrywa część kosztów",
        "Lo Stato paga una parte delle spese", "El Estado paga una parte de los gastos", "L'État paie une partie des frais",
        "Stát platí část nákladů")}),
    17771: ("«Die Kuh gibt Milch» — из букваря", {**all_x(
        "Auf der Wiese stehen ein paar Kühe", "На лугу стоят несколько коров", "На лузі стоїть кілька корів",
        "There are a few cows in the meadow", "Çayırda birkaç inek var", "Na łące stoi kilka krów",
        "Sul prato ci sono alcune mucche", "En el prado hay unas cuantas vacas", "Il y a quelques vaches dans le pré",
        "Na louce stojí pár krav")}),
    6595: (LIST, {"t_ru": "команда, приказ", "t_uk": "команда, наказ", "t_en": "command, order", "t_tr": "komut, emir",
                  "t_pl": "komenda, rozkaz", "t_it": "il comando, l'ordine", "t_es": "la orden, el mando",
                  "t_fr": "l'ordre, le commandement", "t_cs": "povel, rozkaz"}),
    6596: ("перевод — список из восьми", {"t_ru": "записывать, принимать", "t_uk": "записувати, приймати",
                                          "t_en": "to record, to take in", "t_tr": "kaydetmek, kabul etmek",
                                          "t_pl": "nagrywać, przyjmować", "t_it": "registrare, accogliere",
                                          "t_es": "grabar, acoger", "t_fr": "enregistrer, accueillir",
                                          "t_cs": "nahrát, přijmout"}),
    10208: ("перевод — список из шести; «моя самая большая сила» — калька", {
        "t_ru": "сила, сильная сторона", "t_uk": "сила, сильна сторона", "t_en": "strength, strong point",
        "t_tr": "güç, güçlü yön", "t_pl": "siła, mocna strona", "t_it": "la forza, il punto di forza",
        "t_es": "la fuerza, el punto fuerte", "t_fr": "la force, le point fort", "t_cs": "síla, silná stránka",
        "x_ru": "Это моя самая сильная сторона", "x_uk": "Це моя найсильніша сторона"}),
    1844: ("«Ich hörte einen Schrei» — претерит, книжно", {**all_x(
        "Plötzlich habe ich einen Schrei gehört", "Вдруг я услышал крик", "Раптом я почув крик",
        "Suddenly I heard a scream", "Birden bir çığlık duydum", "Nagle usłyszałem krzyk",
        "All'improvviso ho sentito un urlo", "De repente oí un grito", "Tout à coup, j'ai entendu un cri",
        "Najednou jsem uslyšel výkřik")}),
    8774: ("перевод — список из шести; «Der Führer der Gruppe ist weg» — неживо", {
        "t_ru": "руководитель, гид", "t_uk": "керівник, гід", "t_en": "leader, guide", "t_tr": "lider, rehber",
        "t_pl": "przywódca, przewodnik", "t_it": "il capo, la guida", "t_es": "el líder, el guía",
        "t_fr": "le chef, le guide", "t_cs": "vedoucí, průvodce",
        **all_x("Der Führer zeigt uns die Burg", "Гид показывает нам замок", "Гід показує нам замок",
                "The guide is showing us the castle", "Rehber bize kaleyi gösteriyor", "Przewodnik pokazuje nam zamek",
                "La guida ci mostra il castello", "El guía nos enseña el castillo", "Le guide nous fait visiter le château",
                "Průvodce nám ukazuje hrad")}),
    2746: ("«Komm rechtzeitig» — команда из учебника", {**all_x(
        "Wir sind gerade noch rechtzeitig gekommen", "Мы едва успели вовремя", "Ми ледве встигли вчасно",
        "We got there just in time", "Tam zamanında geldik", "Ledwo zdążyliśmy na czas",
        "Siamo arrivati appena in tempo", "Hemos llegado justo a tiempo", "On est arrivés juste à temps",
        "Přišli jsme tak tak včas")}),
    2013: ("«Ich unterstütze dich» — пусто", {**all_x(
        "Meine Eltern unterstützen mich beim Studium", "Родители поддерживают меня во время учёбы",
        "Батьки підтримують мене під час навчання", "My parents support me while I'm studying",
        "Ailem üniversitede bana destek oluyor", "Rodzice wspierają mnie podczas studiów",
        "I miei genitori mi sostengono negli studi", "Mis padres me apoyan en los estudios",
        "Mes parents me soutiennent pendant mes études", "Rodiče mě podporují při studiu")}),
    2927: ("«Das ist gute Unterhaltung» — пусто", {**all_x(
        "Danke für die nette Unterhaltung", "Спасибо за приятную беседу", "Дякую за приємну бесіду",
        "Thanks for the nice chat", "Güzel sohbet için teşekkürler", "Dzięki za miłą rozmowę",
        "Grazie per la piacevole conversazione", "Gracias por la agradable conversación",
        "Merci pour cette conversation agréable", "Díky za příjemný rozhovor")}),
    2344: ("«Der Stoff ist dicht» — шаблон Stoff", {**all_x(
        "Der Wald ist hier sehr dicht", "Лес здесь очень густой", "Ліс тут дуже густий",
        "The forest is very dense here", "Orman burada çok sık", "Las jest tu bardzo gęsty",
        "Qui il bosco è molto fitto", "Aquí el bosque es muy tupido", "La forêt est très dense ici",
        "Les je tady hodně hustý")}),
    2685: ("ru «Я любопытный» — о характере, а не о «сейчас интересно»", {"x_ru": "Мне любопытно", "x_uk": "Мені цікаво"}),
    15980: ("«Der Minister hält eine Rede» — шаблон Präsident", {**all_x(
        "Der Minister ist zurückgetreten", "Министр ушёл в отставку", "Міністр пішов у відставку",
        "The minister has resigned", "Bakan istifa etti", "Minister podał się do dymisji", "Il ministro si è dimesso",
        "El ministro ha dimitido", "Le ministre a démissionné", "Ministr odstoupil")}),
    6605: ("«Das Essen ist sehr fein» — третий пример «Das Essen war …»", {**all_x(
        "Sie hat ein feines Gehör", "У неё тонкий слух", "У неї тонкий слух", "She has a fine ear",
        "Kulağı çok hassas", "Ma delikatny słuch", "Ha un udito fine", "Tiene un oído fino", "Elle a l'oreille fine",
        "Má jemný sluch")}),
    6608: ("«Das ist eindeutig falsch» — шаблон offensichtlich («Das ist offensichtlich falsch»)", {**all_x(
        "Die Antwort war eindeutig: Nein", "Ответ был однозначным: нет", "Відповідь була однозначна: ні",
        "The answer was clear: no", "Cevap netti: hayır", "Odpowiedź była jednoznaczna: nie",
        "La risposta è stata chiara: no", "La respuesta fue clara: no", "La réponse était claire: non",
        "Odpověď byla jednoznačná: ne")}),
    6609: (EN + " («Where are your keys located?»)", {"x_en": "Where are your keys?"}),
    14963: ("«Der Pater hält heute eine Messe» — шаблон Priester", {**all_x(
        "Pater Michael kennt jeden im Dorf", "Патер Михаэль знает всех в деревне", "Патер Міхаель знає всіх у селі",
        "Father Michael knows everyone in the village", "Peder Michael köydeki herkesi tanıyor",
        "Ojciec Michał zna wszystkich we wsi", "Padre Michael conosce tutti in paese",
        "El padre Michael conoce a todo el mundo en el pueblo", "Le père Michael connaît tout le monde au village",
        "Páter Michael zná každého ve vesnici")}),
}

SPLIT_LATER = {}
