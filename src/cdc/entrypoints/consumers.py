import logging
from typing import Callable  # type: ignore

from setup import domain  # type: ignore
from setup.adapters.bus import RedisBus
from setup.domain import events
from src.cdc import broker

logger = logging.getLogger(__name__)


def email_sent(data: dict) -> Callable:
    logger.info("handling %s", data)
    event = events.Email.Schema().load(data)  # type: ignore
    response = broker.handle(event)
    logger.info("response %s", response)
    return response


def valid_consulta_cdc_generated(data: dict) -> Callable:
    logger.info("handling valid consultaCdC %s", data["cdc_folio"])
    event = events.ValidConsultaCdc.Schema().load(data)  # type: ignore
    response = broker.handle(event)
    logger.info("response consultaCdC %s: %s", data["cdc_folio"], response)
    return response


RedisBus.subscribe(events.Email, email_sent)
RedisBus.subscribe(events.ValidConsultaCdc, valid_consulta_cdc_generated)
