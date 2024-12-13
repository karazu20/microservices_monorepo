from __future__ import annotations  # type: ignore

import abc
import logging
from datetime import timedelta
from typing import Any

import redis

from setup import config

logger = logging.getLogger(__name__)


class AbstractCache(abc.ABC):
    cache: Any = NotImplemented

    @classmethod
    @abc.abstractmethod
    def set(cls, key: str, value: Any, expire):
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def get(cls, key: str) -> Any:
        raise NotImplementedError


class RedisCache(AbstractCache):
    cache = redis.Redis(**config.get_redis_host_and_port())

    @classmethod
    def set(cls, key: str, value: Any, expire: int = 3600):
        try:
            cls.cache.setex(
                key,
                timedelta(seconds=expire),
                value=value,
            )
            logger.info("cached: key=%s, value=%s", key, value)
        except Exception as e:
            logger.error("Error to cached key %s error: %s ", key, e)

    @classmethod
    def get(cls, key: str) -> Any:
        try:
            return cls.cache.get(key)
        except Exception as e:
            logger.error("Error to get key %s error: %s ", key, e)
