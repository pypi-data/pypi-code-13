# coding=utf-8
"""
import package
"""
import manager

from redisOrm import (
    RedisModel,
    CharField,
    IntField,
    LongField,
    TimeField,
)

from manager import (
    ModelManager
)

__version__ = '0.0.1'
VERSION = tuple(map(int, __version__.split('.')))

__all__ = ["manager", "RedisModel", "CharField", "IntField",
           "LongField", "TimeField", "ModelManager"]
