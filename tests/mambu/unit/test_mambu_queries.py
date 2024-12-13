from src.mambu.domain.queries import (
    GetClient,
    GetClientId,
    GetGroup,
    GetGroupId,
    GetLoan,
    GetLoanId,
)


def test_get_group():
    query = GetGroup("AB1234", "PRUEBA NAME", 10, 1)
    assert query.group_id == "AB1234"
    assert query.group_name == "PRUEBA NAME"


def test_get_client():
    query = GetClient("AB234", "NOMBRE", "MIDDLE", "GONZALEZ", "GGOO920528", 10, 2)
    assert query.client_id == "AB234"
    assert query.first_name == "NOMBRE"
    assert query.middle_name == "MIDDLE"
    assert query.last_name == "GONZALEZ"
    assert query.rfc == "GGOO920528"


def test_get_loan():
    query = GetLoan("12345", "ACTIVE", 10, 2, None)
    assert query.loan_id == "12345"
    assert query.status == "ACTIVE"


def test_get_group_id():
    query = GetGroupId("MAT11")
    assert query.id == "MAT11"


def test_get_client_id():
    query = GetClientId("AND12")
    assert query.id == "AND12"


def test_get_loan_id():
    query = GetLoanId("27059")
    assert query.id == "27059"
