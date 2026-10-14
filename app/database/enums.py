import enum


class CEFRLevel(enum.Enum):
    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B2 = "B2"
    C1 = "C1"
    C2 = "C2"


class TranslationMode(enum.Enum):
    DE_TO_RU = "DE_TO_RU"
    RU_TO_DE = "RU_TO_DE"
    DE_TO_UK = "DE_TO_UK"
    UK_TO_DE = "UK_TO_DE"
    DE_TO_EN = "DE_TO_EN"
    EN_TO_DE = "EN_TO_DE"
    DE_TO_TR = "DE_TO_TR"
    TR_TO_DE = "TR_TO_DE"


class PartOfSpeech(enum.Enum):
    """Части речи"""
    NOUN = "noun"
    VERB = "verb"
    ADJECTIVE = "adjective"
    ADVERB = "adverb"
    PHRASE = "phrase"
    PRONOUN = "pronoun"
    PREPOSITION = "preposition"
    CONJUNCTION = "conjunction"
    OTHER = "other"


class QuizMode(enum.Enum):
    """Режим викторины"""
    LEVEL = "level"             # По уровню (A1–C2)
    CATEGORY = "category"       # По категории
    ALL_WORDS = "all_words"     # Топ 10К (вся база)
    DIFFICULT = "difficult"     # Сложные слова


class QuizChannel(enum.Enum):
    """
    Каким каналом задан вопрос. Не то же, что QuizMode.

    QuizMode отвечает «какие слова брать» (уровень, категория, топ, сложные).
    QuizChannel — «через что они приходят к человеку»:

        TEXT    слово написано, выбрать значение      — узнавание написанного
        REVERSE значение дано, выбрать слово          — припоминание слова
        AUDIO   слово звучит, выбрать что услышал     — узнавание на слух
        SPEECH  слово написано, произнести вслух      — производство речи
        BUILD   пример дан по-родному, собрать его
                из кнопок-слов на изучаемом           — производство фразы

    Это три РАЗНЫХ навыка, а не три оформления одного. Человек, который
    узнаёт «Verspätung» глазами, не обязательно узнаёт его на слух и почти
    наверняка не произносит. Поэтому прогресс считается по каждому отдельно:
    смешать их в одном счётчике — значит потерять самое полезное, что даёт
    разделение на каналы, то есть видимый разрыв между навыками.

    Значения короткие: они лягут в callback_data, где у Telegram 64 байта.
    """
    # Порядок — ОТ ЛЁГКОГО К ТРУДНОМУ, и он же порядок шкал на домашнем
    # экране, кнопок прямого входа и чередования в круге. Реверс стоит
    # вторым по замеру, а не по ощущению: точность прямых вопросов 87.9%,
    # обратных 87.1% на 28 204 и 1 002 ответах — то есть он чуть труднее
    # карточки и заметно легче слуха.
    #
    # ЧЕМ РЕВЕРС БЫЛ ДО ЭТОГО. Настройкой на весь круг («режим перевода»):
    # включена — ВСЕ пятнадцать вопросов идут в обратную сторону. Включили
    # её 10 человек из 233, и за всю историю так сыграно 65 кругов из 1 769.
    # Настройка, которой не пользуются, — не выбор, а балласт; решение
    # владельца: «реверс будет игрой 5, которая логически будет
    # расставлена среди 15ти вопросов».
    TEXT = "t"
    REVERSE = "r"
    AUDIO = "a"
    SPEECH = "s"
    # ШЕСТАЯ ИГРА — «Собираю»: пример показан на родном языке, человек
    # собирает его на изучаемом из кнопок-слов. Стоит ПОСЛЕДНЕЙ, то есть
    # самой трудной: речь требует одного слова, а здесь — всей фразы с
    # порядком слов и формами, да ещё среди слов-ловушек (der/den/dem).
    # Буква «b» свободна: «m» занята доской (`match_service.BOARD_CHANNEL`).
    BUILD = "b"

    @property
    def key(self) -> str:
        """
        Имя канала в колонках и ключах: `shown_<key>`, `correct_<key>`,
        `channel_<key>`, `home_scale_<key>`.

        ПРАВИЛО, А НЕ СПИСОК. Каналы прежде перечислялись руками в 15
        местах — счётчики слова, месячный зачёт, починка учёта, приёмки,
        шкалы, — и каждый новый канал надо было вписать во все. Пятую игру
        так и вписывали по одному месту, и починка учёта (`repair_accounting`)
        её забыла: «текст» в балле выводится вычитанием, и забытая колонка
        молча врёт. Имя из перечисления не забудешь вписать.
        """
        return self.name.lower()


def counted_channels() -> tuple["QuizChannel", ...]:
    """
    Каналы со СВОИМИ счётчиками в `user_words` и `monthly_stats`.

    Все, кроме карточки: её счётчики выводятся из итога вычитанием (см.
    `UserWord.shown_text`), и своей колонки у неё нет нарочно — колонка
    рано или поздно разошлась бы с итогом.
    """
    return tuple(c for c in QuizChannel if c is not QuizChannel.TEXT)


class WordCategory(enum.Enum):
    """Категории слов (20 категорий)"""
    ARBEIT_BERUF = "Arbeit & Beruf"
    BILDUNG_LERNEN = "Bildung & Lernen"
    EINKAUFEN_GELD = "Einkaufen & Geld"
    EMOTIONEN_CHARAKTER = "Emotionen & Charakter"
    ESSEN_TRINKEN = "Essen & Trinken"
    FREIZEIT_SPORT = "Freizeit & Sport"
    GESUNDHEIT_MEDIZIN = "Gesundheit & Medizin"
    GRAMMATIK = "Grammatik"
    KLEIDUNG_MODE = "Kleidung & Mode"
    KOMMUNIKATION = "Kommunikation"
    KULTUR_KUNST = "Kultur & Kunst"
    MENSCH_FAMILIE = "Mensch & Familie"
    NATUR_WETTER = "Natur & Wetter"
    RECHT_STAAT = "Recht & Staat"
    REISEN_TRANSPORT = "Reisen & Transport"
    TECHNIK_DIGITAL = "Technik & Digital"
    WIRTSCHAFT = "Wirtschaft"
    WISSENSCHAFT = "Wissenschaft"
    WOHNEN_HAUS = "Wohnen & Haus"
    ZEIT_ALLTAG = "Zeit & Alltag"