import marshmallow
import pytest

from fakes.adapters import FakeUnitOfWork
from src.loans_status.domain.commands import ADDLoanStatus
from src.loans_status.services_layer import handlers


def test_add_loan_status():
    uow = FakeUnitOfWork()
    model = ADDLoanStatus(
        id_mambu="123456",
        estatus="PENDIENTE_VALIDACION",
        comentarios="El crédito no pudo ser validado",
    )
    handlers.add_loan_status(model, uow)
    assert uow.committed


def test_add_loan_status_validates():
    model = ADDLoanStatus(
        id_mambu="123456",
        estatus="PENDIENTES",
        comentarios="El crédito no pudo ser validado",
    )
    with pytest.raises(marshmallow.ValidationError):
        model.validates(model.estatus)
