"""
ПРИЁМКА ИГРЫ ВСЛУХ: судит ли бот произношение на всех шести языках.

ЧЕГО НЕ ПРОВЕРЯЛ НИКТО. Речевой канал был проверен как СБОРКА (вопрос
собирается, слово показано, эталон есть — `verify_quiz_channels`) и как
УЧЁТ (ответ пишется строкой круга, двигает счётчики и баллы —
`audit_round`, где распознаватель подменён заглушкой). Сам судья —
`check_pronunciation` — не проверялся ничем: ни разу не было сказано
числом, принимает ли он верное произношение и отвергает ли неверное.

Дыра эта не теоретическая. Игра вслух с 13 октября включена ВСЕМ (прежде
её имел один человек из 233), то есть судья встал на пути у всех.

КАК ПРОВЕРЯЕТСЯ БЕЗ МИКРОФОНА. Боту подаются НАШИ ЖЕ синтезированные
клипы — как будто это голосовое человека. Приём законный: судья принимает
байты любого формата, который читает PyAV, и клип для него ничем не
отличается от записи. Эталонный голос — это «идеальный ученик», и на нём
проверяется ровно то, что должно работать всегда:

    принимает верное    клип слова X подан с целью X  → matched
    отвергает чужое     клип слова X подан с целью Y  → not matched

Второе важнее первого. Судья, который принимает ВСЁ, выглядит
безупречно — и игры при нём нет вовсе: любое мычание засчитывается, и
человек ничему не учится.

ЧЕГО ЭТА ПРОВЕРКА НЕ ЗАМЕНЯЕТ. Живого человека с акцентом. Эталонный
голос — верхняя граница: если судья не принимает даже его, игра сломана
наверняка; принимает — значит сломана не наверняка. Акцент проверяет
только владелец голосом, и это записано в `VERIFICATION.md` §2.

    ENV_FILE=.env.local .venv/Scripts/python.exe -m app.scripts.verify_speech
    ... -m app.scripts.verify_speech --per-lang 20
    ... -m app.scripts.verify_speech --lang de --per-lang 50
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import sys
from dataclasses import dataclass, field

from sqlalchemy import func, select

from app.database.models import Word, WordLangGroup
from app.database.session import AsyncSessionLocal
from app.services import audio_store
from app.services.audio_service import KIND_WORD, spoken_for
from app.services.language_service import LEARNABLE_LANGS, option_label
from app.services.speech_check import check_pronunciation
from app.services.tts_voices import default_voice

logging.disable(logging.ERROR)

DEFAULT_PER_LANG = 10

# Доля верных, ниже которой считаем игру сломанной. Не 100%: судья сверяет
# СТРОКИ после нормализации, и на коротких словах расхождение в одну букву
# роняет похожесть ниже порога — то же самое, что видно в проверке слухом
# (`tts_asr_check`), где de дал 99.8%, а uk 99.3%. Эталонный голос обязан
# проходить почти всегда, но требовать безупречности от распознавателя —
# значит ловить его артефакты, а не наши дефекты.
MIN_ACCEPT_SHARE = 0.85

# Доля чужих слов, которые судья ОБЯЗАН отвергнуть. Строже предыдущей: тут
# ошибка означает, что игра не отличает ответ от любого звука.
MIN_REJECT_SHARE = 0.95


@dataclass
class Report:
    checked: int = 0
    accepted: int = 0
    rejected_wrong: int = 0
    wrong_total: int = 0
    skipped_no_clip: int = 0
    by_lang: dict = field(default_factory=dict)
    problems: list = field(default_factory=list)
    accepted_examples: list = field(default_factory=list)
    refused_examples: list = field(default_factory=list)


async def _words(session, lang: str, limit: int) -> list[Word]:
    """Канонические слова языка в случайном порядке."""
    return (await session.execute(
        select(Word)
        .join(WordLangGroup, (WordLangGroup.word_id == Word.id)
              & (WordLangGroup.lang == lang)
              & (WordLangGroup.is_canonical.is_(True)))
        .order_by(func.random())
        .limit(limit)
    )).scalars().all()


async def _run_lang(session, lang: str, per_lang: int, rep: Report) -> None:
    voice = default_voice(lang)
    words = await _words(session, lang, per_lang * 3)

    accepted = checked = rejected = wrong_total = 0

    for index, word in enumerate(words):
        if checked >= per_lang:
            break

        target = spoken_for(word, lang, KIND_WORD) or option_label(word, lang)
        if not target:
            continue

        data = audio_store.read(lang, voice, KIND_WORD, target)
        if data is None:
            rep.skipped_no_clip += 1
            continue

        checked += 1

        # 1. ВЕРНОЕ: клип слова подан с целью этого же слова
        verdict = await check_pronunciation(data, target, lang)
        if verdict.failed:
            rep.problems.append(
                f"{lang}: судья сорвался на {target!r} "
                f"(услышано {verdict.heard!r})"
            )
        elif verdict.matched:
            accepted += 1
            if len(rep.accepted_examples) < 6:
                rep.accepted_examples.append(
                    f"{lang} {target!r} → услышано {verdict.heard!r}"
                )
        else:
            rep.problems.append(
                f"{lang}: НЕ ПРИНЯЛ эталон {target!r} — "
                f"услышано {verdict.heard!r}, похожесть {verdict.similarity:.2f}"
            )

        # 2. ЧУЖОЕ: тот же клип, но цель — другое слово. Берём слово,
        # заведомо непохожее: соседнее по списку длиной хотя бы в три буквы
        other = next(
            (w for w in words[index + 1:]
             if (spoken_for(w, lang, KIND_WORD) or "") not in ("", target)
             and len(spoken_for(w, lang, KIND_WORD) or "") >= 3),
            None,
        )
        if other is not None:
            other_target = spoken_for(other, lang, KIND_WORD)
            wrong_total += 1
            wrong = await check_pronunciation(data, other_target, lang)
            if wrong.matched:
                rep.problems.append(
                    f"{lang}: ПРИНЯЛ чужое — сказано {target!r}, "
                    f"спрошено {other_target!r}, услышано {wrong.heard!r}"
                )
            else:
                rejected += 1
                if len(rep.refused_examples) < 4:
                    rep.refused_examples.append(
                        f"{lang} сказано {target!r}, спрошено {other_target!r} "
                        f"— отвергнуто"
                    )

    rep.checked += checked
    rep.accepted += accepted
    rep.rejected_wrong += rejected
    rep.wrong_total += wrong_total
    rep.by_lang[lang] = (accepted, checked, rejected, wrong_total)

    share = accepted / checked * 100 if checked else 0
    reject_share = rejected / wrong_total * 100 if wrong_total else 0
    print(f"  {lang}  принято {accepted}/{checked} ({share:.0f}%), "
          f"чужое отвергнуто {rejected}/{wrong_total} ({reject_share:.0f}%)",
          flush=True)


async def run(langs: list[str], per_lang: int) -> int:
    rep = Report()
    print(f"Приёмка игры вслух: по {per_lang} слов на язык, "
          f"голос эталонный\n")

    async with AsyncSessionLocal() as session:
        for lang in langs:
            await _run_lang(session, lang, per_lang, rep)

    print()
    print(f"слов проверено: {rep.checked}")
    if rep.skipped_no_clip:
        print(f"пропущено без клипа: {rep.skipped_no_clip}")

    if not rep.checked:
        print("\nНИ ОДНОГО СЛОВА НЕ ПРОВЕРЕНО — проверять было нечего")
        return 1

    accept_share = rep.accepted / rep.checked
    reject_share = (rep.rejected_wrong / rep.wrong_total) if rep.wrong_total else 0
    print(f"принято верных: {rep.accepted} ({accept_share * 100:.1f}%)")
    print(f"отвергнуто чужих: {rep.rejected_wrong} из {rep.wrong_total} "
          f"({reject_share * 100:.1f}%)")

    if rep.accepted_examples:
        print("\nпримеры принятого:")
        for line in rep.accepted_examples:
            print(f"   {line}")
    if rep.refused_examples:
        print("\nпримеры отказа чужому:")
        for line in rep.refused_examples:
            print(f"   {line}")

    bad = False
    if accept_share < MIN_ACCEPT_SHARE:
        print(f"\nСБОЙ: эталон принимается в {accept_share * 100:.1f}% "
              f"случаев, а должен хотя бы в {MIN_ACCEPT_SHARE * 100:.0f}%")
        bad = True
    if rep.wrong_total and reject_share < MIN_REJECT_SHARE:
        print(f"\nСБОЙ: чужое отвергается в {reject_share * 100:.1f}% "
              f"случаев, а должно хотя бы в {MIN_REJECT_SHARE * 100:.0f}%. "
              f"Судья, принимающий всё, — это отсутствие игры")
        bad = True

    if rep.problems:
        print(f"\nразборов: {len(rep.problems)}")
        for line in rep.problems[:25]:
            print(f"   {line}")
        if len(rep.problems) > 25:
            print(f"   … и ещё {len(rep.problems) - 25}")

    if bad:
        return 1

    print("\nигра вслух судит верно на всех проверенных языках: "
          "эталон принимается, чужое отвергается")
    print("ОСТАЁТСЯ ЖИВОЙ ГОЛОС: эталон — верхняя граница, акцент "
          "проверяет только человек")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--lang", action="append",
                    help="только этот язык (можно повторять)")
    ap.add_argument("--per-lang", type=int, default=DEFAULT_PER_LANG)
    args = ap.parse_args()

    langs = args.lang or sorted(LEARNABLE_LANGS)
    unknown = [lang for lang in langs if lang not in LEARNABLE_LANGS]
    if unknown:
        print(f"неизвестные языки: {', '.join(unknown)}")
        return 2
    return asyncio.run(run(langs, args.per_lang))


if __name__ == "__main__":
    sys.exit(main())
