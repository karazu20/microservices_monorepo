import pytest

from src.sepomex.entrypoints import consumers


@pytest.mark.usefixtures("postgres_db")
def test_consumer_colonia_completed():
    data = {"nombre": "Valle"}
    response = consumers.colonia_completed(data)
    assert response
