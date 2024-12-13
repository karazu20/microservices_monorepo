import pytest
from freezegun import freeze_time

from setup import config as config_setup
from src.storage import config


@freeze_time("2022-05-27 12:00:00")
@pytest.mark.usefixtures("postgres_db")
def test_create_get_storage(client, token_user, mocker):
    data = {
        "tipo": "INE",
        "descripcion": "Documento oficial",
    }

    url = config.get_api_url()
    response = client.post(
        f"{url}/storage/document_type",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )
    assert response.status_code == 201

    data = {
        "tipo": "application/pdf",
    }

    url = config.get_api_url()
    response = client.post(
        f"{url}/storage/filetype",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )
    assert response.status_code == 201

    data = {
        "tipo_entidad": "INTEGRANTE",
        "podemos_id": "12345",
        "tipo_documento_id": 1,
        "tipo_archivo": "application/pdf",
        "file": "cHJ1ZWJhLnhsc3g=",
    }

    url = config.get_api_url()
    response = client.post(
        f"{url}/storage", headers={config_setup.TOKEN_HEADER: token_user}, json=data
    )
    assert response.status_code == 201

    url = config.get_api_url()
    response = client.get(
        f"{url}/storage/get_url?storage_id=Prueba",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )
    assert response.status_code == 404
    assert response.data == (
        b'{"code": "STO404", "error": {"error": "No existe el recurso solicitado'
        b'", "msg_error": "No existe el recurso solicitado"}, "msg": "fail"}\n'
    )

    url = config.get_api_url()
    response = client.get(
        f"{url}/storage/get_url?storage_id=20220527",
        headers={config_setup.TOKEN_HEADER: token_user},
    )

    url = config.get_api_url()
    response = client.get(
        f"{url}/storage/filetype",
        headers={config_setup.TOKEN_HEADER: token_user},
    )
    assert response.status_code == 200

    url = config.get_api_url()
    response = client.get(
        f"{url}/storage/document_type",
        headers={config_setup.TOKEN_HEADER: token_user},
    )
    assert response.status_code == 200


@pytest.mark.usefixtures("postgres_db")
def test_exception_storage(client, token_user, mocker):
    mocker.patch("src.storage.entrypoints.routers.queries")

    url = config.get_api_url()
    response = client.get(
        f"{url}/storage/document_type",
        headers={config_setup.TOKEN_HEADER: token_user},
    )
    assert response.status_code == 500

    response = client.get(
        f"{url}/storage/filetype",
        headers={config_setup.TOKEN_HEADER: token_user},
    )
    assert response.status_code == 500
