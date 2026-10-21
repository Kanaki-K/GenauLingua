"""B1, блок 5: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
SKEL = "пример-скелет («Das Monster ist sehr groß», «Der Richter ist sehr streng») — пусто"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    15946: (SKEL + "; шаблон streng", {**all_x(
        "Am Ende muss der Richter entscheiden", "В конце концов решать будет судья", "Зрештою вирішуватиме суддя",
        "In the end, it's up to the judge", "Sonunda karar hâkime kalıyor", "Ostatecznie zdecyduje sędzia",
        "Alla fine decide il giudice", "Al final decide el juez", "Au final, c'est le juge qui décide",
        "Nakonec rozhodne soudce")}),
    3045: ("«Der Krieg zerstörte die Stadt» — претерит, хроника; " + LIST, {
        "t_ru": "разрушать, уничтожать", "t_uk": "руйнувати, знищувати", "t_en": "to destroy, to ruin",
        "t_tr": "yok etmek, yıkmak", "t_pl": "niszczyć, burzyć",
        **all_x("Der Sturm hat unser Dach zerstört", "Буря разрушила нашу крышу", "Буря зруйнувала наш дах",
                "The storm destroyed our roof", "Fırtına çatımızı yıktı", "Burza zniszczyła nam dach",
                "La tempesta ci ha distrutto il tetto", "La tormenta destruyó nuestro tejado",
                "La tempête a détruit notre toit", "Bouřka nám zničila střechu")}),
    956: ("«Das dauert ungefähr eine Stunde» — шаблон mindestens («Das dauert mindestens zwei Stunden»)", {**all_x(
        "Wie viele Leute kommen? — Ungefähr zwanzig", "Сколько человек придёт? — Примерно двадцать",
        "Скільки людей прийде? — Приблизно двадцять", "How many people are coming? — About twenty",
        "Kaç kişi geliyor? — Aşağı yukarı yirmi", "Ile osób przyjdzie? — Około dwudziestu",
        "Quante persone vengono? — Circa venti", "¿Cuánta gente viene? — Más o menos veinte",
        "Combien de personnes viennent? — Environ vingt", "Kolik lidí přijde? — Asi dvacet")}),
    10111: (SKEL, {**all_x(
        "Mein Sohn hat Angst vor Monstern unter dem Bett", "Мой сын боится чудовищ под кроватью",
        "Мій син боїться чудовиськ під ліжком", "My son is scared of monsters under the bed",
        "Oğlum yatağın altındaki canavarlardan korkuyor", "Mój syn boi się potworów pod łóżkiem",
        "Mio figlio ha paura dei mostri sotto il letto", "Mi hijo tiene miedo de los monstruos debajo de la cama",
        "Mon fils a peur des monstres sous le lit", "Můj syn se bojí příšer pod postelí")}),
    15381: ("«Die Gegend hier ist schön» — пусто; " + LIST, {
        "t_ru": "район, местность", "t_uk": "місцевість, район", "t_en": "area, neighbourhood", "t_tr": "bölge, civar",
        "t_pl": "okolica",
        **all_x("Kennst du dich in der Gegend aus?", "Ты хорошо знаешь этот район?", "Ти добре знаєш цей район?",
                "Do you know your way around this area?", "Bu bölgeyi iyi biliyor musun?", "Znasz tę okolicę?",
                "Conosci bene la zona?", "¿Conoces bien la zona?", "Tu connais bien le coin?",
                "Vyznáš se v tomhle okolí?")}),
    2429: (LIST, {"t_ru": "узнавать, распознавать", "t_uk": "впізнавати, розпізнавати", "t_en": "to recognise, to realise",
                  "t_tr": "tanımak, fark etmek", "t_pl": "rozpoznawać, poznawać", "t_it": "riconoscere",
                  "t_es": "reconocer", "t_fr": "reconnaître", "t_cs": "poznat, rozpoznat",
                  "x_en": "I don't recognise you"}),
    1684: ("«Я сообщаю, что заболел» — калька; " + LIST, {
        "t_ru": "сообщать, дать о себе знать", "t_uk": "повідомляти, дати про себе знати", "t_en": "to report, to let know",
        "t_tr": "bildirmek, haber vermek", "t_pl": "zgłaszać, odezwać się", "t_it": "avvisare, farsi sentire",
        "t_es": "avisar, comunicar", "t_fr": "prévenir, signaler", "t_cs": "hlásit, ozvat se",
        **all_x("Melde dich, wenn du angekommen bist!", "Дай знать, когда доедешь!", "Дай знати, коли доїдеш!",
                "Let me know when you've arrived!", "Varınca haber ver!", "Odezwij się, jak dojedziesz!",
                "Fatti sentire quando arrivi!", "¡Avísame cuando llegues!", "Préviens-moi quand tu es arrivé!",
                "Ozvi se, až dorazíš!")}),
    1528: ("«Я должен это выяснить» — калька с muss", {"x_ru": "Мне нужно это выяснить", "x_en": "I need to find that out"}),
    998: ("«Ich sitze vorne» — шаблон vorn («Ich sitze vorn im Bus»)", {**all_x(
        "Bitte nach vorne durchgehen!", "Проходите, пожалуйста, вперёд!", "Проходьте, будь ласка, вперед!",
        "Please move down to the front!", "Lütfen öne doğru ilerleyin!", "Proszę przejść do przodu!",
        "Andate avanti, per favore!", "¡Pasen hacia delante, por favor!", "Avancez vers l'avant, s'il vous plaît!",
        "Postupte prosím dopředu!")}),
    10112: (LIST + "; «Ты ответственен за это» — книжно", {
        "t_ru": "ответственный", "t_uk": "відповідальний", "t_en": "responsible", "t_tr": "sorumlu",
        "t_pl": "odpowiedzialny", "x_ru": "Ты за это отвечаешь"}),
    10113: (LIST, {"t_ru": "тошно, скверный", "t_uk": "нудить, кепський", "t_en": "sick, nasty",
                   "t_tr": "midesi bulanmak, kötü", "t_pl": "niedobrze, paskudny", "t_it": "nauseato, cattivo",
                   "t_es": "con náuseas, malo", "t_fr": "mal, mauvais", "t_cs": "zle, zlý"}),
    8748: (LIST, {"t_ru": "позволить себе, выполнить", "t_uk": "дозволити собі, виконати", "t_en": "to afford, to accomplish",
                  "t_tr": "karşılamak, başarmak", "t_pl": "pozwolić sobie, dokonać", "t_it": "permettersi, compiere",
                  "t_es": "permitirse, rendir", "t_fr": "se permettre, accomplir", "t_cs": "dovolit si, vykonat",
                  "x_en": "I can't afford it"}),
    6392: ("«Ich nehme die Hälfte» — пусто", {**all_x(
        "Ich habe erst die Hälfte gelesen", "Я прочитал только половину", "Я прочитав лише половину",
        "I've only read half of it", "Daha yarısını okudum", "Przeczytałem dopiero połowę", "Ne ho letto solo la metà",
        "Solo he leído la mitad", "Je n'en ai lu que la moitié", "Přečetl jsem teprve polovinu")}),
    1807: ("«Я испытываю к нему уважение» — книжно; «опасение перед чем-то» — пояснение", {
        "t_ru": "уважение", "t_uk": "повага", "t_en": "respect", "t_tr": "saygı", "t_pl": "szacunek",
        "x_ru": "Я его очень уважаю", "x_uk": "Я його дуже поважаю"}),
    15382: ("«Hier ist eine Spur im Sand» — из детектива; полоса движения — то, что слышат каждый день", {
        "t_ru": "след, полоса", "t_uk": "слід, смуга", "t_en": "trace, lane", "t_tr": "iz, şerit", "t_pl": "ślad, pas ruchu",
        "t_it": "la traccia, la corsia", "t_es": "la huella, el carril", "t_fr": "la trace, la voie", "t_cs": "stopa, pruh",
        **all_x("Bleib auf der rechten Spur", "Держись правой полосы", "Тримайся правої смуги",
                "Stay in the right-hand lane", "Sağ şeritte kal", "Trzymaj się prawego pasa",
                "Resta sulla corsia di destra", "Quédate en el carril derecho", "Reste sur la voie de droite",
                "Zůstaň v pravém pruhu")}),
    1980: (LIST, {"t_ru": "брать на себя, перенимать", "t_uk": "брати на себе, переймати", "t_en": "to take over, to take on",
                  "t_tr": "üstlenmek, devralmak", "t_pl": "przejmować, brać na siebie", "t_it": "assumersi, rilevare",
                  "t_es": "asumir, hacerse cargo de", "t_fr": "assumer, prendre en charge", "t_cs": "převzít"}),
    2482: ("«Das macht mir große Freude» — книжно", {**all_x(
        "Er hat vor Freude geweint", "Он плакал от радости", "Він плакав від радості", "He cried with joy",
        "Sevinçten ağladı", "Płakał z radości", "Ha pianto di gioia", "Lloró de alegría", "Il a pleuré de joie",
        "Plakal radostí")}),
    11635: ("уровень: Abendessen — A1", {"level": "A1"}),
    13866: (LIST, {"t_ru": "субтитры", "t_uk": "субтитри"}),
    719: ("«Das ist eine gute Position» — пусто; " + LIST, {
        "t_ru": "должность, позиция", "t_uk": "посада, позиція", "t_en": "position, job", "t_tr": "pozisyon, konum",
        "t_pl": "stanowisko, pozycja", "t_it": "la posizione, il posto", "t_es": "el puesto, la posición",
        "t_fr": "le poste, la position", "t_cs": "pozice, místo",
        **all_x("Er hat eine neue Position in der Firma", "У него новая должность в фирме", "У нього нова посада у фірмі",
                "He has a new position in the company", "Şirkette yeni bir pozisyonu var", "Ma nowe stanowisko w firmie",
                "Ha una nuova posizione in azienda", "Tiene un nuevo puesto en la empresa",
                "Il a un nouveau poste dans l'entreprise", "Má ve firmě novou pozici")}),
    11636: ("«Хочешь напиток?» — так не предлагают", {"x_ru": "Хочешь коктейль?", "x_uk": "Хочеш коктейль?"}),
    9721: ("tr «temin etmem gerek» — канцелярски", {"x_tr": "Ekmek almam lazım", "x_en": "I need to get some bread"}),
    10119: ("«У нас большие трудности» — пусто", {**all_x(
        "Hast du Schwierigkeiten mit der Aussprache?", "У тебя трудности с произношением?", "У тебе труднощі з вимовою?",
        "Are you having difficulty with the pronunciation?", "Telaffuzda zorluk çekiyor musun?",
        "Masz trudności z wymową?", "Hai difficoltà con la pronuncia?", "¿Tienes dificultades con la pronunciación?",
        "Tu as des difficultés avec la prononciation?", "Máš potíže s výslovností?")}),
    6398: (LIST, {"t_ru": "быть верным, голосовать", "t_uk": "бути правильним, голосувати", "t_en": "to be right, to vote",
                  "t_tr": "doğru olmak, oy vermek", "t_pl": "zgadzać się, głosować", "t_it": "essere giusto, votare",
                  "t_es": "ser correcto, votar", "t_fr": "être juste, voter", "t_cs": "sedět, hlasovat",
                  "x_en": "The numbers don't add up"}),
}

# nahe — то же слово, что nah; vorne — то же, что vorn
REPLACE = [
    {"id": 6387, "by": 1717, "lang": "de", "why": "nahe — вариант того же nah"},
    {"id": 998, "by": 6524, "lang": "de", "why": "vorne — вариант того же vorn"},
]

SPLIT_LATER = {}
