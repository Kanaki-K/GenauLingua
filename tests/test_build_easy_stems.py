# -*- coding: utf-8 -*-
"""
«Собираю» для A1–A2: ловушка — не форма слова фразы (аудит 2.1).

Ловушка «другим словом из чужого примера» сверялась с двойниками только по
закрытым спискам: к «gehe» приходило «geht», к «Hund» — «Hunde». Это та
самая падежная ловушка, которую правило 2.1 новичку запрещает.
"""
import random

from app.services import build_service as bs


def test_easy_trap_is_never_a_form_of_a_target_word():
    target = ["ich", "gehe", "mit", "dem", "Hund"]
    foreign = ["geht", "Hunde", "Katze", "schnell"]
    got = set()
    for seed in range(40):
        picked, _ = bs.pick_distractors(target, "de", foreign, random.Random(seed), 1, easy=True)
        got.update(picked)
    assert not (got & {"geht", "Hunde"}), sorted(got)
    assert got & {"Katze", "schnell"}, "честные ловушки тоже отсеялись"


def test_same_stem():
    assert bs.same_stem("gehe", "geht") and bs.same_stem("Hund", "Hunde")
    assert bs.same_stem("gute", "guten")
    assert not bs.same_stem("mit", "mir") and not bs.same_stem("Haus", "Hand")
    assert not bs.same_stem("kaufen", "laufen")
