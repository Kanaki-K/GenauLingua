"""B1, блок 19: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    2401: ("«Der Empfang war herzlich» — книжно; в жизни Empfang — стойка в отеле", {
        "t_ru": "приём, стойка регистрации", "t_uk": "прийом, рецепція", "t_en": "reception, welcome",
        "t_tr": "resepsiyon, karşılama", "t_pl": "recepcja, przyjęcie", "t_it": "la reception, l'accoglienza",
        "t_es": "la recepción, la acogida", "t_fr": "la réception, l'accueil", "t_cs": "recepce, přijetí",
        **all_x("Den Schlüssel bekommen Sie am Empfang", "Ключ вы получите на стойке регистрации",
                "Ключ ви отримаєте на рецепції", "You'll get the key at reception", "Anahtarı resepsiyondan alırsınız",
                "Klucz jest do odebrania w recepcji", "La chiave la riceve alla reception",
                "La llave se la dan en recepción", "Vous aurez la clé à la réception", "Klíč dostanete na recepci")}),
    10242: ("«Я чувствую к нему жалость» — калька", {"x_ru": "Мне его жалко", "x_uk": "Мені його шкода"}),
    2721: ("«Die Erde ist ein Planet» — школьный факт", {**all_x(
        "Wir haben nur diesen einen Planeten", "У нас есть только одна планета", "У нас є лише одна планета",
        "We only have this one planet", "Sadece bu tek gezegenimiz var", "Mamy tylko tę jedną planetę",
        "Abbiamo solo questo pianeta", "Solo tenemos este planeta", "On n'a que cette seule planète",
        "Máme jen tuhle jednu planetu")}),
    6636: ("«Du musst pünktlich erscheinen» — повестка; живое значение — «выходить» (о книге)", {**all_x(
        "Das Buch erscheint im Mai", "Книга выйдет в мае", "Книжка вийде в травні",
        "The book will be published in May", "Kitap mayısta yayımlanacak", "Książka ukaże się w maju",
        "Il libro esce a maggio", "El libro se publica en mayo", "Le livre paraît en mai", "Kniha vyjde v květnu")}),
    15428: ("«Der Stern leuchtet» — пусто", {**all_x(
        "Heute Nacht sieht man viele Sterne", "Сегодня ночью видно много звёзд", "Сьогодні вночі видно багато зірок",
        "You can see lots of stars tonight", "Bu gece çok yıldız görünüyor", "Dziś w nocy widać dużo gwiazd",
        "Stanotte si vedono molte stelle", "Esta noche se ven muchas estrellas", "Cette nuit, on voit beaucoup d'étoiles",
        "Dnes v noci je vidět hodně hvězd")}),
    6638: ("снова «головная боль»", {**all_x(
        "Die Arbeit bereitet mir viel Freude", "Работа доставляет мне много радости", "Робота приносить мені багато радості",
        "The work gives me a lot of pleasure", "İş bana çok mutluluk veriyor", "Praca sprawia mi dużo radości",
        "Il lavoro mi procura molta gioia", "El trabajo me da mucha alegría", "Le travail me donne beaucoup de joie",
        "Práce mi působí velkou radost")}),
    1915: ("«Es gibt eine Störung» — пусто; перевод — список из шести", {
        "t_ru": "сбой, беспокойство", "t_uk": "збій, турбування", "t_en": "fault, disturbance", "t_tr": "arıza, rahatsız etme",
        "t_pl": "awaria, przeszkadzanie", "t_it": "il guasto, il disturbo", "t_es": "la avería, la molestia",
        "t_fr": "la panne, le dérangement", "t_cs": "porucha, rušení",
        **all_x("Entschuldigen Sie die Störung", "Извините за беспокойство", "Вибачте за турбування",
                "Sorry for the disturbance", "Rahatsız ettiğim için kusura bakmayın", "Przepraszam, że przeszkadzam",
                "Scusi il disturbo", "Perdone la molestia", "Excusez-moi du dérangement", "Promiňte, že ruším")}),
    6645: ("«Das ist die zentrale Frage» — книжно; в жизни — «liegt zentral»", {**all_x(
        "Die Wohnung liegt sehr zentral", "Квартира находится в центре города", "Квартира в центрі міста",
        "The flat is very central", "Daire şehir merkezinde", "Mieszkanie jest położone w centrum",
        "L'appartamento è molto centrale", "El piso es muy céntrico", "L'appartement est très central", "Byt je v centru")}),
    9448: ("«Die erste Lektion war schwierig» — шаблон schwierig; живое значение — «урок» из жизни", {**all_x(
        "Das war mir eine Lektion", "Это стало для меня уроком", "Це стало для мене уроком", "That taught me a lesson",
        "Bu bana ders oldu", "To była dla mnie nauczka", "Mi è servito da lezione", "Me sirvió de lección",
        "Ça m'a servi de leçon", "Bylo mi to ponaučením")}),
    14399: ("«Ich trage ein Kreuz um den Hals» — шаблон одежды", {**all_x(
        "Mach ein Kreuz bei der richtigen Antwort", "Поставь крестик у правильного ответа",
        "Постав хрестик біля правильної відповіді", "Put a cross next to the right answer",
        "Doğru cevaba çarpı işareti koy", "Postaw krzyżyk przy dobrej odpowiedzi", "Metti una croce sulla risposta giusta",
        "Pon una cruz en la respuesta correcta", "Mets une croix à côté de la bonne réponse",
        "Udělej křížek u správné odpovědi")}),
    6652: ("«Dreh dich um!» — тот же пример, что у drehen", {**all_x(
        "Dreh das Fleisch nach fünf Minuten um", "Через пять минут переверни мясо", "Через п'ять хвилин переверни м'ясо",
        "Turn the meat over after five minutes", "Beş dakika sonra eti ters çevir", "Po pięciu minutach odwróć mięso",
        "Dopo cinque minuti gira la carne", "Dale la vuelta a la carne a los cinco minutos",
        "Retourne la viande au bout de cinq minutes", "Po pěti minutách maso otoč")}),
    18142: ("«Hier ist überall Staub» — шаблон Dreck («Hier ist überall Dreck»)", {**all_x(
        "Am Samstag wische ich Staub", "По субботам я вытираю пыль", "По суботах я витираю пил",
        "On Saturdays I do the dusting", "Cumartesileri toz alıyorum", "W soboty ścieram kurze",
        "Il sabato tolgo la polvere", "Los sábados quito el polvo", "Le samedi, je fais la poussière",
        "V sobotu utírám prach")}),
    15430: ("«Der Tiger ist sehr gefährlich» — пусто", {**all_x(
        "Im Zoo haben wir einen weißen Tiger gesehen", "В зоопарке мы видели белого тигра", "У зоопарку ми бачили білого тигра",
        "We saw a white tiger at the zoo", "Hayvanat bahçesinde beyaz bir kaplan gördük",
        "W zoo widzieliśmy białego tygrysa", "Allo zoo abbiamo visto una tigre bianca", "En el zoo vimos un tigre blanco",
        "Au zoo, on a vu un tigre blanc", "V zoo jsme viděli bílého tygra")}),
    2813: (EN + " («I watch a series»)", {"x_en": "I'm watching a series"}),
    6656: ("девятый пример про погоду («extrem heiß»)", {**all_x(
        "Er ist extrem ehrgeizig", "Он крайне честолюбив", "Він надзвичайно амбітний", "He's extremely ambitious",
        "Son derece hırslı", "Jest niezwykle ambitny", "È estremamente ambizioso", "Es extremadamente ambicioso",
        "Il est extrêmement ambitieux", "Je extrémně ambiciózní")}),
}

# Stellung (о работе) — то же, что Stelle; пример был тот же
REPLACE = [{"id": 8783, "by": 1909, "lang": "de", "why": "Stellung — книжный вариант Stelle (о работе)"}]

SPLIT_LATER = {}
