import pytest

from fakes.adapters import FakeBus, FakeCache, FakeUnitOfWork
from setup import inject
from src.groups.domain.queries import GetGrupo
from src.groups.services_layer import handlers


@pytest.fixture
def broker():
    broker = inject.start_broker(
        handlers=handlers,
        orm=None,
        uow=FakeUnitOfWork(),
        bus=FakeBus(),
        cache=FakeCache(),
    )
    yield broker


def test_broker_groups(mocker, broker):
    get_group = GetGrupo()
    group = broker.handle(get_group)

    assert len(group) == 0
