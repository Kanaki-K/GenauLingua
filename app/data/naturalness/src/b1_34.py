"""B1, блок 34: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    12548: ("«Meine Leber tut weh» — шаблон «tut weh»", {"t_ru": "печень", "t_tr": "karaciğer", "t_pl": "wątroba", **all_x(
        "Zu viel Alkohol ist schlecht für die Leber", "Много алкоголя вредно для печени", "Забагато алкоголю шкодить печінці",
        "Too much alcohol is bad for your liver", "Fazla alkol karaciğere zararlı", "Za dużo alkoholu szkodzi wątrobie",
        "Troppo alcol fa male al fegato", "Demasiado alcohol es malo para el hígado",
        "Trop d'alcool, c'est mauvais pour le foie", "Moc alkoholu škodí játrům")}),
    18171: ("ru «в большой вилле» — предлог", {"x_ru": "Они живут на большой вилле"}),
    10338: ("«Das Essen schmeckt eklig» — снова Essen; убрать пометки (fam.)/(hovor.); " + LIST, {
        "t_ru": "мерзкий, противный", "t_uk": "гидкий, огидний", "t_en": "gross, disgusting", "t_tr": "iğrenç",
        "t_pl": "obrzydliwy, paskudny", "t_fr": "dégoûtant, dégueulasse", "t_cs": "nechutný, hnusný",
        **all_x("Igitt, ist das eklig!", "Фу, как мерзко!", "Фу, як гидко!", "Ew, that's gross!", "Iyy, ne iğrenç!",
                "Fuj, jakie obrzydliwe!", "Che schifo!", "¡Puaj, qué asqueroso!", "Beurk, c'est dégoûtant!",
                "Fuj, to je nechutné!")}),
    6860: (EN + " («behavior» — американское)", {"x_en": "His behaviour was really odd"}),
    3066: ("«Wir möchten zusammenarbeiten» — пусто", {**all_x(
        "Wir arbeiten seit Jahren gut zusammen", "Мы уже много лет хорошо работаем вместе",
        "Ми вже багато років добре працюємо разом", "We've worked well together for years",
        "Yıllardır iyi bir şekilde birlikte çalışıyoruz", "Od lat dobrze ze sobą współpracujemy",
        "Collaboriamo bene da anni", "Llevamos años trabajando bien juntos",
        "On travaille bien ensemble depuis des années", "Roky spolu dobře spolupracujeme")}),
    10339: ("ru «Ты просто трусливый» — так не говорят", {"x_ru": "Ты просто трус", "x_en": "You're just a coward"}),
    1230: (LIST, {"t_ru": "обслуживать, управлять", "t_uk": "обслуговувати, керувати", "t_en": "to serve, to operate",
                  "t_tr": "hizmet etmek, cihazı kullanmak", "t_pl": "obsługiwać, posługiwać się"}),
    10340: ("«Seine Moral ist sehr gut» — так не говорят; " + LIST, {
        "t_ru": "мораль, боевой дух", "t_uk": "мораль, бойовий дух", "t_en": "moral, morale", "t_tr": "ahlak, moral",
        "t_pl": "moralność, morale",
        **all_x("Und was ist die Moral von der Geschichte?", "И какова мораль этой истории?", "І яка мораль цієї історії?",
                "And what's the moral of the story?", "Peki bu hikâyenin ahlaki dersi ne?", "A jaki jest morał tej historii?",
                "E qual è la morale della storia?", "¿Y cuál es la moraleja de la historia?",
                "Et quelle est la morale de l'histoire?", "A jaká je morálka toho příběhu?")}),
    1508: (LIST, {"t_ru": "ремень, пояс", "t_uk": "ремінь, пасок", "t_en": "belt", "t_tr": "kemer, kuşak", "t_cs": "pásek, opasek"}),
    6863: ("«Die Zeit wird schnell vergehen» — так не говорят; " + LIST, {
        "t_ru": "проходить, пропадать", "t_uk": "минати, зникати", "t_en": "to pass, to fade away",
        "t_tr": "geçmek, kaybolmak", "t_pl": "mijać, przemijać",
        **all_x("Der Schmerz vergeht bald", "Боль скоро пройдёт", "Біль скоро мине", "The pain will soon pass",
                "Ağrı yakında geçer", "Ból wkrótce minie", "Il dolore passerà presto", "El dolor se pasará pronto",
                "La douleur va bientôt passer", "Bolest brzy pomine")}),
    15455: (EN + " («cozy» — американское)", {"x_en": "The atmosphere here is really cosy"}),
    10341: ("ru «Мы должны уважать» — калька", {"x_ru": "Надо уважать его решение", "x_uk": "Треба поважати його рішення",
                                              "x_en": "We have to respect his decision"}),
    1199: (EN, {"x_en": "Pick something out!"}),
    15003: ("«Er ballte die Faust» — претерит", {**all_x(
        "Er hat vor Wut die Faust geballt", "Он сжал кулак от злости", "Він стиснув кулак від злості",
        "He clenched his fist in anger", "Öfkeden yumruğunu sıktı", "Zacisnął pięść ze złości",
        "Ha stretto il pugno dalla rabbia", "Apretó el puño de rabia", "Il a serré le poing de colère",
        "Zaťal pěst vzteky")}),
    10343: ("«Ich bin sehr erleichtert» — пусто", {**all_x(
        "Ich bin so erleichtert, dass alles gut gegangen ist", "Какое облегчение, что всё прошло хорошо",
        "Яке полегшення, що все минуло добре", "I'm so relieved everything went well",
        "Her şey yolunda gittiği için çok rahatladım", "Odczuwam ulgę, że wszystko poszło dobrze",
        "Sono sollevato che sia andato tutto bene", "Estoy aliviado de que todo haya salido bien",
        "Je suis soulagé que tout se soit bien passé", "Mám úlevu, že všechno dobře dopadlo")}),
    2261: (LIST + "; en «I have mastered three languages» — так не говорят", {
        "t_ru": "владеть, сдерживать себя", "t_uk": "володіти, стримувати себе", "t_en": "to master, to control",
        "t_tr": "hakim olmak, kontrol etmek", "t_pl": "opanować, panować nad czymś", "t_it": "padroneggiare, controllare",
        "x_en": "I have a good command of three languages"}),
    16052: ("пример про прилагательное unschuldig, а не про das/der Unschuldige; претерит", {**all_x(
        "Im Krieg sterben immer Unschuldige", "На войне всегда гибнут невинные", "На війні завжди гинуть невинні",
        "Innocent people always die in war", "Savaşta hep masumlar ölür", "Na wojnie zawsze giną niewinni",
        "In guerra muoiono sempre gli innocenti", "En la guerra siempre mueren inocentes",
        "À la guerre, ce sont toujours des innocents qui meurent", "Ve válce vždycky umírají nevinní")}),
    13946: ("«Ein herzliches Dankeschön für deine Hilfe» — шаблон vielmals («Danke vielmals für deine Hilfe»)", {**all_x(
        "Das ist ein kleines Dankeschön für dich", "Это тебе в знак благодарности", "Це тобі на знак подяки",
        "This is a little thank-you for you", "Bu sana küçük bir teşekkür", "To małe podziękowanie dla ciebie",
        "È un piccolo ringraziamento per te", "Es un pequeño agradecimiento para ti", "C'est un petit remerciement pour toi",
        "To je pro tebe malé poděkování")}),
    1724: (LIST, {"t_tr": "yeğen"}),
    16054: ("«Der Herzog lebte in diesem Schloss» — претерит, шаблон Fürst/Graf", {**all_x(
        "Harry ist der Herzog von Sussex", "Гарри — герцог Сассекский", "Гаррі — герцог Сассекський",
        "Harry is the Duke of Sussex", "Harry, Sussex Dükü", "Harry jest księciem Sussex", "Harry è il duca di Sussex",
        "Harry es el duque de Sussex", "Harry est le duc de Sussex", "Harry je vévoda ze Sussexu")}),
    14434: (LIST, {"t_ru": "акт, поступок", "t_uk": "акт, вчинок", "t_en": "act, deed", "t_tr": "eylem, perde",
                   "t_pl": "akt, czyn"}),
    13947: (LIST, {"t_cs": "šum hlasů, hlahol"}),
    10345: ("убрать пометки (fam.)/(hovor.)", {"t_fr": "idiot, débile", "t_cs": "hloupý, pitomý"}),
    12152: ("«Der Reiter fiel vom Pferd» — претерит; " + LIST, {
        "t_ru": "всадник, вкладка", "t_uk": "вершник, вкладка", "t_en": "rider, tab", "t_tr": "binici, sekme",
        "t_pl": "jeździec, zakładka",
        **all_x("Der Reiter ist vom Pferd gefallen", "Всадник упал с лошади", "Вершник упав з коня",
                "The rider fell off the horse", "Binici attan düştü", "Jeździec spadł z konia",
                "Il cavaliere è caduto da cavallo", "El jinete se ha caído del caballo", "Le cavalier est tombé de cheval",
                "Jezdec spadl z koně")}),
    15006: (LIST + " (было шесть значений)", {
        "t_ru": "отношения, соотношение", "t_uk": "стосунки, співвідношення", "t_en": "relationship, ratio",
        "t_tr": "ilişki, oran", "t_pl": "relacja, proporcja", "t_it": "il rapporto, la proporzione",
        "t_fr": "la relation, le rapport"}),
}

REPLACE = [{"id": 18685, "by": 993, "lang": "de", "why": "vorüber — книжный вариант vorbei"}]

SPLIT_LATER = {}
