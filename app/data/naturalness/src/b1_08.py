"""B1, блок 8: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
SKEL = "пример-скелет («Der Kapitän ist auf dem Schiff», «Der Gang ist dunkel») — пусто"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    6453: ("«Das ist vollkommen richtig» — книжно; " + LIST, {
        "t_ru": "совершенно, полностью", "t_uk": "абсолютно, цілком", "t_en": "completely, perfect",
        "t_tr": "tamamen, kusursuz", "t_pl": "całkowicie, doskonały", "t_it": "completamente, perfettamente",
        "t_es": "completamente, totalmente", "t_fr": "tout à fait, parfaitement", "t_cs": "naprosto, dokonale",
        **all_x("Du hast vollkommen recht", "Ты совершенно прав", "Ти абсолютно правий", "You're completely right",
                "Tamamen haklısın", "Masz całkowitą rację", "Hai perfettamente ragione", "Tienes completamente razón",
                "Tu as tout à fait raison", "Máš naprostou pravdu")}),
    10143: ("«Die Idioten fahren viel zu schnell» — неживо", {**all_x(
        "Ich bin so ein Idiot!", "Какой же я идиот!", "Який же я ідіот!", "I'm such an idiot!", "Ne kadar aptalım!",
        "Ale ze mnie idiota!", "Che idiota che sono!", "¡Qué idiota soy!", "Quel idiot je suis!", "Já jsem ale idiot!")}),
    8755: ("«Mein Bruder ist Soldat» — пусто, шаблон «Mein Bruder …»", {**all_x(
        "Er war zwei Jahre Soldat", "Он два года служил солдатом", "Він два роки був солдатом",
        "He was a soldier for two years", "İki yıl askerlik yaptı", "Przez dwa lata był żołnierzem",
        "È stato soldato per due anni", "Fue soldado durante dos años", "Il a été soldat pendant deux ans",
        "Dva roky byl vojákem")}),
    10144: ("«Die beiden wollen sich küssen» — неживо", {**all_x(
        "Er hat sie zum Abschied geküsst", "Он поцеловал её на прощание", "Він поцілував її на прощання",
        "He kissed her goodbye", "Vedalaşırken onu öptü", "Pocałował ją na pożegnanie", "L'ha baciata per salutarla",
        "La besó para despedirse", "Il l'a embrassée pour lui dire au revoir", "Na rozloučenou ji políbil")}),
    6457: ("«Rauchen ist hier nicht erlaubt» — табличка", {**all_x(
        "Ist es erlaubt, hier zu fotografieren?", "Здесь разрешено фотографировать?", "Тут дозволено фотографувати?",
        "Are you allowed to take photos here?", "Burada fotoğraf çekmek serbest mi?", "Czy wolno tu robić zdjęcia?",
        "È permesso fare foto qui?", "¿Está permitido hacer fotos aquí?", "C'est autorisé de prendre des photos ici?",
        "Je tady povoleno fotit?")}),
    2643: (LIST, {"t_ru": "склад, лагерь", "t_uk": "склад, табір", "t_en": "warehouse, camp", "t_tr": "depo, kamp",
                  "t_pl": "magazyn, obóz", "t_it": "il magazzino, il campo", "t_es": "el almacén, el campamento",
                  "t_fr": "l'entrepôt, le camp", "t_cs": "sklad, tábor"}),
    10145: (LIST, {"t_ru": "знакомый, близкий", "t_uk": "знайомий, близький", "t_en": "familiar, close",
                   "t_tr": "tanıdık, yakın", "t_pl": "znajomy, bliski", "t_it": "familiare, intimo",
                   "t_es": "familiar, íntimo", "t_fr": "familier, intime", "t_cs": "známý, důvěrný"}),
    14378: (LIST, {"t_ru": "сцена, скандал", "t_uk": "сцена, скандал", "t_en": "scene", "t_tr": "sahne, olay",
                   "t_pl": "scena, awantura", "t_it": "la scena, la scenata", "t_es": "la escena, el escándalo",
                   "t_fr": "la scène", "t_cs": "scéna, výstup"}),
    6462: ("перевод — список из шести; " + LIST, {
        "t_ru": "сдаваться, отправлять (посылку)", "t_uk": "здаватися, відправляти", "t_en": "to give up, to post",
        "t_tr": "vazgeçmek, postaya vermek", "t_pl": "poddać się, nadać", "t_it": "arrendersi, spedire",
        "t_es": "rendirse, facturar", "t_fr": "abandonner, poster", "t_cs": "vzdát se, podat"}),
    17913: ("«Das Labor ist heute geschlossen» — шаблон Museum, Neujahr", {**all_x(
        "Die Ergebnisse aus dem Labor kommen morgen", "Результаты из лаборатории придут завтра",
        "Результати з лабораторії прийдуть завтра", "The lab results come in tomorrow",
        "Laboratuvar sonuçları yarın çıkacak", "Wyniki z laboratorium będą jutro",
        "I risultati del laboratorio arrivano domani", "Los resultados del laboratorio llegan mañana",
        "Les résultats du labo arrivent demain", "Výsledky z laboratoře přijdou zítra")}),
    8756: (SKEL, {**all_x(
        "Der Kapitän der Mannschaft ist erst neunzehn", "Капитану команды всего девятнадцать",
        "Капітанові команди лише дев'ятнадцять", "The team captain is only nineteen",
        "Takım kaptanı sadece on dokuz yaşında", "Kapitan drużyny ma dopiero dziewiętnaście lat",
        "Il capitano della squadra ha solo diciannove anni", "El capitán del equipo tiene solo diecinueve años",
        "Le capitaine de l'équipe n'a que dix-neuf ans", "Kapitánovi týmu je teprve devatenáct")}),
    13881: ("«Das war nur ein Scherz» — шаблон bloß («Das ist bloß ein Scherz»)", {**all_x(
        "Mach keine Scherze!", "Брось шутить!", "Не жартуй!", "Stop joking!", "Şaka yapma!", "Nie żartuj!",
        "Non scherzare!", "¡No bromees!", "Arrête de plaisanter!", "Nežertuj!")}),
    1907: ("«Er wollte mein Geld stehlen» — пусто", {**all_x(
        "Mir wurde im Zug das Handy gestohlen", "У меня в поезде украли телефон", "У мене в поїзді вкрали телефон",
        "My phone was stolen on the train", "Trende telefonum çalındı", "W pociągu ukradli mi telefon",
        "Mi hanno rubato il telefono in treno", "Me robaron el móvil en el tren",
        "On m'a volé mon portable dans le train", "Ve vlaku mi ukradli mobil")}),
    2497: (SKEL + "; перевод — список из пяти", {
        "t_ru": "коридор, передача (в машине)", "t_uk": "коридор, передача", "t_en": "corridor, gear",
        "t_tr": "koridor, vites", "t_pl": "korytarz, bieg", "t_it": "il corridoio, la marcia", "t_es": "el pasillo, la marcha",
        "t_fr": "le couloir, la vitesse", "t_cs": "chodba, rychlost",
        **all_x("Die Toilette ist am Ende des Gangs", "Туалет в конце коридора", "Туалет у кінці коридору",
                "The toilet is at the end of the corridor", "Tuvalet koridorun sonunda", "Toaleta jest na końcu korytarza",
                "Il bagno è in fondo al corridoio", "El baño está al final del pasillo",
                "Les toilettes sont au bout du couloir", "Záchod je na konci chodby")}),
    182: ("«im Dienst der Polizei» — канцелярски", {**all_x(
        "Er ist heute nicht im Dienst", "Он сегодня не на дежурстве", "Він сьогодні не на чергуванні",
        "He's not on duty today", "Bugün nöbette değil", "Dzisiaj nie jest na dyżurze", "Oggi non è in servizio",
        "Hoy no está de servicio", "Il n'est pas de service aujourd'hui", "Dnes nemá službu")}),
    15953: ("«Der Bürgermeister kommt heute» — пусто", {**all_x(
        "Der Bürgermeister hat das neue Schwimmbad eröffnet", "Мэр открыл новый бассейн", "Мер відкрив новий басейн",
        "The mayor opened the new swimming pool", "Belediye başkanı yeni yüzme havuzunu açtı",
        "Burmistrz otworzył nowy basen", "Il sindaco ha inaugurato la nuova piscina",
        "El alcalde ha inaugurado la nueva piscina", "Le maire a inauguré la nouvelle piscine",
        "Starosta otevřel nový bazén")}),
    494: ("«Er verletzt sich am Knie» — шаблон Arm, Finger; «Schmerzen im Knie» — у Schmerz", {**all_x(
        "Der Rock geht bis zum Knie", "Юбка длиной до колена", "Спідниця до коліна", "The skirt comes down to the knee",
        "Etek dize kadar", "Spódnica jest do kolan", "La gonna arriva al ginocchio", "La falda llega hasta la rodilla",
        "La jupe arrive au genou", "Sukně je ke kolenům")}),
}

SPLIT_LATER = {}
