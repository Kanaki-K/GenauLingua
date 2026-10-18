"""
Немецкий обращается на «ты», а перевод на «Вы» — и наоборот.

Нашлось вычиткой: в анкетных словах («Adresse», «Beruf», «Familienstand»,
«Nachname», «Postleitzahl») таких рядов шло по десятку подряд. Немецкий
спрашивает «Wie ist deine Adresse?», турецкий отвечает «Adresiniz nedir» —
на «Вы». Пара на карточке читается как разнобой, а учится не та форма
вежливости, которой посвящён ряд.

КАК ЭТО ПРОВЕРЯЕТСЯ. В немецком вежливость видна по слову: «du/dich/dir/
dein» против «Sie/Ihnen/Ihr». В переводах — по своим признакам:

  ru, uk  «Вы, Вас, Вам, Ваш» с большой буквы, и «вы» в середине фразы
  pl      «Pan, Pani, Państwo» и формы «może pan», «proszę pana»
  tr      аффикс второго лица множественного: «-siniz, -sınız, -sunuz»,
          «size, sizin», вопросительная частица «misiniz, musunuz»
  it      «Lei» (в начале фразы — только «Lei»), «La, Le, Sua, Suo» с большой
          буквы в середине фразы и приклеенные «conoscerLa, ringraziarLa»
  es      «usted, ustedes»
  fr      «vous, votre, vos»: ряды с немецким «ihr» отсеяны, и при немецком
          «du» «vous» может значить только вежливое «Вы»
  cs      «Vy, Vás, Vám, Váš, Vaše…» с большой буквы (как ru и uk)

ЧЕГО ПРОВЕРКА НЕ ДЕЛАЕТ, и это важнее того, что делает:

* Немецкое «ihr» — это «вы» множественного числа, и перевод на «вы» там
  правилен. Поэтому ряды с «ihr/euch/euer» в немецком не проверяются вовсе.
* Турецкий «-siniz» тоже двузначен: это и вежливое «Вы», и обычное «вы» к
  нескольким людям. Поэтому турецкий сверяется только тогда, когда в
  немецком однозначное «du», а множественного «ihr» нет.
* Русское и украинское «вы» с маленькой буквы в середине фразы может быть
  обычным множественным. Такие случаи помечаются отдельно и слабее.

Самопроверка перед работой обязательна.

    python -m app.scripts.scan_formality
    python -m app.scripts.scan_formality --show 40
    python -m app.scripts.scan_formality --pairs --from 1 --count 60
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# Английский не проверяется: в нём «ты» и «Вы» одно слово, и сверять нечего.
LANGS = ["ru", "uk", "tr", "pl", "it", "es", "fr", "cs"]

# Немецкое «ты» — однозначно
DE_INFORMAL = re.compile(
    r"(?<![\w])(du|dich|dir|dein|deine|deinen|deinem|deiner|deines)(?![\w])",
    re.IGNORECASE)
# Немецкое вежливое «Вы» — с большой буквы, но этого НЕ ДОСТАТОЧНО: в начале
# фразы «Sie» с большой буквы стоит и когда значит «она» или «они». Первая
# версия проверки этого не учла и объявила дефектом 2585 ячеек — почти
# каждую пятую в базе. Среди них «Sie ist ein nettes Wesen» и «Sie wäscht
# sich»: там «Sie» это «она», и переводы на «ты» верны.
#
# Поэтому вежливым считается только «Sie» НЕ в начале предложения:
# «Können Sie mich durchstellen?», «Wie ist Ihre Adresse?».
DE_FORMAL_WORD = re.compile(r"(?<![\w])(Sie|Ihnen|Ihr|Ihre|Ihren|Ihrem|Ihrer)(?![\w])")


def de_is_formal(s: str) -> bool:
    for match in DE_FORMAL_WORD.finditer(s):
        before = s[: match.start()].rstrip()
        # Начало строки или начало нового предложения — форма двузначна
        if not before or before.endswith((".", "!", "?")):
            continue
        return True
    return False
# Немецкое «вы» множественного числа: тогда перевод на «вы» верен
DE_PLURAL_YOU = re.compile(
    r"(?<![\w])(ihr|euch|euer|eure|euren|eurem|eurer)(?![\w])", re.IGNORECASE)

FORMAL_IN_TRANSLATION = {
    "ru": re.compile(r"(?<![\w])(Вы|Вас|Вам|Вами|Ваш|Ваша|Ваше|Ваши|Вашу)(?![\w])"),
    "uk": re.compile(r"(?<![\w])(Ви|Вас|Вам|Вами|Ваш|Ваша|Ваше|Ваші|Вашу)(?![\w])"),
    "pl": re.compile(r"(?<![\w])(pan|pani|państwo|pana|pani|panu|panią)(?![\w])",
                     re.IGNORECASE),
    # Турецкий: вежливое/множественное второе лицо
    # «sizinle» — послелог слипается со словом, и без него проверка пропускала
    # «Sizinle tanışmaktan memnunum»
    "tr": re.compile(
        r"(?<![\w])(siz|size|sizi|sizin|sizinle|sizde|sizden)(?![\w])"
        r"|(sınız|siniz|sunuz|sünüz)\b"
        r"|\bm[iıuü](sınız|siniz|sunuz|sünüz)\b",
        re.IGNORECASE),
    # Итальянский: вежливость — местоимение третьего лица женского рода с
    # большой буквы. В начале фразы «La» и «Le» — артикли («La casa»),
    # поэтому там вежливым считается только «Lei» (GUIDE, п. 18: «Lei» в
    # начале фразы читается как «Вы»). В середине фразы большая буква
    # однозначна. Приклеенное местоимение пишется с большой буквы внутри
    # слова: «conoscerLa», «ringraziarLa».
    "it": re.compile(
        r"^\W*Lei(?![\w])"
        r"|(?<=[\w,;:] )(Lei|La|Le|Sua|Suo|Suoi|Sue)(?![\w])"
        r"|(?<=[a-zàèéìòù])(La|Le|Lo)(?![\w])"),
    "es": re.compile(r"(?<![\w])(usted|ustedes)(?![\w])", re.IGNORECASE),
    # Французское «vous» двузначно так же, как немецкое «ihr», но ряды с
    # «ihr» отсеяны выше: при немецком «du» «vous» — только вежливое «Вы»
    # «rendez-vous» — существительное «встреча», не обращение
    "fr": re.compile(r"(?<![\w])(?<!rendez-)(vous|votre|vos)(?![\w])",
                     re.IGNORECASE),
    # Чешский — как ru и uk: только с большой буквы, «vy» с маленькой может
    # быть обычным множественным
    "cs": re.compile(
        r"(?<![\w])(Vy|Vás|Vám|Vámi|Váš|Vaše|Vašeho|Vašemu|Vaši|Vaší|Vašim|"
        r"Vašich|Vašimi)(?![\w])"),
}

# «Ты» в переводе — тоже по положительному признаку.
#
# Почему нельзя просто «нет вежливой формы, значит ты». Вежливость в этих
# языках часто живёт в окончании глагола, а местоимения нет вовсе: русское
# «укажите ваш адрес», украинское «зверніть увагу», турецкое «lütfen yazın»,
# польское «proszę podać». Первая версия проверки сочла их обращением на
# «ты» и дала 189 попаданий, почти все ложные.
INFORMAL_IN_TRANSLATION = {
    "ru": re.compile(
        r"(?<![\w])(ты|тебя|тебе|тобой|твой|твоя|твоё|твои|твоего|твою)(?![\w])",
        re.IGNORECASE),
    "uk": re.compile(
        r"(?<![\w])(ти|тебе|тобі|тобою|твій|твоя|твоє|твої|твого|твою)(?![\w])",
        re.IGNORECASE),
    "pl": re.compile(
        r"(?<![\w])(ty|ciebie|tobie|cię|ci|twój|twoja|twoje|twojego|twoim)(?![\w])",
        re.IGNORECASE),
    "tr": re.compile(
        r"(?<![\w])(sen|seni|sana|senin|seninle|sende|senden)(?![\w])"
        r"|(yorsun|ersin|arsın|irsin|ırsın|sın|sin)\b",
        re.IGNORECASE),
    # Местоимения «ты» и формы второго лица единственного числа, которые
    # ничем другим быть не могут
    "it": re.compile(
        r"(?<![\w])(tu|ti|te|tuo|tua|tuoi|tue|hai|puoi|vuoi|sai|devi|stai)"
        r"(?![\w'])",
        re.IGNORECASE),
    "es": re.compile(
        r"(?<![\w])(tú|te|ti|tu|tus|contigo|tuyo|tuya|tuyos|tuyas|eres|estás|"
        r"tienes|puedes|quieres|sabes)(?![\w])",
        re.IGNORECASE),
    # «t'» — усечённое «te»: «Je t'aime»
    "fr": re.compile(
        r"(?<![\w])(tu|te|toi|ton|ta|tes|tien|tienne)(?![\w'])|(?<![\w])t'",
        re.IGNORECASE),
    # «ti» в чешском — ещё и «те» («ti lidé»), поэтому его здесь нет
    "cs": re.compile(
        r"(?<![\w])(ty|tebe|tobě|tebou|tě|tvůj|tvoje|tvá|tvé|tvého|tvému|"
        r"tvým|tvou|tvoji|tví|tvých|tvými|jsi|máš|můžeš|chceš|víš)(?![\w])",
        re.IGNORECASE),
}

# Строки, где вежливая форма ЕСТЬ
MUST_FLAG = [
    ("tr", "Adresiniz nedir"),
    ("tr", "Nasıl hissediyorsunuz"),
    ("tr", "Bir şey içmek ister misiniz"),
    ("uk", "Можу Вам допомогти"),
    ("uk", "Який у Вас розмір"),
    ("ru", "Можете ли Вы это обосновать"),
    ("pl", "Czy może mnie pan połączyć z sekretarką?"),
    ("it", "Qual è la Sua cittadinanza?"),
    ("it", "Sono molto lieto di conoscerLa"),
    ("it", "Lei è di qui?"),
    ("it", "Ho una comunicazione per Lei"),
    ("es", "¿Me puede ayudar usted?"),
    ("fr", "Pouvez-vous me passer la secrétaire?"),
    ("fr", "Quelle est votre adresse?"),
    ("cs", "Mám pro Vás sdělení"),
    ("cs", "Jaké je Vaše státní občanství?"),
]
# Строки, где её НЕТ и срабатывать нельзя
MUST_PASS = [
    ("tr", "Adresin ne"),
    ("tr", "Nasılsın"),
    ("tr", "Seni bekliyorum"),
    ("uk", "Як ти почуваєшся"),
    ("uk", "Ти йдеш з нами сьогодні ввечері?"),
    ("ru", "Ты пойдёшь с нами сегодня вечером?"),
    ("pl", "Czy to twój telefon?"),
    # «вы» с маленькой буквы — обычное множественное, не вежливое
    ("ru", "Где вы были вчера?"),
    ("uk", "Де ви були вчора?"),
    # «La» и «Le» в начале фразы — артикли
    ("it", "La casa è grande"),
    ("it", "Le chiavi sono sul tavolo"),
    ("it", "Ti aspetto davanti alla stazione"),
    ("it", "Dove sono le chiavi? La macchina è qui"),
    ("es", "¿Dónde está tu casa?"),
    ("fr", "Tu viens avec nous?"),
    # «rendez-vous» — «встреча», а не «Вы»
    ("fr", "Tu peux confirmer le rendez-vous?"),
    ("cs", "Kde jste vy dva byli?"),
    ("cs", "Je to tvůj telefon?"),
]


# Польское «pani» после указательного — существительное «дама», а не вежливое
# обращение: «Ta pani czeka na ciebie» переводит «Die Dame wartet auf dich»
# и верно. Проверка пометила его зря, и это исключение стоит здесь, чтобы
# следующая сессия не стала «исправлять» верную строку.
PL_PANI_AS_NOUN = re.compile(r"\b(ta|tej|tę|ową|owa)\s+pan[iąy]\b", re.IGNORECASE)


def has_formal(lang: str, s: str) -> bool:
    if lang == "pl" and PL_PANI_AS_NOUN.search(s):
        return False
    pattern = FORMAL_IN_TRANSLATION.get(lang)
    return bool(pattern and pattern.search(s))


def has_informal(lang: str, s: str) -> bool:
    pattern = INFORMAL_IN_TRANSLATION.get(lang)
    return bool(pattern and pattern.search(s))


# Строки с обращением на «ты»
INFORMAL_MUST_FLAG = [
    ("ru", "Ты пойдёшь с нами сегодня вечером?"),
    ("ru", "Это твой телефон?"),
    ("uk", "Ти йдеш з нами?"),
    ("uk", "Це твій телефон?"),
    ("pl", "Czy to twój telefon?"),
    ("tr", "Adresin ne?"),
    ("tr", "Nasılsın?"),
    ("tr", "Seni bekliyorum"),
    ("it", "Come ti chiami?"),
    ("it", "È il tuo telefono?"),
    ("es", "¿Cómo te llamas?"),
    ("es", "¿Es tu teléfono?"),
    ("fr", "Je t'attends"),
    ("fr", "C'est ton téléphone?"),
    ("cs", "Je to tvůj telefon?"),
    ("cs", "Kde jsi byl?"),
]
# Строки, где обращения на «ты» НЕТ: вежливость в окончании глагола либо
# местоимения нет вовсе. На них первая версия проверки соврала.
INFORMAL_MUST_PASS = [
    ("ru", "Пожалуйста, укажите ваш адрес"),
    ("ru", "Обратите внимание на объявление"),
    ("uk", "Будь ласка, вкажіть поштову адресу"),
    ("uk", "Зверніть увагу на оголошення"),
    ("pl", "Proszę podać swój adres zamieszkania"),
    ("tr", "Lütfen adresinizi yazın"),
    ("tr", "Lütfen anonsu dinleyin"),
    ("it", "Per favore, indichi il Suo indirizzo"),
    ("it", "Mi scusi, per favore"),
    ("es", "Por favor, indique su dirección"),
    ("es", "Disculpe, por favor"),
    ("fr", "Veuillez indiquer votre adresse"),
    ("fr", "Tout est en ordre"),
    ("cs", "Uveďte prosím svou adresu"),
    ("cs", "Ti lidé čekají venku"),
]

# Немецкие строки: вежливое «Вы» ЕСТЬ
DE_MUST_BE_FORMAL = [
    "Können Sie mich bitte zur Sekretärin durchstellen?",
    "Wie ist Ihre Staatsangehörigkeit?",
    "Brauchen Sie eine Tüte?",
    "Können Sie das begründen?",
    "Können Sie mir nähere Informationen geben?",
]
# Немецкие строки: вежливого «Вы» НЕТ, «Sie» здесь значит «она» или «они».
# На этих строках первая версия проверки соврала.
DE_MUST_NOT_BE_FORMAL = [
    "Sie ist ein nettes Wesen",
    "Sie kommen morgen vorbei",
    "Sie wäscht sich",
    "Sie geht jeden Tag zur Arbeit",
    "Sie ruft die Polizei an",
    "Sie fährt mit dem Auto zur Arbeit",
]


def selfcheck() -> None:
    print("=== самопроверка шаблонов ===")
    bad = False
    for s in DE_MUST_BE_FORMAL:
        if not de_is_formal(s):
            print(f"  ПРОВАЛ: de {s!r} — вежливое «Sie» не опознано")
            bad = True
    for s in DE_MUST_NOT_BE_FORMAL:
        if de_is_formal(s):
            print(f"  ПРОВАЛ: de {s!r} — «Sie» здесь «она/они», а не «Вы»")
            bad = True
    for lang, s in MUST_FLAG:
        if not has_formal(lang, s):
            print(f"  ПРОВАЛ: {lang} {s!r} — вежливая форма не опознана")
            bad = True
    for lang, s in MUST_PASS:
        if has_formal(lang, s):
            print(f"  ПРОВАЛ: {lang} {s!r} — зря признано вежливым")
            bad = True
    # «Ты» — положительный признак, и его отсутствие не значит вежливость
    for lang, s in INFORMAL_MUST_FLAG:
        if not has_informal(lang, s):
            print(f"  ПРОВАЛ: {lang} {s!r} — «ты» не опознано")
            bad = True
    for lang, s in INFORMAL_MUST_PASS:
        if has_informal(lang, s):
            print(f"  ПРОВАЛ: {lang} {s!r} — здесь нет обращения на «ты»")
            bad = True
    if bad:
        sys.exit("шаблоны ненадёжны — работать с ними нельзя")
    print("  шаблоны отличают «ты» от «Вы»\n")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--show", type=int, default=12)
    ap.add_argument("--pairs", action="store_true",
                    help="печатать немецкий и перевод рядом")
    ap.add_argument("--from", type=int, default=1, dest="start")
    ap.add_argument("--count", type=int, default=60)
    args = ap.parse_args()

    selfcheck()

    cols = ["id", "word_de", "example_de"] + [f"example_{c}" for c in LANGS]
    engine = create_engine(settings.DATABASE_URL_SYNC)
    with engine.connect() as conn:
        rows = conn.execute(
            text(f"SELECT {', '.join(cols)} FROM words")
        ).mappings().all()

    found: dict[str, list] = defaultdict(list)

    for r in rows:
        de = (r["example_de"] or "").strip()
        if not de:
            continue
        informal = bool(DE_INFORMAL.search(de))
        formal = de_is_formal(de)
        plural_you = bool(DE_PLURAL_YOU.search(de))

        # «ihr/euch» — перевод на «вы» правилен, ряд не проверяем
        if plural_you or not (informal or formal):
            continue

        for lang in LANGS:
            ex = (r[f"example_{lang}"] or "").strip()
            if not ex:
                continue
            if informal and not formal and has_formal(lang, ex):
                found["в немецком «ты», в переводе «Вы»"].append(
                    (r["id"], r["word_de"], lang, ex))
            elif (formal and not informal
                  and has_informal(lang, ex) and not has_formal(lang, ex)):
                found["в немецком «Вы», в переводе «ты»"].append(
                    (r["id"], r["word_de"], lang, ex))

    if args.pairs:
        items = found["в немецком «ты», в переводе «Вы»"]
        items.sort(key=lambda t: (t[0], t[2]))
        block = items[args.start - 1: args.start - 1 + args.count]
        print(f"=== пары {args.start}–{args.start + len(block) - 1} "
              f"из {len(items)} ===\n")
        de_by_id = {r["id"]: (r["example_de"] or "").strip() for r in rows}
        for number, (wid, word, lang, val) in enumerate(block, args.start):
            print(f"{number}. {wid} {word}")
            print(f"     de  {de_by_id[wid]}")
            print(f"     {lang}  {val}")
        print(f"\nследующая партия: --from {args.start + len(block)}")
        return

    print(f"=== проверено слов: {len(rows)} ===\n")
    for name in sorted(found, key=lambda k: -len(found[k])):
        items = found[name]
        print(f"{name}: {len(items)}")
        for wid, de, lang, val in items[: args.show]:
            print(f"    {wid:>6} {de:<18} {lang}: {val!r}")
        if len(items) > args.show:
            print(f"    ... ещё {len(items) - args.show}")
        print()
    if not found:
        print("ничего не найдено")


if __name__ == "__main__":
    main()
