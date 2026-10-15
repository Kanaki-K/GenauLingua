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
    "btn_back": "Powrót",
    "menu_placeholder": "Proszę wybrać działanie…",

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

    "notif_btn_toggle_on": "Przypomnienia: włączone",
    "notif_btn_toggle_off": "Przypomnienia: wyłączone",
    "notif_btn_time": "Godzina: {time}",
    "notif_btn_days": "Wybór dni",
    "notif_btn_timezone": "Zmiana strefy czasowej",

    "notif_timezone_title": "<b>Proszę wybrać strefę czasową</b>",
    "notif_timezone_current": "Obecnie: {timezone}",
    "notif_timezone_prompt": "Proszę wybrać miasto z tej samej strefy czasowej:",
    "notif_timezone_more": "Inne miasto",
    "notif_timezone_back": "Powrót",
    "notif_timezone_set": "✓ Strefa czasowa ustawiona: {city}",

    "notif_time_title": "<b>Proszę wybrać godzinę przypomnienia</b>",
    "notif_time_current": "Obecna godzina: {time}",
    "notif_time_timezone": "Strefa czasowa: {timezone}",
    "notif_time_hint": "Przypomnienie będzie przychodzić codziennie o wybranej godzinie.",
    "notif_time_set": "✓ Godzina ustawiona: {time}",

    "notif_days_title": "<b>Proszę wybrać dni przypomnień</b>",
    "notif_days_hint": "Proszę nacisnąć dzień, żeby go włączyć lub wyłączyć.\n✓ — dzień włączony\n✗ — dzień wyłączony\n\nNa koniec proszę nacisnąć „Zapisać”.",
    "notif_days_all": "Wszystkie dni",
    "notif_days_weekdays": "Dni powszednie (pn–pt)",
    "notif_days_save": "Zapisać",
    "notif_days_saved": "✓ Dni zapisane!",
    "notif_days_all_selected": "✓ Wybrano wszystkie dni",
    "notif_days_weekdays_selected": "✓ Wybrano dni powszednie (pn–pt)",
    "notif_days_none": "Proszę wybrać przynajmniej jeden dzień przypomnień!",

    "notif_toggle_on": "Przypomnienia włączone!",
    "notif_toggle_off": "Przypomnienia wyłączone",

    "day_mon": "Pn",
    "day_tue": "Wt",
    "day_wed": "Śr",
    "day_thu": "Cz",
    "day_fri": "Pt",
    "day_sat": "So",
    "day_sun": "Nd",

    "notif_btn_back": "Powrót do ustawień",

    "notif_default_name": "przyjacielu",

    "anchor_streak": "🔥 {days}",


    # JEDEN POWÓD, BY WRÓCIĆ — i musi być prawdziwy

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

    "qmode_btn_level": "Według poziomu",
    "qmode_btn_category": "Temat",
    "qmode_btn_all": "Wszystkie słowa",
    "qmode_btn_difficult": "Trudne",

    "qmode_level_short": "{level}",
    "qmode_category_short": "{category}",
    "qmode_all_short": "Wszystkie słowa",
    "qmode_difficult_short": "Trudne słowa",

    "qmode_level_title": "<b>Wybór poziomu</b>",
    "qmode_level_desc": "Od pierwszych słów do swobodnych dyskusji. Wszystkie poziomy są otwarte — proszę wybrać odpowiedni.\n\n• A1–A2 — podstawowe słownictwo\n• B1–B2 — swobodna rozmowa\n• C1–C2 — biegła znajomość",
    "qmode_level_set": "✓ Tryb: według poziomu ({level})",

    "qmode_category_title": "<b>Wybór tematu</b>",
    "qmode_category_desc": "Od jedzenia do nauki — proszę wybrać potrzebny temat.\n\nKażdy temat zawiera słowa ze wszystkich poziomów.",
    "qmode_category_set": "✓ Temat: {category}",

    # Nazwy kategorii
    "cat_arbeit_beruf": "Praca",
    "cat_bildung_lernen": "Edukacja",
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
    "cat_wissenschaft": "Nauka",
    "cat_wohnen_haus": "Mieszkanie",
    "cat_zeit_alltag": "Codzienność",

    "qmode_all_set": "✓ Tryb: wszystkie słowa",

    "qmode_difficult_set": "✓ Tryb: trudne słowa",
    "qmode_difficult_few": "Trudnych słów na razie: {count} — potrzeba co najmniej 4.\nWarto przejść jeszcze kilka lekcji!",
    "qmode_difficult_empty": "Na razie brak trudnych słów.\nWarto przejść kilka lekcji!",

    "quiz_btn_change_mode": "Poziom i tematy",
    "quiz_btn_report_error": "Zgłosić błąd",
    "report_btn_confirm": "✓ Potwierdzam ({count})",
    "report_btn_send": "Wysłać",
    "report_no_words": "Brak słów do zgłoszenia",
    "report_none_selected": "Proszę wybrać przynajmniej jedno słowo",
    "report_pick_kind": "Wybrano słów: {count}. Teraz proszę wskazać, co jest nie tak — tłumaczenie czy wymowa.",
    "report_sent": "✓ Wysłano zgłoszeń: {count} — dziękujemy!\nJeśli błąd się potwierdzi, przyznamy +{points}",
    "report_daily_limit": "Dzienny limit zgłoszeń wyczerpany (maks. 20)",
    "report_all_reported": "✓ Wszystkie słowa z tej lekcji są już zgłoszone",
    "report_already_sent": "✓ Już wysłane wcześniej",
    "report_btn_kind_text": "Błędne tłumaczenie",
    "report_btn_kind_audio": "Błędna wymowa",
    "report_sent_audio": "✓ Wysłano zgłoszeń: {count} — dziękujemy!\nZgłoszenia wymowy są szczególnie cenne: automatyczna kontrola nie słyszy akcentu.\nJeśli błąd się potwierdzi — +{points}",
    "report_approved": "✓ Zgłoszenie dotyczące <b>{word}</b> zostało przyjęte — poprawimy tłumaczenie.\n+{points} punktów do wyniku miesiąca — dziękujemy, słownik będzie lepszy dla wszystkich.",
    "award_won": "{mark} {month}: miejsce {rank} w rankingu miesiąca.\nDo wyniku ogólnego dodano {bonus} pkt.",
    "report_approved_audio": "✓ Zgłoszenie wymowy przyjęte: <b>{word}</b>.\nNagranie zostanie przygotowane na nowo. +{points} punktów do wyniku miesiąca — dziękujemy.",

    # ============================================================================
    # QUIZ
    # ============================================================================
    "quiz_no_level": "Najpierw proszę wybrać poziom poleceniem /start",
    "quiz_error_generation": "✗ Przy przygotowaniu lekcji wystąpił błąd.\nProszę spróbować jeszcze raz przez /start",
    "quiz_no_words": "✗ Niestety dla tego poziomu nie ma jeszcze słów.\nProszę wybrać inny poziom.",

    "quiz_question_number": "{current} / {total}",

    "quiz_correct": "✓ <b>Dobrze</b>",
    "quiz_wrong": "✗ <b>Źle</b>",
    "quiz_correct_answer": "Prawidłowa odpowiedź:",

    "quiz_btn_next": "Dalej →",

    "quiz_answer_already_counted": "Odpowiedź została już zaliczona. Kontynuujemy?",
    "quiz_btn_repeat_errors": "Powtórka błędów",

    "quiz_completed": "<b>Lekcja ukończona</b>",
    "quiz_result_correct": "Poprawnie: <b>{correct}/{total}</b>",
    "quiz_result_percentage": "Wynik: <b>{percentage}%</b>",
    "quiz_result_details": "<b>Szczegóły:</b>",
    "quiz_result_errors": "Błędów: {count}",

    # POCHWAŁA NA KONIEC LEKCJI — tylko za to, co się stało
    "praise_first_round": "Pierwsza lekcja ukończona. Teraz słowa zaczną wracać — dzięki temu zostają w pamięci.",
    "praise_first_learned": "Pierwsze słowo nauczone: trzy poprawne odpowiedzi z rzędu, w różne dni.",
    "praise_learned": "Nauczone słowa podczas tej lekcji: {count}",
    "praise_best_streak": "Rekord osobisty: {days_word} z rzędu",
    "praise_milestone": "Już {count} słów w nauce",
    "praise_first_speech": "Pierwsza poprawna odpowiedź głosem",
    "praise_first_audio": "Pierwsza poprawna odpowiedź ze słuchu",
    "praise_comeback": "Witamy z powrotem. Przerwa trwała {days_word}.",
    "praise_perfect": "Lekcja bez błędu",
    "praise_streak": "Seria: {days_word} z rzędu",
    "praise_freeze_saved": "Wczoraj była przerwa, ale ochrona serii ją uratowała: {days_word} z rzędu. Kolejna ochrona będzie dostępna za tydzień.",
    "praise_streak_3": "Trzy dni z rzędu — nawyk się zaczyna.",
    "praise_streak_7": "Cały tydzień z rzędu! To najważniejszy próg: dalej nawyk trzyma się sam.",
    "praise_streak_14": "Dwa tygodnie z rzędu — świetne tempo.",
    "praise_streak_30": "Miesiąc z rzędu! To już prawdziwy nawyk.",
    "praise_new_words": "Nowe słowa: {count}",
    "praise_returned": "Rozpoznane ponownie: {count}",
    "praise_progress": "Słowa w nauce: {count} · do {target} jeszcze {left}",
    "praise_progress_top": "Słowa w nauce: {count}",
    "praise_points": "Punkty: +{points}",

    "quiz_repeat_title": "<b>Powtórka błędów</b>",
    "quiz_no_errors": "✓ Lekcja bez żadnych błędów!",
    "quiz_error_next": "✗ Nie udało się wczytać następnego pytania.",

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
    "rating_start_quiz": "Zapraszamy na pierwszą lekcję!",
    "rating_join_by_lesson": "Punkty za zgłoszenia ({score}) zostały przyznane. Proszę ukończyć lekcję, aby dołączyć do rankingu miesiąca.",
    "release_notes_2026_10": "✨ <b>GenauLingua 2.0 — zbudowaliśmy bota od nowa</b>\n\n<b>Nie tylko niemiecki.</b> Można uczyć się ukraińskiego, angielskiego, tureckiego, niemieckiego, polskiego lub rosyjskiego — z każdego z nich. Interfejs też jest w sześciu językach.\n\n<b>Sześć gier zamiast jednej.</b> Wcześniej było tylko „wybierz tłumaczenie”.\n\nTeraz gry w lekcji się zmieniają:\n📖 Czytam · 💭 Przypominam · 🎧 Słucham · 🎤 Mówię · 🧩 Proszę znaleźć pary · 🧱 Układam\n\nW „Mówię” odpowiada się głosem, w „Układam” składa się zdanie ze słów — bot pokaże, które słowo jest nie na miejscu.\n\n<b>Bot mówi.</b> Każde słowo i przykład ma nagranie naturalnym głosem.\n\n<b>Nowy wygląd.</b> Nowe menu, czysty czat bez zbędnych wiadomości, ekran główny z umiejętnościami, czytelne statystyki, nowy awatar i powitanie.\n\n<b>Cały słownik sprawdzony</b> — wszystkie 12 902 słowa, tłumaczenia i przykłady.\n\n<b>Bot sam się dostosowuje:</b> wraca do słów tuż przed tym, jak wylecą z pamięci, i proponuje wyższy poziom, gdy robi się łatwo.\n\n<b>Poprawione błędy:</b> seria dni liczy się prawidłowo, a punkty w rankingu są uczciwe — za wysiłek. „Nauczone” też liczy się teraz uczciwie: słowo jest nauczone, gdy zostało rozpoznane trzy razy z rzędu w różne dni, a wszystkie przerobione słowa widać w wierszu „Słowa w nauce”.\n\n<b>Przypomnienia są włączone</b> — o wybranej porze. Zmienić lub wyłączyć: Ustawienia → Bot → Przypomnienia.\n\n⭐ Błąd w słowniku? Wystarczy zgłosić go z podsumowania lekcji: każde potwierdzone zgłoszenie to +15 punktów.\n\nPostęp i punkty są zachowane. Proszę spróbować — lekcja zajmuje kilka minut.",
    "rating_position": "Pozycja: <b>#{rank}</b> z {total}",
    "rating_points": "Punkty: <b>{score}</b>",
    "rating_your_month": "<b>Wyniki — {month}:</b>",
    "rating_quizzes": "Lekcje: {count}",
    "rating_words_learned": "Nauczone słowa: {count}",
    "rating_streak": "Seria: {days_word}",
    "rating_avg_result": "Średni wynik: {percent}%",
    "rating_scoring_title": "<b>Jak zdobyć punkty:</b>",
    "rating_scoring_report": "• Potwierdzone zgłoszenie błędu → +{points}",

    "rating_title_alltime": "<b>Moja pozycja — ogółem</b>",
    "rating_position_alltime": "Pozycja: <b>#{rank}</b>",
    "rating_position_none": "Pozycja: <b>—</b>",
    "rating_achievements": "<b>Osiągnięcia:</b>",
    "rating_wins": "Zwycięstwa (1. miejsce): {count}",
    "rating_total_words": "Nauczone słowa: {count}",
    "rating_motivation_start": "Wszystko zaczyna się od pierwszej lekcji — pierwszy krok jest najważniejszy.",
    "rating_motivation_continue": "Tak dalej — pierwsze zwycięstwo blisko!",
    "rating_motivation_champion": "Prawdziwe mistrzostwo!",

    "table_title_monthly": "<b>Tabela liderów — {month} {year}</b>",
    "table_title_alltime": "<b>Tabela liderów — ogółem</b>",
    "table_empty": "Na razie nikt nie bierze udziału.\nPierwsze miejsce czeka!",
    "table_you_in_top": "Moje miejsce: <b>#{rank}</b> z {total}",
    "table_you_not_in_top": "Moje miejsce: <b>#{rank}</b> z {total} — {score}",
    "table_you_outside": "Moje miejsce: poza pierwszą dziesiątką — {score}",
    "table_you_not_ranked": "Brak jeszcze pozycji w rankingu",
    "btn_leaderboard_table": "Tabela liderów",
    "btn_back_to_rating": "Powrót do pozycji",
    "rating_tab_month": "Miesiąc",
    "rating_tab_alltime": "Ogółem",

    # ============================================================================
    # STATYSTYKI (NOWE)
    # ============================================================================
    "stats_header": "<b>Statystyki</b>",
    "stats_in_work_line": "Słowa w nauce: {count} · do {target} jeszcze {left}",
    "stats_in_work_top": "Słowa w nauce: {count}",
    "stats_details": "W toku: {progress}\nNowe: {new}\nTrudne: {difficult}",
    "stats_achievements_title": "<b>Osiągnięcia</b>",
    "stats_words_count": "Nauczone słowa: <b>{count}</b>",
    "stats_streak_line": "Seria: {days_word} z rzędu",
    "stats_best_streak_line": "Najlepsza seria: {days_word}",
    "stats_quizzes_header": "<b>Lekcje · {level}</b>",
    "stats_quizzes_passed_line": "Ukończone: <b>{count}</b>",
    "stats_quizzes_avg_line": "Średni wynik: <b>{percent}%</b>",
    "stats_quizzes_best_line": "Najlepszy wynik: <b>{percent}%</b>",
    "stats_quizzes_empty": "Na razie brak ukończonych lekcji",
    "stats_recent_header": "<b>Ostatnie lekcje</b>",
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
    "learning_lang_set": "✓ Język nauki: {language}",
    # Wiersz w menu ustawień i ekran «Wymowa»
    "settings_audio_line": "Wymowa: <b>{state}</b>",
    "settings_btn_audio": "Wymowa",
    "audio_state_on": "włączona",
    "audio_state_off": "wyłączona",

    "audio_title": "<b>Wymowa</b>",
    "audio_description": "Słowo brzmi naturalnym głosem. W pytaniu samo słowo, po odpowiedzi — słowo razem z przykładem.",
    "audio_current_voice": "Głos: <b>{voice}</b>",
    "audio_btn_turn_on": "Włączyć wymowę",
    "audio_btn_turn_off": "Wyłączyć wymowę",
    "audio_btn_choose_voice": "Wybór głosu",
    "audio_turned_on": "✓ Wymowa włączona",
    "audio_turned_off": "Wymowa wyłączona",

    "voice_title": "<b>Wybór głosu</b>",
    "voice_description": "Proszę nacisnąć głos, żeby go odsłuchać. Znaczek ✓ oznacza wybrany głos.",
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
    "help_how_to_use_text": "<b>Lekcja</b>\n{words}, cztery warianty odpowiedzi. Gry zmieniają się same: „Czytam”, „Przypominam”, „Słucham”, „Mówię” i plansza do łączenia w pary. Bot zapamiętuje błędy i częściej wraca do trudnych słów. Po lekcji można od razu powtórzyć pytania z błędami.\n\n<b>Wymowa</b>\nW pytaniu brzmi słowo, po odpowiedzi — słowo razem z przykładem. Głos można wybrać w ustawieniach, męski albo żeński.\n\n<b>Języki</b>\n{languages} — w każdej parze. Postępy i ranking liczą się osobno dla każdego języka.\n\n\nSłowo jest <b>nauczone</b> po trzech poprawnych odpowiedziach z rzędu, w różne dni.\n<b>Seria</b> to kolejne dni, w których była co najmniej jedna lekcja.\nBłąd w tłumaczeniu lub wymowie — przycisk „Zgłosić błąd” po lekcji.",
    "help_community_title": "<b>O bocie i społeczności</b>",
    "help_community_text": "<b>GenauLingua</b> — {language_count} języków w każdej parze: {languages}\n12 900 słów A1–C2, każde z przykładem i naturalnie brzmiącą wymową.\nInterfejs: {interface_languages}\n\n<b>t.me/genaulingua_chat</b>\nBłędy, pomyłki w tłumaczeniu, pomysły — czytamy wszystko. Zgłoszenia o wymowie są szczególnie cenne: maszyna nie słyszy akcentu.",
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
    "rating_scoring_quiz": "• Ukończona lekcja → +10",
    "rating_scoring_word": "• Nauczone słowo → +3",
    "rating_scoring_streak": "• Każdy kolejny dzień serii jest wart więcej, do +10",
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
    "settings_btn_channels": "Gry w lekcji",
    "settings_channels_line": "Lekcja: <b>{channels}</b>",
    "channels_title": "<b>Gry w lekcji</b>",
    "channels_description": "Gry, które trafiają do lekcji. Nowe słowo przychodzi jako karta „Czytam”, a gdy jest już znane — wraca w innych grach: przypomnieć, usłyszeć, powiedzieć, ułożyć zdanie. Im więcej gier, tym trwalej słowo zostaje w pamięci.",
    "channel_text": "📖 Czytam",
    "channel_audio": "🎧 Słucham",
    "channel_speech": "🎤 Mówię",
    "channel_build": "🧱 Układam",
    "home_scale_build": "Układam",
    "quiz_result_built": "🧱 Ułożone: {count}",
    "build_hint": "Proszę ułożyć zdanie ze słów poniżej — niektóre są zbędne",
    "build_btn_check": "Sprawdzić",
    "build_full": "Wszystkie miejsca są zajęte. Proszę usunąć słowo przyciskiem ⌫ albo nacisnąć „Sprawdzić”.",
    "build_order_only": "↔ <b>Słowa poprawne, inna kolejność</b>",
    "build_reference": "Poprawnie:",
    "build_yours": "Odpowiedź:",
    "build_extra": "Zbędne: {words}",
    "build_missing": "Brakuje: {words}",
    "stats_grammar_line": "Gramatyka: poprawnie {correct} z {shown}",
    "quiz_result_recalled": "💭 Przypomniane: {count}",
    "home_scale_reverse": "Przypominam",
    "channel_reverse": "💭 Przypominam",
    "channels_text_always": "„Czytam” nie da się wyłączyć: od tej karty zaczyna się każde nowe słowo.",
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
    "quiz_question_speak": "🎤 Proszę wypowiedzieć to słowo na głos w wiadomości głosowej: nacisnąć i przytrzymać ikonę mikrofonu w polu wpisywania Telegrama, w prawym dolnym rogu",
    "speech_btn_reference": "Odsłuchać wolniej",
    "speech_btn_skip": "Pominąć",
    "speech_listening": "🎧 Słucham…",
    "speech_not_understood": "Nie udało się rozpoznać. Proszę nagrać jeszcze raz — bliżej mikrofonu i trochę głośniej.",
    "speech_try_again": "Brzmiało to jak „{heard}” — jeszcze nie to. Proszę nagrać ponownie: próba {attempt} z {total}.",
    "speech_send_voice": "🎤 Na to pytanie odpowiada się wiadomością głosową. Proszę nacisnąć i przytrzymać przycisk mikrofonu.",
    "speech_skipped": "Pominięto",
    "speech_not_counted": "Znowu brzmiało jak „{heard}”. Nie liczę tego ani jako dobrej odpowiedzi, ani jako błędu — proszę posłuchać, jak to brzmi, i idziemy dalej.",
    "lesson_expired": "Ta lekcja została przerwana — bot był aktualizowany albo skończyła się dawno temu. Proszę zacząć nową przyciskiem poniżej.",
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
    "home_streak": "seria: {days_word}",
    "home_rank": "miejsce {rank}",
    "home_hint": "",
    "home_channel_not_ready": "{channel}: jeszcze za wcześnie. Słów gotowych do tej gry: {ready}, potrzeba co najmniej {minimum}. Warto poćwiczyć na kartach — to one otwierają pozostałe gry.",
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
    "settings_group_how_about": "Z czego składa się lekcja i jak brzmi.",
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
    "quiz_btn_one_more": "Jeszcze jedna lekcja",
    "home_btn_stats": "Szczegóły",
    "notif_off_how_to_return": "Włączyć ponownie: Ustawienia → Bot → Przypomnienia",
    "reminder_offer": "Przypominać raz dziennie? Łatwiej wtedy utrzymać to, co już nauczone, i nie przerwać serii.",
    "reminder_offer_yes": "Tak, proszę przypominać",
    "reminder_offer_no": "Nie trzeba",
    "reminder_offer_done": "✓ Gotowe: przypomnienie przyjdzie o <b>{time}</b> ({city}). Godzinę, dni i strefę czasową można dostosować.",
    "reminder_offer_setup": "Ustawienia przypomnień",
    "level_offer": "Na poziomie <b>{current}</b> błędów prawie nie ma. Przejść na <b>{following}</b>? Wszystkie postępy zostają.",
    "level_offer_yes": "Tak, przejść na {following}",
    "level_offer_no": "Zostaję",
    "level_offer_done": "Nowy poziom: <b>{following}</b>. Słowa będą trudniejsze.",
    "level_offer_pick": "Poziom <b>{current}</b> wydaje się łatwy. Proszę wybrać, od którego poziomu kontynuować. Wszystkie postępy zostają.",
    "level_offer_stay": "Zostaję na {current}",
    "level_down_offer": "Na poziomie <b>{current}</b> jest na razie sporo błędów. Przejść na <b>{previous}</b>? Słowa będą łatwiejsze, wszystkie postępy zostają.",
    "level_down_yes": "Tak, przejść na {previous}",
    "level_down_done": "Nowy poziom: <b>{previous}</b>. Słowa będą łatwiejsze.",
})


# ============================================================================
# ЗАЧЕМ УЧИШЬ — ОПРОС, ВСТРОЕННЫЙ В ПЕРВОЕ НАЖАТИЕ
#
# Режим «по категории» работает, и им пользуются ТРИ человека из 233:
# он спрятан третьим уровнем настроек. Каждая кнопка здесь И отвечает
# на вопрос, И начинает первый круг — шага не прибавилось.
# ============================================================================
TEXTS.update({
    "goal_question": "Do czego potrzebny jest język? Dobierzemy słowa do celu.",
    "goal_work": "Do pracy",
    "goal_travel": "Do podróży",
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
    "intro_games": "Każde słowo ćwiczy się tu na kilka sposobów: przeczytać, przypomnieć sobie po znaczeniu, rozpoznać ze słuchu, powiedzieć na głos, dopasować w pary na planszy.\nLekcja sama je miesza.",
    "intro_numbers": "12 902 słowa · 20 tematów · 6 poziomów\nSześć języków w dowolnej parze: na przykład polski przez angielski.",
    "intro_menu_settings": "język, gry w lekcji, przypomnienia",
    "intro_menu_stats": "postępy",
    "intro_menu_rating": "ranking miesiąca",
    "intro_menu_learn": "lekcja",
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
    "match_wrong": "✗ To nie para",
    "match_done": "<b>Plansza ukończona!</b>",
    "match_done_counted": "Do postępu zaliczono {counted} z {total}: tylko pary dopasowane za pierwszym razem i nigdy ostatnia — przy niej nie ma już wyboru.",
    "match_btn_again": "Jeszcze jedna plansza",
    "match_not_ready": "Jeszcze za wcześnie: plansza potrzebuje {need} znanych słów, a jest {have}. Warto poćwiczyć na kartach — one ją otworzą.",
})

TEXTS["match_back_to_round"] = "Wracamy do lekcji."

TEXTS.update({
    "settings_btn_match": "Plansza w lekcji",
    "settings_match_title": "<b>Plansza w lekcji</b>",
    "settings_match_description": "W środku każdej lekcji pojawia się plansza — w miejsce jednego pytania: pięć słów i pięć znaczeń, trzeba znaleźć pary. Trafiają na nią tylko znane słowa, więc plansza wchodzi do gry, gdy jest ich co najmniej dziesięć.",
    "match_state_on": "Plansza włączona: pojawi się w środku lekcji.",
    "settings_match_short_on": "z planszą",
    "settings_channels_short_one": "tylko „Czytam”",
    "settings_channels_short_some": "{count} z {total} gier",
    "settings_channels_short_all": "wszystkie gry",
    "plural_words": "słowo|słowa|słów",
    "plural_points": "punkt|punkty|punktów",
    "plural_days": "dzień|dni|dni",
    "settings_audio_short_off": "bez dźwięku",
    "settings_audio_short_on": "z dźwiękiem",
    "settings_match_short_off": "bez planszy",
    "match_state_off": "Plansza wyłączona: lekcja to same pytania.",
})

# ============================================================================
# СООБЩЕНИЯ ПО ИНИЦИАТИВЕ БОТА — патч 2.1 «Вовлечение» (`nudge_texts`).
# Голос и запрет значков — в ru.py; номера вариантов `_N` те же (тест).
# ============================================================================
TEXTS.update({
    "plural_lessons": "lekcja|lekcje|lekcji",
    "nd_teaser_quiz_1": "Co znaczy {word}? {meaning}",
    "nd_teaser_quiz_2": "Sprawdźmy: {word} - {meaning}",
    "nd_teaser_quiz_3": "Jedno ze słów w nauce: {word} - {meaning}",
    "nd_teaser_quiz_4": "Jak przetłumaczyć {word}? {meaning}",
    "nd_teaser_new_1": "Na przykład: {word} - {meaning}",
    "nd_teaser_new_2": "Pierwsze słowo: {word} - {meaning}",
    "nd_teaser_new_3": "Jak przetłumaczyć {word}? Tłumaczenie jest ukryte - wystarczy je dotknąć: {meaning}",
    "nd_streak_head_1": "<b>{name}, seria: {days} z rzędu</b>",
    "nd_streak_head_2": "<b>{name}, {days} z rzędu. Kontynuujemy?</b>",
    "nd_streak_head_3": "<b>{name}, już {days} z rzędu</b>",
    "nd_streak_head_4": "<b>{name}, {days} bez przerwy</b>",
    "nd_streak_head_5": "<b>{name}, jeszcze jedna lekcja, i będzie {next_days} z rzędu</b>",
    "nd_streak_head_6": "<b>{name}, seria czeka na ciąg dalszy: {days}</b>",
    "nd_streak_head_7": "<b>{days} z rzędu, {name}</b>",
    "nd_streak_head_8": "<b>{name}, {days} z rzędu. Dziś jeszcze jedna lekcja?</b>",
    "nd_body_learned_1": "Znane słowa: {known_n} · nauczone: {learned}",
    "nd_body_learned_2": "Słowa w nauce: {in_work} · nauczone: {learned}",
    "nd_body_learned_3": "Znane słowa: {known_n}, z tego nauczone: {learned}.",
    "nd_body_known_1": "Znane słowa: {known_n}. Każda lekcja dodaje nowe.",
    "nd_body_known_2": "Słowa w nauce: {in_work}. Pierwsze nauczone już blisko.",
    "nd_body_known_3": "Znane słowa: {known_n}.",
    "nd_streak_close_1": "Małymi krokami do dużego celu.",
    "nd_streak_close_2": "Codziennie po trochu: tak słowa zostają w pamięci.",
    "nd_streak_close_3": "Jedna lekcja dziś przedłuży serię.",
    "nd_streak_close_4": "Lekcja to około {minutes_n} minut.",
    "nd_streak_close_5": "Regularność jest ważniejsza niż długość lekcji.",
    "nd_progress_head_known": "<b>{name}, znane słowa: {known_n}</b>",
    "nd_progress_head_1": "<b>{name}, słowa czekają na powtórkę</b>",
    "nd_progress_head_2": "<b>{name}, znajdzie się kilka minut?</b>",
    "nd_progress_head_3": "<b>{name}, kontynuujemy od tego samego miejsca?</b>",
    "nd_progress_head_4": "<b>{name}, wracamy do słów?</b>",
    "nd_progress_head_5": "<b>{name}, dobry moment, by odświeżyć słowa</b>",
    "nd_due_1": "Słowa do powtórki: {due_n}. Terminy bot liczy sam.",
    "nd_due_2": "Pora powtórzyć: {due}, zanim wylecą z pamięci.",
    "nd_due_3": "Słów do powtórki: {due_n}. Bot już wybrał, od których zacząć.",
    "nd_due_many_1": "Słów do powtórki uzbierało się sporo: lekcja sama zacznie od najważniejszych.",
    "nd_due_many_2": "Powtórki się nazbierały. Wystarczy jedna lekcja dziennie, reszta poczeka.",
    "nd_praise_1": "Ukończone lekcje: {lessons_n}. Po trochu, ale regularnie.",
    "nd_praise_2": "Ukończone lekcje: {lessons_n}. Małymi krokami do dużego celu.",
    "nd_praise_3": "Ukończone lekcje: {lessons_n}, i każda dodała słów.",
    "nd_short_1": "Jedna lekcja to około {minutes_n} minut.",
    "nd_short_2": "To kilka minut.",
    "nd_first_head_words": "<b>{name}, wczoraj nowe słowa: {first_n}</b>",
    "nd_first_head_1": "<b>{name}, dobry początek</b>",
    "nd_first_head_2": "<b>{name}, sprawdzimy wczorajsze słowa?</b>",
    "nd_first_body_1": "Powtórka następnego dnia pomaga utrwalić słowa.",
    "nd_first_body_2": "Drugi dzień to najlepszy moment, by utrwalić nowe słowa.",
    "nd_first_close_1": "To kilka minut.",
    "nd_first_close_2": "Lekcja to około {minutes_n} minut.",
    "nd_kept_head_1": "<b>{name}, wszystko jest na miejscu</b>",
    "nd_kept_head_2": "<b>{name}, słowa są zapisane</b>",
    "nd_kept_head_3": "<b>{name}, dawno się nie widzieliśmy</b>",
    "nd_kept_body_1": "Znane słowa: {known_n} · nauczone: {learned}. Nic nie przepadło - lekcja zacznie od tych, które warto odświeżyć.",
    "nd_kept_body_2": "Cały postęp jest zapisany. Lekcja zacznie od słów, które warto odświeżyć.",
    "nd_kept_body_3": "Przerwy zdarzają się każdemu. Zacząć można od jednej krótkiej lekcji.",
    "nd_kept_best": "Najlepsza seria: {best} z rzędu. Nowa zaczyna się od jednej lekcji.",
    "nd_farewell_head_1": "<b>{name}, przypomnień już nie będzie</b>",
    "nd_farewell_head_2": "<b>{name}, ostatnie przypomnienie</b>",
    "nd_farewell_body_1": "Bot nie będzie już pisać aż do powrotu. Wszystko jest zapisane: znane słowa {known_n}, nauczone {learned}. Kontynuować można w każdej chwili przyciskiem poniżej.",
    "nd_farewell_body_2": "Wygląda na to, że teraz nie ma czasu na naukę - to normalne. Przypomnień już nie będzie. Słowa i postęp są zapisane.",
    "nd_start_head_1": "<b>{name}, pierwsze słowa już czekają</b>",
    "nd_start_head_2": "<b>{name}, zaczynamy?</b>",
    "nd_start_head_3": "<b>{name}, pierwsza lekcja to około {minutes_n} minut</b>",
    "nd_start_body_1": "Bot dobierze najpotrzebniejsze słowa do poziomu i sam będzie pilnować, kiedy je powtórzyć.",
    "nd_start_body_2": "Zaczniemy od najczęstszych słów, tych, które słychać codziennie.",
    "nd_start_body_3": "Nic nie trzeba przygotowywać: {questions} pytań, a potem bot podpowie, co i kiedy powtórzyć.",
    "nd_start3_head_1": "<b>{name}, spróbujemy?</b>",
    "nd_start3_head_2": "<b>{name}, pierwsze słowa wciąż czekają</b>",
    "nd_start_last_head": "<b>{name}, ostatnie zaproszenie</b>",
    "nd_start_last_body": "Przypomnień już nie będzie. Pierwsza lekcja to około {minutes_n} minut - przycisk jest poniżej.",
    "nd_btn_optin": "Przypomnienie o {time}",
    "nd_btn_stop": "Nie wysyłać",
    "nd_optin_done": "✓ Gotowe: przypomnienie będzie przychodzić o <b>{time}</b>. Godzinę można zmienić w ustawieniach.",
})
