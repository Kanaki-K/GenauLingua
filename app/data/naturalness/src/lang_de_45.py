"""Вычитка немецкого, порция p045 (C1–C2), 23.10: заглушки → бытовые"""

W = "вычитка немецкого: учебная заглушка → живая бытовая фраза"

def ex(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"example_de": de, "example_ru": ru, "example_uk": uk, "example_en": en, "example_tr": tr,
            "example_pl": pl, "example_it": it, "example_es": es, "example_fr": fr, "example_cs": cs}

FIXES = {
    8449: (W + "; «multiple Probleme» — коряво", ex("Meine Kollegin hat multiple Sklerose und arbeitet trotzdem voll",
        "У моей коллеги рассеянный склероз, но она всё равно работает полный день", "У моєї колеги розсіяний склероз, але вона все одно працює повний день",
        "My colleague has multiple sclerosis and still works full-time", "İş arkadaşımda multipl skleroz var ama yine de tam gün çalışıyor",
        "Moja koleżanka z pracy ma stwardnienie rozsiane, a mimo to pracuje na cały etat", "La mia collega ha la sclerosi multipla e lavora comunque a tempo pieno",
        "Mi compañera tiene esclerosis múltiple y aun así trabaja a jornada completa", "Ma collègue a une sclérose en plaques et travaille quand même à plein temps",
        "Moje kolegyně má roztroušenou sklerózu a stejně pracuje na plný úvazek")),
    8518: (W, ex("Für die Bewerbung brauche ich noch eine kurze Vita mit Foto",
        "Для заявки на работу мне ещё нужно краткое резюме с фото", "Для подання на роботу мені ще потрібне коротке резюме з фото",
        "For the application I still need a short CV with a photo", "Başvuru için fotoğraflı kısa bir özgeçmiş daha lazım",
        "Do podania o pracę potrzebuję jeszcze krótkiego życiorysu ze zdjęciem", "Per la candidatura mi serve ancora un breve curriculum con foto",
        "Para la solicitud aún necesito un currículum breve con foto", "Pour la candidature, il me faut encore un petit CV avec photo",
        "K žádosti ještě potřebuju krátký životopis s fotkou")),
    8534: (W, ex("Umkreise im Text alle Verben mit Rot",
        "Обведи в тексте все глаголы красным", "Обведи в тексті всі дієслова червоним",
        "Circle all the verbs in the text in red", "Metindeki bütün fiilleri kırmızıyla daire içine al",
        "Zakreśl w tekście wszystkie czasowniki na czerwono", "Cerchia in rosso tutti i verbi del testo",
        "Rodea en rojo todos los verbos del texto", "Entoure tous les verbes du texte en rouge",
        "Zakroužkuj v textu všechna slovesa červeně")),
    8553: (W, ex("Um Mitternacht brennen alle auf der Straße ihr Feuerwerk ab",
        "В полночь все на улице запускают фейерверки", "Опівночі всі на вулиці запускають феєрверки",
        "At midnight everyone lets off their fireworks in the street", "Gece yarısı herkes sokakta havai fişeklerini patlatıyor",
        "O północy wszyscy na ulicy odpalają fajerwerki", "A mezzanotte tutti per strada accendono i fuochi d'artificio",
        "A medianoche todos tiran sus fuegos artificiales en la calle", "À minuit, tout le monde tire ses feux d'artifice dans la rue",
        "O půlnoci všichni na ulici odpalují ohňostroj")),
    8579: (W, ex("Nach dem Sturm versperrt ein umgestürzter Baum die Straße",
        "После бури улицу перегораживает упавшее дерево", "Після бурі вулицю перегороджує повалене дерево",
        "After the storm a fallen tree is blocking the road", "Fırtınadan sonra devrilmiş bir ağaç yolu kapatıyor",
        "Po burzy przewrócone drzewo blokuje ulicę", "Dopo la tempesta un albero caduto blocca la strada",
        "Después de la tormenta un árbol caído corta la calle", "Après la tempête, un arbre tombé barre la route",
        "Po bouři zatarasil silnici vyvrácený strom")),
    8582: (W, ex("Im Sommer wimmelt es am See von Mücken",
        "Летом у озера кишат комары", "Улітку біля озера аж кишить комарами",
        "In summer the lake is swarming with mosquitoes", "Yazın göl kenarı sivrisinek kaynıyor",
        "Latem nad jeziorem roi się od komarów", "D'estate al lago brulica di zanzare",
        "En verano el lago está plagado de mosquitos", "En été, le lac grouille de moustiques",
        "V létě se to u jezera hemží komáry")),
}

REPLACE = []

SPLIT_LATER = {}
