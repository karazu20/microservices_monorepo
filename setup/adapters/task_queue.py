from __future__ import annotations

import abc
import logging
from typing import Any, Callable

import redis
from rq import Queue

from setup import config

logger = logging.getLogger(__name__)
import time


class AbstractQueue(abc.ABC):
    queue: Any = NotImplemented

    @classmethod
    @abc.abstractmethod
    def enqueue(cls, funct: Callable, params: Any) -> Any:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def retrieve_result(cls, id_job: str):
        raise NotImplementedError


class CdcQueue(AbstractQueue):
    queue = Queue("cdc_queue", connection=redis.Redis(**config.get_redis_host_and_port()))

    @classmethod
    def enqueue(cls, func: Callable, params: tuple, max_queued=10):
        queued_jobs = cls.queue.jobs
        if len(queued_jobs) > max_queued:
            time.sleep(2)
        job = cls.queue.enqueue(
            func,
            args=params,
        )
        return job

    @classmethod
    def retrieve_result(cls, id_job: str):
        job = cls.queue.fetch_job(id_job)
        status = job.get_status(refresh=True)
        if status == "finished":
            return job.result
        time.sleep(2)
        return job.result
