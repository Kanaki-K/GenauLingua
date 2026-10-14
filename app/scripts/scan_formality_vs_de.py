"""Немецкий эталон на «ты», а турецкий перевод — на «вы».

Класс нашёлся в блоках 69 и 70: немецкий говорит «Zeig deinen
Personalausweis», «Gib dein Kennwort ein», «Füll das
Überweisungsformular aus», «Geh zur Startseite», а турецкий отвечает
вежливым множественным — «Kimlik kartınızı gösterin», «Şifrenizi
girin», «Havale formunu doldurun», «Ana sayfaya gidin». Девять рядов
за два блока, значит класс.

Почему именно турецкий. У него вежливость размечена суффиксом, и
суффикс однозначен: `-ınız/-iniz/-unuz/-ünüz` — это притяжательное
или повелительное второго лица МНОЖЕСТВЕННОГО числа, другого чтения
нет. У украинского и русского такого признака нет: «прочитайте» это
и вежливое «вы», и обращение к нескольким людям, а различить их можно
только по смыслу фразы. Поэтому примета берёт одну сторону класса
из пяти, и это честная цена за точность.

Как определяется, что немецкий на «ты». Не по глаголу — немецкое
повелительное на «ты» это голая основа (`Geh`, `Zeig`, `Füll`), и
отличить её от существительного регулярка не может. Признак берётся
по местоимению: в эталоне есть `du`, `dein…`, `dich`, `dir` — и НЕТ
вежливых `Sie`, `Ihr…`, `Ihnen`. Так отсеиваются и вежливые ряды, и
те, где обращения нет вовсе.

Чего примета не видит:
  • ряды без местоимения вообще («Entsorgen Sie den Müll
    ordnungsgerecht» видна, а «Tabelle ausfüllen» — нет);
  • украинскую и русскую половину класса (см. выше);
  • обратное направление — немецкий на «Sie», турецкий на «ты».
    Оно встречается реже и ловится глазами; добавить его сюда нельзя,
    потому что турецкое повелительное на «ты» это голая основа,
    и отличить её от существительного регулярка опять не сможет.

Гейтом быть не может: `-ınız` бывает законным, когда немецкий
ряд обращён к одному человеку, а турецкая фраза — к нескольким
(«Kinder, …»). Белый список по (id) для таких случаев.

    python -m app.scripts.scan_formality_vs_de
"""

from __future__ import annotations

import re
import sys

from sqlalchemy import create_engine, text

from app.config import settings

# Неформальное обращение в немецком: только по местоимению.
INFORMAL_DE = re.compile(r"\b(du|dein\w*|dich|dir)\b", re.IGNORECASE)
# Вежливое обращение в немецком. `Sie`/`Ihr` с заглавной: строчное
# `sie` это «она»/«они», а `ihr` — «вы» на «ты» во множественном.
FORMAL_DE = re.compile(r"\b(Sie|Ihr|Ihre|Ihren|Ihrem|Ihrer|Ihres|Ihnen)\b")

# Турецкая вежливость, признак первый: притяжательное или личное
# второго лица множественного числа. Границы слова после суффикса НЕТ
# намеренно: за ним ещё идёт падеж — `kartınızı`, `şifrenizi`,
# `numaranızdan`. Сочетание букв `ınız/iniz/unuz/ünüz` внутри слова
# другого чтения в турецком не имеет.
# Гласная перед `n` необязательна: после согласной суффикс выглядит как
# `-ınız` (`kart` → `kartınız`), после гласной берёт буфер `n` и
# выглядит как `-niz` (`şifre` → `şifreniz`).
FORMAL_TR_POSS = re.compile(r"[ıiuü]?n[ıiuü]z|\bsizin?\b")
# Слова, внутри которых то же сочетание букв стоит по своему праву:
# `deniz` это море, а не «ваш». Сверка по началу слова, чтобы падежи
# (`denizde`, `denizin`) отсеивались тоже.
NOT_POSS = ("deniz", "temiz", "beniz", "peniz")

# Признак второй: вежливое повелительное `-ın/-in/-un/-ün`. Оно
# короткое и омонимично родительному падежу (`evin` — дома чего-то),
# поэтому берётся только ПОСЛЕДНЕЕ слово фразы: родительный на конце
# предложения в турецком не стоит, он требует определяемого после себя.
IMPERATIVE_TR = re.compile(r"^\w{4,}(ın|in|un|ün)$")
# Что на `-in` похоже, но вежливым повелительным не является:
#   • `-dın/-tın` — второе лицо ЕДИНСТВЕННОГО числа прошедшего
#     времени («geldin» — ты пришёл), то есть ровно наоборот;
#   • `-sın/-sin/-sun/-sün` — второе лицо единственного в настоящем
#     и в именном сказуемом («istiyorsun», «akıllısın»), тоже «ты».
#     Без этого исключения примета дала 207 попаданий, почти все
#     ложные: турецкое «ты» само кончается на те же две буквы;
#   • `-sun/-sün` ещё и третье лицо желательного («Tanrı korusun»).
# Вежливое повелительное на `-sın` в турецком не оканчивается
# (gösterin, girin, doldurun, okuyun), поэтому исключение безопасно.
NOT_IMPERATIVE = re.compile(r"(d|t|s)(ın|in|un|ün)$")
STOP_TR = {"için", "yarın", "benim", "senin", "kimin", "bütün", "yakın",
           "sabahın", "bunun", "onun", "altın", "yarım"}


# Явное «ты» в самой турецкой фразе снимает подозрение целиком. Нужно
# из-за притяжательного второго лица единственного: «hayalin» (твоя
# мечта) кончается на те же буквы, что и вежливое повелительное, и
# различить их по форме нельзя — а по соседнему «senin» можно.
INFORMAL_TR = re.compile(r"\b(sen|senin|sana|seni|seninle)\b")


def formal_tr(tr: str) -> bool:
    if INFORMAL_TR.search(tr.lower()):
        return False
    for word in re.findall(r"\w+", tr.lower()):
        if word.startswith(NOT_POSS):
            continue
        if FORMAL_TR_POSS.search(word):
            return True
    last = tr.rstrip("?!.").split()[-1].lower() if tr.split() else ""
    if last in STOP_TR or NOT_IMPERATIVE.search(last):
        return False
    return bool(IMPERATIVE_TR.match(last))

# Ряды, где турецкое множественное законно: немецкий обращён к одному,
# турецкий — к нескольким, и это не ошибка, а разный адресат.
LEGIT: set[int] = set()

GOOD = [
    # немецкий на «ты», турецкий на «ты» — так и надо
    ("Zeig deinen Personalausweis", "Kimlik kartını göster"),
    ("Gib dein Kennwort ein", "Şifreni gir"),
    # немецкий вежливый, турецкий вежливый — тоже верно
    ("Geben Sie die Kundenreferenz an", "Müşteri referansını belirtin"),
    ("Entsorgen Sie den Müll ordnungsgerecht", "Çöpü kurallara uygun şekilde atın"),
    # обращения в немецком нет — примета молчит
    ("Die Situation ist schwierig", "Durumunuz zor"),
    # «sie» строчное это «она», а не вежливое обращение
    ("Sie geht ins Sprechzimmer", "Muayene odasına gidiyor"),
]
BAD = [
    ("Zeig deinen Personalausweis", "Kimlik kartınızı gösterin"),
    ("Gib dein Kennwort ein", "Şifrenizi girin"),
    ("Füll das Überweisungsformular aus, du hast Zeit", "Havale formunu doldurun"),
    ("Wie lautet deine Kundennummer?", "Müşteri numaranız nedir?"),
]


def flagged(de: str, tr: str) -> bool:
    if not de or not tr:
        return False
    if FORMAL_DE.search(de):
        return False
    if not INFORMAL_DE.search(de):
        return False
    return formal_tr(tr)


def selfcheck() -> None:
    bad_good = [p for p in GOOD if flagged(*p)]
    good_bad = [p for p in BAD if not flagged(*p)]
    if bad_good or good_bad:
        print("САМОПРОВЕРКА НЕ ПРОШЛА")
        for de, tr in bad_good:
            print(f"  ложное срабатывание: {de!r} / {tr!r}")
        for de, tr in good_bad:
            print(f"  не поймано: {de!r} / {tr!r}")
        sys.exit(1)
    print(f"самопроверка: {len(GOOD)} чистых, {len(BAD)} грязных — ок\n")


def main() -> None:
    selfcheck()
    engine = create_engine(settings.DATABASE_URL_SYNC)
    with engine.connect() as conn:
        rows = conn.execute(
            text("SELECT id, word_de, example_de, example_tr FROM words ORDER BY id")
        ).all()

    hits = [r for r in rows if r.id not in LEGIT and flagged(r.example_de, r.example_tr)]
    for r in hits:
        print(f"id={r.id} {r.word_de}")
        print(f"  de  {r.example_de}")
        print(f"  tr  {r.example_tr}")

    print(f"\nпрочитано рядов: {len(rows)}")
    print(f"в белом списке: {len(LEGIT)}")
    print(f"расхождений в обращении: {len(hits)}")


if __name__ == "__main__":
    main()
