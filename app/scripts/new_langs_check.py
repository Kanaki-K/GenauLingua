#!/usr/bin/env python3
"""
Проверка формы переводов на it, es, fr, cs — блоков archive/new_langs/out.

Правила — archive/new_langs/GUIDE.md. Скрипт ловит то, что ловится формой:
пропуск ряда, чужой id, точку в конце, скобки и косые черты, букву не из
алфавита языка, слово без диакритики, существительное без артикля, пример
без самого слова. Смысл он не проверяет.

Две ступени: «ошибка» — блок не годен, пока она есть; «проверить» —
эвристика (неправильные глаголы дают ложные срабатывания: essere → sono),
каждую надо посмотреть глазами и оставить, если пример верен.

    python -m app.scripts.new_langs_check archive/new_langs/out/block_0000.jsonl [...]
    python -m app.scripts.new_langs_check --selftest
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

LANGS = ("it", "es", "fr", "cs")

# Буквы сверх латиницы a–z, допустимые в языке. Всё прочее буквенное —
# чужое: «ř» в итальянском, «ñ» во французском.
EXTRA_LETTERS = {
    "it": "àèéìíîòóùêç",  # ê, ç — в заимствованиях: crêpe, brioche
    "es": "áéíóúñü",
    "fr": "àâæçéèêëîïôœùûüÿ",
    "cs": "áčďéěíňóřšťúůýž",
}

ARTICLES = {
    "it": ("il ", "lo ", "la ", "i ", "gli ", "le ", "l'"),
    "es": ("el ", "la ", "los ", "las ", "lo "),  # lo — субстантивированное: «lo útil»
    "fr": ("le ", "la ", "les ", "l'"),
}

# Слова, которые без диакритики пишутся только по ошибке. Список не полон —
# это примета, а не словарь: ловит модель, потерявшую диакритику целиком.
NO_DIACRITIC = {
    "it": {"perche", "piu", "citta", "gia", "cosi", "puo", "caffe", "lunedi",
           "universita", "verita", "liberta"},
    "es": {"tambien", "facil", "dificil", "rapido", "aqui", "alli", "despues",
           "adios", "nino", "nina", "manana", "senor", "senora", "musica",
           "telefono", "arbol", "jamas", "ademas", "cancion", "estacion"},
    "fr": {"tres", "deja", "francais", "eleve", "ecole", "etre", "frere",
           "mere", "pere", "cafe", "apres", "bientot", "garcon",
           "fenetre", "bete", "theatre", "etudiant", "televiseur"},
    "cs": {"dobry", "dekuji", "muzu", "prace", "skola", "jeste", "rict",
           "mesto", "clovek", "zena", "muz", "reci", "dite", "pristi",
           "vecer", "zitra", "vcera", "ceska", "cesky"},
}

# Подряд стоящие слова-обёртки, которые снимаются при поиске слова в примере
STRIP_WORDS = {
    "it": {"l", "il", "lo", "la", "i", "gli", "le", "un", "uno", "una", "si", "di", "a", "da"},
    "es": {"el", "la", "los", "las", "un", "una", "se", "de", "a"},
    "fr": {"l", "le", "la", "les", "un", "une", "se", "s", "de", "d", "à"},
    "cs": {"se", "si"},
}

VERB_ENDINGS = {
    "it": ("are", "ere", "ire", "rre", "rsi", "rci", "rla", "rlo", "rne", "rsela", "rsene"),
    "es": ("ar", "er", "ir", "ír", "arse", "erse", "irse", "írse", "arla", "erla", "irla"),
    "fr": ("er", "ir", "re", "oir"),
    "cs": ("t", "ct", "ci", "ti", "t se", "t si", "ct se", "ct si", "ci se", "ci si", "ti se", "ti si"),
}


def fold(s: str) -> str:
    """Нижний регистр без диакритики — для поиска слова в примере."""
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if not unicodedata.combining(c))


def tokens(s: str) -> list[str]:
    return [t for t in re.split(r"[^\w]+", fold(s)) if t]


def meanings(value: str) -> list[str]:
    return [m.strip() for m in value.split(",")]


def word_in_example(lang: str, value: str, example: str) -> bool:
    """
    Есть ли в примере хоть одно значение — по общему началу слова.

    Длина общей части — длина слова минус окончание, но не меньше трёх:
    «andare» ↔ «andiamo» (and), «libro» ↔ «libri» (libr), «být» ↔ «byl» —
    нет, это и есть ложное срабатывание неправильного глагола; его
    разбирают глазами.
    """
    ex_tokens = tokens(example)
    if lang == "cs":
        # Отрицание пишется слитно: «Nezavazuj» — форма «zavazovat»
        ex_tokens += [t[2:] for t in ex_tokens if t.startswith("ne") and len(t) > 4]
    for m in meanings(value):
        words = [t for t in tokens(m) if t not in STRIP_WORDS[lang]]
        if not words:
            words = tokens(m)
        # Многословное значение («essere in grado di», «crier sur») ищется
        # по главному слову — остальные в примере законно меняют вид
        words = words[:1]
        ok = True
        for w in words:
            need = max(3, min(len(w) - 2, 6)) if len(w) > 3 else len(w)
            stem = w[:need]
            if not any(t.startswith(stem) for t in ex_tokens):
                ok = False
                break
        if ok:
            return True
    return False


def check_row(row: dict, src: dict | None) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warns: list[str] = []
    if src is not None and row.get("de") != src["de"]:
        errors.append(f"de «{row.get('de')}» не совпадает с базой «{src['de']}»")
    pos = (src or {}).get("pos", row.get("pos", ""))

    for lang in LANGS:
        for field in (lang, "ex_" + lang):
            v = row.get(field)
            if not isinstance(v, str) or not v.strip():
                errors.append(f"{field}: пусто")
                continue
            if v != v.strip() or "  " in v:
                errors.append(f"{field}: лишние пробелы")
            if v.rstrip().endswith((".", "…")) and not v.rstrip().endswith("..."):
                errors.append(f"{field}: точка в конце")
            if v.rstrip().endswith("..."):
                errors.append(f"{field}: многоточие в конце")
            if "’" in v or "‘" in v:
                errors.append(f"{field}: кривой апостроф ’ — нужен '")
            allowed = EXTRA_LETTERS[lang]
            if field.startswith("ex_"):
                # Имена в примере пишутся как в оригинале: «Herr Müller», не «Mueller»
                allowed += "äöüß"
            alien = sorted({c for c in v.lower() if c.isalpha()
                            and not ("a" <= c <= "z") and c not in allowed})
            if alien:
                errors.append(f"{field}: буквы не из языка: {''.join(alien)}")
            bare = set(tokens(v)) & NO_DIACRITIC[lang]
            # tokens() снимает диакритику, поэтому сверяем с исходным написанием
            for b in sorted(bare):
                if re.search(rf"(?<!\w){b}(?!\w)", v.lower()):
                    errors.append(f"{field}: «{b}» без диакритики")

        value = row.get(lang) or ""
        example = row.get("ex_" + lang) or ""
        if not value or not example:
            continue

        # Пометки регистра (GUIDE п.13) — единственные допустимые скобки
        marks = r"\s\((colloq|volg|coloq|vulg|fam|hovor)\.\)"
        if re.search(r"[()\[\]/;:]", re.sub(marks, "", value)):
            errors.append(f"{lang}: скобки, косая черта или двоеточие в переводе")
        ms = meanings(value)
        if any(not m for m in ms):
            errors.append(f"{lang}: пустое значение (лишняя запятая)")
        # Без диакритики сравнивать нельзя: «vymýšlet» и «vymyslet», «cómo» и
        # «como» — разные слова. Бот сравнивает значения в нижнем регистре.
        if len({m.lower() for m in ms}) != len(ms):
            errors.append(f"{lang}: значение повторяется")
        if len(ms) > 6:
            warns.append(f"{lang}: {len(ms)} значений — не синонимический ряд ли?")

        if pos == "NOUN" and lang in ARTICLES:
            for m in ms:
                if m and not m.lower().startswith(ARTICLES[lang]):
                    # Существительное в роли междометия («Ach Mist» → «accidenti»)
                    # переводится без артикля — GUIDE п.15, с пометкой в note
                    if row.get("note"):
                        warns.append(f"{lang}: без артикля (см. note): «{m}»")
                    else:
                        errors.append(f"{lang}: существительное без артикля: «{m}»")
        if pos == "VERB":
            first = ms[0].lower()
            if lang in ("it", "es", "fr") and first.startswith(("se ", "s'")):
                first = first.split(" ", 1)[-1] if first.startswith("se ") else first[2:]
            # Составной глагол («faire la connaissance», «venire qui», «mít rád»)
            # — инфинитив его первое слово; чешское «se/si» — второе
            head = first if lang == "cs" else first.split(" ")[0]
            if lang == "cs" and " " in first and first.split(" ")[1] not in ("se", "si"):
                head = first.split(" ")[0]
            # «mal comprendre», «špatně pochopit» — инфинитив не первым словом
            if not head.endswith(VERB_ENDINGS[lang]) and not any(
                    w.endswith(VERB_ENDINGS[lang]) for w in first.split(" ")):
                warns.append(f"{lang}: глагол не похож на инфинитив: «{ms[0]}»")
        # Заглавная — только у имён собственных; английская колонка подсказывает,
        # имя ли это («Germany»), а «I» — единственное иное исключение
        en = (src or {}).get("en") or "x"
        if value[:1].isupper() and not en[:1].isupper():
            warns.append(f"{lang}: перевод с заглавной")

        if re.search(r"[,:;!?](?=[^\W\d_])", example):
            errors.append(f"ex_{lang}: нет пробела после знака препинания")
        body = example.lstrip("¿¡\"«")
        if body[:1] and not body[:1].isupper() and not body[:1].isdigit():
            errors.append(f"ex_{lang}: начинается со строчной")
        if lang == "es":
            if "?" in example and "¿" not in example:
                errors.append("ex_es: вопрос без «¿»")
            if "!" in example and "¡" not in example:
                errors.append("ex_es: восклицание без «¡»")
        if lang == "es":
            # Итальянское «zz» в испанском — след соседней колонки («autorizzado»);
            # pizza, jazz — исключения, их видно глазами
            for w in re.findall(r"\w*zz\w*", (value + " " + example).lower()):
                if w not in ("pizza", "pizzas", "jazz", "pizzería", "jacuzzi"):
                    warns.append(f"es: «{w}» — итальянское zz?")
        if lang == "fr" and re.search(r"\s[?!]", example):
            errors.append("ex_fr: пробел перед ? или !")
        # Подлежащее-местоимение в начале: в it/es/cs его опускают, а it «Lei»
        # в начале фразы читается как вежливое «Вы» (GUIDE, «Lei»)
        lead = {"it": ("Lei ", "Lui "), "es": ("Ella ", "Él "), "cs": ("Ona ", "On ")}
        if example.lstrip("¿¡").startswith(lead.get(lang, ())):
            warns.append(f"ex_{lang}: местоимение-подлежащее в начале — опустить?")
        if not word_in_example(lang, value, example):
            warns.append(f"ex_{lang}: слова «{value}» в примере не видно")
        elif len(ms) > 1 and not word_in_example(lang, ms[0], example):
            # В примере стоит дальнее значение, а первое — другое (GUIDE п.19:
            # первым — значение из примера)
            warns.append(f"ex_{lang}: в примере не первое значение «{ms[0]}»")
        de_q = (src or {}).get("ex_de", "").rstrip().endswith("?")
        if de_q and not example.rstrip().endswith("?"):
            warns.append(f"ex_{lang}: немецкий пример — вопрос, этот нет")

    return errors, warns


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def check_file(path: Path) -> tuple[int, int]:
    src_path = path.parent.parent / "src" / path.name
    src_rows = load_jsonl(src_path) if src_path.exists() else []
    try:
        rows = load_jsonl(path)
    except json.JSONDecodeError as e:
        print(f"{path.name}: ОШИБКА — не JSONL: {e}")
        return 1, 0
    n_err = n_warn = 0

    if src_rows:
        want = [r["id"] for r in src_rows]
        got = [r.get("id") for r in rows]
        if got != want:
            missing = set(want) - set(got)
            extra = set(got) - set(want)
            print(f"{path.name}: ОШИБКА — ряды не совпадают с src: нет {sorted(missing)[:20]}, "
                  f"лишние {sorted(x for x in extra if x is not None)[:20]}, "
                  f"порядок {'другой' if not missing and not extra else '—'}")
            n_err += 1
    by_id = {r["id"]: r for r in src_rows}

    for row in rows:
        errors, warns = check_row(row, by_id.get(row.get("id")))
        for e in errors:
            print(f"  ОШИБКА    id={row.get('id')} {row.get('de')}: {e}")
        for w in warns:
            print(f"  проверить id={row.get('id')} {row.get('de')}: {w}")
        n_err += len(errors)
        n_warn += len(warns)
    print(f"{path.name}: рядов {len(rows)}, ошибок {n_err}, проверить {n_warn}")
    return n_err, n_warn


def selftest() -> int:
    """Заведомо верные ряды проходят без ошибок, каждый битый ловится."""
    src = {"id": 1, "de": "Buch", "pos": "NOUN", "ex_de": "Ich lese ein Buch", "en": "book"}
    good = {
        "id": 1, "de": "Buch",
        "it": "il libro", "ex_it": "Leggo un libro",
        "es": "el libro", "ex_es": "Leo un libro",
        "fr": "le livre", "ex_fr": "Je lis un livre",
        "cs": "kniha", "ex_cs": "Čtu knihu",
    }
    verb_src = {"id": 2, "de": "gehen", "pos": "VERB", "ex_de": "Wohin gehst du?", "en": "to go"}
    verb = {
        "id": 2, "de": "gehen",
        "it": "andare", "ex_it": "Dove vai?",
        "es": "ir", "ex_es": "¿Adónde vas?",
        "fr": "aller", "ex_fr": "Où vas-tu?",
        "cs": "jít", "ex_cs": "Kam jdeš?",
    }
    failures = 0
    e, _ = check_row(good, src)
    if e:
        print("ЛОЖНАЯ ОШИБКА на верном ряду:", e)
        failures += 1
    e, w = check_row(verb, verb_src)
    if e:
        print("ЛОЖНАЯ ОШИБКА на верном глаголе:", e)
        failures += 1
    if not any("ex_it" in x for x in w):
        print("неправильный глагол andare → vai должен уйти в «проверить»")
        failures += 1

    broken = [
        ({"ex_it": "Leggo un libro."}, "точка в конце"),
        ({"it": "libro"}, "без артикля"),
        ({"fr": "le livre (roman)"}, "скобки"),
        ({"cs": "kniha, Kniha"}, "повторяется"),
        ({"es": "el libro, "}, "пустое значение"),
        ({"ex_es": "Lees un libro?"}, "без «¿»"),
        ({"ex_fr": "Tu lis un livre ?"}, "пробел перед"),
        ({"ex_fr": "J’ai un livre"}, "кривой апостроф"),
        ({"cs": "kníha", "ex_cs": "Čtu knihu ñ"}, "буквы не из языка"),
        ({"it": "il librö"}, "буквы не из языка"),
        ({"fr": "le café", "ex_fr": "Un cafe"}, "без диакритики"),
        ({"it": ""}, "пусто"),
        ({"de": "Bach"}, "не совпадает"),
        ({"ex_cs": "čtu knihu"}, "строчной"),
        ({"ex_cs": "Řekl:Čtu knihu"}, "нет пробела"),
    ]
    for patch, needle in broken:
        row = {**good, **patch}
        e, _ = check_row(row, src)
        if not any(needle in x for x in e):
            print(f"НЕ ПОЙМАНО: {patch} — ждали «{needle}», получили {e}")
            failures += 1
    _, w = check_row({**good, "ex_it": "Leggo un giornale"}, src)
    if not any("не видно" in x for x in w):
        print("НЕ ПОЙМАНО: пример без слова")
        failures += 1

    print(f"самопроверка: {'ОК' if not failures else f'провалов {failures}'}")
    return failures


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        sys.exit(1 if selftest() else 0)
    total_err = 0
    for f in args.files:
        err, _ = check_file(Path(f))
        total_err += err
    sys.exit(1 if total_err else 0)


if __name__ == "__main__":
    main()
