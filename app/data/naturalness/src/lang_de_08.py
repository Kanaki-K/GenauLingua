"""Вычитка немецкого, порция p008 (B1), 23.10: заглушки → живые бытовые фразы"""

W = "вычитка немецкого: учебная заглушка → живая бытовая фраза"

def ex(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"example_de": de, "example_ru": ru, "example_uk": uk, "example_en": en, "example_tr": tr,
            "example_pl": pl, "example_it": it, "example_es": es, "example_fr": fr, "example_cs": cs}

FIXES = {
    969: (W, ex("Die Untersuchung beim Arzt hat nur zehn Minuten gedauert",
        "Обследование у врача заняло всего десять минут", "Обстеження в лікаря тривало лише десять хвилин",
        "The examination at the doctor's only took ten minutes", "Doktordaki muayene sadece on dakika sürdü",
        "Badanie u lekarza trwało tylko dziesięć minut", "La visita dal medico è durata solo dieci minuti",
        "La revisión en el médico solo duró diez minutos", "L'examen chez le médecin n'a duré que dix minutes",
        "Vyšetření u lékaře trvalo jen deset minut")),
    1001: (W, ex("Die Wände hier sind so dünn, man hört jedes Wort",
        "Стены здесь такие тонкие, что слышно каждое слово", "Стіни тут такі тонкі, що чути кожне слово",
        "The walls here are so thin you can hear every word", "Buradaki duvarlar o kadar ince ki her kelime duyuluyor",
        "Ściany są tu takie cienkie, że słychać każde słowo", "Qui i muri sono così sottili che si sente ogni parola",
        "Aquí las paredes son tan finas que se oye cada palabra", "Ici, les murs sont si fins qu'on entend chaque mot",
        "Zdi jsou tu tak tenké, že je slyšet každé slovo")),
    1021: (W, ex("Mein Opa verkleidet sich jedes Jahr als Weihnachtsmann",
        "Мой дедушка каждый год наряжается Дедом Морозом", "Мій дідусь щороку перевдягається Дідом Морозом",
        "Every year my grandad dresses up as Father Christmas", "Dedem her yıl Noel Baba kılığına giriyor",
        "Mój dziadek co roku przebiera się za Świętego Mikołaja", "Mio nonno ogni anno si traveste da Babbo Natale",
        "Mi abuelo se disfraza de Papá Noel todos los años", "Mon grand-père se déguise en père Noël tous les ans",
        "Můj děda se každý rok převléká za Santa Clause")),
    1090: (W + "; почти повтор Verkehrsmittel (979)", ex("Die Toiletten im Park sind öffentlich und kostenlos",
        "Туалеты в парке общественные и бесплатные", "Туалети в парку громадські й безкоштовні",
        "The toilets in the park are public and free", "Parktaki tuvaletler halka açık ve ücretsiz",
        "Toalety w parku są publiczne i bezpłatne", "I bagni nel parco sono pubblici e gratuiti",
        "Los baños del parque son públicos y gratuitos", "Les toilettes du parc sont publiques et gratuites",
        "Záchody v parku jsou veřejné a zadarmo")),
    1221: (W + "; «die Basis unserer Arbeit» — корпоративный текст", ex("Bei meinen Soßen ist die Basis immer Zwiebel und Knoblauch",
        "Основа моих соусов — всегда лук и чеснок", "Основа моїх соусів — завжди цибуля й часник",
        "The basis of my sauces is always onion and garlic", "Soslarımın temeli hep soğan ve sarımsak",
        "Bazą moich sosów jest zawsze cebula i czosnek", "La base dei miei sughi è sempre cipolla e aglio",
        "La base de mis salsas siempre es cebolla y ajo", "La base de mes sauces, c'est toujours oignon et ail",
        "Základem mých omáček je vždycky cibule a česnek")),
    1279: (W + "; «Jeder hat einen anderen Bildungsweg» — пусто", ex("Mein Bildungsweg war nicht gerade: erst Lehre, dann Abitur, dann Studium",
        "Мой образовательный путь был непрямым: сначала профучилище, потом аттестат, потом вуз", "Мій освітній шлях був непрямий: спершу профучилище, потім атестат, потім виш",
        "My educational path wasn't straightforward: first an apprenticeship, then A levels, then university", "Eğitim yolum düz değildi: önce meslek eğitimi, sonra lise diploması, sonra üniversite",
        "Moja droga edukacji nie była prosta: najpierw szkoła zawodowa, potem matura, potem studia", "Il mio percorso di studi non è stato lineare: prima l'apprendistato, poi la maturità, poi l'università",
        "Mi trayectoria educativa no fue recta: primero FP, luego bachillerato y luego la carrera", "Mon parcours scolaire n'a pas été tout droit : d'abord l'apprentissage, puis le bac, puis la fac",
        "Moje vzdělávací cesta nebyla rovná: nejdřív učňák, pak maturita, pak vysoká")),
    1387: (W, ex("Am Wochenende will ich mich einfach nur entspannen",
        "На выходных я хочу просто расслабиться", "На вихідних я хочу просто розслабитися",
        "At the weekend I just want to relax", "Hafta sonu sadece rahatlamak istiyorum",
        "W weekend chcę się po prostu zrelaksować", "Nel fine settimana voglio solo rilassarmi",
        "El fin de semana solo quiero relajarme", "Le week-end, je veux juste me détendre",
        "O víkendu si chci prostě jen odpočinout")),
}

REPLACE = []

SPLIT_LATER = {}
