"""Вычитка немецкого, порция p033 (B2), 23.10: заглушки → бытовые фразы"""

W = "вычитка немецкого: учебная заглушка → живая бытовая фраза"

def ex(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"example_de": de, "example_ru": ru, "example_uk": uk, "example_en": en, "example_tr": tr,
            "example_pl": pl, "example_it": it, "example_es": es, "example_fr": fr, "example_cs": cs}

FIXES = {
    13516: (W, ex("Hiervon darf meine Frau nichts erfahren, das ist eine Überraschung",
        "Об этом моя жена не должна ничего узнать, это сюрприз", "Про це моя дружина не повинна нічого дізнатися, це сюрприз",
        "My wife mustn't find out about this, it's a surprise", "Karım bundan haberdar olmamalı, bu bir sürpriz",
        "Moja żona nie może się o tym dowiedzieć, to niespodzianka", "Mia moglie non deve saperne niente, è una sorpresa",
        "Mi mujer no puede enterarse de esto, es una sorpresa", "Ma femme ne doit rien en savoir, c'est une surprise",
        "Moje žena se o tom nesmí dozvědět, je to překvapení")),
    13517: (W + "; «Hierbei ist Vorsicht geboten» — инструкция", ex("Wir streichen am Samstag die Küche, hierbei helfen uns die Nachbarn",
        "В субботу мы красим кухню, при этом нам помогают соседи", "У суботу ми фарбуємо кухню, при цьому нам допомагають сусіди",
        "We're painting the kitchen on Saturday, and the neighbours are helping us with it", "Cumartesi mutfağı boyuyoruz, bu işte komşular bize yardım ediyor",
        "W sobotę malujemy kuchnię, przy tym pomagają nam sąsiedzi", "Sabato imbianchiamo la cucina, e in questo ci aiutano i vicini",
        "El sábado pintamos la cocina, y para ello nos ayudan los vecinos", "Samedi, on repeint la cuisine, et les voisins nous aident pour ça",
        "V sobotu malujeme kuchyň, a při tom nám pomáhají sousedé")),
    13525: (W, ex("Hier im Dorf kennt jedermann jeden",
        "Здесь в деревне каждый знает каждого", "Тут у селі кожен знає кожного",
        "Here in the village everyone knows everybody", "Burada köyde herkes herkesi tanır",
        "Tu na wsi każdy zna każdego", "Qui in paese ognuno conosce tutti",
        "Aquí en el pueblo todo el mundo se conoce", "Ici, au village, tout le monde connaît tout le monde",
        "Tady na vesnici zná každý každého")),
    13664: (W, ex("Du hast Lippenstift am Zahn",
        "У тебя помада на зубе", "У тебе помада на зубі",
        "You've got lipstick on your tooth", "Dişinde ruj var",
        "Masz szminkę na zębie", "Hai del rossetto sul dente",
        "Tienes pintalabios en el diente", "Tu as du rouge à lèvres sur la dent",
        "Máš rtěnku na zubu")),
    13670: (W, ex("Das Armband hat mir meine Tochter selbst gebastelt",
        "Этот браслет дочка сделала мне своими руками", "Цей браслет донька зробила мені власноруч",
        "My daughter made this bracelet for me herself", "Bu bileziği kızım kendi elleriyle yaptı",
        "Tę bransoletkę zrobiła mi córka sama", "Questo braccialetto me l'ha fatto mia figlia da sola",
        "Esta pulsera me la hizo mi hija ella misma", "Ce bracelet, c'est ma fille qui me l'a fabriqué elle-même",
        "Tenhle náramek mi dcera sama vyrobila")),
    13674: (W + "; второе значение: ставить на огонь", ex("Ich setze schon mal Wasser für die Nudeln auf",
        "Я пока поставлю воду для макарон", "Я поки поставлю воду для макаронів",
        "I'll put the water on for the pasta", "Ben makarna için suyu ocağa koyayım",
        "Nastawię już wodę na makaron", "Intanto metto su l'acqua per la pasta",
        "Voy poniendo el agua para la pasta", "Je mets déjà l'eau à chauffer pour les pâtes",
        "Dám zatím vařit vodu na těstoviny")),
    13687: (W, ex("Meine Halskette hat sich im Koffer total verknotet",
        "Моя цепочка в чемодане совсем запуталась", "Мій ланцюжок у валізі зовсім заплутався",
        "My necklace got completely tangled in the suitcase", "Kolyem bavulda tamamen düğümlenmiş",
        "Mój naszyjnik całkiem się splątał w walizce", "La mia collana si è tutta annodata in valigia",
        "Mi collar se ha enredado entero en la maleta", "Mon collier s'est complètement emmêlé dans la valise",
        "Řetízek se mi v kufru úplně zamotal")),
    14007: (W + "; реклама", ex("Die Stadt macht eine Kampagne gegen Müll im Park",
        "Город проводит кампанию против мусора в парке", "Місто проводить кампанію проти сміття в парку",
        "The council is running a campaign against litter in the park", "Belediye parkta çöpe karşı bir kampanya yürütüyor",
        "Miasto prowadzi kampanię przeciw śmieciom w parku", "Il comune fa una campagna contro i rifiuti nel parco",
        "El ayuntamiento hace una campaña contra la basura en el parque", "La ville fait une campagne contre les déchets dans le parc",
        "Město dělá kampaň proti odpadkům v parku")),
    14029: (W, ex("Wer überbringt ihr die schlechte Nachricht?",
        "Кто передаст ей плохую новость?", "Хто передасть їй погану новину?",
        "Who's going to break the bad news to her?", "Kötü haberi ona kim iletecek?",
        "Kto przekaże jej złą wiadomość?", "Chi le porta la brutta notizia?",
        "¿Quién le da la mala noticia?", "Qui va lui annoncer la mauvaise nouvelle ?",
        "Kdo jí předá tu špatnou zprávu?")),
}

REPLACE = []

SPLIT_LATER = {}
