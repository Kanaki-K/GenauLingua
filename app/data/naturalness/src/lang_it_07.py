"""Вычитка итальянского, порция p007 (A2/B1), 23.10: повторы («Qual è il tuo cognome», «C'è un posto libero», «oggi non c'è»), голые фразы, «Müller»"""

T = "вычитка итальянского: "

FIXES = {
    782: (T + "повтор 18752 «dormo fino a tardi»", {"example_it": "Il sabato faccio la spesa per tutta la settimana"}),
    17915: (T + "«Il medico deve visitarmi» — калька", {"example_it": "Il medico mi ha visitato con calma"}),
    18184: (T + "повтор 681 «la stanza»", {"example_it": "Domenica riordiniamo la cantina"}),
    18216: (T + "«Cucino la zuppa in una pentola» — учебниково", {"example_it": "La pentola è troppo piccola per tutta la pasta"}),
    18248: (T + "повтор 6483 «al terzo piano»", {"example_it": "A che piano abiti?"}),
    18660: (T + "«Devo riposarmi» — оборвано", {"example_it": "Dopo pranzo il nonno si riposa un'ora"}),
    18933: (T + "повтор 995 «La mattina lavoro»", {"example_it": "Di mattina lavoriamo, di pomeriggio studiamo"}),
    18967: (T + "повтор «la farmacia»", {"example_it": "Il negozio la domenica è chiuso, dobbiamo aspettare fino a lunedì"}),
    18969: (T + "«i Müller» — не итальянская фамилия", {"example_it": "Conosci i Bianchi? Il loro figlio è in classe con il nostro"}),
    18988: (T + "«a Berlino» — без нужды", {"example_it": "Da quando vivi a Londra, mi manchi tanto"}),
    44: (T + "«Lavora nello studio» — учебниково", {"example_it": "Ho trasformato la camera degli ospiti in uno studio"}),
    85: (T + "«Bevo il caffè da una tazza» — тавтология", {"example_it": "Ai bambini do i bicchieri di plastica"}),
    152: (T + "повтор 8759 «oggi non c'è»", {"example_it": "Il capo mi ha dato il venerdì libero"}),
    231: (T + "«Credo di prendermi» — коряво", {"example_it": "Credo di essermi preso il raffreddore"}),
    241: (T + "повтор 10 «Qual è il … indirizzo?»", {"example_it": "Il vostro appartamento è bellissimo"}),
    333: (T + "«È divorziata» — без ситуации", {"example_it": "I miei genitori sono divorziati da anni"}),
    412: (T + "«Mangio il miele sul pane» — учебниково", {"example_it": "Un cucchiaino di miele nel tè?"}),
    477: (T + "«Pesa due chili» — без ситуации", {"example_it": "Un chilo di mele, per favore"}),
    485: (T + "нет слова карточки «la roba»", {"example_it": "Prendi la tua roba e andiamo"}),
    496: (T + "повтор 8792 «fa il cuoco»", {"example_it": "Il cuoco del ristorante è napoletano"}),
    510: (T + "«È in ospedale» — без ситуации", {"example_it": "Il nonno è in ospedale da una settimana"}),
    579: (T + "«Ho bisogno di farina» — калька", {"example_it": "Per la pizza serve mezzo chilo di farina"}),
    611: (T + "«La luna splende luminosa» — тавтология", {"example_it": "Stanotte c'è la luna piena"}),
    636: (T + "повтор 253 «Qual è il tuo cognome?»", {"example_it": "Il cognome si scrive con due elle"}),
    700: (T + "повтор 717 «C'è un posto libero qui?»", {"example_it": "Il parcheggio sotto casa è sempre pieno"}),
    708: (T + "«Si mette un cerotto» — учебниково", {"example_it": "Mettiti un cerotto sulla vescica"}),
    711: (T + "«Raccoglie funghi» — учебниково", {"example_it": "In autunno andiamo per funghi"}),
    750: (T + "повтор 49 «Il libro è sul…»", {"example_it": "Lo scaffale è pieno di vecchi giornali"}),
}

REPLACE = []

SPLIT_LATER = {}
