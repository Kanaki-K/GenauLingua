"""
Deutsche Lokalisierung für GenauLingua Bot

Набор ключей совпадает с остальными локалями — это проверяется тестом
test_all_locales_have_identical_key_sets. Подсказки режимов перевода
(settings_mode_hint_*) намеренно оставлены на языке самого режима: так они
устроены во всех локалях.
"""

TEXTS = {
    # ============================================================================
    # HAUPTMENÜ
    # ============================================================================
    "btn_learn_words": "Wörter lernen",
    "btn_stats": "Statistik",
    "btn_settings": "Einstellungen",
    "btn_help": "Hilfe",
    "btn_back": "Zurück",
    "menu_placeholder": "Wählen Sie eine Aktion …",

    # ============================================================================
    # BEGRÜSSUNG UND START
    # ============================================================================
    "welcome_title": "<b>Hallo, {name}!</b>",








    # ============================================================================
    # ERINNERUNGEN
    # ============================================================================
    "notif_title": "<b>Erinnerungen</b>",
    "notif_status": "Status: {status}",
    "notif_status_on": "Ein",
    "notif_status_off": "Aus",
    "notif_time": "Zeit: {time}",
    "notif_days": "Tage: {days}",
    "notif_timezone": "Zeitzone: {timezone}",
    "notif_hint": "Die Erinnerung kommt zur gewählten Zeit in Ihrer Zeitzone.",
    "notif_hint_off": "Schalten Sie die Erinnerungen ein — so bleibt Ihre Serie leichter bestehen.",

    "notif_btn_toggle_on": "Erinnerungen: Ein",
    "notif_btn_toggle_off": "Erinnerungen: Aus",
    "notif_btn_time": "Zeit: {time}",
    "notif_btn_days": "Tage wählen",
    "notif_btn_timezone": "Zeitzone ändern",

    "notif_timezone_title": "<b>Wählen Sie Ihre Zeitzone</b>",
    "notif_timezone_current": "Aktuell: {timezone}",
    "notif_timezone_prompt": "Wählen Sie eine Stadt in Ihrer Zeitzone:",
    "notif_timezone_more": "Andere Stadt wählen",
    "notif_timezone_back": "Zurück",
    "notif_timezone_set": "✓ Zeitzone gesetzt: {city}",

    "notif_time_title": "<b>Wählen Sie die Uhrzeit der Erinnerung</b>",
    "notif_time_current": "Aktuelle Zeit: {time}",
    "notif_time_timezone": "Zeitzone: {timezone}",
    "notif_time_hint": "Die Erinnerung kommt an den gewählten Tagen zur gewählten Zeit.",
    "notif_time_set": "✓ Zeit gesetzt: {time}",

    "notif_days_title": "<b>Wählen Sie die Tage für Erinnerungen</b>",
    "notif_days_hint": "Tippen Sie auf einen Tag, um ihn ein- oder auszuschalten.\n✓ — Tag an\n✗ — Tag aus\n\nWenn Sie fertig sind, tippen Sie auf „Speichern“.",
    "notif_days_all": "Alle Tage",
    "notif_days_weekdays": "Wochentage (Mo–Fr)",
    "notif_days_save": "Speichern",
    "notif_days_saved": "✓ Tage gespeichert!",
    "notif_days_all_selected": "✓ Alle Tage ausgewählt",
    "notif_days_weekdays_selected": "✓ Wochentage ausgewählt (Mo–Fr)",
    "notif_days_none": "Wählen Sie mindestens einen Tag für Erinnerungen!",

    "notif_toggle_on": "Erinnerungen eingeschaltet!",
    "notif_toggle_off": "Erinnerungen ausgeschaltet",

    "day_mon": "Mo",
    "day_tue": "Di",
    "day_wed": "Mi",
    "day_thu": "Do",
    "day_fri": "Fr",
    "day_sat": "Sa",
    "day_sun": "So",

    "notif_btn_back": "Zurück zu den Einstellungen",

    "notif_default_name": "Freund",



    # EIN GRUND ZURÜCKZUKOMMEN — und er muss stimmen

    # ============================================================================
    # EINSTELLUNGEN
    # ============================================================================
    "settings_title": "<b>Einstellungen</b>",
    "settings_mode": "Richtung: <b>{mode}</b>",
    "settings_language": "Bot-Sprache: <b>{language}</b>",

    "settings_btn_quiz_mode": "Niveau und Themen",
    "settings_btn_change_language": "Bot-Sprache",
    "settings_btn_notifications": "Erinnerungen",

    "settings_quiz_mode_line": "Niveau: <b>{mode}</b>",
    "start_pick_language": "Wählen Sie Ihre Sprache",
    "onboard_your_lang": "✓ Ihre Sprache: {language}",
    "onboard_change_hint": "Sie können sie jederzeit ändern: Befehl /language.",
    "onboard_phone_hint": "Ihr Telegram ist auf Deutsch. Falls Sie die Sprache versehentlich gewählt haben, tippen Sie auf „{back}“.",
    "lang_confirm_learning": "Sie lernen: {language}",
    "lang_progress_kept": "Der Fortschritt bleibt für jede Sprache erhalten.",
    "btn_done": "Fertig",
    "btn_change_learning": "Lernsprache ändern",
    "intro_pair": "Sie lernen {learning} mit Übersetzung ins {native}.",
    "intro_menu_language": "Bot-Sprache",
    "plural_languages": "Sprache|Sprachen",
    "cmd_start": "Start und was der Bot kann",
    "cmd_language": "Bot-Sprache",
    "cmd_settings": "Einstellungen",
    "cmd_help": "Hilfe",

    "language_changed": "✓ Sprache geändert: {language}",
    "user_not_found": "✗ Nutzer nicht gefunden. Bitte senden Sie /start.",

    # Namen der Oberflächensprachen — jeweils in der Sprache selbst
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

    # Übersetzungsrichtungen

    # ============================================================================
    # QUIZ-MODUS
    # ============================================================================
    "qmode_title": "<b>Niveau und Themen</b>",
    "qmode_current": "Jetzt: <b>{mode}</b>",
    "qmode_choose": "Wählen Sie, wie Sie Wörter lernen möchten.\nSie können das jederzeit ändern — der Fortschritt bleibt erhalten.",

    "qmode_btn_level": "Nach Niveau",
    "qmode_btn_category": "Nach Thema",
    "qmode_btn_all": "Alle Wörter",
    "qmode_btn_difficult": "Schwierige",

    "qmode_level_short": "{level}",
    "qmode_category_short": "{category}",
    "qmode_all_short": "Alle Wörter",
    "qmode_difficult_short": "Schwierige Wörter",

    "qmode_level_title": "<b>Niveau wählen</b>",
    "qmode_level_desc": "Von den ersten Wörtern bis zur freien Diskussion. Alle Niveaus sind offen — wählen Sie Ihres.\n\n• A1–A2 — Grundwortschatz\n• B1–B2 — sicher kommunizieren\n• C1–C2 — die Sprache frei beherrschen",
    "qmode_level_set": "✓ Modus: Nach Niveau ({level})",

    "qmode_category_title": "<b>Thema wählen</b>",
    "qmode_category_desc": "Von Essen bis Wissenschaft — wählen Sie das Thema, das Sie brauchen.\n\nJedes Thema enthält Wörter aller Niveaus.",
    "qmode_category_set": "✓ Modus: {category}",

    # Namen der Kategorien
    "cat_arbeit_beruf": "Arbeit",
    "cat_bildung_lernen": "Lernen",
    "cat_einkaufen_geld": "Einkaufen",
    "cat_emotionen_charakter": "Gefühle",
    "cat_essen_trinken": "Essen",
    "cat_freizeit_sport": "Sport",
    "cat_gesundheit_medizin": "Gesundheit",
    "cat_grammatik": "Grammatik",
    "cat_kleidung_mode": "Kleidung",
    "cat_kommunikation": "Kommunikation",
    "cat_kultur_kunst": "Kultur",
    "cat_mensch_familie": "Familie",
    "cat_natur_wetter": "Natur",
    "cat_recht_staat": "Recht",
    "cat_reisen_transport": "Reisen",
    "cat_technik_digital": "Technik",
    "cat_wirtschaft": "Wirtschaft",
    "cat_wissenschaft": "Wissenschaft",
    "cat_wohnen_haus": "Wohnen",
    "cat_zeit_alltag": "Alltag",

    "qmode_all_set": "✓ Modus: Alle Wörter",

    "qmode_difficult_set": "✓ Modus: Schwierige Wörter",
    "qmode_difficult_few": "Schwierige Wörter bisher: {count} — nötig sind mindestens 4.\nMachen Sie noch ein paar Lektionen!",
    "qmode_difficult_empty": "Sie haben bisher keine schwierigen Wörter.\nMachen Sie ein paar Lektionen!",

    "quiz_btn_change_mode": "Niveau und Themen",
    "quiz_btn_report_error": "Fehler melden",
    "report_btn_confirm": "✓ Bestätigen ({count})",
    "report_btn_send": "Senden",
    "report_kind_text": "Übersetzung",
    "report_kind_example": "Beispiel",
    "report_kind_audio": "Aussprache",
    "report_pick_hint": "Was stimmt nicht? Markieren Sie es und tippen Sie auf „Senden“",
    "report_btn_sent": "✓ Meldung gesendet",
    "report_sent_one": "✓ Danke!\nWenn sich der Fehler bestätigt, erhalten Sie +{points}.",
    "report_approved_example": "✓ Ihre Meldung zum Beispielsatz von <b>{word}</b> wurde angenommen\n\nDas Beispiel wird korrigiert\n\n+{points} Punkte für die Rangliste des Monats - danke",
    "report_no_words": "Keine Wörter zum Melden",
    "report_none_selected": "Wählen Sie mindestens ein Wort",
    "report_pick_kind": "{count} Wort(e) ausgewählt. Was ist falsch — die Übersetzung oder die Aussprache?",
    "report_sent": "✓ Meldungen gesendet: {count} — danke!\nWird der Fehler bestätigt, bekommen Sie +{points}.",
    "report_daily_limit": "Tageslimit für Meldungen erreicht (max. 20)",
    "report_all_reported": "✓ Alle Wörter aus dieser Lektion sind schon gemeldet",
    "report_already_sent": "✓ Schon früher gesendet",
    "report_btn_kind_text": "Falsche Übersetzung",
    "report_btn_kind_audio": "Falsche Aussprache",
    "report_sent_audio": "✓ Meldungen gesendet: {count} — danke!\nMeldungen zur Aussprache sind besonders wertvoll: Eine Maschine hört die Betonung nicht.\nWird der Fehler bestätigt, bekommen Sie +{points}.",
    "report_approved": "✓ Ihre Meldung zu <b>{word}</b> wurde angenommen - wir korrigieren die Übersetzung\n\n+{points} Punkte für die Rangliste des Monats - danke, das Wörterbuch wird besser für alle",
    "award_won": "{mark} Platz {rank} in der Rangliste für {month}\n\n{bonus} Punkte wurden Ihrem Gesamtstand gutgeschrieben",
    "report_approved_audio": "✓ Ihre Meldung zur Aussprache von <b>{word}</b> wurde angenommen\n\nDie Aussprache wird neu erzeugt\n\n+{points} Punkte für die Rangliste des Monats - danke",
    # ============================================================================
    # QUIZ
    # ============================================================================
    "quiz_no_level": "Wählen Sie zuerst Ihr Niveau mit dem Befehl /start",
    "quiz_error_generation": "✗ Beim Vorbereiten der Lektion ist ein Fehler aufgetreten.\nVersuchen Sie es noch einmal über /start.",
    "quiz_no_words": "✗ Für dieses Niveau gibt es leider noch keine Wörter.\nWählen Sie ein anderes Niveau.",

    "quiz_question_number": "{current} / {total}",

    "quiz_correct": "✓ <b>Richtig</b>",
    "quiz_wrong": "✗ <b>Falsch</b>",
    "quiz_correct_answer": "Richtige Antwort:",

    "quiz_btn_next": "Weiter →",

    "quiz_answer_already_counted": "Ihre Antwort wurde bereits gewertet. Machen wir weiter?",
    "quiz_btn_repeat_errors": "Fehler wiederholen",
    "lesson_resume_prompt": 'Sie haben eine nicht beendete Lektion: {done} von {total}',
    "btn_lesson_resume": 'Fortsetzen',
    "btn_lesson_new": 'Neu beginnen',
    "speech_offer_text": 'Laut sprechen passt gerade nicht? Kein Problem. „Ich spreche“ aus den Lektionen entfernen? In den Einstellungen können Sie es jederzeit zurückholen',
    "btn_speech_off": '„Ich spreche“ entfernen',
    "btn_speech_keep": 'Behalten',
    "speech_off_done": 'Erledigt, „Ich spreche“ ist entfernt. Zurückholen können Sie es in den Einstellungen',
    "speech_invite_text": '🎤 Möchten Sie versuchen, laut zu antworten? Der Bot hört Ihre Aussprache an und sagt Ihnen, wenn etwas nicht stimmt. Ganz freiwillig',
    "btn_speech_try": 'Ausprobieren',
    "btn_speech_later": 'Nicht jetzt',
    "speech_try_done": 'Prima! „Ich spreche“ kommt in Ihren nächsten Lektionen. Zum Antworten halten Sie das Mikrofon-Symbol unten rechts gedrückt und sagen das Wort',

    "quiz_completed": "<b>Lektion geschafft</b>",
    "quiz_result_correct": "Richtig: <b>{correct}/{total}</b>",
    "quiz_result_percentage": "Ergebnis: <b>{percentage}%</b>",
    "quiz_result_details": "<b>Einzelheiten:</b>",
    "quiz_result_errors": "Fehler: {count}",

    # LOB AM ENDE DER LEKTION — nur für das, was wirklich geschah
    "praise_first_round": "Erste Lektion geschafft. Ab jetzt kommen Wörter zurück — so bleiben sie hängen.",
    "praise_first_learned": "Erstes Wort gelernt: drei richtige Antworten hintereinander, an verschiedenen Tagen.",
    "praise_learned": "Gelernte Wörter in dieser Lektion: {count}",
    "praise_best_streak": "Persönlicher Rekord: {days_word} in Folge",
    "praise_milestone": "Schon {count} Wörter in Arbeit",
    "praise_first_speech": "Erste richtige Antwort per Stimme",
    "praise_first_audio": "Erste richtige Antwort nach Gehör",
    "praise_comeback": "Willkommen zurück. Die Pause dauerte {days_word}.",
    "praise_perfect": "Lektion ohne einen Fehler",
    "praise_streak": "Serie: {days_word} in Folge",
    "praise_freeze_saved": "Gestern gab es eine Pause, aber der Serienschutz hat Ihre Serie gerettet: {days_word} in Folge. Der nächste Schutz ist in einer Woche wieder frei.",
    "praise_streak_3": "Drei Tage in Folge — die Gewohnheit beginnt.",
    "praise_streak_7": "Eine ganze Woche in Folge! Das ist die wichtigste Hürde: Ab jetzt trägt die Gewohnheit sich selbst.",
    "praise_streak_14": "Zwei Wochen in Folge — starkes Tempo.",
    "praise_streak_30": "Ein Monat in Folge! Das ist jetzt eine echte Gewohnheit.",
    "praise_new_words": "Neue Wörter: {count}",
    "praise_returned": "Wiedererkannt: {count}",
    "praise_progress": "Wörter in Arbeit: {count} · noch {left} bis {target}",
    "praise_progress_top": "Wörter in Arbeit: {count}",
    "praise_points": "Punkte: +{points}",

    "quiz_repeat_title": "<b>Fehler wiederholen</b>",
    "quiz_no_errors": "✓ Sie hatten keine Fehler!",
    "quiz_error_next": "✗ Die nächste Frage konnte nicht geladen werden.",

    # ============================================================================
    # STATISTIK
    # ============================================================================
    "stats_no_level": "<b>Wählen Sie zuerst ein Niveau!</b>\n\nNutzen Sie den Befehl /start, um zu beginnen.",





    # ============================================================================
    # HILFE
    # ============================================================================
    "help_title": "<b>Hilfe — GenauLingua</b>",
    "help_description": "Hier: wie die Übungen funktionieren und wie Sie die Community erreichen.",
    "help_choose": "Wählen Sie einen Bereich:",

    "help_btn_how_to_use": "So funktioniert es",
    "help_btn_community": "Community",

    "help_how_to_use_title": "<b>So benutzen Sie den Bot</b>",


    "help_community_title": "<b>GenauLingua Community</b>",
    "help_community_text": """ <b>t.me/genaulingua_chat</b>

Im Chat:
Sie erfahren zuerst von Neuerungen
Fehler gefunden — schreiben Sie uns oder schicken Sie einen Screenshot
Fehler in der Übersetzung — melden Sie ihn, wir korrigieren
Ideen und Wünsche — wir lesen alles und nehmen es auf
Austausch mit anderen Lernenden


Je lebendiger die Community, desto besser wird der Bot. Nur keine Scheu! """,


    # ============================================================================
    # PLATZIERUNG
    # ============================================================================
    "rating_not_active": "✗ Die Platzierung ist noch nicht aktiv.",
    "rating_not_in_ranking": "Sie sind noch nicht in der Rangliste",
    "rating_start_quiz": "Machen Sie Ihre erste Lektion!",
    "rating_join_by_lesson": "Ihre Punkte für Meldungen ({score}) sind gutgeschrieben. Absolvieren Sie eine Lektion, um in die Monatsrangliste zu kommen.",
    "release_notes_2026_10": "✨ <b>GenauLingua 2.0 — wir haben den Bot von Grund auf neu gebaut</b>\n\n<b>Nicht nur Deutsch.</b> Lernen Sie Ukrainisch, Englisch, Türkisch, Deutsch, Polnisch oder Russisch — aus jeder dieser Sprachen. Die Oberfläche gibt es ebenfalls in allen sechs.\n\n<b>Sechs Spiele statt einem.</b> Früher gab es nur „Übersetzung wählen“.\n\nJetzt wechseln sich die Spiele in jeder Lektion ab:\n📖 Ich lese · 💭 Ich erinnere · 🎧 Ich höre · 🎤 Ich spreche · 🧩 Finden Sie die Paare · 🧱 Ich baue\n\nBei „Ich spreche“ antworten Sie mit der Stimme, bei „Ich baue“ setzen Sie einen Satz aus Wörtern zusammen — der Bot zeigt, welches Wort nicht passt.\n\n<b>Der Bot spricht.</b> Jedes Wort und jedes Beispiel ist mit natürlicher Stimme vertont.\n\n<b>Neues Aussehen.</b> Neues Menü, ein aufgeräumter Chat ohne überflüssige Nachrichten, ein Startbildschirm mit Ihren Fähigkeiten, übersichtliche Statistik, neuer Avatar und neue Begrüßung.\n\n<b>Das ganze Wörterbuch wurde geprüft</b> — alle 12.902 Wörter, Übersetzungen und Beispiele.\n\n<b>Der Bot passt sich an:</b> Er bringt Wörter zurück, kurz bevor Sie sie vergessen, und schlägt das nächste Niveau vor, wenn es leicht wird.\n\n<b>Fehler behoben:</b> Ihre Tagesserie wird richtig gezählt, und die Ranglistenpunkte sind fair — sie belohnen Einsatz. Auch „gelernt“ ist jetzt ehrlich: Ein Wort gilt als gelernt, wenn Sie es dreimal hintereinander an verschiedenen Tagen richtig hatten; alle geübten Wörter sehen Sie unter „Wörter in Arbeit“.\n\n<b>Erinnerungen sind eingeschaltet</b> — zu Ihrer Zeit. Ändern oder ausschalten: Einstellungen → Bot → Erinnerungen.\n\n⭐ Einen Fehler gefunden? Melden Sie ihn direkt im Ergebnis der Lektion: Jede bestätigte Meldung bringt +15 Punkte.\n\nIhr Fortschritt und Ihre Punkte bleiben erhalten. Probieren Sie es aus — eine Lektion dauert nur ein paar Minuten.",
    "release_notes_2026_10_22": '✨ <b>GenauLingua 2.2 - jetzt zehn Sprachen</b>\n\nGuten Tag!\n\nEin großes Update ist da:\n\n<b>4 neue Sprachen</b>\n\n🇮🇹 Italienisch, 🇪🇸 Spanisch, 🇫🇷 Französisch und 🇨🇿 Tschechisch - Sie können sie von jeder Sprache des Bots aus lernen\nJede hat über 12.000 Wörter mit Beispielen, alles vertont\n\n<b>Eine Rangliste, in der es um etwas geht</b>\n\nMonatsmedaillen 🥇🥈🥉, eine Krone 👑 für Platz 1 unter allen, die Ihre Sprache lernen, und Ränge, die mit Ihnen wachsen. Die ersten Ergebnisse nach den neuen Regeln - am 1. November\n\n<b>Die Serie verzeiht eine Pause</b>\n\nEinmal pro Woche rettet der Serienschutz 🧊 Ihre Serie, wenn Sie einen Tag auslassen\n\n<b>Außerdem:</b> Fehler in Übersetzung, Beispiel oder Aussprache melden - direkt unter der Antwort (+15 Punkte pro bestätigter Meldung)\n\nBekannte Wörter lernen Sie schneller, und Updates des Bots unterbrechen keine Lektion mehr\n\nDanke, dass Sie mit uns lernen und Fehler melden - so wird der Bot für alle besser 💙\n\nAlles Neue kurz und anschaulich: <a href="{url}">neu in 2.2</a>',
    "btn_release_news": 'Was ist neu →',


    "table_empty": "Noch nimmt niemand teil.\nMachen Sie die erste Lektion und eröffnen Sie die Rangliste!",
    "table_you_not_ranked": "Sie sind noch nicht in der Rangliste",
    "rating_tab_month": "Monat",
    "rating_tab_alltime": "Gesamt",
    "rating_crown_rule": "Platz 1 erhält die Krone für den ganzen nächsten Monat",
    "rating_screen_title": "<b>Rangliste · {month} {year}</b>",
    "rating_screen_title_alltime": "<b>Rangliste · Gesamt</b>",
    "rating_you": "<b>Sie: #{rank} von {total}</b> · {points}",
    "rating_results_in": "Monatsergebnis in {days}",
    "info_title": "<b>So funktioniert die Rangliste</b>",
    "info_month": "<b>Monat</b> — alle. Die besten drei erhalten 🥇 🥈 🥉 (ab 3 Lektionen).",
    "info_lang": "<b>Sprache</b> — wer Ihre Sprache lernt. Platz 1 erhält 👑 für den nächsten Monat.",
    "info_alltime": "<b>Gesamt</b> — alle Punkte. Medaillen heben Ihren Rang 🌱 🌳 🌙 🪐 ☀️",
    "info_points_title": "<b>Punkte</b>",
    "info_points": "Antwort +1 · nach Gehör +2 · laut +3\nLektion +10 · Wort gelernt +3\nTage in Folge — bis +10 · Treffsicherheit über 60% — Bonus\nBestätigte Meldung +{points}",
    "title_sprout": "Spross",
    "title_tree": "Baum",
    "title_moon": "Mond",
    "title_planet": "Planet",
    "title_sun": "Sonne",
    "title_galaxy": "Galaxie",
    "btn_rating_info": "Info",
    "card_medal_need": "Für eine Medaille nötige Lektionen: {need} · Sie haben {have}",
    "card_crown_small": "Um die Krone geht es, wenn die Sprache 3+ Personen mit 3+ Lektionen hat",
    "summary_place": "↑ Platz im Monat: {rank}",
    "summary_gap": "bis {name} {gap}",
    "summary_record": "Neuer Monatsrekord: {points}",
    "collection_title": "<b>Sammlung</b> · {open} von {total} freigeschaltet",
    "collection_locked": "▫️ ???",
    "ach_streak_7": "7 Tage in Folge",
    "ach_streak_30": "30 Tage in Folge",
    "ach_streak_100": "100 Tage in Folge",
    "ach_streak_365": "365 Tage in Folge",
    "ach_streak_1000": "1000 Tage in Folge",
    "ach_words_100": "100 gelernte Wörter",
    "ach_words_1000": "1000 gelernte Wörter",
    "ach_words_3000": "3000 gelernte Wörter",
    "ach_perfect_10": "10 Lektionen ohne Fehler",
    "ach_voice_1000": "1000 richtige gesprochene Antworten",
    "ach_editor": "Wörterbuch-Redaktion: 5 angenommene Meldungen",
    "ach_polyglot": "Polyglott: 100 Wörter in zwei Sprachen",
    "award_month_header": "<b>Ergebnisse des Monats</b>",
    "award_crown": "👑 Krone: Sie sind die Nummer eins in {language}. Tragen Sie sie den ganzen nächsten Monat",
    "award_glory": "+{glory} Ruhm",
    "award_new_title": "Neuer Rang: {mark} {name}",
    "nd_overtaken": "Sie wurden in der Monatsrangliste überholt.\nIhr Platz: {rank} · bis {name} {gap}.",
    "nd_finish": "Bis Monatsende: {days}.\nIhr Platz: {rank} · bis zur Medaille {gap}.",

    # ============================================================================
    # STATISTIK (NEU)
    # ============================================================================
    "stats_header": "<b>Ihre Statistik</b>",
    "stats_in_work_line": "Wörter in Arbeit: {count} · noch {left} bis {target}",
    "stats_in_work_top": "Wörter in Arbeit: {count}",
    "stats_details": "Noch in Übung: {progress}\nNeu: {new}\nSchwierig: {difficult}",
    "stats_achievements_title": "<b>Ihre Erfolge</b>",
    "stats_words_count": "Wörter gelernt: <b>{count}</b>",
    "stats_best_streak_line": "Beste Serie: {days_word}",
    "stats_quizzes_header": "<b>Lektionen · {level}</b>",
    "stats_quizzes_passed_line": "Abgeschlossen: <b>{count}</b>",
    "stats_quizzes_avg_line": "Durchschnitt: <b>{percent}%</b>",
    "stats_quizzes_best_line": "Bestes Ergebnis: <b>{percent}%</b>",
    "stats_quizzes_empty": "Noch keine Lektion abgeschlossen",
    "stats_recent_header": "<b>Letzte Lektionen</b>",
    "stats_explanation": "Wort gelernt = drei richtige Antworten hintereinander, an verschiedenen Tagen",
}

# ============================================================================
# MEHRSPRACHIGKEIT: Lernsprache, Bedeutungssprache und Richtung
# ============================================================================
TEXTS.update({
    # Namen der Sprachen
    "langname_de": "Deutsch",
    "langname_en": "Englisch",
    "langname_ru": "Russisch",
    "langname_uk": "Ukrainisch",
    "langname_tr": "Türkisch",
    "langname_pl": "Polnisch",
    "langname_it": "Italienisch",
    "langname_es": "Spanisch",
    "langname_fr": "Französisch",
    "langname_cs": "Tschechisch",
    # Bindewort für die Aufzählung der Sprachen in Hilfe und Begrüßung
    "and_word": "und",

    # Zeilen im Einstellungsmenü
    "settings_learning_lang_line": "Ich lerne: <b>{language}</b>",

    "settings_btn_learning_lang": "Sprache",

    # Bildschirm «Welche Sprache lernen»
    "learning_lang_title": "<b>Welche Sprache lernen Sie?</b>",
    "learning_lang_description": "Wählen Sie die Sprache, deren Wörter Sie lernen möchten.\nDer Fortschritt wird für jede Sprache getrennt gezählt.",
    "learning_lang_set": "✓ Sie lernen jetzt: {language}",
    # Zeile im Einstellungsmenü und Bildschirm «Aussprache»
    "settings_audio_line": "Aussprache: <b>{state}</b>",
    "settings_btn_audio": "Aussprache",
    "audio_state_on": "ein",
    "audio_state_off": "aus",

    "audio_title": "<b>Aussprache</b>",
    "audio_description": "Das Wort erklingt mit einer natürlich klingenden Stimme. In der Frage das Wort allein, nach der Antwort das Wort zusammen mit dem Beispiel.",
    "audio_current_voice": "Stimme: <b>{voice}</b>",
    "audio_btn_turn_on": "Aussprache einschalten",
    "audio_btn_turn_off": "Aussprache ausschalten",
    "audio_btn_choose_voice": "Stimme wählen",
    "audio_turned_on": "✓ Aussprache eingeschaltet",
    "audio_turned_off": "Aussprache ausgeschaltet",

    "voice_title": "<b>Stimme wählen</b>",
    "voice_description": "Tippen Sie auf eine Stimme, um sie zu hören. Das Häkchen markiert die gewählte.",
    "voice_male": "Männlich",
    "voice_female": "Weiblich",
    "voice_set": "✓ Stimme: {voice}",
    "voice_use": "{voice} wählen",
    "voice_listening": "{voice} läuft",
    "voice_only_one": "Für diese Sprache gibt es eine männliche und eine weibliche Stimme — mehr nicht.",
    "voice_preview_failed": "Die Hörprobe konnte nicht geladen werden. Versuchen Sie es noch einmal.",
})


# ============================================================================
# АПГРЕЙД ПОД ШЕСТЬ ЯЗЫКОВ
#
# Добавлено, когда бот перестал быть «ботом для немецкого»: при первом запуске
# человек теперь выбирает не только язык интерфейса, но и какой язык учить, а
# подсказки направления стали работать на все тридцать пар вместо восьми.
# ============================================================================
TEXTS.update({
    "btn_rating": "Rangliste",
    "friend_fallback": "Freund",
    "onboarding_learning_title": "<b>Welche Sprache lernen Sie?</b>",
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
    "help_how_to_use_text": "<b>Lektion</b>\n{words}, je vier Antworten. Die Spiele wechseln sich von selbst ab: „Ich lese“, „Ich erinnere“, „Ich höre“, „Ich spreche“, „Ich baue“ und die Tafel „Finden Sie die Paare“. Der Bot merkt sich Ihre Fehler und bringt Schwieriges öfter zurück. Nach der Lektion können Sie Ihre Fehler sofort wiederholen.\n\n<b>Aussprache</b>\nIn der Frage erklingt das Wort, nach der Antwort das Wort mit seinem Beispiel. Die Stimme wählen Sie in den Einstellungen — männlich oder weiblich.\n\n<b>Sprachen</b>\n{languages} — in jedem Paar. Der Fortschritt wird für jede Sprache getrennt gezählt; die Rangliste hat die Reiter „Monat“, „Gesamt“ und „Sprache“.\n\n\nEin Wort gilt als <b>gelernt</b> nach drei richtigen Antworten hintereinander, und zwar an verschiedenen Tagen. Ist die erste Antwort auf ein neues Wort richtig, genügt danach noch eine.\nDie <b>Serie</b> zählt Tage in Folge: Eine Lektion am Tag genügt. Ein ausgelassener Tag pro Woche unterbricht sie nicht — der Serienschutz fängt ihn auf.\nFehler in Übersetzung oder Aussprache — dafür gibt es den Knopf „Fehler melden“ unter der Antwort.",
    "help_community_title": "<b>Über den Bot und die Gemeinschaft</b>",
    "help_community_text": "<b>GenauLingua</b> — {language_count} Sprachen, in jeder Kombination: {languages}\n12 900 Wörter A1–C2, jedes mit Beispiel und natürlich klingender Aussprache.\nOberfläche: {interface_languages}\n\n<b>t.me/genaulingua_chat</b>\nFehler, falsche Übersetzungen, Ideen — wir lesen alles. Hinweise zur Aussprache sind besonders willkommen: Eine Maschine hört die Betonung nicht.",
})


# ============================================================================
# ВОПРОС НА СЛУХ
#
# Самого слова на экране нет — иначе слушать незачем. Варианты стоят на
# ИЗУЧАЕМОМ языке: спрашивают «что услышал», а не «что это значит».
# ============================================================================
TEXTS.update({
    "quiz_question_listen": "Hören Sie zu und wählen Sie, was Sie gehört haben:",
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
    "quiz_result_by_ear": "🎧 Nach Gehör: {count}",
})


# ============================================================================
# СОСТАВ ЗАНЯТИЯ
#
# Три канала — три РАЗНЫХ навыка, а не три оформления одного. Экран нужен,
# потому что до него колонка quiz_channels была недостижима: выключить
# вопросы на слух можно было только выключив озвучку целиком.
# ============================================================================
TEXTS.update({
    "settings_btn_channels": "Spiele in der Lektion",
    "settings_channels_line": "Spiele: <b>{channels}</b>",
    "channels_title": "<b>Spiele in der Lektion</b>",
    "channels_description": "Welche Spiele in die Lektion kommen. Ein neues Wort kommt als „Ich lese“-Karte; kennen Sie es, kommt es in anderen Spielen zurück: erinnern, hören, sprechen, einen Satz zusammensetzen. Je mehr Spiele, desto fester sitzt das Wort.",
    "channel_text": "📖 Ich lese",
    "channel_audio": "🎧 Ich höre",
    "channel_speech": "🎤 Ich spreche",
    "channel_build": "🧱 Ich baue",
    "home_scale_build": "Ich baue",
    "quiz_result_built": "🧱 Gebaut: {count}",
    "build_hint": "Setzen Sie den Satz aus den Wörtern unten zusammen — einige davon sind überflüssig",
    "build_btn_check": "Prüfen",
    "build_full": "Alle Plätze sind belegt. Entfernen Sie ein Wort mit ⌫ oder tippen Sie auf „Prüfen“.",
    "build_order_only": "↔ <b>Richtige Wörter, andere Reihenfolge</b>",
    "build_reference": "Richtig:",
    "build_yours": "Ihre Antwort:",
    "build_extra": "Überflüssig: {words}",
    "build_missing": "Es fehlt: {words}",
    "stats_grammar_line": "Grammatik: {correct} von {shown} richtig",
    "quiz_result_recalled": "💭 Erinnert: {count}",
    "home_scale_reverse": "Ich erinnere",
    "channel_reverse": "💭 Ich erinnere",
    "channels_text_always": "„Ich lese“ lässt sich nicht abschalten: Jedes neue Wort kommt zuerst als Karte.",
    "channels_audio_blocked": "🎧 „Ich höre“ und „Ich spreche“ sind nicht verfügbar: Die Aussprache ist ausgeschaltet.",
})


# ============================================================================
# ВОПРОС ВСЛУХ
#
# Ответ приходит голосовым сообщением, а не нажатием. Распознаватель отвечает
# на вопрос «то ли слово сказано», и только на него: качество произношения он
# судить не умеет — он обучен ПОНИМАТЬ акцент, а не замечать его.
# ============================================================================
TEXTS.update({
    "quiz_question_speak": "🎤 Sprechen Sie dieses Wort laut aus — nehmen Sie eine Sprachnachricht auf: Mikrofonsymbol im Telegram-Eingabefeld unten rechts gedrückt halten",
    "speech_btn_reference": "Langsam anhören",
    "speech_btn_skip": "Überspringen",
    "speech_listening": "🎧 Ich höre zu…",
    "speech_not_understood": "Nicht verstanden. Nehmen Sie es noch einmal auf — näher am Mikrofon und etwas lauter.",
    "speech_try_again": "Das klang wie „{heard}“ — noch nicht ganz. Bitte nehmen Sie es noch einmal auf: Versuch {attempt} von {total}.",
    "speech_send_voice": "🎤 Diese Frage wird mit einer Sprachnachricht beantwortet. Halten Sie die Mikrofontaste gedrückt.",
    "speech_skipped": "Übersprungen",
    "speech_not_counted": "Wieder klang es wie „{heard}“. Das zählt weder als richtig noch als Fehler — hören Sie sich an, wie es klingt, und weiter geht’s.",
    "lesson_expired": "Diese Lektion wurde unterbrochen — der Bot wurde aktualisiert oder sie ist längst beendet. Starten Sie eine neue mit der Taste unten.",
    "quiz_result_spoken": "🎤 Gesprochen: {count}",
})


# ============================================================================
# ДОМАШНИЙ ЭКРАН: ТРИ ШКАЛЫ
# ============================================================================
TEXTS.update({
    "home_scale_text": "Ich lese",
    "home_scale_audio": "Ich höre",
    "home_scale_speech": "Ich spreche",
    "home_btn_learn": "Wörter lernen",
    "home_rank": "Platz {rank}",
    "home_hint": "",
    "home_channel_not_ready": "{channel}: noch zu früh. Dafür geeignete Wörter: {ready}, nötig sind mindestens {minimum}. Üben Sie mit Karten — sie schalten die anderen Spiele frei.",
})


# ============================================================================
# НАСТРОЙКИ: ТРИ ГРУППЫ
#
# «Что учу» человек меняет часто, «как мне удобно» ставит один раз. Восемь
# равных пунктов перемешивали то и другое, и первым в списке стоял режим
# викторины, которым не пользуются 96%.
# ============================================================================
TEXTS.update({
    "settings_group_what": "Was ich lerne",
    "settings_group_what_title": "<b>Was ich lerne</b>",
    "settings_group_how": "Wie ich lerne",
    "settings_group_how_title": "<b>Wie ich lerne</b>",
    "settings_group_bot": "Bot",
    "settings_group_bot_title": "<b>Bot</b>",
    "settings_group_what_about": "Sprache, Ziel und Niveau.",
    "settings_group_how_about": "Woraus eine Lektion besteht und wie sie klingt.",
    "settings_group_bot_about": "Bot-Sprache, Erinnerungen und Hilfe.",
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
    "quiz_btn_one_more": "Noch eine Lektion",
    "home_btn_stats": "Mehr Details",
    "notif_off_how_to_return": "Wieder einschalten: Einstellungen → Bot → Erinnerungen",
    "reminder_offer_done": "✓ Fertig: Die Erinnerung kommt um <b>{time}</b> ({city})\n\nUhrzeit, Tage und Zeitzone können Sie anpassen",
    "reminder_offer_setup": "Erinnerungen anpassen",
    "level_offer": "Auf <b>{current}</b> machen Sie kaum noch Fehler\n\nWeiter zu <b>{following}</b>?\n\nAlles Gelernte bleibt Ihnen erhalten",
    "level_offer_yes": "Ja, weiter zu {following}",
    "level_offer_no": "Hier bleiben",
    "level_offer_done": "Niveau <b>{following}</b>\n\nDie Wörter werden jetzt schwerer",
    "level_offer_pick": "<b>{current}</b> scheint Ihnen leichtzufallen\n\nMit welchem Niveau möchten Sie weitermachen?\n\nAlles Gelernte bleibt Ihnen erhalten",
    "level_offer_stay": "Bei {current} bleiben",
    "level_down_offer": "Auf <b>{current}</b> gibt es noch viele Fehler\n\nZu <b>{previous}</b> wechseln?\n\nDie Wörter werden leichter, alles Gelernte bleibt Ihnen erhalten",
    "level_down_yes": "Ja, zu {previous}",
    "level_down_done": "Niveau <b>{previous}</b>\n\nDie Wörter werden jetzt leichter",
})


# ============================================================================
# ЗАЧЕМ УЧИШЬ — ОПРОС, ВСТРОЕННЫЙ В ПЕРВОЕ НАЖАТИЕ
#
# Режим «по категории» работает, и им пользуются ТРИ человека из 233:
# он спрятан третьим уровнем настроек. Каждая кнопка здесь И отвечает
# на вопрос, И начинает первый круг — шага не прибавилось.
# ============================================================================
TEXTS.update({
    "goal_question": "Wofür brauchen Sie die Sprache? Wir suchen passende Wörter aus.",
    "goal_work": "Für die Arbeit",
    "goal_travel": "Für Reisen",
    "goal_living": "Fürs Leben im Ausland",
    "goal_study": "Fürs Studium",
    "goal_any": "Einfach Wörter lernen",
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
    "intro_games": "Jedes Wort lernen Sie hier in fünf Spielen: lesen, aus der Bedeutung erinnern, hören, laut sagen und auf der Tafel zuordnen.\nIn der Lektion wechseln sie sich von selbst ab.",
    "intro_numbers": "12 902 Wörter · 20 Themen · 6 Niveaus\n{languages} in jeder Kombination: Lernen Sie zum Beispiel Polnisch über Englisch.",
    "intro_menu_settings": "Sprache, Spiele in der Lektion, Erinnerungen",
    "intro_menu_stats": "Ihr Fortschritt",
    "intro_menu_rating": "Rangliste des Monats",
    "intro_menu_learn": "eine Lektion",
    "intro_menu_title": "Was wo ist:",
})


# ============================================================================
# ЗАЧЕМ УЧУ — ЭКРАН НАСТРОЙКИ
#
# Без него цель осталась бы пустой навсегда у всех 233 нынешних
# пользователей: онбординг у них давно позади. Та же дыра, что была у
# состава занятия — колонка есть, экрана нет.
# ============================================================================
TEXTS.update({
    "settings_btn_goal": "Ziel",
    "settings_goal_title": "<b>Wofür ich lerne</b>",
    "settings_goal_description": "Unter den neuen Wörtern kommen die zu Ihrem Ziel zuerst. Die Schwierigkeit richtet sich weiter nach dem Niveau, und Gelerntes kommt zur Wiederholung zurück.",
    "settings_goal_set": "Ziel gespeichert",
    "settings_goal_line": "Ziel: <b>{goal}</b>",
    "settings_goal_none": "nicht gewählt",
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
    "match_title": "<b>Finden Sie die Paare</b>",
    "match_progress": "Gefunden: {matched} von {total}",
    "match_errors": "✗ Fehlgriffe: {count}",
    "match_hint": "Tippen Sie ein Wort auf einer Seite an, dann sein Paar auf der anderen.",
    "match_wrong": "✗ Kein Paar",
    "match_done": "<b>Tafel geschafft!</b>",
    "match_done_counted": "Für den Fortschritt gezählt: {counted} von {total} — nur Paare, die Sie beim ersten Versuch gefunden haben, und nie das letzte, bei dem keine Wahl mehr bleibt.",
    "match_btn_again": "Noch eine Tafel",
    "match_not_ready": "Noch zu früh: Für eine Tafel braucht es {need} bekannte Wörter, Sie haben {have}. Üben Sie mit Karten — so kommen bekannte Wörter dazu.",
})

TEXTS["match_back_to_round"] = "Zurück zur Lektion."

TEXTS.update({
    "settings_btn_match": "Tafel in der Lektion",
    "settings_match_title": "<b>Tafel in der Lektion</b>",
    "settings_match_description": "In jeder Lektion kommt in der Mitte eine Tafel statt einer Frage: fünf Wörter und fünf Bedeutungen, die Sie einander zuordnen. Es sind nur bekannte Wörter, daher erscheint die Tafel, sobald Sie zehn davon haben.",
    "match_state_on": "Die Tafel ist an und kommt in der Mitte der Lektion.",
    "settings_match_short_on": "mit Tafel",
    "settings_channels_short_one": "nur „Ich lese“",
    "settings_channels_short_some": "{count} von {total} Spielen",
    "settings_channels_short_all": "alle Spiele",
    "plural_words": "Wort|Wörter",
    "plural_points": "Punkt|Punkte",
    "plural_days": "Tag|Tage",
    "settings_audio_short_off": "ohne Ton",
    "settings_audio_short_on": "mit Ton",
    "settings_match_short_off": "ohne Tafel",
    "match_state_off": "Die Tafel ist aus: Die Lektion besteht nur aus Fragen.",
})

# ============================================================================
# СООБЩЕНИЯ ПО ИНИЦИАТИВЕ БОТА — патч 2.1 «Вовлечение» (`nudge_texts`).
# Голос и запрет значков — в ru.py; номера вариантов `_N` те же (тест).
# ============================================================================
TEXTS.update({
    "plural_lessons": "Lektion|Lektionen",
    "nd_teaser_quiz_1": "Wissen Sie noch, was {word} heißt? {meaning}",
    "nd_teaser_quiz_2": "Prüfen Sie sich: {word} - {meaning}",
    "nd_teaser_quiz_3": "Eines Ihrer Wörter: {word} - {meaning}",
    "nd_teaser_quiz_4": "Wie übersetzt man {word}? {meaning}",
    "nd_teaser_new_1": "Zum Beispiel: {word} - {meaning}",
    "nd_teaser_new_2": "Erstes Wort: {word} - {meaning}",
    "nd_teaser_new_3": "Wie übersetzt man {word}? Die Übersetzung ist verdeckt - tippen Sie darauf: {meaning}",
    "nd_streak_head_1": "<b>{name}, Serie: {days} in Folge</b>",
    "nd_streak_head_2": "<b>{name}, {days} in Folge. Weitermachen?</b>",
    "nd_streak_head_3": "<b>{name}, schon {days} in Folge</b>",
    "nd_streak_head_4": "<b>{name}, {days} ohne Pause</b>",
    "nd_streak_head_5": "<b>{name}, noch eine Lektion, dann sind es {next_days} in Folge</b>",
    "nd_streak_head_6": "<b>{name}, Ihre Serie wartet: {days}</b>",
    "nd_streak_head_7": "<b>{days} in Folge, {name}</b>",
    "nd_streak_head_8": "<b>{name}, {days} in Folge. Heute noch eine Lektion?</b>",
    "nd_body_learned_1": "Bekannte Wörter: {known_n} · gelernt: {learned}",
    "nd_body_learned_2": "Wörter in Arbeit: {in_work} · gelernt: {learned}",
    "nd_body_learned_3": "Sie kennen schon {known}, davon gelernt: {learned}.",
    "nd_body_known_1": "Bekannte Wörter: {known_n}. Jede Lektion bringt neue dazu.",
    "nd_body_known_2": "Wörter in Arbeit: {in_work}. Die ersten gelernten sind nah.",
    "nd_body_known_3": "Sie kennen schon {known}.",
    "nd_streak_close_1": "Kleine Schritte, großes Ergebnis.",
    "nd_streak_close_2": "Jeden Tag ein wenig: so bleiben Wörter hängen.",
    "nd_streak_close_3": "Eine Lektion heute verlängert die Serie.",
    "nd_streak_close_4": "Eine Lektion dauert etwa {minutes_n} Minuten.",
    "nd_streak_close_5": "Regelmäßigkeit zählt mehr als die Länge der Lektionen.",
    "nd_progress_head_known": "<b>{name}, Sie kennen schon {known}</b>",
    "nd_progress_head_1": "<b>{name}, Ihre Wörter sind zur Wiederholung fällig</b>",
    "nd_progress_head_2": "<b>{name}, haben Sie nur wenige Minuten?</b>",
    "nd_progress_head_3": "<b>{name}, dort weitermachen, wo Sie aufgehört haben?</b>",
    "nd_progress_head_4": "<b>{name}, zurück zu Ihren Wörtern?</b>",
    "nd_progress_head_5": "<b>{name}, ein guter Moment, Ihre Wörter aufzufrischen</b>",
    "nd_due_1": "Wörter zur Wiederholung: {due_n}. Die Termine berechnet der Bot selbst.",
    "nd_due_2": "Zeit, {due} zu wiederholen, bevor sie verblassen.",
    "nd_due_3": "Wörter zum Wiederholen: {due_n}. Der Bot hat schon ausgewählt, womit es losgeht.",
    "nd_due_many_1": "Es haben sich viele Wörter zum Wiederholen angesammelt: die Lektion beginnt mit den wichtigsten.",
    "nd_due_many_2": "Die Wiederholungen haben sich gestaut. Eine Lektion am Tag reicht, der Rest kann warten.",
    "nd_praise_1": "{lessons} geschafft. Schritt für Schritt, aber regelmäßig.",
    "nd_praise_2": "Abgeschlossene Lektionen: {lessons_n}. Kleine Schritte, großes Ergebnis.",
    "nd_praise_3": "{lessons} liegen hinter Ihnen, und jede hat Wörter gebracht.",
    "nd_short_1": "Eine Lektion dauert etwa {minutes_n} Minuten.",
    "nd_short_2": "Das dauert nur wenige Minuten.",
    "nd_first_head_words": "<b>{name}, gestern haben Sie {words} gelernt</b>",
    "nd_first_head_1": "<b>{name}, ein guter Start</b>",
    "nd_first_head_2": "<b>{name}, die Wörter von gestern prüfen?</b>",
    "nd_first_body_1": "Eine Wiederholung am nächsten Tag hilft, Wörter zu festigen.",
    "nd_first_body_2": "Am zweiten Tag festigen sich neue Wörter am besten.",
    "nd_first_close_1": "Das dauert nur wenige Minuten.",
    "nd_first_close_2": "Eine Lektion dauert etwa {minutes_n} Minuten.",
    "nd_kept_head_1": "<b>{name}, alles ist noch da</b>",
    "nd_kept_head_2": "<b>{name}, Ihre Wörter sind gespeichert</b>",
    "nd_kept_head_3": "<b>{name}, lange nicht gesehen</b>",
    "nd_kept_body_1": "Bekannte Wörter: {known_n} · gelernt: {learned}. Nichts ist verloren - die Lektion beginnt mit den fälligen Wörtern.",
    "nd_kept_body_2": "Alles, was Sie gelernt haben, ist gespeichert. Die Lektion beginnt mit den Wörtern, die aufgefrischt werden sollten.",
    "nd_kept_body_3": "Pausen hat jeder. Anfangen können Sie mit einer kurzen Lektion.",
    "nd_kept_best": "Beste Serie: {best} in Folge. Eine neue beginnt mit einer Lektion.",
    "nd_farewell_head_1": "<b>{name}, es kommen keine Erinnerungen mehr</b>",
    "nd_farewell_head_2": "<b>{name}, die letzte Erinnerung</b>",
    "nd_farewell_body_1": "Der Bot schreibt erst wieder, wenn Sie zurückkommen. Alles ist gespeichert: bekannte Wörter {known_n}, gelernt {learned}. Weitermachen können Sie jederzeit mit dem Button unten.",
    "nd_farewell_body_2": "Gerade passt es wohl nicht - das ist in Ordnung. Es kommen keine Erinnerungen mehr. Wörter und Fortschritt sind gespeichert.",
    "nd_start_head_1": "<b>{name}, Ihre ersten Wörter warten</b>",
    "nd_start_head_2": "<b>{name}, wollen wir anfangen?</b>",
    "nd_start_head_3": "<b>{name}, die erste Lektion dauert etwa {minutes_n} Minuten</b>",
    "nd_start_body_1": "Der Bot wählt die wichtigsten Wörter für Ihr Niveau aus und achtet selbst darauf, wann sie zu wiederholen sind.",
    "nd_start_body_2": "Wir beginnen mit den häufigsten Wörtern, denen, die man jeden Tag hört.",
    "nd_start_body_3": "Keine Vorbereitung nötig: {questions} Fragen, danach sagt der Bot, was wann zu wiederholen ist.",
    "nd_start3_head_1": "<b>{name}, ausprobieren?</b>",
    "nd_start3_head_2": "<b>{name}, Ihre ersten Wörter warten noch</b>",
    "nd_start_last_head": "<b>{name}, die letzte Einladung</b>",
    "nd_start_last_body": "Es kommen keine Erinnerungen mehr. Wenn Sie anfangen möchten: Die erste Lektion dauert etwa {minutes_n} Minuten - der Button ist unten.",
    "nd_btn_optin": "Um {time} erinnern",
    "nd_btn_stop": "Nicht mehr senden",
    "nd_auto_time": "Ich erinnere Sie täglich um {time}. Die Uhrzeit können Sie ändern",
    "nd_btn_change_time": "Uhrzeit ändern",
    "nd_optin_done": "✓ Erledigt: Die Erinnerung kommt um <b>{time}</b>\n\nDie Uhrzeit können Sie in den Einstellungen ändern",
})
