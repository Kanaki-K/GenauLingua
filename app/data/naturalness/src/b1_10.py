"""B1, блок 10: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    611: (LIST, {"t_ru": "луна", "t_uk": "місяць", "t_tr": "ay"}),
    6495: (LIST, {"t_ru": "действовать, торговаться", "t_uk": "діяти, торгуватися", "t_en": "to act, to haggle",
                  "t_tr": "hareket etmek, pazarlık yapmak", "t_pl": "działać, targować się", "t_it": "agire, contrattare",
                  "t_es": "actuar, regatear", "t_fr": "agir, marchander", "t_cs": "jednat, smlouvat"}),
    11648: (LIST, {"t_ru": "сытый, надоело", "t_uk": "ситий, набридло", "t_en": "full, fed up", "t_tr": "tok, bıkmış",
                   "t_pl": "najedzony, syty"}),
    13886: ("строка — прилагательное, а пример про язык (это Englisch)", {
        "t_uk": "англійський", "t_tr": "İngiliz", "t_cs": "anglický",
        **all_x("Wir haben einen englischen Film mit Untertiteln geschaut",
                "Мы смотрели английский фильм с субтитрами", "Ми дивилися англійський фільм із субтитрами",
                "We watched an English film with subtitles", "Altyazılı bir İngiliz filmi izledik",
                "Oglądaliśmy angielski film z napisami", "Abbiamo guardato un film inglese con i sottotitoli",
                "Vimos una película inglesa con subtítulos", "On a regardé un film anglais sous-titré",
                "Dívali jsme se na anglický film s titulky")}),
    1452: (EN, {"x_en": "I'm buying a used car"}),
    1827: ("снова Kleid; " + LIST, {
        "t_ru": "нарядный, элегантный", "t_uk": "елегантний, стильний", "t_en": "smart, stylish",
        **all_x("Für die Hochzeit hat er sich richtig schick gemacht", "На свадьбу он оделся очень нарядно",
                "На весілля він вбрався дуже елегантно", "He got really dressed up for the wedding",
                "Düğün için çok şık giyinmiş", "Na wesele ubrał się bardzo elegancko",
                "Per il matrimonio si è vestito molto elegante", "Para la boda se puso muy elegante",
                "Il s'est fait très chic pour le mariage", "Na svatbu se oblékl hodně elegantně")}),
    13887: (EN, {"x_en": "Can you be quiet for a moment?"}),
    1277: ("«Wir bieten gute Bedingungen» — реклама вакансии", {**all_x(
        "Die Stadt bietet viel für Familien", "Город может многое предложить семьям", "Місто багато що пропонує родинам",
        "The city has a lot to offer families", "Şehir ailelere çok şey sunuyor", "Miasto ma wiele do zaoferowania rodzinom",
        "La città offre molto alle famiglie", "La ciudad ofrece mucho a las familias", "La ville offre beaucoup aux familles",
        "Město nabízí rodinám hodně")}),
    10166: ("«Keine Panik, alles wird gut» — шаблон beruhigen («Beruhige dich mal, alles wird gut»)", {**all_x(
        "Als das Feuer ausbrach, gab es Panik", "Когда начался пожар, началась паника", "Коли почалася пожежа, почалася паніка",
        "When the fire broke out, there was panic", "Yangın çıkınca panik oldu", "Kiedy wybuchł pożar, wybuchła panika",
        "Quando è scoppiato l'incendio, c'è stato il panico", "Cuando empezó el incendio, cundió el pánico",
        "Quand le feu s'est déclaré, ça a été la panique", "Když vypukl požár, nastala panika")}),
    10167: ("«Du bist so ein Trottel» — шаблон Idiot («Ich bin so ein Idiot!»)", {**all_x(
        "Der Trottel hat mein Auto zugeparkt", "Этот болван заблокировал мою машину",
        "Цей бовдур заблокував мою машину", "That idiot has blocked my car in", "O ahmak arabamın önünü kapatmış",
        "Ten dureń zastawił mi samochód", "Quell'idiota mi ha bloccato la macchina", "El idiota ese me ha bloqueado el coche",
        "Cet imbécile m'a bloqué la voiture", "Ten trouba mi zablokoval auto")}),
    10168: (LIST, {"t_ru": "прощать, распределять", "t_uk": "пробачати, розподіляти", "t_en": "to forgive, to award",
                   "t_tr": "affetmek, vermek", "t_pl": "wybaczyć, przyznać", "t_it": "perdonare, assegnare",
                   "t_es": "perdonar, otorgar", "t_fr": "pardonner, attribuer", "t_cs": "odpustit, udělit"}),
    6506: ("«Das war viel Mühe umsonst» — шаблон umsonst («Das war alles umsonst»)", {**all_x(
        "Gib dir ein bisschen mehr Mühe!", "Постарайся немного побольше!", "Постарайся трохи більше!",
        "Make a bit more effort!", "Biraz daha çaba göster!", "Postaraj się trochę bardziej!",
        "Sforzati un po' di più!", "¡Esfuérzate un poco más!", "Fais un peu plus d'efforts!", "Snaž se trochu víc!")}),
    3056: ("«Das wird nicht zugelassen» — канцелярский пассив", {**all_x(
        "Das lasse ich nicht zu!", "Я этого не допущу!", "Я цього не допущу!", "I won't allow that!",
        "Buna izin vermem!", "Nie dopuszczę do tego!", "Non lo permetterò!", "¡No lo permitiré!",
        "Je ne le permettrai pas!", "To nedovolím!")}),
    10171: ("«Du bist sehr schlau» — пусто, и шаблон klug", {**all_x(
        "Der Fuchs ist ein schlaues Tier", "Лиса — хитрое животное", "Лисиця — хитра тварина",
        "The fox is a cunning animal", "Tilki kurnaz bir hayvandır", "Lis to sprytne zwierzę",
        "La volpe è un animale furbo", "El zorro es un animal astuto", "Le renard est un animal rusé",
        "Liška je mazané zvíře")}),
    10172: ("«Ich traue dir nicht» — шаблон vertrauen («Ich vertraue dir»)", {**all_x(
        "Ich traue mich nicht, ihn zu fragen", "Я не решаюсь его спросить", "Я не наважуюся його запитати",
        "I don't dare ask him", "Ona sormaya cesaret edemiyorum", "Nie odważę się go zapytać",
        "Non oso chiederglielo", "No me atrevo a preguntarle", "Je n'ose pas lui demander",
        "Neodvážím se ho zeptat")}),
    6518: ("«Я сопровождаю тебя к врачу» — канцелярски", {"x_ru": "Я провожу тебя к врачу",
                                                     "x_uk": "Я проведу тебе до лікаря"}),
    6519: ("«Deckung vor dem Regen» — шаблон Schutz («Schutz vor Regen»)", {**all_x(
        "Alle in Deckung!", "Все в укрытие!", "Усі в укриття!", "Everyone take cover!", "Herkes siper alsın!",
        "Wszyscy do schronienia!", "Tutti al riparo!", "¡Todos a cubierto!", "Tout le monde à l'abri!",
        "Všichni do úkrytu!")}),
    14945: ("«живём раздельно» — не первое, что слышат; в жизни — «zusammen oder getrennt?» в кафе", {**all_x(
        "Zahlen Sie zusammen oder getrennt?", "Вы платите вместе или раздельно?", "Ви платите разом чи окремо?",
        "Are you paying together or separately?", "Birlikte mi ödüyorsunuz, ayrı ayrı mı?",
        "Płacą Państwo razem czy osobno?", "Pagate insieme o separatamente?", "¿Pagan juntos o por separado?",
        "Vous payez ensemble ou séparément?", "Platíte dohromady, nebo zvlášť?")}),
}

SPLIT_LATER = {}
