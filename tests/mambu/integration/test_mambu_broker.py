import pytest

from fakes.adapters import FakeBus, FakeCache, FakeUnitOfWork
from setup import inject
from src.mambu.domain.queries import (
    GetClient,
    GetClientId,
    GetGroup,
    GetGroupId,
    GetLoan,
    GetLoanId,
)
from src.mambu.services_layer import handlers


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


def test_group(broker, mambu):
    group_fake = mambu.groups.build(id="ZX870", group_name="TestName")
    mambu.groups.add(group_fake)
    group_get = GetGroup("ZX870", "", 10, 2)
    group = broker.handle(group_get)
    assert group[0]["id"] == "ZX870"

    group_get = GetGroup(None, "Prueba", 11, 5)
    group = broker.handle(group_get)

    assert len(group) == 1


def test_client(broker, mambu):
    client_fake = mambu.clients.build(id="AB123", first_name="Prueba", last_name="Prueba")
    mambu.clients.add(client_fake)
    client_get = GetClient("AB123", None, None, None, None, 10, 2)
    client = broker.handle(client_get)
    assert client[0]["id"] == "AB123"

    client_get = GetClient(None, "Nombre", None, None, None, 10, 2)
    client = broker.handle(client_get)

    assert len(client) == 1


def test_loan(broker, mambu):
    loans_fake = mambu.loans.build(id="12345", account_state="ACTIVE")
    mambu.loans.add(loans_fake)
    loan_get = GetLoan("12345", None, 10, 1, None)
    loan = broker.handle(loan_get)
    assert loan[0]["id"] == "12345"

    loan_get = GetLoan(None, "ACTIVE", 10, 3, None)
    loan = broker.handle(loan_get)

    assert len(loan) == 1


def test_group_id(broker, mambu):
    group_fake = mambu.groups.build(id="ZX870", group_name="TestName")
    mambu.groups.add(group_fake)
    group_get = GetGroupId("ZX870")
    group = broker.handle(group_get)
    assert group["id"] == "ZX870"


def test_client_id(broker, mambu):
    client_fake = mambu.clients.build(id="AB123", first_name="Prueba", last_name="Prueba")
    mambu.clients.add(client_fake)
    client_get = GetClientId("AB123")
    client = broker.handle(client_get)
    assert client["id"] == "AB123"


def test_loan_id(broker, mambu):
    loans_fake = mambu.loans.build(id="12345", account_state="ACTIVE")
    mambu.loans.add(loans_fake)
    loan_get = GetLoanId("12345")
    loan = broker.handle(loan_get)
    assert loan["id"] == "12345"
