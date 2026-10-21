"""B1, блок 44: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    17935: ("«Der Winkel … ist 90 Grad» — учебник; " + LIST, {
        "t_ru": "угол, закуток", "t_uk": "кут, закуток", "t_en": "angle, corner", "t_tr": "açı, köşe", "t_pl": "kąt, zakątek",
        **all_x("Aus diesem Winkel sieht das Foto besser aus", "Под этим углом фото выглядит лучше",
                "Під цим кутом фото виглядає краще", "The photo looks better from this angle",
                "Fotoğraf bu açıdan daha iyi görünüyor", "Pod tym kątem zdjęcie wygląda lepiej",
                "Da quest'angolo la foto viene meglio", "Desde este ángulo la foto queda mejor",
                "Sous cet angle, la photo est plus belle", "Z tohohle úhlu vypadá fotka líp")}),
    1183: ("«Ich führe den Befehl aus» — армия; " + LIST, {
        "t_ru": "выполнять, выводить на прогулку", "t_uk": "виконувати, виводити на прогулянку",
        "t_en": "to carry out, to take out (for a walk)", "t_tr": "yerine getirmek, gezdirmek",
        "t_pl": "wykonywać, wyprowadzać (psa)", "t_it": "eseguire, portare fuori", "t_es": "ejecutar, sacar a pasear",
        "t_fr": "exécuter, promener", "t_cs": "provádět, venčit",
        **all_x("Abends führe ich den Hund aus", "Вечером я вывожу собаку на прогулку", "Увечері я виводжу собаку на прогулянку",
                "In the evening I take the dog out for a walk", "Akşamları köpeği gezdiriyorum", "Wieczorem wyprowadzam psa",
                "La sera porto fuori il cane", "Por la noche saco a pasear al perro", "Le soir, je promène le chien",
                "Večer venčím psa")}),
    6965: (LIST + "; en «cancel the trip» — не тот смысл", {
        "t_ru": "прервать, бросить (учёбу)", "t_uk": "перервати, покинути (навчання)", "t_en": "to break off, to drop out",
        "t_tr": "yarıda kesmek, bırakmak", "t_pl": "przerwać, zrezygnować", "t_it": "interrompere, abbandonare",
        "t_es": "interrumpir, abandonar", "t_fr": "interrompre, abandonner", "t_cs": "přerušit, ukončit",
        "x_en": "Unfortunately we had to cut the trip short"}),
    2400: ("«Das war sehr emotional» — пусто", {**all_x(
        "Bei Hochzeiten werde ich immer emotional", "На свадьбах я всегда очень эмоциональна", "На весіллях я завжди дуже емоційна",
        "I always get emotional at weddings", "Düğünlerde hep duygusallaşırım", "Na weselach zawsze robię się emocjonalna",
        "Ai matrimoni divento sempre emotiva", "En las bodas siempre me pongo emotiva",
        "Aux mariages, je deviens toujours émotive", "Na svatbách jsem vždycky emotivní")}),
    18698: ("«Ich bin seiner ewigen Nörgeleien … müde» — книжно; " + LIST, {
        "t_ru": "вечный, бесконечный", "t_uk": "вічний, безкінечний", "t_en": "eternal, endless", "t_tr": "sonsuz, bitmek bilmeyen",
        "t_pl": "wieczny, nieustanny",
        **all_x("Hör auf mit deinem ewigen Gejammer!", "Хватит твоего вечного нытья!", "Досить твого вічного ниття!",
                "Stop your endless moaning!", "Bitmek bilmeyen sızlanmanı kes!", "Przestań z tym swoim wiecznym marudzeniem!",
                "Smettila con le tue eterne lamentele!", "¡Deja ya tus eternas quejas!", "Arrête avec tes éternelles jérémiades!",
                "Přestaň s tím věčným fňukáním!")}),
    13975: ("пример многословный", {**all_x(
        "Das ist doch völlig verständlich", "Это же вполне понятно", "Це ж цілком зрозуміло", "That's perfectly understandable",
        "Bu çok anlaşılır", "To zupełnie zrozumiałe", "È del tutto comprensibile", "Es totalmente comprensible",
        "C'est tout à fait compréhensible", "To je naprosto pochopitelné")}),
    2979: ("«Das verursacht Probleme» — пусто", {**all_x(
        "Wer hat den Unfall verursacht?", "Кто стал причиной аварии?", "Хто спричинив аварію?", "Who caused the accident?",
        "Kazaya kim sebep oldu?", "Kto spowodował wypadek?", "Chi ha causato l'incidente?", "¿Quién causó el accidente?",
        "Qui a causé l'accident?", "Kdo způsobil tu nehodu?")}),
    6969: (EN + " («I determined»)", {"x_en": "I've found out he isn't coming"}),
    6970: ("ru «должно действовать» — калька", {"x_ru": "Это правило действует для всех"}),
    12166: ("«Der Streich war witzig …» — претерит", {**all_x(
        "Die Kinder haben dem Lehrer einen Streich gespielt", "Дети устроили учителю проделку", "Діти влаштували вчителеві витівку",
        "The kids played a prank on the teacher", "Çocuklar öğretmene şaka yaptı", "Dzieci spłatały nauczycielowi figla",
        "I bambini hanno fatto uno scherzo al maestro", "Los niños le gastaron una broma al profesor",
        "Les enfants ont joué un tour au prof", "Děti udělaly učiteli žert")}),
    15481: ("«Wir saßen am Ufer …» — претерит", {**all_x(
        "Wir machen ein Picknick am Ufer vom See", "Мы устраиваем пикник на берегу озера", "Ми влаштовуємо пікнік на березі озера",
        "We're having a picnic on the lake shore", "Göl kıyısında piknik yapıyoruz", "Robimy piknik nad brzegiem jeziora",
        "Facciamo un picnic sulla riva del lago", "Hacemos un pícnic en la orilla del lago", "On pique-nique au bord du lac",
        "Děláme si piknik na břehu jezera")}),
    9770: ("«Der Eintritt ist gratis» — шаблон kostenlos («Für Kinder ist der Eintritt kostenlos»)", {**all_x(
        "Den Kaffee gibt's gratis dazu", "Кофе дают бесплатно в придачу", "Каву дають безкоштовно на додачу",
        "The coffee comes free", "Kahve bedava veriliyor", "Kawa jest gratis", "Il caffè te lo danno gratis",
        "El café te lo dan gratis", "Le café est offert gratuitement", "Kafe je k tomu zdarma")}),
    2794: ("«Ich schneide eine Scheibe Brot» — пусто", {**all_x(
        "Möchtest du noch eine Scheibe Käse?", "Хочешь ещё ломтик сыра?", "Хочеш ще скибочку сиру?",
        "Would you like another slice of cheese?", "Bir dilim peynir daha ister misin?", "Chcesz jeszcze plasterek sera?",
        "Vuoi un'altra fetta di formaggio?", "¿Quieres otra loncha de queso?", "Tu veux encore une tranche de fromage?",
        "Dáš si ještě plátek sýra?")}),
    13976: ("«Der Skandal war in den Nachrichten …» — претерит, хроника", {**all_x(
        "Das ist ja ein Skandal!", "Это же скандал!", "Це ж скандал!", "That's a scandal!", "Bu tam bir skandal!",
        "To skandal!", "È uno scandalo!", "¡Es un escándalo!", "C'est un scandale!", "To je skandál!")}),
    9771: ("«Der Käufer war zufrieden …» — претерит", {**all_x(
        "Für das alte Auto finde ich keinen Käufer", "Я не могу найти покупателя на старую машину",
        "Я не можу знайти покупця на стару машину", "I can't find a buyer for the old car",
        "Eski araba için alıcı bulamıyorum", "Nie mogę znaleźć kupca na stary samochód",
        "Non trovo un acquirente per la vecchia macchina", "No encuentro comprador para el coche viejo",
        "Je ne trouve pas d'acheteur pour la vieille voiture", "Na staré auto nemůžu najít kupce")}),
    6975: ("«Der Himmel war grau und bedeckt» — снова погода, претерит", {**all_x(
        "Der Boden ist mit Laub bedeckt", "Земля покрыта листьями", "Земля вкрита листям", "The ground is covered with leaves",
        "Yer yapraklarla örtülü", "Ziemia jest pokryta liśćmi", "Il terreno è coperto di foglie",
        "El suelo está cubierto de hojas", "Le sol est couvert de feuilles", "Zem je pokrytá listím")}),
    9772: ("пример про sparen, а не про ersparen; " + LIST, {
        "t_ru": "избавить, сэкономить", "t_uk": "позбавити, уберегти", "t_en": "to spare, to save",
        "t_tr": "birini bir şeyden kurtarmak, tasarruf etmek", "t_pl": "oszczędzić komuś czegoś, zaoszczędzić",
        **all_x("Erspar mir die Details!", "Избавь меня от подробностей!", "Позбав мене подробиць!", "Spare me the details!",
                "Beni ayrıntılardan kurtar!", "Oszczędź mi szczegółów!", "Risparmiami i dettagli!", "¡Ahórrame los detalles!",
                "Épargne-moi les détails!", "Ušetři mě podrobností!")}),
    17122: ("«Die Landung … war sanft und sicher» — претерит", {**all_x(
        "Kurz vor der Landung bin ich aufgewacht", "Я проснулся перед самой посадкой", "Я прокинувся перед самою посадкою",
        "I woke up just before landing", "İnişten hemen önce uyandım", "Obudziłem się tuż przed lądowaniem",
        "Mi sono svegliato poco prima dell'atterraggio", "Me desperté justo antes del aterrizaje",
        "Je me suis réveillé juste avant l'atterrissage", "Probudil jsem se těsně před přistáním")}),
    6977: (EN, {"x_en": "I'm tired anyway and don't feel like working any more"}),
    10405: ("«Er war sehr konzentriert und hat sich … fokussiert» — масло масляное", {**all_x(
        "Er arbeitet sehr konzentriert", "Он работает очень сосредоточенно", "Він працює дуже зосереджено",
        "He works in a very focused way", "Çok odaklanmış çalışıyor", "Pracuje bardzo skupiony", "Lavora molto concentrato",
        "Trabaja muy concentrado", "Il travaille de façon très concentrée", "Pracuje velmi soustředěně")}),
    6978: ("«Rauchen schadet deiner Gesundheit» — надпись на пачке", {**all_x(
        "Ein bisschen Bewegung kann nicht schaden", "Немного движения не повредит", "Трохи руху не зашкодить",
        "A bit of exercise can't hurt", "Biraz hareket zarar vermez", "Trochę ruchu nie zaszkodzi",
        "Un po' di movimento non fa male", "Un poco de ejercicio no hace daño",
        "Un peu d'exercice ne peut pas faire de mal", "Trocha pohybu neuškodí")}),
}

REPLACE = [
    {"id": 6966, "by": 2426, "lang": "de", "why": "erhöht — причастие от erhöhen"},
    {"id": 18700, "by": 1008, "lang": "de", "why": "gewaschen — причастие от waschen; пример пустой"},
]

SPLIT_LATER = {}
