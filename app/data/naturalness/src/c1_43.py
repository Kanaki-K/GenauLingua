"""C1, блок 43 (последний в C1): 9 строк. Вычитано вручную 22.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"
EMPTY = "пример пустой, ничего о жизни"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    16929: ("пусто; " + LIST, {
        "t_ru": "вызывать (в суд)", "t_uk": "викликати (до суду)", "t_en": "to summon", "t_tr": "mahkemeye çağırmak", "t_pl": "wezwać (do sądu)",
        "t_fr": "citer, convoquer",
        **all_x("Wegen des Auffahrunfalls hat mich das Gericht als Zeugin vorgeladen, jetzt muss ich mir freinehmen",
                "Из-за той аварии суд вызвал меня свидетельницей — теперь придётся брать выходной",
                "Через ту аварію суд викликав мене свідкинею — тепер доведеться брати вихідний",
                "The court has summoned me as a witness to the rear-end collision, so now I have to take a day off",
                "Arkadan çarpma kazası yüzünden mahkeme beni tanık olarak çağırdı, şimdi izin almam gerekiyor",
                "Przez tę stłuczkę sąd wezwał mnie na świadka, teraz muszę wziąć wolne",
                "Per quel tamponamento il tribunale mi ha citata come testimone, ora devo prendermi un giorno libero",
                "Por el choque por alcance el juzgado me ha citado como testigo, y ahora tengo que pedirme el día libre",
                "À cause de l'accrochage, le tribunal m'a citée comme témoin, maintenant je dois prendre un jour de congé",
                "Kvůli té bouračce mě soud předvolal jako svědkyni, teď si musím vzít volno")}),
    15324: ("претерит; «чресла» — книжное; живое — кухня; " + LIST, {
        "t_ru": "вырезка, поясница", "t_uk": "вирізка, поперек", "t_en": "loin, tenderloin", "t_tr": "bonfile, bel", "t_pl": "polędwica, lędźwie",
        "t_it": "il lombo, il filetto", "t_es": "el lomo, la zona lumbar", "t_fr": "la longe, les reins", "t_cs": "svíčková, bedra",
        **all_x("Zum Geburtstag brate ich eine Schweinelende mit Pilzsoße",
                "На день рождения я жарю свиную вырезку с грибным соусом",
                "На день народження я смажу свинячу вирізку з грибним соусом",
                "For the birthday I'm roasting a pork loin with mushroom sauce",
                "Doğum günü için mantar soslu domuz bonfile kızartıyorum",
                "Na urodziny piekę polędwicę wieprzową w sosie grzybowym",
                "Per il compleanno preparo un lombo di maiale con salsa ai funghi",
                "Para el cumpleaños hago un lomo de cerdo con salsa de setas",
                "Pour l'anniversaire, je fais rôtir une longe de porc sauce aux champignons",
                "K narozeninám peču vepřovou svíčkovou s houbovou omáčkou")}),
    8647: ("канцелярит; рядом Ziel 3047; " + LIST, {
        "t_ru": "добиваться, иметь целью", "t_uk": "домагатися, мати на меті", "t_en": "to aim at, to be after", "t_tr": "amaçlamak", "t_pl": "mieć na celu, zmierzać do",
        **all_x("Was bezweckst du eigentlich mit diesen ganzen Fragen?",
                "Чего ты вообще добиваешься всеми этими вопросами?",
                "Чого ти взагалі домагаєшся всіма цими питаннями?",
                "What are you actually after with all these questions?",
                "Bütün bu sorularla aslında neyi amaçlıyorsun?",
                "Do czego właściwie zmierzasz tymi wszystkimi pytaniami?",
                "Ma a che cosa miri con tutte queste domande?",
                "¿Qué pretendes en realidad con todas estas preguntas?",
                "Qu'est-ce que tu vises au juste avec toutes ces questions ?",
                "Co vlastně sleduješ všemi těmi otázkami?")}),
    16936: ("претерит trafen; дубль C2 16987; " + LIST, {
        "t_ru": "посланник, посол", "t_uk": "посланець, посол", "t_en": "envoy", "t_tr": "elçi", "t_pl": "wysłannik, poseł",
        "t_it": "l'inviato", "t_es": "el enviado", "t_fr": "l'envoyé", "t_cs": "vyslanec",
        **all_x("Im Schloss zeigt die Führerin den Saal, in dem der König die Gesandten empfangen hat",
                "В замке экскурсовод показывает зал, где король принимал посланников",
                "У замку екскурсоводка показує зал, де король приймав посланців",
                "At the castle the guide shows the hall where the king received the envoys",
                "Şatoda rehber, kralın elçileri kabul ettiği salonu gösteriyor",
                "W zamku przewodniczka pokazuje salę, w której król przyjmował posłów",
                "Nel castello la guida mostra la sala in cui il re riceveva gli inviati",
                "En el castillo la guía enseña la sala donde el rey recibía a los enviados",
                "Au château, la guide montre la salle où le roi recevait les envoyés",
                "Na zámku průvodkyně ukazuje sál, kde král přijímal vyslance")}),
    13156: ("претерит; диагноз → живое переносное «противоречиво»", {
        "t_ru": "шизофренический, абсурдно противоречивый", "t_uk": "шизофренічний, абсурдно суперечливий", "t_en": "schizophrenic, absurdly contradictory", "t_tr": "şizofrenik, çelişkili", "t_pl": "schizofreniczny, absurdalnie sprzeczny",
        **all_x("Es ist doch schizophren: Wir fahren mit dem Auto ins Fitnessstudio, um dort aufs Laufband zu gehen",
                "Это же абсурд: мы едем в фитнес-клуб на машине, чтобы там встать на беговую дорожку",
                "Це ж абсурд: ми їдемо до фітнес-клубу машиною, щоб там стати на бігову доріжку",
                "It's schizophrenic, really: we drive to the gym to go on the treadmill",
                "Düpedüz çelişkili: koşu bandına çıkmak için spor salonuna arabayla gidiyoruz",
                "To przecież schizofreniczne: jedziemy samochodem na siłownię, żeby tam wejść na bieżnię",
                "È proprio schizofrenico: andiamo in palestra in macchina per salire sul tapis roulant",
                "Es esquizofrénico: vamos en coche al gimnasio para subirnos a la cinta de correr",
                "C'est quand même schizophrène : on va à la salle de sport en voiture pour monter sur le tapis de course",
                "Je to vlastně schizofrenní: jedeme autem do posilovny, abychom tam šli na běžecký pás")}),
    14835: ("en movie/store → британское", {
        "t_en": "video shop, video rental shop",
        "x_en": "We used to rent a film from the video shop every Friday"}),
    11602: ("война → живое «ist mir ein Gräuel»; рядом Ekel 10784; " + LIST, {
        "t_ru": "ужас, мерзость", "t_uk": "жах, мерзота", "t_en": "horror, abomination", "t_tr": "dehşet, nefret edilen şey", "t_pl": "zgroza, okropność",
        **all_x("Bügeln ist mir ein Gräuel, deshalb kaufe ich nur Hemden, die nicht knittern",
                "Гладить для меня сущий ужас, поэтому я покупаю только немнущиеся рубашки",
                "Прасувати для мене — справжній жах, тому я купую лише сорочки, що не мнуться",
                "Ironing is a horror to me, so I only buy shirts that don't crease",
                "Ütü yapmak benim için tam bir dehşet, o yüzden sadece buruşmayan gömlekler alıyorum",
                "Prasowanie to dla mnie zgroza, dlatego kupuję tylko niegniotące się koszule",
                "Stirare per me è un orrore, perciò compro solo camicie che non si stropicciano",
                "Planchar es para mí un horror, por eso solo compro camisas que no se arrugan",
                "Repasser, c'est une horreur pour moi, alors je n'achète que des chemises infroissables",
                "Žehlení je pro mě hrůza, proto kupuju jen nemačkavé košile")}),
    16988: ("пусто; рядом Behörde 1238; " + LIST, {
        "t_ru": "власти, начальство", "t_uk": "влада, начальство", "t_en": "the authorities, the powers that be", "t_tr": "yetkililer, üst makam", "t_pl": "władza, zwierzchność",
        "t_cs": "vrchnost, úřady",
        **all_x("Mein Opa hat vor der Obrigkeit nie viel Respekt gehabt, nicht mal vor dem Pfarrer",
                "Мой дед никогда особо не уважал начальство, даже священника",
                "Мій дід ніколи особливо не поважав начальство, навіть священника",
                "My grandad never had much respect for the powers that be, not even the vicar",
                "Dedemin yetkililere hiç pek saygısı olmadı, papaza bile",
                "Mój dziadek nigdy nie miał wielkiego szacunku dla władzy, nawet dla proboszcza",
                "Mio nonno non ha mai avuto molto rispetto per le autorità, neanche per il parroco",
                "Mi abuelo nunca ha tenido mucho respeto por las autoridades, ni siquiera por el cura",
                "Mon grand-père n'a jamais eu beaucoup de respect pour les autorités, même pas pour le curé",
                "Můj děda nikdy neměl moc respekt před vrchností, ani před farářem")}),
    11618: ("претерит; рядом ehrlich 10048; " + LIST, {
        "t_ru": "порядочный, честный", "t_uk": "порядний, чесний", "t_en": "upright, honest", "t_tr": "dürüst, doğru", "t_pl": "prawy, uczciwy",
        "t_cs": "poctivý, čestný",
        **all_x("Der Taxifahrer ist ein rechtschaffener Mensch, er hat mir mein Handy sofort zurückgebracht",
                "Таксист — порядочный человек: он сразу вернул мне телефон",
                "Таксист — порядна людина: він одразу повернув мені телефон",
                "The taxi driver is an upright man — he brought my phone straight back to me",
                "Taksici dürüst bir insan, telefonumu hemen geri getirdi",
                "Taksówkarz to prawy człowiek, od razu oddał mi telefon",
                "Il tassista è una persona onesta, mi ha riportato subito il telefono",
                "El taxista es un hombre honrado, me ha devuelto el móvil enseguida",
                "Le chauffeur de taxi est un homme intègre, il m'a tout de suite rapporté mon portable",
                "Taxikář je poctivý člověk, hned mi vrátil mobil")}),
}

REPLACE = []

SPLIT_LATER = {}
