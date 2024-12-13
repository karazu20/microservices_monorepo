import json

import pytest

from setup import config as config_setup
from src.sepomex import config


@pytest.mark.usefixtures("postgres_db")
def test_create_colonia(client, token_user):

    data = {
        "nombre": "CDMX",
    }
    url = config.get_api_url()
    response = client.post(
        f"{url}/sepomex/estados",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )
    response_data = json.loads(response.data)
    assert response.status_code == 201

    assert "data" in response_data
    assert response_data.get("msg") == "success"

    response = client.get(
        f"{url}/sepomex/estados", headers={config_setup.TOKEN_HEADER: token_user}
    )
    response_data = json.loads(response.data)
    assert response.status_code == 200
    assert "data" in response_data
    assert response_data.get("msg") == "success"

    response_data = json.loads(response.data)
    assert "data" in response_data

    data = {
        "nombre": "Miguel Hidalgo",
        "estado": "CDMX",
    }
    url = config.get_api_url()
    response = client.post(
        f"{url}/sepomex/municipios",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )
    response_data = json.loads(response.data)
    assert response.status_code == 201
    response_data = json.loads(response.data)
    assert "data" in response_data
    assert response_data.get("msg") == "success"

    qry_params = "?estado=CDMX"
    response = client.get(
        f"{url}/sepomex/municipios{qry_params}",
        headers={config_setup.TOKEN_HEADER: token_user},
    )
    response_data = json.loads(response.data)
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert "data" in response_data
    assert response_data.get("msg") == "success"

    data = {
        "nombre": "Narvarte Poniente",
        "ciudad": "CDMX",
        "asentamiento": "México",
        "codigo_postal": "00965",
        "municipio": "Miguel Hidalgo",
    }
    url = config.get_api_url()
    response = client.post(
        f"{url}/sepomex/colonias",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )
    response_data = json.loads(response.data)
    assert response.status_code == 201
    response_data = json.loads(response.data)
    assert "data" in response_data
    assert response_data.get("msg") == "success"

    qry_params = "?municipio=Miguel Hidalgo"
    response = client.get(
        f"{url}/sepomex/colonias{qry_params}",
        headers={config_setup.TOKEN_HEADER: token_user},
    )
    response_data = json.loads(response.data)
    assert response.status_code == 200
    assert response_data.get("msg") == "success"

    qry_params = "?codigo_postal=00965"
    response = client.get(
        f"{url}/sepomex/colonias_cp{qry_params}",
        headers={config_setup.TOKEN_HEADER: token_user},
    )
    response_data = json.loads(response.data)
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert "data" in response_data
    assert response_data.get("msg") == "success"


@pytest.mark.usefixtures("postgres_db")
def test_create_fail(client, token_user):

    data = {
        "nombre": "CDMX",
    }
    url = config.get_api_url()
    response = client.post(
        f"{url}/sepomex/estados",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )
    assert response.status_code == 201

    data = {
        "nombre": "Miguel Hidalgo",
        "estado": "DF",
    }
    url = config.get_api_url()
    response = client.post(
        f"{url}/sepomex/municipios",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )
    assert response.status_code == 500

    qry_params = "?estado=DF"
    response = client.get(
        f"{url}/sepomex/municipios{qry_params}",
        headers={config_setup.TOKEN_HEADER: token_user},
    )
    assert response.status_code == 500

    data = {
        "nombre": "Narvarte Poniente",
        "ciudad": "DF",
        "asentamiento": "México",
        "codigo_postal": "00965",
        "municipio": "DF",
    }
    url = config.get_api_url()
    response = client.post(
        f"{url}/sepomex/colonias",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )
    assert response.status_code == 500

    qry_params = "?municipio=Iztacalco"
    response = client.get(
        f"{url}/sepomex/colonias{qry_params}",
        headers={config_setup.TOKEN_HEADER: token_user},
    )
    assert response.status_code == 500

    qry_params = "?wrong data=1"
    response = client.get(
        f"{url}/sepomex/estados{qry_params}",
        headers={config_setup.TOKEN_HEADER: token_user},
    )
    assert response.status_code == 500

    response = client.post(
        f"{url}/sepomex/estados",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )
    assert response.status_code == 500
