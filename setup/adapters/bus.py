from __future__ import annotations  # type: ignore

import abc
import json
import logging
from dataclasses import asdict
from typing import Any, Callable, List, Type

import redis

from setup import config, domain

logger = logging.getLogger(__name__)


class AbstractBus(abc.ABC):
    bus: Any = NotImplemented

    @classmethod
    @abc.abstractmethod
    def publish(cls, event: domain.Event):
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def subscribe(cls, event: Type[domain.Event], consumer: Callable):
        raise NotImplementedError


class RedisBus(AbstractBus):
    bus = redis.Redis(**config.get_redis_host_and_port())
    _subscriptions: List[dict] = []

    @classmethod
    def publish(cls, event: domain.Event):
        try:
            cls.bus.publish(event.channel, json.dumps(asdict(event)))
            logger.info("publishing: channel=%s, event=%s", event.channel, event)
        except Exception as e:
            logger.error("Error to publish event %s on redis %s ", event, e)

    @classmethod
    def pubsubs(cls, channels: List[str]) -> Any:  # pragma: no cover
        pubsubs = cls.bus.pubsub(ignore_subscribe_messages=True)
        for channel in channels:
            pubsubs.subscribe(channel)
        return pubsubs

    @classmethod
    def subscribe(cls, event: Type[domain.Event], consumer: Callable) -> Any:
        cls._subscriptions.append({"channel": event.channel, "consumer": consumer})

    @classmethod
    def get_subscriptions(cls):
        return cls._subscriptions
