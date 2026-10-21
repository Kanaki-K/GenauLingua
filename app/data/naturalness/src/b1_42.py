"""B1, блок 42: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    6942: (LIST, {"t_ru": "расставлять, выдвигать (кандидата)", "t_uk": "розставляти, висувати (кандидата)",
                  "t_en": "to set up, to nominate", "t_tr": "kurmak, aday göstermek", "t_pl": "ustawiać, wystawiać kandydata",
                  "t_it": "sistemare, candidare", "t_es": "colocar, presentar", "t_fr": "installer, présenter"}),
    6943: ("«Ich presse die Zitrone aus» — это auspressen; " + LIST, {
        "t_ru": "прижимать, давить", "t_uk": "притискати, тиснути", "t_en": "to press, to squeeze", "t_tr": "bastırmak, sıkmak",
        "t_pl": "przyciskać, wyciskać",
        **all_x("Er presst die Hand auf die Wunde", "Он прижимает руку к ране", "Він притискає руку до рани",
                "He presses his hand onto the wound", "Elini yaraya bastırıyor", "Przyciska rękę do rany",
                "Preme la mano sulla ferita", "Aprieta la mano contra la herida", "Il presse la main sur la plaie",
                "Tiskne ruku na ránu")}),
    6944: ("в речи Kater — чаще «похмелье»; убрать пометки (colloq.)/(fam.)", {
        "t_ru": "похмелье, кот", "t_uk": "похмілля, кіт", "t_en": "hangover, tomcat", "t_tr": "akşamdan kalmalık, erkek kedi",
        "t_pl": "kac, kocur", "t_it": "i postumi della sbornia, il gatto", "t_es": "la resaca, el gato",
        "t_fr": "la gueule de bois, le matou", "t_cs": "kocovina, kocour",
        **all_x("Ich habe einen fürchterlichen Kater", "У меня жуткое похмелье", "У мене жахливе похмілля",
                "I've got a terrible hangover", "Feci akşamdan kalmayım", "Mam straszliwego kaca",
                "Ho dei postumi della sbornia terribili", "Tengo una resaca horrible", "J'ai une sacrée gueule de bois",
                "Mám příšernou kocovinu")}),
    10390: ("ru «Мой инстинкт говорит мне» — калька", {"x_ru": "Чутьё мне подсказывает, что что-то не так",
                                                     "x_uk": "Чуття підказує мені, що щось не так",
                                                     "x_en": "My gut feeling tells me something's wrong"}),
    6945: ("«Der Dichter schreibt wunderbare Gedichte» — масло масляное", {**all_x(
        "Goethe ist Deutschlands berühmtester Dichter", "Гёте — самый известный поэт Германии", "Ґете — найвідоміший поет Німеччини",
        "Goethe is Germany's most famous poet", "Goethe, Almanya'nın en ünlü şairi", "Goethe to najsłynniejszy poeta Niemiec",
        "Goethe è il poeta più famoso della Germania", "Goethe es el poeta más famoso de Alemania",
        "Goethe est le poète le plus célèbre d'Allemagne", "Goethe je nejslavnější německý básník")}),
    17933: ("«Die Erfindung des Autos war revolutionär» — учебник", {"t_cs": "vynález, výmysl", **all_x(
        "Das ist eine reine Erfindung!", "Это чистая выдумка!", "Це чиста вигадка!", "That's pure fabrication!",
        "Bu tamamen uydurma!", "To czysty wymysł!", "È un'invenzione bella e buona!", "¡Eso es un invento!",
        "C'est une pure invention!", "To je čistý výmysl!")}),
    6946: ("«Eine Unbekannte rief mich heute an» — претерит", {**all_x(
        "Eine Unbekannte hat nach dir gefragt", "Тебя спрашивала какая-то незнакомка", "Тебе питала якась незнайомка",
        "Some unknown woman was asking about you", "Tanımadık bir kadın seni sordu", "Pytała o ciebie jakaś nieznajoma",
        "Una sconosciuta ha chiesto di te", "Una desconocida ha preguntado por ti",
        "Une inconnue a demandé après toi", "Ptala se po tobě nějaká neznámá")}),
    8833: ("«Der Geschäftsmann hat ein großes Unternehmen» — пусто", {**all_x(
        "Er ist ein knallharter Geschäftsmann", "Он жёсткий бизнесмен", "Він жорсткий бізнесмен", "He's a hard-nosed businessman",
        "Çok sert bir iş adamı", "To bezwzględny biznesmen", "È un uomo d'affari spietato",
        "Es un hombre de negocios implacable", "C'est un homme d'affaires impitoyable", "Je to tvrdý podnikatel")}),
    1599: ("«Schreib einen Kommentar» — кнопка сайта", {**all_x(
        "Spar dir deine Kommentare!", "Оставь свои комментарии при себе!", "Залиш свої коментарі при собі!",
        "Keep your comments to yourself!", "Yorumlarını kendine sakla!", "Zachowaj swoje komentarze dla siebie!",
        "Risparmiati i commenti!", "¡Ahórrate los comentarios!", "Garde tes commentaires pour toi!", "Nech si své komentáře!")}),
    17784: ("ru — порядок слов", {"x_ru": "В этой отрасли очень сильная конкуренция",
                                  "x_en": "There's very strong competition in this industry"}),
    8834: ("пример про Werbeagentur, а не про Agentur", {**all_x(
        "Wir haben die Wohnung über eine Agentur gefunden", "Мы нашли квартиру через агентство",
        "Ми знайшли квартиру через агентство", "We found the flat through an agency",
        "Daireyi bir ajans aracılığıyla bulduk", "Znaleźliśmy mieszkanie przez agencję",
        "Abbiamo trovato l'appartamento tramite un'agenzia", "Encontramos el piso a través de una agencia",
        "On a trouvé l'appartement par une agence", "Byt jsme našli přes agenturu")}),
    2970: (LIST, {"t_ru": "обеспечивать, ухаживать", "t_uk": "забезпечувати, доглядати", "t_en": "to provide, to look after",
                  "t_tr": "sağlamak, bakmak", "t_pl": "zaopatrywać, opiekować się"}),
    15476: ("«Der Hai ist ein großes Meerestier» — учебник", {**all_x(
        "Haie greifen Menschen nur selten an", "Акулы редко нападают на людей", "Акули рідко нападають на людей",
        "Sharks rarely attack people", "Köpek balıkları insanlara nadiren saldırır", "Rekiny rzadko atakują ludzi",
        "Gli squali attaccano raramente le persone", "Los tiburones rara vez atacan a las personas",
        "Les requins attaquent rarement les humains", "Žraloci na lidi útočí jen zřídka")}),
    16090: ("пример про Anwaltskanzlei, а не про Kanzlei; " + LIST, {
        "t_ru": "адвокатская контора, юридическая фирма", "t_en": "law firm, chancellery", "t_tr": "hukuk bürosu, kalem",
        **all_x("Ich habe einen Termin in der Kanzlei", "У меня встреча в адвокатской конторе",
                "У мене зустріч в адвокатській конторі", "I've got an appointment at the law firm",
                "Hukuk bürosunda randevum var", "Mam spotkanie w kancelarii", "Ho un appuntamento allo studio legale",
                "Tengo una cita en el bufete", "J'ai rendez-vous au cabinet", "Mám schůzku v advokátní kanceláři")}),
    16091: ("«Die Ermittlung der Polizei dauerte lange» — претерит", {**all_x(
        "Die Ermittlungen laufen noch", "Расследование ещё идёт", "Розслідування ще триває",
        "The investigation is still ongoing", "Soruşturma hâlâ sürüyor", "Śledztwo wciąż trwa",
        "Le indagini sono ancora in corso", "La investigación sigue en curso", "L'enquête est toujours en cours",
        "Vyšetřování stále probíhá")}),
    1105: (LIST, {"t_en": "to refuse, to turn down"}),
    2311: (EN + " («He does boxing»)", {"x_en": "He goes to boxing training"}),
    15477: ("«Der Sonnenaufgang ist sehr schön» — пусто", {**all_x(
        "Wir sind extra früh aufgestanden, um den Sonnenaufgang zu sehen",
        "Мы специально встали рано, чтобы увидеть восход солнца", "Ми спеціально встали рано, щоб побачити схід сонця",
        "We got up extra early to see the sunrise", "Gündoğumunu görmek için özellikle erken kalktık",
        "Specjalnie wstaliśmy wcześnie, żeby zobaczyć wschód słońca", "Ci siamo alzati presto apposta per vedere l'alba",
        "Nos levantamos muy temprano para ver el amanecer", "On s'est levés exprès tôt pour voir le lever du soleil",
        "Vstali jsme schválně brzy, abychom viděli východ slunce")}),
    12565: ("«Der Sanitäter half dem verletzten Mann» — претерит; " + LIST, {
        "t_ru": "медик скорой, фельдшер", "t_uk": "медик швидкої, фельдшер", "t_en": "paramedic, medic",
        "t_tr": "sağlık görevlisi, paramedik", "t_pl": "ratownik medyczny, sanitariusz",
        **all_x("Die Sanitäter sind in fünf Minuten da", "Медики приедут через пять минут", "Медики приїдуть за п'ять хвилин",
                "The paramedics will be here in five minutes", "Sağlık görevlileri beş dakikaya burada",
                "Ratownicy medyczni będą za pięć minut", "I soccorritori arrivano tra cinque minuti",
                "Los sanitarios llegan en cinco minutos", "Les ambulanciers seront là dans cinq minutes",
                "Záchranáři tu budou za pět minut")}),
    1264: ("«Die Besprechung beginnt um 10 Uhr» — пусто; " + LIST, {"t_pl": "narada, zebranie", **all_x(
        "Ich bin gerade in einer Besprechung, ich rufe zurück", "Я сейчас на совещании, перезвоню", "Я зараз на нараді, передзвоню",
        "I'm in a meeting right now, I'll call you back", "Şu an bir toplantıdayım, seni geri ararım",
        "Jestem teraz na naradzie, oddzwonię", "Sono in riunione, ti richiamo", "Ahora estoy en una reunión, te llamo luego",
        "Je suis en réunion, je te rappelle", "Jsem zrovna na poradě, zavolám ti zpátky")}),
    16092: ("«Der Sklave hatte keine Freiheit» — претерит, учебник истории", {**all_x(
        "Ich bin doch nicht dein Sklave!", "Я тебе не раб!", "Я тобі не раб!", "I'm not your slave!",
        "Ben senin kölen değilim!", "Nie jestem twoim niewolnikiem!", "Non sono mica il tuo schiavo!", "¡No soy tu esclavo!",
        "Je ne suis pas ton esclave!", "Nejsem tvůj otrok!")}),
    417: ("«Sie hat Husten» — пусто", {**all_x(
        "Ich habe seit einer Woche Husten", "У меня уже неделю кашель", "У мене вже тиждень кашель",
        "I've had a cough for a week", "Bir haftadır öksürüğüm var", "Od tygodnia mam kaszel", "Ho la tosse da una settimana",
        "Tengo tos desde hace una semana", "J'ai de la toux depuis une semaine", "Už týden mám kašel")}),
    6952: (LIST, {"t_ru": "отправляться, взламывать", "t_uk": "вирушати, зламувати", "t_en": "to set off, to break open",
                  "t_tr": "yola çıkmak, zorla açmak", "t_pl": "wyruszać, wyłamywać", "t_it": "partire, forzare",
                  "t_es": "partir, forzar", "t_fr": "partir, forcer", "t_cs": "vyrazit, vypáčit"}),
    10392: ("«Das war naiv von dir» — шаблон «… von dir»", {**all_x(
        "Sei doch nicht so naiv!", "Не будь таким наивным!", "Не будь таким наївним!", "Don't be so naive!",
        "Bu kadar saf olma!", "Nie bądź taki naiwny!", "Non essere così ingenuo!", "¡No seas tan ingenuo!",
        "Ne sois pas si naïf!", "Nebuď tak naivní!")}),
    10393: (LIST + "; en «I have a craving» — книжно", {
        "t_ru": "охота, козёл", "t_uk": "охота, козел", "t_en": "craving, billy goat", "t_tr": "istek, teke",
        "t_pl": "ochota, kozioł", "x_en": "I've got a craving for pizza"}),
    10394: ("«Das ist gruselig» — пусто; убрать пометку (fam.)", {"t_fr": "effrayant, flippant", **all_x(
        "Der Keller ist mir zu gruselig", "В подвале мне жутко", "У підвалі мені лячно", "The cellar's too creepy for me",
        "Bodrum bana fazla ürkütücü geliyor", "Piwnica jest dla mnie zbyt upiorna", "La cantina è troppo inquietante per me",
        "El sótano es demasiado espeluznante para mí", "La cave est trop flippante pour moi",
        "Sklep je na mě moc strašidelný")}),
    10395: ("«Ich kann das nicht aushalten» — пусто", {**all_x(
        "Ich halte diese Hitze nicht mehr aus", "Я больше не могу выносить эту жару", "Я більше не можу витримувати цю спеку",
        "I can't stand this heat any more", "Bu sıcağa artık dayanamıyorum", "Nie wytrzymam już tego upału",
        "Non sopporto più questo caldo", "Ya no aguanto este calor", "Je ne supporte plus cette chaleur",
        "Už to vedro nevydržím")}),
    16093: ("«Der Gauner hat das Geld gestohlen» — шаблон stehlen", {**all_x(
        "So ein Gauner, er hat mich übers Ohr gehauen!", "Вот жулик, он меня надул!", "Ото шахрай, він мене ошукав!",
        "What a crook, he ripped me off!", "Ne üçkağıtçı, beni kazıkladı!", "Co za kanciarz, oszukał mnie!",
        "Che furfante, mi ha fregato!", "¡Qué granuja, me ha timado!", "Quel filou, il m'a arnaqué!",
        "To je darebák, natáhl mě!")}),
    16094: ("«Der Polizist hatte einen Revolver …» — претерит", {**all_x(
        "Im Western hat jeder einen Revolver", "В вестернах у каждого есть револьвер", "У вестернах у кожного є револьвер",
        "In westerns everyone has a revolver", "Westernlerde herkesin bir tabancası var", "W westernach każdy ma rewolwer",
        "Nei western tutti hanno un revolver", "En los westerns todo el mundo tiene un revólver",
        "Dans les westerns, tout le monde a un revolver", "Ve westernech má každý revolver")}),
    16095: ("«Der General bekam einen hohen Orden …» — претерит; " + LIST, {
        "t_ru": "орден, медаль", "t_uk": "орден, медаль", "t_en": "medal, order", "t_tr": "madalya, nişan",
        "t_pl": "order, odznaczenie", "t_it": "la medaglia, l'onorificenza", "t_es": "la medalla, la condecoración",
        "t_fr": "la médaille, la décoration", "t_cs": "řád, medaile",
        **all_x("An seiner Jacke hängen viele Orden", "На его пиджаке висит много орденов", "На його піджаку висить багато орденів",
                "Lots of medals hang on his jacket", "Ceketinde bir sürü madalya asılı", "Na jego marynarce wisi wiele odznaczeń",
                "Sulla sua giacca ci sono tante medaglie", "En su chaqueta cuelgan muchas medallas",
                "Il a plein de médailles sur sa veste", "Na saku má spoustu řádů")}),
}

SPLIT_LATER = {
    16095: ["der Orden = монашеский орден (Jesuitenorden)"],
}
