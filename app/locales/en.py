"""
English localization for GenauLingua Bot
"""

TEXTS = {
    # ============================================================================
    # MAIN MENU BUTTONS
    # ============================================================================
    "btn_learn_words": "Learn words",
    "btn_stats": "Statistics",
    "btn_settings": "Settings",
    "btn_help": "Help",
    "btn_back": "Back",
    "menu_placeholder": "Choose an action…",

    # ============================================================================
    # WELCOME & START
    # ============================================================================
    "welcome_title": "<b>Hello, {name}!</b>",








    # ============================================================================
    # NOTIFICATIONS
    # ============================================================================
    "notif_title": "<b>Reminders</b>",
    "notif_status": "Status: {status}",
    "notif_status_on": "on",
    "notif_status_off": "off",
    "notif_time": "Time: {time}",
    "notif_days": "Days: {days}",
    "notif_timezone": "Time zone: {timezone}",
    "notif_hint": "The reminder arrives at the chosen time in your time zone.",
    "notif_hint_off": "Turn reminders on — it's easier to keep your streak going.",

    "notif_btn_toggle_on": "Reminders: on",
    "notif_btn_toggle_off": "Reminders: off",
    "notif_btn_time": "Time: {time}",
    "notif_btn_days": "Choose days",
    "notif_btn_timezone": "Change time zone",

    "notif_timezone_title": "<b>Your time zone</b>",
    "notif_timezone_current": "Current: {timezone}",
    "notif_timezone_prompt": "Pick a city in your time zone:",
    "notif_timezone_more": "Another city",
    "notif_timezone_back": "Back",
    "notif_timezone_set": "✓ Time zone set: {city}",

    "notif_time_title": "<b>Reminder time</b>",
    "notif_time_current": "Current time: {time}",
    "notif_time_timezone": "Time zone: {timezone}",
    "notif_time_hint": "The reminder arrives at this time on the days you've chosen.",
    "notif_time_set": "✓ Time set: {time}",

    "notif_days_title": "<b>Reminder days</b>",
    "notif_days_hint": "Tap a day to turn it on or off.\n✓ — day on\n✗ — day off\n\nWhen you're done, tap “Save”.",
    "notif_days_all": "All days",
    "notif_days_weekdays": "Weekdays (Mon–Fri)",
    "notif_days_save": "Save",
    "notif_days_saved": "✓ Days saved!",
    "notif_days_all_selected": "✓ All days selected",
    "notif_days_weekdays_selected": "✓ Weekdays selected (Mon–Fri)",
    "notif_days_none": "Pick at least one day.",

    "notif_toggle_on": "Reminders are on",
    "notif_toggle_off": "Reminders are off",

    "notif_message_btn_disable": "Turn off reminders",

    "day_mon": "Mon",
    "day_tue": "Tue",
    "day_wed": "Wed",
    "day_thu": "Thu",
    "day_fri": "Fri",
    "day_sat": "Sat",
    "day_sun": "Sun",

    "notif_btn_back": "Back to settings",

    "notif_default_name": "friend",

    "anchor_streak": "🔥 {days}",
    "notif_message_greeting": "<b>Time to practise, {name}!</b>",
    "notif_message_greeting_v2": "<b>{name}, a couple of minutes for words?</b>",
    "notif_message_greeting_v3": "<b>{name}, your words are waiting</b>",
    "notif_message_greeting_v4": "<b>Time for a lesson, {name}!</b>",
    "notif_message_greeting_v5": "<b>{name}, shall we continue?</b>",


    # ONE REASON TO COME BACK — and it has to be true
    "remind_streak_risk": "{days_word} in a row · not today yet",
    "remind_streak_risk_v2": "A {days_word} streak — today's lesson keeps it going",
    "remind_streak_risk_v3": "{days_word} in a row. One short lesson today and the streak grows",
    "remind_streak_risk_v4": "Don't lose your streak: {days_word} in a row, and no lesson yet today",
    "remind_due": "Words due for review: {count} — the bot keeps track of the timing",
    "remind_due_v2": "Words to review: {count}. Now is the right moment, before they fade",
    "remind_due_v3": "Words due for review: {count} — just right for one lesson",
    "remind_due_v4": "Today's review is scheduled — words: {count}",
    "remind_due_many": "Words are waiting for review — the lesson starts with them on its own. One lesson is enough; the rest can wait.",
    "remind_due_many_v2": "Quite a few words are due — the lesson picks the most important ones itself.",
    "remind_due_many_v3": "Reviews have piled up — one lesson today is enough, the rest can wait.",
    "day2_hook_words": "Yesterday you met {count} new words. Shall we check what stuck? It takes 2 minutes.",
    "day2_hook": "Yesterday you started learning words. Shall we check what stuck? It takes 2 minutes.",
    "remind_streak_lost": "Your best streak was {days_word}. A new one starts with a single lesson.",
    "remind_streak_lost_v2": "Your record is {days_word} in a row. Start a new streak today?",
    "remind_streak_lost_v3": "Your {days_word} record is still there. A new streak starts with one lesson.",
    "remind_milestone_close": "Words you're learning: {count} · {left} more to {target} — that's one lesson",
    "remind_milestone_close_v2": "{left} to go until {target} — one lesson and it's yours",
    "remind_milestone_close_v3": "Already {count} words in progress — {target} is close: {left} more",
    "remind_almost_learned": "You're one correct answer away from your first learned word. Words this close: {count}",
    "remind_almost_learned_v2": "Words one step from “learned”: {count}. One correct answer and your first learned word is yours.",
    "remind_almost_learned_v3": "Your first learned word is very close: one more correct review. Candidates: {count}",
    "remind_rank": "#{rank} of {total} in this month's ranking for this language",
    "remind_rank_v2": "You're {rank} of {total} in this month's ranking — one lesson can move you up",
    "remind_rank_v3": "This month's ranking: {rank} of {total}. Today you can climb",
    "remind_fact_1": "A word sticks when it comes back: after a day, three days, a week. The bot keeps the schedule.",
    "remind_fact_2": "An answer by ear is worth more: there's no written word to lean on.",
    "remind_fact_3": "Saying a word out loud is harder than recognising it — and worth three times as much.",
    "remind_fact_4": "Fifteen questions take about four minutes — less than a queue for coffee.",

    # ============================================================================
    # SETTINGS
    # ============================================================================
    "settings_title": "<b>Settings</b>",
    "settings_mode": "Mode: <b>{mode}</b>",
    "settings_language": "Bot language: <b>{language}</b>",

    "settings_btn_quiz_mode": "Level and topics",
    "settings_btn_change_language": "Interface language",
    "settings_btn_notifications": "Reminders",

    "settings_quiz_mode_line": "Level: <b>{mode}</b>",


    "settings_language_title": "<b>Interface language</b>",
    "settings_language_description": "Choose the bot interface language:",
    "start_pick_language": "Choose a language",

    "language_changed": "✓ Language changed to {language}",
    "user_not_found": "✗ Profile not found. Please send /start",

    "lang_ru": "Русский",
    "lang_uk": "Українська",
    "lang_en": "English",
    "lang_tr": "Türkçe",
    "lang_de": "Deutsch",
    "lang_pl": "Polski",



    # ============================================================================
    # QUIZ MODE (NEW)
    # ============================================================================
    "qmode_title": "<b>Level and topics</b>",
    "qmode_current": "Current: <b>{mode}</b>",
    "qmode_choose": "Choose how you want to learn.\nYou can switch at any time — your progress is saved.",

    "qmode_btn_level": "By level",
    "qmode_btn_category": "By topic",
    "qmode_btn_all": "All words",
    "qmode_btn_difficult": "Difficult words",

    "qmode_level_short": "{level}",
    "qmode_category_short": "{category}",
    "qmode_all_short": "All words",
    "qmode_difficult_short": "Difficult words",

    "qmode_level_title": "<b>Choose a level</b>",
    "qmode_level_desc": "From your first words to free-flowing conversation. All levels are open — pick yours.\n\n• A1–A2 — basic vocabulary\n• B1–B2 — confident communication\n• C1–C2 — fluent, nuanced language",
    "qmode_level_set": "✓ Mode: by level ({level})",

    "qmode_category_title": "<b>Choose a topic</b>",
    "qmode_category_desc": "From food to science — pick the topic you need.\n\nEach topic includes words from all levels.",
    "qmode_category_set": "✓ Topic: {category}",

    # Category names
    "cat_arbeit_beruf": "Work",
    "cat_bildung_lernen": "Education",
    "cat_einkaufen_geld": "Shopping",
    "cat_emotionen_charakter": "Emotions",
    "cat_essen_trinken": "Food",
    "cat_freizeit_sport": "Sport",
    "cat_gesundheit_medizin": "Health",
    "cat_grammatik": "Grammar",
    "cat_kleidung_mode": "Clothing",
    "cat_kommunikation": "Communication",
    "cat_kultur_kunst": "Culture",
    "cat_mensch_familie": "Family",
    "cat_natur_wetter": "Nature",
    "cat_recht_staat": "Law",
    "cat_reisen_transport": "Travel",
    "cat_technik_digital": "Technology",
    "cat_wirtschaft": "Economy",
    "cat_wissenschaft": "Science",
    "cat_wohnen_haus": "Housing",
    "cat_zeit_alltag": "Daily life",

    "qmode_all_set": "✓ Mode: all words",

    "qmode_difficult_set": "✓ Mode: difficult words",
    "qmode_difficult_few": "Difficult words so far: {count} — at least 4 needed.\nDo a few more lessons!",
    "qmode_difficult_empty": "No difficult words yet.\nDo a few lessons first!",

    "quiz_btn_change_mode": "Level and topics",
    "quiz_btn_report_error": "Report an error",
    "report_btn_confirm": "✓ Confirm ({count})",
    "report_btn_send": "Send",
    "report_no_words": "No words to report",
    "report_none_selected": "Select at least one word",
    "report_pick_kind": "Words selected: {count}. Now choose what's wrong: the translation or the pronunciation.",
    "report_sent": "✓ Reports sent: {count} — thank you!\nEach confirmed report earns +{points}.",
    "report_daily_limit": "You've reached today's limit of 20 reports.",
    "report_all_reported": "✓ All words from this lesson have already been reported",
    "report_already_sent": "✓ Already reported",
    "report_btn_kind_text": "Wrong translation",
    "report_btn_kind_audio": "Wrong pronunciation",
    "report_sent_audio": "✓ Reports sent: {count} — thank you!\nPronunciation reports are especially valuable: the automated check can't hear stress.\nEach confirmed report earns +{points}.",
    "report_approved": "✓ Your report on <b>{word}</b> was accepted — we'll fix the translation.\n+{points} points to your monthly score. Thank you — the dictionary gets better for everyone.",
    "award_won": "{mark} You finished #{rank} on the {month} leaderboard.\n{bonus} points added to your all-time score.",
    "report_approved_audio": "✓ Your pronunciation report on <b>{word}</b> was accepted.\nThe audio will be fixed. +{points} points to your monthly score — thank you.",

    # ============================================================================
    # QUIZ
    # ============================================================================
    "quiz_no_level": "Please choose your level first: /start",
    "quiz_error_generation": "✗ Something went wrong while preparing the lesson.\nPlease try again via /start",
    "quiz_no_words": "✗ Sorry, there are no words for this level.\nPlease try a different level.",

    "quiz_question_number": "{current} / {total}",

    "quiz_correct": "✓ <b>Correct</b>",
    "quiz_wrong": "✗ <b>Wrong</b>",
    "quiz_correct_answer": "Correct answer:",

    "quiz_btn_next": "Next →",

    "quiz_answer_already_counted": "Your answer has already been counted. Shall we continue?",
    "quiz_btn_repeat_errors": "Retry mistakes",

    "quiz_completed": "<b>Lesson complete</b>",
    "quiz_result_correct": "Correct: <b>{correct}/{total}</b>",
    "quiz_result_percentage": "Result: <b>{percentage}%</b>",
    "quiz_result_details": "<b>Details:</b>",
    "quiz_result_errors": "Mistakes: {count}",

    # PRAISE AT THE END OF A LESSON — only for what actually happened
    "praise_first_round": "First lesson done. From here words start coming back — that is how they stick.",
    "praise_first_learned": "First word learned: three correct answers in a row, none of them on the day you met it.",
    "praise_learned": "Words learned in this lesson: {count}",
    "praise_best_streak": "Personal best: {days_word} in a row",
    "praise_milestone": "You're now learning {count} words",
    "praise_first_speech": "First correct answer out loud",
    "praise_first_audio": "First correct answer by ear",
    "praise_comeback": "Welcome back! It's been {days_word}.",
    "praise_perfect": "A lesson without a single mistake",
    "praise_streak": "Streak: {days_word} in a row",
    "praise_freeze_saved": "You missed yesterday, but a streak freeze kept your streak: {days_word} in a row. The next freeze is available in a week.",
    "praise_streak_3": "Three days in a row — a habit is forming.",
    "praise_streak_7": "A whole week in a row! That's the key milestone: from here the habit holds itself.",
    "praise_streak_14": "Two weeks in a row — great pace.",
    "praise_streak_30": "A month in a row! That's a real habit now.",
    "praise_new_words": "New words: {count}",
    "praise_returned": "Recognised again: {count}",
    "praise_progress": "Words you're learning: {count} · {left} more to {target}",
    "praise_progress_top": "Words you're learning: {count}",
    "praise_points": "Points: +{points}",

    "quiz_repeat_title": "<b>Retry mistakes</b>",
    "quiz_no_errors": "✓ No mistakes this time!",
    "quiz_error_next": "✗ Couldn't load the next question.",

    # ============================================================================
    # STATISTICS
    # ============================================================================
    "stats_no_level": "<b>Choose your level first!</b>\n\nUse /start to begin.",





    # ============================================================================
    # HELP
    # ============================================================================
    "help_title": "<b>Help — GenauLingua</b>",
    "help_description": "How lessons work and how to reach the community.",
    "help_choose": "Choose a section:",

    "help_btn_how_to_use": "How to use",
    "help_btn_community": "Community",

    "help_how_to_use_title": "<b>How to use the bot</b>",


    "help_community_title": "<b>GenauLingua Community</b>",
    "help_community_text": """ <b>t.me/genaulingua_chat</b>

In the chat:
Be the first to know about updates
Found a bug — write or send a screenshot
Translation error — report it, we'll fix it
Ideas and suggestions — we read everything
Chat with other learners


The more active the community — the better the bot gets. Don't be shy! """,


    # ============================================================================
    # RATING
    # ============================================================================
    "rating_title_monthly": "<b>My rating — {month} {year}</b>",
    "rating_not_active": "✗ The rating isn't active yet.",
    "rating_not_in_ranking": "You're not in the ranking yet",
    "rating_start_quiz": "Take your first lesson!",
    "rating_join_by_lesson": "Your report points ({score}) are credited. Complete a lesson to join this month's ranking.",
    "release_notes_2026_10": "✨ <b>GenauLingua 2.0 — we rebuilt the bot from scratch</b>\n\n<b>Not just German.</b> Learn Ukrainian, English, Turkish, German, Polish or Russian — from any of them. The interface speaks all six too.\n\n<b>Six games instead of one.</b> It used to be just “pick the translation”.\n\nNow games alternate within each lesson:\n📖 I read · 💭 I recall · 🎧 I listen · 🎤 I speak · 🧩 Find the pairs · 🧱 I build\n\nIn “I speak” you answer by voice; in “I build” you put a sentence together — the bot shows which word is out of place.\n\n<b>The bot can talk.</b> Every word and example is read aloud in a natural voice.\n\n<b>A new look.</b> A new menu, a clean chat without clutter, a home screen with your skills, clear statistics, a new avatar and greeting.\n\n<b>The whole dictionary has been proofread</b> — all 12,902 words, translations and examples.\n\n<b>It adapts to you:</b> words come back just before you'd forget them, and the bot suggests the next level when things get easy.\n\n<b>Bugs fixed:</b> your day streak is counted correctly, and ranking points are fair — they reward effort. “Learned” is honest now too: a word counts as learned once you've got it right three times in a row on different days, and every word you've practised shows up under “Words you're learning”.\n\n<b>Reminders are on</b> — at your time. To change or turn them off: Settings → Bot → Reminders.\n\n⭐ Spotted a mistake? Report it right from the lesson summary: each confirmed report earns +15 points.\n\nYour progress and points are kept. Give it a try — a lesson takes a couple of minutes.",
    "rating_position": "Position: <b>#{rank}</b> of {total}",
    "rating_points": "Points: <b>{score}</b>",
    "rating_your_month": "<b>Your {month}:</b>",
    "rating_quizzes": "Lessons: {count}",
    "rating_words_learned": "Words learned: {count}",
    "rating_streak": "Streak: {days_word}",
    "rating_avg_result": "Average result: {percent}%",
    "rating_scoring_title": "<b>How to earn points:</b>",
    "rating_scoring_quiz": "• Lesson finished → +10",
    "rating_scoring_word": "• Word learned → +3",
    "rating_scoring_streak": "• Streak → each day in a row is worth more, up to +10",
    "rating_scoring_bonus": "• Accuracy above 60% → a bonus that grows with accuracy",
    "rating_scoring_report": "• Confirmed error report → +{points}",

    "rating_title_alltime": "<b>My rating — all time</b>",
    "rating_position_alltime": "Position: <b>#{rank}</b>",
    "rating_position_none": "Position: <b>—</b>",
    "rating_achievements": "<b>Your achievements:</b>",
    "rating_wins": "Wins (1st place): {count}",
    "rating_total_words": "Words learned: {count}",
    "rating_motivation_start": "Take a lesson in this language to join the ranking.",
    "rating_motivation_continue": "Keep going — a first win on the monthly leaderboard is within reach.",
    "rating_motivation_champion": "You're a true champion!",

    "table_title_monthly": "<b>Leaderboard — {month} {year}</b>",
    "table_title_alltime": "<b>Leaderboard — all time</b>",
    "table_empty": "No participants yet.\nBe the first to take a lesson!",
    "table_you_in_top": "You: <b>#{rank}</b> of {total}",
    "table_you_not_in_top": "You: <b>#{rank}</b> of {total} — {score}",
    "table_you_outside": "You: outside the top 10 — {score}",
    "table_you_not_ranked": "You're not ranked yet",
    "btn_leaderboard_table": "Leaderboard",
    "btn_back_to_rating": "Back to rating",
    "rating_tab_month": "Month",
    "rating_tab_alltime": "All time",

    "stats_header": "<b>Your statistics</b>",
    "stats_in_work_line": "Words you're learning: {count} · {left} more to {target}",
    "stats_in_work_top": "Words you're learning: {count}",
    "stats_details": "Learning: {progress}\nNew: {new}\nDifficult: {difficult}",
    "stats_achievements_title": "<b>Your achievements</b>",
    "stats_words_count": "Words learned: <b>{count}</b>",
    "stats_streak_line": "Streak: {days_word} in a row",
    "stats_best_streak_line": "Best streak: {days_word}",
    "stats_quizzes_header": "<b>Lessons · {level}</b>",
    "stats_quizzes_passed_line": "Completed: <b>{count}</b>",
    "stats_quizzes_avg_line": "Average result: <b>{percent}%</b>",
    "stats_quizzes_best_line": "Best result: <b>{percent}%</b>",
    "stats_quizzes_empty": "No lessons completed yet",
    "stats_recent_header": "<b>Recent lessons</b>",
    "stats_overall_header": "<b>Overall progress</b>",
    "stats_overall_learned": "Words learned: <b>{learned}</b> of {total}",
    "stats_explanation": "A word counts as learned after three correct answers in a row, on different days.",
}

# ============================================================================
# MULTILINGUAL: learning language, meaning language and direction
# ============================================================================
TEXTS.update({
    "langname_de": "German",
    "langname_en": "English",
    "langname_ru": "Russian",
    "langname_uk": "Ukrainian",
    "langname_tr": "Turkish",
    "langname_pl": "Polish",
    # Союз для перечисления языков в текстах помощи и приветствия
    "and_word": "and",

    "settings_learning_lang_line": "Learning: <b>{language}</b>",

    "settings_btn_learning_lang": "Language",

    "learning_lang_title": "<b>Language to learn</b>",
    "learning_lang_description": "Pick the language whose words you want to learn.\nProgress is tracked separately for each language.",
    "learning_lang_set": "✓ Learning: {language}",
    # Settings line and the audio screen
    "settings_audio_line": "Audio: <b>{state}</b>",
    "settings_btn_audio": "Audio",
    "audio_state_on": "on",
    "audio_state_off": "off",

    "audio_title": "<b>Audio</b>",
    "audio_description": "Words are read aloud by a natural-sounding AI voice. The question plays the word alone, the answer plays it with the example.",
    "audio_current_voice": "Voice: <b>{voice}</b>",
    "audio_btn_turn_on": "Turn audio on",
    "audio_btn_turn_off": "Turn audio off",
    "audio_btn_choose_voice": "Choose a voice",
    "audio_turned_on": "✓ Audio is on",
    "audio_turned_off": "Audio is off",

    "voice_title": "<b>Choose a voice</b>",
    "voice_description": "Tap a voice to hear it. The checkmark shows the current one.",
    "voice_male": "Male",
    "voice_female": "Female",
    "voice_set": "✓ Voice: {voice}",
    "voice_use": "Use {voice}",
    "voice_listening": "Playing {voice}",
    "voice_only_one": "For this language there is only one male and one female voice.",
    "voice_preview_failed": "Couldn't load a sample. Please try again.",
})


# ============================================================================
# АПГРЕЙД ПОД ШЕСТЬ ЯЗЫКОВ
#
# Добавлено, когда бот перестал быть «ботом для немецкого»: при первом запуске
# человек теперь выбирает не только язык интерфейса, но и какой язык учить, а
# подсказки направления стали работать на все тридцать пар вместо восьми.
# ============================================================================
TEXTS.update({
    "btn_rating": "Rating",
    "friend_fallback": "friend",
    "onboarding_learning_title": "<b>Which language will you learn?</b>",
    "onboarding_learning_desc": "Meanings will be shown in {native}.\nYou can change the language in settings at any time.",
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
    "help_how_to_use_text": "<b>Lesson</b>\n{words}, four options each. A lesson mixes five games: “I read”, “I recall”, “I listen”, “I speak” and the “Find the pairs” board. The bot remembers your mistakes and brings hard words back more often. After a lesson you can retry the ones you missed.\n\n<b>Audio</b>\nThe question plays the word; after your answer you hear the word with its example. Pick a male or female voice in settings.\n\n<b>Languages</b>\n{languages} — in any pair. Progress and rating are tracked separately for each language.\n\n\nA word counts as <b>learned</b> after three correct answers in a row, on different days.\nYour <b>streak</b> grows with every day you do at least one lesson.\nWrong translation or pronunciation? Use the “Report an error” button after the lesson.",
    "help_community_title": "<b>About the bot and the community</b>",
    "help_community_text": "<b>GenauLingua</b> — {language_count} languages in any pair: {languages}\n12,900 words A1–C2, each with an example and natural-sounding audio.\nInterface: {interface_languages}\n\n<b>t.me/genaulingua_chat</b>\nBugs, translation errors, ideas — we read everything. Pronunciation reports are especially welcome: a machine can't hear stress.",
})


# ============================================================================
# ВОПРОС НА СЛУХ
#
# Самого слова на экране нет — иначе слушать незачем. Варианты стоят на
# ИЗУЧАЕМОМ языке: спрашивают «что услышал», а не «что это значит».
# ============================================================================
TEXTS.update({
    "quiz_question_listen": "Listen and pick what you heard:",
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
    "rating_scoring_answer": "• Correct answer → +1, by ear → +2, out loud → +3",
    "rating_scoring_quiz": "• Lesson finished → +10",
    "rating_scoring_word": "• Word learned → +3",
    "rating_scoring_streak": "• Streak → each day in a row is worth more, up to +10",
    "rating_scoring_bonus": "• Accuracy above 60% → a bonus that grows with accuracy",
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
    "quiz_result_by_ear": "🎧 By ear: {count}",
})


# ============================================================================
# СОСТАВ ЗАНЯТИЯ
#
# Три канала — три РАЗНЫХ навыка, а не три оформления одного. Экран нужен,
# потому что до него колонка quiz_channels была недостижима: выключить
# вопросы на слух можно было только выключив озвучку целиком.
# ============================================================================
TEXTS.update({
    "settings_btn_channels": "Lesson games",
    "settings_channels_line": "Lesson: <b>{channels}</b>",
    "channels_title": "<b>Lesson games</b>",
    "channels_description": "Which games to mix into a lesson. A new word comes as an “I read” card; once you know it, it comes back in other games: recall it, hear it, say it, build a sentence with it. The more games, the better the word sticks.",
    "channel_text": "📖 I read",
    "channel_audio": "🎧 I listen",
    "channel_speech": "🎤 I speak",
    "channel_build": "🧱 I build",
    "home_scale_build": "I build",
    "quiz_result_built": "🧱 Built: {count}",
    "build_hint": "Build the sentence from the words below — some of them are extra",
    "build_btn_check": "Check",
    "build_full": "All places are filled. Remove a word with ⌫ or press “Check”.",
    "build_order_only": "↔ <b>Right words, different order</b>",
    "build_reference": "Correct:",
    "build_yours": "Your answer:",
    "build_extra": "Extra: {words}",
    "build_missing": "Missing: {words}",
    "stats_grammar_line": "Grammar: {correct} of {shown} correct",
    "quiz_result_recalled": "💭 Recalled: {count}",
    "home_scale_reverse": "I recall",
    "channel_reverse": "💭 I recall",
    "channels_text_always": "“I read” can't be switched off: every new word starts with it.",
    "channels_audio_blocked": "🎧 “I listen” and “I speak” are unavailable while audio is off.",
})


# ============================================================================
# ВОПРОС ВСЛУХ
#
# Ответ приходит голосовым сообщением, а не нажатием. Распознаватель отвечает
# на вопрос «то ли слово сказано», и только на него: качество произношения он
# судить не умеет — он обучен ПОНИМАТЬ акцент, а не замечать его.
# ============================================================================
TEXTS.update({
    "quiz_question_speak": "🎤 Say this word out loud — record a voice message: press and hold the microphone icon in the Telegram message field, bottom right",
    "speech_btn_reference": "Listen slowly",
    "speech_btn_skip": "Skip",
    "speech_listening": "🎧 Listening…",
    "speech_not_understood": "Couldn't make that out. Please record again — closer to the mic and a little louder.",
    "speech_try_again": "That sounded like “{heard}” — not quite. Please record it again: attempt {attempt} of {total}.",
    "speech_send_voice": "🎤 This question needs a voice message. Press and hold the microphone button.",
    "speech_skipped": "Skipped",
    "speech_not_counted": "Again it sounded like “{heard}”. This counts neither as right nor as a mistake — listen to how it sounds, and let's move on.",
    "lesson_expired": "This lesson was interrupted — the bot was updated or the lesson ended long ago. Start a new one with the button below.",
    "quiz_result_spoken": "🎤 Spoken: {count}",
})


# ============================================================================
# ДОМАШНИЙ ЭКРАН: ТРИ ШКАЛЫ
# ============================================================================
TEXTS.update({
    "home_scale_text": "I read",
    "home_scale_audio": "I listen",
    "home_scale_speech": "I speak",
    "home_btn_learn": "Learn words",
    "home_streak": "streak {days_word}",
    "home_rank": "rank {rank}",
    "home_hint": "",
    "home_channel_not_ready": "{channel}: not yet. Words ready: {ready}, at least {minimum} needed. Practise with “I read” cards — they unlock the other games.",
})


# ============================================================================
# НАСТРОЙКИ: ТРИ ГРУППЫ
#
# «Что учу» человек меняет часто, «как мне удобно» ставит один раз. Восемь
# равных пунктов перемешивали то и другое, и первым в списке стоял режим
# викторины, которым не пользуются 96%.
# ============================================================================
TEXTS.update({
    "settings_group_what": "What I learn",
    "settings_group_what_title": "<b>What I learn</b>",
    "settings_group_how": "How I learn",
    "settings_group_how_title": "<b>How I learn</b>",
    "settings_group_bot": "Bot",
    "settings_group_bot_title": "<b>Bot</b>",
    "settings_group_what_about": "Language, goal and level.",
    "settings_group_how_about": "What a lesson is made of and how it sounds.",
    "settings_group_bot_about": "Bot language, reminders and help.",
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
    "quiz_btn_one_more": "Another lesson",
    "home_btn_stats": "More details",
    "notif_off_how_to_return": "To turn it back on: Settings → Bot → Reminders",
    "reminder_offer": "Shall I remind you once a day? It makes it easier to keep what you've learnt — and your streak.",
    "reminder_offer_yes": "Yes, remind me",
    "reminder_offer_no": "No, thanks",
    "reminder_offer_done": "✓ Done: the reminder will arrive at <b>{time}</b> ({city}). You can adjust the time, days and time zone.",
    "reminder_offer_setup": "Adjust reminders",
    "level_offer": "You rarely make mistakes at <b>{current}</b>. Move up to <b>{following}</b>? Everything you've learnt stays with you.",
    "level_offer_yes": "Yes, move to {following}",
    "level_offer_no": "Stay here",
    "level_offer_done": "You're now at <b>{following}</b>. The words will be harder.",
    "level_offer_pick": "Looks like <b>{current}</b> is easy for you. Which level would you like to continue at? Everything you've learnt stays with you.",
    "level_offer_stay": "Stay at {current}",
    "level_down_offer": "There are quite a few mistakes at <b>{current}</b> for now. Move to <b>{previous}</b>? The words will be easier, and everything you've learnt stays with you.",
    "level_down_yes": "Yes, move to {previous}",
    "level_down_done": "You're now at <b>{previous}</b>. The words will be easier.",
})


# ============================================================================
# ЗАЧЕМ УЧИШЬ — ОПРОС, ВСТРОЕННЫЙ В ПЕРВОЕ НАЖАТИЕ
#
# Режим «по категории» работает, и им пользуются ТРИ человека из 233:
# он спрятан третьим уровнем настроек. Каждая кнопка здесь И отвечает
# на вопрос, И начинает первый круг — шага не прибавилось.
# ============================================================================
TEXTS.update({
    "goal_question": "What do you need the language for? We'll pick words to match.",
    "goal_work": "For work",
    "goal_travel": "For travel",
    "goal_living": "For living abroad",
    "goal_study": "For studying",
    "goal_any": "Just learn words",
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
    "intro_games": "Each word is learned through five games here: read it, recall it from the meaning, hear it, say it out loud and match it on the board.\nEach lesson mixes them for you.",
    "intro_numbers": "12,902 words · 20 topics · 6 levels\nSix languages in any pair: learn Polish through English if you like.",
    "intro_menu_settings": "language, lesson games, reminders",
    "intro_menu_stats": "your progress",
    "intro_menu_rating": "this month's leaderboard",
    "intro_menu_learn": "a lesson",
    "intro_menu_title": "What is where:",
})


# ============================================================================
# ЗАЧЕМ УЧУ — ЭКРАН НАСТРОЙКИ
#
# Без него цель осталась бы пустой навсегда у всех 233 нынешних
# пользователей: онбординг у них давно позади. Та же дыра, что была у
# состава занятия — колонка есть, экрана нет.
# ============================================================================
TEXTS.update({
    "settings_btn_goal": "Goal",
    "settings_goal_title": "<b>What I need it for</b>",
    "settings_goal_description": "Words from your topic will come first. Difficulty still follows your level, and what you've learnt keeps coming back for review.",
    "settings_goal_set": "Goal saved",
    "settings_goal_line": "Goal: <b>{goal}</b>",
    "settings_goal_none": "not chosen",
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
    "match_title": "<b>Find the pairs</b>",
    "match_progress": "Matched: {matched} of {total}",
    "match_errors": "✗ mistakes: {count}",
    "match_hint": "Tap a word on either side, then its pair on the other.",
    "match_wrong": "✗ Not a pair",
    "match_done": "<b>Board cleared!</b>",
    "match_done_counted": "Counted towards progress: {counted} of {total}. Only pairs matched on the first try count, and never the last one: by then there's no choice left.",
    "match_btn_again": "One more board",
    "match_not_ready": "Not yet: a board needs {need} familiar words, and you have {have}. Practise with “I read” cards — they unlock it.",
})

TEXTS["match_back_to_round"] = "Back to the lesson."

TEXTS.update({
    "settings_btn_match": "Board in the lesson",
    "settings_match_title": "<b>Board in the lesson</b>",
    "settings_match_description": "In every lesson, a board takes the place of one question halfway through: five words and five meanings to pair up. It uses only familiar words, so it appears once you have at least ten.",
    "match_state_on": "The board is on: it comes halfway through the lesson.",
    "settings_match_short_on": "with the board",
    "settings_channels_short_one": "“I read” only",
    "settings_channels_short_some": "{count} of {total} games",
    "settings_channels_short_all": "all games",
    "plural_words": "word|words",
    "plural_points": "point|points",
    "plural_days": "day|days",
    "settings_audio_short_off": "no sound",
    "settings_audio_short_on": "with sound",
    "settings_match_short_off": "no board",
    "match_state_off": "The board is off: the lesson is questions only.",
})
