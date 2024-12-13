from src.storage.domain.queries import GetUrl


def test_get_url():
    query = GetUrl("s320230130")
    assert query.storage_id == "s320230130"
