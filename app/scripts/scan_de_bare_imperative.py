"""
ЗАМЕР, а не примета: голая основа в повелительном немецкого эталона.

Зачем понадобилось. Второй проход дал четыре ряда подряд, где эталон
стоит в повелительном без «-e»: `Folg mir bitte` (блок 3), `Bitte zahl
hier`, `Wart mal eine Sekunde`, `Steck den Stecker in die Steckdose`
(блок 4). `scan_de_imperative` их не видит нарочно: та примета
перечисляет основы, у которых «-e» ОБЯЗАТЕЛЬНО (öffne, arbeite,
betätige), а у `folgen`, `zahlen`, `warten`… «-e» по Дудену
необязательно, и внести их туда значило бы ловить законное.

Но четыре ряда — это класс, и прежде чем править класс, надо знать,
что в базе норма. Поэтому здесь не приговор, а СЧЁТ: сколько в базе
повелительных с «-e» и сколько без него. Если база в основном пишет
полную форму, голые — выбросы и их надо править. Если наоборот —
правка блока 3 была неверной, и это надо признать.

Как ищется. Основы берутся НЕ из рук, а из самой базы: все ряды с
частью речи VERB, инфинитив минус «-en». Так список не может
«собраться по найденным примерам» — дыра, которую scan_de_colloquial
показал четыре раза.

Сильные глаголы исключены: у них голое повелительное — единственно
верная форма (komm, geh, nimm, gib, lass, halt). Список сильных задан
немецкой грамматикой, а не наблюдениями, и сопоставляется по концу
инфинитива, чтобы ловить и приставочные (anfangen → fangen).

Основы на «-el»/«-er» (ändere/ändre, handle) исключены: там сокращение
законно и вариативно.

Позиция. Повелительное отличимо от прочего только по месту: начало
фразы, после «Bitte», после запятой. Середина фразы — предмет
scan_de_colloquial («Ich zahl nicht»).

Самопроверка обязательна: заведомо верные строки молчат, заведомо
усечённые ловятся. Не сошлось — падаем и ничего не печатаем.

    python -m app.scripts.scan_de_bare_imperative
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# Сильные и неправильные глаголы: у них повелительное БЕЗ «-e» — норма,
# а часто и единственная форма. Список из немецкой грамматики, не из
# наблюдений. Сверяется по концу инфинитива: «anfangen» кончается на
# «fangen», значит сильный.
STRONG = """
backen befehlen beginnen beissen beißen bergen bersten betrügen biegen bieten
binden bitten blasen bleiben braten brechen brennen bringen denken dringen
dürfen empfehlen erlöschen erschrecken essen fahren fallen fangen fechten
finden fliegen fliehen fließen fressen frieren gebären geben gedeihen gehen
gelingen gelten genesen genießen geschehen gewinnen gießen gleichen gleiten
graben greifen haben halten hängen hauen heben heissen heißen helfen kennen
klingen kneifen kommen können kriechen laden lassen laufen leiden leihen lesen
liegen lügen mahlen meiden melken messen misslingen mögen müssen nehmen nennen
pfeifen preisen quellen raten reiben reissen reißen reiten rennen riechen
ringen rinnen rufen saufen saugen schaffen scheiden scheinen schelten scheren
schieben schiessen schießen schinden schlafen schlagen schleichen schleifen
schliessen schließen schlingen schmeissen schmeißen schmelzen schneiden
schreiben schreien schreiten schweigen schwellen schwimmen schwinden schwingen
schwören sehen sein senden singen sinken sinnen sitzen sollen spinnen sprechen
spriessen sprießen springen stechen stehen stehlen steigen sterben stinken
stossen stoßen streichen streiten tragen treffen treiben treten trinken trügen
tun verderben vergessen verlieren verzeihen wachsen waschen weichen weisen
wenden werben werden werfen wiegen winden wissen wollen ziehen zwingen
""".split()

# Приставки, которые отделяются: у «anfangen» повелительное — «fang … an»,
# значит основу надо искать и от остатка.
SEPARABLE = (
    "ab", "an", "auf", "aus", "bei", "da", "durch", "ein", "entgegen", "fest",
    "fort", "her", "herum", "hin", "los", "mit", "nach", "um", "vor", "weg",
    "weiter", "wieder", "zu", "zurück", "zusammen",
)


def syllabic_el_er(stem: str) -> bool:
    """Кончается ли основа слоговым «-el»/«-er».

    У таких основ (`änder`, `handel`, `sammel`) немецкий законно
    сокращает двумя способами — `ändere`/`ändre`, — и голая основа от
    них на письме неотличима от выбора стиля.

    НО отбрасывать по одному виду букв нельзя: у всех глаголов на
    `-ieren` основа тоже кончается на «er» (`kontrollier`,
    `reparier`, `telefonier`, `organisier`), а там никакого слогового
    «-er» нет — это корень. Первая версия приметы выбрасывала их все,
    и замер «99 против 41» был занижен: `Bitte kontrollier die
    Rechnung` в счёт не попал.

    Различает их буква перед «el»/«er»: у слогового окончания там
    согласная (`änd-er`), у корня — гласная (`kontroll-i-er`).
    """
    if not stem.endswith(("el", "er")):
        return False
    return len(stem) > 2 and stem[-3] not in "aeiouäöü"


def is_obligatory_e(infinitive: str) -> bool:
    """Обязательно ли «-e» в повелительном.

    Основа на «-t», «-d», «-ig» или на «-n» после согласной требует «-e»:
    `warte`, `arbeite`, `beruhige`, `öffne`. Голой формы у них в немецком
    нет вообще, поэтому это не стиль, а ошибка.
    """
    stem = infinitive[:-2] if infinitive.endswith("en") else infinitive
    if stem.endswith(("t", "d", "chn", "ffn", "rdn", "ppn", "tm")):
        return True
    # «-ig» требует «-e» только когда это суффикс: beruhig-, entschuldig-,
    # betätig-. У `zeigen`/`neigen` «ig» — часть корня (дифтонг «ei»), и
    # «Zeig mir den Weg» совершенно верно. Различает их буква перед «ig»:
    # у суффикса там согласная, у корня — гласная.
    return stem.endswith("ig") and len(stem) > 2 and stem[-3] not in "aeiouäöü"


def is_strong(infinitive: str) -> bool:
    """Сильный ли глагол: сверка по концу инфинитива, чтобы ловить приставочные."""
    low = infinitive.lower()
    return any(low == s or low.endswith(s) for s in STRONG)


def function_words(conn) -> set[str]:
    """Служебные слова базы: местоимения, артикли, числительные, частицы.

    Берутся ИЗ БАЗЫ, а не из рук. Нужны потому, что основа слабого глагола
    может совпасть со служебным словом: `meinen` даёт основу `mein`, и
    «Mein Zimmer ist klein» иначе попало бы в улов. Совпадения с
    СУЩЕСТВИТЕЛЬНЫМИ нарочно не исключаются: `zahl`/`Zahl` — как раз
    тот случай, который надо видеть, а не прятать.
    """
    rows = conn.execute(
        text(
            "SELECT word_de FROM words WHERE word_de IS NOT NULL AND pos IN "
            "('PRONOUN','OTHER','PREPOSITION','CONJUNCTION','ADVERB','ADJECTIVE')"
        )
    ).scalars()
    out: set[str] = set()
    for raw in rows:
        for part in str(raw).split(","):
            part = part.strip().lower()
            if part and " " not in part:
                out.add(part)
    return out


def stems_from_base(conn, skip: set[str]) -> dict[str, str]:
    """Основы слабых глаголов → инфинитив, из которого основа взята."""
    rows = conn.execute(
        text("SELECT word_de FROM words WHERE pos = 'VERB' AND word_de IS NOT NULL")
    ).scalars()
    out: dict[str, str] = {}
    for raw in rows:
        for inf in (p.strip() for p in str(raw).split(",")):
            inf = inf.replace("sich ", "").strip()
            if not inf or " " in inf or not inf.endswith("en"):
                continue
            if is_strong(inf):
                continue
            stem = inf[:-2]
            if syllabic_el_er(stem):
                continue
            if len(stem) < 3 or stem.lower() in skip:
                continue
            out.setdefault(stem.lower(), inf)
            # приставочный: добавить и основу остатка (fang от anfangen)
            for pref in SEPARABLE:
                if inf.startswith(pref) and len(inf) > len(pref) + 3:
                    rest = inf[len(pref):]
                    if rest.endswith("en") and not is_strong(rest):
                        bare = rest[:-2]
                        if len(bare) >= 3 and not syllabic_el_er(bare) \
                                and bare.lower() not in skip:
                            out.setdefault(bare.lower(), rest)
    return out


def positions(sentence: str) -> list[str]:
    """Слова в позиции повелительного: начало фразы, после «Bitte», после запятой."""
    out: list[str] = []
    for chunk in re.split(r"[,;:!?]|\.\s", sentence):
        chunk = chunk.strip()
        if not chunk:
            continue
        words = chunk.split()
        if not words:
            continue
        first = words[0].strip(".,!?»«\"'").lower()
        if first == "bitte" and len(words) > 1:
            out.append(words[1].strip(".,!?»«\"'").lower())
        else:
            out.append(first)
    return out


def selfcheck(stems: dict[str, str]) -> None:
    good = [
        "Komm her",                       # сильный: голое — норма
        "Gib mir das Buch",               # сильный
        "Nimm Kontakt auf",               # сильный
        "Lass das bitte",                 # сильный
        "Geh nach Hause",                 # сильный
        "Warte mal eine Sekunde",         # слабый, но с «-e»
        "Bitte zahle hier",               # слабый с «-e» после Bitte
        "Öffne das Fenster, bitte",       # «-e» обязательно, предмет другой приметы
        "Ich zahl nicht",                 # середина фразы: предмет scan_de_colloquial
        "Der Zug fährt ab",               # не повелительное вовсе
        "Mein Zimmer ist klein",          # основа `mein` от `meinen` — служебное слово
        "Wo wart ihr?",                   # прошедшее от sein: `wart` не в начале фразы
        "Laut der Untersuchung ist alles gut",  # `laut` — предлог, не основа от lauten
    ]
    bad = [
        "Bitte zahl hier",
        "Wart mal eine Sekunde",
        "Steck den Stecker in die Steckdose",
        "Folg mir bitte",
        "Frag ihn doch",
        "Hol mir bitte Wasser",
    ]
    # отдельно проверяем сам разбор «обязательно ли -e»
    for inf in ("warten", "arbeiten", "beruhigen", "öffnen", "betätigen", "atmen"):
        if not is_obligatory_e(inf):
            print(f"САМОПРОВЕРКА НЕ ПРОШЛА: у {inf} «-e» обязательно, а разбор говорит нет")
            sys.exit(1)
    for inf in ("zeigen", "neigen", "zahlen", "machen", "folgen", "stecken"):
        if is_obligatory_e(inf):
            print(f"САМОПРОВЕРКА НЕ ПРОШЛА: у {inf} «-e» необязательно, а разбор говорит да")
            sys.exit(1)
    # слоговое «-el»/«-er» против корневого «-ier»
    for stem in ("änder", "handel", "sammel", "wander"):
        if not syllabic_el_er(stem):
            print(f"САМОПРОВЕРКА НЕ ПРОШЛА: у {stem} слоговое окончание, а разбор говорит нет")
            sys.exit(1)
    for stem in ("kontrollier", "reparier", "telefonier", "organisier"):
        if syllabic_el_er(stem):
            print(f"САМОПРОВЕРКА НЕ ПРОШЛА: у {stem} «-er» корневое, а разбор говорит слоговое")
            sys.exit(1)

    errs = []
    for s in good:
        if any(w in stems for w in positions(s)):
            errs.append(f"ложная тревога: {s!r}")
    for s in bad:
        if not any(w in stems for w in positions(s)):
            errs.append(f"пропущено: {s!r}")
    if errs:
        print("САМОПРОВЕРКА НЕ ПРОШЛА:")
        for e in errs:
            print("   ", e)
        sys.exit(1)
    print(f"самопроверка: {len(good)} правильных и {len(bad)} усечённых строк разобраны верно")


def main() -> None:
    engine = create_engine(settings.DATABASE_URL_SYNC)
    with engine.connect() as conn:
        stems = stems_from_base(conn, function_words(conn))
        selfcheck(stems)
        print(f"основ слабых глаголов из базы: {len(stems)}")

        rows = conn.execute(
            text(
                "SELECT id, word_de, example_de FROM words "
                "WHERE example_de IS NOT NULL ORDER BY id"
            )
        ).mappings().all()

    bare: list[tuple[int, str, str, str]] = []
    full: list[tuple[int, str, str, str]] = []
    for r in rows:
        for w in positions(r["example_de"]):
            if w in stems:
                bare.append((r["id"], r["word_de"], stems[w], r["example_de"]))
                break
            if w.endswith("e") and w[:-1] in stems:
                full.append((r["id"], r["word_de"], stems[w[:-1]], r["example_de"]))
                break

    print(f"\nпрочитано немецких примеров: {len(rows)}")
    print(f"повелительное с «-e»:  {len(full)}")
    print(f"повелительное без «-e»: {len(bare)}")

    # ГЕЙТ. Голая основа — выбор стиля, кроме тех основ, у которых «-e»
    # в повелительном обязательно: там голой формы в немецком просто нет.
    # Позиция снимает ту двусмысленность, из-за которой `wart` выброшено
    # из scan_de_imperative: «Wo wart ihr?» — это прошедшее от `sein`, но
    # там `wart` стоит не в начале фразы, а вторым словом.
    broken = [h for h in bare if is_obligatory_e(h[2])]
    print(f"\nиз них форм, которых в немецком НЕТ: {len(broken)}")
    for wid, word, inf, ex in broken:
        print(f"  {wid:>6}  {word:<22} ({inf})  {ex}")

    print("\n── БЕЗ «-e» ───────────────────────────────────────────────")
    for wid, word, inf, ex in bare:
        print(f"  {wid:>6}  {word:<22} ({inf})  {ex}")

    print("\n── С «-e» (для сравнения) ─────────────────────────────────")
    for wid, word, inf, ex in full:
        print(f"  {wid:>6}  {word:<22} ({inf})  {ex}")

    if broken:
        sys.exit(1)


if __name__ == "__main__":
    main()
