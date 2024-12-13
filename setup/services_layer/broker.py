# pylint: disable=broad-except, attribute-defined-outside-init
from __future__ import annotations  # type: ignore

import logging
from typing import Callable, Dict, Type, Union

from setup.domain import Command, Event, Query

logger = logging.getLogger(__name__)

Message = Union[Command, Query, Event]


class Broker:
    def __init__(
        self,
        query_handlers: Dict[Type[Query], Callable],
        command_handlers: Dict[Type[Command], Callable],
        event_handlers: Dict[Type[Event], Callable],
    ):
        self.query_handlers = query_handlers
        self.command_handlers = command_handlers
        self.event_handlers = event_handlers

    def handle(self, message: Message):
        if isinstance(message, Query):
            return self.handler_query(message)
        elif isinstance(message, Command):
            return self.handler_command(message)
        elif isinstance(message, Event):
            return self.handler_event(message)
        else:
            raise Exception(f"{message} was not an Query or Command or Event")

    def handler_command(self, command: Command):
        logger.info("handling command %s", command)
        try:
            handler = self.command_handlers[type(command)]  # get command
            return handler(command)
        except Exception as e:
            logger.exception("Exception handling command %s: %s", command, e)
            raise

    def handler_query(self, query: Query):
        logger.info("handling query %s", query)
        try:
            handler = self.query_handlers[type(query)]
            return handler(query)
        except Exception as e:
            logger.exception("Exception handling query %s: %s", query, e)
            raise

    def handler_event(self, event: Event):
        logger.info("handling event %s", event)
        try:
            handler = self.event_handlers[type(event)]
            return handler(event)
        except Exception as e:
            logger.error("Exception handling event %s: %s", event, e)
            raise e
