import pytest

from setup import config as config_setup
from src.loans_status import config


@pytest.mark.usefixtures("postgres_db")
def test_create_get_loans_status(client, token_user):
    data = [
        {
            "id_mambu": "12345",
            "estatus": "PRUEBA",
        }
    ]

    url = config.get_api_url()
    response = client.post(
        f"{url}/loans_status", headers={config_setup.TOKEN_HEADER: token_user}, json=data
    )

    assert response.status_code == 500
    assert (
        response.data
        == b"{\"message\": \"{'estatus': ['El Estatus enviado no se encuentra en los estatus v\\u00e1lidos']}\"}\n"
    )

    data = [
        {"id_mambu": "12345", "estatus": "PENDIENTE_VALIDACION", "comentarios": "Prueba"}
    ]

    response = client.post(
        f"{url}/loans_status", headers={config_setup.TOKEN_HEADER: token_user}, json=data
    )

    assert response.status_code == 201
    assert response.data == b'{"code": 201, "data": "OK", "msg": "Success"}\n'

    response = client.get(
        f"{url}/loans_status?id_mambu=12345",
        headers={config_setup.TOKEN_HEADER: token_user},
        json={"id_mambu": ["12345"]},
    )
    assert response.status_code == 200
    assert (
        response.data
        == b'{"code": 200, "data": [{"id": 1, "id_mambu": "12345", "estatus": "PENDIENTE_VALIDACION", "comentarios": "Prueba"}], "msg": "Success"}\n'
    )

    response = client.get(
        f"{url}/loans_status",
        headers={config_setup.TOKEN_HEADER: token_user},
        json={"id_mambu": ["12345"], "estatus": ["PENDIENTE_VALIDACION"]},
    )

    assert response.status_code == 200
    assert (
        response.data
        == b'{"code": 200, "data": [{"id": 1, "id_mambu": "12345", "estatus": "PENDIENTE_VALIDACION", "comentarios": "Prueba"}], "msg": "Success"}\n'
    )

    response = client.get(
        f"{url}/loans_status",
        headers={config_setup.TOKEN_HEADER: token_user},
        json={"estatus": ["PENDIENTE_VALIDACION"]},
    )

    assert response.status_code == 200
    assert (
        response.data
        == b'{"code": 200, "data": [{"id": 1, "id_mambu": "12345", "estatus": "PENDIENTE_VALIDACION", "comentarios": "Prueba"}], "msg": "Success"}\n'
    )

    response = client.get(
        f"{url}/loans_status", headers={config_setup.TOKEN_HEADER: token_user}, json={}
    )

    assert response.status_code == 200
    assert (
        response.data
        == b'{"code": 200, "data": [{"id": 1, "id_mambu": "12345", "estatus": "PENDIENTE_VALIDACION", "comentarios": "Prueba"}], "msg": "Success"}\n'
    )
