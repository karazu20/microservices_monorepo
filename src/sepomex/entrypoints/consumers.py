import logging
from typing import Callable  # type: ignore

from setup import domain  # type: ignore
from setup.adapters.bus import RedisBus
from setup.domain import events
from src.sepomex import broker

logger = logging.getLogger(__name__)


def colonia_completed(data: dict):
    logger.info("handling %s", data)
    event = events.CompletedColonia.Schema().load(data)  # type: ignore
    response = broker.handle(event)
    logger.info("response %s", response)
    return response


RedisBus.subscribe(events.CompletedColonia, colonia_completed)
