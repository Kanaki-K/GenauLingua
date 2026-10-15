"""
Где хранится занятие (состояние FSM): в Redis или в памяти.

ЗАЧЕМ REDIS. В памяти занятие живёт, пока жив процесс бота. Любая выкатка
обрывала уроки на середине: 15.10.2026 перезапуски при исправлениях дважды
оборвали людям занятия (человек начал в 16:33, бот перезапущен в 16:36), а
после обрыва — «занятие устарело» и начинай заново. С Redis бот поднимается
и продолжает с того же вопроса.

СРОК ЖИЗНИ. Состояние без движения дольше двух суток стирается: занятие,
брошенное позавчера, продолжать незачем — повторение уже ушло по срокам, а
лишние ключи копились бы без конца.

Адреса нет — память, как прежде: тестам и старым .env ничего не меняется.
"""
from __future__ import annotations

from datetime import timedelta
from typing import Optional

from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage

STATE_TTL = timedelta(days=2)


def make_storage(redis_url: Optional[str]) -> BaseStorage:
    if not redis_url:
        return MemoryStorage()
    from aiogram.fsm.storage.redis import RedisStorage

    return RedisStorage.from_url(redis_url, state_ttl=STATE_TTL, data_ttl=STATE_TTL)
