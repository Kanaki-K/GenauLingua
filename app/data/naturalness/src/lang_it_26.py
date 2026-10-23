"""Вычитка итальянского, порция p026 (B1/B2), 23.10: дом и время — повторы, кальки, нет слова карточки"""

T = "вычитка итальянского: "

FIXES = {
    18244: (T + "без ситуации", {"example_it": "Nel quartiere costruiranno una nuova scuola"}),
    18317: (T + "«Usiamo sempre … quando arriviamo» — громоздко", {"example_it": "Quando siamo in ritardo passiamo dall'ingresso sul retro"}),
    18320: (T + "«una teiera di tè» — тавтология", {"example_it": "Attento, la teiera è ancora calda"}),
    18349: (T + "повтор «decorare» (18412)", {"example_it": "Addobbiamo l'albero tutti insieme"}),
    18378: (T + "«Dov'è la sua residenza fissa?» — канцелярит", {"example_it": "Non ha una residenza fissa"}),
    18429: (T + "«molto idilliaca» — книжно", {"example_it": "La cittadina sulla costa era un vero sogno"}),
    18639: (T + "«ti corro dietro» — не тот смысл", {"example_it": "Corre sempre dietro al fratello maggiore"}),
    18664: (T + "нет слова карточки «la fretta»", {"example_it": "Nella fretta ho dimenticato il telefono"}),
    18678: (T + "«Per ora dobbiamo stare a vedere» — калька", {"example_it": "Stiamo a vedere cosa dice"}),
    18725: (T + "«dovrebbero imparare da noi» — книжно", {"example_it": "Ecco il mio futuro ufficio!"}),
    18744: (T + "«Non vogliamo poltrire» — калька", {"example_it": "Non resto tutto il giorno a poltrire"}),
    18751: (T + "повтор 18823 «il treno è in ritardo»", {"example_it": "Il volo in ritardo è finalmente decollato"}),
    18878: (T + "«Dovremmo partire presto» — калька", {"example_it": "Bisogna partire per tempo"}),
    18910: (T + "«ha fatto molto» — книжно", {"example_it": "L'inquilino precedente ha lasciato i mobili"}),
    18949: (T + "повтор 18948 «…sera … sempre»", {"example_it": "Giovedì sera sono impegnato, scusa"}),
    19030: (T + "«Lo ritengo una buona idea» — книжно", {"example_it": "Secondo me è una buona idea, proviamoci!"}),
    1272: (T + "«Dobbiamo» — калька", {"example_it": "Bisogna mantenere il sangue freddo"}),
    7092: (T + "повтор 9899 «tagliare l'etichetta»", {"example_it": "Ci hanno tagliato la corrente"}),
}

REPLACE = []

SPLIT_LATER = {}
