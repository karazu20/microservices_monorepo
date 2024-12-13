import json

import pytest

from setup import config as config_setup
from src.nip import config
from src.nip.errors import NipError


@pytest.mark.usefixtures("postgres_db")
def test_generate(mocker, client, token_user):
    data = {
        "nombre": "JUAN PRUEBA DOS",
        "telefono": "5567914402",
        "curp": "EARJ950927MDFSBS09",
    }
    url = config.get_api_url()
    response_generate = client.post(
        f"{url}/nip/generateNIP",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )
    assert response_generate.status_code == 201

    response_generate = client.post(
        f"{url}/nip/generateNIP",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )
    assert response_generate.status_code == 201

    nip_test = json.loads(response_generate.data)
    data = {"nip": str(nip_test["data"]["nip"])}
    response = client.post(
        f"{url}/nip/validateNIP",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )
    assert response.status_code == 201
    data = {"nip": str(nip_test["data"]["nip"])}
    response = client.post(
        f"{url}/nip/resendNIP", headers={config_setup.TOKEN_HEADER: token_user}, json=data
    )
    assert response.status_code == 201

    data = {
        "nombre": "",
        "telefono": "5567914402",
        "curp": "EARJ950927MDFSBS09",
    }
    url = config.get_api_url()
    response = client.post(
        f"{url}/nip/generateNIP",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )
    data_response = json.loads(response.data)
    assert data_response["error"]["msg_error"] == "El nombre no debe estar vacio,"

    data = {
        "nombre": "JUAN PRUEBA",
        "telefono": "55679144025555",
        "curp": "EARJ950927MDFSBS09",
    }
    url = config.get_api_url()
    response = client.post(
        f"{url}/nip/generateNIP",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )
    data_response = json.loads(response.data)
    assert data_response["error"]["msg_error"] == "El teléfono debe tener 10 dígitos,"


@pytest.mark.usefixtures("postgres_db")
def test_resend(mocker, client, token_user):
    data = {
        "nombre": "JUAN PRUEBA DOS",
        "telefono": "5543542827",
        "curp": "EARJ950927MDFSBS09",
    }
    url = config.get_api_url()
    response_generate = client.post(
        f"{url}/nip/generateNIP",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )
    assert response_generate.status_code == 201
    nip_test = json.loads(response_generate.data)
    data = {"nip": str(nip_test["data"]["nip"])}
    response = client.post(
        f"{url}/nip/resendNIP", headers={config_setup.TOKEN_HEADER: token_user}, json=data
    )
    assert response.status_code == 201


@pytest.mark.usefixtures("postgres_db")
def test_generate_massive(mocker, client, token_user):
    data = [
        {
            "nombre": "JUAN PRUEBA DOS",
            "telefono": "5567914402",
            "curp": "EARJ950927MDFSBS09",
        },
        {
            "nombre": "JUAN PRUEBA TRES",
            "telefono": "5626538414",
            "curp": "SWIF891213MDFSBS09",
        },
        {
            "nombre": "",
            "telefono": "5623538414",
            "curp": "JOEJ891213MDFSBS09",
        },
        {
            "nombre": "JUAN PRUEBA TRES",
            "telefono": "",
            "curp": "NICK920513MDFSBS09",
        },
        {
            "nombre": "JUAN PRUEBA CUATRO",
            "telefono": "5626538714",
            "curp": "",
        },
        {
            "nombre": "JUAN PRUEBA TRES",
            "telefono": "5567928451",
            "curp": "KEVI920513",
        },
        {
            "nombre": "JUAN PRUEBA TRES",
            "telefono": " 556792845",
            "curp": "KEVI920513MDFRNR06",
        },
        {
            "nombre": "JUAN PRUEBA TRES",
            "telefono": "55555556792845",
            "curp": "KEVI920513MDFRNR06",
        },
    ]
    url = config.get_api_url()

    response = client.post(
        f"{url}/nip/generateMassiveNIP",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )

    data = json.loads(response.data)

    assert response.status_code == 201
    assert data["data"]["prospectas"][2]["status_msg"] == "El nombre no debe estar vacio,"
    assert (
        data["data"]["prospectas"][3]["status_msg"] == "El teléfono no debe estar vacío,"
    )
    assert data["data"]["prospectas"][4]["status_msg"] == "El CURP no debe estar vacío,"
    assert data["data"]["prospectas"][5]["status_msg"] == "El CURP esta mal capturado,"
    assert (
        data["data"]["prospectas"][6]["status_msg"]
        == "El teléfono debe tener 10 dígitos,"
    )

    mock_user = mocker.patch("src.nip.entrypoints.routers.commands.GenerateNip.Schema")

    mock_user.side_effect = NipError("Prueba")

    response = client.post(
        f"{url}/nip/generateMassiveNIP",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )

    assert response.status_code == 201
