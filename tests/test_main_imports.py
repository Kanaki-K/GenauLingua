# -*- coding: utf-8 -*-
"""
Боевой вход `app.main` хотя бы импортируется.

15.10 (патч 2.1) в `app.main` попал импорт `SimpleEventIsolation` не из того
модуля: 1143 теста прошли, а бот не запускался вовсе — ни один тест
`app.main` не импортировал. Тест ловит такое до выкатки.
"""
import importlib


def test_main_module_imports():
    module = importlib.import_module("app.main")
    assert callable(module.main)
