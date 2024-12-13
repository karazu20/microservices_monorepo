from src.transactions.domain.queries import GetInstallments, GetTransactions


def test_get_closed_loans():
    query = GetTransactions("12345")
    assert query.loan_id == "12345"


def test_get_closed_loans():
    query = GetInstallments("54321")
    assert query.loan_id == "54321"
