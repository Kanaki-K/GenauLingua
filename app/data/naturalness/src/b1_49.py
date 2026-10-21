"""B1, блок 49: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    190: (LIST + "; «розетка» — это Steckdose", {
        "t_ru": "банка, жестянка", "t_uk": "банка, бляшанка", "t_en": "can, tin", "t_tr": "kutu, teneke kutu",
        "t_pl": "puszka, konserwa", "t_it": "la scatoletta, la lattina", "t_es": "la lata", "t_fr": "la boîte, la canette",
        "t_cs": "konzerva, plechovka"}),
    7029: (LIST, {"t_ru": "огромный, мощный", "t_uk": "величезний, потужний", "t_en": "huge, tremendous",
                  "t_tr": "muazzam, kocaman", "t_pl": "ogromny, potężny"}),
    7030: ("«Es gibt einen Mangel an Lebensmitteln» — хроника", {**all_x(
        "Aus Mangel an Zeit kann ich nicht kommen", "Из-за нехватки времени я не смогу прийти",
        "Через нестачу часу я не зможу прийти", "I can't come for lack of time", "Zaman eksikliğinden gelemem",
        "Z braku czasu nie mogę przyjść", "Per mancanza di tempo non posso venire", "Por falta de tiempo no puedo ir",
        "Par manque de temps, je ne peux pas venir", "Z nedostatku času nemůžu přijít")}),
    10433: ("«Ich verfluchte meinen Mangel an Glück» — претерит, калька", {**all_x(
        "Ich verfluche den Tag, an dem ich ihn getroffen habe", "Я проклинаю тот день, когда его встретила",
        "Я проклинаю той день, коли його зустріла", "I curse the day I met him", "Onunla tanıştığım günü lanetliyorum",
        "Przeklinam dzień, w którym go poznałam", "Maledico il giorno in cui l'ho conosciuto",
        "Maldigo el día en que lo conocí", "Je maudis le jour où je l'ai rencontré", "Proklínám den, kdy jsem ho potkala")}),
    12581: ("«Die Autopsie zeigte …» — претерит", {**all_x(
        "Die Autopsie hat die wahre Ursache gezeigt", "Вскрытие показало истинную причину", "Розтин показав справжню причину",
        "The autopsy revealed the real cause", "Otopsi gerçek nedeni ortaya çıkardı", "Sekcja zwłok wykazała prawdziwą przyczynę",
        "L'autopsia ha rivelato la vera causa", "La autopsia reveló la verdadera causa", "L'autopsie a révélé la vraie cause",
        "Pitva odhalila skutečnou příčinu")}),
    14453: ("«Pop ist eine beliebte Musikrichtung» — учебник", {**all_x(
        "Ich höre am liebsten Pop", "Я больше всего люблю слушать поп", "Я найбільше люблю слухати поп",
        "I like listening to pop best", "En çok pop dinlemeyi seviyorum", "Najbardziej lubię słuchać popu",
        "Preferisco ascoltare il pop", "Lo que más me gusta escuchar es pop", "Ce que je préfère écouter, c'est la pop",
        "Nejradši poslouchám pop")}),
    7031: ("«Das Konzert war überaus gelungen» — шаблон «Das Konzert war …»", {**all_x(
        "Er ist ein überaus begabter Musiker", "Он чрезвычайно талантливый музыкант", "Він надзвичайно талановитий музикант",
        "He's an exceedingly gifted musician", "Son derece yetenekli bir müzisyen", "To niezwykle utalentowany muzyk",
        "È un musicista estremamente dotato", "Es un músico sumamente talentoso", "C'est un musicien extrêmement doué",
        "Je to nesmírně nadaný hudebník")}),
    11703: (EN + " («fries» — американское)", {"x_en": "I'd like a portion of chips with ketchup", "t_en": "chips, fries"}),
    17787: ("«Die Kompanie war sehr erfolgreich» — не тот смысл; " + LIST, {
        "t_ru": "рота", "t_uk": "рота", "t_en": "company (of soldiers)", "t_tr": "bölük", "t_pl": "kompania",
        "t_it": "la compagnia", "t_es": "la compañía", "t_fr": "la compagnie", "t_cs": "rota",
        **all_x("Er dient in der dritten Kompanie", "Он служит в третьей роте", "Він служить у третій роті",
                "He serves in the third company", "Üçüncü bölükte görev yapıyor", "Służy w trzeciej kompanii",
                "Presta servizio nella terza compagnia", "Sirve en la tercera compañía", "Il sert dans la troisième compagnie",
                "Slouží u třetí roty")}),
    10434: ("«Sie ist eine liebende Mutter» — книжно; живое — «liebend gern»", {
        "t_ru": "любящий, с удовольствием", "t_uk": "люблячий, з радістю", "t_en": "loving, gladly",
        "t_tr": "sevgi dolu, büyük bir zevkle", "t_pl": "kochający, z przyjemnością", "t_it": "amorevole, volentieri",
        "t_es": "cariñoso, con gusto", "t_fr": "aimant, volontiers", "t_cs": "milující, rád",
        **all_x("Das mache ich liebend gern", "Я с огромным удовольствием это сделаю", "Я з радістю це зроблю",
                "I'll gladly do that", "Bunu büyük bir zevkle yaparım", "Zrobię to z przyjemnością",
                "Lo faccio molto volentieri", "Lo hago con mucho gusto", "Je le fais très volontiers", "To udělám moc rád")}),
    7032: ("«Die Soldaten marschieren in die Stadt» — война", {**all_x(
        "Wir sind zwei Stunden durch den Wald marschiert", "Мы два часа шагали по лесу", "Ми дві години крокували лісом",
        "We marched through the forest for two hours", "İki saat ormanda yürüdük", "Maszerowaliśmy dwie godziny przez las",
        "Abbiamo marciato due ore nel bosco", "Marchamos dos horas por el bosque", "On a marché deux heures dans la forêt",
        "Dvě hodiny jsme pochodovali lesem")}),
    17788: (LIST, {"t_ru": "производство, съёмки", "t_uk": "виробництво, зйомки", "t_en": "production, output",
                   "t_tr": "üretim, yapım", "t_pl": "produkcja, realizacja filmu"}),
    10435: ("«Ich sah die Verzweiflung in seinen Augen» — претерит", {**all_x(
        "Aus Verzweiflung hat er alles verkauft", "От отчаяния он всё продал", "Від відчаю він усе продав",
        "Out of desperation he sold everything", "Çaresizlikten her şeyi sattı", "Z rozpaczy sprzedał wszystko",
        "Per disperazione ha venduto tutto", "Por desesperación lo vendió todo", "Par désespoir, il a tout vendu",
        "Ze zoufalství všechno prodal")}),
    11704: (LIST, {"t_ru": "смешивать, тасовать", "t_uk": "змішувати, тасувати", "t_en": "to mix, to shuffle",
                   "t_tr": "karıştırmak, iskambil karmak", "t_pl": "mieszać, tasować"}),
    7034: ("«Der Chef erteilte uns eine neue Aufgabe» — претерит; " + LIST + " (было пять значений)", {
        "t_ru": "давать, выдавать", "t_uk": "давати, видавати", "t_en": "to give, to grant", "t_tr": "vermek",
        "t_pl": "udzielać, wydawać",
        **all_x("Wer hat dir die Erlaubnis erteilt?", "Кто дал тебе разрешение?", "Хто дав тобі дозвіл?",
                "Who gave you permission?", "Sana kim izin verdi?", "Kto udzielił ci pozwolenia?",
                "Chi ti ha dato il permesso?", "¿Quién te ha dado permiso?", "Qui t'a donné la permission?",
                "Kdo ti dal svolení?")}),
    10436: ("«Die Fans jubelten, als das Tor fiel» — претерит, шаблон Jubel", {**all_x(
        "Die Kinder jubeln über den ersten Schnee", "Дети ликуют, увидев первый снег", "Діти радіють першому снігу",
        "The kids are cheering at the first snow", "Çocuklar ilk kar için sevinç çığlıkları atıyor",
        "Dzieci radują się z pierwszego śniegu", "I bambini esultano per la prima neve",
        "Los niños celebran la primera nieve", "Les enfants exultent devant la première neige",
        "Děti jásají nad prvním sněhem")}),
    6707: ("«eine mächtige Explosion» — хроника; живое — «mächtig stolz»", {"t_cs": "mocný, velmi", **all_x(
        "Er ist mächtig stolz auf seinen Sohn", "Он очень гордится сыном", "Він дуже пишається сином",
        "He's mighty proud of his son", "Oğluyla çok gurur duyuyor", "Jest ogromnie dumny z syna",
        "È enormemente orgoglioso di suo figlio", "Está enormemente orgulloso de su hijo",
        "Il est énormément fier de son fils", "Je na syna velmi pyšný")}),
    8850: ("«Die Feuerwehr kam schnell zum Einsatz» — претерит, протокол", {**all_x(
        "Ruf die Feuerwehr, es brennt!", "Звони пожарным, пожар!", "Дзвони пожежникам, пожежа!",
        "Call the fire brigade, there's a fire!", "İtfaiyeyi ara, yangın var!", "Dzwoń po straż pożarną, pali się!",
        "Chiama i pompieri, c'è un incendio!", "¡Llama a los bomberos, hay un incendio!", "Appelle les pompiers, il y a le feu!",
        "Zavolej hasiče, hoří!")}),
    17790: ("«Die Waren sind im Lagerhaus» — шаблон Lager («Die Ware ist im Lager»)", {**all_x(
        "Er arbeitet nachts in einem Lagerhaus", "Он работает по ночам на складе", "Він працює вночі на складі",
        "He works nights in a warehouse", "Geceleri bir depoda çalışıyor", "Pracuje nocami w magazynie",
        "Lavora di notte in un magazzino", "Trabaja de noche en un almacén", "Il travaille la nuit dans un entrepôt",
        "V noci pracuje ve skladu")}),
    7039: (LIST + " (было пять значений)", {
        "t_ru": "зависеть, тусоваться", "t_uk": "залежати, тусуватися", "t_en": "to depend, to hang out",
        "t_tr": "bağlı olmak, takılmak", "t_pl": "zależeć, urwać się komuś", "t_it": "dipendere, togliere",
        "t_es": "depender, descolgar", "t_fr": "dépendre, décrocher", "t_cs": "záviset, sundat"}),
    16128: ("«Er saß drei Jahre in Haft» — претерит", {**all_x(
        "Er sitzt seit zwei Jahren in Haft", "Он уже два года в заключении", "Він уже два роки в ув'язненні",
        "He's been in prison for two years", "İki yıldır hapiste", "Od dwóch lat siedzi w areszcie",
        "È in carcere da due anni", "Lleva dos años en la cárcel", "Il est en prison depuis deux ans",
        "Už dva roky sedí ve vězení")}),
    10437: (LIST + "; ru «Напряжение в фильме было отличным» — калька; en «movie»", {
        "t_ru": "напряжение, интрига", "t_uk": "напруга, інтрига", "t_en": "tension, suspense", "t_tr": "gerilim, merak",
        "t_pl": "napięcie, niepewność", "x_ru": "Фильм держал в напряжении до конца",
        "x_en": "The film had great suspense"}),
    8851: (EN + " («janitor» — американское)", {"x_en": "The caretaker looks after the heating in the building",
                                              "t_en": "caretaker, janitor"}),
    1335: ("«Ich brauche dieses Dokument» — пусто", {**all_x(
        "Speicher das Dokument, bevor du den Computer ausmachst", "Сохрани документ, прежде чем выключишь компьютер",
        "Збережи документ, перш ніж вимкнеш комп'ютер", "Save the document before you turn off the computer",
        "Bilgisayarı kapatmadan önce belgeyi kaydet", "Zapisz dokument, zanim wyłączysz komputer",
        "Salva il documento prima di spegnere il computer", "Guarda el documento antes de apagar el ordenador",
        "Enregistre le document avant d'éteindre l'ordinateur", "Ulož dokument, než vypneš počítač")}),
    12175: ("ru «играть вместе с нами» — калька", {"x_ru": "Хочешь поиграть с нами?"}),
    7040: ("«Er starrte auf die Wand» — претерит", {**all_x(
        "Starr mich nicht so an!", "Не смотри на меня так пристально!", "Не витріщайся так на мене!",
        "Stop staring at me like that!", "Bana öyle dik dik bakma!", "Nie gap się tak na mnie!", "Non fissarmi così!",
        "¡No me mires tan fijamente!", "Arrête de me fixer comme ça!", "Nezírej na mě tak!")}),
}

REPLACE = [{"id": 7038, "by": 6576, "lang": "de", "why": "überlass — повелительная форма überlassen"}]

SPLIT_LATER = {}
