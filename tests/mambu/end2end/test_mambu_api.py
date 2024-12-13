import json

from setup import config as config_setup
from src.mambu import config


def test_get_groups(client, mambu, token_user):
    group_fake = mambu.groups.build(id="ZX870", group_name="TestName")
    mambu.groups.add(group_fake)

    url = config.get_api_url()
    response = client.get(
        f"{url}/mambu/groups/ZX870",
        headers={config_setup.TOKEN_HEADER: token_user},
    )

    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["id"] == "ZX870"
    assert data["group_name"] == "TestName"
    assert "encoded_key" in data

    response = client.get(
        f"{url}/mambu/groups?group_name=TestName",
        headers={config_setup.TOKEN_HEADER: token_user},
    )

    data = json.loads(response.data)

    assert response.status_code == 200
    assert data[0]["id"] == "ZX870"
    assert data[0]["group_name"] == "TestName"
    assert "encoded_key" in data[0]


def test_get_loans(client, mambu, token_user):
    loans_fake = mambu.loans.build(id="12345", account_state="ACTIVE")
    mambu.loans.add(loans_fake)

    url = config.get_api_url()
    response = client.get(
        f"{url}/mambu/loans/12345",
        headers={config_setup.TOKEN_HEADER: token_user},
    )

    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["id"] == "12345"
    assert data["status"] == "ACTIVE"
    assert "encoded_key" in data

    response = client.get(
        f"{url}/mambu/loans?status=INACTIVE",
        headers={config_setup.TOKEN_HEADER: token_user},
    )

    data = json.loads(response.data)

    assert response.status_code == 200
    assert data[0]["id"] == "12345"
    assert data[0]["status"] == "ACTIVE"
    assert "encoded_key" in data[0]

    response = client.get(
        f"{url}/mambu/loans?date_init=2022-12-27",
        headers={config_setup.TOKEN_HEADER: token_user},
    )

    data = json.loads(response.data)
    assert response.status_code == 500
    assert "date_end es requerida" in data["message"]

    response = client.get(
        f"{url}/mambu/loans?date_end=2022-12-27",
        headers={config_setup.TOKEN_HEADER: token_user},
    )

    data = json.loads(response.data)
    assert response.status_code == 500
    assert "date_init es requerida" in data["message"]

    response = client.get(
        f"{url}/mambu/loans?date_init=202212-01&date_end=2022-12-27",
        headers={config_setup.TOKEN_HEADER: token_user},
    )
    data = json.loads(response.data)
    assert response.status_code == 500
    assert (
        "date_init formato incorrecto de fecha, el correcto es Y-m-d" in data["message"]
    )

    response = client.get(
        f"{url}/mambu/loans?date_init=2022-12-01&date_end=202212-27",
        headers={config_setup.TOKEN_HEADER: token_user},
    )
    data = json.loads(response.data)
    assert response.status_code == 500
    assert "date_end formato incorrecto de fecha, el correcto es Y-m-d" in data["message"]

    response = client.get(
        f"{url}/mambu/loans?date_init=2022-12-01&date_end=2022-12-27",
        headers={config_setup.TOKEN_HEADER: token_user},
    )

    data = json.loads(response.data)
    assert response.status_code == 200
    assert data[0]["id"] == "12345"
    assert data[0]["status"] == "ACTIVE"
    assert "encoded_key" in data[0]


def test_get_clients(client, mambu, token_user):
    client_fake = mambu.clients.build(
        id="AH123", first_name="Andres", middle_name="Marco", last_name="De la Torre"
    )
    mambu.clients.add(client_fake)

    url = config.get_api_url()
    response = client.get(
        f"{url}/mambu/clients/AH123",
        headers={config_setup.TOKEN_HEADER: token_user},
    )

    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["id"] == "AH123"
    assert data["full_name"] == "Andres Marco De la Torre"
    assert "encoded_key" in data

    response = client.get(
        f"{url}/mambu/clients?rfc=TOGM920527",
        headers={config_setup.TOKEN_HEADER: token_user},
    )

    data = json.loads(response.data)

    assert response.status_code == 200
    assert data[0]["id"] == "AH123"
    assert data[0]["full_name"] == "Andres Marco De la Torre"
    assert "encoded_key" in data[0]


def test_get_loans_data_response(client, mambu, token_user):
    loans_fake = mambu.loans.build(id="12345", account_state="ACTIVE")
    mambu.loans.add(loans_fake)

    url = config.get_api_url()
    response = client.get(
        f"{url}/mambu/loans?status=PENDING_APPROVAL&data_response=id",
        headers={config_setup.TOKEN_HEADER: token_user},
    )

    data = json.loads(response.data)

    assert response.status_code == 200
    assert data[0]["id"] == "12345"


def test_get_loans_tribu(client, mambu, token_user):
    assigned_centre = mambu.centres.build(name="TribuNZ-1")
    loans_fake = mambu.loans.build(
        id="12345", account_state="ACTIVE", assigned_centre=assigned_centre
    )
    mambu.loans.add(loans_fake)

    url = config.get_api_url()
    response = client.get(
        f"{url}/mambu/loans?tribu=TribuNZ-1",
        headers={config_setup.TOKEN_HEADER: token_user},
    )

    data = json.loads(response.data)

    assert response.status_code == 200
    assert data[0]["id"] == "12345"
    assert data[0]["tribu"] == "TribuNZ-1"
