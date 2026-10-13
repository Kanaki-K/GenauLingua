"""
Перевод-вопрос без знака: дописать знак там, где вопросительная форма цела.

Сплошной поиск `scan_question_mark` нашёл 812 ячеек, где немецкий пример —
вопрос, а перевод знака не имеет. Дописать знак всем нельзя: ячейки двух
разных видов, и разница принципиальная.

**Потерян только знак.** «Wie ist deine Adresse?» — «What is your address»,
«Яка твоя адреса», «Jaki jest twój adres». Форма вопроса на месте, фраза
верная, не хватает одного символа. Это правится механически.

**Потеряна сама вопросительная форма.** «Wie heißt du?» — «The little dog
is called Rex»; «Möchtest du noch etwas Saft?» — «I drink apple juice».
Здесь перевод переводит другое предложение, и знак ничего не исправит:
получится неверный вопрос вместо неверного утверждения. Такие ячейки
скрипт не трогает — они идут в разбор глазами.

КАК ОТЛИЧАЕТСЯ ОДНО ОТ ДРУГОГО. По вопросительному слову или частице в
переводе: английское «what/is/do», польское «czy/jaki», украинское
«який/де/скільки», турецкая частица «mı/mi/mu/mü». Если их нет, ячейка
считается сомнительной и остаётся человеку — даже если на самом деле знак
там единственное, чего не хватает. Славянский вопрос «Тут є вільне місце»
отличается от утверждения только интонацией, и формально этого не видно;
лучше оставить такую ячейку человеку, чем приписать знак фразе «Столик на
дві особи, будь ласка».

Самопроверка на заведомо верных и заведомо битых строках — обязательна и
стоит перед работой: проверка, которая врёт, опаснее отсутствия проверки.

Чего скрипт НЕ делает: не меняет вежливую форму. «Nasıl hissediyorsunuz»
останется на «Вы», хотя немецкий спрашивает на «ты». Это отдельный класс,
и смешивать его с правкой знака значило бы прятать одну правку внутри
другой.

    python -m app.scripts.fix_question_marks_translations            # показать
    python -m app.scripts.fix_question_marks_translations --apply    # применить
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402
from app.scripts.scan_question_mark import LANGS, is_question  # noqa: E402

# Вопросительное начало — по языкам. Только однозначное: «what», «czy»,
# «який». Утверждение, начинающееся так же, здесь не встречается, а если
# встретится, то ячейка всё равно верная по смыслу.
QUESTION_FORM = {
    "en": re.compile(
        r"^(what|where|when|why|how|which|who|whom|whose|"
        r"do|does|did|is|are|am|was|were|can|could|will|would|shall|should|"
        r"may|might|have|has|had)\b", re.IGNORECASE),
    "ru": re.compile(
        r"^(что|чего|чему|кто|кого|кому|где|куда|откуда|когда|как|какой|"
        r"какая|какое|какие|какого|каком|сколько|почему|зачем|чей|чья|чьё|"
        r"чьи|разве|неужели)\b", re.IGNORECASE),
    "uk": re.compile(
        r"^(що|чого|чому|хто|кого|кому|де|куди|звідки|коли|як|який|яка|яке|"
        r"які|якого|якому|скільки|навіщо|чий|чия|чиє|чиї|хіба|невже)\b",
        re.IGNORECASE),
    "pl": re.compile(
        r"^(czy|co|czego|czemu|kto|kogo|komu|gdzie|dokąd|skąd|kiedy|jak|jaki|"
        r"jaka|jakie|jakiego|który|która|które|ile|dlaczego|czyj|czyja)\b",
        re.IGNORECASE),
    # Турецкий спрашивает частицей в конце — она же несёт лицо:
    # «mı, misin, musunuz». Плюс вопросительные слова, которые стоят внутри.
    "tr": re.compile(
        r"(\bm[iıuü](sin|siniz|sın|sınız|yım|yim)?\s*$|"
        r"\b(ne|nerede|nereye|nereden|neden|niçin|niye|kaç|kaçta|hangi|"
        r"nasıl|kim|kimin|kime)\b)", re.IGNORECASE),
}

# Турецкое «ne» бывает и не вопросом: «ne yazık ki» — «к сожалению»,
# «ne … ne» — «ни … ни». Без этого исключения проверка приписала бы знак
# фразе «Çiçek ne yazık ki ölü».
TR_NOT_QUESTION = re.compile(
    r"\bne (yazık|de olsa|var ne yok)\b|\bne\b.*\bne\b", re.IGNORECASE)

# Строки, которым знак дописать НАДО
MUST_APPEND = [
    ("en", "What is your address"),
    ("en", "Do you have an eraser"),
    ("en", "Is there a free seat here"),
    ("ru", "Где карта"),
    ("uk", "Яка твоя адреса"),
    ("uk", "Скільки це коштує"),
    ("pl", "Jaki jest twój adres"),
    ("tr", "Harita nerede"),
    ("tr", "Yeterince paran var mı"),
    ("tr", "Burada boş yer var mı"),
    ("tr", "Kaç kişisiniz"),
]
# Строки, которые трогать НЕЛЬЗЯ: это другое предложение, а не потерянный знак
MUST_SKIP = [
    ("en", "The little dog is called Rex"),
    ("en", "I drink apple juice"),
    ("en", "She likes to read before bed"),
    ("en", "We go to the department store"),
    ("uk", "Столик на дві особи, будь ласка"),
    ("uk", "Назви мені рік"),
    ("uk", "Прочитай мені цей лист"),
    ("pl", "Proszę podać imię i nazwisko"),
    ("pl", "W formularzu wpisz swój stan cywilny"),
    ("tr", "Yeni telefon bana çok pahalıya mal oldu"),
    ("tr", "Elma suyu içiyorum"),
    ("tr", "Bir kitap okuyor"),
    ("tr", "Çiçek ne yazık ki ölü"),      # «ne yazık ki» — «к сожалению»
    # Вопрос без частицы: формально не отличается от утверждения, и по
    # правилу этого скрипта такая ячейка идёт человеку, а не под знак
    ("pl", "Chcesz coś do picia"),
    ("uk", "Тут є вільне місце"),
]


def has_question_form(lang: str, s: str) -> bool:
    s = s.strip()
    if lang == "tr" and TR_NOT_QUESTION.search(s):
        return False
    pattern = QUESTION_FORM.get(lang)
    return bool(pattern and pattern.search(s))


def selfcheck() -> None:
    print("=== самопроверка шаблонов ===")
    bad = False
    for lang, s in MUST_APPEND:
        if not has_question_form(lang, s):
            print(f"  ПРОВАЛ: {lang} {s!r} — форма вопроса не опознана")
            bad = True
    for lang, s in MUST_SKIP:
        if has_question_form(lang, s):
            print(f"  ПРОВАЛ: {lang} {s!r} — зря признано вопросом")
            bad = True
    if bad:
        sys.exit("шаблоны ненадёжны — работать с ними нельзя")
    print("  шаблоны отличают потерянный знак от другой фразы\n")


def main() -> None:
    apply_mode = "--apply" in sys.argv
    show = "--show" in sys.argv
    selfcheck()

    cols = ["id", "word_de", "example_de"] + [f"example_{c}" for c in LANGS]
    engine = create_engine(settings.DATABASE_URL_SYNC)
    with engine.connect() as conn:
        rows = conn.execute(
            text(f"SELECT {', '.join(cols)} FROM words")
        ).mappings().all()

    planned: list[tuple[int, str, str, str]] = []
    manual: list[tuple[int, str, str, str, str]] = []

    for r in rows:
        de = (r["example_de"] or "").strip()
        if not de or not is_question(de):
            continue
        for lang in LANGS:
            ex = (r[f"example_{lang}"] or "").strip()
            if not ex or is_question(ex):
                continue
            if has_question_form(lang, ex):
                planned.append((r["id"], f"example_{lang}", ex, ex + "?"))
            else:
                manual.append((r["id"], r["word_de"], lang, de, ex))

    print(f"=== ячеек без знака: {len(planned) + len(manual)} ===")
    print(f"  потерян только знак — правлю: {len(planned)}")
    print(f"  потеряна вопросительная форма — человеку: {len(manual)}")
    print()

    if show:
        for wid, col, was, now in planned[:40]:
            print(f"  {wid} {col}: {was!r} → {now!r}")
        print(f"  ... всего {len(planned)}\n")
        print("Остаётся человеку:")
        for wid, word, lang, de, ex in manual[:40]:
            print(f"  {wid} {word}\n       de  {de}\n       {lang}  {ex}")
        print(f"  ... всего {len(manual)}")

    if not apply_mode:
        print("\nэто показ. Для применения — флаг --apply, "
              "для списков — --show")
        return

    with engine.begin() as conn:
        for wid, col, _, now in planned:
            conn.execute(text(f"UPDATE words SET {col} = :v WHERE id = :i"),
                         {"v": now, "i": wid})
    print(f"применено: {len(planned)}")

    with engine.connect() as conn:
        bad = 0
        for wid, col, _, now in planned:
            cur = (conn.execute(
                text(f"SELECT {col} FROM words WHERE id = :i"), {"i": wid}
            ).scalar() or "").strip()
            if cur != now:
                print(f"  ТРЕВОГА: {wid} {col} не записалось")
                bad += 1
        print(f"самопроверка: не записалось {bad}")


if __name__ == "__main__":
    main()
