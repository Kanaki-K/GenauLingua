"""
Polska lokalizacja dla GenauLingua Bot

Набор ключей совпадает с остальными локалями — это проверяется тестом
test_all_locales_have_identical_key_sets. Подсказки режимов перевода
(settings_mode_hint_*) намеренно оставлены на языке самого режима: так они
устроены во всех локалях.
"""

TEXTS = {
    # ============================================================================
    # MENU GŁÓWNE
    # ============================================================================
    "btn_learn_words": "📚 Ucz się słów",
    "btn_stats": "📊 Statystyki",
    "btn_settings": "🦾 Ustawienia",
    "btn_help": "❓ Pomoc",
    "btn_back": "◀️ Wróć",
    "menu_placeholder": "Wybierz działanie...",

    # ============================================================================
    # POWITANIE I START
    # ============================================================================
    "welcome_title": "👋 <b>Cześć, {name}!</b>",






    "welcome_choose_level": "🎯 <b>Od czego zaczniemy?</b>\n\nTwój poziom — {language}\n\n• A1–A2 — podstawowe słownictwo\n• B1–B2 — swobodna rozmowa\n• C1–C2 — biegła znajomość",
    "choose_level_prompt": "Wybierz poziom:",

    "level_selected": "✅ Poziom <b>{level}</b> wybrany.\n\n12 902 słowa, sześć języków. Zacznijmy od piętnastu.",
    "level_locked": "🔒 Ten poziom jest jeszcze w przygotowaniu",

    # ============================================================================
    # PRZYPOMNIENIA
    # ============================================================================
    "notif_title": "🔔 <b>Przypomnienia</b>",
    "notif_status": "Stan: {status}",
    "notif_status_on": "🔔 Włączone",
    "notif_status_off": "🔕 Wyłączone",
    "notif_time": "Godzina: {time}",
    "notif_days": "Dni: {days}",
    "notif_timezone": "Strefa czasowa: {timezone}",
    "notif_hint": "💡 Przypomnienia przyjdą o podanej godzinie w twojej strefie czasowej.",
    "notif_hint_off": "💡 Włącz przypomnienia, żeby nie zapominać o codziennej nauce!",

    "notif_btn_toggle_on": "🔔 Przypomnienia: Włączone",
    "notif_btn_toggle_off": "🔕 Przypomnienia: Wyłączone",
    "notif_btn_time": "🕐 Godzina: {time}",
    "notif_btn_days": "📅 Wybierz dni",
    "notif_btn_timezone": "🌍 Zmień strefę czasową",

    "notif_timezone_title": "🌍 <b>Wybierz swoją strefę czasową</b>",
    "notif_timezone_current": "Obecnie: {timezone}",
    "notif_timezone_prompt": "Wybierz miasto w swojej strefie czasowej:",
    "notif_timezone_more": "🌍 Wybierz inne miasto ▼",
    "notif_timezone_back": "◀️ Wróć",
    "notif_timezone_set": "✅ Strefa czasowa ustawiona: {city}",

    "notif_time_title": "🕐 <b>Wybierz godzinę przypomnienia</b>",
    "notif_time_current": "Obecna godzina: {time}",
    "notif_time_timezone": "Strefa czasowa: {timezone}",
    "notif_time_hint": "Przypomnienie będzie przychodzić codziennie o wybranej godzinie.",
    "notif_time_set": "✅ Godzina ustawiona: {time}",

    "notif_days_title": "📅 <b>Wybierz dni przypomnień</b>",
    "notif_days_hint": "Naciśnij dzień, żeby go włączyć lub wyłączyć.\n✅ Zielony haczyk — dzień włączony\n❌ Czerwony krzyżyk — dzień wyłączony\n\nGdy skończysz — naciśnij «Zapisz».",
    "notif_days_all": "📅 Wszystkie dni",
    "notif_days_weekdays": "🗓️ Dni powszednie (pn–pt)",
    "notif_days_save": "💾 Zapisz",
    "notif_days_saved": "✅ Dni zapisane!",
    "notif_days_all_selected": "✅ Wybrano wszystkie dni",
    "notif_days_weekdays_selected": "✅ Wybrano dni powszednie (pn–pt)",
    "notif_days_none": "⚠️ Wybierz przynajmniej jeden dzień przypomnień!",

    "notif_toggle_on": "🔔 Przypomnienia włączone!",
    "notif_toggle_off": "🔕 Przypomnienia wyłączone",

    "notif_message_btn_disable": "🔕 Wyłącz przypomnienia",

    "day_mon": "Pn",
    "day_tue": "Wt",
    "day_wed": "Śr",
    "day_thu": "Cz",
    "day_fri": "Pt",
    "day_sat": "So",
    "day_sun": "Nd",

    "notif_btn_back": "◀️ Wróć do ustawień",

    "notif_default_name": "przyjacielu",
    "notif_message_greeting": "🔥 <b>Czas na naukę, {name}!</b>",

    "notif_motivation_1": "Krok po kroku dojdziesz do celu!",
    "notif_motivation_2": "Twoja seria rośnie — tak dalej!",
    "notif_motivation_3": "Dziś kolejny krok do biegłej znajomości!",
    "notif_motivation_4": "Mały wysiłek codziennie = duży wynik!",
    "notif_motivation_5": "Jesteś na dobrej drodze! Nie zatrzymuj się!",
    "notif_motivation_6": "Każdy quiz przybliża cię do celu!",

    # ============================================================================
    # USTAWIENIA
    # ============================================================================
    "settings_title": "🦾 <b>Ustawienia</b>",
    "settings_level": "📚 Poziom: <b>{level}</b>",
    "settings_mode": "🔄 Tłumaczenie: <b>{mode}</b>",
    "settings_language": "🌍 Język interfejsu: <b>{language}</b>",
    "settings_choose": "Wybierz, co chcesz zmienić:",

    "settings_btn_quiz_mode": "📝 Tryb quizu",
    "settings_btn_change_mode": "🔄 Kierunek tłumaczenia",
    "settings_btn_change_language": "🌍 Język interfejsu",
    "settings_btn_notifications": "🔔 Przypomnienia",

    "settings_quiz_mode_line": "📝 Tryb: <b>{mode}</b>",

    "settings_mode_title": "🔄 <b>Kierunek tłumaczenia</b>",
    "settings_mode_description": "Wybierz kierunek tłumaczenia:",

    "settings_language_title": "🌍 <b>Język interfejsu</b>",
    "settings_language_description": "Wybierz język interfejsu bota:",

    "language_changed": "✅ Język zmieniony na {language}",
    "level_not_selected": "Nie wybrano",
    "user_not_found": "❌ Nie znaleziono użytkownika. Użyj /start",

    # Nazwy języków interfejsu — każda w swoim języku
    "lang_ru": "🏴 Русский",
    "lang_uk": "🇺🇦 Українська",
    "lang_en": "🇬🇧 English",
    "lang_tr": "🇹🇷 Türkçe",
    "lang_de": "🇩🇪 Deutsch",
    "lang_pl": "🇵🇱 Polski",

    # Kierunki tłumaczenia
    "mode_de_to_ru": "🇩🇪 DE → 🏴 RU",
    "mode_ru_to_de": "🏴 RU → 🇩🇪 DE",
    "mode_de_to_uk": "🇩🇪 DE → 🇺🇦 UK",
    "mode_uk_to_de": "🇺🇦 UK → 🇩🇪 DE",
    "mode_de_to_en": "🇩🇪 DE → 🇬🇧 EN",
    "mode_en_to_de": "🇬🇧 EN → 🇩🇪 DE",
    "mode_de_to_tr": "🇩🇪 DE → 🇹🇷 TR",
    "mode_tr_to_de": "🇹🇷 TR → 🇩🇪 DE",

    # ============================================================================
    # TRYB QUIZU
    # ============================================================================
    "qmode_title": "📝 <b>Tryb quizu</b>",
    "qmode_current": "Teraz: <b>{mode}</b>",
    "qmode_choose": "Wybierz, jak chcesz uczyć się słów\nMożesz zmienić w każdej chwili — postępy zostają",

    "qmode_btn_level": "📚 Po poziomie",
    "qmode_btn_category": "🗂 Kategoria",
    "qmode_btn_all": "🌍 Top 10 tysięcy",
    "qmode_btn_difficult": "⚠️ Trudne",

    "qmode_level_short": "📚 Poziom {level}",
    "qmode_category_short": "🗂 {category}",
    "qmode_all_short": "🌍 Top 10 tysięcy",
    "qmode_difficult_short": "⚠️ Trudne słowa",

    "qmode_level_title": "📚 <b>Wybór poziomu</b>",
    "qmode_level_desc": "Od pierwszego «Hallo» do swobodnych dyskusji\nWszystkie poziomy są dostępne — wybierz swój!\n\n• A1–A2 — podstawowe słownictwo\n• B1–B2 — swobodna rozmowa\n• C1–C2 — biegła znajomość",
    "qmode_level_set": "✅ Tryb: Po poziomie ({level})",

    "qmode_category_title": "🗂 <b>Wybór kategorii</b>",
    "qmode_category_desc": "Od jedzenia do nauki — wybierz temat, który ci potrzebny\n\nKażda kategoria zawiera słowa ze wszystkich poziomów",
    "qmode_category_set": "✅ Tryb: {category}",

    # Nazwy kategorii
    "cat_arbeit_beruf": "Praca",
    "cat_bildung_lernen": "Nauka",
    "cat_einkaufen_geld": "Zakupy",
    "cat_emotionen_charakter": "Emocje",
    "cat_essen_trinken": "Jedzenie",
    "cat_freizeit_sport": "Sport",
    "cat_gesundheit_medizin": "Zdrowie",
    "cat_grammatik": "Gramatyka",
    "cat_kleidung_mode": "Ubrania",
    "cat_kommunikation": "Komunikacja",
    "cat_kultur_kunst": "Kultura",
    "cat_mensch_familie": "Rodzina",
    "cat_natur_wetter": "Przyroda",
    "cat_recht_staat": "Prawo",
    "cat_reisen_transport": "Podróże",
    "cat_technik_digital": "Technika",
    "cat_wirtschaft": "Gospodarka",
    "cat_wissenschaft": "Nauka ścisła",
    "cat_wohnen_haus": "Mieszkanie",
    "cat_zeit_alltag": "Codzienność",

    "qmode_all_set": "✅ Tryb: Top 10 tysięcy",

    "qmode_difficult_set": "✅ Tryb: Trudne słowa",
    "qmode_difficult_few": "Masz na razie tylko {count} trudnych słów — potrzeba przynajmniej 4\nZrób jeszcze kilka quizów!",
    "qmode_difficult_empty": "Nie masz na razie trudnych słów.\nZrób kilka quizów!",

    "quiz_btn_change_mode": "⚙️ Tryb quizu",
    "quiz_btn_report_error": "📝 Zgłoś błąd",
    "report_btn_confirm": "✅ Potwierdź ({count})",
    "report_btn_send": "📨 Wyślij",
    "report_no_words": "Brak słów do zgłoszenia",
    "report_none_selected": "Wybierz przynajmniej jedno słowo",
    "report_sent": "✅ Wysłano {count} zgłoszeń — dziękujemy!\nJeśli błąd się potwierdzi, dostaniesz +{points} punktów",
    "report_daily_limit": "⚠️ Dzienny limit zgłoszeń wyczerpany (maks. 20)",
    "report_all_reported": "✅ Wszystkie słowa z tego quizu są już zgłoszone",
    "report_already_sent": "✔️ Już wysłane wcześniej",
    "report_kind_title": "Co konkretnie jest nie tak?",
    "report_btn_kind_text": "📝 Błędne tłumaczenie",
    "report_btn_kind_audio": "🔊 Błędna wymowa",
    "report_sent_audio": "✅ Wysłano {count} — dziękujemy!\nZgłoszenia wymowy są szczególnie cenne: sprawdzanie maszynowe nie słyszy akcentu\nJeśli się potwierdzi — +{points} punktów",
    "report_approved": "✅ Twoje zgłoszenie przyjęte: <b>{word}</b> poprawiono.\n+{points} punktów do wyniku miesiąca — dzięki, słownik stał się lepszy dla wszystkich.",
    "report_approved_audio": "✅ Zgłoszenie wymowy przyjęte: <b>{word}</b>.\nNagranie powstanie na nowo. +{points} punktów do wyniku miesiąca — dzięki.",

    # ============================================================================
    # QUIZ
    # ============================================================================
    "quiz_no_level": "⚠️ Najpierw wybierz swój poziom poleceniem /start",
    "quiz_error_generation": "❌ Przy przygotowaniu quizu wystąpił błąd.\nSpróbuj jeszcze raz przez /start",
    "quiz_no_words": "❌ Niestety dla tego poziomu nie ma jeszcze słów.\nWybierz inny poziom.",

    "quiz_question_number": "Pytanie {current}/{total}",
    "quiz_question_choose_word": "Wybierz właściwe słowo:",
    "quiz_question_choose_translation": "Wybierz właściwe tłumaczenie:",

    "quiz_correct": "✅ <b>Dobrze!</b>",
    "quiz_wrong": "❌ <b>Źle!</b>",
    "quiz_correct_answer": "Prawidłowa odpowiedź:",

    "quiz_btn_next": "Dalej →",
    "quiz_btn_repeat_errors": "🔄 Powtórz błędy",

    "quiz_completed": "🎉 <b>Quiz ukończony!</b>",
    "quiz_result_correct": "✅ Dobrze: <b>{correct}/{total}</b>",
    "quiz_result_percentage": "📈 Wynik: <b>{percentage}%</b>",
    "quiz_result_details": "📝 <b>Szczegóły:</b>",
    "quiz_result_errors": "❌ Błędów: {count}",

    # POCHWAŁA NA KONIEC RUNDY — tylko za to, co się stało
    "praise_first_round": "Pierwsza runda za tobą. Dalej słowa zaczną wracać — tak się je pamięta.",
    "praise_first_learned": "Pierwsze słowo nauczone: trzy poprawne odpowiedzi z rzędu i poznane nie dziś.",
    "praise_learned": "Nauczone słowa w tej rundzie: {count}",
    "praise_best_streak": "Rekord osobisty: {days} dni z rzędu",
    "praise_milestone": "Próg {count} osiągnięty",
    "praise_first_speech": "Pierwsza poprawna odpowiedź głosem",
    "praise_first_audio": "Pierwsza poprawna odpowiedź ze słuchu",
    "praise_comeback": "Witaj z powrotem. Przerwa trwała {days} dni.",
    "praise_perfect": "Runda bez błędu",
    "praise_streak": "Seria: {days} dni z rzędu",
    "praise_new_words": "Nowe słowa: {count}",
    "praise_returned": "Rozpoznane ponownie: {count}",
    "praise_progress": "Słów w pracy: {count} · do {target} jeszcze {left}",
    "praise_progress_top": "Słów w pracy: {count}",
    "praise_points": "Punkty: +{points}",

    "quiz_repeat_title": "🔄 <b>Powtórka błędów</b>",
    "quiz_repeat_question": "🔄 Powtórka {current}/{total}",
    "quiz_no_errors": "✅ Nie miałeś żadnych błędów!",
    "quiz_error_next": "❌ Nie udało się wczytać następnego pytania.",
    "quiz_error_generate": "❌ Nie udało się utworzyć następnego pytania.",

    # ============================================================================
    # STATYSTYKI
    # ============================================================================
    "stats_title": "📊 <b>Statystyki</b>",
    "stats_no_level": "⚠️ <b>Najpierw wybierz poziom!</b>\n\nUżyj polecenia /start, żeby zacząć.",

    "stats_all_words": "📚 Cała baza ({count} słowo|słowa|słów)",
    "stats_learned": "✅ Nauczone: {count}",
    "stats_in_progress": "🔄 W toku: {count}",
    "stats_new": "🆕 Nowe: {count}",
    "stats_difficult": "❌ Trudne: {count}",

    "stats_level_title": "🎯 Poziom {level} · {mode} ({count} słowo|słowa|słów)",
    "stats_quizzes_title": "🏆 <b>Quizy (poziom {level}):</b>",
    "stats_quizzes_passed": "Ukończone: {count}",
    "stats_quizzes_avg": "Średni wynik: {percentage}%",
    "stats_quizzes_best": "Najlepszy wynik: {percentage}%",
    "stats_quizzes_none": "Nie zrobiłeś jeszcze quizów na tym poziomie.",

    "stats_activity_title": "🔥 <b>Aktywność:</b>",
    "stats_streak": "└─ Seria: <b>{days}</b> dni z rzędu",

    "stats_recent_title": "<b>Ostatnie quizy:</b>",
    "stats_learned_explanation": "💡 <b>Nauczone</b> — 3 dobre odpowiedzi z rzędu, i nie w dniu pierwszego spotkania ze słowem",

    # ============================================================================
    # POMOC
    # ============================================================================
    "help_title": "❓ <b>Pomoc — GenauLingua</b>",
    "help_description": "Tu znajdziesz instrukcję, dowiesz się, co wkrótce pojawi się w bocie, i jak skontaktować się ze społecznością.",
    "help_choose": "Wybierz dział:",

    "help_btn_how_to_use": "📖 Jak korzystać",
    "help_btn_community": "💬 Społeczność",

    "help_how_to_use_title": "📖 <b>Jak korzystać z bota</b>",
    "help_how_to_use_text": """1️⃣ <b>Wybierz, jakiego języka się uczysz</b>
🦾 Ustawienia → 🎯 Jakiego języka się uczyć: {languages}.
Tam też poziom A1–C2, kierunek tłumaczenia i język interfejsu.
Postępy liczą się osobno dla każdego języka: możesz uczyć się dwóch równolegle.

2️⃣ <b>Wybierz tryb quizu</b>
🦾 Ustawienia → 📝 Tryb quizu:
• Po poziomie — słowa twojego poziomu
• Po kategorii — 20 tematów: jedzenie, praca, podróże...
• Top 10 tysięcy — cała baza słów
• Trudne — słowa, w których często się mylisz

3️⃣ <b>Ucz się codziennie</b>
📚 Ucz się słów → quiz z 25 słów.
Bot pamięta twoje błędy i częściej pokazuje trudne słowa.

4️⃣ <b>Powtarzaj błędy</b>
Po quizie możesz od razu powtórzyć słowa, w których się pomyliłeś.

5️⃣ <b>Śledź postępy</b>
📊 Statystyki → ile nauczone, historia quizów, seria.

6️⃣ <b>Rywalizuj z innymi</b>
🏆 Moja pozycja → twoje punkty za miesiąc i za cały czas.
📊 Tabela liderów → top 10 wszystkich uczestników.
Ranking jest osobny dla każdego języka — uczący się angielskiego rywalizują między sobą.

7️⃣ <b>Ustaw przypomnienia</b>
🦾 Ustawienia → 🔔 Przypomnienia → wybierz godzinę, dni i strefę czasową.

🔊 <b>Wymowa</b>
Słowo wybrzmiewa głosem native speakera: w pytaniu samo słowo, po odpowiedzi — słowo razem z przykładem. Tak słychać i wymowę, i to, jak słowo żyje w mowie.
🦾 Ustawienia → 🔊 Wymowa: można wyłączyć albo wybrać głos. Dla niemieckiego trzy męskie i trzy żeńskie, naciśnięcie od razu odtwarza próbkę.
W kierunku odwrotnym dźwięk przychodzi po odpowiedzi: inaczej wypowiedziane słowo byłoby odpowiedzią.

━━━━━━━━━━━━━━━━━
💡 Słowo jest <b>nauczone</b> — 3 dobre odpowiedzi z rzędu, i nie w dniu pierwszego spotkania: trzeba wrócić do niego przynajmniej następnego dnia.
🔥 <b>Seria</b> rośnie, jeśli zrobiłeś tego dnia przynajmniej 1 quiz.
📝 Znalazłeś błąd? Naciśnij przycisk po quizie i powiedz, co nie tak — tłumaczenie czy wymowa. Zgłoszenia wymowy są szczególnie potrzebne: maszyna nie słyszy akcentu.

Pytania? → t.me/genaulingua_chat""",


    "help_community_title": "💬 <b>Społeczność GenauLingua</b>",
    "help_community_text": """👉 <b>t.me/genaulingua_chat</b>

Na czacie:
📢 Pierwszy dowiesz się o nowościach
🐛 Znalazłeś błąd — pisz albo przyślij zrzut ekranu
📝 Błąd w tłumaczeniu — zgłaszaj, poprawimy
💡 Pomysły i życzenia — wszystko czytamy i bierzemy do pracy
👥 Rozmowy z innymi uczącymi się

━━━━━━━━━━━━━━━━━
Im aktywniejsza społeczność, tym lepszy bot. Nie krępuj się! 🙌""",


    # ============================================================================
    # RANKING
    # ============================================================================
    "rating_title_monthly": "🏆 <b>Moja pozycja — {month} {year}</b>",
    "rating_not_active": "❌ Ranking nie jest jeszcze aktywny.",
    "rating_not_in_ranking": "📍 Nie jesteś jeszcze w rankingu",
    "rating_start_quiz": "🚀 Zrób pierwszy quiz!",
    "rating_position": "📍 Pozycja: <b>#{rank}</b> z {total}",
    "rating_points": "💎 Punkty: <b>{score}</b>",
    "rating_your_month": "⭐ <b>Twój {month}:</b>",
    "rating_quizzes": "├ Quizy: {count}",
    "rating_words_learned": "├ Nauczone słowa: {count}",
    "rating_streak": "├ Seria: {count} dni",
    "rating_avg_result": "└ Średni wynik: {percent}%",
    "rating_goal": "🎯 Do #{rank} ({name}): jeszcze {diff} punktów",
    "rating_scoring_title": "💡 <b>Jak zdobyć punkty:</b>",
    "rating_scoring_quiz": "• Ukończony quiz → +10",
    "rating_scoring_reverse": "• Tryb «Odwrotny» → +5",
    "rating_scoring_word": "• Nauczone słowo → +2",
    "rating_scoring_streak": "• Dzień z rzędu → +3",
    "rating_scoring_bonus": "• Celność 90%+ → +50 bonus",
    "rating_scoring_report": "• Potwierdzone zgłoszenie → +1",

    "rating_title_alltime": "🏆 <b>Moja pozycja — Za cały czas</b>",
    "rating_position_alltime": "📍 Pozycja: <b>#{rank}</b>",
    "rating_position_none": "📍 Pozycja: <b>—</b>",
    "rating_achievements": "⭐ <b>Twoje osiągnięcia:</b>",
    "rating_wins": "├ Zwycięstwa (1. miejsce): {count}",
    "rating_total_words": "└ Nauczone słowa: {count}",
    "rating_motivation_start": "🚀 Zacznij uczyć się słów — pierwszy krok jest najważniejszy!",
    "rating_motivation_continue": "🎯 Tak dalej — pierwsze zwycięstwo blisko!",
    "rating_motivation_champion": "🔥 Jesteś prawdziwym mistrzem!",
    "rating_lifetime_title": "🌟 <b>Punkty Lifetime — to:</b>",
    "rating_lifetime_desc": "• Wszystkie punkty ze wszystkich miesięcy\n• +100 za 🥇 · +50 za 🥈 · +25 za 🥉",

    "table_title_monthly": "📊 <b>Tabela liderów — {month} {year}</b>",
    "table_title_alltime": "📊 <b>Tabela liderów — Za cały czas</b>",
    "table_empty": "Na razie nikt nie bierze udziału.\nZrób quiz pierwszy! 💪",
    "table_you_in_top": "📍 Ty: <b>#{rank}</b> z {total}",
    "table_you_not_in_top": "📍 Ty: <b>#{rank}</b> z {total} — {score} punktów",
    "table_you_outside": "📍 Ty: poza top 10 — {score} punktów",
    "table_you_not_ranked": "📍 Nie jesteś jeszcze w rankingu",
    "table_points": "punktów",
    "btn_leaderboard_table": "📊 Tabela liderów",
    "btn_back_to_rating": "◀️ Wróć do pozycji",

    # ============================================================================
    # STATYSTYKI (NOWE)
    # ============================================================================
    "stats_header": "📊 <b>Twoje statystyki</b>",
    "stats_learned_of": "└─ Nauczone <b>{learned}</b> z {total}",
    "stats_details": "⏳ W toku: {progress}\n🆕 Nowe: {new}\n⚠️ Trudne: {difficult}",
    "stats_achievements_title": "<b>Twoje osiągnięcia</b>",
    "stats_words_count": "├─ Nauczone słowa: <b>{count}</b>",
    "stats_streak_line": "└─ Seria: <b>{days} dni z rzędu</b>",
    "stats_quizzes_header": "<b>Quizy · {level}</b>",
    "stats_quizzes_passed_line": "├─ Ukończone: <b>{count}</b>",
    "stats_quizzes_avg_line": "├─ Średni wynik: <b>{percent}%</b>",
    "stats_quizzes_best_line": "└─ Najlepszy wynik: <b>{percent}%</b>",
    "stats_quizzes_empty": "└─ Na razie brak ukończonych quizów",
    "stats_recent_header": "📈 <b>Ostatnie quizy</b>",
    "stats_overall_header": "🌍 <b>Postęp ogólny</b>",
    "stats_overall_learned": "└─ Nauczone <b>{learned}</b> z {total} słów",
    "stats_cta_start": "💪 Zacznij uczyć się słów — pierwszy krok jest najważniejszy!",
    "stats_cta_begin": "🚀 Świetny początek! Tak dalej!",
    "stats_cta_halfway": "🔥 Jesteś w połowie drogi! Nie zatrzymuj się!",
    "stats_cta_almost": "🏆 Prawie u celu! Dobra robota!",
    "stats_explanation": "—————————————————————\nSłowo nauczone = 3 dobre odpowiedzi z rzędu",
    "stats_btn_rating": "🏆 Moja pozycja",
}

# ============================================================================
# WIELOJĘZYCZNOŚĆ: język nauki, język znaczeń i kierunek
# ============================================================================
TEXTS.update({
    # Nazwy języków
    "langname_de": "🇩🇪 Niemiecki",
    "langname_en": "🇬🇧 Angielski",
    "langname_ru": "🏴 Rosyjski",
    "langname_uk": "🇺🇦 Ukraiński",
    "langname_tr": "🇹🇷 Turecki",
    "langname_pl": "🇵🇱 Polski",
    # Spójnik do wyliczania języków w pomocy i powitaniu
    "and_word": "i",

    # Wiersze w menu ustawień
    "settings_learning_lang_line": "🎯 Uczę się: <b>{language}</b>",

    "settings_btn_learning_lang": "🎯 Jakiego języka się uczyć",

    # Ekran «jakiego języka się uczyć»
    "learning_lang_title": "🎯 <b>Jakiego języka się uczyć</b>",
    "learning_lang_description": "Wybierz język, którego słów będziesz się uczyć.\nPostępy liczą się osobno dla każdego języka.",
    "learning_lang_set": "✅ Uczymy się: {language}",
    # Wiersz w menu ustawień i ekran «Wymowa»
    "settings_audio_line": "🔊 Wymowa: <b>{state}</b>",
    "settings_btn_audio": "🔊 Wymowa",
    "audio_state_on": "włączona",
    "audio_state_off": "wyłączona",

    "audio_title": "🔊 <b>Wymowa</b>",
    "audio_description": "Słowo wybrzmiewa głosem native speakera. W pytaniu samo słowo, po odpowiedzi — słowo razem z przykładem.",
    "audio_current_voice": "🎙 Głos: <b>{voice}</b>",
    "audio_btn_turn_on": "🔊 Włącz wymowę",
    "audio_btn_turn_off": "🔇 Wyłącz wymowę",
    "audio_btn_choose_voice": "🎙 Wybierz głos",
    "audio_turned_on": "✅ Wymowa włączona",
    "audio_turned_off": "🔇 Wymowa wyłączona",

    "voice_title": "🎙 <b>Wybór głosu</b>",
    "voice_description": "Naciśnij głos, żeby go posłuchać. Haczyk oznacza wybrany.",
    "voice_male": "Męskie",
    "voice_female": "Żeńskie",
    "voice_set": "✅ Głos: {voice}",
    "voice_only_one": "Dla tego języka syntezator ma jeden głos męski i jeden żeński — więcej nie istnieje.",
    "voice_preview_failed": "Nie udało się pobrać próbki, spróbuj jeszcze raz",
})


# ============================================================================
# АПГРЕЙД ПОД ШЕСТЬ ЯЗЫКОВ
#
# Добавлено, когда бот перестал быть «ботом для немецкого»: при первом запуске
# человек теперь выбирает не только язык интерфейса, но и какой язык учить, а
# подсказки направления стали работать на все тридцать пар вместо восьми.
# ============================================================================
TEXTS.update({
    "btn_rating": "🏆 Ranking",
    "friend_fallback": "przyjacielu",
    "onboarding_learning_title": "🎯 <b>Jakiego języka będziesz się uczyć?</b>",
    "onboarding_learning_desc": "Znaczenia będą pokazywane w języku: {native}\nJęzyk i kierunek zmienisz w ustawieniach w każdej chwili.",
    "mode_hint_forward": "💡 {learning} → {native} jest łatwiejszy: znaczenie podpowiada kontekst",
    "mode_hint_reverse": "💡 {native} → {learning} jest trudniejszy: lepiej utrwala słowa",
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
    "help_how_to_use_text": "🎮 <b>Quiz</b>\n25 słów, cztery warianty. Bot zapamiętuje błędy i częściej wraca do trudnych słów. Po quizie można od razu powtórzyć to, w czym się pomyliłeś.\n\n🔊 <b>Wymowa</b>\nW pytaniu brzmi słowo, po odpowiedzi — słowo razem z przykładem. Głos wybierzesz w ustawieniach, męski albo żeński.\n\n🌍 <b>Języki</b>\n{languages} — w każdej parze i w obie strony. Postępy i ranking liczą się osobno dla każdego języka.\n\n━━━━━━━━━━━━━━━━━\n💡 Słowo jest <b>opanowane</b> po trzech poprawnych odpowiedziach z rzędu, w różne dni.\n🔥 <b>Seria</b> rośnie za każdy quiz w danym dniu.\n📝 Błąd w tłumaczeniu lub wymowie — przycisk pod quizem.",
    "help_community_title": "💬 <b>O bocie i społeczności</b>",
    "help_community_text": "🤖 <b>GenauLingua</b> — {language_count} języków w każdej parze: {languages}\n12 900 słów A1–C2, każde z przykładem i wymową native speakera.\nInterfejs: {interface_languages}\n\n💬 <b>t.me/genaulingua_chat</b>\nBłędy, pomyłki w tłumaczeniu, pomysły — czytamy wszystko. Zgłoszenia o wymowie są szczególnie cenne: maszyna nie słyszy akcentu.",
})


# ============================================================================
# ВОПРОС НА СЛУХ
#
# Самого слова на экране нет — иначе слушать незачем. Варианты стоят на
# ИЗУЧАЕМОМ языке: спрашивают «что услышал», а не «что это значит».
# ============================================================================
TEXTS.update({
    "quiz_question_listen": "🔊 Posłuchaj i wybierz, co usłyszałeś:",
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
    "rating_scoring_answer": "• Poprawna odpowiedź → +1, ze słuchu → +2, na głos → +3",
    "rating_scoring_quiz": "• Ukończona runda → +10",
    "rating_scoring_reverse": "• Kierunek odwrotny → +5",
    "rating_scoring_word": "• Opanowane słowo → +3",
    "rating_scoring_streak": "• Każdy kolejny dzień wart więcej, do +10",
    "rating_scoring_bonus": "• Celność powyżej 60% — im wyżej, tym więcej",
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
    "voice_not_ready_hint": "<i>· przy głosie oznacza, że nie jest jeszcze w całości nagrany: słowo powstaje na żywo, czasem z opóźnieniem lub bez dźwięku</i>",
})


# ============================================================================
# ИТОГ КРУГА: сколько вопросов было на слух
#
# Иначе новая игра растворяется в общем списке, и человек не замечает, что
# уже узнаёт слова ушами. Строка показывается, только если такие вопросы
# были.
# ============================================================================
TEXTS.update({
    "quiz_result_by_ear": "🎧 Ze słuchu: {count}",
})


# ============================================================================
# СОСТАВ ЗАНЯТИЯ
#
# Три канала — три РАЗНЫХ навыка, а не три оформления одного. Экран нужен,
# потому что до него колонка quiz_channels была недостижима: выключить
# вопросы на слух можно было только выключив озвучку целиком.
# ============================================================================
TEXTS.update({
    "settings_btn_channels": "🎮 Skład zajęć",
    "settings_channels_line": "🎮 Zajęcia: <b>{channels}</b>",
    "channels_title": "🎮 <b>Skład zajęć</b>",
    "channels_description": "Jakie pytania zadawać. Im więcej kanałów, tym trwalej zapada słowo: rozpoznać je wzrokiem, ze słuchu i wypowiedzieć to trzy różne umiejętności.",
    "channel_text": "🔤 Karta",
    "channel_audio": "🎧 Ze słuchu",
    "channel_speech": "🎤 Mowa",
    "channels_text_always": "🔤 Karty się nie wyłączają: zajęcia bez żadnego kanału to pusty ekran.",
    "channels_audio_blocked": "🎧 Ze słuchu niedostępne: wymowa jest wyłączona.",
    "channels_speech_soon": "🎤 Mowa pojawi się wkrótce.",
    "channels_need_one": "Musi zostać co najmniej jeden kanał",
})


# ============================================================================
# ВОПРОС ВСЛУХ
#
# Ответ приходит голосовым сообщением, а не нажатием. Распознаватель отвечает
# на вопрос «то ли слово сказано», и только на него: качество произношения он
# судить не умеет — он обучен ПОНИМАТЬ акцент, а не замечать его.
# ============================================================================
TEXTS.update({
    "quiz_question_speak": "🎤 Wypowiedz to słowo na głos — nagraj wiadomość głosową",
    "speech_btn_reference": "🔊 Posłuchaj",
    "speech_btn_skip": "⏭ Pomiń",
    "speech_listening": "🎧 Słucham…",
    "speech_heard": "Usłyszałem: <i>{heard}</i>",
    "speech_not_understood": "🤔 Nie zrozumiałem. Nagraj jeszcze raz — bliżej mikrofonu i trochę głośniej.",
    "speech_send_voice": "🎤 Na to pytanie odpowiada się wiadomością głosową. Naciśnij i przytrzymaj przycisk mikrofonu.",
    "speech_skipped": "⏭ Pominięto",
    "quiz_result_spoken": "🎤 Na głos: {count}",
})


# ============================================================================
# ДОМАШНИЙ ЭКРАН: ТРИ ШКАЛЫ
# ============================================================================
TEXTS.update({
    "home_scale_text": "Napisane",
    "home_scale_audio": "Na słuch",
    "home_scale_speech": "Na głos",
    "home_btn_learn": "▶️ Ucz się · {count}",
    "home_streak": "🔥 seria: {days}",
    "home_rank": "🏆 miejsce: {rank}",
    "home_hint": "Pasek to udział słów, które już spotkałeś: trzy poprawne odpowiedzi danym kanałem i słowo liczy się na jego konto. Różnica między skalami pokazuje, czego brakuje.",
    "home_channel_not_ready": "{channel}: jeszcze za wcześnie. Gotowych słów jest {ready}, potrzeba co najmniej {minimum}. Poucz się kartami — otwierają pozostałe kanały.",
})


# ============================================================================
# НАСТРОЙКИ: ТРИ ГРУППЫ
#
# «Что учу» человек меняет часто, «как мне удобно» ставит один раз. Восемь
# равных пунктов перемешивали то и другое, и первым в списке стоял режим
# викторины, которым не пользуются 96%.
# ============================================================================
TEXTS.update({
    "settings_group_what": "🎯 Czego się uczę",
    "settings_group_what_title": "<b>🎯 Czego się uczę</b>",
    "settings_group_how": "🎮 Jak się uczę",
    "settings_group_how_title": "<b>🎮 Jak się uczę</b>",
    "settings_group_bot": "🔧 Bot",
    "settings_group_bot_title": "<b>🔧 Bot</b>",
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
    "quiz_btn_one_more": "▶️ Jeszcze jedna runda",
    "home_btn_stats": "📊 Szczegóły",
    "notif_off_how_to_return": "Włączyć ponownie: ⚙️ Ustawienia → 🔧 Bot → 🔔 Przypomnienia",
    "reminder_offer": "🔔 Przypominać raz na dzień? Łatwiej nie zgubić tego, czego się nauczyłeś — i seria się nie urywa.",
    "reminder_offer_yes": "🔔 Tak, przypominaj",
    "reminder_offer_no": "Nie trzeba",
    "reminder_offer_done": "🔔 Gotowe. Godzinę i dni zmienisz w ustawieniach.",
    "level_offer": "📈 Na poziomie <b>{current}</b> prawie się nie mylisz. Przejść na <b>{following}</b>? Wszystko, czego się nauczyłeś, zostaje.",
    "level_offer_yes": "📈 Tak, przejdź na {following}",
    "level_offer_no": "Zostaję",
    "level_offer_done": "📈 Poziom <b>{following}</b>. Słowa będą trudniejsze.",
})


# ============================================================================
# ЗАЧЕМ УЧИШЬ — ОПРОС, ВСТРОЕННЫЙ В ПЕРВОЕ НАЖАТИЕ
#
# Режим «по категории» работает, и им пользуются ТРИ человека из 233:
# он спрятан третьим уровнем настроек. Каждая кнопка здесь И отвечает
# на вопрос, И начинает первый круг — шага не прибавилось.
# ============================================================================
TEXTS.update({
    "goal_question": "Do czego potrzebujesz języka? Dobierzemy słowa pod odpowiedź.",
    "goal_work": "💼 Do pracy",
    "goal_travel": "✈️ Na podróże",
    "goal_living": "🏠 Do życia za granicą",
    "goal_study": "🎓 Do nauki",
    "goal_any": "📚 Po prostu uczyć się słów",
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
    "intro_title": "🌍 <b>GenauLingua</b>",
    "intro_three_games": "Słowo to trzy różne umiejętności, nie jedna:\n🔤 rozpoznać zapisane\n🎧 rozpoznać ze słuchu\n🎤 wypowiedzieć na głos\n\nW nauce zmieniają się same — zależnie od tego, jak dobrze znasz każde słowo.",
    "intro_numbers": "12 902 słowa · 20 tematów · 6 poziomów\nSześć języków w dowolnej parze: ucz się polskiego przez angielski, jeśli chcesz.",
    "intro_where_you_are": "Teraz: <b>{language}</b> · {mode}",
    "intro_btn_progress": "📊 Postępy",
    "settings_title_short": "🦾 Ustawienia",
})


# ============================================================================
# ЗАЧЕМ УЧУ — ЭКРАН НАСТРОЙКИ
#
# Без него цель осталась бы пустой навсегда у всех 233 нынешних
# пользователей: онбординг у них давно позади. Та же дыра, что была у
# состава занятия — колонка есть, экрана нет.
# ============================================================================
TEXTS.update({
    "settings_btn_goal": "🧭 Po co się uczę",
    "settings_goal_title": "🧭 <b>Po co się uczę</b>",
    "settings_goal_description": "Słowa z twojego tematu będą przychodzić pierwsze. Trudność nadal zależy od poziomu, a to, czego się nauczyłeś, wraca do powtórek.",
    "settings_goal_set": "Cel zapisany",
    "settings_goal_line": "🧭 Cel: <b>{goal}</b>",
    "settings_goal_none": "nie wybrano",
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
    "match_title": "🧩 <b>Znajdź pary</b>",
    "match_progress": "Dopasowano: {matched} z {total}",
    "match_errors": "❌ pomyłki: {count}",
    "match_hint": "Naciśnij słowo z dowolnej strony, potem jego parę z drugiej.",
    "match_wrong": "❌ Nie para",
    "match_done": "🧩 <b>Plansza ukończona!</b>",
    "match_done_counted": "Do postępu zaliczono {counted} z {total}: tylko pary dopasowane za pierwszym razem i nigdy ostatnia — przy niej nie ma już wyboru.",
    "match_btn_again": "🧩 Jeszcze jedna plansza",
    "match_not_ready": "🧩 Jeszcze za wcześnie: plansza potrzebuje {need} znanych słów, a masz {have}. Poucz się kartami — one ją otworzą.",
    "home_btn_match": "🧩 Znajdź pary",
})

TEXTS["match_back_to_round"] = "Wracamy do rundy."

TEXTS.update({
    "settings_btn_match": "🧩 Plansza w rundzie",
    "settings_match_title": "🧩 <b>Plansza w rundzie</b>",
    "settings_match_description": "Co drugą naukę w środku rundy zamiast pięciu pytań przychodzi plansza: pięć słów i pięć znaczeń, trzeba znaleźć pary. Brane są tylko znane słowa.",
    "match_state_on": "Plansza włączona: przyjdzie w środku rundy.",
    "match_state_off": "Plansza wyłączona: runda to same pytania.",
})
