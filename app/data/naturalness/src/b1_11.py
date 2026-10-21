"""B1, блок 11: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    6521: ("«Der Fisch ist noch lebendig» — пусто", {**all_x(
        "Die Stadt ist abends sehr lebendig", "Вечером город очень оживлённый", "Увечері місто дуже пожвавлене",
        "The city is very lively in the evenings", "Şehir akşamları çok canlı", "Wieczorem miasto jest bardzo ożywione",
        "La sera la città è molto vivace", "Por la noche la ciudad está muy animada", "Le soir, la ville est très animée",
        "Večer je město plné života")}),
    2905: ("«Ich überzeuge dich» — так не говорят", {**all_x(
        "Du hast mich überzeugt", "Ты меня убедил", "Ти мене переконав", "You've convinced me", "Beni ikna ettin",
        "Przekonałeś mnie", "Mi hai convinto", "Me has convencido", "Tu m'as convaincu", "Přesvědčil jsi mě")}),
    10173: ("«Это не было моим намерением» — калька", {"x_ru": "У меня не было такого намерения",
                                                   "x_uk": "У мене не було такого наміру"}),
    6527: ("«Ich bin komplett müde» — так не говорят", {**all_x(
        "Die Wohnung ist komplett möbliert", "Квартира полностью меблирована", "Квартира повністю мебльована",
        "The flat is completely furnished", "Daire tamamen eşyalı", "Mieszkanie jest kompletnie umeblowane",
        "L'appartamento è completamente arredato", "El piso está completamente amueblado",
        "L'appartement est complètement meublé", "Byt je kompletně zařízený")}),
    2298: ("«Ich mache das ganz bewusst» — книжно; в речи — «Das war mir nicht bewusst»", {**all_x(
        "Das war mir nicht bewusst", "Я этого не осознавал", "Я цього не усвідомлював", "I wasn't aware of that",
        "Bunun farkında değildim", "Nie byłem tego świadomy", "Non ne ero consapevole", "No era consciente de eso",
        "Je n'en étais pas conscient", "Nebyl jsem si toho vědom")}),
    6530: (EN + " («come in briefly»)", {"x_en": "Can I come in for a moment?"}),
    14385: ("«beginnt um acht» — шаблон Konzert, anfangen", {**all_x(
        "Ich habe keine Vorstellung, wie das geht", "Я не имею представления, как это делается",
        "Я не маю уявлення, як це робиться", "I have no idea how that works",
        "Bunun nasıl yapıldığına dair hiçbir fikrim yok", "Nie mam wyobrażenia, jak to działa",
        "Non ho idea di come si faccia", "No tengo ni idea de cómo se hace",
        "Je n'ai aucune idée de comment ça marche", "Nemám představu, jak to funguje")}),
    10177: ("«Я чувствую себя сегодня одиноко» — калька", {"x_ru": "Сегодня мне одиноко", "x_uk": "Сьогодні мені самотньо"}),
    17069: ("«Der Bus hält an der Kirche an» — пусто", {**all_x(
        "Halt mal kurz an, mir ist schlecht", "Останови на минутку, мне плохо", "Зупинись на хвилинку, мені погано",
        "Pull over for a moment, I feel sick", "Bir dakika dur, midem bulanıyor", "Zatrzymaj się na chwilę, niedobrze mi",
        "Fermati un attimo, mi sento male", "Para un momento, que me encuentro mal",
        "Arrête-toi un instant, je ne me sens pas bien", "Zastav na chvilku, je mi špatně")}),
    6531: ("«Du musst den Ball stoppen» — пусто", {**all_x(
        "Die Polizei hat uns gestoppt", "Нас остановила полиция", "Нас зупинила поліція", "The police stopped us",
        "Polis bizi durdurdu", "Zatrzymała nas policja", "La polizia ci ha fermati", "La policía nos paró",
        "La police nous a arrêtés", "Zastavila nás policie")}),
    12492: ("перевод — список из шести; «Mückenstich» прячет слово", {
        "t_ru": "укус (насекомого), укол", "t_uk": "укус, укол", "t_en": "sting, bite", "t_tr": "sokma",
        "t_pl": "ukłucie, użądlenie", "t_it": "la puntura", "t_es": "la picadura", "t_fr": "la piqûre",
        "t_cs": "štípnutí, bodnutí",
        **all_x("Der Stich juckt total", "Укус ужасно чешется", "Укус страшенно свербить", "The bite is really itchy",
                "Sokulan yer çok kaşınıyor", "To ukłucie strasznie swędzi", "La puntura prude tantissimo",
                "La picadura me pica muchísimo", "La piqûre me démange énormément", "To štípnutí strašně svědí")}),
    2646: ("«Das Flugzeug landet» — пусто", {**all_x(
        "Wir landen in zehn Minuten in Wien", "Через десять минут мы приземлимся в Вене",
        "За десять хвилин ми приземлимося у Відні", "We'll be landing in Vienna in ten minutes",
        "On dakika içinde Viyana'ya iniyoruz", "Za dziesięć minut lądujemy w Wiedniu",
        "Tra dieci minuti atterriamo a Vienna", "Aterrizamos en Viena dentro de diez minutos",
        "Nous atterrissons à Vienne dans dix minutes", "Za deset minut přistáváme ve Vídni")}),
    10186: ("en «excited before the exam» — смысл другой (нервничаю)", {"x_en": "I'm really nervous before the exam"}),
    6536: (EN + " («I almost came late»)", {"x_en": "I was almost late"}),
    12494: ("«Ich studiere Medizin» — шаблон intelligent («… studiert Medizin»)", {**all_x(
        "Hast du deine Medizin schon genommen?", "Ты уже принял лекарство?", "Ти вже прийняв ліки?",
        "Have you taken your medicine yet?", "İlacını aldın mı?", "Wziąłeś już lekarstwo?", "Hai già preso la medicina?",
        "¿Ya te has tomado la medicina?", "Tu as déjà pris ton médicament?", "Vzal sis už lék?")}),
    6538: ("Alarm — не будильник (Wecker); «будильник» в переводе вводит в заблуждение", {
        "t_ru": "сигнализация, тревога", "t_uk": "сигналізація, тривога", "t_en": "alarm", "t_tr": "alarm",
        "t_pl": "alarm", "t_it": "l'allarme", "t_es": "la alarma", "t_fr": "l'alarme", "t_cs": "alarm, poplach",
        **all_x("Der Alarm ging mitten in der Nacht los", "Сигнализация сработала посреди ночи",
                "Сигналізація спрацювала посеред ночі", "The alarm went off in the middle of the night",
                "Alarm gecenin ortasında çaldı", "Alarm włączył się w środku nocy",
                "L'allarme è scattato nel cuore della notte", "La alarma saltó en mitad de la noche",
                "L'alarme s'est déclenchée en pleine nuit", "Alarm se spustil uprostřed noci")}),
    6542: ("«Er kommt möglicherweise zu spät» — шаблон vermutlich", {**all_x(
        "Möglicherweise regnet es morgen", "Возможно, завтра будет дождь", "Можливо, завтра буде дощ",
        "Possibly it'll rain tomorrow", "Muhtemelen yarın yağmur yağacak", "Możliwe, że jutro będzie padać",
        "Forse domani piove", "Posiblemente llueva mañana", "Il va peut-être pleuvoir demain",
        "Možná zítra bude pršet")}),
}

SPLIT_LATER = {}
