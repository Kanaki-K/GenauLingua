"""B1, блок 46: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    16114: ("«Die Vergewaltigung war …» — претерит; общее утверждение — настоящее время", {**all_x(
        "Vergewaltigung ist ein schweres Verbrechen", "Изнасилование — тяжкое преступление", "Зґвалтування — тяжкий злочин",
        "Rape is a serious crime", "Tecavüz ağır bir suçtur", "Gwałt to ciężkie przestępstwo", "Lo stupro è un reato grave",
        "La violación es un delito grave", "Le viol est un crime grave", "Znásilnění je závažný trestný čin")}),
    1150: ("«Bitte folge den Anweisungen» — табличка; " + LIST, {
        "t_ru": "указание, инструкция", "t_uk": "вказівка, інструкція", "t_en": "instruction, directive",
        "t_tr": "talimat, yönerge", "t_pl": "wskazówka, polecenie", "t_it": "l'istruzione, l'indicazione",
        "t_es": "la instrucción, la indicación", "t_fr": "l'instruction, la consigne", "t_cs": "pokyn, instrukce",
        **all_x("Halt dich genau an die Anweisungen vom Arzt", "Строго соблюдай указания врача", "Чітко дотримуйся вказівок лікаря",
                "Follow the doctor's instructions exactly", "Doktorun talimatlarına harfiyen uy",
                "Trzymaj się dokładnie wskazówek lekarza", "Segui alla lettera le indicazioni del medico",
                "Sigue al pie de la letra las indicaciones del médico", "Suis exactement les consignes du médecin",
                "Drž se přesně pokynů lékaře")}),
    16115: ("«Der Abzug der Truppen …» — хроника; " + LIST + " (было шесть значений)", {
        "t_ru": "вычет, спусковой крючок", "t_uk": "відрахування, спусковий гачок", "t_en": "deduction, trigger",
        "t_tr": "kesinti, tetik", "t_pl": "potrącenie, spust", "t_it": "la detrazione, il grilletto",
        "t_es": "la deducción, el gatillo", "t_fr": "la déduction, la détente", "t_cs": "srážka, spoušť",
        **all_x("Nach Abzug der Steuern bleibt nicht viel übrig", "После вычета налогов остаётся немного",
                "Після відрахування податків лишається небагато", "After deduction of tax there isn't much left",
                "Vergi kesintisinden sonra pek bir şey kalmıyor", "Po potrąceniu podatków niewiele zostaje",
                "Dopo la detrazione delle tasse non resta molto", "Tras la deducción de impuestos no queda mucho",
                "Après déduction des impôts, il ne reste pas grand-chose", "Po srážce daní moc nezbude")}),
    6995: ("«Er kniet nieder und bittet um Vergebung» — книжно", {**all_x(
        "Er kniet sich hin und macht ihr einen Antrag", "Он встаёт на колено и делает ей предложение",
        "Він стає на коліно й робить їй пропозицію", "He kneels down and proposes to her",
        "Diz çöküp ona evlenme teklif ediyor", "Klęka i oświadcza się jej", "Si inginocchia e le chiede di sposarlo",
        "Se arrodilla y le pide matrimonio", "Il s'agenouille et la demande en mariage", "Poklekne a požádá ji o ruku")}),
    13983: ("«Der Tiger brüllt laut im Zoo» — шаблон Tiger", {**all_x(
        "Brüll nicht so, ich bin nicht taub!", "Не ори так, я не глухой!", "Не горлай так, я не глухий!",
        "Don't yell like that, I'm not deaf!", "Böyle bağırma, sağır değilim!", "Nie wrzeszcz tak, nie jestem głuchy!",
        "Non urlare così, non sono sordo!", "¡No grites así, que no estoy sordo!", "Ne hurle pas comme ça, je ne suis pas sourd!",
        "Neřvi tak, nejsem hluchý!")}),
    16116: ("«Der Sprengstoff wurde von der Polizei gefunden» — претерит, хроника", {**all_x(
        "Spürhunde können Sprengstoff riechen", "Служебные собаки чуют взрывчатку", "Службові собаки чують вибухівку",
        "Sniffer dogs can smell explosives", "Arama köpekleri patlayıcıların kokusunu alabilir",
        "Psy tropiące wyczuwają materiały wybuchowe", "I cani antiesplosivo fiutano l'esplosivo",
        "Los perros rastreadores huelen los explosivos", "Les chiens renifleurs sentent les explosifs",
        "Služební psi dokážou ucítit výbušniny")}),
    11695: ("убрать пометку (colloq.)", {"t_it": "la gomma da masticare, la cicca"}),
    17523: (LIST, {"t_ru": "профиль, протектор", "t_uk": "профіль, протектор", "t_en": "profile, tread",
                   "t_tr": "profil, lastik dişi"}),
    6998: (LIST + " (было шесть значений)", {
        "t_ru": "фиксировать, осознать", "t_uk": "фіксувати, усвідомити", "t_en": "to record, to grasp",
        "t_tr": "kaydetmek, kavramak", "t_pl": "rejestrować, pojąć", "t_it": "registrare, afferrare",
        "t_es": "registrar, comprender", "t_fr": "enregistrer, saisir", "t_cs": "zachytit, pochopit"}),
    1817: ("«Der Saal ist groß» — пусто", {**all_x(
        "Der Saal war bis auf den letzten Platz voll", "Зал был полон до последнего места", "Зала була заповнена до останнього місця",
        "The hall was packed to the last seat", "Salon son koltuğuna kadar doluydu", "Sala była wypełniona do ostatniego miejsca",
        "La sala era piena fino all'ultimo posto", "La sala estaba llena hasta el último asiento",
        "La salle était pleine jusqu'à la dernière place", "Sál byl plný do posledního místa")}),
    260: ("убрать пометку (hovor.); " + LIST, {"t_en": "end of the working day, knocking-off time",
                                              "t_ru": "конец рабочего дня", "t_uk": "кінець робочого дня",
                                              "t_cs": "konec práce, padla", "x_en": "Work's over! Let's go"}),
    9773: ("«Meine Handtasche ist rot» — пусто", {**all_x(
        "In ihrer Handtasche findet sie nie etwas", "В своей сумочке она никогда ничего не может найти",
        "У своїй сумочці вона ніколи нічого не може знайти", "She can never find anything in her handbag",
        "El çantasında hiçbir şey bulamıyor", "W swojej torebce nigdy nic nie może znaleźć",
        "Nella sua borsetta non trova mai niente", "En su bolso nunca encuentra nada",
        "Elle ne trouve jamais rien dans son sac à main", "Ve své kabelce nikdy nic nenajde")}),
    7000: ("«Die Daten sind geschützt» — пусто", {**all_x(
        "Hier bist du vor dem Regen geschützt", "Здесь ты защищён от дождя", "Тут ти захищений від дощу",
        "You're protected from the rain here", "Burada yağmurdan korunursun", "Tu jesteś chroniony przed deszczem",
        "Qui sei protetto dalla pioggia", "Aquí estás protegido de la lluvia", "Ici, tu es protégé de la pluie",
        "Tady jsi chráněný před deštěm")}),
    10415: ("«Das Wetter ist erbärmlich» — снова погода", {**all_x(
        "Er hat sich erbärmlich benommen", "Он вёл себя отвратительно", "Він поводився жалюгідно",
        "His behaviour was pitiful", "Berbat davrandı", "Zachował się żałośnie", "Si è comportato in modo pietoso",
        "Se comportó de forma lamentable", "Il s'est comporté de façon lamentable", "Choval se ubohým způsobem")}),
    2336: ("«Deutschland ist eine Demokratie» — шаблон Republik («Deutschland ist eine Republik»)", {**all_x(
        "In einer Demokratie darf jeder seine Meinung sagen", "В демократии каждый может высказывать своё мнение",
        "У демократії кожен може висловлювати свою думку", "In a democracy everyone can say what they think",
        "Demokraside herkes fikrini söyleyebilir", "W demokracji każdy może mówić, co myśli",
        "In democrazia ognuno può dire la sua", "En una democracia todos pueden decir lo que piensan",
        "En démocratie, chacun peut dire ce qu'il pense", "V demokracii může každý říct svůj názor")}),
    16120: ("«Der Herrscher war sehr streng» — претерит, пусто", {**all_x(
        "Der Herrscher von Dubai ist sehr reich", "Правитель Дубая очень богат", "Правитель Дубая дуже багатий",
        "The ruler of Dubai is very rich", "Dubai'nin hükümdarı çok zengin", "Władca Dubaju jest bardzo bogaty",
        "Il sovrano di Dubai è ricchissimo", "El gobernante de Dubái es muy rico", "Le souverain de Dubaï est très riche",
        "Vládce Dubaje je velmi bohatý")}),
    7001: ("убрать пометки (fam.)/(hovor.); " + LIST, {
        "t_ru": "затруднительное положение, зажим", "t_uk": "скрутне становище, зажим", "t_en": "tight spot, clamp",
        "t_tr": "zor durum, kıskaç", "t_pl": "tarapaty, zacisk", "t_it": "il guaio, il morsetto", "t_es": "el apuro, la pinza",
        "t_fr": "le pétrin, la pince", "t_cs": "kaše, svorka"}),
    12574: ("«Ich muss mich erholen» — пусто", {**all_x(
        "Im Urlaub habe ich mich gut erholt", "В отпуске я хорошо отдохнул", "У відпустці я добре відпочив",
        "I had a good rest on holiday", "Tatilde iyice dinlendim", "Na urlopie dobrze wypocząłem",
        "In vacanza mi sono riposato bene", "En vacaciones descansé bien", "En vacances, je me suis bien reposé",
        "Na dovolené jsem si dobře odpočinul")}),
    2607: (EN + " («on weekends» — американское)", {"x_en": "At weekends I go climbing in the mountains"}),
    3065: ("«Die Zusammenarbeit mit dem Team ist sehr produktiv» — отчёт", {**all_x(
        "Danke für die gute Zusammenarbeit!", "Спасибо за хорошее сотрудничество!", "Дякую за хорошу співпрацю!",
        "Thanks for the great cooperation!", "İyi iş birliği için teşekkürler!", "Dziękuję za dobrą współpracę!",
        "Grazie per la buona collaborazione!", "¡Gracias por la buena colaboración!", "Merci pour la bonne collaboration!",
        "Díky za skvělou spolupráci!")}),
    8844: (LIST, {"t_ru": "повышение по службе, перевозка", "t_uk": "підвищення по службі, перевезення",
                  "t_en": "promotion, transport", "t_tr": "terfi, taşıma", "t_es": "el ascenso, el transporte"}),
}

REPLACE = [
    {"id": 10412, "by": 10291, "lang": "de", "why": "Alptraum — другое написание Albtraum"},
    {"id": 13510, "by": 13481, "lang": "de", "why": "demselben — форма слова derselbe"},
]

SPLIT_LATER = {}
