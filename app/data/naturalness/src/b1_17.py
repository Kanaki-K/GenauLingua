"""B1, блок 17: следующие 40 по частоте. Вычитано вручную 21.10."""

EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    9733: (EN + " («I receive a check»)", {"x_en": "I'm getting a cheque for 100 euros"}),
    18140: ("«Die Mauer ist sehr hoch» — скелет; Mauer у немца — прежде всего Берлинская стена", {**all_x(
        "Die Berliner Mauer ist 1989 gefallen", "Берлинская стена пала в 1989 году", "Берлінська стіна впала в 1989 році",
        "The Berlin Wall came down in 1989", "Berlin Duvarı 1989'da yıkıldı", "Mur berliński upadł w 1989 roku",
        "Il Muro di Berlino è caduto nel 1989", "El Muro de Berlín cayó en 1989", "Le mur de Berlin est tombé en 1989",
        "Berlínská zeď padla v roce 1989")}),
    15990: ("«Der Verbrecher ist im Gefängnis» — пусто, шаблон Gefängnis", {**all_x(
        "Er sieht nicht aus wie ein Verbrecher", "Он не похож на преступника", "Він не схожий на злочинця",
        "He doesn't look like a criminal", "Bir suçluya benzemiyor", "Nie wygląda na przestępcę",
        "Non sembra un criminale", "No parece un delincuente", "Il n'a pas l'air d'un criminel",
        "Nevypadá jako zločinec")}),
    2004: ("«Er trägt eine Uniform» — шаблон одежды", {**all_x(
        "Ohne Uniform erkenne ich ihn gar nicht", "Без формы я его даже не узнаю", "Без форми я його навіть не впізнаю",
        "I don't even recognise him without his uniform", "Üniforması olmadan onu tanımıyorum bile",
        "Bez munduru w ogóle go nie poznaję", "Senza divisa non lo riconosco nemmeno", "Sin uniforme ni lo reconozco",
        "Sans uniforme, je ne le reconnais même pas", "Bez uniformy ho vůbec nepoznám")}),
    2973: (EN + " («We need support»)", {"x_en": "We need backup"}),
    10218: ("«Ты должен лучше себя вести» — калька с sollst", {"x_ru": "Тебе надо лучше себя вести",
                                                         "x_uk": "Тобі треба краще поводитися"}),
    813: ("«Die Schulter tut weh» — шаблон Bauch, Ohr, Knie", {**all_x(
        "Er legt mir die Hand auf die Schulter", "Он кладёт мне руку на плечо", "Він кладе мені руку на плече",
        "He puts his hand on my shoulder", "Elini omzuma koyuyor", "Kładzie mi rękę na ramieniu",
        "Mi mette una mano sulla spalla", "Me pone la mano en el hombro", "Il me met la main sur l'épaule",
        "Položí mi ruku na rameno")}),
    14966: ("«Die Scheidung ist sehr schwer» — пусто", {**all_x(
        "Nach der Scheidung ist sie nach Berlin gezogen", "После развода она переехала в Берлин",
        "Після розлучення вона переїхала до Берліна", "After the divorce she moved to Berlin",
        "Boşandıktan sonra Berlin'e taşındı", "Po rozwodzie przeprowadziła się do Berlina",
        "Dopo il divorzio si è trasferita a Berlino", "Después del divorcio se mudó a Berlín",
        "Après le divorce, elle a déménagé à Berlin", "Po rozvodu se přestěhovala do Berlína")}),
    10219: ("снова Film; en «excited about the movie» — смысл другой", {**all_x(
        "Die Kinder waren total begeistert vom Zoo", "Дети были в полном восторге от зоопарка",
        "Діти були в повному захваті від зоопарку", "The kids were really excited about the zoo",
        "Çocuklar hayvanat bahçesine hayran kaldı", "Dzieci były zachwycone zoo",
        "I bambini erano entusiasti dello zoo", "Los niños estaban encantados con el zoo",
        "Les enfants étaient ravis du zoo", "Děti byly ze zoo nadšené")}),
    18652: (EN + " («I don't have time currently»)", {"x_en": "I don't have time at the moment"}),
    10221: ("«clevere Idee von dir» — шаблон klug, schlau («… von dir»)", {**all_x(
        "Er ist ein cleverer Geschäftsmann", "Он смекалистый бизнесмен", "Він кмітливий бізнесмен",
        "He's a shrewd businessman", "Kurnaz bir iş adamı", "To sprytny biznesmen", "È un uomo d'affari furbo",
        "Es un hombre de negocios astuto", "C'est un homme d'affaires astucieux", "Je to mazaný obchodník")}),
    10224: ("«Sein Hass gegen ihn ist groß» — неживо", {**all_x(
        "Ich verstehe diesen Hass nicht", "Я не понимаю этой ненависти", "Я не розумію цієї ненависті",
        "I don't understand this hatred", "Bu nefreti anlamıyorum", "Nie rozumiem tej nienawiści",
        "Non capisco quest'odio", "No entiendo este odio", "Je ne comprends pas cette haine", "Nechápu tu nenávist")}),
    12511: ("«Streng dein Hirn mal an» — шаблон Gehirn («Schalt mal dein Gehirn ein!»)", {**all_x(
        "Mein Hirn funktioniert heute überhaupt nicht", "У меня сегодня мозг совсем не работает",
        "У мене сьогодні мозок зовсім не працює", "My brain's not working at all today",
        "Bugün beynim hiç çalışmıyor", "Mój mózg dziś w ogóle nie działa", "Oggi il cervello non mi funziona",
        "Hoy el cerebro no me funciona", "Aujourd'hui, mon cerveau ne marche pas du tout",
        "Mozek mi dneska vůbec nefunguje")}),
    6625: ("«Er kommt sicherlich zu spät» — шаблон vermutlich («Er kommt vermutlich zu spät»)", {**all_x(
        "Du hast sicherlich Hunger nach der Reise", "Ты наверняка проголодался после поездки",
        "Ти напевно зголоднів після поїздки", "You're surely hungry after the journey",
        "Yolculuktan sonra kesinlikle acıkmışsındır", "Pewnie jesteś głodny po podróży",
        "Sicuramente hai fame dopo il viaggio", "Seguramente tienes hambre después del viaje",
        "Tu as sûrement faim après le voyage", "Určitě máš po cestě hlad")}),
    6627: ("«einen amerikanischen Film» — шаблон englisch («einen englischen Film»)", {**all_x(
        "Das ist ein typisch amerikanisches Frühstück", "Это типично американский завтрак",
        "Це типово американський сніданок", "That's a typical American breakfast", "Bu tipik bir Amerikan kahvaltısı",
        "To typowo amerykańskie śniadanie", "È una colazione tipicamente americana",
        "Es un desayuno típicamente americano", "C'est un petit-déjeuner typiquement américain",
        "To je typicky americká snídaně")}),
    14397: ("«Das Publikum klatscht Applaus» — масло масляное, шаблон Publikum", {**all_x(
        "Am Ende gab es viel Applaus", "В конце долго аплодировали", "Наприкінці довго аплодували",
        "There was a lot of applause at the end", "Sonunda uzun uzun alkışlandı", "Na koniec były gromkie oklaski",
        "Alla fine c'è stato un lungo applauso", "Al final hubo muchos aplausos",
        "À la fin, il y a eu beaucoup d'applaudissements", "Na konci byl velký potlesk")}),
    2024: (EN + " («I'm saying goodbye»)", {"x_en": "I'll say goodbye then"}),
}

SPLIT_LATER = {}
