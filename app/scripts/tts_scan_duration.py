# -*- coding: utf-8 -*-
"""
ПРИМЕТА 49: длительность клипа против длины его текста.

    python -m app.scripts.tts_scan_duration

ЗАЧЕМ ОНА НУЖНА. Проверка слухом (`tts_asr_check`) идёт по ВЫБОРКЕ: десять
клипов в минуту, 121 269 ею не покрыть — это сутки счёта. А вот обрубленный,
пустой, зацикленный или неоправданно длинный клип выдаёт себя ДЛИТЕЛЬНОСТЬЮ,
и её можно взять из заголовков кадров mp3 без раскодировки звука. Всё
хранилище — пять минут.

Это ЕДИНСТВЕННАЯ проверка озвучки со сплошным покрытием. Слух отвечает на
«то ли сказано», длительность — на «целиком ли сказано».

КАК МЕРИТ. Секунд на символ зависит и от языка, и от того, слово это или
фраза, а у коротких текстов велика постоянная часть (вдох, затухание).
Поэтому сравнение идёт не с общей медианой, а внутри КОРЗИНЫ своей длины:
клипы бьются по (язык, вид, длина // 5), берётся медиана корзины, и клип
считается выбросом, если он короче 0.5 медианы или длиннее 2.2. Корзины
меньше 20 клипов не судятся — медиана там шумная (таких ~230 клипов).

Пороги выбраны по разбросу: внутри корзины 99.99 % клипов укладываются в
диапазон, значит всё за его пределами стоит посмотреть глазами.

ЧТО НАЙДЕНО ПРИ ПЕРВОМ ПРОГОНЕ (октябрь 2026)

    судимо 121 035 клипов
    КОРОЧЕ НОРМЫ: 0
    ДЛИННЕЕ НОРМЫ: 5

**Ноль коротких — главный результат, и он отрицательный:** обрезка тишины
(`mp3_trim`) нигде не съела речь. Это ровно тот страх, из-за которого
обрезку проверяли вручную по десятку клипов; теперь он снят замером по
всему хранилищу.

Из пяти длинных четыре были одним рядом — 10021 «die IBAN», где пример
диктовал номер счёта на 22 знака:

    pl  Mój numer IBAN to DE75512108001234567890   14.30 с (норма 4.73)
    de  Meine IBAN ist DE75512108001234567890      10.56 с (норма 4.22)

Движок читает номер по цифре, и это верно — иначе IBAN не прочитать.
Неверен был пример. Исправлено в `fix_long_digit_example.py`, после правки
pl 4.51 с, de 3.94 с.

ОЖИДАЕМЫЙ ОСТАТОК — 1, И ЭТО ЛОЖНАЯ ТРЕВОГА

    uk  «картопля фрі» (11703)  2.81 с против медианы корзины 1.08

Проверено замером начала и хвоста: речь с 0.095 до 2.713, тишины по 0.09 с
с каждой стороны, обрезка цела. Это просто ДВА слова, прочитанные неспешно,
а медиана корзины «10–14 знаков» набрана одиночными словами. Дефекта нет.

Остаток не обнуляется расширением корзин или смягчением порога: и то и
другое ослабило бы примету ради одного ряда. Один задокументированный
ложный срабатыватель дешевле слепого места.

КАК ЧИТАТЬ НОВЫЙ ВЫБРОС

    короче нормы   — подозрение на срезанную речь. Мерь начало и конец:
                     mp3_trim.speech_bounds(mp3_trim.decode(data), 16000)
    длиннее нормы  — смотри ТЕКСТ, а не клип. Почти всегда это цифры,
                     аббревиатура по буквам или лишнее в примере.

Скрипт ТОЛЬКО ЧИТАЕТ: ничего не правит, не синтезирует и не удаляет.
"""
from __future__ import annotations

import collections
import os
import pathlib
import statistics
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
os.environ.setdefault("ENV_FILE", ".env.local")

from sqlalchemy import create_engine, text  # noqa: E402
from sqlalchemy.orm import Session  # noqa: E402

from app.config import settings  # noqa: E402
from app.database.models import Word  # noqa: E402
from app.services import audio_store, mp3_trim  # noqa: E402
from app.services.audio_service import KIND_FULL, KIND_WORD, spoken_for  # noqa: E402
from app.services.language_service import SUPPORTED_LANGS  # noqa: E402
from app.services.tts_voices import default_voice  # noqa: E402

BUCKET = 5          # ширина корзины в символах
MIN_BUCKET = 20     # меньше — медиана шумная, не судим
LOW, HIGH = 0.50, 2.20

EXPECTED = 1  # uk «картопля фрі» (11703) — два слова неспешно, см. docstring


def main() -> int:
    engine = create_engine(settings.DATABASE_URL_SYNC)
    t0 = time.time()
    clips: list[tuple[str, str, int, int, float, str]] = []

    with Session(engine) as s:
        for lang in SUPPORTED_LANGS:
            voice = default_voice(lang)
            ids = s.execute(text("""
                SELECT w.id FROM words w
                JOIN word_lang_groups g
                  ON g.word_id = w.id AND g.lang = :l AND g.is_canonical
                ORDER BY w.id
            """), {"l": lang}).scalars().all()
            seen: set[tuple[str, str, str]] = set()
            for i in ids:
                w = s.get(Word, i)
                for kind in (KIND_WORD, KIND_FULL):
                    spoken = spoken_for(w, lang, kind)
                    if not spoken or (lang, kind, spoken) in seen:
                        continue
                    seen.add((lang, kind, spoken))
                    data = audio_store.read(lang, voice, kind, spoken)
                    if data is None:
                        continue
                    dur = sum(f[2] for f in mp3_trim.frame_index(data))
                    clips.append((lang, kind, i, len(spoken), dur, spoken))

    groups: dict[tuple, list[float]] = collections.defaultdict(list)
    for lang, kind, _, n, d, _ in clips:
        groups[(lang, kind, n // BUCKET)].append(d)
    medians = {k: statistics.median(v)
               for k, v in groups.items() if len(v) >= MIN_BUCKET}
    skipped = sum(len(v) for k, v in groups.items() if len(v) < MIN_BUCKET)

    hits = []
    for lang, kind, i, n, d, spoken in clips:
        m = medians.get((lang, kind, n // BUCKET))
        if not m:
            continue
        ratio = d / m
        if ratio < LOW or ratio > HIGH:
            hits.append((ratio, lang, kind, i, n, d, m, spoken))
    hits.sort()

    short = sum(1 for h in hits if h[0] < LOW)
    for ratio, lang, kind, i, n, d, m, spoken in hits:
        side = "КОРОЧЕ" if ratio < LOW else "длиннее"
        print(f"{lang} {kind:5s} ряд {i:6d}  {side} нормы в {ratio:.2f} раза")
        print(f"    {n} симв, {d:.2f} с, медиана корзины {m:.2f} с")
        print(f"      · {spoken}")

    judged = len(clips) - skipped
    print(f"\nклипов измерено: {len(clips)} за {time.time() - t0:.0f} с")
    print(f"судимо: {judged}, в мелких корзинах пропущено: {skipped}")
    print(f"всего попаданий: {len(hits)}  (короче нормы {short}, "
          f"длиннее {len(hits) - short})")
    print(f"ожидаемый остаток: {EXPECTED} — ложная тревога, см. docstring")

    if short:
        print("ВНИМАНИЕ: есть клипы КОРОЧЕ нормы — проверь, не срезана ли речь:")
        print("    mp3_trim.speech_bounds(mp3_trim.decode(data), 16000)")
        return 1
    if len(hits) != EXPECTED:
        print("ВНИМАНИЕ: остаток изменился — разбери и обнови docstring")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
