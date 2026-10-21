"""B1, блок 25: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    8799: (LIST, {"t_ru": "персонал, сотрудники", "t_uk": "персонал, працівники", "t_en": "staff, personnel",
                  "t_tr": "personel, çalışanlar", "t_pl": "personel, pracownicy", "x_en": "The hotel staff are very friendly"}),
    2718: ("«Das ist eine schwierige Phase» — пусто; ru «сложная фаза» — калька; " + LIST, {
        "t_ru": "период, этап", "t_uk": "період, етап", "t_en": "phase, stage", "t_tr": "dönem, aşama",
        "t_pl": "okres, etap",
        **all_x("Er ist gerade in einer schwierigen Phase", "У него сейчас трудный период", "У нього зараз важкий період",
                "He's going through a difficult phase", "Şu an zor bir dönemden geçiyor", "Przechodzi teraz trudny okres",
                "Sta attraversando una fase difficile", "Está pasando por una etapa difícil",
                "Il traverse une période difficile", "Prochází teď těžkým obdobím")}),
    6728: ("«Solche Probleme existieren überall» — газета; " + LIST, {
        "t_ru": "существовать", "t_uk": "існувати", "t_en": "to exist", "t_tr": "var olmak", "t_pl": "istnieć",
        **all_x("Für ihn existiere ich gar nicht", "Для него я вообще не существую", "Для нього я взагалі не існую",
                "As far as he's concerned, I don't exist", "Onun için ben yokum", "Dla niego w ogóle nie istnieję",
                "Per lui io non esisto proprio", "Para él no existo", "Pour lui, je n'existe pas",
                "Pro něj vůbec neexistuju")}),
    6729: ("ru «тайно читала» — книжно; " + LIST, {
        "t_ru": "тайком, втайне", "t_uk": "потайки, таємно", "t_en": "secretly, on the sly", "t_tr": "gizlice, el altından",
        "t_pl": "potajemnie, ukradkiem", "x_ru": "Она тайком читала его сообщения",
        "x_uk": "Вона потайки читала його повідомлення", "x_en": "She's been secretly reading his messages"}),
    16024: ("«Die Räuber teilten ihre Beute auf» — претерит, сказка; " + LIST, {
        "t_ru": "добыча, награбленное", "t_uk": "здобич, награбоване", "t_en": "prey, loot", "t_tr": "av, ganimet",
        "t_pl": "zdobycz, łup",
        **all_x("Die Katze bringt ihre Beute nach Hause", "Кошка приносит добычу домой", "Кішка приносить здобич додому",
                "The cat brings its prey home", "Kedi avını eve getiriyor", "Kot przynosi zdobycz do domu",
                "Il gatto porta a casa la preda", "La gata trae su presa a casa", "Le chat ramène sa proie à la maison",
                "Kočka nosí kořist domů")}),
    12134: ("«Das war ein perfekter Treffer» — пусто; " + LIST, {
        "t_ru": "попадание, гол", "t_uk": "влучання, гол", "t_en": "hit, goal", "t_tr": "isabet, gol",
        "t_pl": "trafienie, gol", "t_it": "il colpo, il gol", "t_es": "el acierto, el gol",
        **all_x("Noch ein Treffer, und wir gewinnen!", "Ещё один гол — и мы победим!", "Ще один гол — і ми переможемо!",
                "One more goal and we win!", "Bir gol daha, kazanırız!", "Jeszcze jeden gol i wygrywamy!",
                "Ancora un gol e vinciamo!", "¡Un gol más y ganamos!", "Encore un but et on gagne!",
                "Ještě jeden gól a vyhrajeme!")}),
    2144: (LIST, {
        "t_ru": "похудеть, снимать", "t_uk": "схуднути, знімати", "t_en": "to lose weight, to take off",
        "t_tr": "kilo vermek, çıkarmak", "t_pl": "schudnąć, zdejmować", "t_it": "dimagrire, togliere",
        "t_es": "adelgazar, quitar", "t_fr": "maigrir, enlever", "t_cs": "zhubnout, sundat"}),
    18153: (LIST, {
        "t_ru": "накрывать, покрывать", "t_uk": "накривати, покривати", "t_en": "to set (the table), to cover",
        "t_tr": "masayı kurmak, örtmek", "t_pl": "nakrywać, pokrywać"}),
    13927: (LIST, {
        "t_ru": "договорить, отговорить", "t_uk": "договорити, відмовити", "t_en": "to finish speaking, to talk out of",
        "t_tr": "sözünü bitirmek, vazgeçirmek", "t_pl": "dokończyć mówić, wyperswadować",
        "x_en": "Please let me finish"}),
    8800: ("«Die Sekretärin schreibt die Termine auf» — пусто; en «female secretary» — лишнее", {
        "t_en": "secretary", "t_tr": "sekreter",
        **all_x("Rufen Sie bitte meine Sekretärin an", "Позвоните, пожалуйста, моей секретарше",
                "Зателефонуйте, будь ласка, моїй секретарці", "Please call my secretary", "Lütfen sekreterimi arayın",
                "Proszę zadzwonić do mojej sekretarki", "Chiami la mia segretaria, per favore",
                "Llame a mi secretaria, por favor", "Appelez ma secrétaire, s'il vous plaît",
                "Zavolejte prosím mé sekretářce")}),
    2663: ("ru «Доставка придёт» — так не говорят", {"x_ru": "Доставка будет завтра",
                                                    "x_en": "The delivery's coming tomorrow"}),
    2416: ("«Wir entwickeln neue Ideen» — пусто; " + LIST, {
        "t_ru": "разрабатывать, развивать", "t_uk": "розробляти, розвивати", "t_en": "to develop, to design",
        "t_tr": "geliştirmek, tasarlamak", "t_pl": "opracowywać, rozwijać",
        **all_x("Die Firma entwickelt Apps für Kinder", "Фирма разрабатывает приложения для детей",
                "Фірма розробляє застосунки для дітей", "The company develops apps for kids",
                "Şirket çocuklar için uygulama geliştiriyor", "Firma opracowuje aplikacje dla dzieci",
                "L'azienda sviluppa app per bambini", "La empresa desarrolla aplicaciones para niños",
                "L'entreprise développe des applis pour enfants", "Firma vyvíjí aplikace pro děti")}),
    6733: ("снова Projekt; ru «вовлечён» — калька", {
        "t_ru": "причастный, участвующий", "t_uk": "причетний, залучений", "t_en": "involved", "t_tr": "karışmış, katılan",
        "t_pl": "zamieszany, biorący udział", "t_it": "coinvolto", "t_es": "implicado", "t_fr": "impliqué",
        "t_cs": "zapojený, zúčastněný",
        **all_x("Er war an dem Streit nicht beteiligt", "Он не был причастен к ссоре", "Він не був причетний до сварки",
                "He wasn't involved in the argument", "Kavgaya karışmadı", "Nie był zamieszany w kłótnię",
                "Non era coinvolto nella lite", "No estaba implicado en la pelea", "Il n'était pas impliqué dans la dispute",
                "Do hádky nebyl zapojený")}),
    2937: ("«Ich bin verärgert» — пусто; " + LIST, {
        "t_ru": "сердитый, раздражённый", "t_uk": "сердитий, роздратований", "t_en": "annoyed, cross",
        "t_tr": "kızgın, sinirli", "t_pl": "zły, zirytowany", "t_it": "arrabbiato, seccato", "t_es": "enfadado, molesto",
        "t_fr": "fâché, agacé",
        **all_x("Sie ist verärgert, weil ich zu spät gekommen bin", "Она сердита, потому что я опоздал",
                "Вона сердита, бо я запізнився", "She's annoyed because I was late", "Geç kaldığım için bana kızgın",
                "Jest zła, bo się spóźniłem", "È arrabbiata perché sono arrivato tardi",
                "Está enfadada porque llegué tarde", "Elle est fâchée parce que je suis arrivé en retard",
                "Je naštvaná, protože jsem přišel pozdě")}),
    6734: (LIST, {
        "t_ru": "аккуратный, как следует", "t_uk": "акуратний, як слід", "t_en": "tidy, properly",
        "t_tr": "düzenli, adamakıllı", "t_pl": "porządny, jak należy", "t_fr": "rangé, correct"}),
    18154: ("«Wir sitzen auf der Couch» — пусто", {"t_ru": "диван", "t_uk": "диван", "t_tr": "kanepe", **all_x(
        "Du kannst heute auf der Couch schlafen", "Сегодня можешь поспать на диване", "Сьогодні можеш поспати на дивані",
        "You can sleep on the couch tonight", "Bu gece kanepede yatabilirsin", "Dziś możesz spać na kanapie",
        "Stanotte puoi dormire sul divano", "Esta noche puedes dormir en el sofá", "Ce soir, tu peux dormir sur le canapé",
        "Dneska můžeš spát na gauči")}),
    6735: (LIST + "; en «trash» — американское", {
        "t_ru": "опорожнять, выносить", "t_uk": "спорожняти, виносити", "t_pl": "opróżniać, wynosić",
        "x_en": "Can you empty the bin, please?"}),
    12135: ("«Das amüsiert mich sehr» — пусто; " + LIST, {
        "t_ru": "забавлять, веселиться", "t_uk": "розважати, веселитися", "t_en": "to amuse, to have fun",
        "t_tr": "eğlendirmek, eğlenmek", "t_pl": "bawić, bawić się", "t_cs": "bavit, bavit se",
        **all_x("Amüsiert euch gut!", "Веселитесь как следует!", "Веселіться як слід!", "Have fun!",
                "İyi eğlenceler!", "Bawcie się dobrze!", "Divertitevi!", "¡Divertíos!", "Amusez-vous bien!",
                "Bavte se dobře!")}),
    10285: (LIST, {
        "t_ru": "мотив, причина", "t_uk": "мотив, причина", "t_en": "motive, motif", "t_tr": "neden, motif",
        "t_pl": "motyw, powód", "x_ru": "Какой у тебя был мотив?",
        "x_uk": "Який у тебе був мотив?", "x_en": "What was your motive?"}),
    14986: ("«Wir sind miteinander verlobt» — так не говорят", {"t_en": "engaged", **all_x(
        "Seit wann seid ihr verlobt?", "Давно вы помолвлены?", "Відколи ви заручені?", "How long have you been engaged?",
        "Ne zamandan beri nişanlısınız?", "Od kiedy jesteście zaręczeni?", "Da quando siete fidanzati?",
        "¿Desde cuándo estáis prometidos?", "Vous êtes fiancés depuis quand?", "Odkdy jste zasnoubení?")}),
    10288: ("«Das war sehr unangenehm» — пусто; " + LIST, {
        "t_ru": "неприятный, неловкий", "t_uk": "неприємний, незручний", "t_en": "unpleasant, awkward",
        "t_tr": "tatsız, rahatsız edici", "t_pl": "nieprzyjemny, krępujący", "t_it": "spiacevole, imbarazzante",
        **all_x("Das ist mir echt unangenehm", "Мне правда неловко", "Мені справді незручно",
                "This is really awkward for me", "Bu benim için gerçekten tatsız", "To dla mnie naprawdę krępujące",
                "Per me è davvero imbarazzante", "Me resulta muy incómodo", "C'est vraiment gênant pour moi",
                "Je mi to fakt nepříjemné")}),
    6737: (LIST + "; ru «Мы должны» — калька", {
        "t_ru": "принимать (решение), рубить", "t_uk": "ухвалювати (рішення), рубати", "t_en": "to make (a decision), to fell",
        "t_tr": "(karar) vermek, (ağaç) kesmek", "t_pl": "podejmować (decyzję), ścinać",
        "x_ru": "Нам нужно принять решение", "x_uk": "Нам треба ухвалити рішення"}),
    720: ("«Das ist positiv» — пусто", {
        "t_ru": "положительный, позитивный", **all_x(
            "Der Test ist positiv", "Тест положительный", "Тест позитивний", "The test is positive", "Test pozitif",
            "Test jest pozytywny", "Il test è positivo", "La prueba ha dado positivo", "Le test est positif",
            "Test je pozitivní")}),
    6738: ("ru «не оказывает действия» — канцелярит; " + LIST, {
        "t_ru": "действие, эффект", "t_uk": "дія, ефект", "t_en": "effect, impact", "t_tr": "etki, tesir",
        "t_pl": "działanie, skutek",
        **all_x("Das Medikament hat kaum Wirkung", "Лекарство почти не действует", "Ліки майже не діють",
                "The medicine hardly has any effect", "İlacın neredeyse hiç etkisi yok", "Lek prawie nie działa",
                "La medicina non fa quasi effetto", "La medicina casi no hace efecto",
                "Le médicament ne fait presque pas d'effet", "Lék nemá skoro žádný účinek")}),
    6739: ("«Der Anblick war schrecklich» — пусто", {**all_x(
        "Was für ein schöner Anblick!", "Какое красивое зрелище!", "Яке гарне видовище!", "What a lovely sight!",
        "Ne güzel bir manzara!", "Co za piękny widok!", "Che bello spettacolo!", "¡Qué vista tan bonita!",
        "Quel beau spectacle!", "To je krásný pohled!")}),
    6740: ("«Er kam mir entgegen» — претерит", {**all_x(
        "Ich komme dir entgegen", "Я выйду тебе навстречу", "Я вийду тобі назустріч", "I'll come out to meet you",
        "Sana doğru geliyorum", "Wyjdę ci naprzeciw", "Ti vengo incontro", "Salgo a tu encuentro",
        "Je viens à ta rencontre", "Půjdu ti naproti")}),
    12530: ("«Die Rettung kam rechtzeitig» — книжно; " + LIST, {
        "t_ru": "спасение", "t_uk": "порятунок, рятування", "t_en": "rescue", "t_tr": "kurtarma, kurtuluş",
        "t_pl": "ratunek, ratowanie", "t_it": "il salvataggio, il soccorso", "t_fr": "le sauvetage, les secours",
        **all_x("Die Rettung hat zwei Stunden gedauert", "Спасательная операция заняла два часа",
                "Рятувальна операція тривала дві години", "The rescue took two hours", "Kurtarma iki saat sürdü",
                "Akcja ratunkowa trwała dwie godziny", "Il salvataggio è durato due ore", "El rescate duró dos horas",
                "Le sauvetage a duré deux heures", "Záchrana trvala dvě hodiny")}),
    15439: ("«Der Blitz war sehr hell» — пусто; " + LIST, {
        "t_ru": "молния, вспышка", "t_uk": "блискавка, спалах", "t_en": "lightning, flash", "t_tr": "şimşek, flaş",
        "t_pl": "błyskawica, flesz", "t_it": "il fulmine, il flash", "t_es": "el rayo, el flash",
        "t_fr": "l'éclair, le flash",
        **all_x("Mach das Foto bitte ohne Blitz", "Сфотографируй, пожалуйста, без вспышки",
                "Сфотографуй, будь ласка, без спалаху", "Take the photo without flash, please",
                "Fotoğrafı flaşsız çek lütfen", "Zrób zdjęcie bez flesza", "Fai la foto senza flash, per favore",
                "Haz la foto sin flash, por favor", "Prends la photo sans flash, s'il te plaît",
                "Vyfoť to prosím bez blesku")}),
    10291: ("«Das war ein echter Albtraum» — пусто", {**all_x(
        "Ich hatte heute Nacht einen Albtraum", "Мне сегодня ночью приснился кошмар", "Мені сьогодні вночі наснився кошмар",
        "I had a nightmare last night", "Bu gece kabus gördüm", "Miałem dziś w nocy koszmar", "Stanotte ho fatto un incubo",
        "Anoche tuve una pesadilla", "J'ai fait un cauchemar cette nuit", "V noci se mi zdála noční můra")}),
}

SPLIT_LATER = {
    2144: ["abnehmen = брать трубку (Nimm doch ab!)"],
    13927: ["jemandem etwas ausreden = отговорить"],
    6737: ["ein Urteil fällen = выносить приговор"],
}
