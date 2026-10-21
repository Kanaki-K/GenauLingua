"""B1, блок 7: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
SKEL = "пример-скелет («Das Dach ist neu», «Der Stein ist sehr schwer») — пусто"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    18124: (SKEL, {**all_x(
        "Wir wohnen direkt unterm Dach", "Мы живём прямо под крышей", "Ми живемо просто під дахом",
        "We live right under the roof", "Tam çatı katında oturuyoruz", "Mieszkamy tuż pod dachem",
        "Abitiamo proprio sotto il tetto", "Vivimos justo debajo del tejado", "On habite juste sous le toit",
        "Bydlíme přímo pod střechou")}),
    12481: ("«Das Gehirn ist sehr wichtig» — школьный плакат", {**all_x(
        "Schalt mal dein Gehirn ein!", "Включи мозги!", "Увімкни мізки!", "Use your brain!", "Biraz beynini kullan!",
        "Włącz mózg!", "Accendi il cervello!", "¡Usa el cerebro!", "Fais marcher ton cerveau!", "Zapni mozek!")}),
    2034: ("«Ich verbringe viel Zeit hier» — пусто", {**all_x(
        "Wo verbringt ihr den Urlaub?", "Где вы проводите отпуск?", "Де ви проводите відпустку?",
        "Where are you spending your holiday?", "Tatili nerede geçiriyorsunuz?", "Gdzie spędzacie urlop?",
        "Dove passate le vacanze?", "¿Dónde pasáis las vacaciones?", "Où est-ce que vous passez les vacances?",
        "Kde trávíte dovolenou?")}),
    6432: ("ru «Это же безумие!» — тот же пример, что у irre", {**all_x(
        "Bei dieser Hitze joggen? Das ist Wahnsinn!", "Бегать в такую жару? Это безумие!",
        "Бігати в таку спеку? Це божевілля!", "Jogging in this heat? That's madness!",
        "Bu sıcakta koşmak mı? Bu delilik!", "Biegać w taki upał? To szaleństwo!",
        "Correre con questo caldo? È una follia!", "¿Correr con este calor? ¡Es una locura!",
        "Courir par cette chaleur? C'est de la folie!", "Běhat v tomhle vedru? To je šílenství!")}),
    2696: ("«Das ist offenbar ein Fehler» — шаблон offensichtlich («Das ist offensichtlich falsch»)", {
        "t_ru": "видимо, очевидно", "t_uk": "мабуть, очевидно", "t_en": "apparently, evidently",
        "t_tr": "anlaşılan, görünüşe göre", "t_pl": "najwyraźniej, widocznie", "t_it": "a quanto pare, evidentemente",
        "t_es": "al parecer, evidentemente", "t_fr": "apparemment, manifestement", "t_cs": "zřejmě, očividně",
        **all_x("Er hat offenbar keine Lust", "У него, видимо, нет желания", "Він, мабуть, не хоче",
                "He apparently doesn't feel like it", "Anlaşılan canı istemiyor", "Najwyraźniej nie ma ochoty",
                "A quanto pare non ne ha voglia", "Al parecer no tiene ganas", "Apparemment, il n'a pas envie",
                "Zřejmě se mu nechce")}),
    15390: ("второе значение — непристойность, учебной карточке не нужно", {
        "t_ru": "хвост", "t_uk": "хвіст", "t_en": "tail", "t_tr": "kuyruk", "t_pl": "ogon"}),
    18619: ("en «He was still here earlier» — «только что» потеряно", {"x_en": "He was here just a moment ago"}),
    15393: (SKEL + "; " + LIST, {
        "t_ru": "камень, косточка", "t_uk": "камінь, кісточка", "t_en": "stone, rock", "t_tr": "taş", "t_pl": "kamień, pestka",
        **all_x("Ich habe einen Stein im Schuh", "У меня камешек в ботинке", "У мене камінь у черевику",
                "I've got a stone in my shoe", "Ayakkabımda taş var", "Mam kamień w bucie", "Ho un sasso nella scarpa",
                "Tengo una piedra en el zapato", "J'ai un caillou dans la chaussure", "Mám v botě kámen")}),
    1770: ("«Das ist prima» — пусто; «Prima, dann sehen wir uns morgen» — шаблон super", {**all_x(
        "Das Essen war prima!", "Еда была отличная!", "Їжа була чудова!", "The food was great!", "Yemek harikaydı!",
        "Jedzenie było świetne!", "Il cibo era ottimo!", "¡La comida estaba genial!", "Le repas était super!",
        "Jídlo bylo prima!")}),
    6442: ("«Шар катится по полу» — пусто; в жизни Kugel — шарик мороженого", {
        "t_ru": "шар, шарик (мороженого)", "t_uk": "куля, кулька", "t_en": "ball, scoop", "t_tr": "küre, top",
        "t_pl": "kula, gałka", "t_it": "la palla, la pallina", "t_es": "la bola", "t_fr": "la boule",
        "t_cs": "koule, kulička",
        **all_x("Zwei Kugeln Vanille, bitte", "Два шарика ванильного, пожалуйста", "Дві кульки ванільного, будь ласка",
                "Two scoops of vanilla, please", "İki top vanilya lütfen", "Dwie gałki waniliowych poproszę",
                "Due palline di vaniglia, per favore", "Dos bolas de vainilla, por favor",
                "Deux boules de vanille, s'il vous plaît", "Dvě kuličky vanilkové, prosím")}),
    1447: ("«Die Maschine funktioniert nicht» — шаблон System, Heizung", {**all_x(
        "Wie funktioniert das?", "Как это работает?", "Як це працює?", "How does it work?", "Bu nasıl çalışıyor?",
        "Jak to działa?", "Come funziona?", "¿Cómo funciona?", "Comment ça marche?", "Jak to funguje?")}),
    1908: (LIST, {"t_ru": "подниматься, расти", "t_uk": "підніматися, зростати", "t_en": "to rise, to climb",
                  "t_tr": "yükselmek, artmak", "t_pl": "wzrastać, rosnąć", "t_it": "salire, aumentare",
                  "t_es": "subir, aumentar", "t_fr": "monter, augmenter", "t_cs": "stoupat, růst"}),
    14377: ("«Der Prinz lebt im Schloss» — сказка", {**all_x(
        "Sie wartet auf ihren Prinzen", "Она ждёт своего принца", "Вона чекає свого принца",
        "She's waiting for her prince", "Prensini bekliyor", "Czeka na swojego księcia", "Aspetta il suo principe",
        "Espera a su príncipe", "Elle attend son prince", "Čeká na svého prince")}),
}

SPLIT_LATER = {}
