"""B1, блок 22: следующие 40 по частоте. Вычитано вручную 21.10."""

EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    10262: ("«Das ist total bescheuert» — шаблон lächerlich («Das ist total lächerlich»)", {**all_x(
        "Ich finde die Idee bescheuert", "По-моему, идея дурацкая", "Як на мене, ідея дурна", "I think the idea is stupid",
        "Bence bu fikir saçma", "Moim zdaniem ten pomysł jest głupi", "Secondo me l'idea è stupida",
        "La idea me parece estúpida", "Je trouve l'idée stupide", "Ten nápad mi přijde hloupý")}),
    15435: ("«Der Vogel ist im Käfig» — пусто", {**all_x(
        "Mach bitte den Käfig zu, sonst fliegt der Vogel weg", "Закрой, пожалуйста, клетку, а то птица улетит",
        "Зачини, будь ласка, клітку, бо пташка вилетить", "Close the cage, please, or the bird will fly away",
        "Kafesi kapat lütfen, yoksa kuş uçar", "Zamknij, proszę, klatkę, bo ptak wyleci",
        "Chiudi la gabbia, per favore, sennò l'uccellino scappa",
        "Cierra la jaula, por favor, que si no se escapa el pájaro",
        "Ferme la cage, s'il te plaît, sinon l'oiseau va s'envoler", "Zavři prosím klec, jinak pták uletí")}),
    12129: ("«Der Teddy liegt auf dem Bett» — пусто", {**all_x(
        "Ohne seinen Teddy schläft er nicht ein", "Без своего мишки он не засыпает", "Без свого ведмедика він не засинає",
        "He can't get to sleep without his teddy", "Oyuncak ayısı olmadan uyuyamıyor", "Bez swojego misia nie zaśnie",
        "Senza il suo orsacchiotto non si addormenta", "Sin su osito no se duerme", "Sans son nounours, il ne s'endort pas",
        "Bez svého medvídka neusne")}),
    8790: ("«Die Organisation ist sehr gut» — пусто", {**all_x(
        "Er arbeitet für eine internationale Organisation", "Он работает в международной организации",
        "Він працює в міжнародній організації", "He works for an international organisation",
        "Uluslararası bir kuruluşta çalışıyor", "Pracuje dla międzynarodowej organizacji",
        "Lavora per un'organizzazione internazionale", "Trabaja para una organización internacional",
        "Il travaille pour une organisation internationale", "Pracuje pro mezinárodní organizaci")}),
    6688: ("«Das ist ganz gewöhnlich» — пусто", {**all_x(
        "Gewöhnlich stehe ich um sieben auf", "Обычно я встаю в семь", "Зазвичай я встаю о сьомій",
        "I usually get up at seven", "Genellikle yedide kalkarım", "Zwykle wstaję o siódmej",
        "Di solito mi alzo alle sette", "Normalmente me levanto a las siete", "D'habitude, je me lève à sept heures",
        "Obvykle vstávám v sedm")}),
    760: ("снова «о политике»", {**all_x(
        "Vor dem Haus warten Reporter", "Перед домом ждут репортёры", "Перед будинком чекають репортери",
        "Reporters are waiting outside the house", "Evin önünde muhabirler bekliyor", "Przed domem czekają reporterzy",
        "Davanti alla casa aspettano i reporter", "Delante de la casa esperan los reporteros",
        "Des reporters attendent devant la maison", "Před domem čekají reportéři")}),
    16015: ("«Unsere Nation ist stark» — лозунг", {**all_x(
        "Fußball verbindet die Nation", "Футбол объединяет нацию", "Футбол об'єднує націю",
        "Football brings the nation together", "Futbol milleti birleştiriyor", "Piłka nożna łączy naród",
        "Il calcio unisce la nazione", "El fútbol une a la nación", "Le foot unit la nation", "Fotbal spojuje národ")}),
    17497: ("«Die Technik ist super» — пусто", {**all_x(
        "Mit Technik kenne ich mich nicht aus", "Я не разбираюсь в технике", "Я не розуміюся на техніці",
        "I'm no good with technology", "Teknolojiden anlamam", "Nie znam się na technice",
        "Non me ne intendo di tecnologia", "No entiendo de tecnología", "Je ne m'y connais pas en technologie",
        "Technice nerozumím")}),
    9453: ("«Ich gehe an die Uni» — шаблон Universität", {**all_x(
        "Wir kennen uns von der Uni", "Мы знакомы по универу", "Ми знайомі з універу", "We know each other from uni",
        "Üniversiteden tanışıyoruz", "Znamy się z uczelni", "Ci conosciamo dall'università", "Nos conocemos de la uni",
        "On se connaît de la fac", "Známe se z vysoké školy")}),
    14407: ("«Die Bibel ist alt» — пусто", {**all_x(
        "In der Bibel steht viel über Liebe", "В Библии много написано о любви", "У Біблії багато написано про любов",
        "There's a lot in the Bible about love", "Kutsal Kitap'ta sevgi hakkında çok şey yazıyor",
        "W Biblii dużo jest o miłości", "Nella Bibbia si parla molto dell'amore", "En la Biblia se habla mucho del amor",
        "La Bible parle beaucoup d'amour", "V Bibli se hodně mluví o lásce")}),
    9744: ("«Das Geld ist im Safe» — пусто", {**all_x(
        "Leg deinen Pass in den Safe", "Положи паспорт в сейф", "Поклади паспорт у сейф", "Put your passport in the safe",
        "Pasaportunu kasaya koy", "Włóż paszport do sejfu", "Metti il passaporto in cassaforte",
        "Mete el pasaporte en la caja fuerte", "Mets ton passeport dans le coffre-fort", "Dej si pas do sejfu")}),
    2898: (EN + " («You are surprising me»)", {"x_en": "You surprise me"}),
    18665: ("«Ich habe ihn kürzlich getroffen» — шаблон neulich («… einen alten Freund getroffen»)", {**all_x(
        "Sie hat kürzlich geheiratet", "Она недавно вышла замуж", "Вона нещодавно вийшла заміж",
        "She got married recently", "Kısa süre önce evlendi", "Niedawno wyszła za mąż", "Si è sposata di recente",
        "Se casó hace poco", "Elle s'est mariée récemment", "Nedávno se vdala")}),
    10267: ("«Das ist meine große Schwäche» — шаблон Stärke («Das ist meine größte Stärke»)", {**all_x(
        "Ich habe eine Schwäche für Schokolade", "У меня слабость к шоколаду", "У мене слабкість до шоколаду",
        "I have a weakness for chocolate", "Çikolataya karşı zaafım var", "Mam słabość do czekolady",
        "Ho un debole per il cioccolato", "Tengo debilidad por el chocolate", "J'ai un faible pour le chocolat",
        "Mám slabost pro čokoládu")}),
    2190: ("снова Film; " + EN, {**all_x(
        "Schau mich an, wenn ich mit dir rede!", "Посмотри на меня, когда я с тобой разговариваю!",
        "Подивись на мене, коли я з тобою розмовляю!", "Look at me when I'm talking to you!",
        "Seninle konuşurken bana bak!", "Patrz na mnie, kiedy do ciebie mówię!", "Guardami quando ti parlo!",
        "¡Mírame cuando te hablo!", "Regarde-moi quand je te parle!", "Dívej se na mě, když s tebou mluvím!")}),
}

SPLIT_LATER = {}
