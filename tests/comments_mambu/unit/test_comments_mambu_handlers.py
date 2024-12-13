from src.comments_mambu.domain.commands import (
    ADDCommentClient,
    ADDCommentGroup,
    ADDCommentLoan,
)
from src.comments_mambu.domain.queries import (
    GetClientComments,
    GetGroupComments,
    GetLoanComments,
)


def test_add_comment_loan():
    model = ADDCommentLoan(id_mambu="12345", comment="PRUEBA")
    assert model.id_mambu == "12345"
    assert model.comment == "PRUEBA"


def test_add_comment_group():
    model = ADDCommentGroup(id_mambu="OU774", comment="PRUEBA GRUPO")
    assert model.id_mambu == "OU774"
    assert model.comment == "PRUEBA GRUPO"


def test_add_comment_client():
    model = ADDCommentClient(id_mambu="NUC703", comment="PRUEBA INTEGRANTE")
    assert model.id_mambu == "NUC703"
    assert model.comment == "PRUEBA INTEGRANTE"


def test_get_comment_loan():
    model = GetLoanComments(loan_id="12345")
    assert model.loan_id == "12345"


def test_get_comment_group():
    model = GetGroupComments(group_id="OU774")
    assert model.group_id == "OU774"


def test_get_comment_client():
    model = GetClientComments(client_id="NUC703")
    assert model.client_id == "NUC703"
