"""Вычитка немецкого, порция p034 (B2), 23.10: религия, культура, семья — заглушки → бытовые фразы"""

W = "вычитка немецкого: учебная заглушка → живая бытовая фраза"

def ex(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"example_de": de, "example_ru": ru, "example_uk": uk, "example_en": en, "example_tr": tr,
            "example_pl": pl, "example_it": it, "example_es": es, "example_fr": fr, "example_cs": cs}

FIXES = {
    14392: (W, ex("Auf dem alten Haus liegt angeblich ein Fluch, sagt meine Oma",
        "Бабушка говорит, что на старом доме якобы лежит проклятие", "Бабуся каже, що на старому будинку нібито лежить прокляття",
        "My grandma says there's supposedly a curse on the old house", "Babaanneme göre eski evde güya bir lanet var",
        "Babcia mówi, że na starym domu podobno ciąży klątwa", "Mia nonna dice che sulla vecchia casa c'è una maledizione",
        "Mi abuela dice que sobre la casa vieja pesa una maldición", "Ma grand-mère dit qu'il y a soi-disant une malédiction sur la vieille maison",
        "Babička říká, že na starém domě údajně leží kletba")),
    14467: (W, ex("Meine Großtante war Nonne und hat im Krankenhaus gearbeitet",
        "Моя двоюродная бабушка была монахиней и работала в больнице", "Моя двоюрідна бабуся була черницею й працювала в лікарні",
        "My great-aunt was a nun and worked in a hospital", "Büyük teyzem rahibeydi ve hastanede çalışıyordu",
        "Moja cioteczna babcia była zakonnicą i pracowała w szpitalu", "Mia prozia era suora e lavorava in ospedale",
        "Mi tía abuela era monja y trabajaba en un hospital", "Ma grand-tante était religieuse et travaillait à l'hôpital",
        "Moje prateta byla jeptiška a pracovala v nemocnici")),
    14484: (W, ex("Spaghetti Bolognese sind bei uns ein Klassiker am Sonntag",
        "Спагетти болоньезе — у нас воскресная классика", "Спагеті болоньєзе — у нас недільна класика",
        "Spaghetti Bolognese is a Sunday classic at our house", "Bolonez soslu spagetti bizde pazar klasiği",
        "Spaghetti bolognese to u nas niedzielny klasyk", "Gli spaghetti alla bolognese da noi sono un classico della domenica",
        "Los espaguetis a la boloñesa son un clásico del domingo en casa", "Les spaghettis bolognaise, chez nous, c'est le classique du dimanche",
        "Špagety boloňské jsou u nás nedělní klasika")),
    14494: (W + "; «Ein Christ glaubt an Jesus» — учебник", ex("Meine Nachbarn sind gläubige Christen und gehen jeden Sonntag in die Kirche",
        "Мои соседи — верующие христиане и каждое воскресенье ходят в церковь", "Мої сусіди — віруючі християни й щонеділі ходять до церкви",
        "My neighbours are devout Christians and go to church every Sunday", "Komşularım dindar Hristiyan, her pazar kiliseye gidiyorlar",
        "Moi sąsiedzi są wierzącymi chrześcijanami i co niedzielę chodzą do kościoła", "I miei vicini sono cristiani credenti e vanno in chiesa ogni domenica",
        "Mis vecinos son cristianos creyentes y van a misa todos los domingos", "Mes voisins sont des chrétiens croyants et vont à l'église tous les dimanches",
        "Moji sousedé jsou věřící křesťané a každou neděli chodí do kostela")),
    14497: (W, ex("Der Prediger in der Fußgängerzone ruft jeden Samstag ins Mikrofon",
        "Проповедник на пешеходной улице каждую субботу кричит в микрофон", "Проповідник на пішохідній вулиці щосуботи кричить у мікрофон",
        "The preacher in the high street shouts into a microphone every Saturday", "Yaya bölgesindeki vaiz her cumartesi mikrofona bağırıyor",
        "Kaznodzieja na deptaku co sobotę krzyczy do mikrofonu", "Il predicatore nella zona pedonale ogni sabato grida nel microfono",
        "El predicador de la calle peatonal grita por el micrófono todos los sábados", "Le prédicateur de la rue piétonne crie dans un micro tous les samedis",
        "Kazatel v pěší zóně každou sobotu křičí do mikrofonu")),
    14501: (W, ex("Kurz vor Weihnachten war es im Supermarkt wie bei der Apokalypse",
        "Перед Рождеством в супермаркете был настоящий апокалипсис", "Перед Різдвом у супермаркеті був справжній апокаліпсис",
        "Just before Christmas the supermarket was like the apocalypse", "Noel'den hemen önce süpermarket kıyamet gibiydi",
        "Tuż przed świętami w supermarkecie była istna apokalipsa", "Poco prima di Natale al supermercato sembrava l'apocalisse",
        "Justo antes de Navidad el súper parecía el apocalipsis", "Juste avant Noël, au supermarché, c'était l'apocalypse",
        "Těsně před Vánoci to v supermarketu vypadalo jako apokalypsa")),
    15066: (W + "; «Ihre lesbische Beziehung ist sehr glücklich» — неживо", ex("In der Serie gibt es ein lesbisches Paar mit zwei Kindern",
        "В сериале есть лесбийская пара с двумя детьми", "У серіалі є лесбійська пара з двома дітьми",
        "In the series there's a lesbian couple with two children", "Dizide iki çocuklu lezbiyen bir çift var",
        "W serialu jest lesbijska para z dwójką dzieci", "Nella serie c'è una coppia lesbica con due figli",
        "En la serie hay una pareja lesbiana con dos hijos", "Dans la série, il y a un couple lesbien avec deux enfants",
        "V seriálu je lesbický pár se dvěma dětmi")),
    15073: (W + "; «Partnerschaft sehr erfolgreich» — офис", ex("Nach zwanzig Jahren Partnerschaft wollen die beiden jetzt doch heiraten",
        "После двадцати лет отношений они всё-таки решили пожениться", "Після двадцяти років стосунків вони все-таки вирішили одружитися",
        "After twenty years together the two of them have decided to get married after all", "Yirmi yıllık birliktelikten sonra ikisi sonunda evlenmek istiyor",
        "Po dwudziestu latach związku tych dwoje jednak chce się pobrać", "Dopo vent'anni di convivenza i due adesso vogliono sposarsi",
        "Después de veinte años de pareja ahora sí quieren casarse", "Après vingt ans de vie commune, ils veulent finalement se marier",
        "Po dvaceti letech partnerství se ti dva přece jen chtějí vzít")),
}

REPLACE = []

SPLIT_LATER = {}
