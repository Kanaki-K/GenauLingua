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
    "btn_learn_words": "Nauka słów",
    "btn_stats": "Statystyki",
    "btn_settings": "Ustawienia",
    "btn_help": "Pomoc",
    "btn_back": "Wróć",
    "menu_placeholder": "Proszę wybrać działanie...",

    # ============================================================================
    # POWITANIE I START
    # ============================================================================
    "welcome_title": "<b>Witamy, {name}!</b>",








    # ============================================================================
    # PRZYPOMNIENIA
    # ============================================================================
    "notif_title": "<b>Przypomnienia</b>",
    "notif_status": "Stan: {status}",
    "notif_status_on": "Włączone",
    "notif_status_off": "Wyłączone",
    "notif_time": "Godzina: {time}",
    "notif_days": "Dni: {days}",
    "notif_timezone": "Strefa czasowa: {timezone}",
    "notif_hint": "Przypomnienia przyjdą o podanej godzinie według wybranej strefy czasowej.",
    "notif_hint_off": "Warto włączyć przypomnienia — łatwiej nie przerwać serii.",

    "notif_btn_toggle_on": "Przypomnienia: Włączone",
    "notif_btn_toggle_off": "Przypomnienia: Wyłączone",
    "notif_btn_time": "Godzina: {time}",
    "notif_btn_days": "Wybór dni",
    "notif_btn_timezone": "Zmiana strefy czasowej",

    "notif_timezone_title": "<b>Proszę wybrać strefę czasową</b>",
    "notif_timezone_current": "Obecnie: {timezone}",
    "notif_timezone_prompt": "Proszę wybrać miasto z tej samej strefy czasowej:",
    "notif_timezone_more": "Inne miasto",
    "notif_timezone_back": "Wróć",
    "notif_timezone_set": "✓ Strefa czasowa ustawiona: {city}",

    "notif_time_title": "<b>Proszę wybrać godzinę przypomnienia</b>",
    "notif_time_current": "Obecna godzina: {time}",
    "notif_time_timezone": "Strefa czasowa: {timezone}",
    "notif_time_hint": "Przypomnienie będzie przychodzić codziennie o wybranej godzinie.",
    "notif_time_set": "✓ Godzina ustawiona: {time}",

    "notif_days_title": "<b>Proszę wybrać dni przypomnień</b>",
    "notif_days_hint": "Proszę nacisnąć dzień, żeby go włączyć lub wyłączyć.\n✓ — dzień włączony\n✗ — dzień wyłączony\n\nNa koniec proszę nacisnąć «Zapisz».",
    "notif_days_all": "Wszystkie dni",
    "notif_days_weekdays": "Dni powszednie (pn–pt)",
    "notif_days_save": "Zapisz",
    "notif_days_saved": "✓ Dni zapisane!",
    "notif_days_all_selected": "✓ Wybrano wszystkie dni",
    "notif_days_weekdays_selected": "✓ Wybrano dni powszednie (pn–pt)",
    "notif_days_none": "Proszę wybrać przynajmniej jeden dzień przypomnień!",

    "notif_toggle_on": "Przypomnienia włączone!",
    "notif_toggle_off": "Przypomnienia wyłączone",

    "notif_message_btn_disable": "Wyłączyć przypomnienia",

    "day_mon": "Pn",
    "day_tue": "Wt",
    "day_wed": "Śr",
    "day_thu": "Cz",
    "day_fri": "Pt",
    "day_sat": "So",
    "day_sun": "Nd",

    "notif_btn_back": "Wróć do ustawień",

    "notif_default_name": "przyjacielu",

    "anchor_streak": "🔥 {days}",
    "notif_message_greeting": "<b>Czas na naukę, {name}!</b>",


    # JEDEN POWÓD, BY WRÓCIĆ — i musi być prawdziwy
    "remind_streak_risk": "{days} dni z rzędu · dziś jeszcze nie",
    "remind_due": "Słowa czekają na powtórkę: {count} — terminy bot liczy sam",
    "remind_due_many": "Do powtórki zebrało się wiele. Najlepiej zacząć od jednej rundy, a resztę odłożyć.",
    "remind_streak_lost": "Najlepsza seria to {days} dni. Nowa zaczyna się od jednej rundy.",
    "remind_milestone_close": "Słów w pracy: {count} · do {target} jeszcze {left}, to jedna runda",
    "remind_almost_learned": "Jedna poprawna odpowiedź do pierwszego nauczonego słowa. Takich słów: {count}",
    "remind_rank": "Miejsce {rank} z {total} w rankingu tego języka",
    "remind_fact_1": "Słowo zostaje, gdy wraca: dzień, trzy dni, tydzień. Terminy pilnuje bot.",
    "remind_fact_2": "Odpowiedź ze słuchu liczy się więcej: nie ma zapisu, na którym można się oprzeć.",
    "remind_fact_3": "Powiedzieć na głos jest trudniej niż rozpoznać — i warte trzy razy tyle.",
    "remind_fact_4": "Piętnaście słów to cztery minuty. Krócej niż kolejka po kawę.",

    # ============================================================================
    # USTAWIENIA
    # ============================================================================
    "settings_title": "<b>Ustawienia</b>",
    "settings_mode": "Kierunek: <b>{mode}</b>",
    "settings_language": "Język bota: <b>{language}</b>",

    "settings_btn_quiz_mode": "Poziom i tematy",
    "settings_btn_change_language": "Język interfejsu",
    "settings_btn_notifications": "Przypomnienia",

    "settings_quiz_mode_line": "Poziom: <b>{mode}</b>",


    "settings_language_title": "<b>Język interfejsu</b>",
    "settings_language_description": "Proszę wybrać język interfejsu bota:",
    "start_pick_language": "Proszę wybrać język",

    "language_changed": "✓ Język zmieniony na {language}",
    "user_not_found": "✗ Nie znaleziono użytkownika. Proszę użyć /start",

    # Nazwy języków interfejsu — każda w swoim języku
    "lang_ru": "Русский",
    "lang_uk": "Українська",
    "lang_en": "English",
    "lang_tr": "Türkçe",
    "lang_de": "Deutsch",
    "lang_pl": "Polski",

    # Kierunki tłumaczenia

    # ============================================================================
    # TRYB QUIZU
    # ============================================================================
    "qmode_title": "<b>Poziom i tematy</b>",
    "qmode_current": "Teraz: <b>{mode}</b>",
    "qmode_choose": "Proszę wybrać sposób nauki słów\nMożna go zmienić w każdej chwili — postępy zostają",

    "qmode_btn_level": "Po poziomie",
    "qmode_btn_category": "Kategoria",
    "qmode_btn_all": "Top 10 tysięcy",
    "qmode_btn_difficult": "Trudne",

    "qmode_level_short": "{level}",
    "qmode_category_short": "{category}",
    "qmode_all_short": "Top 10 tysięcy",
    "qmode_difficult_short": "Trudne słowa",

    "qmode_level_title": "<b>Wybór poziomu</b>",
    "qmode_level_desc": "Od pierwszych słów do swobodnych dyskusji. Wszystkie poziomy są otwarte — proszę wybrać odpowiedni.\n\n• A1–A2 — podstawowe słownictwo\n• B1–B2 — swobodna rozmowa\n• C1–C2 — biegła znajomość",
    "qmode_level_set": "✓ Tryb: Po poziomie ({level})",

    "qmode_category_title": "<b>Wybór kategorii</b>",
    "qmode_category_desc": "Od jedzenia do nauki — proszę wybrać potrzebny temat\n\nKażda kategoria zawiera słowa ze wszystkich poziomów",
    "qmode_category_set": "✓ Tryb: {category}",

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

    "qmode_all_set": "✓ Tryb: Top 10 tysięcy",

    "qmode_difficult_set": "✓ Tryb: Trudne słowa",
    "qmode_difficult_few": "Trudnych słów na razie: {count} — potrzeba co najmniej 4.\nWarto zagrać jeszcze kilka rund!",
    "qmode_difficult_empty": "Na razie brak trudnych słów.\nWarto zagrać kilka rund!",

    "quiz_btn_change_mode": "Poziom i tematy",
    "quiz_btn_report_error": "Zgłosić błąd",
    "report_btn_confirm": "✓ Potwierdzam ({count})",
    "report_btn_send": "Wyślij",
    "report_no_words": "Brak słów do zgłoszenia",
    "report_none_selected": "Proszę wybrać przynajmniej jedno słowo",
    "report_pick_kind": "Wybrano słów: {count}. Teraz proszę wskazać, co jest nie tak — tłumaczenie czy wymowa.",
    "report_sent": "✓ Wysłane zgłoszenia: {count} — dziękujemy!\nJeśli błąd się potwierdzi, przyznamy +{points}",
    "report_daily_limit": "Dzienny limit zgłoszeń wyczerpany (maks. 20)",
    "report_all_reported": "✓ Wszystkie słowa z tego quizu są już zgłoszone",
    "report_already_sent": "✓ Już wysłane wcześniej",
    "report_btn_kind_text": "Błędne tłumaczenie",
    "report_btn_kind_audio": "Błędna wymowa",
    "report_sent_audio": "✓ Wysłano {count} — dziękujemy!\nZgłoszenia wymowy są szczególnie cenne: sprawdzanie maszynowe nie słyszy akcentu\nJeśli się potwierdzi — +{points}",
    "report_approved": "✓ Zgłoszenie dotyczące <b>{word}</b> zostało przyjęte — poprawimy tłumaczenie.\n+{points} punktów do wyniku miesiąca — dziękujemy, słownik będzie lepszy dla wszystkich.",
    "award_won": "{mark} Miejsce {rank} w klasyfikacji za {month}.\nDo stałego wyniku dodano {bonus}.",
    "report_approved_audio": "✓ Zgłoszenie wymowy przyjęte: <b>{word}</b>.\nNagranie powstanie na nowo. +{points} punktów do wyniku miesiąca — dziękujemy.",
    "report_approved_capped": "✓ Zgłoszenie dotyczące <b>{word}</b> zostało przyjęte — dziękujemy, słownik będzie lepszy dla wszystkich.\nPunkty za zgłoszenia w tym miesiącu już zdobyte: płacimy za {limit} w miesiącu.",

    # ============================================================================
    # QUIZ
    # ============================================================================
    "quiz_no_level": "Najpierw proszę wybrać poziom poleceniem /start",
    "quiz_error_generation": "✗ Przy przygotowaniu quizu wystąpił błąd.\nProszę spróbować jeszcze raz przez /start",
    "quiz_no_words": "✗ Niestety dla tego poziomu nie ma jeszcze słów.\nProszę wybrać inny poziom.",

    "quiz_question_number": "{current} / {total}",

    "quiz_correct": "✓ <b>Dobrze</b>",
    "quiz_wrong": "✗ <b>Źle</b>",
    "quiz_correct_answer": "Prawidłowa odpowiedź:",

    "quiz_btn_next": "Dalej →",
    "quiz_btn_repeat_errors": "Powtórka błędów",

    "quiz_completed": "<b>Runda ukończona</b>",
    "quiz_result_correct": "Poprawnie: <b>{correct}/{total}</b>",
    "quiz_result_percentage": "Wynik: <b>{percentage}%</b>",
    "quiz_result_details": "<b>Szczegóły:</b>",
    "quiz_result_errors": "Błędów: {count}",

    # POCHWAŁA NA KONIEC RUNDY — tylko za to, co się stało
    "praise_first_round": "Pierwsza runda ukończona. Dalej słowa zaczną wracać — tak się je pamięta.",
    "praise_first_learned": "Pierwsze słowo nauczone: trzy poprawne odpowiedzi z rzędu i poznane nie dziś.",
    "praise_learned": "Nauczone słowa w tej rundzie: {count}",
    "praise_best_streak": "Rekord osobisty: {days} dni z rzędu",
    "praise_milestone": "Próg {count} osiągnięty",
    "praise_first_speech": "Pierwsza poprawna odpowiedź głosem",
    "praise_first_audio": "Pierwsza poprawna odpowiedź ze słuchu",
    "praise_comeback": "Witamy z powrotem. Przerwa trwała {days} dni.",
    "praise_perfect": "Runda bez błędu",
    "praise_streak": "Seria: {days} dni z rzędu",
    "praise_new_words": "Nowe słowa: {count}",
    "praise_returned": "Rozpoznane ponownie: {count}",
    "praise_progress": "Słów w pracy: {count} · do {target} jeszcze {left}",
    "praise_progress_top": "Słów w pracy: {count}",
    "praise_points": "Punkty: +{points}",

    "quiz_repeat_title": "<b>Powtórka błędów</b>",
    "quiz_no_errors": "✓ Runda bez żadnych błędów!",
    "quiz_error_next": "✗ Nie udało się wczytać następnego pytania.",
    "quiz_error_generate": "✗ Nie udało się utworzyć następnego pytania.",

    # ============================================================================
    # STATYSTYKI
    # ============================================================================
    "stats_no_level": "<b>Najpierw proszę wybrać poziom!</b>\n\nAby zacząć, proszę użyć polecenia /start.",





    # ============================================================================
    # POMOC
    # ============================================================================
    "help_title": "<b>Pomoc — GenauLingua</b>",
    "help_description": "Tutaj: jak działają lekcje i jak skontaktować się ze społecznością.",
    "help_choose": "Proszę wybrać dział:",

    "help_btn_how_to_use": "Jak korzystać",
    "help_btn_community": "Społeczność",

    "help_how_to_use_title": "<b>Jak korzystać z bota</b>",


    "help_community_title": "<b>Społeczność GenauLingua</b>",
    "help_community_text": """ <b>t.me/genaulingua_chat</b>

Na czacie:
Nowości — tu najwcześniej
Znaleziony błąd — można napisać albo przysłać zrzut ekranu
Błąd w tłumaczeniu — prosimy zgłaszać, poprawimy
Pomysły i życzenia — wszystko czytamy i bierzemy do pracy
Rozmowy z innymi uczącymi się


Im aktywniejsza społeczność, tym lepszy bot. Serdecznie zapraszamy! """,


    # ============================================================================
    # RANKING
    # ============================================================================
    "rating_title_monthly": "<b>Moja pozycja — {month} {year}</b>",
    "rating_not_active": "✗ Ranking nie jest jeszcze aktywny.",
    "rating_not_in_ranking": "Brak jeszcze pozycji w rankingu",
    "rating_start_quiz": "Zapraszamy do pierwszego quizu!",
    "rating_position": "Pozycja: <b>#{rank}</b> z {total}",
    "rating_points": "Punkty: <b>{score}</b>",
    "rating_title_polyglot": "poliglota",
    "rating_title_professor": "profesor",
    "rating_title_expert": "ekspert",
    "rating_title_student": "uczeń",
    "rating_your_month": "<b>Wyniki za {month}:</b>",
    "rating_quizzes": "Quizy: {count}",
    "rating_words_learned": "Nauczone słowa: {count}",
    "rating_streak": "Seria: {count} dni",
    "rating_avg_result": "Średni wynik: {percent}%",
    "rating_scoring_title": "<b>Jak zdobyć punkty:</b>",
    "rating_scoring_quiz": "• Ukończony quiz → +10",
    "rating_scoring_word": "• Nauczone słowo → +2",
    "rating_scoring_streak": "• Dzień z rzędu → +3",
    "rating_scoring_bonus": "• Celność 90%+ → +50 bonus",
    "rating_scoring_report": "• Potwierdzone zgłoszenie błędu → +{points} (do {limit} w miesiącu)",

    "rating_title_alltime": "<b>Moja pozycja — Za cały czas</b>",
    "rating_position_alltime": "Pozycja: <b>#{rank}</b>",
    "rating_position_none": "Pozycja: <b>—</b>",
    "rating_achievements": "<b>Osiągnięcia:</b>",
    "rating_wins": "Zwycięstwa (1. miejsce): {count}",
    "rating_total_words": "Nauczone słowa: {count}",
    "rating_motivation_start": "Warto zacząć naukę słów — pierwszy krok jest najważniejszy!",
    "rating_motivation_continue": "Tak dalej — pierwsze zwycięstwo blisko!",
    "rating_motivation_champion": "Prawdziwe mistrzostwo!",

    "table_title_monthly": "<b>Tabela liderów — {month} {year}</b>",
    "table_title_alltime": "<b>Tabela liderów — Za cały czas</b>",
    "table_empty": "Na razie nikt nie bierze udziału.\nPierwsze miejsce czeka!",
    "table_you_in_top": "Moje miejsce: <b>#{rank}</b> z {total}",
    "table_you_not_in_top": "Moje miejsce: <b>#{rank}</b> z {total} — {score}",
    "table_you_outside": "Moje miejsce: poza top 10 — {score}",
    "table_you_not_ranked": "Brak jeszcze pozycji w rankingu",
    "btn_leaderboard_table": "Tabela liderów",
    "btn_back_to_rating": "Wróć do pozycji",
    "rating_tab_month": "Miesiąc",
    "rating_tab_alltime": "Cały czas",

    # ============================================================================
    # STATYSTYKI (NOWE)
    # ============================================================================
    "stats_header": "<b>Statystyki</b>",
    "stats_in_work_line": "Słów w pracy: {count} · do {target} jeszcze {left}",
    "stats_in_work_top": "Słów w pracy: {count}",
    "stats_details": "W toku: {progress}\nNowe: {new}\nTrudne: {difficult}",
    "stats_achievements_title": "<b>Osiągnięcia</b>",
    "stats_words_count": "Nauczone słowa: <b>{count}</b>",
    "stats_streak_line": "Seria: {days} dni z rzędu",
    "stats_best_streak_line": "Najlepsza seria: {days} dni",
    "stats_quizzes_header": "<b>Quizy · {level}</b>",
    "stats_quizzes_passed_line": "Ukończone: <b>{count}</b>",
    "stats_quizzes_avg_line": "Średni wynik: <b>{percent}%</b>",
    "stats_quizzes_best_line": "Najlepszy wynik: <b>{percent}%</b>",
    "stats_quizzes_empty": "Na razie brak ukończonych quizów",
    "stats_recent_header": "<b>Ostatnie quizy</b>",
    "stats_overall_header": "<b>Postęp ogólny</b>",
    "stats_overall_learned": "Nauczone słowa: <b>{learned}</b> z {total}",
    "stats_explanation": "Słowo nauczone = trzy poprawne odpowiedzi z rzędu, w różne dni",
}

# ============================================================================
# WIELOJĘZYCZNOŚĆ: język nauki, język znaczeń i kierunek
# ============================================================================
TEXTS.update({
    # Nazwy języków
    "langname_de": "Niemiecki",
    "langname_en": "Angielski",
    "langname_ru": "Rosyjski",
    "langname_uk": "Ukraiński",
    "langname_tr": "Turecki",
    "langname_pl": "Polski",
    # Spójnik do wyliczania języków w pomocy i powitaniu
    "and_word": "i",

    # Wiersze w menu ustawień
    "settings_learning_lang_line": "Uczę się: <b>{language}</b>",

    "settings_btn_learning_lang": "Język",

    # Ekran «jakiego języka się uczyć»
    "learning_lang_title": "<b>Jakiego języka się uczyć</b>",
    "learning_lang_description": "Proszę wybrać język do nauki słów.\nPostępy liczą się osobno dla każdego języka.",
    "learning_lang_set": "✓ Uczymy się: {language}",
    # Wiersz w menu ustawień i ekran «Wymowa»
    "settings_audio_line": "Wymowa: <b>{state}</b>",
    "settings_btn_audio": "Wymowa",
    "audio_state_on": "włączona",
    "audio_state_off": "wyłączona",

    "audio_title": "<b>Wymowa</b>",
    "audio_description": "Słowo wybrzmiewa głosem native speakera. W pytaniu samo słowo, po odpowiedzi — słowo razem z przykładem.",
    "audio_current_voice": "Głos: <b>{voice}</b>",
    "audio_btn_turn_on": "Włączyć wymowę",
    "audio_btn_turn_off": "Wyłączyć wymowę",
    "audio_btn_choose_voice": "Wybór głosu",
    "audio_turned_on": "✓ Wymowa włączona",
    "audio_turned_off": "Wymowa wyłączona",

    "voice_title": "<b>Wybór głosu</b>",
    "voice_description": "Proszę nacisnąć głos, żeby go odsłuchać. Haczyk oznacza wybrany.",
    "voice_male": "Męskie",
    "voice_female": "Żeńskie",
    "voice_set": "✓ Głos: {voice}",
    "voice_use": "Wybieram: {voice}",
    "voice_listening": "Odtwarzanie: {voice}",
    "voice_only_one": "Dla tego języka syntezator ma jeden głos męski i jeden żeński — więcej nie istnieje.",
    "voice_preview_failed": "Nie udało się pobrać próbki, proszę spróbować jeszcze raz",
})


# ============================================================================
# АПГРЕЙД ПОД ШЕСТЬ ЯЗЫКОВ
#
# Добавлено, когда бот перестал быть «ботом для немецкого»: при первом запуске
# человек теперь выбирает не только язык интерфейса, но и какой язык учить, а
# подсказки направления стали работать на все тридцать пар вместо восьми.
# ============================================================================
TEXTS.update({
    "btn_rating": "Ranking",
    "friend_fallback": "przyjacielu",
    "onboarding_learning_title": "<b>Jakiego języka się uczyć?</b>",
    "onboarding_learning_desc": "Znaczenia będą pokazywane w języku: {native}\nJęzyk można zmienić w ustawieniach w każdej chwili.",
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
    "help_how_to_use_text": "<b>Quiz</b>\n{words}, cztery warianty. Bot zapamiętuje błędy i częściej wraca do trudnych słów. Po quizie można od razu powtórzyć pytania z błędami.\n\n<b>Wymowa</b>\nW pytaniu brzmi słowo, po odpowiedzi — słowo razem z przykładem. Głos można wybrać w ustawieniach, męski albo żeński.\n\n<b>Języki</b>\n{languages} — w każdej parze i w obie strony. Postępy i ranking liczą się osobno dla każdego języka.\n\n\nSłowo jest <b>opanowane</b> po trzech poprawnych odpowiedziach z rzędu, w różne dni.\n<b>Seria</b> rośnie za każdy quiz w danym dniu.\nBłąd w tłumaczeniu lub wymowie — przycisk pod quizem.",
    "help_community_title": "<b>O bocie i społeczności</b>",
    "help_community_text": "<b>GenauLingua</b> — {language_count} języków w każdej parze: {languages}\n12 900 słów A1–C2, każde z przykładem i wymową native speakera.\nInterfejs: {interface_languages}\n\n<b>t.me/genaulingua_chat</b>\nBłędy, pomyłki w tłumaczeniu, pomysły — czytamy wszystko. Zgłoszenia o wymowie są szczególnie cenne: maszyna nie słyszy akcentu.",
})


# ============================================================================
# ВОПРОС НА СЛУХ
#
# Самого слова на экране нет — иначе слушать незачем. Варианты стоят на
# ИЗУЧАЕМОМ языке: спрашивают «что услышал», а не «что это значит».
# ============================================================================
TEXTS.update({
    "quiz_question_listen": "Proszę posłuchać i wybrać usłyszane słowo:",
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
    "settings_btn_channels": "Skład zajęć",
    "settings_channels_line": "Zajęcia: <b>{channels}</b>",
    "channels_title": "<b>Skład zajęć</b>",
    "channels_description": "Jakie gry dodawać do rundy. Nowe słowo przychodzi jako karta „Czytam”, a gdy jest już znane — wraca w innych grach: przypomnieć, usłyszeć, powiedzieć. Im więcej gier, tym trwalsze słowo.",
    "channel_text": "📖 Czytam",
    "channel_audio": "🎧 Słucham",
    "channel_speech": "🎤 Mówię",
    "quiz_result_recalled": "💭 Przypomniane: {count}",
    "home_scale_reverse": "Przypominam",
    "channel_reverse": "💭 Przypominam",
    "channels_text_always": "„Czytam” się nie wyłącza: lekcja bez żadnego sposobu to pusty ekran.",
    "channels_audio_blocked": "🎧 „Słucham” i „Mówię” są niedostępne: wymowa jest wyłączona.",
})


# ============================================================================
# ВОПРОС ВСЛУХ
#
# Ответ приходит голосовым сообщением, а не нажатием. Распознаватель отвечает
# на вопрос «то ли слово сказано», и только на него: качество произношения он
# судить не умеет — он обучен ПОНИМАТЬ акцент, а не замечать его.
# ============================================================================
TEXTS.update({
    "quiz_question_speak": "🎤 Proszę wypowiedzieć to słowo na głos — w wiadomości głosowej",
    "speech_btn_reference": "Odsłuchać wolniej",
    "speech_btn_skip": "Pomiń",
    "speech_listening": "🎧 Słucham…",
    "speech_not_understood": "Nie udało się rozpoznać. Proszę nagrać jeszcze raz — bliżej mikrofonu i trochę głośniej.",
    "speech_send_voice": "🎤 Na to pytanie odpowiada się wiadomością głosową. Proszę nacisnąć i przytrzymać przycisk mikrofonu.",
    "speech_skipped": "Pominięto",
    "quiz_result_spoken": "🎤 Na głos: {count}",
})


# ============================================================================
# ДОМАШНИЙ ЭКРАН: ТРИ ШКАЛЫ
# ============================================================================
TEXTS.update({
    "home_scale_text": "Czytam",
    "home_scale_audio": "Słucham",
    "home_scale_speech": "Mówię",
    "home_btn_learn": "Nauka słów",
    "home_streak": "seria {days} dni",
    "home_rank": "miejsce {rank}",
    "home_hint": "",
    "home_channel_not_ready": "{channel}: jeszcze za wcześnie. Gotowych słów jest {ready}, potrzeba co najmniej {minimum}. Warto poćwiczyć na kartach — otwierają pozostałe kanały.",
})


# ============================================================================
# НАСТРОЙКИ: ТРИ ГРУППЫ
#
# «Что учу» человек меняет часто, «как мне удобно» ставит один раз. Восемь
# равных пунктов перемешивали то и другое, и первым в списке стоял режим
# викторины, которым не пользуются 96%.
# ============================================================================
TEXTS.update({
    "settings_group_what": "Czego się uczę",
    "settings_group_what_title": "<b>Czego się uczę</b>",
    "settings_group_how": "Jak się uczę",
    "settings_group_how_title": "<b>Jak się uczę</b>",
    "settings_group_bot": "Bot",
    "settings_group_bot_title": "<b>Bot</b>",
    "settings_group_what_about": "Język, cel i poziom.",
    "settings_group_how_about": "Z czego składa się runda i jak brzmi.",
    "settings_group_bot_about": "Język bota, przypomnienia i pomoc.",
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
    "quiz_btn_one_more": "Jeszcze jedna runda",
    "home_btn_stats": "Szczegóły",
    "notif_off_how_to_return": "Włączyć ponownie: Ustawienia → Bot → Przypomnienia",
    "reminder_offer": "Przypominać raz na dzień? Łatwiej nie zgubić tego, co już opanowane — i seria się nie urywa.",
    "reminder_offer_yes": "Tak, proszę przypominać",
    "reminder_offer_no": "Nie trzeba",
    "reminder_offer_done": "Gotowe. Godzinę i dni można zmienić w ustawieniach.",
    "level_offer": "Na poziomie <b>{current}</b> błędów prawie nie ma. Przejść na <b>{following}</b>? Wszystkie postępy zostają.",
    "level_offer_yes": "Tak, przejść na {following}",
    "level_offer_no": "Zostaję",
    "level_offer_done": "Poziom <b>{following}</b>. Słowa będą trudniejsze.",
})


# ============================================================================
# ЗАЧЕМ УЧИШЬ — ОПРОС, ВСТРОЕННЫЙ В ПЕРВОЕ НАЖАТИЕ
#
# Режим «по категории» работает, и им пользуются ТРИ человека из 233:
# он спрятан третьим уровнем настроек. Каждая кнопка здесь И отвечает
# на вопрос, И начинает первый круг — шага не прибавилось.
# ============================================================================
TEXTS.update({
    "goal_question": "Do czego potrzebny jest język? Dobierzemy słowa pod odpowiedź.",
    "goal_work": "Do pracy",
    "goal_travel": "Na podróże",
    "goal_living": "Do życia za granicą",
    "goal_study": "Do nauki",
    "goal_any": "Po prostu uczyć się słów",
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
    "intro_games": "Jedno słowo uczy się tu na cztery sposoby: przeczytać, przypomnieć ze znaczenia, usłyszeć, powiedzieć na głos.\nLekcja miesza je sama.",
    "intro_numbers": "12 902 słowa · 20 tematów · 6 poziomów\nSześć języków w dowolnej parze: na przykład polski przez angielski.",
    "intro_menu_settings": "język, skład rundy, przypomnienia",
    "intro_menu_stats": "postępy",
    "intro_menu_rating": "klasyfikacja miesiąca",
    "intro_menu_learn": "runda",
    "intro_menu_title": "Co gdzie:",
})


# ============================================================================
# ЗАЧЕМ УЧУ — ЭКРАН НАСТРОЙКИ
#
# Без него цель осталась бы пустой навсегда у всех 233 нынешних
# пользователей: онбординг у них давно позади. Та же дыра, что была у
# состава занятия — колонка есть, экрана нет.
# ============================================================================
TEXTS.update({
    "settings_btn_goal": "Cel",
    "settings_goal_title": "<b>Po co się uczę</b>",
    "settings_goal_description": "Słowa z wybranego tematu będą przychodzić pierwsze. Trudność nadal zależy od poziomu, a to, co już opanowane, wraca do powtórek.",
    "settings_goal_set": "Cel zapisany",
    "settings_goal_line": "Cel: <b>{goal}</b>",
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
    "match_title": "<b>Proszę znaleźć pary</b>",
    "match_progress": "Dopasowano: {matched} z {total}",
    "match_errors": "✗ pomyłki: {count}",
    "match_hint": "Proszę nacisnąć słowo z dowolnej strony, a potem jego parę z drugiej.",
    "match_wrong": "✗ Nie para",
    "match_done": "<b>Plansza ukończona!</b>",
    "match_done_counted": "Do postępu zaliczono {counted} z {total}: tylko pary dopasowane za pierwszym razem i nigdy ostatnia — przy niej nie ma już wyboru.",
    "match_btn_again": "Jeszcze jedna plansza",
    "match_not_ready": "Jeszcze za wcześnie: plansza potrzebuje {need} znanych słów, a jest {have}. Warto poćwiczyć na kartach — one ją otworzą.",
})

TEXTS["match_back_to_round"] = "Wracamy do rundy."

TEXTS.update({
    "settings_btn_match": "Plansza w rundzie",
    "settings_match_title": "<b>Plansza w rundzie</b>",
    "settings_match_description": "Co drugą rundę w środku przychodzi plansza — zamiast jednego pytania: pięć słów i pięć znaczeń, trzeba znaleźć pary. Brane są tylko znane słowa.",
    "match_state_on": "Plansza włączona: przyjdzie w środku rundy.",
    "settings_match_short_on": "z tablicą",
    "settings_channels_short_one": "tylko „Czytam”",
    "settings_channels_short_some": "{count} gry z czterech",
    "settings_channels_short_all": "wszystkie cztery gry",
    "plural_words": "słowo|słowa|słów",
    "plural_points": "punkt|punkty|punktów",
    "settings_audio_short_off": "bez dźwięku",
    "settings_audio_short_on": "z dźwiękiem",
    "settings_match_short_off": "bez tablicy",
    "match_state_off": "Plansza wyłączona: runda to same pytania.",
})
