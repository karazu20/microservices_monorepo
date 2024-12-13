from datetime import datetime

import pytest

from fakes.adapters import FakeBus, FakeCache, FakeUnitOfWork
from setup import inject
from src.closed_loans.domain.queries import GetClosedLoans
from src.closed_loans.services_layer import handlers


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


def test_group(broker, mambu, mocker):
    mocker.patch("setup.adapters.podemos_mambu.Loans._model_rest")
    mocker.patch("setup.adapters.podemos_mambu.Groups._model_rest")
    mock_search = mocker.patch("setup.adapters.podemos_mambu.Loans.search")

    loan = mambu.loans.build(
        id="12345",
        loan_name="Prueba",
        loan_amount=12356.5,
        interest_settings={"prueba": 2},
        closed_date=datetime.now(),
        account_state="CLOSED",
        account_sub_state="REPAID",
    )
    mock_search.return_value = [loan]

    group_fake = mambu.groups.build(id="ZX870", group_name="TestName")
    mambu.groups.add(group_fake)
    group_get = GetClosedLoans("ZX870")
    group = broker.handle(group_get)

    assert group[0]["id"] == "12345"
    assert group[0]["loan_name"] == "Prueba"
    assert group[0]["amount"] == 12356.5
    assert group[0]["account_state"] == "CLOSED"
    assert group[0]["account_sub_state"] == "REPAID"
    assert group[0]["account_sub_state_label"] == "Todas las Obligaciones Cumplidas"
