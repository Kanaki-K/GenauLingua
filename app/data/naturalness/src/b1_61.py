"""B1, блок 61: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    2221: (EN, {"x_en": "We're sharing out the work"}),
    16278: ("«Die Mehrheit der Schüler möchte in die Pause gehen» — так не говорят", {**all_x(
        "Die Mehrheit ist dafür", "Большинство за", "Більшість за", "The majority is in favour", "Çoğunluk lehte",
        "Większość jest za", "La maggioranza è a favore", "La mayoría está a favor", "La majorité est pour", "Většina je pro")}),
    11753: ("«Diese Frucht schmeckt sehr süß und saftig» — пусто; в речи — «Früchte tragen»", {**all_x(
        "Die Mühe hat endlich Früchte getragen", "Усилия наконец принесли плоды", "Зусилля нарешті принесли плоди",
        "The effort has finally borne fruit", "Emek sonunda meyvesini verdi", "Wysiłek w końcu przyniósł owoce",
        "Lo sforzo ha finalmente dato i suoi frutti", "El esfuerzo por fin ha dado sus frutos",
        "L'effort a enfin porté ses fruits", "Úsilí konečně přineslo plody")}),
    2373: ("«Diebe wollten bei uns einbrechen» — претерит", {**all_x(
        "Bei uns ist eingebrochen worden", "К нам вломились воры", "До нас вломилися злодії",
        "Someone's broken into our place", "Evimize hırsız girdi", "Ktoś się do nas włamał", "Ci hanno svaligiato la casa",
        "Han entrado a robar en nuestra casa", "On s'est fait cambrioler", "Někdo se k nám vloupal")}),
    18246: ("«Sie sitzen auf der Terrasse» — пусто", {**all_x(
        "Bei schönem Wetter frühstücken wir auf der Terrasse", "В хорошую погоду мы завтракаем на террасе",
        "У гарну погоду ми снідаємо на терасі", "When the weather's nice we have breakfast on the terrace",
        "Hava güzel olunca terasta kahvaltı ediyoruz", "Przy ładnej pogodzie jemy śniadanie na tarasie",
        "Col bel tempo facciamo colazione in terrazza", "Cuando hace buen tiempo desayunamos en la terraza",
        "Quand il fait beau, on prend le petit-déjeuner sur la terrasse", "Za hezkého počasí snídáme na terase")}),
    16281: ("снова Projekt", {**all_x(
        "Lass uns abstimmen, wohin wir fahren", "Давайте проголосуем, куда поедем", "Давайте проголосуємо, куди поїдемо",
        "Let's vote on where we go", "Nereye gideceğimizi oylayalım", "Zagłosujmy, dokąd jedziemy", "Votiamo dove andare",
        "Votemos adónde vamos", "Votons pour savoir où on va", "Pojďme hlasovat, kam pojedeme")}),
    2193: ("«Die Krankheit ist ansteckend» — пусто", {**all_x(
        "Dein Lachen ist ansteckend", "Твой смех заразный", "Твій сміх заразний", "Your laugh is contagious",
        "Gülüşün bulaşıcı", "Twój śmiech jest zaraźliwy", "La tua risata è contagiosa", "Tu risa es contagiosa",
        "Ton rire est contagieux", "Tvůj smích je nakažlivý")}),
    17178: ("«Die Bremse funktioniert nicht richtig» — шаблон versagen («Die Bremsen haben versagt»)", {**all_x(
        "Tritt auf die Bremse!", "Жми на тормоз!", "Тисни на гальмо!", "Hit the brakes!", "Frene bas!",
        "Naciśnij hamulec!", "Pigia sul freno!", "¡Pisa el freno!", "Appuie sur le frein!", "Šlápni na brzdu!")}),
    2647: ("ru «Меня одолевает скука» — книжно", {**all_x(
        "Ich sterbe vor Langeweile", "Я умираю от скуки", "Я помираю від нудьги", "I'm dying of boredom",
        "Can sıkıntısından ölüyorum", "Umieram z nudów", "Muoio di noia", "Me muero de aburrimiento", "Je meurs d'ennui",
        "Umírám nudou")}),
    2020: ("«Die Blumen sind in der Vase» — пусто", {**all_x(
        "Stell die Blumen in eine Vase", "Поставь цветы в вазу", "Постав квіти у вазу", "Put the flowers in a vase",
        "Çiçekleri vazoya koy", "Wstaw kwiaty do wazonu", "Metti i fiori in un vaso", "Pon las flores en un jarrón",
        "Mets les fleurs dans un vase", "Dej květiny do vázy")}),
    2606: (LIST + " (было семь значений)", {
        "t_ru": "опрокидывать, наклонять", "t_uk": "перевертати, нахиляти", "t_en": "to tip over, to tilt",
        "t_tr": "devirmek, eğmek", "t_pl": "przewracać, przechylać", "t_it": "rovesciare, inclinare",
        "t_es": "volcar, inclinar", "t_fr": "renverser, basculer", "t_cs": "převrhnout, naklonit"}),
    10657: ("пример многословный", {**all_x(
        "Du hast mir einen ganz schönen Schreck eingejagt!", "Ты нагнал на меня страху!", "Ти нагнав на мене страху!",
        "You gave me quite a fright!", "Beni çok korkuttun!", "Ale mi napędziłeś strachu!", "Mi hai fatto prendere uno spavento!",
        "¡Menudo susto me has dado!", "Tu m'as fait une de ces peurs!", "Ty jsi mi nahnal úlek!")}),
    388: ("«Wir haben ein Haustier zu Hause» — пусто", {**all_x(
        "Habt ihr Haustiere?", "У вас есть домашние животные?", "У вас є домашні тварини?", "Do you have any pets?",
        "Evcil hayvanınız var mı?", "Macie zwierzęta domowe?", "Avete animali domestici?", "¿Tenéis mascotas?",
        "Vous avez des animaux de compagnie?", "Máte domácí zvířata?")}),
    2265: ("«Die Belastung ist zu hoch» — пусто; " + LIST + " (было семь значений)", {
        "t_ru": "нагрузка, бремя", "t_uk": "навантаження, тягар", "t_en": "burden, strain", "t_tr": "yük, stres",
        "t_pl": "obciążenie, ciężar",
        **all_x("Die Pflege der Mutter ist eine große Belastung für sie", "Уход за матерью для неё большая нагрузка",
                "Догляд за матір'ю для неї великий тягар", "Caring for her mother is a heavy burden for her",
                "Annesinin bakımı onun için büyük bir yük", "Opieka nad matką to dla niej duże obciążenie",
                "Accudire la madre è un grosso peso per lei", "Cuidar de su madre es una gran carga para ella",
                "S'occuper de sa mère est une lourde charge pour elle", "Péče o matku je pro ni velká zátěž")}),
    1295: ("«Der Briefkasten ist voll» — пусто; en «mailbox»", {"t_en": "letterbox, postbox", **all_x(
        "Wirf den Brief bitte in den Briefkasten", "Брось, пожалуйста, письмо в почтовый ящик", "Кинь, будь ласка, лист у поштову скриньку",
        "Put the letter in the letterbox, please", "Mektubu lütfen posta kutusuna at", "Wrzuć, proszę, list do skrzynki pocztowej",
        "Metti la lettera nella cassetta delle lettere", "Echa la carta al buzón, por favor",
        "Mets la lettre dans la boîte aux lettres, s'il te plaît", "Hoď prosím ten dopis do schránky")}),
    15087: ("«Meine Schwägerin ist nett» — пусто, шаблон Schwager; " + LIST, {
        "t_ru": "невестка, золовка", "t_uk": "невістка, зовиця",
        **all_x("Meine Schwägerin und ich verstehen uns super", "Мы с невесткой отлично ладим",
                "Ми з невісткою чудово ладнаємо", "My sister-in-law and I get on really well",
                "Yengemle çok iyi anlaşıyoruz", "Świetnie dogaduję się ze szwagierką",
                "Io e mia cognata andiamo d'accordissimo", "Mi cuñada y yo nos llevamos genial",
                "Ma belle-sœur et moi, on s'entend super bien", "Se švagrovou si skvěle rozumíme")}),
    16294: ("«… hat neue Gesetze verabschiedet» — шаблон Bund", {**all_x(
        "Das Parlament stimmt morgen über das Gesetz ab", "Парламент завтра голосует по закону", "Парламент завтра голосує за закон",
        "Parliament votes on the law tomorrow", "Meclis yarın yasayı oylayacak", "Parlament jutro głosuje nad ustawą",
        "Il parlamento vota la legge domani", "El parlamento vota mañana la ley", "Le parlement vote la loi demain",
        "Parlament zítra hlasuje o zákoně")}),
    7340: ("ru «Ты должен применить … в своём проекте» — калька, Projekt", {**all_x(
        "Wie wendet man diese Creme an?", "Как применять этот крем?", "Як застосовувати цей крем?", "How do you use this cream?",
        "Bu krem nasıl uygulanıyor?", "Jak stosować ten krem?", "Come si applica questa crema?", "¿Cómo se aplica esta crema?",
        "Comment on applique cette crème?", "Jak se tenhle krém používá?")}),
    8934: ("«Morgen halte ich eine Präsentation …» — шаблон Vortrag", {**all_x(
        "Die Präsentation ist super gelaufen", "Презентация прошла отлично", "Презентація пройшла чудово",
        "The presentation went really well", "Sunum harika geçti", "Prezentacja poszła świetnie",
        "La presentazione è andata benissimo", "La presentación salió genial", "La présentation s'est super bien passée",
        "Prezentace dopadla skvěle")}),
    1101: (LIST, {"t_ru": "снимать (деньги), взлетать", "t_uk": "знімати (гроші), злітати", "t_en": "to withdraw, to take off",
                  "t_tr": "para çekmek, havalanmak", "t_pl": "wypłacać, startować", "t_it": "prelevare, decollare",
                  "t_es": "sacar, despegar", "t_fr": "retirer, décoller", "t_cs": "vybrat, vzlétnout"}),
    693: ("«Die Packung ist leer» — пусто", {**all_x(
        "Mach die Packung bitte wieder zu", "Закрой, пожалуйста, упаковку обратно", "Закрий, будь ласка, упаковку назад",
        "Please close the packet again", "Paketi lütfen tekrar kapat", "Zamknij, proszę, opakowanie z powrotem",
        "Richiudi la confezione, per favore", "Vuelve a cerrar el paquete, por favor", "Referme le paquet, s'il te plaît",
        "Zavři prosím zase to balení")}),
}

SPLIT_LATER = {}
