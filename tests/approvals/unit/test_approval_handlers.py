from src.approvals.domain.commands import ADDApproval
from src.approvals.services_layer import handlers


def test_add_stage(mambu):

    loan = mambu.loans.build(id="12345", account_state="PENDING_APPROVAL")
    mambu.loans.add(loan)
    handler = ADDApproval(id_mambu="12345")
    resp = handlers.add_change_status_approval(handler, mambu)
    assert resp["id_mambu"] == "12345"

    handler = ADDApproval(id_mambu="123456")
    resp = handlers.add_change_status_approval(handler, mambu)
    assert resp["id_mambu"] == "123456"
    assert not resp["status"]

    for value in resp["messages"][0]:
        assert value == "Error al obtener el ID en Mambu 123456"

    loan = mambu.loans.build(id="12347", account_state="OTHER_STATE")
    mambu.loans.add(loan)
    handler = ADDApproval(id_mambu="12347")
    resp = handlers.add_change_status_approval(handler, mambu)
    assert resp["id_mambu"] == "12347"
    assert not resp["status"]
    assert (
        resp["messages"]
        == "La cuenta debe estar en Pendiente de Aprobación (PENDING_APPROVAL)"
    )
