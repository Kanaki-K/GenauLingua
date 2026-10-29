"""
Česká lokalizace pro GenauLingua Bot

Набор ключей совпадает с английской локалью (en.py), порядок тот же.
Обращение — только на «Vy» (заглавная в Vás/Vám/Váš). Прошедшее время
о самом человеке не используется: в чешском вежливое «jste se naučil /
naučila» требует рода, а род неизвестен — фразы построены без причастий.
"""

TEXTS = {
    # ============================================================================
    # HLAVNÍ MENU
    # ============================================================================
    "btn_learn_words": "Učit se slova",
    "btn_stats": "Statistiky",
    "btn_settings": "Nastavení",
    "btn_help": "Nápověda",
    "btn_back": "Zpět",
    "menu_placeholder": "Vyberte akci…",

    # ============================================================================
    # PŘIVÍTÁNÍ A START
    # ============================================================================
    "welcome_title": "<b>Dobrý den, {name}!</b>",








    # ============================================================================
    # PŘIPOMÍNKY
    # ============================================================================
    "notif_title": "<b>Připomínky</b>",
    "notif_status": "Stav: {status}",
    "notif_status_on": "zapnuté",
    "notif_status_off": "vypnuté",
    "notif_time": "Čas: {time}",
    "notif_days": "Dny: {days}",
    "notif_timezone": "Časové pásmo: {timezone}",
    "notif_hint": "Připomínka přijde ve zvolený čas podle Vašeho časového pásma.",
    "notif_hint_off": "Zapněte si připomínky — snáz udržíte svou sérii.",

    "notif_btn_toggle_on": "Připomínky: zapnuté",
    "notif_btn_toggle_off": "Připomínky: vypnuté",
    "notif_btn_time": "Čas: {time}",
    "notif_btn_days": "Vybrat dny",
    "notif_btn_timezone": "Změnit časové pásmo",

    "notif_timezone_title": "<b>Vaše časové pásmo</b>",
    "notif_timezone_current": "Teď: {timezone}",
    "notif_timezone_prompt": "Vyberte město ve svém časovém pásmu:",
    "notif_timezone_more": "Jiné město",
    "notif_timezone_back": "Zpět",
    "notif_timezone_set": "✓ Časové pásmo nastaveno: {city}",

    "notif_time_title": "<b>Čas připomínky</b>",
    "notif_time_current": "Nastavený čas: {time}",
    "notif_time_timezone": "Časové pásmo: {timezone}",
    "notif_time_hint": "Připomínka přijde v tento čas ve zvolené dny.",
    "notif_time_set": "✓ Čas nastaven: {time}",

    "notif_days_title": "<b>Dny připomínek</b>",
    "notif_days_hint": "Klepnutím na den ho zapnete nebo vypnete.\n✓ — den zapnutý\n✗ — den vypnutý\n\nNakonec klepněte na „Uložit“.",
    "notif_days_all": "Všechny dny",
    "notif_days_weekdays": "Pracovní dny (po–pá)",
    "notif_days_save": "Uložit",
    "notif_days_saved": "✓ Dny uloženy!",
    "notif_days_all_selected": "✓ Vybrány všechny dny",
    "notif_days_weekdays_selected": "✓ Vybrány pracovní dny (po–pá)",
    "notif_days_none": "Vyberte aspoň jeden den.",

    "notif_toggle_on": "Připomínky jsou zapnuté",
    "notif_toggle_off": "Připomínky jsou vypnuté",

    "day_mon": "Po",
    "day_tue": "Út",
    "day_wed": "St",
    "day_thu": "Čt",
    "day_fri": "Pá",
    "day_sat": "So",
    "day_sun": "Ne",

    "notif_btn_back": "Zpět do nastavení",

    "notif_default_name": "příteli",



    # JEDEN DŮVOD SE VRÁTIT — a musí být pravdivý

    # ============================================================================
    # NASTAVENÍ
    # ============================================================================
    "settings_title": "<b>Nastavení</b>",
    "settings_mode": "Režim: <b>{mode}</b>",
    "settings_language": "Jazyk bota: <b>{language}</b>",

    "settings_btn_quiz_mode": "Úroveň a témata",
    "settings_btn_change_language": "Jazyk bota",
    "settings_btn_notifications": "Připomínky",

    "settings_quiz_mode_line": "Úroveň: <b>{mode}</b>",
    "start_pick_language": "Vyberte svůj jazyk",
    "onboard_your_lang": "✓ Váš jazyk: {language}",
    "onboard_change_hint": "Změnit ho můžete kdykoli: příkaz /language.",
    "onboard_phone_hint": "Váš Telegram je v češtině. Pokud byl jazyk zvolen omylem, klepněte na „{back}“.",
    "lang_confirm_learning": "Učíte se: {language}",
    "lang_progress_kept": "Pokrok v každém jazyce zůstává uložen.",
    "btn_done": "Hotovo",
    "btn_change_learning": "Změnit jazyk, který se učím",
    "intro_pair": "Učíte se {learning} s překladem do {native}.",
    "intro_menu_language": "jazyk bota",
    "plural_languages": "jazyk|jazyky|jazyků",
    "cmd_start": "Začátek a co bot umí",
    "cmd_language": "Jazyk bota",
    "cmd_settings": "Nastavení",
    "cmd_help": "Nápověda",

    "language_changed": "✓ Jazyk změněn na {language}",
    "user_not_found": "✗ Profil nebyl nalezen. Pošlete prosím /start",

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
    # REŽIM KVÍZU (NOVÝ)
    # ============================================================================
    "qmode_title": "<b>Úroveň a témata</b>",
    "qmode_current": "Teď: <b>{mode}</b>",
    "qmode_choose": "Vyberte, jak se chcete učit.\nZměnit to můžete kdykoli — Váš pokrok zůstane.",

    "qmode_btn_level": "Podle úrovně",
    "qmode_btn_category": "Podle tématu",
    "qmode_btn_all": "Všechna slova",
    "qmode_btn_difficult": "Těžká slova",

    "qmode_level_short": "{level}",
    "qmode_category_short": "{category}",
    "qmode_all_short": "Všechna slova",
    "qmode_difficult_short": "Těžká slova",

    "qmode_level_title": "<b>Vyberte úroveň</b>",
    "qmode_level_desc": "Od prvních slov až po volnou konverzaci. Všechny úrovně jsou otevřené — vyberte si tu svou.\n\n• A1–A2 — základní slovní zásoba\n• B1–B2 — jistá komunikace\n• C1–C2 — plynulý a bohatý jazyk",
    "qmode_level_set": "✓ Režim: podle úrovně ({level})",

    "qmode_category_title": "<b>Vyberte téma</b>",
    "qmode_category_desc": "Od jídla po vědu — vyberte téma, které potřebujete.\n\nKaždé téma obsahuje slova ze všech úrovní.",
    "qmode_category_set": "✓ Téma: {category}",

    # Názvy kategorií
    "cat_arbeit_beruf": "Práce",
    "cat_bildung_lernen": "Vzdělání",
    "cat_einkaufen_geld": "Nakupování",
    "cat_emotionen_charakter": "Emoce",
    "cat_essen_trinken": "Jídlo",
    "cat_freizeit_sport": "Sport",
    "cat_gesundheit_medizin": "Zdraví",
    "cat_grammatik": "Gramatika",
    "cat_kleidung_mode": "Oblečení",
    "cat_kommunikation": "Komunikace",
    "cat_kultur_kunst": "Kultura",
    "cat_mensch_familie": "Rodina",
    "cat_natur_wetter": "Příroda",
    "cat_recht_staat": "Právo",
    "cat_reisen_transport": "Cestování",
    "cat_technik_digital": "Technika",
    "cat_wirtschaft": "Ekonomika",
    "cat_wissenschaft": "Věda",
    "cat_wohnen_haus": "Bydlení",
    "cat_zeit_alltag": "Všední den",

    "qmode_all_set": "✓ Režim: všechna slova",

    "qmode_difficult_set": "✓ Režim: těžká slova",
    "qmode_difficult_few": "Těžkých slov zatím: {count} — potřeba jsou aspoň 4.\nUdělejte ještě pár lekcí!",
    "qmode_difficult_empty": "Zatím žádná těžká slova.\nNejdřív udělejte pár lekcí!",

    "quiz_btn_change_mode": "Úroveň a témata",
    "quiz_btn_report_error": "Nahlásit chybu",
    "report_btn_confirm": "✓ Potvrdit ({count})",
    "report_btn_send": "Odeslat",
    "report_kind_text": "Překlad",
    "report_kind_example": "Příklad",
    "report_kind_audio": "Výslovnost",
    "report_pick_hint": "Co je špatně? Označte to a stiskněte „Odeslat“",
    "report_btn_sent": "✓ Hlášení odesláno",
    "report_sent_one": "✓ Děkujeme!\nPokud se chyba potvrdí, získáte +{points}.",
    "report_approved_example": "✓ Vaše hlášení k příkladu u slova <b>{word}</b> bylo přijato\n\nPříklad opravíme\n\nDo skóre měsíce připisujeme +{points} bodů - děkujeme",
    "report_no_words": "Žádná slova k nahlášení",
    "report_none_selected": "Vyberte aspoň jedno slovo",
    "report_pick_kind": "Vybraná slova: {count}. Teď zvolte, co je špatně: překlad, nebo výslovnost.",
    "report_sent": "✓ Odeslaná hlášení: {count} — děkujeme!\nKaždé potvrzené hlášení přinese +{points}.",
    "report_daily_limit": "Dnešní limit 20 hlášení je vyčerpán.",
    "report_all_reported": "✓ Všechna slova z této lekce už jsou nahlášená",
    "report_already_sent": "✓ Už nahlášeno",
    "report_btn_kind_text": "Špatný překlad",
    "report_btn_kind_audio": "Špatná výslovnost",
    "report_sent_audio": "✓ Odeslaná hlášení: {count} — děkujeme!\nHlášení k výslovnosti jsou obzvlášť cenná: automatická kontrola neslyší přízvuk.\nKaždé potvrzené hlášení přinese +{points}.",
    "report_approved": "✓ Vaše hlášení ke slovu <b>{word}</b> bylo přijato - překlad opravíme\n\nDo skóre měsíce připisujeme +{points} bodů. Děkujeme - slovník bude lepší pro všechny",
    "award_won": "{mark} {month}: {rank}. místo v žebříčku měsíce\n\nK celkovému skóre připsáno bodů: {bonus}",
    "report_approved_audio": "✓ Vaše hlášení k výslovnosti slova <b>{word}</b> bylo přijato\n\nNahrávku opravíme\n\nDo skóre měsíce připisujeme +{points} bodů - děkujeme",
    # ============================================================================
    # KVÍZ
    # ============================================================================
    "quiz_no_level": "Nejdřív prosím vyberte úroveň: /start",
    "quiz_error_generation": "✗ Při přípravě lekce se něco pokazilo.\nZkuste to prosím znovu přes /start",
    "quiz_no_words": "✗ Pro tuto úroveň bohužel nejsou žádná slova.\nZkuste prosím jinou úroveň.",

    "quiz_question_number": "{current} / {total}",

    "quiz_correct": "✓ <b>Správně</b>",
    "quiz_wrong": "✗ <b>Špatně</b>",
    "quiz_correct_answer": "Správná odpověď:",

    "quiz_btn_next": "Dál →",

    "quiz_answer_already_counted": "Vaše odpověď už je započítaná. Pokračujeme?",
    "quiz_btn_repeat_errors": "Zopakovat chyby",
    "lesson_resume_prompt": 'Máte nedokončenou lekci: {done} z {total}',
    "btn_lesson_resume": 'Pokračovat',
    "btn_lesson_new": 'Začít novou',
    "speech_offer_text": 'Mluvit nahlas teď nejde? Nevadí. Odebrat „Mluvím“ z lekcí? Vrátit to můžete kdykoli v nastavení',
    "btn_speech_off": 'Odebrat „Mluvím“',
    "btn_speech_keep": 'Ponechat',
    "speech_off_done": 'Hotovo, „Mluvím“ je odebráno. Vrátit to můžete v nastavení',
    "speech_invite_text": '🎤 Chcete zkusit odpovídat nahlas? Bot si poslechne Vaši výslovnost a poradí, když něco nebude sedět. Je to dobrovolné',
    "btn_speech_try": 'Vyzkoušet',
    "btn_speech_later": 'Teď ne',
    "speech_try_done": 'Skvělé! „Mluvím“ se objeví v dalších lekcích. Pro odpověď podržte ikonu mikrofonu vpravo dole a řekněte slovo',

    "quiz_completed": "<b>Lekce dokončena</b>",
    "quiz_result_correct": "Správně: <b>{correct}/{total}</b>",
    "quiz_result_percentage": "Výsledek: <b>{percentage}%</b>",
    "quiz_result_details": "<b>Podrobnosti:</b>",
    "quiz_result_errors": "Chyby: {count}",

    # CHVÁLA NA KONCI LEKCE — jen za to, co se opravdu stalo
    "praise_first_round": "První lekce je hotová. Odteď se slova začnou vracet — tak se ukládají do paměti.",
    "praise_first_learned": "První naučené slovo: tři správné odpovědi za sebou, ani jedna v den prvního setkání.",
    "praise_learned": "Naučená slova v této lekci: {count}",
    "praise_best_streak": "Osobní rekord: {days_word} v řadě",
    "praise_milestone": "Slova v učení: už {count}",
    "praise_first_speech": "První správná odpověď nahlas",
    "praise_first_audio": "První správná odpověď poslechem",
    "praise_comeback": "Vítejte zpět! Přestávka trvala {days_word}.",
    "praise_perfect": "Lekce bez jediné chyby",
    "praise_streak": "Série: {days_word} v řadě",
    "praise_freeze_saved": "Včera byla přestávka, ale díky ochraně série pokračuje: {days_word} v řadě. Další ochrana bude k dispozici za týden.",
    "praise_streak_3": "Tři dny v řadě — rodí se zvyk.",
    "praise_streak_7": "Celý týden v řadě! To je klíčový milník: odteď se zvyk drží sám.",
    "praise_streak_14": "Dva týdny v řadě — skvělé tempo.",
    "praise_streak_30": "Měsíc v řadě! To už je skutečný zvyk.",
    "praise_new_words": "Nová slova: {count}",
    "praise_returned": "Znovu poznaná: {count}",
    "praise_progress": "Slova v učení: {count} · do {target} zbývá {left}",
    "praise_progress_top": "Slova v učení: {count}",
    "praise_points": "Body: +{points}",

    "quiz_repeat_title": "<b>Opakování chyb</b>",
    "quiz_no_errors": "✓ Tentokrát bez chyb!",
    "quiz_error_next": "✗ Další otázku se nepodařilo načíst.",

    # ============================================================================
    # STATISTIKY
    # ============================================================================
    "stats_no_level": "<b>Nejdřív si vyberte úroveň!</b>\n\nZačněte příkazem /start.",





    # ============================================================================
    # NÁPOVĚDA
    # ============================================================================
    "help_title": "<b>Nápověda — GenauLingua</b>",
    "help_description": "Jak fungují lekce a jak se spojit s komunitou.",
    "help_choose": "Vyberte sekci:",

    "help_btn_how_to_use": "Jak na to",
    "help_btn_community": "Komunita",

    "help_how_to_use_title": "<b>Jak používat bota</b>",


    "help_community_title": "<b>Komunita GenauLingua</b>",
    "help_community_text": """ <b>t.me/genaulingua_chat</b>

V chatu:
O novinkách se dozvíte jako první
Našla se chyba — napište nebo pošlete snímek obrazovky
Chyba v překladu — nahlaste ji, opravíme
Nápady a návrhy — čteme všechno
Povídání s dalšími studenty


Čím aktivnější komunita, tím lepší bot. Nebojte se ozvat! """,


    # ============================================================================
    # ŽEBŘÍČEK
    # ============================================================================
    "rating_not_active": "✗ Žebříček zatím není aktivní.",
    "rating_not_in_ranking": "Zatím nejste v žebříčku",
    "rating_start_quiz": "Udělejte svou první lekci!",
    "rating_join_by_lesson": "Body za hlášení ({score}) jsou připsané. Dokončete lekci a zařaďte se do žebříčku tohoto měsíce.",
    "release_notes_2026_10": "✨ <b>GenauLingua 2.0 — bota jsme postavili znovu od základu</b>\n\n<b>Nejen němčina.</b> Učte se ukrajinsky, anglicky, turecky, německy, polsky nebo rusky — z kteréhokoli z těchto jazyků. Rozhraní mluví také všemi šesti.\n\n<b>Šest her místo jedné.</b> Dřív bylo jen „vyberte překlad“.\n\nTeď se hry v každé lekci střídají:\n📖 Čtu · 💭 Vybavuji si · 🎧 Poslouchám · 🎤 Mluvím · 🧩 Najděte dvojice · 🧱 Skládám\n\nV „Mluvím“ odpovídáte hlasem, ve „Skládám“ skládáte větu — bot ukáže, které slovo je na špatném místě.\n\n<b>Bot mluví.</b> Každé slovo i příklad zazní přirozeným hlasem.\n\n<b>Nový vzhled.</b> Nové menu, čistý chat bez zbytečností, domovská obrazovka s Vašimi dovednostmi, přehledné statistiky, nový avatar a pozdrav.\n\n<b>Celý slovník prošel korekturou</b> — všech 12 902 slov, překladů a příkladů.\n\n<b>Přizpůsobí se Vám:</b> slova se vracejí těsně předtím, než by se zapomněla, a když je to snadné, bot nabídne další úroveň.\n\n<b>Opravené chyby:</b> série dní se počítá správně a body v žebříčku jsou férové — odměňují úsilí. I „naučené“ je teď poctivé: slovo je naučené po třech správných odpovědích za sebou v různých dnech a každé procvičené slovo najdete v řádku „Slova v učení“.\n\n<b>Připomínky jsou zapnuté</b> — ve Vámi zvolený čas. Změnit nebo vypnout: Nastavení → Bot → Připomínky.\n\n⭐ Chyba ve slovníku? Nahlaste ji přímo ze shrnutí lekce: každé potvrzené hlášení přinese +15 bodů.\n\nVáš pokrok i body zůstávají. Vyzkoušejte to — lekce zabere pár minut.",
    "release_notes_2026_10_22": '✨ <b>GenauLingua 2.2 - teď deset jazyků</b>\n\nDobrý den!\n\nVyšla velká aktualizace:\n\n<b>4 nové jazyky</b>\n\n🇮🇹 Italština, 🇪🇸 španělština, 🇫🇷 francouzština a 🇨🇿 čeština - můžete se je učit z kteréhokoli jazyka bota\nKaždý má přes 12 000 slov s příklady, vše namluvené\n\n<b>Žebříček, ve kterém je o co bojovat</b>\n\nMedaile měsíce 🥇🥈🥉, koruna 👑 pro nejlepšího z těch, kdo se učí Váš jazyk, a hodnosti, které rostou s Vámi. První výsledky podle nových pravidel - 1. listopadu\n\n<b>Série odpouští vynechaný den</b>\n\nJednou týdně ochrana série 🧊 zachrání Vaši sérii, když vynecháte den\n\n<b>A ještě:</b> hlášení chyby v překladu, příkladu nebo nahrávce - přímo pod odpovědí (+15 bodů za potvrzené)\n\nZnámá slova se naučíte rychleji a aktualizace bota už nepřeruší lekci\n\nDěkujeme, že se učíte s námi a hlásíte chyby - díky tomu je bot lepší pro všechny 💙\n\nVše nové stručně a přehledně: <a href="{url}">co je nového ve verzi 2.2</a>',
    "release_notes_2026_11": "✨ <b>GenauLingua 2.3 - nové hry a aktualizovaný slovník</b>\n\nDobrý den!\n\nVyšla velká aktualizace:\n\n<b>Slovník je celý zkontrolovaný</b>\n\nKaždé slovo a příklad ve všech 10 jazycích: přesnější překlady, srozumitelnější příklady, sprostá slova jsou pryč. Všechno je znovu namluvené - ženským i mužským hlasem\n\n<b>Dvě nové hry</b>\n\n✍️ Napište slovo sami - bot podtrhne chybu\n🇩🇪 der, die, nebo das - vyberte člen slova, které znáte\n\n<b>Hádat je těžší</b>\n\nMezi možnostmi jsou teď podobná slova. A slovo, které si dvakrát spletete, se vrátí k opakování\n\n<b>A ještě:</b> novým studentům bot sám určí úroveň podle prvních 8 slov a všechna Vaše hlášení chyb jsme zohlednili\n\nDěkujeme, že se učíte s námi 💙\n\nVšechno nové stručně a názorně: <a href=\"{url}\">co je nového ve verzi 2.3</a>",
    "btn_release_news": 'Co je nového →',


    "table_empty": "Zatím tu nikdo není.\nUdělejte lekci jako první!",
    "table_you_not_ranked": "Zatím nejste v žebříčku",
    "rating_tab_month": "Měsíc",
    "rating_tab_alltime": "Celkově",
    "rating_crown_rule": "První místo získá korunu na celý další měsíc",
    "rating_screen_title": "<b>Pořadí · {month} {year}</b>",
    "rating_screen_title_alltime": "<b>Pořadí · celkově</b>",
    "rating_you": "<b>Vy: #{rank} z {total}</b> · {points}",
    "rating_results_in": "Výsledky měsíce za {days}",
    "info_title": "<b>Jak funguje pořadí</b>",
    "info_month": "<b>Měsíc</b> — všichni. Tři nejlepší získají 🥇 🥈 🥉 (od 3 lekcí).",
    "info_lang": "<b>Jazyk</b> — ti, kdo se učí Váš jazyk. První získá 👑 na další měsíc.",
    "info_alltime": "<b>Celkově</b> — všechny body. Medaile zvyšují hodnost 🌱 🌳 🌙 🪐 ☀️",
    "info_points_title": "<b>Body</b>",
    "info_points": "Odpověď +1 · poslechem +2 · nahlas +3\nLekce +10 · naučené slovo +3\nDny v řadě — až +10 · přesnost nad 60% — bonus\nPotvrzené hlášení +{points}",
    "title_sprout": "Klíček",
    "title_tree": "Strom",
    "title_moon": "Měsíc",
    "title_planet": "Planeta",
    "title_sun": "Slunce",
    "title_galaxy": "Galaxie",
    "btn_rating_info": "Info",
    "card_medal_need": "Lekcí potřebných pro medaili: {need} · Vy máte {have}",
    "card_crown_small": "O korunu se hraje, když má jazyk 3+ lidi se 3+ lekcemi",
    "summary_place": "↑ Místo v měsíci: {rank}",
    "summary_gap": "{name} je o {gap} před Vámi",
    "summary_record": "Nový rekord měsíce: {points}",
    "collection_title": "<b>Sbírka</b> · odemčeno {open} z {total}",
    "collection_locked": "▫️ ???",
    "ach_streak_7": "Série 7 dní",
    "ach_streak_30": "Série 30 dní",
    "ach_streak_100": "Série 100 dní",
    "ach_streak_365": "Série 365 dní",
    "ach_streak_1000": "Série 1000 dní",
    "ach_words_100": "100 naučených slov",
    "ach_words_1000": "1000 naučených slov",
    "ach_words_3000": "3000 naučených slov",
    "ach_perfect_10": "10 lekcí bez chyby",
    "ach_voice_1000": "1000 správných odpovědí nahlas",
    "ach_editor": "Redaktor slovníku: 5 přijatých hlášení",
    "ach_polyglot": "Polyglot: 100 slov ve dvou jazycích",
    "award_month_header": "<b>Výsledky měsíce</b>",
    "award_crown": "👑 Koruna — {language}: jste nejlepší z těch, kdo se tento jazyk učí. Noste ji celý další měsíc",
    "award_glory": "+{glory} slávy",
    "award_new_title": "Nová hodnost: {mark} {name}",
    "nd_overtaken": "V měsíčním žebříčku Vás někdo předběhl.\nVaše místo: {rank} · {name} je o {gap} před Vámi.",
    "nd_finish": "Do konce měsíce: {days}.\nVaše místo: {rank} · k medaili chybí {gap}.",

    "stats_header": "<b>Vaše statistiky</b>",
    "stats_in_work_line": "Slova v učení: {count} · do {target} zbývá {left}",
    "stats_in_work_top": "Slova v učení: {count}",
    "stats_details": "V učení: {progress}\nNová: {new}\nTěžká: {difficult}",
    "stats_achievements_title": "<b>Vaše úspěchy</b>",
    "stats_words_count": "Naučená slova: <b>{count}</b>",
    "stats_best_streak_line": "Nejlepší série: {days_word}",
    "stats_quizzes_header": "<b>Lekce · {level}</b>",
    "stats_quizzes_passed_line": "Dokončeno: <b>{count}</b>",
    "stats_quizzes_avg_line": "Průměrný výsledek: <b>{percent}%</b>",
    "stats_quizzes_best_line": "Nejlepší výsledek: <b>{percent}%</b>",
    "stats_quizzes_empty": "Zatím žádné dokončené lekce",
    "stats_recent_header": "<b>Poslední lekce</b>",
    "stats_explanation": "Slovo je naučené po třech správných odpovědích za sebou, v různých dnech.",
}

# ============================================================================
# VÍCEJAZYČNOST: jazyk učení, jazyk významů a směr
# ============================================================================
TEXTS.update({
    "langname_de": "Němčina",
    "langname_en": "Angličtina",
    "langname_ru": "Ruština",
    "langname_uk": "Ukrajinština",
    "langname_tr": "Turečtina",
    "langname_pl": "Polština",
    "langname_it": "Italština",
    "langname_es": "Španělština",
    "langname_fr": "Francouzština",
    "langname_cs": "Čeština",
    # Союз для перечисления языков в текстах помощи и приветствия
    "and_word": "a",

    "settings_learning_lang_line": "Učím se: <b>{language}</b>",

    "settings_btn_learning_lang": "Jazyk",

    "learning_lang_title": "<b>Jazyk k učení</b>",
    "learning_lang_description": "Vyberte jazyk, jehož slova se chcete učit.\nPokrok se počítá zvlášť pro každý jazyk.",
    "learning_lang_set": "✓ Učím se: {language}",
    # Řádek v nastavení a obrazovka zvuku
    "settings_audio_line": "Zvuk: <b>{state}</b>",
    "settings_btn_audio": "Zvuk",
    "audio_state_on": "zapnutý",
    "audio_state_off": "vypnutý",

    "audio_title": "<b>Zvuk</b>",
    "audio_description": "Slova čte přirozeně znějící hlas AI. V otázce zazní samotné slovo, v odpovědi slovo i s příkladem.",
    "audio_current_voice": "Hlas: <b>{voice}</b>",
    "audio_btn_turn_on": "Zapnout zvuk",
    "audio_btn_turn_off": "Vypnout zvuk",
    "audio_btn_choose_voice": "Vybrat hlas",
    "audio_turned_on": "✓ Zvuk je zapnutý",
    "audio_turned_off": "Zvuk je vypnutý",

    "voice_title": "<b>Vyberte hlas</b>",
    "voice_description": "Klepnutím si hlas poslechnete. Zaškrtnutí ukazuje ten aktuální.",
    "voice_male": "Mužský",
    "voice_female": "Ženský",
    "voice_set": "✓ Hlas: {voice}",
    "voice_use": "Zvolit: {voice}",
    "voice_listening": "Přehrávám: {voice}",
    "voice_only_one": "Pro tento jazyk je k dispozici jen jeden mužský a jeden ženský hlas.",
    "voice_preview_failed": "Ukázku se nepodařilo načíst. Zkuste to prosím znovu.",
})


# ============================================================================
# АПГРЕЙД ПОД ШЕСТЬ ЯЗЫКОВ
#
# Добавлено, когда бот перестал быть «ботом для немецкого»: при первом запуске
# человек теперь выбирает не только язык интерфейса, но и какой язык учить, а
# подсказки направления стали работать на все тридцать пар вместо восьми.
# ============================================================================
TEXTS.update({
    "btn_rating": "Pořadí",
    "friend_fallback": "příteli",
    "onboarding_learning_title": "<b>Jaký jazyk se budete učit?</b>",
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
    "help_how_to_use_text": "<b>Lekce</b>\n{words}, u každého čtyři možnosti. Lekce střídá šest her: „Čtu“, „Vybavuji si“, „Poslouchám“, „Mluvím“, „Skládám“ a „Najděte dvojice“. Bot si pamatuje Vaše chyby a těžká slova vrací častěji. Po lekci můžete zopakovat ta, ve kterých byla chyba.\n\n<b>Zvuk</b>\nV otázce zazní slovo, po odpovědi slovo i s příkladem. Mužský nebo ženský hlas si vyberete v nastavení.\n\n<b>Jazyky</b>\n{languages} — v libovolné dvojici. Pokrok se počítá zvlášť pro každý jazyk; žebříček má záložky „Měsíc“, „Celkově“ a „Jazyk“.\n\n\nSlovo je <b>naučené</b> po třech správných odpovědích za sebou, v různých dnech. Když nové slovo uhodnete hned napoprvé, stačí ještě jedna správná odpověď.\n<b>Série</b> roste s každým dnem, kdy uděláte aspoň jednu lekci. Jeden vynechaný den v týdnu ji nepřeruší — pokryje ho ochrana série.\nŠpatný překlad nebo výslovnost? Použijte tlačítko „Nahlásit chybu“ pod odpovědí.",
    "help_community_title": "<b>O botovi a komunitě</b>",
    "help_community_text": "<b>GenauLingua</b> — {language_count} jazyků v libovolné dvojici: {languages}\n12 900 slov A1–C2, každé s příkladem a přirozeně znějící výslovností.\nRozhraní: {interface_languages}\n\n<b>t.me/genaulingua_chat</b>\nChyby, špatné překlady, nápady — čteme všechno. Hlášení k výslovnosti jsou obzvlášť vítaná: stroj neslyší přízvuk.",
})


# ============================================================================
# ВОПРОС НА СЛУХ
#
# Самого слова на экране нет — иначе слушать незачем. Варианты стоят на
# ИЗУЧАЕМОМ языке: спрашивают «что услышал», а не «что это значит».
# ============================================================================
TEXTS.update({
    "quiz_question_listen": "Poslechněte si a vyberte, co zaznělo:",
    "quiz_question_article": "Jaký člen má toto slovo? Klepněte na der, die nebo das 👇🏻",
    "quiz_question_type": "Napište toto slovo zprávou do chatu 👇🏻",
    "quiz_typed_skip": "Nepamatuji si",
    "quiz_typed_typo": "✓ <b>Správně</b>, ale s překlepem",
    "quiz_typed_marked": "Chyba je podtržená",
    "quiz_typed_right": "Správně se píše:",
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
    "quiz_result_by_ear": "🎧 Poslechem: {count}",
})


# ============================================================================
# СОСТАВ ЗАНЯТИЯ
#
# Три канала — три РАЗНЫХ навыка, а не три оформления одного. Экран нужен,
# потому что до него колонка quiz_channels была недостижима: выключить
# вопросы на слух можно было только выключив озвучку целиком.
# ============================================================================
TEXTS.update({
    "settings_btn_channels": "Hry v lekci",
    "settings_channels_line": "Lekce: <b>{channels}</b>",
    "channels_title": "<b>Hry v lekci</b>",
    "channels_description": "Které hry míchat do lekce. Nové slovo přichází jako karta „Čtu“; jakmile ho znáte, vrací se v dalších hrách: vybavit si ho, slyšet ho, říct ho, postavit s ním větu. Čím víc her, tím lépe se slovo usadí v paměti.",
    "channel_text": "📖 Čtu",
    "channel_audio": "🎧 Poslouchám",
    "channel_speech": "🎤 Mluvím",
    "channel_build": "🧱 Skládám",
    "home_scale_build": "Skládám",
    "quiz_result_built": "🧱 Složeno: {count}",
    "build_hint": "Složte větu ze slov níže — některá jsou navíc",
    "build_btn_check": "Zkontrolovat",
    "build_full": "Všechna místa jsou obsazená. Odeberte slovo tlačítkem ⌫ nebo stiskněte „Zkontrolovat“.",
    "build_order_only": "↔ <b>Správná slova, jiné pořadí</b>",
    "build_reference": "Správně:",
    "build_yours": "Vaše odpověď:",
    "build_extra": "Navíc: {words}",
    "build_missing": "Chybí: {words}",
    "stats_grammar_line": "Gramatika: správně {correct} z {shown}",
    "quiz_result_recalled": "💭 Vybaveno: {count}",
    "home_scale_reverse": "Vybavuji si",
    "channel_reverse": "💭 Vybavuji si",
    "channels_text_always": "„Čtu“ vypnout nejde: každé nové slovo začíná právě tady.",
    "channels_audio_blocked": "🎧 „Poslouchám“ a „Mluvím“ nejsou dostupné, dokud je zvuk vypnutý.",
})


# ============================================================================
# ВОПРОС ВСЛУХ
#
# Ответ приходит голосовым сообщением, а не нажатием. Распознаватель отвечает
# на вопрос «то ли слово сказано», и только на него: качество произношения он
# судить не умеет — он обучен ПОНИМАТЬ акцент, а не замечать его.
# ============================================================================
TEXTS.update({
    "quiz_question_speak": "🎤 Řekněte toto slovo nahlas — nahrajte hlasovou zprávu: podržte ikonu mikrofonu v poli pro zprávu v Telegramu, vpravo dole",
    "speech_btn_reference": "Poslechnout pomalu",
    "speech_btn_skip": "Přeskočit",
    "speech_listening": "🎧 Poslouchám…",
    "speech_not_understood": "Nepodařilo se to rozpoznat. Nahrajte to prosím znovu — blíž k mikrofonu a o něco hlasitěji.",
    "speech_try_again": "Znělo to jako „{heard}“ — ještě ne úplně. Nahrajte to prosím znovu: pokus {attempt} z {total}.",
    "speech_send_voice": "🎤 Na tuto otázku se odpovídá hlasovou zprávou. Podržte tlačítko mikrofonu.",
    "speech_skipped": "Přeskočeno",
    "speech_not_counted": "Zase to znělo jako „{heard}“. Nepočítá se to ani jako správně, ani jako chyba — poslechněte si, jak to zní, a jdeme dál.",
    "lesson_expired": "Tato lekce byla přerušena — bot se aktualizoval nebo lekce skončila už dávno. Začněte novou tlačítkem níže.",
    "quiz_result_spoken": "🎤 Nahlas: {count}",
})


# ============================================================================
# ДОМАШНИЙ ЭКРАН: ТРИ ШКАЛЫ
# ============================================================================
TEXTS.update({
    "home_scale_text": "Čtu",
    "home_scale_audio": "Poslouchám",
    "home_scale_speech": "Mluvím",
    "home_btn_learn": "Učit se slova",
    "home_rank": "místo {rank}",
    "home_hint": "",
    "home_channel_not_ready": "{channel}: zatím ne. Připravená slova: {ready}, potřeba je aspoň {minimum}. Procvičujte s kartami „Čtu“ — ty odemykají ostatní hry.",
})


# ============================================================================
# НАСТРОЙКИ: ТРИ ГРУППЫ
#
# «Что учу» человек меняет часто, «как мне удобно» ставит один раз. Восемь
# равных пунктов перемешивали то и другое, и первым в списке стоял режим
# викторины, которым не пользуются 96%.
# ============================================================================
TEXTS.update({
    "settings_group_what": "Co se učím",
    "settings_group_what_title": "<b>Co se učím</b>",
    "settings_group_how": "Jak se učím",
    "settings_group_how_title": "<b>Jak se učím</b>",
    "settings_group_bot": "Bot",
    "settings_group_bot_title": "<b>Bot</b>",
    "settings_group_what_about": "Jazyk, cíl a úroveň.",
    "settings_group_how_about": "Z čeho se skládá lekce a jak zní.",
    "settings_group_bot_about": "Jazyk bota, připomínky a nápověda.",
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
    "quiz_btn_one_more": "Další lekce",
    "home_btn_stats": "Podrobnosti",
    "notif_off_how_to_return": "Znovu zapnout: Nastavení → Bot → Připomínky",
    "reminder_offer_done": "✓ Hotovo: připomínka přijde v <b>{time}</b> ({city})\n\nČas, dny i časové pásmo si můžete upravit",
    "reminder_offer_setup": "Upravit připomínky",
    "level_offer": "Na úrovni <b>{current}</b> chybujete jen zřídka\n\nPřejít na <b>{following}</b>?\n\nVšechno naučené Vám zůstane",
    "level_offer_yes": "Ano, přejít na {following}",
    "level_offer_no": "Zůstat tady",
    "level_offer_done": "Teď jste na úrovni <b>{following}</b>\n\nSlova budou těžší",
    "level_offer_pick": "Zdá se, že úroveň <b>{current}</b> je pro Vás snadná\n\nNa jaké úrovni chcete pokračovat?\n\nVšechno naučené Vám zůstane",
    "level_offer_stay": "Zůstat na {current}",
    "placement_result": "Podle Vašich odpovědí Vám sedí úroveň <b>{level}</b> — další slova budou z této úrovně\n\nPokud chcete jinou, vyberte ji níže",
    "level_set_done": "Úroveň <b>{level}</b>\n\nDalší slova budou z této úrovně",
    "level_down_offer": "Na úrovni <b>{current}</b> je zatím dost chyb\n\nPřejít na <b>{previous}</b>?\n\nSlova budou snazší a všechno naučené Vám zůstane",
    "level_down_yes": "Ano, přejít na {previous}",
    "level_down_done": "Teď jste na úrovni <b>{previous}</b>\n\nSlova budou snazší",
})


# ============================================================================
# ЗАЧЕМ УЧИШЬ — ОПРОС, ВСТРОЕННЫЙ В ПЕРВОЕ НАЖАТИЕ
#
# Режим «по категории» работает, и им пользуются ТРИ человека из 233:
# он спрятан третьим уровнем настроек. Каждая кнопка здесь И отвечает
# на вопрос, И начинает первый круг — шага не прибавилось.
# ============================================================================
TEXTS.update({
    "goal_question": "K čemu jazyk potřebujete? Podle toho vybereme slova.",
    "goal_work": "Do práce",
    "goal_travel": "Na cesty",
    "goal_living": "Pro život v zahraničí",
    "goal_study": "Ke studiu",
    "goal_any": "Prostě se učit slova",
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
    "intro_games": "Každé slovo se tu učíte v pěti hrách: přečíst ho, vybavit si ho podle významu, slyšet ho, říct ho nahlas a spojit ho do dvojice.\nKaždá lekce je pro Vás sama promíchá.",
    "intro_numbers": "12 902 slov · 20 témat · 6 úrovní\n{languages} v libovolné dvojici: klidně se učte polštinu přes angličtinu.",
    "intro_menu_settings": "jazyk, hry v lekci, připomínky",
    "intro_menu_stats": "Váš pokrok",
    "intro_menu_rating": "žebříček tohoto měsíce",
    "intro_menu_learn": "lekce",
    "intro_menu_title": "Co je kde:",
})


# ============================================================================
# ЗАЧЕМ УЧУ — ЭКРАН НАСТРОЙКИ
#
# Без него цель осталась бы пустой навсегда у всех 233 нынешних
# пользователей: онбординг у них давно позади. Та же дыра, что была у
# состава занятия — колонка есть, экрана нет.
# ============================================================================
TEXTS.update({
    "settings_btn_goal": "Cíl",
    "settings_goal_title": "<b>K čemu to potřebuji</b>",
    "settings_goal_description": "Slova z Vašeho tématu přijdou na řadu jako první. Obtížnost se dál řídí Vaší úrovní a naučená slova se dál vracejí k opakování.",
    "settings_goal_set": "Cíl uložen",
    "settings_goal_line": "Cíl: <b>{goal}</b>",
    "settings_goal_none": "nevybrán",
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
    "match_title": "<b>Najděte dvojice</b>",
    "match_progress": "Spojeno: {matched} z {total}",
    "match_errors": "✗ chyby: {count}",
    "match_hint": "Klepněte na slovo na jedné straně a pak na jeho dvojici na druhé.",
    "match_wrong": "✗ Tohle není dvojice",
    "match_done": "<b>Všechny dvojice nalezeny!</b>",
    "match_done_counted": "Do pokroku se započítalo: {counted} z {total}. Počítají se jen dvojice spojené na první pokus a nikdy ta poslední: u ní už není z čeho vybírat.",
    "match_btn_again": "Další dvojice",
    "match_not_ready": "Zatím ne: dvojice potřebují {need} známých slov a Vy jich máte {have}. Procvičujte s kartami „Čtu“ — ty je odemknou.",
})

TEXTS["match_back_to_round"] = "Zpět do lekce."

TEXTS.update({
    "settings_btn_match": "Dvojice v lekci",
    "settings_match_title": "<b>Dvojice v lekci</b>",
    "settings_match_description": "V každé lekci nahradí jednu otázku v polovině hra s dvojicemi: pět slov a pět významů, které spojíte do párů. Používá jen známá slova, takže se objeví, až jich budete mít aspoň deset.",
    "match_state_on": "Dvojice jsou zapnuté: objeví se v polovině lekce.",
    "settings_match_short_on": "s dvojicemi",
    "settings_channels_short_one": "jen „Čtu“",
    "settings_channels_short_some": "{count} z {total} her",
    "settings_channels_short_all": "všechny hry",
    "plural_words": "slovo|slova|slov",
    "plural_points": "bod|body|bodů",
    "plural_days": "den|dny|dní",
    "settings_audio_short_off": "bez zvuku",
    "settings_audio_short_on": "se zvukem",
    "settings_match_short_off": "bez dvojic",
    "match_state_off": "Dvojice jsou vypnuté: lekce obsahuje jen otázky.",
})

# ============================================================================
# СООБЩЕНИЯ ПО ИНИЦИАТИВЕ БОТА — патч 2.1 «Вовлечение» (`nudge_texts`).
# Голос и запрет значков — в ru.py; номера вариантов `_N` те же (тест).
# ============================================================================
TEXTS.update({
    "plural_lessons": "lekce|lekce|lekcí",
    "nd_teaser_quiz_1": "Pamatujete si, co znamená {word}? {meaning}",
    "nd_teaser_quiz_2": "Vyzkoušejte se: {word} - {meaning}",
    "nd_teaser_quiz_3": "Jedno z Vašich slov: {word} - {meaning}",
    "nd_teaser_quiz_4": "Jak přeložíte {word}? {meaning}",
    "nd_teaser_new_1": "Například: {word} - {meaning}",
    "nd_teaser_new_2": "První slovo: {word} - {meaning}",
    "nd_teaser_new_3": "Jak přeložíte {word}? Překlad je skrytý - klepněte na něj: {meaning}",
    "nd_streak_head_1": "<b>{name}, série: {days} v řadě</b>",
    "nd_streak_head_2": "<b>{name}, {days} v řadě. Pokračujeme?</b>",
    "nd_streak_head_3": "<b>{name}, už {days} v řadě</b>",
    "nd_streak_head_4": "<b>{name}, {days} bez přestávky</b>",
    "nd_streak_head_5": "<b>{name}, ještě jedna lekce a bude to {next_days} v řadě</b>",
    "nd_streak_head_6": "<b>{name}, Vaše série čeká: {days}</b>",
    "nd_streak_head_7": "<b>{days} v řadě, {name}</b>",
    "nd_streak_head_8": "<b>{name}, {days} v řadě. Dnes ještě jednu lekci?</b>",
    "nd_body_learned_1": "Známá slova: {known_n} · naučená: {learned}",
    "nd_body_learned_2": "Slova v učení: {in_work} · naučená: {learned}",
    "nd_body_learned_3": "Už znáte {known}, z toho naučená: {learned}.",
    "nd_body_known_1": "Známá slova: {known_n}. Každá lekce přidává nová.",
    "nd_body_known_2": "Slova v učení: {in_work}. První naučená slova jsou na dosah.",
    "nd_body_known_3": "Už znáte {known}.",
    "nd_streak_close_1": "Malými krůčky k velkému výsledku.",
    "nd_streak_close_2": "Každý den trochu: tak se slova usadí v paměti.",
    "nd_streak_close_3": "Jedna lekce dnes prodlouží sérii.",
    "nd_streak_close_4": "Lekce trvá kolem {minutes_n} minut.",
    "nd_streak_close_5": "Pravidelnost je důležitější než délka lekce.",
    "nd_progress_head_known": "<b>{name}, už znáte {known}</b>",
    "nd_progress_head_1": "<b>{name}, Vaše slova čekají na opakování</b>",
    "nd_progress_head_2": "<b>{name}, najdete pár minut?</b>",
    "nd_progress_head_3": "<b>{name}, pokračujeme tam, kde jsme přestali?</b>",
    "nd_progress_head_4": "<b>{name}, zpátky ke slovům?</b>",
    "nd_progress_head_5": "<b>{name}, dobrá chvíle osvěžit si slova</b>",
    "nd_due_1": "Slova k opakování: {due_n}. Termíny hlídá bot.",
    "nd_due_2": "Je čas zopakovat {due}, než se vytratí z paměti.",
    "nd_due_3": "Slova k opakování: {due_n}. Bot už vybral, kterými začít.",
    "nd_due_many_1": "Slov k opakování se sešlo dost: lekce začne těmi nejdůležitějšími.",
    "nd_due_many_2": "Opakování se nahromadilo. Stačí jedna lekce denně, zbytek počká.",
    "nd_praise_1": "Hotové lekce: {lessons_n}. Pomalu, ale pravidelně.",
    "nd_praise_2": "Dokončené lekce: {lessons_n}. Malými krůčky k velkému výsledku.",
    "nd_praise_3": "Hotové lekce: {lessons_n}, a každá přidala nová slova.",
    "nd_short_1": "Jedna lekce trvá kolem {minutes_n} minut.",
    "nd_short_2": "Zabere to pár minut.",
    "nd_first_head_words": "<b>{name}, včera přibyla nová slova: {first_n}</b>",
    "nd_first_head_1": "<b>{name}, dobrý začátek</b>",
    "nd_first_head_2": "<b>{name}, prověříme včerejší slova?</b>",
    "nd_first_body_1": "Opakování druhý den pomáhá slova upevnit.",
    "nd_first_body_2": "Druhý den je nejlepší chvíle upevnit nová slova.",
    "nd_first_close_1": "Zabere to pár minut.",
    "nd_first_close_2": "Lekce trvá kolem {minutes_n} minut.",
    "nd_kept_head_1": "<b>{name}, všechno je na svém místě</b>",
    "nd_kept_head_2": "<b>{name}, Vaše slova jsou uložená</b>",
    "nd_kept_head_3": "<b>{name}, dlouho jsme se neviděli</b>",
    "nd_kept_body_1": "Známá slova: {known_n} · naučená: {learned}. Nic se neztratilo - lekce začne těmi, která je čas osvěžit.",
    "nd_kept_body_2": "Všechno naučené je uložené. Lekce začne slovy, která je čas osvěžit.",
    "nd_kept_body_3": "Přestávku si dá každý. Začít můžete jednou krátkou lekcí.",
    "nd_kept_best": "Nejlepší série: {best} v řadě. Nová začíná jednou lekcí.",
    "nd_farewell_head_1": "<b>{name}, další připomínky už nebudou</b>",
    "nd_farewell_head_2": "<b>{name}, poslední připomínka</b>",
    "nd_farewell_body_1": "Bot už nebude psát, dokud se nevrátíte. Všechno je uložené: známá slova {known_n}, naučená {learned}. Pokračovat můžete kdykoli tlačítkem níže.",
    "nd_farewell_body_2": "Zdá se, že teď na lekce není čas - to nevadí. Další připomínky už nebudou. Vaše slova i pokrok zůstávají uložené.",
    "nd_start_head_1": "<b>{name}, Vaše první slova čekají</b>",
    "nd_start_head_2": "<b>{name}, začneme?</b>",
    "nd_start_head_3": "<b>{name}, první lekce trvá kolem {minutes_n} minut</b>",
    "nd_start_body_1": "Bot vybere nejužitečnější slova pro Vaši úroveň a sám pohlídá, kdy je zopakovat.",
    "nd_start_body_2": "Začneme nejběžnějšími slovy, která slyšíte každý den.",
    "nd_start_body_3": "Žádná příprava není potřeba: {questions} otázek a pak Vám bot řekne, co a kdy zopakovat.",
    "nd_start3_head_1": "<b>{name}, zkusíte to?</b>",
    "nd_start3_head_2": "<b>{name}, Vaše první slova stále čekají</b>",
    "nd_start_last_head": "<b>{name}, poslední pozvánka</b>",
    "nd_start_last_body": "Další připomínky už nebudou. Pokud budete chtít začít, první lekce trvá kolem {minutes_n} minut - tlačítko je níže.",
    "nd_btn_optin": "Připomenout v {time}",
    "nd_btn_stop": "Tyto zprávy neposílat",
    "nd_auto_time": "Připomínám denně v {time}. Čas můžete změnit",
    "nd_btn_change_time": "Změnit čas",
    "nd_optin_done": "✓ Hotovo: připomínka bude chodit v <b>{time}</b>\n\nČas můžete změnit v nastavení",
})
