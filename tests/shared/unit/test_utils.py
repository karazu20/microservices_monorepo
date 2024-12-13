from http import HTTPStatus

from shared.utils import get_full_name
from src.sepomex import config


def test_get_groups(app, client):

    url = config.get_api_url()
    response = client.get(f"{url}/demo/json_encoder_test")

    assert response.status_code == HTTPStatus.OK


def test_get_full_name():
    full_name = get_full_name("JUAN", "PRUEBA", "    ")

    assert full_name == "JUAN PRUEBA"
