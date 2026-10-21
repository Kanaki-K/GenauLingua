"""A2, добор: 7 рядов, которые выгрузка по смещению пропустила 21.10.

Когда слово выключалось заменой (dennoch, jedoch, ebenso …) или уходило на
другой уровень, список уровня укорачивался на ряд, и следующий блок со
смещением +40 начинался на ряд дальше. genauso пришёл в A2 сам (B1→A2).
Выгрузка теперь берёт «ещё не виденные» ряды (`export_next.sh`).
"""

LIST = "список → главное слово и не больше одной альтернативы"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    326: ("«Ich denke genauso wie du» — так говорят «Das sehe ich genauso»; " + LIST, {
        "t_ru": "так же, точно так же", "t_uk": "так само", "t_en": "just as, the same way", "t_tr": "aynı şekilde, tıpkı",
        "t_pl": "tak samo", "t_it": "allo stesso modo, esattamente come", "t_es": "igual, del mismo modo",
        "t_fr": "de la même façon", "t_cs": "stejně",
        **all_x("Das sehe ich genauso", "Я считаю точно так же", "Я вважаю так само", "I see it the same way",
                "Ben de aynı şekilde düşünüyorum", "Uważam tak samo", "La vedo allo stesso modo", "Lo veo igual",
                "Je vois les choses de la même façon", "Vidím to stejně")}),
    895: ("«Setz dich auf den Stuhl» — команда из учебника", {**all_x(
        "Ist der Stuhl noch frei?", "Этот стул свободен?", "Цей стілець вільний?", "Is this chair free?",
        "Bu sandalye boş mu?", "Czy to krzesło jest wolne?", "È libera questa sedia?", "¿Está libre esta silla?",
        "Cette chaise est libre?", "Je tahle židle volná?")}),
    8763: ("en «performs very well» — книжно", {"x_en": "The actor is very good"}),
    8786: ("«Mein Mitarbeiter» — это подчинённый, а не коллега; " + LIST, {
        "t_ru": "сотрудник, работник", "t_uk": "співробітник, працівник", "t_en": "employee, staff member",
        "t_tr": "çalışan, personel", "t_pl": "pracownik, współpracownik",
        **all_x("Die Firma sucht neue Mitarbeiter", "Фирма ищет новых сотрудников", "Фірма шукає нових співробітників",
                "The company is looking for new staff", "Şirket yeni çalışan arıyor", "Firma szuka nowych pracowników",
                "L'azienda cerca nuovi collaboratori", "La empresa busca nuevos empleados",
                "L'entreprise cherche de nouveaux employés", "Firma hledá nové zaměstnance")}),
    14023: ("«Die Kritik war nicht ungerechtfertigt» — двойное отрицание из статьи", {
        "t_ru": "критика, рецензия", "t_uk": "критика, рецензія", "t_en": "criticism, review", "t_tr": "eleştiri",
        "t_pl": "krytyka, recenzja",
        **all_x("Danke für die Kritik, ich versuche es besser zu machen", "Спасибо за критику, постараюсь сделать лучше",
                "Дякую за критику, постараюся зробити краще", "Thanks for the criticism, I'll try to do better",
                "Eleştiri için teşekkürler, daha iyisini yapmaya çalışacağım",
                "Dzięki za krytykę, postaram się zrobić to lepiej", "Grazie per la critica, cercherò di fare meglio",
                "Gracias por la crítica, intentaré hacerlo mejor", "Merci pour la critique, je vais essayer de faire mieux",
                "Díky za kritiku, pokusím se to udělat líp")}),
    7528: (LIST, {"t_ru": "отмечать, выделять", "t_uk": "позначати, виділяти", "t_en": "to mark, to highlight",
                  "t_tr": "işaretlemek", "t_pl": "zaznaczać, oznaczać", "t_it": "segnare, evidenziare",
                  "t_es": "marcar, señalar", "t_fr": "marquer, surligner", "t_cs": "označit, zvýraznit"}),
}

SPLIT_LATER = {}
