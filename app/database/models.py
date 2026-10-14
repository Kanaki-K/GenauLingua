from datetime import datetime, date
from app.core.clock import utcnow
from sqlalchemy import Date
from typing import List, Optional

from sqlalchemy import (
    BigInteger, String, Boolean, DateTime, Integer,
    ForeignKey, Text, Enum as SQLEnum, Float,
    UniqueConstraint, Index, true as sa_true
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ARRAY
from app.database.enums import (
    CEFRLevel, TranslationMode, PartOfSpeech, QuizMode, WordCategory,
    counted_channels,
)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[Optional[str]] = mapped_column(String(255))
    first_name: Mapped[Optional[str]] = mapped_column(String(255))
    last_name: Mapped[Optional[str]] = mapped_column(String(255))

    # Старые поля для статистики
    last_active_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    streak_days: Mapped[int] = mapped_column(Integer, default=0)
    words_learned: Mapped[int] = mapped_column(Integer, default=0)
    quizzes_passed: Mapped[int] = mapped_column(Integer, default=0)
    success_rate: Mapped[int] = mapped_column(Integer, default=0)

    # Уровень и настройки
    level: Mapped[CEFRLevel] = mapped_column(SQLEnum(CEFRLevel), default=CEFRLevel.A1)
    interface_language: Mapped[Optional[str]] = mapped_column(String(2), default=None, nullable=True)

    # === ЯЗЫКОВАЯ ПАРА ===
    # learning_lang — что изучаем, native_lang — на каком языке даётся значение,
    # reverse_mode — спрашивать в обратную сторону (производство вместо узнавания).
    learning_lang: Mapped[str] = mapped_column(String(2), default="de", nullable=False)
    native_lang: Mapped[str] = mapped_column(String(2), default="ru", nullable=False)
    reverse_mode: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Устаревшее поле: пара языков теперь в learning_lang/native_lang/reverse_mode.
    # Оставлено заполняемым для пар с немецким — чтобы прежняя аналитика
    # и откат на предыдущую версию продолжали работать.
    translation_mode: Mapped[Optional[TranslationMode]] = mapped_column(SQLEnum(TranslationMode),
                                                                        default=None, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    anchor_message_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)

    # === РЕЖИМ ВИКТОРИНЫ (НОВОЕ) ===
    quiz_mode: Mapped[QuizMode] = mapped_column(
        SQLEnum(QuizMode, values_callable=lambda e: [m.value for m in e]),
        default=QuizMode.LEVEL, nullable=False
    )
    quiz_category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, default=None)

    # === ЯЗЫКИ И ЛОКАЛИЗАЦИЯ ===
    telegram_language: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)

    # === TIMEZONE ===
    timezone: Mapped[str] = mapped_column(String(50), default="Europe/Berlin")
    utc_offset: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)

    # === ВРЕМЯ АКТИВНОСТИ ===
    first_quiz_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    last_active_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    last_quiz_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    # === НАПОМИНАНИЯ ===
    notifications_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    notification_time: Mapped[str] = mapped_column(String(5), default="20:00")
    notification_days: Mapped[List[int]] = mapped_column(ARRAY(Integer), default=[0, 1, 2, 3, 4, 5, 6])
    last_notification_sent: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Когда боту случилось ПРЕДЛОЖИТЬ напоминания. NULL — не предлагали.
    #
    # Напоминания — единственный замеренный рычаг возврата (6.85 дней против
    # 1.59), но они остаются настройкой, которую надо найти, а настройки не
    # находят: 117 человек из 121 не менял даже время. Поэтому бот предлагает
    # сам — после первого законченного круга, и РОВНО ОДИН РАЗ: второе
    # предложение того же самого человек воспринимает как навязывание.
    reminder_offered_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Уровень, С КОТОРОГО человек отказался подниматься. NULL — не отказывался.
    #
    # Хранится уровень, а не флаг: отказ «не хочу с A1 на A2» не значит
    # «никогда ничего не предлагай». Поднявшись когда-нибудь своей волей,
    # человек снова услышит предложение — уже про следующий. Сравнение идёт
    # с текущим уровнем, поэтому отметка обесценивается сама.
    level_offer_declined: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)
    # На каком по счёту занятии был отказ (`quizzes_passed` в тот момент).
    # Отказ не навсегда: через `level_service.REOFFER_AFTER_ROUNDS` занятий
    # на высокой точности бот спросит снова — владелец, 14 октября.
    level_offer_declined_round: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Зачем человек учит язык: work / travel / living / study / any.
    #
    # Хранится ЦЕЛЬ, а не список категорий: цель — то, что человек о себе
    # сказал, а категории — наша догадка о том, что из этого следует.
    # Догадка будет меняться, сказанное — нет. Сопоставление живёт в
    # `goal_service`, и правится там, не трогая данные людей.
    learning_goal: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)

    # Показывать ли 🧩 доску сопоставления внутри круга.
    #
    # Отдельно от `quiz_channels` нарочно: там каналы — способы задать
    # вопрос про ОДНО слово, а доска берёт пять сразу и каналом быть не
    # может. По умолчанию включено: спрячь за переключателем — и не увидит
    # никто, это в проекте уже измерено.
    match_in_round: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default="true"
    )

    # === НАСТРОЙКИ ВИКТОРИНЫ ===
    # Круг из 15, а не 25: вопросы на слух дольше текстовых, и длинный круг
    # начинают бросать на середине. Короткий чаще ДОВОДЯТ до конца, а
    # законченное занятие — это и отметка в стрике, и строка в рейтинге.
    quiz_word_count: Mapped[int] = mapped_column(Integer, default=15)

    # === ОЗВУЧКА ===
    # Включена по умолчанию: озвучку просили в отзывах, и это главное, за чем
    # человек сюда придёт. Кому мешает — выключает в настройках.
    # Выбранный голос лежит отдельно, в user_tts_voices: он свой на каждый
    # изучаемый язык.
    audio_enabled: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default=sa_true()
    )

    # === СОСТАВ ЗАНЯТИЯ: какими каналами задавать вопросы ===
    # Буквы из QuizChannel: «t» текст, «a» слух, «s» речь. Одна колонка, а не
    # три флага: каналов станет три, и тройку пришлось бы читать в каждом
    # месте, где важен состав. Строка расширяется четвёртым каналом без
    # миграции.
    #
    # По умолчанию «tas» — ВСЕ ТРИ КАНАЛА. Значение по умолчанию и есть
    # решение о том, увидят ли люди новое: 223 пользователя из 233 ни разу не
    # меняли режим викторины, лежащий первым пунктом настроек. Прятать канал
    # за переключателем значит не выпустить его вовсе.
    #
    # Речь была «ta», то есть выключена, и пока её не существовало — это была
    # честность. Замер 13 октября показал цену такой честности, когда игра уже
    # готова: РЕЧЬ ОКАЗАЛАСЬ ВКЛЮЧЕНА У ОДНОГО ЧЕЛОВЕКА ИЗ 233, и тем одним
    # был тестовый счёт. Игра построена, проверена на всех тридцати парах в
    # оба направления — и не доходила ни до кого.
    #
    # Решение владельца 13 октября: «речь да, по умолчанию всем».
    #
    # Резкого скачка это не даёт, и в этом помогает порог допуска: речь
    # открывается слову после ДВУХ верных ответов по нему, так что новичок
    # увидит её не в первом круге, а когда уже знает слово глазами. Пропуск
    # вопроса вслух не считается ошибкой — человек в транспорте ничего не
    # теряет.
    # ПЯТАЯ ИГРА — ПРИПОМИНАНИЕ — тоже по умолчанию. Прежде направление
    # было отдельной настройкой на весь круг, и включили её 10 человек из
    # 233. Решение владельца: она становится игрой среди пятнадцати
    # вопросов, а не режимом.
    # ШЕСТАЯ — «Собираю» (`b`) — тоже по умолчанию и по той же причине:
    # спрятанную игру не увидит никто. Миграция `b6d1e3f7a920` дописала её
    # всем, у кого состав был «tasr».
    quiz_channels: Mapped[str] = mapped_column(
        String(8), nullable=False, default="tasrb", server_default="tasrb"
    )

    # === МЕСЯЧНАЯ СИСТЕМА РЕЙТИНГА ===
    lifetime_score: Mapped[int] = mapped_column(Integer, default=0)
    best_streak_days: Mapped[int] = mapped_column(Integer, default=0)
    total_monthly_wins: Mapped[int] = mapped_column(Integer, default=0)

    # Связи
    quiz_sessions: Mapped[List["QuizSession"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    @property
    def display_name(self) -> str:
        """Отображаемое имя: приоритет имя+фамилия"""
        if self.first_name:
            name = self.first_name
            if self.last_name:
                name += f" {self.last_name}"
            return name
        elif self.last_name:
            return self.last_name
        elif self.username:
            return self.username
        else:
            return f"User {self.id}"

    @property
    def quiz_mode_display(self) -> str:
        """Отображение текущего режима для дебага"""
        if self.quiz_mode == QuizMode.LEVEL:
            return f"Level ({self.level.value})"
        elif self.quiz_mode == QuizMode.CATEGORY:
            return f"Category ({self.quiz_category})"
        elif self.quiz_mode == QuizMode.ALL_WORDS:
            return "All words"
        elif self.quiz_mode == QuizMode.DIFFICULT:
            return "Difficult"
        return "Unknown"


class UserWord(Base):
    __tablename__ = "user_words"

    # КАСКАД ОБЯЗАТЕЛЕН, и это не косметика. Все прочие таблицы, ссылающиеся
    # на человека (quiz_sessions, monthly_stats, translation_reports,
    # win_streaks, user_tts_voices), объявлены с CASCADE — а здесь его не
    # было, и из-за ОДНОЙ этой таблицы человека нельзя было удалить вообще:
    # база отвечала «still referenced from table user_words». Для бота, у
    # которого есть политика приватности и живые люди с личными данными, это
    # значило, что удалить свои данные нельзя никак, кроме правки базы
    # руками. То же с словом: его прогресс держал ряд намертво.
    user_id = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    word_id = mapped_column(
        ForeignKey("words.id", ondelete="CASCADE"), primary_key=True
    )

    # Прогресс считается отдельно по каждому изучаемому языку: выученное
    # «das Haus» не делает выученным «house». Часть первичного ключа.
    learning_lang = mapped_column(String(2), primary_key=True, nullable=False, server_default="de")

    # прогресс по слову — ОБЩИЙ итог по всем каналам
    correct_streak = mapped_column(Integer, default=0, nullable=False)
    times_shown = mapped_column(Integer, default=0, nullable=False)
    times_correct = mapped_column(Integer, default=0, nullable=False)
    last_seen_at = mapped_column(DateTime, nullable=True)

    # Из общего итога выделены два канала: слух и речь. Третий, текстовый,
    # НЕ хранится — он выводится вычитанием и потому не может разойтись с
    # итогом. Отдельной колонкой его рано или поздно обновили бы не вместе с
    # остальными, и это вопрос времени, а не аккуратности.
    #
    # Итог читают все: подбор по SRS, отметка «выучено», рейтинг, статистика
    # и гейт целостности. Поэтому он и остался итогом — ни один существующий
    # запрос трогать не пришлось.
    #
    # Зачем вообще делить: узнать слово глазами, узнать на слух и произнести
    # вслух — три разных навыка. Смешаешь в одном счётчике — потеряешь
    # видимый разрыв между ними, а он и мотивирует сильнее всего.
    shown_audio = mapped_column(Integer, default=0, nullable=False, server_default="0")
    correct_audio = mapped_column(Integer, default=0, nullable=False, server_default="0")
    shown_speech = mapped_column(Integer, default=0, nullable=False, server_default="0")
    correct_speech = mapped_column(Integer, default=0, nullable=False, server_default="0")

    # ПЯТАЯ ИГРА: значение дано, выбрать слово. Своя пара колонок нужна по
    # той же причине, по какой она есть у слуха: без неё бот не отличит
    # «узнаю das Metall» от «вспомню, что металл — это das Metall», и
    # подбор не сможет догружать слабую сторону. Прежде направление было
    # настройкой на весь круг, и в прогрессе слова не отражалось ВОВСЕ.
    shown_reverse = mapped_column(Integer, default=0, nullable=False, server_default="0")
    correct_reverse = mapped_column(Integer, default=0, nullable=False, server_default="0")

    # ШЕСТАЯ ИГРА: собрать пример из кнопок-слов. Своя пара колонок — по
    # той же причине, что у остальных: «узнаю слово» и «соберу с ним
    # фразу» — разные навыки; строка «Грамматика» в подробной статистике
    # считается отсюда.
    shown_build = mapped_column(Integer, default=0, nullable=False, server_default="0")
    correct_build = mapped_column(Integer, default=0, nullable=False, server_default="0")

    @property
    def shown_text(self) -> int:
        """
        Текстовых показов: всё, что не слух, не речь и не припоминание.

        ВЕЗДЕ `or 0`, и это не перестраховка. У только что созданного
        объекта значения по умолчанию ещё не применены — они ставятся при
        вставке, а свойство спрашивают раньше. На трёх каналах это не
        всплывало, потому что их счётчики всегда передавали явно; четвёртый
        уронил вычитание с «unsupported operand type(s) for -: int and
        NoneType» на первом же прогоне тестов.
        """
        # Вычитаются ВСЕ каналы со своими колонками — правилом, а не
        # списком (`counted_channels`): канал, не вписанный сюда руками,
        # раздул бы карточку на все свои ответы
        return (self.times_shown or 0) - sum(
            getattr(self, f"shown_{c.key}") or 0 for c in counted_channels()
        )

    @property
    def correct_text(self) -> int:
        return (self.times_correct or 0) - sum(
            getattr(self, f"correct_{c.key}") or 0 for c in counted_channels()
        )

    # считается "выучено", когда достигнут порог streak
    learned = mapped_column(Boolean, default=False, nullable=False)

    # КОГДА слово стало выученным — переход learned False → True. Пусто,
    # пока слово не выучено; промах, снявший отметку, стирает и дату.
    #
    # Месячный балл «+3 за выученное слово» прежде считал выученные слова
    # с последним показом в этом месяце: слово, выученное в сентябре и
    # повторённое по расписанию в октябре, оплачивалось в обоих месяцах, а
    # в «за всё время» (сумма месяцев) — дважды. Платим за переход, один
    # раз, в том месяце, когда он случился (аудит 14 октября).
    learned_at = mapped_column(DateTime, nullable=True)

    created_at = mapped_column(DateTime, default=utcnow, nullable=False)
    updated_at = mapped_column(DateTime, default=utcnow, onupdate=utcnow, nullable=True)

    user = relationship("User", backref="learned_items")
    word = relationship("Word", backref="learned_by")


class Word(Base):
    __tablename__ = "words"
    __table_args__ = (
        UniqueConstraint("word_de", "level", name="uq_words_word_de_level"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Немецкое слово
    word_de: Mapped[str] = mapped_column(String(255), index=True)
    article: Mapped[Optional[str]] = mapped_column(String(10))  # der/die/das

    # Часть речи и уровень
    pos: Mapped[PartOfSpeech] = mapped_column(SQLEnum(PartOfSpeech))
    level: Mapped[CEFRLevel] = mapped_column(SQLEnum(CEFRLevel), index=True)

    # Категория (НОВОЕ — одна строка вместо массива)
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)

    # Частота (НОВОЕ — для Топ 10К)
    frequency_rank: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True)

    # Переводы
    translation_ru: Mapped[Optional[str]] = mapped_column(String(255))
    translation_uk: Mapped[Optional[str]] = mapped_column(String(255))
    translation_en: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    translation_tr: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    translation_pl: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Примеры использования
    example_de: Mapped[Optional[str]] = mapped_column(Text)
    example_ru: Mapped[Optional[str]] = mapped_column(Text)
    example_uk: Mapped[Optional[str]] = mapped_column(Text)
    example_en: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    example_tr: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    example_pl: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Старое поле categories — оставляем для обратной совместимости
    categories: Mapped[Optional[List[str]]] = mapped_column(
        ARRAY(String),
        default=list
    )

    # Статистика
    times_shown: Mapped[int] = mapped_column(Integer, default=0)
    times_correct: Mapped[int] = mapped_column(Integer, default=0)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utcnow
    )

    # Relationships
    quiz_questions: Mapped[List["QuizQuestion"]] = relationship(
        back_populates="word",
        cascade="all, delete-orphan"
    )

    @property
    def success_rate(self) -> float:
        """Процент правильных ответов"""
        if self.times_shown == 0:
            return 0.0
        return (self.times_correct / self.times_shown) * 100

    @property
    def full_word_de(self) -> str:
        """Полное немецкое слово с артиклем"""
        if self.article and self.article != "-":
            return f"{self.article} {self.word_de}"
        return self.word_de

    def get_translation(self, language: str) -> str:
        """Слово на указанном языке (для немецкого — с артиклем)"""
        from app.services.language_service import word_text

        return word_text(self, language)

    def get_example(self, language: str) -> str:
        """Пример на указанном языке"""
        from app.services.language_service import example_text

        return example_text(self, language)


class QuizSession(Base):
    __tablename__ = "quiz_sessions"
    __table_args__ = (
        Index("ix_quiz_sessions_user_completed", "user_id", "completed_at"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True
    )

    level: Mapped[CEFRLevel] = mapped_column(SQLEnum(CEFRLevel))

    # === ЯЗЫКОВАЯ ПАРА СЕССИИ ===
    learning_lang: Mapped[str] = mapped_column(String(2), default="de", nullable=False)
    native_lang: Mapped[str] = mapped_column(String(2), default="ru", nullable=False)
    is_reverse: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Устаревшее поле — см. User.translation_mode. Стало nullable: пары без
    # немецкого (например ru→en) в старом enum не выражаются.
    translation_mode: Mapped[Optional[TranslationMode]] = mapped_column(
        SQLEnum(TranslationMode), nullable=True
    )

    # Режим викторины (НОВОЕ)
    quiz_mode: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    quiz_category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Статистика сессии.
    # total_questions — СКОЛЬКО ПЛАНИРОВАЛОСЬ (обычно 25).
    # answered_questions — сколько реально отвечено; считать точность нужно
    # по нему, иначе брошенная сессия выглядит как сплошные ошибки.
    # Пишется инкрементально, поэтому у брошенной сессии показывает точку выхода.
    total_questions: Mapped[int] = mapped_column(Integer, default=0)
    answered_questions: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    correct_answers: Mapped[int] = mapped_column(Integer, default=0)

    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)

    @property
    def accuracy_percent(self) -> float:
        """Точность по фактически отвеченным вопросам."""
        if not self.answered_questions:
            return 0.0
        return (self.correct_answers / self.answered_questions) * 100

    # Аналитика
    start_source: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    exit_reason: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    exit_at_question: Mapped[int] = mapped_column(Integer, default=0)

    started_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utcnow
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)

    # Relationships
    user: Mapped["User"] = relationship(back_populates="quiz_sessions")
    questions: Mapped[List["QuizQuestion"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan"
    )

    @property
    def score_percentage(self) -> float:
        """Процент правильных ответов"""
        if self.total_questions == 0:
            return 0.0
        return (self.correct_answers / self.total_questions) * 100


class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    session_id: Mapped[int] = mapped_column(
        ForeignKey("quiz_sessions.id", ondelete="CASCADE"),
        index=True
    )
    word_id: Mapped[int] = mapped_column(
        ForeignKey("words.id", ondelete="CASCADE"),
        index=True
    )

    # Ответ пользователя
    user_answer: Mapped[Optional[str]] = mapped_column(String(255))
    is_correct: Mapped[Optional[bool]] = mapped_column(Boolean)

    # Каким каналом задан ЭТОТ вопрос: «t» текст, «a» слух, «s» речь.
    #
    # Хранится у вопроса, а не у занятия: круг смешанный, и у занятия канала
    # просто НЕТ — есть состав. Единственное место, где канал определён
    # однозначно, — отдельный заданный вопрос.
    #
    # nullable: вопросы, заданные до появления каналов, были текстовыми,
    # других в боте не было. Пустое значение читается как «текст».
    channel: Mapped[Optional[str]] = mapped_column(String(1), nullable=True)

    # Время ответа
    answered_at: Mapped[Optional[datetime]] = mapped_column(DateTime)

    response_time_seconds: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utcnow
    )

    # Relationships
    session: Mapped["QuizSession"] = relationship(back_populates="questions")
    word: Mapped["Word"] = relationship(back_populates="quiz_questions")


# ============================================================================
# МЕСЯЧНЫЙ РЕЙТИНГ
# ============================================================================

class MonthlySeason(Base):
    """Месячный сезон соревнований"""
    __tablename__ = "monthly_seasons"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    month: Mapped[int] = mapped_column(Integer, nullable=False)

    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    winners_finalized: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)

    # Relationships
    stats: Mapped[List["MonthlyStats"]] = relationship(back_populates="season", cascade="all, delete-orphan")
    awards: Mapped[List["MonthlyAward"]] = relationship(back_populates="season", cascade="all, delete-orphan")


class MonthlyStats(Base):
    """Статистика пользователя за месяц (отдельно по каждому изучаемому языку)"""
    __tablename__ = "monthly_stats"
    __table_args__ = (
        UniqueConstraint("user_id", "season_id", "learning_lang",
                         name="uq_monthly_stats_user_season_lang"),
        Index("ix_monthly_stats_user_id", "user_id"),
        Index("ix_monthly_stats_season_id", "season_id"),
        Index("ix_monthly_stats_score", "monthly_score"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    season_id: Mapped[int] = mapped_column(ForeignKey("monthly_seasons.id", ondelete="CASCADE"), nullable=False)

    # Рейтинг считается отдельно по языкам: учащие английский соревнуются
    # с учащими английский, а не с учащими немецкий.
    learning_lang: Mapped[str] = mapped_column(String(2), default="de", nullable=False)

    # Основные метрики
    monthly_score: Mapped[int] = mapped_column(Integer, default=0)
    monthly_quizzes: Mapped[int] = mapped_column(Integer, default=0)
    monthly_reverse: Mapped[int] = mapped_column(Integer, default=0)
    monthly_words: Mapped[int] = mapped_column(Integer, default=0)
    monthly_streak: Mapped[int] = mapped_column(Integer, default=0)
    monthly_avg_percent: Mapped[int] = mapped_column(Integer, default=0)

    # Для расчёта среднего
    total_correct: Mapped[int] = mapped_column(Integer, default=0)
    total_questions: Mapped[int] = mapped_column(Integer, default=0)

    # Верных ответов по каналам. Текстовый не хранится — выводится как
    # total_correct минус остальные, ровно как в user_words: отдельной
    # колонкой его рано или поздно обновили бы не вместе с остальными.
    correct_audio: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    correct_speech: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    correct_reverse: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    correct_build: Mapped[int] = mapped_column(Integer, default=0, server_default="0")

    # Бонус за подтверждённые репорты
    report_bonus: Mapped[int] = mapped_column(Integer, default=0)

    # Финальный ранг (заполняется в конце месяца)
    final_rank: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Служебные
    last_quiz_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, onupdate=utcnow)

    # Relationships
    user: Mapped["User"] = relationship(backref="monthly_stats")
    season: Mapped["MonthlySeason"] = relationship(back_populates="stats")

    # Цена верного ответа по каналам. Отношение 1 : 2 : 3 — не круглые
    # числа ради красоты, а порядок трудности:
    #   текст  узнать написанное, подсказывает и форма слова, и длина
    #   слух   формы нет вовсе, различать приходится на звук
    #   речь   не узнавание, а ПРОИЗВОДСТВО, самый дорогой навык
    # Если платить за все три одинаково, рациональный ученик останется на
    # самом лёгком, и соревнование будет награждать выбор кнопки, а не
    # усилие.
    POINTS_TEXT = 1
    # Припоминание стоит столько же, сколько карточка, И ЭТО ЗАМЕР, а не
    # осторожность: точность прямых вопросов 87.9%, обратных 87.1% на
    # 28 204 и 1 002 ответах. Платить больше за труд, которого замер не
    # находит, значит наградить за выбор кнопки. Когда пятая игра пойдёт
    # всем и накопит свои числа, цену можно будет пересмотреть — на них.
    POINTS_REVERSE = 1
    POINTS_AUDIO = 2
    POINTS_SPEECH = 3
    # Сборка фразы стоит столько же, сколько речь: это тоже ПРОИЗВОДСТВО, и
    # самое длинное в боте — вся фраза с порядком слов и формами, среди
    # слов-ловушек (der/den/dem). Дешевле речи её ставить нельзя: тогда
    # выгоднее было бы говорить, хотя трудом они равны. Решение владельца.
    POINTS_BUILD = 3

    @classmethod
    def points_for(cls, channel) -> int:
        """
        Цена верного ответа каналом — по имени: `POINTS_<КАНАЛ>`.

        Правило, а не таблица: канал без цены упадёт здесь же
        (AttributeError) на первом тесте, а не заплатит тихо как карточка.
        """
        return getattr(cls, f"POINTS_{channel.name}")

    POINTS_PER_ROUND = 10        # за ДОВЕДЁННЫЙ до конца круг
    POINTS_PER_WORD = 3          # слово перешло в «выучено»

    # БОНУСА ЗА ОБРАТНЫЙ КРУГ БОЛЬШЕ НЕТ. Он платил 5 за круг, целиком
    # сыгранный в обратную сторону, — а такого круга больше не существует:
    # направление стало игрой внутри круга и платит за ответ, как
    # остальные. Снятие никого не обидело: в действующем сезоне
    # `monthly_reverse` у всех ноль, то есть бонус не начислился ни разу.
    #
    # Ноль оставлен, а не удалён, чтобы прежние, уже закрытые сезоны
    # пересчитывались тем же кодом и давали те же числа.
    POINTS_PER_REVERSE = 0

    # За ПОДТВЕРЖДЁННУЮ жалобу на перевод или произношение.
    #
    # Было один балл — столько же, сколько за одну прочитанную карточку, и
    # это не сходилось ни с трудом, ни с пользой. Человек должен заметить
    # ошибку, открыть список, выбрать слово, отправить и дождаться
    # подтверждения; а исправленный ряд потом служит ВСЕМ, кто учит этот
    # язык, и во всех шести направлениях сразу. Пять — половина круга:
    # заметно больше выученного слова (3) и заметно меньше, чем за занятие,
    # которого человек не проводил.
    #
    # Накрутить нельзя по устройству: жалоба на слово одна (тройная
    # уникальность в `translation_reports`), в день их не больше двадцати, и
    # платит не отправка, а подтверждение живым админом.
    #
    # 15, А НЕ 5 — решение владельца 14 октября: «подтверждённый репорт я
    # считаю должно быть 15 а то и 20. Чем больше помогают и это
    # подтверждают — больше пользы боту = выше награда». Исправленный ряд
    # служит всем, кто учит язык, во всех шести направлениях.
    POINTS_PER_REPORT = 15

    # ПОТОЛКА ЗА МЕСЯЦ НЕТ — он был и снят решением владельца: «мы платим
    # всегда, если реально репорт подтверждает, что ошибка была! Абуз — это
    # нельзя чтобы на 1 слово несколько раз присылали». Антиабуз —
    # в устройстве: одна жалоба на слово и вид, одна оплата за слово,
    # платит только подтверждение, двадцать жалоб в день (см. admin.py,
    # `_reward_reporters`).

    # Точность начисляется ПЛАВНО, от порога 60%: раньше стоял обрыв
    # (90% → +50, 89% → +30), и человек с 89% видел, что двадцать баллов
    # пропали из-за одного вопроса. Обрыв воспринимается как
    # несправедливость, даже когда он описан в правилах.
    ACCURACY_FLOOR = 60

    # Серия РАСТЁТ в цене: десятый день подряд дороже первого. Это главный
    # рычаг возврата — и он же делает пропуск ощутимой потерей. Потолок,
    # чтобы один марафонец не оторвался от поля навсегда.
    STREAK_DAILY_CAP = 10

    def calculate_monthly_score(self) -> int:
        """
        Месячный балл.

        ПРИНЦИП: платим за УСИЛИЕ, а не за нажатия. Отсюда три отличия от
        прежней формулы.

        1. Верный ответ стоит по-разному в зависимости от канала (1/2/3).
           Прежде все стоили одинаково, и после появления аудирования это
           стало прямо вредным советом: «не напрягайся».
        2. Точность начисляется плавно, без обрыва на 90%.
        3. Серия дней растёт в цене, а не даёт фиксированные три балла.

        Текстовые ответы считаются ВЫЧИТАНИЕМ из общего числа верных —
        своей колонки у них нет, и разойтись с итогом они не могут.
        """
        # Каналы со своими колонками — ВСЕ, правилом (`counted_channels`):
        # канал, забытый в формуле, оплачивался бы как карточка, и по баллу
        # этого было бы не видно
        own = {c: getattr(self, f"correct_{c.key}") or 0 for c in counted_channels()}
        correct_text = max(0, (self.total_correct or 0) - sum(own.values()))

        score = correct_text * self.POINTS_TEXT + sum(
            count * self.points_for(c) for c, count in own.items()
        )

        score += self.monthly_quizzes * self.POINTS_PER_ROUND
        score += self.monthly_reverse * self.POINTS_PER_REVERSE
        score += self.monthly_words * self.POINTS_PER_WORD
        score += self.streak_points(self.monthly_streak or 0)

        over = max(0, (self.monthly_avg_percent or 0) - self.ACCURACY_FLOOR)
        score += round((self.total_questions or 0) * over / 100)

        score += self.report_bonus or 0
        return int(score)

    @classmethod
    def streak_points(cls, days: int) -> int:
        """
        Баллы за серию: каждый следующий день дороже предыдущего, до потолка.

        День 1 даёт 1, день 5 — 5, день 10 и все дальнейшие — по 10. За
        тридцать дней подряд набегает 255, за три дня — 6. Разрыв между
        «хожу каждый день» и «захожу иногда» виден в таблице, и это ровно
        то, ради чего серия в рейтинге и нужна.

        Прежняя формула давала ровно три балла за день, и тридцатый день
        стоил столько же, сколько первый, — то есть терять серию было почти
        не жалко.
        """
        days = max(0, int(days))
        full = min(days, cls.STREAK_DAILY_CAP)
        rest = max(0, days - cls.STREAK_DAILY_CAP)
        return full * (full + 1) // 2 + rest * cls.STREAK_DAILY_CAP


class MonthlyQuizEvent(Base):
    """Таблица для идемпотентности - какие викторины уже учтены"""
    __tablename__ = "monthly_quiz_events"
    __table_args__ = (
        UniqueConstraint("quiz_session_id", name="uq_quiz_event_session"),
        Index("ix_monthly_quiz_events_user_id", "user_id"),
        Index("ix_monthly_quiz_events_season_id", "season_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # Уникальность и индекс объявлены в __table_args__ выше; дублировать
    # их на колонке нельзя — получается лишний индекс
    quiz_session_id: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    season_id: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)


class WinStreak(Base):
    """Серия побед пользователя (win streak)"""
    __tablename__ = "win_streaks"
    __table_args__ = (
        UniqueConstraint("user_id", name="uq_win_streak_user"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), unique=True,
                                         nullable=False)

    current_streak: Mapped[int] = mapped_column(Integer, default=0)
    best_streak: Mapped[int] = mapped_column(Integer, default=0)
    total_wins: Mapped[int] = mapped_column(Integer, default=0)
    last_win_season: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, onupdate=utcnow)

    # Relationship
    user: Mapped["User"] = relationship(backref="win_streak")

    @property
    def streak_emoji(self) -> str:
        """Эмодзи в зависимости от текущего стрика"""
        if self.current_streak >= 12:
            return "👑"
        elif self.current_streak >= 6:
            return "🔥🔥🔥"
        elif self.current_streak >= 3:
            return "🔥🔥"
        elif self.current_streak >= 1:
            return "🔥"
        return ""

    @property
    def streak_title(self) -> str:
        """Титул в зависимости от стрика"""
        if self.current_streak >= 12:
            return "Легенда"
        elif self.current_streak >= 6:
            return "Доминатор"
        elif self.current_streak >= 3:
            return "Чемпион"
        return ""


class MonthlyAward(Base):
    """Награды за месячные достижения"""
    __tablename__ = "monthly_awards"
    __table_args__ = (
        Index("ix_monthly_awards_user_id", "user_id"),
        Index("ix_monthly_awards_season_id", "season_id"),
        # Одна награда на человека, сезон и язык. Закрытие сезона зовётся по
        # расписанию И каждый час страховкой; без этой уникальности сбой
        # посреди закрытия и повторный прогон выдали бы награду и бонус к
        # lifetime дважды — база этому ничем не мешала
        UniqueConstraint("user_id", "season_id", "learning_lang",
                         name="uq_monthly_awards_user_season_lang"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    season_id: Mapped[int] = mapped_column(ForeignKey("monthly_seasons.id", ondelete="CASCADE"), nullable=False)

    # Язык, в котором взято место: топ-10 подводится отдельно по каждому
    # изучаемому языку, и без языка две законные награды одного человека за
    # один месяц (немецкий и английский) не отличить от выданной дважды
    learning_lang: Mapped[str] = mapped_column(String(2), nullable=False, default="de",
                                               server_default="de")

    rank: Mapped[int] = mapped_column(Integer, nullable=False)
    award_type: Mapped[str] = mapped_column(String(50), nullable=False)  # "gold", "silver", "bronze", "top10"
    lifetime_bonus: Mapped[int] = mapped_column(Integer, default=0)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)

    # Когда человеку СООБЩИЛИ о награде. Пусто — значит ещё не сообщили.
    #
    # Отметка нужна потому, что закрытие сезона вызывается дважды: первого
    # числа по расписанию и каждый час страховкой, на случай выключенного
    # бота. Без неё победитель получал бы поздравление каждый час.
    notified_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Relationships
    user: Mapped["User"] = relationship(backref="monthly_awards")
    season: Mapped["MonthlySeason"] = relationship(back_populates="awards")


# ============================================================================
# РЕПОРТЫ ОШИБОК ПЕРЕВОДА
# ============================================================================

class TranslationReport(Base):
    """
    Репорт от пользователя: что со словом не так.

    С появлением озвучки жалоба перестала быть однозначной: перевод может быть
    верным, а произношение нет. Поэтому у репорта есть вид — 'text' или
    'audio'. Это не формальность: живые люди ловят именно то, чего не ловит
    машинная проверка озвучки — ударение и гетеронимы, которые распознавание
    речи пропускает.

    Уникальность стала тройной: одно слово можно зарепортить и по тексту,
    и по озвучке, но каждое по одному разу.
    """
    __tablename__ = "translation_reports"
    __table_args__ = (
        UniqueConstraint(
            "user_id", "word_id", "kind", name="uq_translation_reports_user_word_kind"
        ),
        Index("ix_translation_reports_status", "status"),
        Index("ix_translation_reports_kind", "kind"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    word_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("words.id", ondelete="CASCADE"), nullable=False, index=True
    )
    quiz_session_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("quiz_sessions.id", ondelete="SET NULL"), nullable=True
    )
    # 'text' — неверный перевод, 'audio' — неверное произношение.
    # Прежние репорты все про текст: озвучки тогда не было.
    kind: Mapped[str] = mapped_column(
        String(8), nullable=False, default="text", server_default="text"
    )
    # Каким голосом человек слышал слово. Без этого жалобу на произношение
    # нечем проверить: голосов на язык до шести, и звучат они по-разному.
    voice: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="pending"
    )  # pending / reviewed / fixed / rejected
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)

    # Relationships
    user: Mapped["User"] = relationship(backref="translation_reports")
    word: Mapped["Word"] = relationship(backref="translation_reports")


# ============================================================================
# ГРУППЫ СЛОВ ПО ЯЗЫКАМ (схлопывание дублей)
# ============================================================================

class WordLangGroup(Base):
    """
    Схлопывание строк, которые на конкретном языке дают одно и то же слово.

    Зачем: база немецко-центричная, и Meeting / Sitzung / Treff / Versammlung
    все переводятся на английский как «meeting». Без группировки учащий
    английский получил бы четыре карточки на одно слово, а прогресс по нему
    размазался бы на четыре записи. Дубли есть и в немецком — 131 слово
    повторяется на разных уровнях (wirklich, einfach, genau).

    В викторине участвуют только строки с is_canonical = True; прогресс
    и репорты пишутся на canonical_id.

    Таблица целиком производная от words — пересобирается скриптом
    app/scripts/rebuild_word_groups.py.
    """
    __tablename__ = "word_lang_groups"
    __table_args__ = (
        Index("ix_wlg_lang_canonical", "lang", "canonical_id"),
        Index("ix_wlg_canonical_lookup", "lang", "is_canonical"),
        Index("ix_wlg_lang_norm_key", "lang", "norm_key"),
    )

    lang: Mapped[str] = mapped_column(String(2), primary_key=True)
    word_id: Mapped[int] = mapped_column(
        ForeignKey("words.id", ondelete="CASCADE"), primary_key=True
    )
    canonical_id: Mapped[int] = mapped_column(
        ForeignKey("words.id", ondelete="CASCADE"), nullable=False
    )
    is_canonical: Mapped[bool] = mapped_column(Boolean, nullable=False)

    # Нормализованный headword — ключ группировки. Хранится для отладки
    # и для показа синонимов.
    norm_key: Mapped[str] = mapped_column(String(255), nullable=False)


class UserTtsVoice(Base):
    """
    Выбранный голос — на каждый изучаемый язык свой.

    Отдельной таблицей, а не колонкой: голос осмыслен только в паре с языком,
    и при переключении изучаемого языка должен подтягиваться свой. Колонкой
    это было бы шесть полей, которые надо держать в согласии с реестром.

    Нет записи — используется голос по умолчанию для языка. Так что
    незаполненная таблица это норма, а не незавершённая настройка.
    """
    __tablename__ = "user_tts_voices"

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    lang: Mapped[str] = mapped_column(String(2), primary_key=True)
    voice: Mapped[str] = mapped_column(String(64), nullable=False)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=utcnow, onupdate=utcnow
    )


class WordLemmaOverride(Base):
    """
    Ручное указание: эта строка — форма слова, а лемма вот эта.

    Зачем. В базе есть 99 пар, где форма и лемма лежат как два отдельных слова
    на одном уровне: «komm» при существующем «kommen», «tu» при «tun», «gibt»
    при «geben». Человек учит их как разные слова, хотя это одно.

    Исправить переименованием нельзя: уникальность (word_de, level) не даст
    двум строкам совпасть. Удалить форму тоже нельзя — у quiz_questions
    каскадное удаление, и вместе со словом исчезли бы 326 исторических ответов,
    а точность в завершённых сессиях стала бы неверной.

    Поэтому форма остаётся строкой, но при сборке групп слов принудительно
    попадает в группу леммы. Дальше работает уже проверенный механизм: в
    викторине участвует только каноническое слово, а прогресс с формы
    сливается на лемму тем же кодом, что переносил его при переходе на
    многоязычность.

    Откат — удаление строки отсюда и пересборка групп.
    """
    __tablename__ = "word_lemma_overrides"

    word_id: Mapped[int] = mapped_column(
        ForeignKey("words.id", ondelete="CASCADE"), primary_key=True
    )
    lemma_word_id: Mapped[int] = mapped_column(
        ForeignKey("words.id", ondelete="CASCADE"), nullable=False, index=True
    )
    # Почему указание поставлено: чтобы через полгода было понятно
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)


class WordAudio(Base):
    """
    Кэш озвучки: file_id уже загруженного в Telegram клипа.

    Почему file_id, а не файлы. Полная озвучка базы — 106 380 клипов, это
    2,2 ГБ на диске. Но Telegram отдаёт загруженный однажды файл по строке
    в 80 символов бесконечно и бесплатно, так что на диске держать нечего:
    вся озвучка весит в базе около 10 МБ.

    Заполняется лениво, при первом показе слова: первый ученик ждёт лишнюю
    секунду, все следующие получают звук мгновенно. Поэтому пустой кэш —
    рабочее состояние, а не поломка, и предгенерация ничего не блокирует.

    Ключ включает голос: если ученик выбрал другой голос, это другой клип.
    Отсюда же цена выбора голоса — база озвучки множится на число голосов,
    поэтому предгенерируется только голос по умолчанию.
    """
    __tablename__ = "word_audio"
    __table_args__ = (
        # Уникальный, а не просто индекс: при ленивом заполнении два
        # одновременных показа одного слова иначе создали бы две записи
        UniqueConstraint(
            "word_id", "lang", "kind", "voice", name="uq_word_audio_key"
        ),
        Index("ix_word_audio_lookup", "word_id", "lang", "kind", "voice"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    word_id: Mapped[int] = mapped_column(
        ForeignKey("words.id", ondelete="CASCADE"), nullable=False
    )
    # Язык озвучки — изучаемый язык, на котором слово произносится
    lang: Mapped[str] = mapped_column(String(2), nullable=False)
    # 'word' — только слово (для вопроса), 'full' — слово и пример (для разбора)
    kind: Mapped[str] = mapped_column(String(8), nullable=False)
    voice: Mapped[str] = mapped_column(String(64), nullable=False)

    file_id: Mapped[str] = mapped_column(String(255), nullable=False)
    # 'voice' — голосовое сообщение, 'audio' — обычный аудиофайл. file_id
    # привязан к типу отправки, переиспользовать его между ними нельзя.
    file_kind: Mapped[str] = mapped_column(String(8), nullable=False)

    # Каким ботом получен file_id. По документации Telegram file_id
    # принадлежит конкретному боту и другому боту не передаётся, поэтому
    # клипы, сделанные тестовым ботом, для боевого недействительны.
    #
    # Без этой колонки перенос базы между ботами ломал бы озвучку молча:
    # бот отправлял бы чужие file_id, и карточки падали бы одна за другой.
    # Чужая запись считается промахом кэша и переделывается.
    bot_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)

    # Что именно произнесено: текст после разворота сокращений и чисел.
    # Нужен для проверки распознаванием и чтобы понять, устарел ли клип
    # после правки перевода.
    spoken_text: Mapped[str] = mapped_column(Text, nullable=False)

    # Название, с которым клип ЗАГРУЖЕН в Telegram. Не то же, что
    # spoken_text: произносится одно слово, а в названии клипа с примером
    # стоит «слово — начало примера».
    #
    # Хранится потому, что при отправке по file_id Telegram параметр title
    # ИГНОРИРУЕТ и показывает метаданные первой загрузки. Без этой колонки
    # правка правила названия не сбрасывала кэш: spoken_text не менялся,
    # запись считалась годной, и карточка молча показывала старое название
    # (владелец поймал это на снимке: «Zapomnienie» на карточке против
    # «zapomnienie, niepamięć» в заголовке клипа).
    #
    # nullable: у записей до миграции b1c2d3e4f5a6 название неизвестно —
    # они негодны и переделываются, как и записи без bot_id.
    title: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    duration_seconds: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)