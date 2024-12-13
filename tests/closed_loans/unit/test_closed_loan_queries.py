from src.closed_loans.domain.queries import GetClosedLoans


def test_get_closed_loans():
    query = GetClosedLoans("AB1234")
    assert query.group_id == "AB1234"
