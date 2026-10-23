"""Вычитка немецкого, порция p037 (B2), 23.10: техника, дом — заглушки → бытовые фразы"""

W = "вычитка немецкого: учебная заглушка → живая бытовая фраза"

def ex(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"example_de": de, "example_ru": ru, "example_uk": uk, "example_en": en, "example_tr": tr,
            "example_pl": pl, "example_it": it, "example_es": es, "example_fr": fr, "example_cs": cs}

FIXES = {
    17550: (W + "; «Die Elektrizität ist ausgefallen» — так говорят Strom", ex("Ohne Elektrizität funktioniert in unserem Haus gar nichts, nicht mal die Heizung",
        "Без электричества в нашем доме ничего не работает, даже отопление", "Без електрики в нашому будинку нічого не працює, навіть опалення",
        "Without electricity nothing works in our house, not even the heating", "Elektrik olmadan evimizde hiçbir şey çalışmıyor, kalorifer bile",
        "Bez elektryczności w naszym domu nic nie działa, nawet ogrzewanie", "Senza elettricità a casa nostra non funziona niente, neanche il riscaldamento",
        "Sin electricidad en casa no funciona nada, ni siquiera la calefacción", "Sans électricité, rien ne marche dans notre maison, même pas le chauffage",
        "Bez elektřiny u nás doma nic nefunguje, ani topení")),
    17794: (W + "; офис", ex("Diesen Monat müssen wir mit unseren Ressourcen sparsam umgehen",
        "В этом месяце нам нужно экономно расходовать наши средства", "Цього місяця нам треба економно витрачати наші ресурси",
        "This month we have to be careful with our resources", "Bu ay kaynaklarımızı idareli kullanmamız lazım",
        "W tym miesiącu musimy oszczędnie gospodarować zasobami", "Questo mese dobbiamo gestire con parsimonia le nostre risorse",
        "Este mes tenemos que ir con cuidado con nuestros recursos", "Ce mois-ci, on doit être économes avec nos ressources",
        "Tento měsíc musíme se svými prostředky šetřit")),
    17809: (W, ex("Von dem neuen Familienticket profitieren vor allem Eltern mit drei Kindern",
        "От нового семейного билета выигрывают прежде всего родители с тремя детьми", "Від нового сімейного квитка виграють насамперед батьки з трьома дітьми",
        "Parents with three children benefit most from the new family ticket", "Yeni aile biletinden en çok üç çocuklu ebeveynler yararlanıyor",
        "Na nowym bilecie rodzinnym korzystają przede wszystkim rodzice z trójką dzieci", "Del nuovo biglietto famiglia approfittano soprattutto i genitori con tre figli",
        "Del nuevo billete familiar se benefician sobre todo los padres con tres hijos", "Ce sont surtout les parents de trois enfants qui profitent du nouveau billet famille",
        "Z nové rodinné jízdenky profitují hlavně rodiče se třemi dětmi")),
    18208: (W, ex("Abends sitzen wir gern noch auf der Veranda und trinken Tee",
        "По вечерам мы любим посидеть на веранде за чаем", "Увечері ми любимо посидіти на веранді за чаєм",
        "In the evening we like to sit out on the veranda and drink tea", "Akşamları verandada oturup çay içmeyi seviyoruz",
        "Wieczorami lubimy jeszcze posiedzieć na werandzie przy herbacie", "La sera ci piace stare sulla veranda a bere il tè",
        "Por la tarde nos gusta sentarnos en la veranda a tomar té", "Le soir, on aime s'asseoir sur la véranda et boire du thé",
        "Večer rádi sedíme na verandě a pijeme čaj")),
    18211: (W, ex("Die Türklingel ist kaputt, klopf einfach laut",
        "Дверной звонок сломан, просто громко постучи", "Дверний дзвінок зламаний, просто голосно постукай",
        "The doorbell's broken, just knock loudly", "Kapı zili bozuk, sadece yüksek sesle kapıyı çal",
        "Dzwonek do drzwi jest zepsuty, po prostu głośno zapukaj", "Il campanello è rotto, bussa forte",
        "El timbre está roto, llama fuerte a la puerta", "La sonnette est cassée, frappe fort",
        "Zvonek je rozbitý, prostě nahlas zaklepej")),
    18231: (W, ex("Wo ist denn der Besen? Hier liegen überall Scherben",
        "А где веник? Тут повсюду осколки", "А де віник? Тут скрізь уламки",
        "Where's the broom? There's broken glass everywhere", "Süpürge nerede? Her yerde cam kırıkları var",
        "Gdzie jest miotła? Wszędzie leżą skorupy", "Dov'è la scopa? Ci sono cocci dappertutto",
        "¿Dónde está la escoba? Hay cristales por todas partes", "Où est le balai ? Il y a des éclats partout",
        "Kde je koště? Všude jsou střepy")),
    18243: (W + "; второе значение: жёлтая пресса", ex("Der Boulevard schreibt wieder nur Unsinn über Promis",
        "Жёлтая пресса опять пишет одну чушь про знаменитостей", "Жовта преса знову пише самі дурниці про знаменитостей",
        "The tabloids are writing nonsense about celebrities again", "Magazin basını yine ünlüler hakkında saçmalık yazıyor",
        "Brukowce znowu piszą same bzdury o celebrytach", "La stampa scandalistica scrive di nuovo solo sciocchezze sui vip",
        "La prensa amarilla vuelve a escribir tonterías sobre los famosos", "La presse à scandale raconte encore n'importe quoi sur les stars",
        "Bulvár zase píše jen nesmysly o celebritách")),
}

REPLACE = []

SPLIT_LATER = {}
