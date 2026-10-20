"""A1, блок 19: слова 721–741 по частоте — конец A1. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
TWO = "в строке два разных слова — оставлено главное, второе — отдельной строкой (блок деления)"
EN = "английский пример: так не говорят"
DULL = "пример ни о чём («Der X verb») → фраза из жизни"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    103: (TWO + " («определённый» — прилагательное bestimmt, своя строка)", {
        "t_ru": "точно, наверняка", "t_uk": "напевно, точно", "t_en": "definitely, surely", "t_tr": "kesinlikle, mutlaka",
        "t_pl": "na pewno", "t_it": "sicuramente", "t_es": "seguro, seguramente", "t_fr": "sûrement, certainement",
        "t_cs": "určitě", "x_en": "He'll definitely come"}),
    315: ("tr «Saygıdeğer» — книжно, в письмах «Sayın»", {"t_ru": "уважаемый", "t_uk": "шановний", "t_en": "dear",
                                                         "t_tr": "sayın", "t_pl": "szanowny",
                                                         "x_tr": "Sayın Bayan Müller"}),
    384: ("«die Hausaufgabe machen» — по-немецки во множественном: Hausaufgaben", {**all_x(
        "Sie macht gerade Hausaufgaben", "Она сейчас делает домашнее задание", "Вона зараз робить домашнє завдання",
        "She's doing her homework", "Şu anda ödevini yapıyor", "Właśnie odrabia pracę domową", "Sta facendo i compiti",
        "Está haciendo los deberes", "Elle est en train de faire ses devoirs", "Zrovna dělá domácí úkol")}),
    613: (EN, {"x_en": "I'll come tomorrow"}),
    723: (LIST, {"t_en": "postcode, zip code"}),
    734: ("«Hier ist ein Prospekt» — пример ни о чём", {**all_x(
        "Nimm dir einen Prospekt mit", "Возьми буклет", "Візьми брошуру", "Take a brochure", "Bir broşür al",
        "Weź sobie ulotkę", "Prendi un dépliant", "Llévate un folleto", "Prends une brochure", "Vezmi si prospekt")}),
    756: (LIST + "; «рейс» — другое слово", {"t_ru": "поездка, путешествие", "t_uk": "подорож, поїздка",
                                            "t_en": "trip, journey", "t_tr": "seyahat, yolculuk", "t_pl": "podróż"}),
    810: (LIST + "; " + EN, {"t_ru": "писать, написать", "t_en": "to write", "x_en": "I'm writing a letter"}),
    823: (DULL, {"t_ru": "школьник, ученик", "t_uk": "учень, школяр", "t_en": "pupil", "t_tr": "öğrenci",
                 **all_x("Die Schüler haben heute frei", "У школьников сегодня выходной", "У школярів сьогодні вихідний",
                         "The pupils have the day off today", "Öğrencilerin bugün tatili var", "Uczniowie mają dziś wolne",
                         "Oggi gli alunni sono liberi", "Hoy los alumnos tienen el día libre",
                         "Les élèves n'ont pas cours aujourd'hui", "Žáci mají dnes volno")}),
    892: (DULL, {"t_en": "student", **all_x(
        "Mein Bruder ist Student in München", "Мой брат — студент в Мюнхене", "Мій брат — студент у Мюнхені",
        "My brother is a student in Munich", "Kardeşim Münih'te öğrenci", "Mój brat jest studentem w Monachium",
        "Mio fratello è studente a Monaco", "Mi hermano es estudiante en Múnich", "Mon frère est étudiant à Munich",
        "Můj bratr je student v Mnichově")}),
    980: (DULL, {"t_en": "shop assistant, salesperson", "t_tr": "satıcı", **all_x(
        "Ich frage mal den Verkäufer", "Спрошу у продавца", "Спитаю в продавця", "I'll ask the shop assistant",
        "Satıcıya bir sorayım", "Zapytam sprzedawcę", "Chiedo al commesso", "Le pregunto al dependiente",
        "Je vais demander au vendeur", "Zeptám se prodavače")}),
    1007: (LIST, {"t_ru": "что", "t_uk": "що", "t_en": "what", "t_tr": "ne", "t_pl": "co", "t_it": "che cosa, cosa",
                  "t_es": "qué", "t_fr": "que, quoi"}),
    1138: (LIST, {"t_ru": "кликнуть, нажать", "t_uk": "клікнути, натиснути", "t_en": "to click", "t_tr": "tıklamak",
                  "t_pl": "kliknąć"}),
    1139: (TWO + " («зависеть», «иметь успех» — свои строки)", {
        "t_ru": "прибывать, приезжать", "t_uk": "прибувати, приїжджати", "t_en": "to arrive", "t_tr": "varmak",
        "t_pl": "przyjeżdżać, docierać", "t_it": "arrivare", "t_es": "llegar", "t_fr": "arriver", "t_cs": "přijet, dorazit"}),
    1140: (LIST + "; «выбрать вариант в анкете» — пояснение", {
        "t_ru": "отметить, поставить крестик", "t_uk": "позначити, поставити хрестик", "t_en": "to tick",
        "t_tr": "işaretlemek", "t_pl": "zaznaczyć"}),
    2045: (DULL + "; " + LIST, {
        "t_ru": "хозяин квартиры, арендодатель", "t_uk": "орендодавець, господар квартири", "t_en": "landlord",
        "t_tr": "ev sahibi", "t_pl": "wynajmujący, właściciel mieszkania",
        **all_x("Ich muss den Vermieter anrufen", "Мне нужно позвонить хозяину квартиры", "Мені треба подзвонити орендодавцю",
                "I need to call the landlord", "Ev sahibini aramam lazım", "Muszę zadzwonić do właściciela mieszkania",
                "Devo chiamare il padrone di casa", "Tengo que llamar al casero", "Je dois appeler le propriétaire",
                "Musím zavolat pronajímateli")}),
    2423: (DULL + "; " + LIST, {
        "t_ru": "результат, итог", "t_uk": "результат, підсумок", "t_en": "result, score", "t_tr": "sonuç, skor",
        "t_pl": "wynik", "t_it": "il risultato", "t_es": "el resultado", "t_fr": "le résultat, le score",
        "t_cs": "výsledek",
        **all_x("Was war das Ergebnis vom Spiel?", "Какой результат у матча?", "Який результат матчу?",
                "What was the result of the match?", "Maçın sonucu ne oldu?", "Jaki był wynik meczu?",
                "Qual è stato il risultato della partita?", "¿Cuál fue el resultado del partido?",
                "Quel a été le résultat du match?", "Jaký byl výsledek zápasu?")}),
    2539: ("«Мы бронируем полупансион» — калька; «завтрак и ужин» в переводе — пояснение", {
        "t_ru": "полупансион", "t_uk": "напівпансіон", "t_en": "half board", "t_tr": "yarım pansiyon",
        "t_pl": "niepełne wyżywienie",
        "x_ru": "Мы берём полупансион", "x_uk": "Ми беремо напівпансіон", "x_en": "We're booking half board"}),
}

SPLIT_LATER = {
    103: ["bestimmt = определённый (ein bestimmter Tag)"],
    1139: ["es kommt darauf an = зависит", "gut ankommen = иметь успех"],
}
