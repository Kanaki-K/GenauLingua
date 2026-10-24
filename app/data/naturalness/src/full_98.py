"""Полная вычитка, порция 98: один смысл во всех 10 языках, живой пример со словом карточки"""

T = "полная вычитка: "

FIXES = {
    13067: (T + "двойник с 12807 «бабушка в доме престарелых» — везде «по воскресеньям навещаем дедушку в доме престарелых»", {"example_de": "Sonntags besuchen wir Opa im Altenheim", "example_ru": "По воскресеньям мы навещаем дедушку в доме престарелых", "example_uk": "Щонеділі ми відвідуємо дідуся в будинку для літніх людей", "example_en": "On Sundays we visit Grandad at the care home", "example_tr": "Pazar günleri huzurevinde dedemi ziyaret ediyoruz", "example_pl": "W niedziele odwiedzamy dziadka w domu opieki", "example_it": "La domenica andiamo a trovare il nonno alla casa di riposo", "example_es": "Los domingos visitamos al abuelo en la residencia de ancianos", "example_fr": "Le dimanche, on rend visite à papi à la maison de retraite", "example_cs": "V neděli navštěvujeme dědu v domově pro seniory"}),
    14390: (T + "двойник с 12141 «зрители громко хлопали» — везде «в конце спектакля вся публика встала»", {"example_de": "Am Ende der Vorstellung stand das ganze Publikum auf", "example_ru": "В конце спектакля вся публика встала", "example_uk": "Наприкінці вистави вся публіка встала", "example_en": "At the end of the show the whole audience was on its feet", "example_tr": "Gösterinin sonunda bütün seyirciler ayağa kalktı", "example_pl": "Na koniec przedstawienia cała publiczność wstała z miejsc", "example_it": "Alla fine dello spettacolo tutto il pubblico era in piedi", "example_es": "Al final del espectáculo todo el público estaba de pie", "example_fr": "À la fin du spectacle, tout le public était debout", "example_cs": "Na konci představení celé publikum vstalo"}),
}

REPLACE = []
SPLIT_LATER = {}
