"""B1, блок 9: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
SKEL = "пример-скелет («Der Griff ist kaputt», «Die Übersetzung ist fertig») — пусто"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    2428: ("«Das ist eine schöne Erinnerung» — пусто", {**all_x(
        "Ich habe keine Erinnerung an den Unfall", "У меня не осталось воспоминаний об аварии",
        "У мене не залишилося спогадів про аварію", "I have no memory of the accident",
        "Kazayla ilgili hiçbir anım yok", "Nie mam żadnych wspomnień z wypadku",
        "Non ho nessun ricordo dell'incidente", "No tengo ningún recuerdo del accidente",
        "Je n'ai aucun souvenir de l'accident", "Na tu nehodu nemám žádnou vzpomínku")}),
    13445: (EN + " («Why are you not coming?»)", {"x_en": "Why aren't you coming?"}),
    6475: (EN + " («protection from rain»)", {"x_en": "We need shelter from the rain"}),
    2943: ("«Я преследую свою цель» — калька; " + LIST, {
        "t_ru": "преследовать, следить", "t_uk": "переслідувати, стежити", "t_en": "to follow, to pursue",
        "t_tr": "takip etmek, peşine düşmek", "t_pl": "śledzić, ścigać", "t_it": "seguire, inseguire",
        "t_es": "seguir, perseguir", "t_fr": "suivre, poursuivre", "t_cs": "sledovat, pronásledovat",
        **all_x("Ich habe das Gefühl, jemand verfolgt mich", "Мне кажется, меня кто-то преследует",
                "Мені здається, хтось мене переслідує", "I feel like someone's following me",
                "Biri beni takip ediyor gibi hissediyorum", "Mam wrażenie, że ktoś mnie śledzi",
                "Ho la sensazione che qualcuno mi segua", "Tengo la sensación de que alguien me sigue",
                "J'ai l'impression que quelqu'un me suit", "Mám pocit, že mě někdo sleduje")}),
    6477: (LIST, {"t_ru": "требовать, просить", "t_uk": "вимагати, просити", "t_en": "to demand, to charge",
                  "t_tr": "talep etmek, istemek", "t_pl": "żądać, wymagać", "t_it": "chiedere, pretendere",
                  "t_es": "pedir, exigir", "t_fr": "demander, exiger", "t_cs": "požadovat, chtít",
                  "x_en": "They're charging too much money"}),
    6478: (SKEL + "; " + LIST, {
        "t_ru": "ручка, рукоятка", "t_uk": "ручка, рукоятка", "t_en": "handle, grip", "t_tr": "sap, tutamak",
        "t_pl": "uchwyt, rączka", "t_it": "il manico, la maniglia", "t_es": "el asa, el mango", "t_fr": "la poignée, la prise",
        "t_cs": "držadlo, rukojeť",
        **all_x("Der Griff von der Tasche ist abgerissen", "У сумки оторвалась ручка", "У сумки відірвалася ручка",
                "The handle on the bag has come off", "Çantanın sapı koptu", "Urwał się uchwyt od torby",
                "Si è staccato il manico della borsa", "Se ha roto el asa del bolso", "La poignée du sac s'est arrachée",
                "Utrhlo se držadlo od tašky")}),
    710: ("в Германии Pfund — это полкило на рынке, а не валюта", {**all_x(
        "Ein Pfund Tomaten, bitte", "Полкило помидоров, пожалуйста", "Півкіло помідорів, будь ласка",
        "Half a kilo of tomatoes, please", "Yarım kilo domates lütfen", "Pół kilo pomidorów poproszę",
        "Mezzo chilo di pomodori, per favore", "Medio kilo de tomates, por favor", "Une livre de tomates, s'il vous plaît",
        "Půl kila rajčat, prosím")}),
    6481: ("«Она милое существо» — неживо", {**all_x(
        "Sie hat ein freundliches Wesen", "У неё дружелюбный характер", "У неї привітний характер",
        "She has a friendly nature", "Cana yakın bir huyu var", "Ma przyjazny charakter", "Ha un'indole gentile",
        "Tiene un carácter amable", "Elle a une nature aimable", "Má přátelskou povahu")}),
    2901: (SKEL, {**all_x(
        "Die deutsche Übersetzung ist besser als das Original", "Немецкий перевод лучше оригинала",
        "Німецький переклад кращий за оригінал", "The German translation is better than the original",
        "Almanca çeviri orijinalinden daha iyi", "Niemieckie tłumaczenie jest lepsze od oryginału",
        "La traduzione tedesca è meglio dell'originale", "La traducción alemana es mejor que el original",
        "La traduction allemande est meilleure que l'original", "Německý překlad je lepší než originál")}),
    13884: ("«Das ist doch Blödsinn» — шаблон Unsinn, Quatsch", {**all_x(
        "Mach keinen Blödsinn!", "Не делай глупостей!", "Не роби дурниць!", "Don't do anything stupid!",
        "Saçmalama!", "Nie rób głupot!", "Non fare stupidaggini!", "¡No hagas tonterías!", "Ne fais pas de bêtises!",
        "Nedělej blbosti!")}),
    8760: ("«Sie wurden alle entlassen» — пассив из новостей; " + LIST, {
        "t_ru": "уволить, выписать (из больницы)", "t_uk": "звільнити, виписати", "t_en": "to dismiss, to discharge",
        "t_tr": "işten çıkarmak, taburcu etmek", "t_pl": "zwolnić, wypisać", "t_it": "licenziare, dimettere",
        "t_es": "despedir, dar de alta", "t_fr": "licencier, laisser sortir", "t_cs": "propustit",
        **all_x("Morgen werde ich aus dem Krankenhaus entlassen", "Завтра меня выписывают из больницы",
                "Завтра мене виписують з лікарні", "I'm being discharged from hospital tomorrow",
                "Yarın hastaneden taburcu oluyorum", "Jutro wypisują mnie ze szpitala",
                "Domani mi dimettono dall'ospedale", "Mañana me dan el alta del hospital",
                "Demain, on me laisse sortir de l'hôpital", "Zítra mě propustí z nemocnice")}),
    12485: ("«Der Hund hat einen Knochen» — пусто, и снова Hund", {**all_x(
        "Mir tun alle Knochen weh", "У меня ломит все кости", "У мене болять усі кістки",
        "Every bone in my body aches", "Bütün kemiklerim ağrıyor", "Bolą mnie wszystkie kości",
        "Mi fanno male tutte le ossa", "Me duelen todos los huesos", "J'ai mal à tous les os",
        "Bolí mě všechny kosti")}),
    14939: ("«Она подарила ему поцелуй» — книжно", {"x_ru": "Она его поцеловала", "x_uk": "Вона його поцілувала"}),
    2808: (EN + " («Of course, that's obvious»)", {"x_en": "That goes without saying"}),
    10161: (EN + " («This cursed computer»)", {"x_en": "This damn computer just won't work"}),
    6491: ("«Ich finde es nirgendwo» — шаблон nirgends («… nirgends finden»)", {**all_x(
        "Hier gibt es nirgendwo einen Parkplatz", "Здесь нигде нет парковки", "Тут ніде немає парковки",
        "There's nowhere to park around here", "Burada hiçbir yerde park yeri yok",
        "Tu nigdzie nie ma miejsca do parkowania", "Qui non c'è un parcheggio da nessuna parte",
        "Aquí no hay aparcamiento en ninguna parte", "Il n'y a de place de parking nulle part ici",
        "Tady není nikde parkoviště")}),
    133: ("«Die Braut trägt ein weißes Kleid» — шаблон одежды и Kleid; " + LIST, {
        "t_ru": "невеста", "t_uk": "наречена, молода", "t_en": "bride", "t_tr": "gelin", "t_pl": "panna młoda",
        **all_x("Auf der Hochzeit hat die Braut eine Rede gehalten", "На свадьбе невеста произнесла речь",
                "На весіллі наречена виголосила промову", "The bride gave a speech at the wedding",
                "Düğünde gelin bir konuşma yaptı", "Na weselu panna młoda wygłosiła przemowę",
                "Al matrimonio la sposa ha fatto un discorso", "En la boda la novia dio un discurso",
                "Au mariage, la mariée a fait un discours", "Na svatbě měla nevěsta proslov")}),
}

# nirgendwo — вариант того же nirgends
REPLACE = [{"id": 6491, "by": 6726, "lang": "de", "why": "nirgendwo — вариант того же nirgends"}]

SPLIT_LATER = {}
