import json

from setup import config as config_setup
from src.sepomex import config


def test_microservice_authenticated(client, token_user):

    url = config.get_api_url()

    # with out token
    response = client.get(f"{url}/demo/authenticated")
    assert response.status_code == 401

    # valid token
    response = client.get(
        f"{url}/demo/authenticated",
        headers={config_setup.TOKEN_HEADER: token_user},
        json={},
    )
    assert response.status_code == 200

    # empty token
    response = client.get(
        f"{url}/demo/authenticated",
        json={},
    )

    response_data = json.loads(response.data)
    assert response.status_code == 401
    assert response_data["msg"] == "fail"
    assert (
        response_data["error"]["msg_error"]
        == "Se requiere login de usuario para acceder a este recurso"
    )


def test_microservice_public(client):
    url = config.get_api_url()

    response = client.get(f"{url}/demo/public", json={})
    assert response.status_code == 200
