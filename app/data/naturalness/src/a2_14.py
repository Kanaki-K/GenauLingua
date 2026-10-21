"""A2, блок 14: слова 521–560 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
SKEL = "пример-скелет («X ist dünn/gelb/lila») — так о вещи не говорят"
EN = "английский пример: так не говорят"
COLOR = "цвета: «Die Blume ist gelb/lila», «Das Hemd ist orange» — один шаблон на все; у каждого цвета своя фраза"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    122: (LIST, {"t_ru": "лист", "t_uk": "аркуш, листок", "t_en": "sheet, leaf", "t_tr": "yaprak, kağıt",
                 "t_pl": "kartka, liść", "t_it": "il foglio, la foglia", "t_cs": "list"}),
    1342: (SKEL + "; " + LIST, {
        "t_ru": "тонкий, худой", "t_uk": "тонкий, худий", "t_en": "thin", "t_tr": "ince, zayıf",
        "t_pl": "cienki, chudy", "t_es": "fino, delgado",
        **all_x("Du bist aber dünn geworden!", "Как ты похудел!", "Як ти схуд!", "You've got so thin!",
                "Ne kadar zayıflamışsın!", "Ale schudłeś!", "Come sei dimagrito!", "¡Qué delgado te has quedado!",
                "Tu es devenu tout mince!", "Ty jsi ale zhubnul!")}),
    17926: (LIST, {"t_ru": "развитие, разработка", "t_uk": "розвиток, розробка", "t_en": "development",
                   "t_tr": "gelişim, geliştirme", "t_pl": "rozwój"}),
    2509: ("«Mein Gehalt wurde erhöht» — пассив, так не говорят; " + LIST, {
        "t_ru": "зарплата, оклад", "t_uk": "зарплата, оклад", "t_en": "salary, pay", "t_tr": "maaş",
        "t_pl": "pensja, wypłata",
        **all_x("Das Gehalt kommt immer am Monatsende", "Зарплата всегда приходит в конце месяца",
                "Зарплата завжди приходить наприкінці місяця", "My salary always comes at the end of the month",
                "Maaş hep ay sonunda yatıyor", "Pensja zawsze przychodzi pod koniec miesiąca",
                "Lo stipendio arriva sempre a fine mese", "El sueldo siempre llega a final de mes",
                "Le salaire tombe toujours en fin de mois", "Plat chodí vždycky na konci měsíce")}),
    17515: ("пятый пример про политику; " + LIST, {
        "t_ru": "СМИ, медиа", "t_uk": "ЗМІ, медіа", "t_en": "media", "t_tr": "medya, basın", "t_pl": "media",
        **all_x("Das stand gestern in allen Medien", "Вчера об этом писали все СМИ", "Учора про це писали всі ЗМІ",
                "It was all over the media yesterday", "Dün bütün medyada bu vardı", "Wczoraj pisały o tym wszystkie media",
                "Ieri ne parlavano tutti i media", "Ayer salió en todos los medios", "Hier, c'était dans tous les médias",
                "Včera o tom psala všechna média")}),
    12155: (EN + " («A big competition takes place»); " + LIST, {
        "t_ru": "соревнование, конкурс", "t_uk": "змагання, конкурс", "t_en": "competition, contest",
        "t_tr": "yarışma, rekabet", "t_pl": "konkurs, zawody",
        "x_ru": "На следующей неделе пройдёт большое соревнование", "x_uk": "Наступного тижня відбудеться велике змагання",
        "x_en": "There's a big competition next week"}),
    1029: ("«в мастерской» — о машине говорят «в автосервисе»; " + LIST, {
        "t_ru": "мастерская, автосервис", "t_uk": "майстерня, автосервіс", "t_en": "workshop, garage",
        "t_tr": "tamirhane, atölye", "t_pl": "warsztat",
        "x_ru": "Машина в автосервисе", "x_uk": "Машина в автосервісі", "x_en": "The car's at the garage"}),
    2263: (EN + " («an acquaintance of mine» — книжно)", {"x_en": "She's someone I know"}),
    18178: (EN, {"x_en": "Can you pass me the towel?"}),
    13501: (LIST, {"t_ru": "причём, хотя", "t_uk": "причому, хоча", "t_en": "although, while", "t_tr": "gerçi",
                   "t_pl": "przy czym, choć", "t_it": "anche se", "t_es": "aunque", "t_fr": "même si",
                   "t_cs": "i když, přičemž"}),
    8822: ("шаблон intelligent («Meine Schwester ist sehr …»); " + LIST, {
        "t_ru": "организованный, собранный", "t_uk": "організований", "t_en": "organised", "t_tr": "düzenli, organize",
        "t_pl": "zorganizowany",
        **all_x("Er ist sehr organisiert, er hat für alles einen Plan", "Он очень организованный, у него на всё есть план",
                "Він дуже організований, у нього на все є план", "He's very organised, he has a plan for everything",
                "Çok düzenli biri, her şey için bir planı var", "Jest bardzo zorganizowany, na wszystko ma plan",
                "È molto organizzato, ha un piano per tutto", "Es muy organizado, tiene un plan para todo",
                "Il est très organisé, il a un plan pour tout", "Je velmi organizovaný, má na všechno plán")}),
    10362: (LIST, {"t_ru": "опыт, переживание", "t_uk": "досвід, переживання", "t_en": "experience",
                   "t_tr": "deneyim, tecrübe", "t_pl": "doświadczenie, przeżycie"}),
    343: ("«Mein Bruder spielt …» — шаблон erwachsen, Klavier", {**all_x(
        "Kannst du Gitarre spielen?", "Ты умеешь играть на гитаре?", "Ти вмієш грати на гітарі?",
        "Can you play the guitar?", "Gitar çalabiliyor musun?", "Umiesz grać na gitarze?", "Sai suonare la chitarra?",
        "¿Sabes tocar la guitarra?", "Tu sais jouer de la guitare?", "Umíš hrát na kytaru?")}),
    2548: (LIST, {"t_ru": "часто, нередко", "t_uk": "часто, нерідко", "t_en": "often, frequently", "t_tr": "sık sık",
                  "t_pl": "często"}),
    2157: ("«Er ist sehr aktiv» — пусто", {**all_x(
        "Mein Opa ist mit 80 noch sehr aktiv", "Мой дедушка и в 80 лет очень активный",
        "Мій дідусь і у 80 років дуже активний", "My grandad is still very active at 80",
        "Dedem 80 yaşında hâlâ çok aktif", "Mój dziadek w wieku 80 lat jest wciąż bardzo aktywny",
        "Mio nonno a 80 anni è ancora molto attivo", "Mi abuelo, con 80 años, sigue muy activo",
        "À 80 ans, mon grand-père est encore très actif", "Můj děda je i v osmdesáti pořád velmi aktivní")}),
    630: ("«Sie trägt eine Mütze» — шаблон одежды", {**all_x(
        "Ich habe meine Mütze im Bus vergessen", "Я забыл шапку в автобусе", "Я забув шапку в автобусі",
        "I left my hat on the bus", "Beremi otobüste unuttum", "Zapomniałem czapki w autobusie",
        "Ho dimenticato il berretto sull'autobus", "Me he dejado el gorro en el autobús",
        "J'ai oublié mon bonnet dans le bus", "Zapomněl jsem čepici v autobuse")}),
    13503: (LIST, {"t_ru": "как… так и", "t_uk": "як… так і", "t_en": "both … and", "t_tr": "hem … hem de",
                   "t_pl": "zarówno… jak i", "t_es": "tanto… como", "t_fr": "aussi bien… que", "t_cs": "jak… tak"}),
    6915: ("«Стол зарезервирован» — о ресторане говорят «столик забронирован»; " + LIST, {
        "t_ru": "забронированный, сдержанный", "t_uk": "заброньований, стриманий", "t_en": "reserved, booked",
        "t_tr": "rezerve", "t_pl": "zarezerwowany",
        "x_ru": "Столик в ресторане забронирован", "x_uk": "Столик у ресторані заброньований"}),
    17783: ("«популярен у клиентов» — язык рекламы; " + LIST, {
        "t_ru": "продукт, товар", "t_uk": "продукт, товар", "t_en": "product", "t_tr": "ürün", "t_pl": "produkt, wyrób",
        **all_x("Dieses Produkt gibt es nur online", "Этот товар продаётся только онлайн", "Цей товар продається лише онлайн",
                "This product is only available online", "Bu ürün sadece internette satılıyor",
                "Ten produkt jest dostępny tylko online", "Questo prodotto si trova solo online",
                "Este producto solo se vende por internet", "Ce produit n'existe qu'en ligne",
                "Tenhle výrobek je jen online")}),
    1165: (LIST, {"t_ru": "злить, сердиться", "t_uk": "злити, сердитися", "t_en": "to annoy, to be annoyed",
                  "t_tr": "kızdırmak, kızmak", "t_pl": "złościć, złościć się", "t_it": "far arrabbiare, arrabbiarsi",
                  "t_es": "molestar, enfadarse", "t_fr": "énerver, s'énerver", "t_cs": "zlobit, rozčilovat se"}),
    679: (COLOR, {**all_x(
        "Im Herbst werden die Blätter gelb und orange", "Осенью листья становятся жёлтыми и оранжевыми",
        "Восени листя стає жовтим і помаранчевим", "In autumn the leaves turn yellow and orange",
        "Sonbaharda yapraklar sarı ve turuncu olur", "Jesienią liście robią się żółte i pomarańczowe",
        "In autunno le foglie diventano gialle e arancioni", "En otoño las hojas se vuelven amarillas y naranjas",
        "En automne, les feuilles deviennent jaunes et orange", "Na podzim jsou listy žluté a oranžové")}),
    320: (COLOR, {**all_x(
        "Er hat die gelbe Karte bekommen", "Он получил жёлтую карточку", "Він отримав жовту картку",
        "He got a yellow card", "Sarı kart gördü", "Dostał żółtą kartkę", "Ha preso il cartellino giallo",
        "Le sacaron tarjeta amarilla", "Il a pris un carton jaune", "Dostal žlutou kartu")}),
    555: (COLOR, {**all_x(
        "Sie hat sich die Haare lila gefärbt", "Она покрасила волосы в фиолетовый", "Вона пофарбувала волосся у фіолетовий",
        "She's dyed her hair purple", "Saçını mora boyatmış", "Ufarbowała włosy na fioletowo",
        "Si è tinta i capelli di viola", "Se ha teñido el pelo de morado", "Elle s'est teint les cheveux en violet",
        "Obarvila si vlasy na fialovo")}),
    132: (COLOR + "; «Sein Mantel ist braun»", {**all_x(
        "Ich hätte gern die braunen Schuhe in Größe 40", "Мне, пожалуйста, коричневые туфли сорокового размера",
        "Мені, будь ласка, коричневі туфлі сорокового розміру", "I'd like the brown shoes in size 40, please",
        "Kahverengi ayakkabıların 40 numarasını alabilir miyim?", "Poproszę te brązowe buty w rozmiarze 40",
        "Vorrei le scarpe marroni nel 40", "Quería los zapatos marrones en el 40",
        "Je voudrais les chaussures marron en 40", "Prosím ty hnědé boty ve velikosti 40")}),
    6936: ("«Это крепкий хват» — так не говорят; «Halt dich fest» — пример festhalten; " + LIST, {
        "t_ru": "крепкий, постоянный", "t_uk": "міцний, постійний", "t_en": "firm, permanent", "t_tr": "sıkı, sabit",
        "t_pl": "mocny, stały", "t_it": "saldo, fisso", "t_es": "firme, fijo", "t_fr": "ferme, fixe",
        "t_cs": "pevný, stálý",
        **all_x("Er hat jetzt eine feste Stelle", "У него теперь постоянная работа", "У нього тепер постійна робота",
                "He's got a permanent job now", "Artık sabit bir işi var", "Ma teraz stałą pracę",
                "Adesso ha un lavoro fisso", "Ahora tiene un trabajo fijo", "Il a maintenant un emploi fixe",
                "Má teď stálou práci")}),
    1111: (LIST, {"t_ru": "запирать, завершать", "t_uk": "зачиняти на ключ, завершувати", "t_en": "to lock, to finish",
                  "t_tr": "kilitlemek, bitirmek", "t_pl": "zamykać na klucz, kończyć",
                  "t_it": "chiudere a chiave, concludere", "t_es": "cerrar con llave, terminar",
                  "t_fr": "fermer à clé, terminer", "t_cs": "zamknout, dokončit"}),
    8839: (EN + " («We organize a party»); " + LIST, {
        "t_ru": "организовывать, доставать", "t_uk": "організовувати, діставати", "t_en": "to organise, to get hold of",
        "t_tr": "düzenlemek, ayarlamak", "t_pl": "organizować, załatwiać", "t_it": "organizzare, procurarsi",
        "t_es": "organizar, conseguir", "t_fr": "organiser, se procurer", "t_cs": "organizovat, sehnat",
        "x_ru": "Мы устраиваем вечеринку", "x_en": "We're organising a party"}),
    909: ("«Du schreibst an die Tafel» — неживо; " + LIST, {
        "t_ru": "доска, плитка", "t_uk": "дошка, плитка", "t_en": "board, bar (of chocolate)", "t_tr": "tahta, tablet",
        "t_pl": "tablica, tabliczka", "t_it": "la lavagna, la tavoletta", "t_es": "la pizarra, la tableta",
        "t_fr": "le tableau, la tablette", "t_cs": "tabule, tabulka",
        **all_x("Kannst du das an die Tafel schreiben?", "Можешь написать это на доске?", "Можеш написати це на дошці?",
                "Could you write it on the board?", "Bunu tahtaya yazabilir misin?", "Możesz to napisać na tablicy?",
                "Puoi scriverlo alla lavagna?", "¿Puedes escribirlo en la pizarra?", "Tu peux l'écrire au tableau?",
                "Můžeš to napsat na tabuli?")}),
    17521: ("перевод длиннее и книжнее немецкого", {
        "x_ru": "Не забудь пароль, а то не войдёшь", "x_uk": "Не забудь пароль, бо не зайдеш",
        "x_it": "Non dimenticare la password, sennò non entri", "x_cs": "Nezapomeň heslo, jinak se nepřihlásíš"}),
    2105: ("«Die Wirtschaft wächst» — шаблон Bevölkerung («Die Bevölkerung wächst»); «трактир» — другое значение", {
        "t_ru": "экономика, хозяйство", "t_uk": "економіка, господарство", "t_en": "economy, economics",
        "t_tr": "ekonomi", "t_pl": "gospodarka, ekonomia", "t_it": "l'economia", "t_es": "la economía",
        "t_fr": "l'économie", "t_cs": "ekonomika, hospodářství",
        **all_x("Er studiert Wirtschaft", "Он изучает экономику", "Він вивчає економіку", "He's studying economics",
                "Ekonomi okuyor", "Studiuje ekonomię", "Studia economia", "Estudia economía",
                "Il fait des études d'économie", "Studuje ekonomii")}),
    2285: (LIST + "; «Я жалуюсь менеджеру» — о намерении говорят «пожалуюсь»", {
        "t_ru": "жаловаться", "t_uk": "скаржитися", "t_en": "to complain", "t_tr": "şikâyet etmek",
        "t_pl": "skarżyć się, narzekać", "t_it": "lamentarsi, reclamare", "t_es": "quejarse, reclamar",
        "t_fr": "se plaindre, réclamer", "t_cs": "stěžovat si",
        "x_ru": "Я пожалуюсь менеджеру", "x_uk": "Я поскаржуся менеджеру",
        "x_en": "I'm going to complain to the manager"}),
    18701: ("«Ich wasche meine Hände mit Seife» — так о себе не рассказывают", {**all_x(
        "Wasch dir die Hände mit Seife!", "Помой руки с мылом!", "Помий руки з милом!", "Wash your hands with soap!",
        "Ellerini sabunla yıka!", "Umyj ręce mydłem!", "Lavati le mani col sapone!", "¡Lávate las manos con jabón!",
        "Lave-toi les mains avec du savon!", "Umyj si ruce mýdlem!")}),
    977: (EN + " («the prices of the stores»); " + LIST, {
        "t_ru": "сравнивать", "t_uk": "порівнювати", "t_en": "to compare", "t_tr": "karşılaştırmak",
        "t_pl": "porównywać", "t_it": "confrontare",
        "x_ru": "Мы сравниваем цены в магазинах", "x_en": "We're comparing prices in different shops"}),
    1094: (EN + " («I'll come to you»)", {"x_en": "I'll come and see you the day after tomorrow"}),
    2845: ("снова Konzert — у двадцати слов пример про концерт", {**all_x(
        "Die Party findet bei mir statt", "Вечеринка пройдёт у меня", "Вечірка відбудеться в мене",
        "The party's being held at my place", "Parti bende yapılacak", "Impreza odbędzie się u mnie",
        "La festa si tiene a casa mia", "La fiesta se celebra en mi casa", "La fête a lieu chez moi",
        "Večírek se koná u mě")}),
}

SPLIT_LATER = {
    2105: ["die Wirtschaft = трактир, пивная"],
}
