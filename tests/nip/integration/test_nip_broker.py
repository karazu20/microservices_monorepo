import pytest

from fakes.adapters import FakeBus, FakeCache, FakeTwilioService, FakeUnitOfWork
from setup import inject
from src.nip.domain.commands import GenerateNip
from src.nip.services_layer import handlers


@pytest.fixture
def broker():
    broker = inject.start_broker(
        handlers=handlers,
        orm=None,
        uow=FakeUnitOfWork(),
        bus=FakeBus(),
        cache=FakeCache(),
        messenger_service=FakeTwilioService(),
    )
    yield broker


def test_broker_persona(mocker, broker):
    persona = GenerateNip(
        nombre="JUAN PRUEBA TRES",
        telefono="5567914402",
        curp="EARJ950927MDFSBS09",
    )

    nip = broker.handle(persona)
    assert nip is not None
