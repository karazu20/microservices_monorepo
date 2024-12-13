import inspect
import os
from typing import Any

from setup.adapters import bus, cache, messenger_service, podemos_mambu, smtp, storage
from setup.services_layer import broker, unit_of_work

if os.environ.get("FLASK_ENV") == "test":
    from fakes.adapters import (
        FakeBus,
        FakeEmail,
        FakePodemosMambu,
        FakeStorage,
        FakeTwilioService,
    )

    mambu_instance = FakePodemosMambu
    twilio_instance = FakeTwilioService
    s3_instance = FakeStorage
    smtp_instance = FakeEmail
    bus_instance = FakeBus()
else:
    mambu_instance = podemos_mambu.PodemosMambu
    twilio_instance = messenger_service.TwilioService
    s3_instance = storage.S3
    smtp_instance = smtp.SmtpEmail
    bus_instance = bus.RedisBus()


def start_broker(
    handlers: Any,
    orm: Any,
    uow: unit_of_work.AbstractUnitOfWork,
    bus: bus.AbstractBus = bus_instance,
    cache: cache.AbstractCache = cache.RedisCache(),
    mambu: podemos_mambu.AbstractMambu = mambu_instance,
    messenger_service: messenger_service.MessengerService = twilio_instance,
    storage: storage.AbstractStorage = s3_instance,
    smtp: smtp.AbstractSMTP = smtp_instance,
) -> broker.Broker:

    if orm:
        orm.start_mappers()

    dependencies = {
        "uow": uow,
        "bus": bus,
        "cache": cache,
        "mambu": mambu,
        "messenger_service": messenger_service,
        "storage": storage,
        "smtp": smtp,
    }
    injected_queries_handlers = {
        query_type: inject_dependencies(handler, dependencies)
        for query_type, handler in handlers.QUERY_HANDLERS.items()
    }
    injected_command_handlers = {
        command_type: inject_dependencies(handler, dependencies)
        for command_type, handler in handlers.COMMAND_HANDLERS.items()
    }
    injected_event_handlers = {
        event_type: inject_dependencies(handler, dependencies)
        for event_type, handler in handlers.EVENT_HANDLERS.items()
    }

    return broker.Broker(
        query_handlers=injected_queries_handlers,
        command_handlers=injected_command_handlers,
        event_handlers=injected_event_handlers,
    )


def inject_dependencies(handler, dependencies):
    params = inspect.signature(handler).parameters
    deps = {
        name: dependency for name, dependency in dependencies.items() if name in params
    }
    return lambda message: handler(message, **deps)
