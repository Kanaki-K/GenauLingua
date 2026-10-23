"""Вычитка итальянского, порция p019 (B1), 23.10: «volentieri», повторы («temo che», «dopo mangiato beviamo», «la nonna fa…»), нет слова карточки"""

T = "вычитка итальянского: "

FIXES = {
    10434: (T + "«molto volentieri» — калька gern", {"example_it": "È una madre molto amorevole"}),
    10436: (T + "«esultano per la prima neve» — книжно", {"example_it": "Tutta la sala esulta quando il gruppo sale sul palco"}),
    10443: (T + "«situazione minacciosa» — книжно", {"example_it": "Il cielo è minaccioso, torniamo a casa"}),
    10459: (T + "повтор 10233 «che (non) funzioni»", {"example_it": "Dubito che dica la verità"}),
    10462: (T + "учебниково", {"example_it": "Apprezzo la tua sincerità"}),
    10463: (T + "повтор 10233 «Temo che»", {"example_it": "Temo un po' la riunione di domani"}),
    10548: (T + "«realisti con i nostri obiettivi» — книжно", {"example_it": "Sii realista, non finiremo mai prima di venerdì"}),
    10812: (T + "повтор 8285 «fischietta»", {"example_it": "I bambini giocano allegri in giardino"}),
    11134: (T + "повтор «la chiave»", {"example_it": "Il mio calzino è sparito in modo misterioso"}),
    11337: (T + "«I rumori forti spaventano il bambino» — учебниково", {"example_it": "La maschera del fratello ha spaventato la piccola"}),
    11542: (T + "без ситуации", {"example_it": "Difendo sempre i miei amici"}),
    11708: (T + "«Il bambino inghiotte» — учебниково", {"example_it": "Non riesco a inghiottire queste pastiglie enormi"}),
    11711: (T + "повтор «la nonna fa … più buone»", {"example_it": "La domenica mangiamo i pancake con lo sciroppo"}),
    11816: (T + "«currywurst» — не итальянский быт", {"example_it": "Mangiamo al volo un panino al chiosco"}),
    11850: (T + "повтор «per la tosse» (11851)", {"example_it": "Non mangiare troppe caramelle prima di cena"}),
    11854: (T + "повтор «la nonna fa da sé»", {"example_it": "Al nord si mangiano molti crauti"}),
    11891: (T + "нет слова карточки «il rinfresco»", {"example_it": "All'ingresso offrono un rinfresco"}),
    11944: (T + "повтор 11724 «al bar / all'osteria … birra»", {"example_it": "Abbiamo dormito in una vecchia locanda in montagna"}),
    11991: (T + "повтор 11677 «Dopo mangiato beviamo»", {"example_it": "Mia zia fa da sé il liquore di ciliegie"}),
    12028: (T + "«abbiamo arrostito» — учебниково", {"example_it": "A Natale mangiamo il tacchino"}),
    12098: (T + "«È un piacere per me» — калька", {"example_it": "Che piacere vederti!"}),
}

REPLACE = []

SPLIT_LATER = {}
