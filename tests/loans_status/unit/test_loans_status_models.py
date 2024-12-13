from src.loans_status.domain.models import LoanStatus


def test_loan_status():
    model = LoanStatus("12356", "PENDIENTE_VALIDACION", "El crédito no pudo ser validado")
    assert model.id is None
    assert model.id_mambu == "12356"
    assert model.estatus == "PENDIENTE_VALIDACION"
    assert model.comentarios == "El crédito no pudo ser validado"
