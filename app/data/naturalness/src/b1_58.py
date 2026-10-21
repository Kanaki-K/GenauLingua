"""B1, блок 58: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    446: ("«Der Herbst ist eine schöne Jahreszeit» — сочинение", {**all_x(
        "Welche Jahreszeit magst du am liebsten?", "Какое время года тебе нравится больше всего?",
        "Яка пора року тобі подобається найбільше?", "Which season do you like best?", "En çok hangi mevsimi seversin?",
        "Którą porę roku lubisz najbardziej?", "Qual è la tua stagione preferita?", "¿Qué estación del año te gusta más?",
        "Quelle saison tu préfères?", "Které roční období máš nejradši?")}),
    14493: ("«Der Schöpfer des Universums ist unbekannt» — бессмыслица", {**all_x(
        "Wer ist der Schöpfer dieser Figur?", "Кто создатель этого персонажа?", "Хто творець цього персонажа?",
        "Who's the creator of this character?", "Bu karakterin yaratıcısı kim?", "Kto jest twórcą tej postaci?",
        "Chi è il creatore di questo personaggio?", "¿Quién es el creador de este personaje?",
        "Qui est le créateur de ce personnage?", "Kdo je tvůrcem té postavy?")}),
    2026: ("«Wir veranstalten ein Fest» — пусто", {**all_x(
        "Die Schule veranstaltet ein Sommerfest", "Школа устраивает летний праздник", "Школа влаштовує літнє свято",
        "The school is holding a summer party", "Okul bir yaz şenliği düzenliyor", "Szkoła organizuje festyn letni",
        "La scuola organizza una festa d'estate", "El colegio organiza una fiesta de verano",
        "L'école organise une fête d'été", "Škola pořádá letní slavnost")}),
    1012: (LIST + " (было шесть значений)", {
        "t_ru": "смена, переход", "t_uk": "зміна, перехід", "t_en": "change, switch", "t_tr": "değişim, geçiş",
        "t_pl": "zmiana, wymiana", "t_it": "il cambio, il passaggio", "t_es": "el cambio, el paso",
        "t_fr": "le changement, le passage", "t_cs": "změna, přechod"}),
    7195: ("«Der Ballon ist geplatzt» — шаблон explodieren («Der Ballon ist plötzlich explodiert»)", {
        "t_uk": "лопнути, тріснути",
        **all_x("Mir platzt gleich der Kragen!", "Сейчас я лопну от злости!", "Я зараз лопну від злості!",
                "I'm about to burst with anger!", "Neredeyse öfkeden patlayacağım!", "Zaraz pęknę ze złości!",
                "Sto per scoppiare dalla rabbia!", "¡Estoy a punto de reventar de rabia!", "Je vais éclater de colère!",
                "Za chvíli prasknu vzteky!")}),
    17541: ("«Die Software ist kostenlos» — пусто", {**all_x(
        "Du musst die Software aktualisieren", "Тебе нужно обновить программу", "Тобі треба оновити програму",
        "You need to update the software", "Yazılımı güncellemen lazım", "Musisz zaktualizować oprogramowanie",
        "Devi aggiornare il software", "Tienes que actualizar el software", "Tu dois mettre à jour le logiciel",
        "Musíš aktualizovat software")}),
    18222: ("«Es gibt viel Schmutz auf der Straße» — шаблон «Es gibt …»", {**all_x(
        "Zieh die Schuhe aus, sonst bringst du den Schmutz rein", "Сними обувь, а то натащишь грязи",
        "Зніми взуття, бо нанесеш бруду", "Take your shoes off or you'll bring the dirt in",
        "Ayakkabılarını çıkar, yoksa kiri içeri taşırsın", "Zdejmij buty, bo naniesiesz brudu",
        "Togliti le scarpe, sennò porti dentro lo sporco", "Quítate los zapatos, que si no metes la suciedad",
        "Enlève tes chaussures, sinon tu ramènes la saleté", "Zuj se, jinak natáhneš špínu")}),
    3011: ("«Das Weltall ist unendlich» — шаблон Weltraum", {**all_x(
        "Sind wir allein im Weltall?", "Одни ли мы во вселенной?", "Чи ми самі у всесвіті?", "Are we alone in the universe?",
        "Evrende yalnız mıyız?", "Czy jesteśmy sami we wszechświecie?", "Siamo soli nell'universo?",
        "¿Estamos solos en el universo?", "Sommes-nous seuls dans l'univers?", "Jsme ve vesmíru sami?")}),
    14496: ("«Die Sängerin singt wunderschön» — масло масляное", {"t_en": "singer", "t_tr": "şarkıcı", **all_x(
        "Die Sängerin gibt nächste Woche ein Konzert in Berlin", "Певица на следующей неделе даёт концерт в Берлине",
        "Співачка наступного тижня дає концерт у Берліні", "The singer is giving a concert in Berlin next week",
        "Şarkıcı gelecek hafta Berlin'de konser veriyor", "Piosenkarka daje w przyszłym tygodniu koncert w Berlinie",
        "La cantante tiene un concerto a Berlino la settimana prossima", "La cantante da un concierto en Berlín la semana que viene",
        "La chanteuse donne un concert à Berlin la semaine prochaine", "Zpěvačka má příští týden koncert v Berlíně")}),
    17543: ("«Ich habe eine Nachricht auf dem Anrufbeantworter» — пусто", {**all_x(
        "Ich habe dir auf den Anrufbeantworter gesprochen", "Я оставил тебе сообщение на автоответчике",
        "Я залишив тобі повідомлення на автовідповідачі", "I left you a message on the answering machine",
        "Telesekreterine mesaj bıraktım", "Nagrałem ci się na automatyczną sekretarkę",
        "Ti ho lasciato un messaggio in segreteria", "Te he dejado un mensaje en el contestador",
        "Je t'ai laissé un message sur le répondeur", "Nechal jsem ti vzkaz na záznamníku")}),
    18735: ("«Die Mittagspause dauert eine Stunde» — правила внутреннего распорядка", {**all_x(
        "Ich bin gerade in der Mittagspause", "У меня сейчас обеденный перерыв", "У мене зараз обідня перерва",
        "I'm on my lunch break right now", "Şu an öğle arasındayım", "Mam teraz przerwę obiadową",
        "Sono in pausa pranzo", "Ahora estoy en la pausa para comer", "Je suis en pause déjeuner", "Mám zrovna polední pauzu")}),
    8894: ("«Der Fotograf macht gute Bilder» — пусто", {**all_x(
        "Für die Hochzeit haben wir einen Fotografen gebucht", "На свадьбу мы заказали фотографа", "На весілля ми замовили фотографа",
        "We've booked a photographer for the wedding", "Düğün için bir fotoğrafçı ayarladık", "Na wesele zamówiliśmy fotografa",
        "Per il matrimonio abbiamo prenotato un fotografo", "Para la boda hemos contratado a un fotógrafo",
        "Pour le mariage, on a réservé un photographe", "Na svatbu jsme si objednali fotografa")}),
    2480: ("«Viele Freiwillige helfen mit» — пусто", {**all_x(
        "Wir suchen noch Freiwillige für das Fest", "Мы ещё ищем добровольцев для праздника", "Ми ще шукаємо волонтерів на свято",
        "We're still looking for volunteers for the party", "Şenlik için hâlâ gönüllü arıyoruz",
        "Szukamy jeszcze wolontariuszy na festyn", "Cerchiamo ancora volontari per la festa",
        "Todavía buscamos voluntarios para la fiesta", "On cherche encore des bénévoles pour la fête",
        "Na slavnost ještě hledáme dobrovolníky")}),
    17159: (EN + " («truck» — американское)", {"x_en": "We're moving the furniture in a lorry"}),
    10548: ("ru «Мы должны быть реалистичны» — калька", {"x_ru": "Нам надо быть реалистами в своих целях"}),
    13675: ("«Die Jacke ist aus echtem Leder» — шаблон Wolle («Diese Jacke ist aus echter Wolle»)", {**all_x(
        "Die Schuhe sind aus Leder und halten ewig", "Эти туфли из кожи и прослужат вечно", "Ці черевики зі шкіри і прослужать вічно",
        "The shoes are made of leather and last for ever", "Ayakkabılar deriden, ömür boyu dayanır",
        "Buty są ze skóry i wytrzymają wieki", "Le scarpe sono di pelle e durano una vita",
        "Los zapatos son de cuero y duran toda la vida", "Les chaussures sont en cuir et durent une éternité",
        "Boty jsou z kůže a vydrží věčně")}),
    14044: ("ru «я должен тебе возразить» — калька", {"x_ru": "Тут я тебе возражу", "x_uk": "Тут я тобі заперечу"}),
    2922: ("«Sei nicht so ungeduldig» — шаблон naiv («Sei doch nicht so naiv!»)", {**all_x(
        "Die Kinder werden im Auto immer ungeduldig", "Дети в машине всегда становятся нетерпеливыми",
        "Діти в машині завжди стають нетерплячими", "The kids always get impatient in the car",
        "Çocuklar arabada hep sabırsızlanıyor", "Dzieci w samochodzie zawsze się niecierpliwią",
        "In macchina i bambini diventano sempre impazienti", "En el coche los niños siempre se impacientan",
        "Les enfants deviennent toujours impatients en voiture", "Děti jsou v autě vždycky netrpělivé")}),
    12641: ("«Gute Pflege ist wichtig für deine Haut» — реклама", {**all_x(
        "Meine Oma braucht Pflege", "Моей бабушке нужен уход", "Моїй бабусі потрібен догляд", "My gran needs care",
        "Anneanemin bakıma ihtiyacı var", "Moja babcia potrzebuje opieki", "Mia nonna ha bisogno di assistenza",
        "Mi abuela necesita cuidados", "Ma grand-mère a besoin de soins", "Babička potřebuje péči")}),
    2027: ("«Die Veranstaltung beginnt um 19 Uhr» — шаблон «beginnt um …»", {**all_x(
        "Die Veranstaltung wird wegen Regen verschoben", "Мероприятие переносится из-за дождя", "Захід переносять через дощ",
        "The event is being postponed because of rain", "Etkinlik yağmur yüzünden erteleniyor",
        "Wydarzenie zostaje przełożone z powodu deszczu", "L'evento viene rinviato per la pioggia",
        "El evento se aplaza por la lluvia", "L'événement est reporté à cause de la pluie", "Akce se kvůli dešti odkládá")}),
    15536: ("«Der Elefant ist das größte Landtier» — учебник", {**all_x(
        "Er benimmt sich wie ein Elefant im Porzellanladen", "Он ведёт себя как слон в посудной лавке",
        "Він поводиться як слон у посудній лавці", "He behaves like an elephant in a china shop",
        "Züccaciye dükkânındaki fil gibi davranıyor", "Zachowuje się jak słoń w składzie porcelany",
        "Si comporta come un elefante in una cristalleria", "Se comporta como un elefante en una cacharrería",
        "Il se comporte comme un éléphant dans un magasin de porcelaine", "Chová se jako slon v porcelánu")}),
    636: (EN + " («last name» — американское)", {"t_en": "surname, family name", "x_en": "What's your surname?"}),
    16230: ("ru «Ты должен соблюдать» — калька", {**all_x(
        "Vorschrift ist Vorschrift", "Правила есть правила", "Правила є правила", "Rules are rules", "Kural kuraldır",
        "Przepis to przepis", "Le regole sono regole", "Las normas son las normas", "Le règlement, c'est le règlement",
        "Předpis je předpis")}),
}

SPLIT_LATER = {}
