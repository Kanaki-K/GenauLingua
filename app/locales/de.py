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

    "notif_message_btn_disable": "Erinnerungen abschalten",

    "day_mon": "Mo",
    "day_tue": "Di",
    "day_wed": "Mi",
    "day_thu": "Do",
    "day_fri": "Fr",
    "day_sat": "Sa",
    "day_sun": "So",

    "notif_btn_back": "Zurück zu den Einstellungen",

    "notif_default_name": "Freund",

    "anchor_streak": "🔥 {days}",
    "notif_message_greeting": "<b>Zeit zum Üben, {name}!</b>",


    # EIN GRUND ZURÜCKZUKOMMEN — und er muss stimmen
    "remind_streak_risk": "{days_word} in Folge · heute noch nicht",
    "remind_due": "Zur Wiederholung fällig: {count} — die Termine behält der Bot im Blick",
    "remind_due_many": "Es hat sich viel angesammelt. Fangen Sie mit einer Lektion an, der Rest wartet.",
    "remind_streak_lost": "Ihre beste Serie war {days_word}. Eine neue beginnt mit einer Lektion.",
    "remind_milestone_close": "Wörter in Arbeit: {count} · noch {left} bis {target}, das ist eine Lektion",
    "remind_almost_learned": "Nur noch eine richtige Antwort bis zum ersten gelernten Wort. Solche Wörter: {count}",
    "remind_rank": "Platz {rank} von {total} in der Monatsrangliste dieser Sprache",
    "remind_fact_1": "Ein Wort bleibt, wenn es wiederkommt: nach einem Tag, nach drei Tagen, nach einer Woche. Die Termine behält der Bot im Blick.",
    "remind_fact_2": "Eine Antwort nach Gehör zählt doppelt: Das geschriebene Wort fehlt, Sie unterscheiden nur am Klang.",
    "remind_fact_3": "Aussprechen ist schwerer als Erkennen — und dreimal so viel wert.",
    "remind_fact_4": "Fünfzehn Fragen dauern etwa vier Minuten. Kürzer als die Schlange am Kaffeestand.",

    # ============================================================================
    # EINSTELLUNGEN
    # ============================================================================
    "settings_title": "<b>Einstellungen</b>",
    "settings_mode": "Richtung: <b>{mode}</b>",
    "settings_language": "Bot-Sprache: <b>{language}</b>",

    "settings_btn_quiz_mode": "Niveau und Themen",
    "settings_btn_change_language": "Oberflächensprache",
    "settings_btn_notifications": "Erinnerungen",

    "settings_quiz_mode_line": "Niveau: <b>{mode}</b>",


    "settings_language_title": "<b>Oberflächensprache</b>",
    "settings_language_description": "Wählen Sie die Sprache der Bot-Oberfläche:",
    "start_pick_language": "Sprache wählen",

    "language_changed": "✓ Sprache geändert: {language}",
    "user_not_found": "✗ Nutzer nicht gefunden. Bitte senden Sie /start.",

    # Namen der Oberflächensprachen — jeweils in der Sprache selbst
    "lang_ru": "Русский",
    "lang_uk": "Українська",
    "lang_en": "English",
    "lang_tr": "Türkçe",
    "lang_de": "Deutsch",
    "lang_pl": "Polski",

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
    "report_approved": "✓ Ihre Meldung zu <b>{word}</b> wurde angenommen — wir korrigieren die Übersetzung.\n+{points} Punkte für die Rangliste des Monats — danke, das Wörterbuch wird besser für alle.",
    "award_won": "{mark} Platz {rank} in der Rangliste für {month}.\n{bonus} Punkte wurden Ihrem Gesamtstand gutgeschrieben.",
    "report_approved_audio": "✓ Ihre Meldung zur Aussprache von <b>{word}</b> wurde angenommen.\nDie Aussprache wird neu erzeugt. +{points} Punkte für die Rangliste des Monats — danke.",

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
    "quiz_btn_repeat_errors": "Fehler wiederholen",

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
    "rating_title_monthly": "<b>Meine Platzierung — {month} {year}</b>",
    "rating_not_active": "✗ Die Platzierung ist noch nicht aktiv.",
    "rating_not_in_ranking": "Sie sind noch nicht in der Rangliste",
    "rating_start_quiz": "Machen Sie Ihre erste Lektion!",
    "rating_join_by_lesson": "Ihre Punkte für Meldungen ({score}) sind gutgeschrieben. Absolvieren Sie eine Lektion, um in die Monatsrangliste zu kommen.",
    "release_notes_2026_10": "✨ <b>GenauLingua 2.0 — wir haben den Bot von Grund auf neu gebaut</b>\n\n<b>Nicht nur Deutsch.</b> Lernen Sie Ukrainisch, Englisch, Türkisch, Deutsch, Polnisch oder Russisch — aus jeder dieser Sprachen. Die Oberfläche gibt es ebenfalls in allen sechs.\n\n<b>Sechs Spiele statt einem.</b> Früher gab es nur „Übersetzung wählen“. Jetzt wechseln sich die Spiele in jeder Lektion ab:\n📖 Ich lese · 💭 Ich erinnere · 🎧 Ich höre · 🎤 Ich spreche · 🧩 Finden Sie die Paare · 🧱 Ich baue\nBei „Ich spreche“ antworten Sie mit der Stimme, bei „Ich baue“ setzen Sie einen Satz aus Wörtern zusammen — der Bot zeigt, welches Wort nicht passt.\n\n<b>Der Bot spricht.</b> Jedes Wort und jedes Beispiel ist mit natürlicher Stimme vertont.\n\n<b>Neues Aussehen.</b> Neues Menü, ein aufgeräumter Chat ohne überflüssige Nachrichten, ein Startbildschirm mit Ihren Fähigkeiten, übersichtliche Statistik, neuer Avatar und neue Begrüßung.\n\n<b>Das ganze Wörterbuch wurde geprüft</b> — alle 12.902 Wörter, Übersetzungen und Beispiele.\n\n<b>Der Bot passt sich an:</b> Er bringt Wörter zurück, kurz bevor Sie sie vergessen, und schlägt das nächste Niveau vor, wenn es leicht wird.\n\n<b>Fehler behoben:</b> Ihre Tagesserie wird richtig gezählt, und die Ranglistenpunkte sind fair — sie belohnen Einsatz. Auch „gelernt“ ist jetzt ehrlich: Ein Wort gilt als gelernt, wenn Sie es dreimal hintereinander an verschiedenen Tagen richtig hatten; alle geübten Wörter sehen Sie unter „Wörter in Arbeit“.\n\n<b>Erinnerungen sind eingeschaltet</b> — zu Ihrer Zeit. Ändern oder ausschalten: Einstellungen → Bot → Erinnerungen.\n\n⭐ Einen Fehler gefunden? Melden Sie ihn direkt im Ergebnis der Lektion: Jede bestätigte Meldung bringt +15 Punkte.\n\nIhr Fortschritt und Ihre Punkte bleiben erhalten. Probieren Sie es aus — eine Lektion dauert nur ein paar Minuten.",
    "rating_position": "Platz: <b>#{rank}</b> von {total}",
    "rating_points": "Punkte: <b>{score}</b>",
    "rating_title_polyglot": "Polyglott",
    "rating_title_professor": "Professor",
    "rating_title_expert": "Experte",
    "rating_title_student": "Schüler",
    "rating_your_month": "<b>Ihr {month}:</b>",
    "rating_quizzes": "Lektionen: {count}",
    "rating_words_learned": "Wörter gelernt: {count}",
    "rating_streak": "Serie: {days_word}",
    "rating_avg_result": "Durchschnitt: {percent}%",
    "rating_scoring_title": "<b>So verdienen Sie Punkte:</b>",
    "rating_scoring_quiz": "• Lektion beendet → +10",
    "rating_scoring_word": "• Wort gelernt → +3",
    "rating_scoring_streak": "• Jeder Tag in Folge zählt mehr, bis +10",
    "rating_scoring_bonus": "• Treffsicherheit über 60% → Bonus, je höher, desto mehr",
    "rating_scoring_report": "• Bestätigte Fehlermeldung → +{points}",

    "rating_title_alltime": "<b>Meine Platzierung — Insgesamt</b>",
    "rating_position_alltime": "Platz: <b>#{rank}</b>",
    "rating_position_none": "Platz: <b>—</b>",
    "rating_achievements": "<b>Ihre Erfolge:</b>",
    "rating_wins": "Siege (1. Platz): {count}",
    "rating_total_words": "Wörter gelernt: {count}",
    "rating_motivation_start": "Fangen Sie an, Wörter zu lernen — der erste Schritt ist der wichtigste!",
    "rating_motivation_continue": "Machen Sie weiter — der erste Sieg ist nah!",
    "rating_motivation_champion": "Sie sind ein echter Champion!",

    "table_title_monthly": "<b>Rangliste — {month} {year}</b>",
    "table_title_alltime": "<b>Rangliste — Insgesamt</b>",
    "table_empty": "Noch nimmt niemand teil.\nMachen Sie die erste Lektion und eröffnen Sie die Rangliste!",
    "table_you_in_top": "Sie: <b>#{rank}</b> von {total}",
    "table_you_not_in_top": "Sie: <b>#{rank}</b> von {total} — {score}",
    "table_you_outside": "Sie: außerhalb der Top 10 — {score}",
    "table_you_not_ranked": "Sie sind noch nicht in der Rangliste",
    "btn_leaderboard_table": "Tabelle",
    "btn_back_to_rating": "Zurück zur Platzierung",
    "rating_tab_month": "Monat",
    "rating_tab_alltime": "Gesamt",

    # ============================================================================
    # STATISTIK (NEU)
    # ============================================================================
    "stats_header": "<b>Ihre Statistik</b>",
    "stats_in_work_line": "Wörter in Arbeit: {count} · noch {left} bis {target}",
    "stats_in_work_top": "Wörter in Arbeit: {count}",
    "stats_details": "Noch in Übung: {progress}\nNeu: {new}\nSchwierig: {difficult}",
    "stats_achievements_title": "<b>Ihre Erfolge</b>",
    "stats_words_count": "Wörter gelernt: <b>{count}</b>",
    "stats_streak_line": "Serie: {days_word} in Folge",
    "stats_best_streak_line": "Beste Serie: {days_word}",
    "stats_quizzes_header": "<b>Lektionen · {level}</b>",
    "stats_quizzes_passed_line": "Abgeschlossen: <b>{count}</b>",
    "stats_quizzes_avg_line": "Durchschnitt: <b>{percent}%</b>",
    "stats_quizzes_best_line": "Bestes Ergebnis: <b>{percent}%</b>",
    "stats_quizzes_empty": "Noch keine Lektion abgeschlossen",
    "stats_recent_header": "<b>Letzte Lektionen</b>",
    "stats_overall_header": "<b>Gesamtfortschritt</b>",
    "stats_overall_learned": "Gelernte Wörter: <b>{learned}</b> von {total}",
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
    "onboarding_learning_desc": "Die Bedeutungen erscheinen auf {native}.\nDie Sprache können Sie jederzeit in den Einstellungen ändern.",
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
    "help_how_to_use_text": "<b>Lektion</b>\n{words}, je vier Antworten. Die Spiele wechseln sich von selbst ab: „Ich lese“, „Ich erinnere“, „Ich höre“, „Ich spreche“ und die Tafel „Finden Sie die Paare“. Der Bot merkt sich Ihre Fehler und bringt Schwieriges öfter zurück. Nach der Lektion können Sie Ihre Fehler sofort wiederholen.\n\n<b>Aussprache</b>\nIn der Frage erklingt das Wort, nach der Antwort das Wort mit seinem Beispiel. Die Stimme wählen Sie in den Einstellungen — männlich oder weiblich.\n\n<b>Sprachen</b>\n{languages} — in jedem Paar. Fortschritt und Platzierung werden für jede Sprache getrennt gezählt.\n\n\nEin Wort gilt als <b>gelernt</b> nach drei richtigen Antworten hintereinander, und zwar an verschiedenen Tagen.\nDie <b>Serie</b> zählt Tage in Folge: Eine Lektion am Tag genügt.\nFehler in Übersetzung oder Aussprache — dafür gibt es den Knopf „Fehler melden“ am Ende der Lektion.",
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
    "rating_scoring_answer": "• Richtige Antwort → +1, nach Gehör → +2, laut gesprochen → +3",
    "rating_scoring_quiz": "• Lektion beendet → +10",
    "rating_scoring_word": "• Wort gelernt → +3",
    "rating_scoring_streak": "• Jeder Tag in Folge zählt mehr, bis +10",
    "rating_scoring_bonus": "• Treffsicherheit über 60% → Bonus, je höher, desto mehr",
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
    "build_hint": "Setzen Sie den Satz aus den Wörtern unten zusammen — einige davon sind überflüssig. Tippen Sie auf ein gesetztes Wort, um es zurückzulegen",
    "build_btn_check": "Prüfen",
    "build_full": "Alle Plätze sind belegt. Tippen Sie auf ein gesetztes Wort, um es zurückzulegen, oder auf „Prüfen“.",
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
    "quiz_question_speak": "🎤 Sprechen Sie dieses Wort laut aus — nehmen Sie eine Sprachnachricht auf",
    "speech_btn_reference": "Langsam anhören",
    "speech_btn_skip": "Überspringen",
    "speech_listening": "🎧 Ich höre zu…",
    "speech_not_understood": "Nicht verstanden. Nehmen Sie es noch einmal auf — näher am Mikrofon und etwas lauter.",
    "speech_try_again": "Das klang wie „{heard}“ — noch nicht ganz. Bitte nehmen Sie es noch einmal auf: Versuch {attempt} von {total}.",
    "speech_send_voice": "🎤 Diese Frage wird mit einer Sprachnachricht beantwortet. Halten Sie die Mikrofontaste gedrückt.",
    "speech_skipped": "Übersprungen",
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
    "home_streak": "Serie {days_word}",
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
    "reminder_offer": "Einmal am Tag erinnern? So verlieren Sie das Gelernte nicht — und die Serie bleibt.",
    "reminder_offer_yes": "Ja, bitte erinnern",
    "reminder_offer_no": "Nein, danke",
    "reminder_offer_done": "✓ Fertig: Die Erinnerung kommt um <b>{time}</b> ({city}). Uhrzeit, Tage und Zeitzone können Sie anpassen.",
    "reminder_offer_setup": "Erinnerungen anpassen",
    "level_offer": "Auf <b>{current}</b> machen Sie kaum noch Fehler. Weiter zu <b>{following}</b>? Alles Gelernte bleibt Ihnen erhalten.",
    "level_offer_yes": "Ja, weiter zu {following}",
    "level_offer_no": "Hier bleiben",
    "level_offer_done": "Niveau <b>{following}</b>. Die Wörter werden jetzt schwerer.",
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
    "intro_numbers": "12 902 Wörter · 20 Themen · 6 Niveaus\nSechs Sprachen in jeder Kombination: Lernen Sie zum Beispiel Polnisch über Englisch.",
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
    "settings_channels_short_some": "{count} von vier Spielen",
    "settings_channels_short_all": "alle vier Spiele",
    "plural_words": "Wort|Wörter",
    "plural_points": "Punkt|Punkte",
    "plural_days": "Tag|Tage",
    "settings_audio_short_off": "ohne Ton",
    "settings_audio_short_on": "mit Ton",
    "settings_match_short_off": "ohne Tafel",
    "match_state_off": "Die Tafel ist aus: Die Lektion besteht nur aus Fragen.",
})
