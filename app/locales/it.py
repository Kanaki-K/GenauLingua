"""
Localizzazione italiana per GenauLingua Bot

Только уважительная форма (Lei), «занятие» — lezione. Набор и порядок ключей —
как в en.py.
"""

TEXTS = {
    # ============================================================================
    # MENU PRINCIPALE
    # ============================================================================
    "btn_learn_words": "Imparare parole",
    "btn_stats": "Statistiche",
    "btn_settings": "Impostazioni",
    "btn_help": "Aiuto",
    "btn_back": "Indietro",
    "menu_placeholder": "Scelga un'azione…",

    # ============================================================================
    # BENVENUTO E AVVIO
    # ============================================================================
    "welcome_title": "<b>Salve, {name}!</b>",








    # ============================================================================
    # PROMEMORIA
    # ============================================================================
    "notif_title": "<b>Promemoria</b>",
    "notif_status": "Stato: {status}",
    "notif_status_on": "attivi",
    "notif_status_off": "disattivati",
    "notif_time": "Ora: {time}",
    "notif_days": "Giorni: {days}",
    "notif_timezone": "Fuso orario: {timezone}",
    "notif_hint": "Il promemoria arriva all'ora scelta, nel suo fuso orario.",
    "notif_hint_off": "Attivi i promemoria: così è più facile non interrompere la serie.",

    "notif_btn_toggle_on": "Promemoria: attivi",
    "notif_btn_toggle_off": "Promemoria: disattivati",
    "notif_btn_time": "Ora: {time}",
    "notif_btn_days": "Scegliere i giorni",
    "notif_btn_timezone": "Cambiare fuso orario",

    "notif_timezone_title": "<b>Il suo fuso orario</b>",
    "notif_timezone_current": "Attuale: {timezone}",
    "notif_timezone_prompt": "Scelga una città nel suo fuso orario:",
    "notif_timezone_more": "Un'altra città",
    "notif_timezone_back": "Indietro",
    "notif_timezone_set": "✓ Fuso orario impostato: {city}",

    "notif_time_title": "<b>Ora del promemoria</b>",
    "notif_time_current": "Ora attuale: {time}",
    "notif_time_timezone": "Fuso orario: {timezone}",
    "notif_time_hint": "Il promemoria arriva a quest'ora nei giorni scelti.",
    "notif_time_set": "✓ Ora impostata: {time}",

    "notif_days_title": "<b>Giorni del promemoria</b>",
    "notif_days_hint": "Tocchi un giorno per attivarlo o disattivarlo.\n✓ — giorno attivo\n✗ — giorno disattivato\n\nAlla fine tocchi «Salva».",
    "notif_days_all": "Tutti i giorni",
    "notif_days_weekdays": "Feriali (Lun–Ven)",
    "notif_days_save": "Salva",
    "notif_days_saved": "✓ Giorni salvati!",
    "notif_days_all_selected": "✓ Tutti i giorni selezionati",
    "notif_days_weekdays_selected": "✓ Giorni feriali selezionati (Lun–Ven)",
    "notif_days_none": "Scelga almeno un giorno.",

    "notif_toggle_on": "Promemoria attivi",
    "notif_toggle_off": "Promemoria disattivati",

    "day_mon": "Lun",
    "day_tue": "Mar",
    "day_wed": "Mer",
    "day_thu": "Gio",
    "day_fri": "Ven",
    "day_sat": "Sab",
    "day_sun": "Dom",

    "notif_btn_back": "Torna alle impostazioni",

    "notif_default_name": "amico",



    # ONE REASON TO COME BACK — and it has to be true

    # ============================================================================
    # IMPOSTAZIONI
    # ============================================================================
    "settings_title": "<b>Impostazioni</b>",
    "settings_mode": "Modalità: <b>{mode}</b>",
    "settings_language": "Lingua del bot: <b>{language}</b>",

    "settings_btn_quiz_mode": "Livello e argomenti",
    "settings_btn_change_language": "Lingua del bot",
    "settings_btn_notifications": "Promemoria",

    "settings_quiz_mode_line": "Livello: <b>{mode}</b>",
    "start_pick_language": "Scelga la Sua lingua",
    "onboard_your_lang": "✓ La Sua lingua: {language}",
    "onboard_change_hint": "Può cambiarla in qualsiasi momento: comando /language.",
    "onboard_phone_hint": "Il Suo Telegram è in italiano. Se ha scelto la lingua per errore, tocchi «{back}».",
    "lang_confirm_learning": "Lingua di studio: {language}",
    "lang_progress_kept": "I progressi di ogni lingua restano salvati.",
    "btn_done": "Fatto",
    "btn_change_learning": "Cambiare la lingua che studio",
    "intro_pair": "Lei studia {learning} con traduzione in {native}.",
    "intro_menu_language": "lingua del bot",
    "plural_languages": "lingua|lingue",
    "cmd_start": "Inizio e cosa fa il bot",
    "cmd_language": "Lingua del bot",
    "cmd_settings": "Impostazioni",
    "cmd_help": "Aiuto",

    "language_changed": "✓ Lingua cambiata: {language}",
    "user_not_found": "✗ Profilo non trovato. Invii /start",

    "lang_ru": "Русский",
    "lang_uk": "Українська",
    "lang_en": "English",
    "lang_tr": "Türkçe",
    "lang_de": "Deutsch",
    "lang_pl": "Polski",
    "lang_it": "Italiano",
    "lang_es": "Español",
    "lang_fr": "Français",
    "lang_cs": "Čeština",



    # ============================================================================
    # MODALITÀ DI STUDIO
    # ============================================================================
    "qmode_title": "<b>Livello e argomenti</b>",
    "qmode_current": "Attuale: <b>{mode}</b>",
    "qmode_choose": "Scelga come vuole studiare.\nPuò cambiare in qualsiasi momento: i progressi restano salvati.",

    "qmode_btn_level": "Per livello",
    "qmode_btn_category": "Per argomento",
    "qmode_btn_all": "Tutte le parole",
    "qmode_btn_difficult": "Parole difficili",

    "qmode_level_short": "{level}",
    "qmode_category_short": "{category}",
    "qmode_all_short": "Tutte le parole",
    "qmode_difficult_short": "Parole difficili",

    "qmode_level_title": "<b>Scelga un livello</b>",
    "qmode_level_desc": "Dalle prime parole alla conversazione scorrevole. Tutti i livelli sono aperti: scelga il suo.\n\n• A1–A2 — lessico di base\n• B1–B2 — comunicazione sicura\n• C1–C2 — lingua fluente e ricca di sfumature",
    "qmode_level_set": "✓ Modalità: per livello ({level})",

    "qmode_category_title": "<b>Scelga un argomento</b>",
    "qmode_category_desc": "Dal cibo alla scienza: scelga l'argomento che le serve.\n\nOgni argomento contiene parole di tutti i livelli.",
    "qmode_category_set": "✓ Argomento: {category}",

    # Category names
    "cat_arbeit_beruf": "Lavoro",
    "cat_bildung_lernen": "Istruzione",
    "cat_einkaufen_geld": "Acquisti",
    "cat_emotionen_charakter": "Emozioni",
    "cat_essen_trinken": "Cibo",
    "cat_freizeit_sport": "Sport",
    "cat_gesundheit_medizin": "Salute",
    "cat_grammatik": "Grammatica",
    "cat_kleidung_mode": "Abbigliamento",
    "cat_kommunikation": "Comunicazione",
    "cat_kultur_kunst": "Cultura",
    "cat_mensch_familie": "Famiglia",
    "cat_natur_wetter": "Natura",
    "cat_recht_staat": "Diritto",
    "cat_reisen_transport": "Viaggi",
    "cat_technik_digital": "Tecnologia",
    "cat_wirtschaft": "Economia",
    "cat_wissenschaft": "Scienza",
    "cat_wohnen_haus": "Casa",
    "cat_zeit_alltag": "Vita quotidiana",

    "qmode_all_set": "✓ Modalità: tutte le parole",

    "qmode_difficult_set": "✓ Modalità: parole difficili",
    "qmode_difficult_few": "Parole difficili finora: {count}, ne servono almeno 4.\nFaccia ancora qualche lezione!",
    "qmode_difficult_empty": "Ancora nessuna parola difficile.\nFaccia prima qualche lezione!",

    "quiz_btn_change_mode": "Livello e argomenti",
    "quiz_btn_report_error": "Segnalare un errore",
    "report_btn_confirm": "✓ Conferma ({count})",
    "report_btn_send": "Invia",
    "report_kind_text": "Traduzione",
    "report_kind_example": "Esempio",
    "report_kind_audio": "Audio",
    "report_pick_hint": "Cosa non va? Lo segni e prema «Invia»",
    "report_btn_sent": "✓ Segnalazione inviata",
    "report_sent_one": "✓ Grazie!\nSe l'errore viene confermato, riceverà +{points}.",
    "report_approved_example": "✓ La sua segnalazione sull'esempio di <b>{word}</b> è stata accettata\n\nCorreggeremo l'esempio\n\n+{points} punti al punteggio del mese, grazie",
    "report_no_words": "Nessuna parola da segnalare",
    "report_none_selected": "Selezioni almeno una parola",
    "report_pick_kind": "Parole selezionate: {count}. Ora scelga cosa non va: la traduzione o la pronuncia.",
    "report_sent": "✓ Segnalazioni inviate: {count}, grazie!\nOgni segnalazione confermata vale +{points}.",
    "report_daily_limit": "Ha raggiunto il limite di oggi: 20 segnalazioni.",
    "report_all_reported": "✓ Tutte le parole di questa lezione sono già state segnalate",
    "report_already_sent": "✓ Già segnalato",
    "report_btn_kind_text": "Traduzione sbagliata",
    "report_btn_kind_audio": "Pronuncia sbagliata",
    "report_sent_audio": "✓ Segnalazioni inviate: {count}, grazie!\nLe segnalazioni sulla pronuncia sono particolarmente preziose: il controllo automatico non sente l'accento.\nOgni segnalazione confermata vale +{points}.",
    "report_approved": "✓ La sua segnalazione su <b>{word}</b> è stata accettata: correggeremo la traduzione\n\n+{points} punti al punteggio del mese. Grazie, così il dizionario migliora per tutti",
    "award_won": "{mark} Il suo posto nella classifica di {month}: #{rank}\n\n{bonus} punti aggiunti al punteggio di sempre",
    "report_approved_audio": "✓ La sua segnalazione sulla pronuncia di <b>{word}</b> è stata accettata\n\nL'audio verrà corretto\n\n+{points} punti al punteggio del mese, grazie",
    # ============================================================================
    # LEZIONE
    # ============================================================================
    "quiz_no_level": "Prima scelga il suo livello: /start",
    "quiz_error_generation": "✗ Qualcosa è andato storto nel preparare la lezione.\nRiprovi con /start",
    "quiz_no_words": "✗ Spiacenti, per questo livello non ci sono parole.\nProvi un altro livello.",

    "quiz_question_number": "{current} / {total}",

    "quiz_correct": "✓ <b>Giusto</b>",
    "quiz_wrong": "✗ <b>Sbagliato</b>",
    "quiz_correct_answer": "Risposta giusta:",

    "quiz_btn_next": "Avanti →",

    "quiz_answer_already_counted": "La sua risposta è già stata conteggiata. Continuiamo?",
    "quiz_btn_repeat_errors": "Ripetere gli errori",
    "lesson_resume_prompt": 'Ha una lezione non finita: {done} su {total}',
    "btn_lesson_resume": 'Continuare',
    "btn_lesson_new": 'Iniziarne una nuova',
    "speech_offer_text": 'Sembra che ora non sia comodo parlare ad alta voce. Togliere «Parlo» dalle lezioni? Può rimetterlo nelle impostazioni',
    "btn_speech_off": 'Togliere «Parlo»',
    "btn_speech_keep": 'Lasciare',
    "speech_off_done": 'Fatto: «Parlo» non comparirà più nelle lezioni. Può rimetterlo nelle impostazioni',

    "quiz_completed": "<b>Lezione completata</b>",
    "quiz_result_correct": "Giuste: <b>{correct}/{total}</b>",
    "quiz_result_percentage": "Risultato: <b>{percentage}%</b>",
    "quiz_result_details": "<b>Dettagli:</b>",
    "quiz_result_errors": "Errori: {count}",

    # PRAISE AT THE END OF A LESSON — only for what actually happened
    "praise_first_round": "Prima lezione fatta. Da qui le parole iniziano a tornare: è così che si fissano.",
    "praise_first_learned": "Prima parola imparata: tre risposte giuste di fila, nessuna nel giorno in cui l'ha incontrata.",
    "praise_learned": "Parole imparate in questa lezione: {count}",
    "praise_best_streak": "Record personale: {days_word} di fila",
    "praise_milestone": "Ora sta studiando {count} parole",
    "praise_first_speech": "Prima risposta giusta ad alta voce",
    "praise_first_audio": "Prima risposta giusta ad orecchio",
    "praise_comeback": "Che piacere rivederla! L'ultima lezione è stata {days_word} fa.",
    "praise_perfect": "Una lezione senza nemmeno un errore",
    "praise_streak": "Serie: {days_word} di fila",
    "praise_freeze_saved": "Ieri non ha fatto lezione, ma la protezione della serie l'ha salvata: {days_word} di fila. La prossima protezione sarà disponibile tra una settimana.",
    "praise_streak_3": "Tre giorni di fila: sta nascendo un'abitudine.",
    "praise_streak_7": "Un'intera settimana di fila! È il traguardo chiave: da qui l'abitudine si regge da sola.",
    "praise_streak_14": "Due settimane di fila: ottimo ritmo.",
    "praise_streak_30": "Un mese di fila! Ormai è una vera abitudine.",
    "praise_new_words": "Parole nuove: {count}",
    "praise_returned": "Riconosciute di nuovo: {count}",
    "praise_progress": "Parole in studio: {count} · ancora {left} per arrivare a {target}",
    "praise_progress_top": "Parole in studio: {count}",
    "praise_points": "Punti: +{points}",

    "quiz_repeat_title": "<b>Ripetere gli errori</b>",
    "quiz_no_errors": "✓ Nessun errore questa volta!",
    "quiz_error_next": "✗ Impossibile caricare la domanda successiva.",

    # ============================================================================
    # STATISTICHE
    # ============================================================================
    "stats_no_level": "<b>Prima scelga il suo livello!</b>\n\nPer iniziare usi /start.",





    # ============================================================================
    # AIUTO
    # ============================================================================
    "help_title": "<b>Aiuto — GenauLingua</b>",
    "help_description": "Come funzionano le lezioni e come raggiungere la community.",
    "help_choose": "Scelga una sezione:",

    "help_btn_how_to_use": "Come si usa",
    "help_btn_community": "Community",

    "help_how_to_use_title": "<b>Come usare il bot</b>",


    "help_community_title": "<b>La community di GenauLingua</b>",
    "help_community_text": """ <b>t.me/genaulingua_chat</b>

Nella chat:
Le novità arrivano qui per prime
Ha trovato un bug? Ci scriva o mandi uno screenshot
Errore di traduzione? Ce lo segnali, lo correggeremo
Idee e proposte: leggiamo tutto
Parli con altri studenti


Più la community è attiva, migliore diventa il bot. Ci scriva senza timore! """,


    # ============================================================================
    # CLASSIFICA
    # ============================================================================
    "rating_not_active": "✗ La classifica non è ancora attiva.",
    "rating_not_in_ranking": "Non è ancora in classifica",
    "rating_start_quiz": "Faccia la sua prima lezione!",
    "rating_join_by_lesson": "I punti delle segnalazioni ({score}) sono stati accreditati. Completi una lezione per entrare nella classifica di questo mese.",
    "release_notes_2026_10": "✨ <b>GenauLingua 2.0 — abbiamo ricostruito il bot da zero</b>\n\n<b>Non solo tedesco.</b> Può imparare ucraino, inglese, turco, tedesco, polacco o russo, partendo da una qualsiasi di queste lingue. Anche l'interfaccia parla tutte e sei.\n\n<b>Sei giochi invece di uno.</b> Prima c'era solo «scegliere la traduzione».\n\nOra in ogni lezione i giochi si alternano:\n📖 Leggo · 💭 Ricordo · 🎧 Ascolto · 🎤 Parlo · 🧩 Trovare le coppie · 🧱 Compongo\n\nIn «Parlo» risponde a voce; in «Compongo» mette insieme una frase, e il bot mostra quale parola è fuori posto.\n\n<b>Il bot parla.</b> Ogni parola e ogni esempio vengono letti ad alta voce con una voce naturale.\n\n<b>Un nuovo aspetto.</b> Un nuovo menu, una chat pulita e ordinata, una schermata iniziale con le sue abilità, statistiche chiare, un nuovo avatar e un nuovo saluto.\n\n<b>Tutto il dizionario è stato ricontrollato</b>: tutte le 12.902 parole, le traduzioni e gli esempi.\n\n<b>Si adatta a lei:</b> le parole tornano poco prima che le dimentichi, e il bot propone il livello successivo quando diventa facile.\n\n<b>Errori corretti:</b> la serie di giorni viene contata correttamente e i punti della classifica sono equi: premiano l'impegno. Anche «Imparata» ora è onesto: una parola conta come imparata dopo tre risposte giuste di fila in giorni diversi, e ogni parola che ha esercitato compare tra le «Parole in studio».\n\n<b>I promemoria sono attivi</b>, all'ora che preferisce. Per cambiarli o disattivarli: Impostazioni → Bot → Promemoria.\n\n⭐ Ha notato un errore? Lo segnali direttamente dal riepilogo della lezione: ogni segnalazione confermata vale +15 punti.\n\nI suoi progressi e i suoi punti sono conservati. Provi: una lezione richiede un paio di minuti.",
    "release_notes_2026_10_22": '✨ <b>GenauLingua 2.2 - ora dieci lingue</b>\n\nBuongiorno!\n\nÈ uscito un grande aggiornamento:\n\n<b>4 nuove lingue</b>\n\n🇮🇹 Italiano, 🇪🇸 spagnolo, 🇫🇷 francese e 🇨🇿 ceco - può studiarle da qualsiasi lingua del bot\nOgnuna ha oltre 12.000 parole con esempi, tutte con audio\n\n<b>Una classifica per cui vale la pena gareggiare</b>\n\nMedaglie del mese 🥇🥈🥉, una corona 👑 al primo posto tra chi studia la Sua lingua e gradi che crescono insieme a Lei. I primi risultati con le nuove regole - il primo novembre\n\n<b>La serie perdona un giorno saltato</b>\n\nUna volta alla settimana la protezione della serie 🧊 salva la Sua serie se salta un giorno\n\n<b>E inoltre:</b> segnalazione di un errore nella traduzione, nell’esempio o nell’audio - subito sotto la risposta (+15 punti per ogni segnalazione confermata)\n\nLe parole note si imparano più in fretta, e gli aggiornamenti del bot non interrompono più la lezione\n\nGrazie di studiare con noi e di segnalare gli errori - così il bot migliora per tutti 💙\n\nTutte le novità, in breve e in modo chiaro: <a href="{url}">novità della 2.2</a>',
    "btn_release_news": 'Novità →',


    "table_empty": "Ancora nessun partecipante.\nInizi lei con una lezione!",
    "table_you_not_ranked": "Non è ancora in classifica",
    "rating_tab_month": "Mese",
    "rating_tab_alltime": "Di sempre",
    "rating_crown_rule": "Il primo posto riceve la corona per tutto il mese successivo",
    "rating_screen_title": "<b>Classifica · {month} {year}</b>",
    "rating_screen_title_alltime": "<b>Classifica · di sempre</b>",
    "rating_you": "<b>Lei: #{rank} su {total}</b> · {points}",
    "rating_results_in": "Risultati del mese tra {days}",
    "info_title": "<b>Come funziona la classifica</b>",
    "info_month": "<b>Mese</b> — tutti. I tre migliori ricevono 🥇 🥈 🥉 (con almeno 3 lezioni).",
    "info_lang": "<b>Lingua</b> — chi studia la Sua lingua. Il primo riceve 👑 per il mese successivo.",
    "info_alltime": "<b>Di sempre</b> — tutti i punti. Le medaglie fanno salire il grado 🌱 🌳 🌙 🪐 ☀️",
    "info_points_title": "<b>Punti</b>",
    "info_points": "Risposta +1 · ad orecchio +2 · ad alta voce +3\nLezione +10 · parola imparata +3\nGiorni di fila — fino a +10 · precisione sopra il 60% — bonus\nSegnalazione confermata +{points}",
    "title_sprout": "Germoglio",
    "title_tree": "Albero",
    "title_moon": "Luna",
    "title_planet": "Pianeta",
    "title_sun": "Sole",
    "title_galaxy": "Galassia",
    "btn_rating_info": "Info",
    "card_medal_need": "Lezioni necessarie per una medaglia: {need} · Lei ne ha {have}",
    "card_crown_small": "La corona si gioca quando la lingua ha 3+ persone con 3+ lezioni",
    "summary_place": "↑ Posto nel mese: {rank}",
    "summary_gap": "a {name} {gap}",
    "summary_record": "Nuovo record del mese: {points}",
    "collection_title": "<b>Collezione</b> · {open} su {total} sbloccati",
    "collection_locked": "▫️ ???",
    "ach_streak_7": "Serie di 7 giorni",
    "ach_streak_30": "Serie di 30 giorni",
    "ach_streak_100": "Serie di 100 giorni",
    "ach_streak_365": "Serie di 365 giorni",
    "ach_streak_1000": "Serie di 1000 giorni",
    "ach_words_100": "100 parole imparate",
    "ach_words_1000": "1000 parole imparate",
    "ach_words_3000": "3000 parole imparate",
    "ach_perfect_10": "10 lezioni senza errori",
    "ach_voice_1000": "1000 risposte corrette a voce",
    "ach_editor": "Redattore del dizionario: 5 segnalazioni accettate",
    "ach_polyglot": "Poliglotta: 100 parole in due lingue",
    "award_month_header": "<b>Risultati del mese</b>",
    "award_crown": "👑 Corona — {language}: primo posto. La porterà per tutto il mese successivo",
    "award_glory": "+{glory} di gloria",
    "award_new_title": "Nuovo grado: {mark} {name}",
    "nd_overtaken": "L’hanno superata nella classifica del mese.\nIl Suo posto: {rank} · a {name} {gap}.",
    "nd_finish": "Alla fine del mese: {days}.\nIl Suo posto: {rank} · per una medaglia mancano {gap}.",

    "stats_header": "<b>Le sue statistiche</b>",
    "stats_in_work_line": "Parole in studio: {count} · ancora {left} per arrivare a {target}",
    "stats_in_work_top": "Parole in studio: {count}",
    "stats_details": "In studio: {progress}\nNuove: {new}\nDifficili: {difficult}",
    "stats_achievements_title": "<b>I suoi traguardi</b>",
    "stats_words_count": "Parole imparate: <b>{count}</b>",
    "stats_best_streak_line": "Serie migliore: {days_word}",
    "stats_quizzes_header": "<b>Lezioni · {level}</b>",
    "stats_quizzes_passed_line": "Completate: <b>{count}</b>",
    "stats_quizzes_avg_line": "Risultato medio: <b>{percent}%</b>",
    "stats_quizzes_best_line": "Miglior risultato: <b>{percent}%</b>",
    "stats_quizzes_empty": "Ancora nessuna lezione completata",
    "stats_recent_header": "<b>Ultime lezioni</b>",
    "stats_explanation": "Una parola conta come imparata dopo tre risposte giuste di fila, in giorni diversi.",
}

# ============================================================================
# MULTILINGUAL: learning language, meaning language and direction
# ============================================================================
TEXTS.update({
    "langname_de": "Tedesco",
    "langname_en": "Inglese",
    "langname_ru": "Russo",
    "langname_uk": "Ucraino",
    "langname_tr": "Turco",
    "langname_pl": "Polacco",
    "langname_it": "Italiano",
    "langname_es": "Spagnolo",
    "langname_fr": "Francese",
    "langname_cs": "Ceco",
    # Союз для перечисления языков в текстах помощи и приветствия
    "and_word": "e",

    "settings_learning_lang_line": "Studio: <b>{language}</b>",

    "settings_btn_learning_lang": "Lingua",

    "learning_lang_title": "<b>Lingua da imparare</b>",
    "learning_lang_description": "Scelga la lingua di cui vuole imparare le parole.\nI progressi sono contati a parte per ogni lingua.",
    "learning_lang_set": "✓ Studio: {language}",
    # Settings line and the audio screen
    "settings_audio_line": "Audio: <b>{state}</b>",
    "settings_btn_audio": "Audio",
    "audio_state_on": "attivo",
    "audio_state_off": "disattivato",

    "audio_title": "<b>Audio</b>",
    "audio_description": "Le parole sono lette ad alta voce da una voce IA dal suono naturale. La domanda fa sentire solo la parola, la risposta la parola con l'esempio.",
    "audio_current_voice": "Voce: <b>{voice}</b>",
    "audio_btn_turn_on": "Attivare l'audio",
    "audio_btn_turn_off": "Disattivare l'audio",
    "audio_btn_choose_voice": "Scegliere la voce",
    "audio_turned_on": "✓ Audio attivo",
    "audio_turned_off": "Audio disattivato",

    "voice_title": "<b>Scelga una voce</b>",
    "voice_description": "Tocchi una voce per ascoltarla. Il segno di spunta indica quella attuale.",
    "voice_male": "Maschile",
    "voice_female": "Femminile",
    "voice_set": "✓ Voce: {voice}",
    "voice_use": "Usare {voice}",
    "voice_listening": "In riproduzione: {voice}",
    "voice_only_one": "Per questa lingua c'è una sola voce maschile e una sola femminile.",
    "voice_preview_failed": "Impossibile caricare l'esempio. Riprovi.",
})


# ============================================================================
# АПГРЕЙД ПОД ШЕСТЬ ЯЗЫКОВ
#
# Добавлено, когда бот перестал быть «ботом для немецкого»: при первом запуске
# человек теперь выбирает не только язык интерфейса, но и какой язык учить, а
# подсказки направления стали работать на все тридцать пар вместо восьми.
# ============================================================================
TEXTS.update({
    "btn_rating": "Classifica",
    "friend_fallback": "amico",
    "onboarding_learning_title": "<b>Quale lingua vuole imparare?</b>",
})


# ============================================================================
# ПОМОЩЬ ПОСЛЕ СОКРАЩЕНИЯ: было четыре экрана, стало два
#
# Убран экран «Скоро в боте» — он обещал Goethe/ÖSD и тексты на немецком,
# то есть врал всем, кто учит не немецкий. «О боте» слит с «Сообществом».
# Инструкция сокращена: из неё выброшено всё, что человек и так видит на
# экране, и оставлено то, чего из интерфейса не видно.
# ============================================================================
TEXTS.update({
    "help_how_to_use_text": "<b>Lezione</b>\n{words}, quattro opzioni ciascuna. Una lezione mescola sei giochi: «Leggo», «Ricordo», «Ascolto», «Parlo», «Compongo» e la tavola «Trovare le coppie». Il bot ricorda i Suoi errori e ripropone più spesso le parole difficili. Dopo la lezione può ripetere quelle sbagliate.\n\n<b>Audio</b>\nLa domanda fa sentire la parola; dopo la risposta sente la parola con il suo esempio. Nelle impostazioni può scegliere una voce maschile o femminile.\n\n<b>Lingue</b>\n{languages}, in qualsiasi coppia. I progressi sono contati a parte per ogni lingua; la classifica ha le schede «Mese», «Di sempre» e «Lingua».\n\n\nUna parola conta come <b>imparata</b> dopo tre risposte giuste di fila, in giorni diversi. Se indovina una parola nuova al primo colpo, basta un'altra risposta giusta.\nLa sua <b>serie</b> cresce ogni giorno in cui fa almeno una lezione. Un giorno saltato a settimana non la interrompe: lo copre la protezione della serie.\nTraduzione o pronuncia sbagliata? Usi il pulsante «Segnalare un errore» sotto la risposta.",
    "help_community_title": "<b>Il bot e la community</b>",
    "help_community_text": "<b>GenauLingua</b> — {language_count} lingue in qualsiasi coppia: {languages}\n12.900 parole A1–C2, ognuna con un esempio e un audio dal suono naturale.\nInterfaccia: {interface_languages}\n\n<b>t.me/genaulingua_chat</b>\nBug, errori di traduzione, idee: leggiamo tutto. Le segnalazioni sulla pronuncia sono particolarmente gradite: una macchina non sente l'accento.",
})


# ============================================================================
# ВОПРОС НА СЛУХ
#
# Самого слова на экране нет — иначе слушать незачем. Варианты стоят на
# ИЗУЧАЕМОМ языке: спрашивают «что услышал», а не «что это значит».
# ============================================================================
TEXTS.update({
    "quiz_question_listen": "Ascolti e scelga ciò che ha sentito:",
})


# ============================================================================
# БАЛЛЫ: ПЛАТИМ ЗА УСИЛИЕ, А НЕ ЗА НАЖАТИЯ
#
# Верный ответ стоит по-разному в зависимости от канала (1/2/3): узнать на
# слух труднее, чем прочитать, а произнести труднее, чем узнать. Платить
# за все три одинаково значило бы советовать «не напрягайся».
#
# Точность начисляется плавно, без прежнего обрыва на 90%: человек с 89%
# видел, что двадцать баллов пропали из-за одного вопроса.
#
# Серия растёт в цене: десятый день дороже первого. Прежде день давал ровно
# три балла, и терять серию было почти не жалко.
# ============================================================================
TEXTS.update({
})


# ============================================================================
# ГОТОВНОСТЬ ГОЛОСА
#
# Предсинтезированы не все голоса: это гигабайты и часы на каждый. У
# остальных клип делается на лету, и на недокументированном движке синтез
# срывается примерно в одном случае из пяти — слово приходит без звука.
#
# Владелец выбрал голос без единого клипа и половину карточек слушал молча,
# не имея возможности узнать причину: все голоса выглядели одинаково.
# ============================================================================
TEXTS.update({
})


# ============================================================================
# ИТОГ КРУГА: сколько вопросов было на слух
#
# Иначе новая игра растворяется в общем списке, и человек не замечает, что
# уже узнаёт слова ушами. Строка показывается, только если такие вопросы
# были.
# ============================================================================
TEXTS.update({
    "quiz_result_by_ear": "🎧 Ad orecchio: {count}",
})


# ============================================================================
# СОСТАВ ЗАНЯТИЯ
#
# Три канала — три РАЗНЫХ навыка, а не три оформления одного. Экран нужен,
# потому что до него колонка quiz_channels была недостижима: выключить
# вопросы на слух можно было только выключив озвучку целиком.
# ============================================================================
TEXTS.update({
    "settings_btn_channels": "Giochi della lezione",
    "settings_channels_line": "Lezione: <b>{channels}</b>",
    "channels_title": "<b>Giochi della lezione</b>",
    "channels_description": "Quali giochi mescolare in una lezione. Una parola nuova arriva come carta «Leggo»; quando la conosce, torna in altri giochi: ricordarla, sentirla, dirla, comporre una frase con essa. Più giochi ci sono, meglio la parola si fissa.",
    "channel_text": "📖 Leggo",
    "channel_audio": "🎧 Ascolto",
    "channel_speech": "🎤 Parlo",
    "channel_build": "🧱 Compongo",
    "home_scale_build": "Compongo",
    "quiz_result_built": "🧱 Composte: {count}",
    "build_hint": "Componga la frase con le parole qui sotto: alcune sono di troppo",
    "build_btn_check": "Verifica",
    "build_full": "Tutti i posti sono occupati. Tolga una parola con ⌫ oppure prema «Verifica».",
    "build_order_only": "↔ <b>Parole giuste, ordine diverso</b>",
    "build_reference": "Giusto:",
    "build_yours": "La sua risposta:",
    "build_extra": "Di troppo: {words}",
    "build_missing": "Mancano: {words}",
    "stats_grammar_line": "Grammatica: {correct} giuste su {shown}",
    "quiz_result_recalled": "💭 Ricordate: {count}",
    "home_scale_reverse": "Ricordo",
    "channel_reverse": "💭 Ricordo",
    "channels_text_always": "«Leggo» non si può disattivare: ogni parola nuova comincia da lì.",
    "channels_audio_blocked": "🎧 «Ascolto» e «Parlo» non sono disponibili finché l'audio è disattivato.",
})


# ============================================================================
# ВОПРОС ВСЛУХ
#
# Ответ приходит голосовым сообщением, а не нажатием. Распознаватель отвечает
# на вопрос «то ли слово сказано», и только на него: качество произношения он
# судить не умеет — он обучен ПОНИМАТЬ акцент, а не замечать его.
# ============================================================================
TEXTS.update({
    "quiz_question_speak": "🎤 Dica questa parola ad alta voce: registri un messaggio vocale tenendo premuta l'icona del microfono nel campo dei messaggi di Telegram, in basso a destra",
    "speech_btn_reference": "Ascoltare lentamente",
    "speech_btn_skip": "Saltare",
    "speech_listening": "🎧 Ascolto…",
    "speech_not_understood": "Non sono riuscito a capire. Registri di nuovo, più vicino al microfono e un po' più forte.",
    "speech_try_again": "Sembrava «{heard}»: non proprio. Registri di nuovo: tentativo {attempt} di {total}.",
    "speech_send_voice": "🎤 Questa domanda richiede un messaggio vocale. Tenga premuto il pulsante del microfono.",
    "speech_skipped": "Saltata",
    "speech_not_counted": "Di nuovo sembrava «{heard}». Non conta né come giusta né come errore: ascolti come suona, e andiamo avanti.",
    "lesson_expired": "Questa lezione è stata interrotta: il bot è stato aggiornato oppure la lezione è finita da tempo. Ne inizi una nuova con il pulsante qui sotto.",
    "quiz_result_spoken": "🎤 Pronunciate: {count}",
})


# ============================================================================
# ДОМАШНИЙ ЭКРАН: ТРИ ШКАЛЫ
# ============================================================================
TEXTS.update({
    "home_scale_text": "Leggo",
    "home_scale_audio": "Ascolto",
    "home_scale_speech": "Parlo",
    "home_btn_learn": "Imparare parole",
    "home_rank": "posizione {rank}",
    "home_hint": "",
    "home_channel_not_ready": "{channel}: non ancora. Parole pronte: {ready}, ne servono almeno {minimum}. Si eserciti con le carte «Leggo»: sbloccano gli altri giochi.",
})


# ============================================================================
# НАСТРОЙКИ: ТРИ ГРУППЫ
#
# «Что учу» человек меняет часто, «как мне удобно» ставит один раз. Восемь
# равных пунктов перемешивали то и другое, и первым в списке стоял режим
# викторины, которым не пользуются 96%.
# ============================================================================
TEXTS.update({
    "settings_group_what": "Cosa studio",
    "settings_group_what_title": "<b>Cosa studio</b>",
    "settings_group_how": "Come studio",
    "settings_group_how_title": "<b>Come studio</b>",
    "settings_group_bot": "Bot",
    "settings_group_bot_title": "<b>Bot</b>",
    "settings_group_what_about": "Lingua, obiettivo e livello.",
    "settings_group_how_about": "Di cosa è fatta una lezione e come suona.",
    "settings_group_bot_about": "Lingua del bot, promemoria e aiuto.",
})


# ============================================================================
# ПЕТЛЯ ВОЗВРАТА
#
# Замер на 233 людях: 79% тех, кто вообще играл, ни разу не занимались два
# дня подряд. У каждого экрана, которым кончается действие, должна быть
# кнопка следующего — иначе человек уходит там, где был готов продолжить.
# Разбор — MENU_CONCEPT.md.
# ============================================================================
TEXTS.update({
    "quiz_btn_one_more": "Un'altra lezione",
    "home_btn_stats": "Più dettagli",
    "notif_off_how_to_return": "Per riattivarli: Impostazioni → Bot → Promemoria",
    "reminder_offer_done": "✓ Fatto: il promemoria arriverà alle <b>{time}</b> ({city})\n\nPuò regolare ora, giorni e fuso orario",
    "reminder_offer_setup": "Regolare i promemoria",
    "level_offer": "Al livello <b>{current}</b> sbaglia raramente\n\nPassare a <b>{following}</b>?\n\nTutto ciò che ha imparato resta",
    "level_offer_yes": "Sì, passare a {following}",
    "level_offer_no": "Restare qui",
    "level_offer_done": "Il suo livello ora è <b>{following}</b>\n\nLe parole saranno più difficili",
    "level_offer_pick": "Sembra che <b>{current}</b> sia facile per lei\n\nCon quale livello vuole continuare?\n\nTutto ciò che ha imparato resta",
    "level_offer_stay": "Restare a {current}",
    "level_down_offer": "Al livello <b>{current}</b> per ora ci sono parecchi errori\n\nPassare a <b>{previous}</b>?\n\nLe parole saranno più facili, e tutto ciò che ha imparato resta",
    "level_down_yes": "Sì, passare a {previous}",
    "level_down_done": "Il suo livello ora è <b>{previous}</b>\n\nLe parole saranno più facili",
})


# ============================================================================
# ЗАЧЕМ УЧИШЬ — ОПРОС, ВСТРОЕННЫЙ В ПЕРВОЕ НАЖАТИЕ
#
# Режим «по категории» работает, и им пользуются ТРИ человека из 233:
# он спрятан третьим уровнем настроек. Каждая кнопка здесь И отвечает
# на вопрос, И начинает первый круг — шага не прибавилось.
# ============================================================================
TEXTS.update({
    "goal_question": "A cosa le serve la lingua? Sceglieremo le parole di conseguenza.",
    "goal_work": "Per lavoro",
    "goal_travel": "Per viaggiare",
    "goal_living": "Per vivere all'estero",
    "goal_study": "Per studio",
    "goal_any": "Solo imparare parole",
})


# ============================================================================
# ВСТУПИТЕЛЬНЫЙ БЛОК /start
#
# Сюда возвращаются, только набрав команду руками, — то есть затем,
# чтобы понять, что это за бот и что он умеет. Прежний текст вместо
# этого перечислял кнопки, которые человек видит перед собой, и обещал
# «Помощь» среди них, откуда она уехала в настройки.
# ============================================================================
TEXTS.update({
    "intro_games": "Qui ogni parola si impara con cinque giochi: leggerla, ricordarla dal significato, sentirla, dirla ad alta voce e abbinarla sulla tavola.\nOgni lezione li mescola per lei.",
    "intro_numbers": "12.902 parole · 20 argomenti · 6 livelli\n{languages} in qualsiasi coppia: per esempio il polacco tramite l'inglese.",
    "intro_menu_settings": "lingua, giochi della lezione, promemoria",
    "intro_menu_stats": "i suoi progressi",
    "intro_menu_rating": "la classifica del mese",
    "intro_menu_learn": "una lezione",
    "intro_menu_title": "Cosa c'è dove:",
})


# ============================================================================
# ЗАЧЕМ УЧУ — ЭКРАН НАСТРОЙКИ
#
# Без него цель осталась бы пустой навсегда у всех 233 нынешних
# пользователей: онбординг у них давно позади. Та же дыра, что была у
# состава занятия — колонка есть, экрана нет.
# ============================================================================
TEXTS.update({
    "settings_btn_goal": "Obiettivo",
    "settings_goal_title": "<b>A cosa mi serve</b>",
    "settings_goal_description": "Le parole del suo argomento arriveranno per prime. La difficoltà segue comunque il suo livello, e ciò che ha imparato continua a tornare per il ripasso.",
    "settings_goal_set": "Obiettivo salvato",
    "settings_goal_line": "Obiettivo: <b>{goal}</b>",
    "settings_goal_none": "non scelto",
})


# ============================================================================
# ДОСКА СОПОСТАВЛЕНИЯ — ЧЕТВЁРТАЯ ИГРА
#
# Пять слов слева, их значения справа, стоят не напротив друг друга.
# Это НЕ четвёртый навык: сопоставление проверяет узнавание
# написанного, то есть то же, что карточка, только задачу делает легче
# — последняя пара достаётся бесплатно. Поэтому в прогресс идут лишь
# пары, сошедшиеся с первой попытки, и никогда последняя.
# ============================================================================
TEXTS.update({
    "match_title": "<b>Trovare le coppie</b>",
    "match_progress": "Abbinate: {matched} su {total}",
    "match_errors": "✗ errori: {count}",
    "match_hint": "Tocchi una parola da un lato, poi la sua coppia dall'altro.",
    "match_wrong": "✗ Non è una coppia",
    "match_done": "<b>Tavola completata!</b>",
    "match_done_counted": "Conteggiate nei progressi: {counted} su {total}. Contano solo le coppie trovate al primo tentativo, e mai l'ultima: a quel punto non c'è più scelta.",
    "match_btn_again": "Un'altra tavola",
    "match_not_ready": "Non ancora: per una tavola servono {need} parole conosciute, e lei ne ha {have}. Si eserciti con le carte «Leggo»: la sbloccano.",
})

TEXTS["match_back_to_round"] = "Torniamo alla lezione."

TEXTS.update({
    "settings_btn_match": "Tavola nella lezione",
    "settings_match_title": "<b>Tavola nella lezione</b>",
    "settings_match_description": "In ogni lezione, a metà, una tavola prende il posto di una domanda: cinque parole e cinque significati da abbinare. Usa solo parole conosciute, quindi compare quando ne ha almeno dieci.",
    "match_state_on": "La tavola è attiva: arriva a metà lezione.",
    "settings_match_short_on": "con la tavola",
    "settings_channels_short_one": "solo «Leggo»",
    "settings_channels_short_some": "{count} giochi su {total}",
    "settings_channels_short_all": "tutti i giochi",
    "plural_words": "parola|parole",
    "plural_points": "punto|punti",
    "plural_days": "giorno|giorni",
    "settings_audio_short_off": "senza audio",
    "settings_audio_short_on": "con audio",
    "settings_match_short_off": "senza tavola",
    "match_state_off": "La tavola è disattivata: la lezione è solo domande.",
})

# ============================================================================
# СООБЩЕНИЯ ПО ИНИЦИАТИВЕ БОТА — патч 2.1 «Вовлечение» (`nudge_texts`).
# Голос и запрет значков — в ru.py; номера вариантов `_N` те же (тест).
# ============================================================================
TEXTS.update({
    "plural_lessons": "lezione|lezioni",
    "nd_teaser_quiz_1": "Ricorda cosa significa {word}? {meaning}",
    "nd_teaser_quiz_2": "Si metta alla prova: {word} - {meaning}",
    "nd_teaser_quiz_3": "Una delle sue parole: {word} - {meaning}",
    "nd_teaser_quiz_4": "Come si traduce {word}? {meaning}",
    "nd_teaser_new_1": "Per esempio: {word} - {meaning}",
    "nd_teaser_new_2": "Prima parola: {word} - {meaning}",
    "nd_teaser_new_3": "Come si traduce {word}? La traduzione è nascosta - la tocchi: {meaning}",
    "nd_streak_head_1": "<b>{name}, serie: {days} di fila</b>",
    "nd_streak_head_2": "<b>{name}, {days} di fila. Continuiamo?</b>",
    "nd_streak_head_3": "<b>{name}, già {days} di fila</b>",
    "nd_streak_head_4": "<b>{name}, {days} senza pause</b>",
    "nd_streak_head_5": "<b>{name}, ancora una lezione e saranno {next_days} di fila</b>",
    "nd_streak_head_6": "<b>{name}, la sua serie la aspetta: {days}</b>",
    "nd_streak_head_7": "<b>{days} di fila, {name}</b>",
    "nd_streak_head_8": "<b>{name}, {days} di fila. Ancora una lezione oggi?</b>",
    "nd_body_learned_1": "Parole conosciute: {known_n} · imparate: {learned}",
    "nd_body_learned_2": "Parole in studio: {in_work} · imparate: {learned}",
    "nd_body_learned_3": "Parole conosciute: {known_n}, di cui imparate: {learned}.",
    "nd_body_known_1": "Parole conosciute: {known_n}. Ogni lezione ne aggiunge di nuove.",
    "nd_body_known_2": "Parole in studio: {in_work}. Le prime parole imparate sono vicine.",
    "nd_body_known_3": "Parole conosciute: {known_n}.",
    "nd_streak_close_1": "Piccoli passi portano a grandi risultati.",
    "nd_streak_close_2": "Un po' ogni giorno: è così che le parole restano.",
    "nd_streak_close_3": "Una lezione oggi allungherà la serie.",
    "nd_streak_close_4": "Una lezione dura circa {minutes_n} minuti.",
    "nd_streak_close_5": "La costanza conta più della durata della lezione.",
    "nd_progress_head_known": "<b>{name}, parole conosciute: {known_n}</b>",
    "nd_progress_head_1": "<b>{name}, le sue parole sono da ripassare</b>",
    "nd_progress_head_2": "<b>{name}, ha qualche minuto?</b>",
    "nd_progress_head_3": "<b>{name}, riprendiamo da dove eravamo rimasti?</b>",
    "nd_progress_head_4": "<b>{name}, torniamo alle sue parole?</b>",
    "nd_progress_head_5": "<b>{name}, un buon momento per ripassare le parole</b>",
    "nd_due_1": "Parole da ripassare: {due_n}. I tempi li calcola il bot.",
    "nd_due_2": "È ora di ripassare {due} prima che svaniscano.",
    "nd_due_3": "Parole da ripassare: {due_n}. Il bot ha già scelto da dove cominciare.",
    "nd_due_many_1": "Ci sono parecchie parole da ripassare: la lezione comincerà dalle più importanti.",
    "nd_due_many_2": "I ripassi si sono accumulati. Basta una lezione al giorno, il resto può aspettare.",
    "nd_praise_1": "Lezioni completate: {lessons_n}. Poco alla volta, ma con costanza.",
    "nd_praise_2": "Lezioni completate: {lessons_n}. Piccoli passi portano a grandi risultati.",
    "nd_praise_3": "Lezioni completate: {lessons_n}, e ognuna ha aggiunto parole.",
    "nd_short_1": "Una lezione dura circa {minutes_n} minuti.",
    "nd_short_2": "Bastano pochi minuti.",
    "nd_first_head_words": "<b>{name}, ieri ha imparato {words}</b>",
    "nd_first_head_1": "<b>{name}, un buon inizio</b>",
    "nd_first_head_2": "<b>{name}, ripassiamo le parole di ieri?</b>",
    "nd_first_body_1": "Ripassare il giorno dopo aiuta le parole a restare.",
    "nd_first_body_2": "Il secondo giorno è il momento migliore per fissare le parole nuove.",
    "nd_first_close_1": "Bastano pochi minuti.",
    "nd_first_close_2": "Una lezione dura circa {minutes_n} minuti.",
    "nd_kept_head_1": "<b>{name}, tutto è al suo posto</b>",
    "nd_kept_head_2": "<b>{name}, le sue parole sono salvate</b>",
    "nd_kept_head_3": "<b>{name}, è passato un po' di tempo</b>",
    "nd_kept_body_1": "Parole conosciute: {known_n} · imparate: {learned}. Non si è perso nulla - la lezione comincerà da quelle da rinfrescare.",
    "nd_kept_body_2": "Tutto ciò che ha imparato è salvato. La lezione comincerà dalle parole da rinfrescare.",
    "nd_kept_body_3": "Le pause capitano a tutti. Può ricominciare con una lezione breve.",
    "nd_kept_best": "Serie migliore: {best} di fila. Una nuova comincia con una lezione.",
    "nd_farewell_head_1": "<b>{name}, non ci saranno altri promemoria</b>",
    "nd_farewell_head_2": "<b>{name}, l'ultimo promemoria</b>",
    "nd_farewell_body_1": "Il bot non scriverà più finché non tornerà. È tutto salvato: parole conosciute {known_n}, imparate {learned}. Può continuare quando vuole con il pulsante qui sotto.",
    "nd_farewell_body_2": "Sembra che ora non sia il momento per le lezioni - va benissimo. Non ci saranno altri promemoria. Le sue parole e i suoi progressi sono salvati.",
    "nd_start_head_1": "<b>{name}, le sue prime parole la aspettano</b>",
    "nd_start_head_2": "<b>{name}, cominciamo?</b>",
    "nd_start_head_3": "<b>{name}, la prima lezione dura circa {minutes_n} minuti</b>",
    "nd_start_body_1": "Il bot sceglierà le parole più utili per il suo livello e terrà conto di quando ripassarle.",
    "nd_start_body_2": "Cominciamo dalle parole più frequenti, quelle che si sentono ogni giorno.",
    "nd_start_body_3": "Non serve prepararsi: {questions} domande, e poi il bot le dirà cosa ripassare e quando.",
    "nd_start3_head_1": "<b>{name}, vuole provare?</b>",
    "nd_start3_head_2": "<b>{name}, le sue prime parole la aspettano ancora</b>",
    "nd_start_last_head": "<b>{name}, l'ultimo invito</b>",
    "nd_start_last_body": "Non ci saranno altri promemoria. Se vuole cominciare, la prima lezione dura circa {minutes_n} minuti - il pulsante è qui sotto.",
    "nd_btn_optin": "Promemoria alle {time}",
    "nd_btn_stop": "Niente più messaggi",
    "nd_auto_time": "Le manderò un promemoria ogni giorno alle {time}. Può cambiare l'orario",
    "nd_btn_change_time": "Cambiare orario",
    "nd_optin_done": "✓ Fatto: il promemoria arriverà alle <b>{time}</b>\n\nPuò cambiare l'ora nelle impostazioni",
})
