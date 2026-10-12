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
    "btn_learn_words": "📚 Wörter lernen",
    "btn_stats": "📊 Statistik",
    "btn_settings": "🦾 Einstellungen",
    "btn_help": "❓ Hilfe",
    "btn_back": "◀️ Zurück",
    "menu_placeholder": "Wähle eine Aktion...",

    # ============================================================================
    # BEGRÜSSUNG UND START
    # ============================================================================
    "welcome_title": "👋 <b>Hallo, {name}!</b>",
    "welcome_description": "🌍 <b>GenauLingua</b> — Wortschatz spielerisch lernen\nSprachen zur Auswahl: {languages}\n12 000+ Wörter · 20 Themen · 6 Niveaus\n\nDer Bot wählt die Wörter für dich aus — je mehr\ndu spielst, desto treffsicherer die Auswahl",
    "welcome_separator": "──────────────────",

    "welcome_learn_words_title": "📚 <b>Wörter lernen</b>",
    "welcome_learn_words_desc": "Quiz starten",

    "welcome_stats_title": "📊 <b>Statistik</b>",
    "welcome_stats_desc": "Dein Fortschritt",

    "welcome_settings_title": "🦾 <b>Einstellungen</b>",
    "welcome_settings_desc": "Modus, Sprache, Themen",

    "welcome_help_title": "❓ <b>Hilfe</b>",
    "welcome_help_desc": "Anleitung und Rückmeldung",

    "welcome_your_level": "Dein Niveau: <b>{level}</b>\nModus: <b>{mode}</b>",
    "welcome_call_to_action": "Tippe auf 📚 Wörter lernen — und los!",

    "welcome_choose_level": "🎯 <b>Womit fangen wir an?</b>\n\nDein Niveau — {language}\n\n• A1–A2 — Grundwortschatz\n• B1–B2 — sicheres Sprechen\n• C1–C2 — freie Beherrschung",
    "choose_level_prompt": "Wähle ein Niveau:",

    "level_selected": "✅ Niveau <b>{level}</b> ausgewählt.\n\nTippe auf 📚 Wörter lernen — und los!",
    "level_locked": "🔒 Dieses Niveau ist noch in Arbeit",

    # ============================================================================
    # ERINNERUNGEN
    # ============================================================================
    "notif_title": "🔔 <b>Erinnerungen</b>",
    "notif_status": "Status: {status}",
    "notif_status_on": "🔔 Ein",
    "notif_status_off": "🔕 Aus",
    "notif_time": "Zeit: {time}",
    "notif_days": "Tage: {days}",
    "notif_timezone": "Zeitzone: {timezone}",
    "notif_hint": "💡 Die Erinnerungen kommen zur angegebenen Zeit in deiner Zeitzone.",
    "notif_hint_off": "💡 Schalte die Erinnerungen ein, damit du das tägliche Üben nicht vergisst!",

    "notif_btn_toggle_on": "🔔 Erinnerungen: Ein",
    "notif_btn_toggle_off": "🔕 Erinnerungen: Aus",
    "notif_btn_time": "🕐 Zeit: {time}",
    "notif_btn_days": "📅 Tage wählen",
    "notif_btn_timezone": "🌍 Zeitzone ändern",

    "notif_timezone_title": "🌍 <b>Wähle deine Zeitzone</b>",
    "notif_timezone_current": "Aktuell: {timezone}",
    "notif_timezone_prompt": "Wähle eine Stadt in deiner Zeitzone:",
    "notif_timezone_more": "🌍 Andere Stadt wählen ▼",
    "notif_timezone_back": "◀️ Zurück",
    "notif_timezone_set": "✅ Zeitzone gesetzt: {city}",

    "notif_time_title": "🕐 <b>Wähle die Uhrzeit der Erinnerung</b>",
    "notif_time_current": "Aktuelle Zeit: {time}",
    "notif_time_timezone": "Zeitzone: {timezone}",
    "notif_time_hint": "Die Erinnerung kommt täglich zur gewählten Zeit.",
    "notif_time_set": "✅ Zeit gesetzt: {time}",

    "notif_days_title": "📅 <b>Wähle die Tage für Erinnerungen</b>",
    "notif_days_hint": "Tippe auf einen Tag, um ihn ein- oder auszuschalten.\n✅ Grüner Haken — Tag ist an\n❌ Rotes Kreuz — Tag ist aus\n\nWenn du fertig bist — tippe auf «Speichern».",
    "notif_days_all": "📅 Alle Tage",
    "notif_days_weekdays": "🗓️ Wochentage (Mo–Fr)",
    "notif_days_save": "💾 Speichern",
    "notif_days_saved": "✅ Tage gespeichert!",
    "notif_days_all_selected": "✅ Alle Tage ausgewählt",
    "notif_days_weekdays_selected": "✅ Wochentage ausgewählt (Mo–Fr)",
    "notif_days_none": "⚠️ Wähle mindestens einen Tag für Erinnerungen!",

    "notif_toggle_on": "🔔 Erinnerungen eingeschaltet!",
    "notif_toggle_off": "🔕 Erinnerungen ausgeschaltet",

    "notif_message_title": "{emoji} <b>Zeit zu üben!</b>",
    "notif_message_streak": "🔥 Serie: {days} Tage in Folge",
    "notif_message_words": "📊 Gelernte Wörter: {count}",
    "notif_message_cta": "💪 Lass deine Serie nicht reißen!",
    "notif_message_btn_start": "📚 Quiz starten",
    "notif_message_btn_disable": "🔕 Erinnerungen abschalten",

    "day_mon": "Mo",
    "day_tue": "Di",
    "day_wed": "Mi",
    "day_thu": "Do",
    "day_fri": "Fr",
    "day_sat": "Sa",
    "day_sun": "So",

    "notif_btn_back": "◀️ Zurück zu den Einstellungen",

    "notif_default_name": "Freund",
    "notif_message_greeting": "🔥 <b>Zeit zu üben, {name}!</b>",
    "notif_message_progress_title": "📊 <b>Dein Fortschritt:</b>",
    "notif_progress_streak": "├ Serie: {days} Tage 🎯",
    "notif_progress_quizzes": "├ Quizze absolviert: {count}",
    "notif_progress_words": "├ Wörter gelernt: {count}",
    "notif_progress_accuracy": "└ Treffsicherheit: {percent}%",

    "notif_motivation_1": "Schritt für Schritt kommst du ans Ziel!",
    "notif_motivation_2": "Deine Serie wächst — bleib dabei!",
    "notif_motivation_3": "Heute noch ein Schritt zur freien Beherrschung!",
    "notif_motivation_4": "Kleine Mühe jeden Tag = großes Ergebnis!",
    "notif_motivation_5": "Du bist auf dem richtigen Weg! Mach weiter!",
    "notif_motivation_6": "Jedes Quiz bringt dich näher an dein Ziel!",

    # ============================================================================
    # EINSTELLUNGEN
    # ============================================================================
    "settings_title": "🦾 <b>Einstellungen</b>",
    "settings_level": "📚 Niveau: <b>{level}</b>",
    "settings_mode": "🔄 Übersetzung: <b>{mode}</b>",
    "settings_language": "🌍 Oberflächensprache: <b>{language}</b>",
    "settings_choose": "Wähle aus, was du ändern möchtest:",

    "settings_btn_quiz_mode": "📝 Quiz-Modus",
    "settings_btn_change_mode": "🔄 Übersetzungsrichtung",
    "settings_btn_change_language": "🌍 Oberflächensprache",
    "settings_btn_notifications": "🔔 Erinnerungen",

    "settings_quiz_mode_line": "📝 Modus: <b>{mode}</b>",

    "settings_mode_title": "🔄 <b>Übersetzungsrichtung</b>",
    "settings_mode_description": "Wähle die Richtung der Übersetzung:",

    "settings_language_title": "🌍 <b>Oberflächensprache</b>",
    "settings_language_description": "Wähle die Sprache der Bot-Oberfläche:",

    "language_changed": "✅ Sprache geändert auf {language}",
    "level_not_selected": "Nicht gewählt",
    "user_not_found": "❌ Nutzer nicht gefunden. Nutze /start",

    # Namen der Oberflächensprachen — jeweils in der Sprache selbst
    "lang_ru": "🏴 Русский",
    "lang_uk": "🇺🇦 Українська",
    "lang_en": "🇬🇧 English",
    "lang_tr": "🇹🇷 Türkçe",
    "lang_de": "🇩🇪 Deutsch",
    "lang_pl": "🇵🇱 Polski",

    # Übersetzungsrichtungen
    "mode_de_to_ru": "🇩🇪 DE → 🏴 RU",
    "mode_ru_to_de": "🏴 RU → 🇩🇪 DE",
    "mode_de_to_uk": "🇩🇪 DE → 🇺🇦 UK",
    "mode_uk_to_de": "🇺🇦 UK → 🇩🇪 DE",
    "mode_de_to_en": "🇩🇪 DE → 🇬🇧 EN",
    "mode_en_to_de": "🇬🇧 EN → 🇩🇪 DE",
    "mode_de_to_tr": "🇩🇪 DE → 🇹🇷 TR",
    "mode_tr_to_de": "🇹🇷 TR → 🇩🇪 DE",

    # ============================================================================
    # QUIZ-MODUS
    # ============================================================================
    "qmode_title": "📝 <b>Quiz-Modus</b>",
    "qmode_current": "Jetzt: <b>{mode}</b>",
    "qmode_choose": "Wähle, wie du Wörter lernen willst\nDu kannst es jederzeit ändern — der Fortschritt bleibt",

    "qmode_btn_level": "📚 Nach Niveau",
    "qmode_btn_category": "🗂 Kategorie",
    "qmode_btn_all": "🌍 Top 10 Tausend",
    "qmode_btn_difficult": "⚠️ Schwierige",

    "qmode_level_short": "📚 Niveau {level}",
    "qmode_category_short": "🗂 {category}",
    "qmode_all_short": "🌍 Top 10 Tausend",
    "qmode_difficult_short": "⚠️ Schwierige Wörter",

    "qmode_level_title": "📚 <b>Niveau wählen</b>",
    "qmode_level_desc": "Vom ersten «Hallo» bis zur freien Diskussion\nAlle Niveaus sind offen — wähle deins!\n\n• A1–A2 — Grundwortschatz\n• B1–B2 — sicheres Sprechen\n• C1–C2 — freie Beherrschung",
    "qmode_level_set": "✅ Modus: Nach Niveau ({level})",

    "qmode_category_title": "🗂 <b>Kategorie wählen</b>",
    "qmode_category_desc": "Von Essen bis Wissenschaft — wähle das Thema, das du brauchst\n\nJede Kategorie enthält Wörter aller Niveaus",
    "qmode_category_set": "✅ Modus: {category}",

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

    "qmode_all_set": "✅ Modus: Top 10 Tausend",

    "qmode_difficult_set": "✅ Modus: Schwierige Wörter",
    "qmode_difficult_few": "Du hast bisher nur {count} schwierige Wörter — es braucht mindestens 4\nMach noch ein paar Quizze!",
    "qmode_difficult_empty": "Du hast bisher keine schwierigen Wörter.\nMach ein paar Quizze!",

    "quiz_btn_change_mode": "⚙️ Quiz-Modus",
    "quiz_btn_report_error": "📝 Fehler melden",
    "report_btn_confirm": "✅ Bestätigen ({count})",
    "report_btn_send": "📨 Senden",
    "report_no_words": "Keine Wörter zum Melden",
    "report_none_selected": "Wähle mindestens ein Wort",
    "report_sent": "✅ {count} Meldungen gesendet — danke!\nWenn der Fehler bestätigt wird, bekommst du +1 Punkt",
    "report_daily_limit": "⚠️ Tageslimit für Meldungen erreicht (max. 20)",
    "report_all_reported": "✅ Alle Wörter aus diesem Quiz sind schon gemeldet",
    "report_already_sent": "✔️ Schon früher gesendet",
    "report_kind_title": "Was genau stimmt nicht?",
    "report_btn_kind_text": "📝 Falsche Übersetzung",
    "report_btn_kind_audio": "🔊 Falsche Aussprache",
    "report_sent_audio": "✅ {count} gesendet — danke!\nMeldungen zur Aussprache sind besonders wertvoll: die maschinelle Prüfung hört die Betonung nicht",

    # ============================================================================
    # QUIZ
    # ============================================================================
    "quiz_no_level": "⚠️ Wähle zuerst dein Niveau mit dem Befehl /start",
    "quiz_error_generation": "❌ Beim Vorbereiten des Quiz ist ein Fehler aufgetreten.\nVersuche es noch einmal über /start",
    "quiz_no_words": "❌ Für dieses Niveau gibt es leider noch keine Wörter.\nWähle ein anderes Niveau.",

    "quiz_question_number": "Frage {current}/{total}",
    "quiz_question_choose_word": "Wähle das richtige Wort:",
    "quiz_question_choose_translation": "Wähle die richtige Übersetzung:",

    "quiz_correct": "✅ <b>Richtig!</b>",
    "quiz_wrong": "❌ <b>Falsch!</b>",
    "quiz_correct_answer": "Richtige Antwort:",

    "quiz_btn_next": "Weiter →",
    "quiz_btn_repeat_errors": "🔄 Fehler wiederholen",

    "quiz_completed": "🎉 <b>Quiz beendet!</b>",
    "quiz_result_correct": "✅ Richtig: <b>{correct}/{total}</b>",
    "quiz_result_percentage": "📈 Ergebnis: <b>{percentage}%</b>",
    "quiz_result_details": "📝 <b>Einzelheiten:</b>",
    "quiz_result_errors": "❌ Fehler: {count}",

    "quiz_repeat_title": "🔄 <b>Fehler wiederholen</b>",
    "quiz_repeat_question": "🔄 Wiederholung {current}/{total}",
    "quiz_no_errors": "✅ Du hattest keine Fehler!",
    "quiz_error_next": "❌ Die nächste Frage konnte nicht geladen werden.",
    "quiz_error_generate": "❌ Die nächste Frage konnte nicht erstellt werden.",

    # ============================================================================
    # STATISTIK
    # ============================================================================
    "stats_title": "📊 <b>Statistik</b>",
    "stats_no_level": "⚠️ <b>Wähle zuerst ein Niveau!</b>\n\nNutze den Befehl /start, um zu beginnen.",

    "stats_all_words": "📚 Ganze Datenbank ({count} Wort|Wörter|Wörter)",
    "stats_learned": "✅ Gelernt: {count}",
    "stats_in_progress": "🔄 In Arbeit: {count}",
    "stats_new": "🆕 Neu: {count}",
    "stats_difficult": "❌ Schwierig: {count}",

    "stats_level_title": "🎯 Niveau {level} · {mode} ({count} Wort|Wörter|Wörter)",
    "stats_quizzes_title": "🏆 <b>Quizze (Niveau {level}):</b>",
    "stats_quizzes_passed": "Absolviert: {count}",
    "stats_quizzes_avg": "Durchschnitt: {percentage}%",
    "stats_quizzes_best": "Bestes Ergebnis: {percentage}%",
    "stats_quizzes_none": "Du hast auf diesem Niveau noch keine Quizze gemacht.",

    "stats_activity_title": "🔥 <b>Aktivität:</b>",
    "stats_streak": "└─ Serie: <b>{days}</b> Tage in Folge",

    "stats_recent_title": "<b>Letzte Quizze:</b>",
    "stats_learned_explanation": "💡 <b>Gelernt</b> — 3 richtige Antworten in Folge, und nicht am Tag des ersten Kontakts",

    # ============================================================================
    # HILFE
    # ============================================================================
    "help_title": "❓ <b>Hilfe — GenauLingua</b>",
    "help_description": "Hier findest du die Anleitung, erfährst, was bald dazukommt, und wie du die Community erreichst.",
    "help_choose": "Wähle einen Bereich:",

    "help_btn_how_to_use": "📖 So funktioniert es",
    "help_btn_community": "💬 Community",

    "help_how_to_use_title": "📖 <b>So benutzt du den Bot</b>",
    "help_how_to_use_text": """1️⃣ <b>Wähle, welche Sprache du lernst</b>
🦾 Einstellungen → 🎯 Welche Sprache lernen: {languages}.
Dort auch das Niveau A1–C2, die Übersetzungsrichtung und die Oberflächensprache.
Der Fortschritt zählt pro Sprache getrennt: du kannst zwei parallel lernen.

2️⃣ <b>Wähle den Quiz-Modus</b>
🦾 Einstellungen → 📝 Quiz-Modus:
• Nach Niveau — Wörter deines Niveaus
• Nach Kategorie — 20 Themen: Essen, Arbeit, Reisen...
• Top 10 Tausend — die ganze Datenbank
• Schwierige — Wörter, bei denen du oft Fehler machst

3️⃣ <b>Lerne jeden Tag</b>
📚 Wörter lernen → Quiz aus 25 Wörtern.
Der Bot merkt sich deine Fehler und zeigt schwierige Wörter häufiger.

4️⃣ <b>Wiederhole die Fehler</b>
Nach dem Quiz kannst du die Wörter sofort wiederholen, bei denen du falsch lagst.

5️⃣ <b>Verfolge deinen Fortschritt</b>
📊 Statistik → wie viel gelernt ist, Quiz-Verlauf, Serie.

6️⃣ <b>Tritt gegen andere an</b>
🏆 Meine Platzierung → deine Punkte für den Monat und insgesamt.
📊 Rangliste → die Top 10 aller Teilnehmer.
Die Rangliste läuft pro Sprache getrennt — wer Englisch lernt, tritt gegen andere Englischlernende an.

7️⃣ <b>Richte Erinnerungen ein</b>
🦾 Einstellungen → 🔔 Erinnerungen → wähle Zeit, Tage und Zeitzone.

🔊 <b>Aussprache</b>
Das Wort erklingt mit der Stimme eines Muttersprachlers: in der Frage das Wort allein, nach der Antwort das Wort zusammen mit dem Beispiel. So hörst du die Aussprache und wie das Wort in echter Rede lebt.
🦾 Einstellungen → 🔊 Aussprache: abschaltbar, Stimme wählbar. Für Deutsch drei männliche und drei weibliche — ein Tippen spielt sofort eine Probe.
In der umgekehrten Richtung kommt der Ton nach der Antwort: sonst wäre das gesprochene Wort schon die Lösung.

━━━━━━━━━━━━━━━━━
💡 Ein Wort ist <b>gelernt</b> — 3 richtige Antworten in Folge, und nicht am Tag des ersten Kontakts: du musst mindestens am nächsten Tag darauf zurückkommen.
🔥 Die <b>Serie</b> wächst, wenn du an diesem Tag mindestens 1 Quiz gemacht hast.
📝 Fehler gefunden? Tippe nach dem Quiz auf die Taste und sage, was nicht stimmt — Übersetzung oder Aussprache. Meldungen zur Aussprache sind besonders nötig: die Maschine hört die Betonung nicht.

Fragen? → t.me/genaulingua_chat""",


    "help_community_title": "💬 <b>GenauLingua Community</b>",
    "help_community_text": """👉 <b>t.me/genaulingua_chat</b>

Im Chat:
📢 Du erfährst zuerst von Neuerungen
🐛 Fehler gefunden — schreib oder schick einen Screenshot
📝 Fehler in der Übersetzung — melde ihn, wir korrigieren
💡 Ideen und Wünsche — wir lesen alles und nehmen es auf
👥 Austausch mit anderen Lernenden

━━━━━━━━━━━━━━━━━
Je lebendiger die Community, desto besser wird der Bot. Nur keine Scheu! 🙌""",


    # ============================================================================
    # PLATZIERUNG
    # ============================================================================
    "rating_title_monthly": "🏆 <b>Meine Platzierung — {month} {year}</b>",
    "rating_not_active": "❌ Die Platzierung ist noch nicht aktiv.",
    "rating_not_in_ranking": "📍 Du bist noch nicht in der Rangliste",
    "rating_start_quiz": "🚀 Mach dein erstes Quiz!",
    "rating_position": "📍 Platz: <b>#{rank}</b> von {total}",
    "rating_points": "💎 Punkte: <b>{score}</b>",
    "rating_your_month": "⭐ <b>Dein {month}:</b>",
    "rating_quizzes": "├ Quizze: {count}",
    "rating_words_learned": "├ Wörter gelernt: {count}",
    "rating_streak": "├ Serie: {count} T.",
    "rating_avg_result": "└ Durchschnitt: {percent}%",
    "rating_goal": "🎯 Bis #{rank} ({name}): noch {diff} Punkte",
    "rating_scoring_title": "💡 <b>So verdienst du Punkte:</b>",
    "rating_scoring_quiz": "• Absolviertes Quiz → +10",
    "rating_scoring_reverse": "• Modus «Umgekehrt» → +5",
    "rating_scoring_word": "• Gelerntes Wort → +2",
    "rating_scoring_streak": "• Tag in Folge → +3",
    "rating_scoring_bonus": "• Treffsicherheit 90%+ → +50 Bonus",
    "rating_scoring_report": "• Bestätigte Meldung → +1",

    "rating_title_alltime": "🏆 <b>Meine Platzierung — Insgesamt</b>",
    "rating_position_alltime": "📍 Platz: <b>#{rank}</b>",
    "rating_position_none": "📍 Platz: <b>—</b>",
    "rating_achievements": "⭐ <b>Deine Erfolge:</b>",
    "rating_wins": "├ Siege (1. Platz): {count}",
    "rating_total_words": "└ Wörter gelernt: {count}",
    "rating_motivation_start": "🚀 Fang an, Wörter zu lernen — der erste Schritt ist der wichtigste!",
    "rating_motivation_continue": "🎯 Mach weiter — der erste Sieg ist nah!",
    "rating_motivation_champion": "🔥 Du bist ein echter Champion!",
    "rating_lifetime_title": "🌟 <b>Lifetime-Punkte — das sind:</b>",
    "rating_lifetime_desc": "• Alle Punkte aus allen Monaten\n• +100 für 🥇 · +50 für 🥈 · +25 für 🥉",

    "table_title_monthly": "📊 <b>Rangliste — {month} {year}</b>",
    "table_title_alltime": "📊 <b>Rangliste — Insgesamt</b>",
    "table_empty": "Noch nimmt niemand teil.\nMach das Quiz als Erster! 💪",
    "table_you_in_top": "📍 Du: <b>#{rank}</b> von {total}",
    "table_you_not_in_top": "📍 Du: <b>#{rank}</b> von {total} — {score} Punkte",
    "table_you_outside": "📍 Du: außerhalb der Top 10 — {score} Punkte",
    "table_you_not_ranked": "📍 Du bist noch nicht in der Rangliste",
    "table_points": "Punkte",
    "btn_leaderboard_table": "📊 Rangliste",
    "btn_back_to_rating": "◀️ Zurück zur Platzierung",

    # ============================================================================
    # STATISTIK (NEU)
    # ============================================================================
    "stats_header": "📊 <b>Deine Statistik</b>",
    "stats_learned_of": "└─ Gelernt <b>{learned}</b> von {total}",
    "stats_details": "⏳ In Arbeit: {progress}\n🆕 Neu: {new}\n⚠️ Schwierig: {difficult}",
    "stats_achievements_title": "<b>Deine Erfolge</b>",
    "stats_words_count": "├─ Wörter gelernt: <b>{count}</b>",
    "stats_streak_line": "└─ Serie: <b>{days} Tage in Folge</b>",
    "stats_quizzes_header": "<b>Quizze · {level}</b>",
    "stats_quizzes_passed_line": "├─ Absolviert: <b>{count}</b>",
    "stats_quizzes_avg_line": "├─ Durchschnitt: <b>{percent}%</b>",
    "stats_quizzes_best_line": "└─ Bestes Ergebnis: <b>{percent}%</b>",
    "stats_quizzes_empty": "└─ Noch keine absolvierten Quizze",
    "stats_recent_header": "📈 <b>Letzte Quizze</b>",
    "stats_overall_header": "🌍 <b>Gesamtfortschritt</b>",
    "stats_overall_learned": "└─ Gelernt <b>{learned}</b> von {total} Wörtern",
    "stats_cta_start": "💪 Fang an, Wörter zu lernen — der erste Schritt ist der wichtigste!",
    "stats_cta_begin": "🚀 Starker Anfang! Bleib dabei!",
    "stats_cta_halfway": "🔥 Du bist auf halbem Weg! Nicht aufhören!",
    "stats_cta_almost": "🏆 Fast am Ziel! Gut gemacht!",
    "stats_explanation": "—————————————————————\nEin Wort ist gelernt = 3 richtige Antworten in Folge",
    "stats_btn_rating": "🏆 Meine Platzierung",
}

# ============================================================================
# MEHRSPRACHIGKEIT: Lernsprache, Bedeutungssprache und Richtung
# ============================================================================
TEXTS.update({
    # Namen der Sprachen
    "langname_de": "🇩🇪 Deutsch",
    "langname_en": "🇬🇧 Englisch",
    "langname_ru": "🏴 Russisch",
    "langname_uk": "🇺🇦 Ukrainisch",
    "langname_tr": "🇹🇷 Türkisch",
    "langname_pl": "🇵🇱 Polnisch",
    # Bindewort für die Aufzählung der Sprachen in Hilfe und Begrüßung
    "and_word": "und",

    # Zeilen im Einstellungsmenü
    "settings_learning_lang_line": "🎯 Ich lerne: <b>{language}</b>",

    "settings_btn_learning_lang": "🎯 Welche Sprache lernen",

    # Bildschirm «Welche Sprache lernen»
    "learning_lang_title": "🎯 <b>Welche Sprache lernen</b>",
    "learning_lang_description": "Wähle die Sprache, deren Wörter du lernen willst.\nDer Fortschritt zählt pro Sprache getrennt.",
    "learning_lang_set": "✅ Wir lernen: {language}",
    # Zeile im Einstellungsmenü und Bildschirm «Aussprache»
    "settings_audio_line": "🔊 Aussprache: <b>{state}</b>",
    "settings_btn_audio": "🔊 Aussprache",
    "audio_state_on": "ein",
    "audio_state_off": "aus",

    "audio_title": "🔊 <b>Aussprache</b>",
    "audio_description": "Das Wort erklingt mit der Stimme eines Muttersprachlers. In der Frage das Wort allein, nach der Antwort das Wort zusammen mit dem Beispiel.",
    "audio_current_voice": "🎙 Stimme: <b>{voice}</b>",
    "audio_btn_turn_on": "🔊 Aussprache einschalten",
    "audio_btn_turn_off": "🔇 Aussprache ausschalten",
    "audio_btn_choose_voice": "🎙 Stimme wählen",
    "audio_turned_on": "✅ Aussprache eingeschaltet",
    "audio_turned_off": "🔇 Aussprache ausgeschaltet",

    "voice_title": "🎙 <b>Stimme wählen</b>",
    "voice_description": "Tippe auf eine Stimme, um sie zu hören. Der Haken zeigt die gewählte.",
    "voice_male": "Männlich",
    "voice_female": "Weiblich",
    "voice_set": "✅ Stimme: {voice}",
    "voice_only_one": "Für diese Sprache hat der Synthesizer eine männliche und eine weibliche Stimme — mehr gibt es nicht.",
    "voice_preview_failed": "Die Probe konnte nicht geladen werden, versuche es noch einmal",
})


# ============================================================================
# АПГРЕЙД ПОД ШЕСТЬ ЯЗЫКОВ
#
# Добавлено, когда бот перестал быть «ботом для немецкого»: при первом запуске
# человек теперь выбирает не только язык интерфейса, но и какой язык учить, а
# подсказки направления стали работать на все тридцать пар вместо восьми.
# ============================================================================
TEXTS.update({
    "btn_rating": "🏆 Rangliste",
    "friend_fallback": "Freund",
    "onboarding_learning_title": "🎯 <b>Welche Sprache lernst du?</b>",
    "onboarding_learning_desc": "Die Bedeutungen erscheinen auf {native}\nSprache und Richtung kannst du jederzeit in den Einstellungen ändern.",
    "mode_hint_forward": "💡 {learning} → {native} ist leichter: die Bedeutung lässt sich erraten",
    "mode_hint_reverse": "💡 {native} → {learning} ist schwerer: prägt die Wörter besser ein",
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
    "help_how_to_use_text": "🎮 <b>Quiz</b>\n25 Wörter, vier Antworten. Der Bot merkt sich deine Fehler und zeigt Schweres öfter. Nach dem Quiz kannst du die Fehler sofort wiederholen.\n\n🔊 <b>Aussprache</b>\nIn der Frage klingt das Wort, nach der Antwort das Wort mit seinem Beispiel. Die Stimme wählst du in den Einstellungen — männlich oder weiblich.\n\n🌍 <b>Sprachen</b>\n{languages} — in jedem Paar und in beide Richtungen. Fortschritt und Platzierung zählen pro Sprache getrennt.\n\n━━━━━━━━━━━━━━━━━\n💡 Ein Wort gilt als <b>gelernt</b> nach drei richtigen Antworten hintereinander, und zwar an verschiedenen Tagen.\n🔥 Die <b>Serie</b> wächst mit jedem Quiz an diesem Tag.\n📝 Fehler in Übersetzung oder Aussprache — der Knopf unter dem Quiz.",
    "help_community_title": "💬 <b>Über den Bot und die Gemeinschaft</b>",
    "help_community_text": "🤖 <b>GenauLingua</b> — {language_count} Sprachen in jedem Paar: {languages}\n12 900 Wörter A1–C2, jedes mit Beispiel und Muttersprachler-Aussprache.\nOberfläche: {interface_languages}\n\n💬 <b>t.me/genaulingua_chat</b>\nFehler, falsche Übersetzungen, Ideen — wir lesen alles. Hinweise zur Aussprache sind besonders willkommen: eine Maschine hört die Betonung nicht.",
})


# ============================================================================
# ВОПРОС НА СЛУХ
#
# Самого слова на экране нет — иначе слушать незачем. Варианты стоят на
# ИЗУЧАЕМОМ языке: спрашивают «что услышал», а не «что это значит».
# ============================================================================
TEXTS.update({
    "quiz_question_listen": "🔊 Hör zu und wähle, was du gehört hast:",
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
    "rating_scoring_answer": "• Richtige Antwort → +1, nach Gehör → +2, laut → +3",
    "rating_scoring_quiz": "• Runde beendet → +10",
    "rating_scoring_reverse": "• Umgekehrte Richtung → +5",
    "rating_scoring_word": "• Wort gelernt → +3",
    "rating_scoring_streak": "• Jeder Tag in Folge zählt mehr, bis +10",
    "rating_scoring_bonus": "• Genauigkeit über 60% — je höher, desto mehr",
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
    "voice_not_ready_hint": "<i>· neben einer Stimme heißt: noch nicht vollständig aufgenommen — das Wort wird live erzeugt, manchmal verzögert oder ohne Ton</i>",
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
    "settings_btn_channels": "🎮 Aufbau der Übung",
    "settings_channels_line": "🎮 Übung: <b>{channels}</b>",
    "channels_title": "🎮 <b>Aufbau der Übung</b>",
    "channels_description": "Welche Fragen gestellt werden. Je mehr Kanäle, desto fester sitzt ein Wort: es mit den Augen erkennen, nach Gehör erkennen und aussprechen sind drei verschiedene Fähigkeiten.",
    "channel_text": "🔤 Karte",
    "channel_audio": "🎧 Nach Gehör",
    "channel_speech": "🎤 Sprechen",
    "channels_text_always": "🔤 Karten lassen sich nicht abschalten: eine Übung ohne Kanal ist ein leerer Bildschirm.",
    "channels_audio_blocked": "🎧 Nach Gehör nicht verfügbar: die Aussprache ist aus.",
    "channels_speech_soon": "🎤 Sprechen kommt bald.",
    "channels_need_one": "Mindestens ein Kanal muss bleiben",
})


# ============================================================================
# ВОПРОС ВСЛУХ
#
# Ответ приходит голосовым сообщением, а не нажатием. Распознаватель отвечает
# на вопрос «то ли слово сказано», и только на него: качество произношения он
# судить не умеет — он обучен ПОНИМАТЬ акцент, а не замечать его.
# ============================================================================
TEXTS.update({
    "quiz_question_speak": "🎤 Sprich dieses Wort laut aus — nimm eine Sprachnachricht auf",
    "speech_btn_reference": "🔊 Anhören",
    "speech_btn_skip": "⏭ Überspringen",
    "speech_listening": "🎧 Ich höre zu…",
    "speech_heard": "Gehört: <i>{heard}</i>",
    "speech_not_understood": "🤔 Nicht verstanden. Nimm es noch einmal auf — näher am Mikrofon und etwas lauter.",
    "speech_send_voice": "🎤 Diese Frage wird mit einer Sprachnachricht beantwortet. Halte die Mikrofontaste gedrückt.",
    "speech_skipped": "⏭ Übersprungen",
    "quiz_result_spoken": "🎤 Gesprochen: {count}",
})


# ============================================================================
# ДОМАШНИЙ ЭКРАН: ТРИ ШКАЛЫ
# ============================================================================
TEXTS.update({
    "home_scale_text": "Geschrieben",
    "home_scale_audio": "Gehört",
    "home_scale_speech": "Gesprochen",
    "home_btn_learn": "▶️ Üben · {count}",
    "home_streak": "🔥 Serie: {days}",
    "home_rank": "🏆 Platz: {rank}",
    "home_hint": "Der Balken ist der Anteil der Wörter, die du schon getroffen hast: drei richtige Antworten über einen Kanal, und das Wort zählt für ihn. Der Abstand zwischen den Skalen zeigt, was fehlt.",
    "home_channel_not_ready": "{channel}: noch zu früh. Bereit sind {ready} Wörter, nötig sind mindestens {minimum}. Übe mit Karten — sie schalten die anderen Kanäle frei.",
})


# ============================================================================
# НАСТРОЙКИ: ТРИ ГРУППЫ
#
# «Что учу» человек меняет часто, «как мне удобно» ставит один раз. Восемь
# равных пунктов перемешивали то и другое, и первым в списке стоял режим
# викторины, которым не пользуются 96%.
# ============================================================================
TEXTS.update({
    "settings_group_what": "🎯 Was ich lerne",
    "settings_group_what_title": "<b>🎯 Was ich lerne</b>",
    "settings_group_how": "🎮 Wie ich lerne",
    "settings_group_how_title": "<b>🎮 Wie ich lerne</b>",
    "settings_group_bot": "🔧 Bot",
    "settings_group_bot_title": "<b>🔧 Bot</b>",
})
