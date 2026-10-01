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
    "welcome_description": "🌍 <b>GenauLingua</b> — ucz się języka przez grę\nJęzyki do wyboru: {languages}\n12 000+ słów · 20 tematów · 6 poziomów\n\nBot dobiera słowa pod ciebie — im więcej\ngrasz, tym trafniejszy dobór",
    "welcome_separator": "──────────────────",

    "welcome_learn_words_title": "📚 <b>Ucz się słów</b>",
    "welcome_learn_words_desc": "Start quizu",

    "welcome_stats_title": "📊 <b>Statystyki</b>",
    "welcome_stats_desc": "Twoje postępy",

    "welcome_settings_title": "🦾 <b>Ustawienia</b>",
    "welcome_settings_desc": "Tryb, język, tematy",

    "welcome_help_title": "❓ <b>Pomoc</b>",
    "welcome_help_desc": "Instrukcja i kontakt",

    "welcome_your_level": "Twój poziom: <b>{level}</b>\nTryb: <b>{mode}</b>",
    "welcome_call_to_action": "Naciśnij 📚 Ucz się słów — i zaczynamy!",

    "welcome_choose_level": "🎯 <b>Od czego zaczniemy?</b>\n\nWybierz swój poziom\n\n• A1–A2 — podstawowe słownictwo\n• B1–B2 — swobodna rozmowa\n• C1–C2 — biegła znajomość",
    "choose_level_prompt": "Wybierz poziom:",

    "level_selected": "✅ Poziom <b>{level}</b> wybrany.\n\nNaciśnij 📚 Ucz się słów — i zaczynamy!",
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

    "notif_message_title": "{emoji} <b>Czas na naukę!</b>",
    "notif_message_streak": "🔥 Seria: {days} dni z rzędu",
    "notif_message_words": "📊 Nauczone słowa: {count}",
    "notif_message_cta": "💪 Nie przerywaj swojej serii!",
    "notif_message_btn_start": "📚 Zacznij quiz",
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
    "notif_message_progress_title": "📊 <b>Twoje postępy:</b>",
    "notif_progress_streak": "├ Seria: {days} dni 🎯",
    "notif_progress_quizzes": "├ Ukończone quizy: {count}",
    "notif_progress_words": "├ Nauczone słowa: {count}",
    "notif_progress_accuracy": "└ Celność: {percent}%",

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
    "settings_mode_hint_de_ru": "💡 DE→RU легче — можно угадать по логике",
    "settings_mode_hint_ru_de": "💡 RU→DE сложнее — лучше закрепляет слова",
    "settings_mode_hint_de_uk": "💡 DE→UK легше — можна вгадати за логікою",
    "settings_mode_hint_uk_de": "💡 UK→DE складніше — краще закріплює слова",
    "settings_mode_hint_de_en": "💡 DE→EN easier — you can guess from context",
    "settings_mode_hint_en_de": "💡 EN→DE harder — better memorization",
    "settings_mode_hint_de_tr": "💡 DE→TR daha kolay — mantıkla tahmin edebilirsiniz",
    "settings_mode_hint_tr_de": "💡 TR→DE daha zor — kelimeleri daha iyi pekiştirir",

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
    "report_sent": "✅ Wysłano {count} zgłoszeń — dziękujemy!\nJeśli błąd się potwierdzi, dostaniesz +1 punkt",
    "report_daily_limit": "⚠️ Dzienny limit zgłoszeń wyczerpany (maks. 20)",
    "report_all_reported": "✅ Wszystkie słowa z tego quizu są już zgłoszone",
    "report_already_sent": "✔️ Już wysłane wcześniej",
    "report_kind_title": "Co konkretnie jest nie tak?",
    "report_btn_kind_text": "📝 Błędne tłumaczenie",
    "report_btn_kind_audio": "🔊 Błędna wymowa",
    "report_sent_audio": "✅ Wysłano {count} — dziękujemy!\nZgłoszenia wymowy są szczególnie cenne: sprawdzanie maszynowe nie słyszy akcentu",

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
    "help_btn_roadmap": "🚀 Wkrótce w bocie",
    "help_btn_community": "💬 Społeczność",
    "help_btn_about": "ℹ️ O bocie",

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

    "help_roadmap_title": "🚀 <b>Wkrótce w GenauLingua</b>",
    "help_roadmap_text": """🏆 <b>Osiągnięcia</b>
Odznaki za postępy — pierwszy quiz, 7 dni z rzędu, 100 nauczonych słów, quiz na 100% i inne.

🎓 <b>Przygotowanie do egzaminów</b>
Tryby przygotowania do egzaminów Goethe/ÖSD A2–B2. Trening słownictwa, które pojawia się na egzaminach.

📖 <b>Praca z tekstami</b>
Czytanie i omawianie tekstów niemieckich z tłumaczeniem, nowymi słowami i zadaniami.

📝 <b>Gramatyka</b>
Interaktywne ćwiczenia z gramatyki — rodzajniki, przypadki, czasy, szyk zdania.

━━━━━━━━━━━━━━━━━
💬 Pomysły i życzenia — pisz na czat:
t.me/genaulingua_chat""",

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

    "help_about_title": "ℹ️ <b>O bocie</b>",
    "help_about_text": """🤖 <b>GenauLingua</b> — osobisty pomocnik w nauce słówek.

✨ <b>Co potrafi:</b>
• Baza słów A1–C2 (12 000+ słów na każdy język)
• 20 kategorii tematycznych
• 4 tryby quizu: po poziomie, po kategorii, top 10K, trudne słowa
• Trafny dobór słów — algorytm SRS
• {language_count} języków do wyboru: {languages} —
  w każdej parze i w obie strony
• Wymowa wszystkich słów i przykładów głosami native speakerów
• Powtórka błędów po quizie
• Zgłoszenie błędu w tłumaczeniu wprost z quizu
• Statystyki, seria i pasek postępu
• Ranking miesięczny i tabela liderów — osobno dla każdego języka
• Przypomnienia z elastycznym harmonogramem
• Interfejs: {interface_languages}

💬 Śledź nowości: t.me/genaulingua_chat""",

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
