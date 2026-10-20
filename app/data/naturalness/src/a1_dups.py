"""A1: совпадающие немецкие примеры у разных слов — по проверке всей базы 21.10.

Два повтора внёс сам при вычитке (Kurs — как у Deutschkurs, Licht — как у
anmachen), остальные были в базе. Правится строка, которая уже вычитана;
вторая из пары — при своей очереди.
"""

SAME = "пример совпадал с примером другого слова (проверка всей базы 21.10)"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    520: (SAME + " — Deutschkurs (внесено мной в блоке 11)", {**all_x(
        "Wie viele Leute sind in deinem Kurs?", "Сколько человек у тебя на курсах?", "Скільки людей у тебе на курсах?",
        "How many people are in your class?", "Kursunda kaç kişi var?", "Ile osób jest na twoim kursie?",
        "Quante persone ci sono nel tuo corso?", "¿Cuántas personas hay en tu curso?",
        "Combien de personnes il y a dans ton cours?", "Kolik lidí je ve tvém kurzu?")}),
    6296: (SAME + " — anmachen (внесено мной в блоке 8)", {**all_x(
        "Mach bitte das Licht aus, wenn du gehst", "Выключай свет, когда уходишь", "Вимикай світло, коли йдеш",
        "Turn off the light when you leave", "Çıkarken ışığı kapat", "Wyłączaj światło, kiedy wychodzisz",
        "Spegni la luce quando esci", "Apaga la luz cuando salgas", "Éteins la lumière quand tu pars",
        "Zhasni světlo, až budeš odcházet")}),
    732: (SAME + " — kein («Das ist kein Problem»)", {**all_x(
        "Wir haben ein kleines Problem", "У нас небольшая проблема", "У нас невелика проблема",
        "We have a small problem", "Küçük bir sorunumuz var", "Mamy mały problem", "Abbiamo un piccolo problema",
        "Tenemos un pequeño problema", "On a un petit problème", "Máme malý problém")}),
    382: (SAME + " — zu Hause («Ich bin zu Hause»)", {**all_x(
        "Unser Haus hat einen großen Garten", "У нашего дома большой сад", "У нашого будинку великий сад",
        "Our house has a big garden", "Evimizin büyük bir bahçesi var", "Nasz dom ma duży ogród",
        "La nostra casa ha un grande giardino", "Nuestra casa tiene un jardín grande",
        "Notre maison a un grand jardin", "Náš dům má velkou zahradu")}),
    319: (SAME + " — spazieren («Ich gehe spazieren»)", {**all_x(
        "Gehst du heute noch zum Supermarkt?", "Ты сегодня ещё пойдёшь в магазин?", "Ти сьогодні ще підеш до магазину?",
        "Are you going to the supermarket today?", "Bugün markete gidecek misin?", "Idziesz dziś jeszcze do sklepu?",
        "Vai ancora al supermercato oggi?", "¿Vas a ir hoy al supermercado?",
        "Tu vas encore au supermarché aujourd'hui?", "Půjdeš dnes ještě do obchodu?")}),
    1071: (SAME + " — keine («Ich habe keine Zeit»)", {**all_x(
        "Hast du morgen Zeit?", "У тебя завтра есть время?", "У тебе завтра є час?", "Do you have time tomorrow?",
        "Yarın vaktin var mı?", "Masz jutro czas?", "Hai tempo domani?", "¿Tienes tiempo mañana?",
        "Tu as le temps demain?", "Máš zítra čas?")}),
    421: (SAME + " — Musik («Ich höre gern Musik»)", {**all_x(
        "Hörst du mich?", "Ты меня слышишь?", "Ти мене чуєш?", "Can you hear me?", "Beni duyuyor musun?",
        "Słyszysz mnie?", "Mi senti?", "¿Me oyes?", "Tu m'entends?", "Slyšíš mě?")}),
    135: (SAME + " — schreiben («Ich schreibe einen Brief»)", {**all_x(
        "Ich habe einen Brief von meiner Oma bekommen", "Я получил письмо от бабушки", "Я отримав листа від бабусі",
        "I got a letter from my grandma", "Büyükannemden bir mektup aldım", "Dostałem list od babci",
        "Ho ricevuto una lettera da mia nonna", "He recibido una carta de mi abuela",
        "J'ai reçu une lettre de ma grand-mère", "Dostal jsem dopis od babičky")}),
    1043: (SAME + " — kalt («Im Winter ist es kalt»)", {**all_x(
        "Im Winter fahren wir Ski", "Зимой мы катаемся на лыжах", "Взимку ми катаємося на лижах",
        "In winter we go skiing", "Kışın kayak yaparız", "Zimą jeździmy na nartach", "D'inverno andiamo a sciare",
        "En invierno vamos a esquiar", "En hiver, on fait du ski", "V zimě jezdíme lyžovat")}),
    1091: (SAME + " — reden («Wir reden über das Problem»)", {**all_x(
        "Das Bild hängt über dem Sofa", "Картина висит над диваном", "Картина висить над диваном",
        "The picture hangs over the sofa", "Resim kanepenin üstünde asılı", "Obraz wisi nad kanapą",
        "Il quadro è appeso sopra il divano", "El cuadro está colgado encima del sofá",
        "Le tableau est accroché au-dessus du canapé", "Obraz visí nad gaučem")}),
    19: (SAME + " — hängen, Wand («Das Bild hängt an der Wand»)", {**all_x(
        "Wir treffen uns an der Haltestelle", "Встретимся на остановке", "Зустрінемося на зупинці",
        "Let's meet at the bus stop", "Durakta buluşalım", "Spotkajmy się na przystanku", "Ci vediamo alla fermata",
        "Nos vemos en la parada", "On se retrouve à l'arrêt", "Sejdeme se na zastávce")}),
}
