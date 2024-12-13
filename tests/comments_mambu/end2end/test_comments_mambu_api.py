import json

import pytest

from setup import config as config_setup
from setup.adapters.mambu_models import Comments
from src.comments_mambu import config


@pytest.mark.usefixtures("postgres_db")
def test_create_comments_loan_mambu(client, mambu, mocker, token_user):
    mocker.patch("setup.adapters.podemos_mambu.Loans.add_comment")

    loan_fake = mambu.loans.build(id="12345", account_state="APPROVE")
    mambu.loans.add(loan_fake)

    data = {"id_mambu": "12345", "comment": "Prueba"}

    url = config.get_api_url()
    response = client.post(
        f"{url}/comments_mambu/loan",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )

    json_response = json.loads(response.data)

    assert response.status_code == 201

    assert json_response["code"] == 201
    assert json_response["msg"] == "Success"
    assert json_response["data"] == {
        "status": True,
        "message": "Mensaje agregado con éxito",
    }


@pytest.mark.usefixtures("postgres_db")
def test_create_comments_loan_mambu_exception(client, mocker, token_user):
    mocker.patch("setup.adapters.podemos_mambu.Loans.add_comment")
    mock_mambu = mocker.patch("src.comments_mambu.services_layer.handlers.podemos_mambu")
    mock_mambu.loans.get.side_effect = Exception("Error")

    data = {"id_mambu": "54321", "comment": "Prueba"}

    url = config.get_api_url()
    response = client.post(
        f"{url}/comments_mambu/loan",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )

    assert response.status_code == 500


@pytest.mark.usefixtures("postgres_db")
def test_create_comments_mambu_group(client, mambu, mocker, token_user):
    mocker.patch("setup.adapters.podemos_mambu.Groups.add_comment")

    group_fake = mambu.groups.build(id="OU774")
    mambu.groups.add(group_fake)

    data = {"id_mambu": "OU774", "comment": "Prueba"}

    url = config.get_api_url()
    response = client.post(
        f"{url}/comments_mambu/group",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )

    json_response = json.loads(response.data)

    assert response.status_code == 201

    assert json_response["code"] == 201
    assert json_response["msg"] == "Success"
    assert json_response["data"] == {
        "status": True,
        "message": "Mensaje agregado con éxito",
    }


@pytest.mark.usefixtures("postgres_db")
def test_create_comments_mambu_group_exception(client, mocker, token_user):
    mocker.patch("setup.adapters.podemos_mambu.Groups.add_comment")
    mock_mambu = mocker.patch("src.comments_mambu.services_layer.handlers.podemos_mambu")
    mock_mambu.groups.get.side_effect = Exception("Error")

    data = {"id_mambu": "OU774", "comment": "Prueba"}

    url = config.get_api_url()
    response = client.post(
        f"{url}/comments_mambu/group",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )

    assert response.status_code == 500


@pytest.mark.usefixtures("postgres_db")
def test_create_comments_mambu_client(client, mambu, mocker, token_user):
    mocker.patch("setup.adapters.podemos_mambu.Clients.add_comment")

    client_fake = mambu.clients.build(id="OU774")
    mambu.clients.add(client_fake)

    data = {"id_mambu": "OU774", "comment": "Prueba"}

    url = config.get_api_url()
    response = client.post(
        f"{url}/comments_mambu/client",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )

    json_response = json.loads(response.data)

    assert response.status_code == 201

    assert json_response["code"] == 201
    assert json_response["msg"] == "Success"
    assert json_response["data"] == {
        "status": True,
        "message": "Mensaje agregado con éxito",
    }


@pytest.mark.usefixtures("postgres_db")
def test_create_comments_mambu_client_exception(client, mocker, token_user):
    mocker.patch("setup.adapters.podemos_mambu.Clients.add_comment")
    mock_mambu = mocker.patch("src.comments_mambu.services_layer.handlers.podemos_mambu")
    mock_mambu.clients.get.side_effect = Exception("Error")

    data = {"id_mambu": "OU774", "comment": "Prueba"}

    url = config.get_api_url()
    response = client.post(
        f"{url}/comments_mambu/client",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )

    assert response.status_code == 500


@pytest.mark.usefixtures("postgres_db")
def test_get_without_comments_mambu_loan(client, mambu, mocker, token_user):
    mocker.patch("setup.adapters.podemos_mambu.Loans._model_rest")

    loan_fake = mambu.loans.build(id="12345")
    mambu.loans.add(loan_fake)

    url = config.get_api_url()
    response = client.get(
        f"{url}/comments_mambu/loan?loan_id=12345",
        headers={config_setup.TOKEN_HEADER: token_user},
    )

    json_response = json.loads(response.data)
    assert response.status_code == 200

    assert json_response["code"] == 200
    assert json_response["msg"] == "Success"
    assert json_response["data"] == []


@pytest.mark.usefixtures("postgres_db")
def test_get_with_comments_mambu_loan(client, mambu, mocker, token_user):
    url = config.get_api_url()

    loan_fake = mambu.loans.build(
        id="12345",
        comments=[Comments(creation_date="2022-08-18", text="Prueba", user_key="1234")],
    )

    user_fake = mambu.users.build(id="1234", first_name="ANAKIN", last_name="SKYWALKER")

    mambu.loans.add(loan_fake)
    mambu.users.add(user_fake)

    response = client.get(
        f"{url}/comments_mambu/loan?loan_id=12345",
        headers={config_setup.TOKEN_HEADER: token_user},
    )

    json_response = json.loads(response.data)

    assert json_response["code"] == 200
    assert json_response["msg"] == "Success"
    assert json_response["data"] == [
        {"created": "2022-08-18", "comment": "Prueba", "user": "ANAKIN SKYWALKER"}
    ]


@pytest.mark.usefixtures("postgres_db")
def test_get_without_comments_mambu_group(client, mambu, mocker, token_user):
    mocker.patch("setup.adapters.podemos_mambu.Groups._model_rest")

    group_fake = mambu.groups.build(id="AB123")
    mambu.groups.add(group_fake)

    url = config.get_api_url()
    response = client.get(
        f"{url}/comments_mambu/group?group_id=AB123",
        headers={config_setup.TOKEN_HEADER: token_user},
    )

    json_response = json.loads(response.data)
    assert response.status_code == 200

    assert json_response["code"] == 200
    assert json_response["msg"] == "Success"
    assert json_response["data"] == []


@pytest.mark.usefixtures("postgres_db")
def test_get_with_comments_mambu_group(client, mambu, mocker, token_user):
    url = config.get_api_url()

    group_fake = mambu.groups.build(
        id="12345",
        comments=[
            Comments(creation_date="2022-08-18", text="Prueba Grupo", user_key="1234")
        ],
    )

    user_fake = mambu.users.build(id="1234", first_name="AHSOKA", last_name="TANO")

    mambu.groups.add(group_fake)
    mambu.users.add(user_fake)

    response = client.get(
        f"{url}/comments_mambu/group?group_id=12345",
        headers={config_setup.TOKEN_HEADER: token_user},
    )

    json_response = json.loads(response.data)

    assert json_response["code"] == 200
    assert json_response["msg"] == "Success"
    assert json_response["data"] == [
        {"created": "2022-08-18", "comment": "Prueba Grupo", "user": "AHSOKA TANO"}
    ]


@pytest.mark.usefixtures("postgres_db")
def test_get_without_comments_mambu_client(client, mambu, mocker, token_user):
    mocker.patch("setup.adapters.podemos_mambu.Clients._model_rest")

    client_fake = mambu.clients.build(id="AB123")
    mambu.clients.add(client_fake)

    url = config.get_api_url()
    response = client.get(
        f"{url}/comments_mambu/client?client_id=AB123",
        headers={config_setup.TOKEN_HEADER: token_user},
    )

    json_response = json.loads(response.data)
    assert response.status_code == 200

    assert json_response["code"] == 200
    assert json_response["msg"] == "Success"
    assert json_response["data"] == []


@pytest.mark.usefixtures("postgres_db")
def test_get_with_comments_mambu_client(client, mambu, mocker, token_user):
    url = config.get_api_url()

    client_fake = mambu.clients.build(
        id="12345",
        comments=[
            Comments(creation_date="2022-08-18", text="Prueba Grupo", user_key="1234")
        ],
    )

    user_fake = mambu.users.build(id="1234", first_name="OBI WAN", last_name="KENOBI")

    mambu.clients.add(client_fake)
    mambu.users.add(user_fake)

    response = client.get(
        f"{url}/comments_mambu/client?client_id=12345",
        headers={config_setup.TOKEN_HEADER: token_user},
    )

    json_response = json.loads(response.data)

    assert json_response["code"] == 200
    assert json_response["msg"] == "Success"
    assert json_response["data"] == [
        {"created": "2022-08-18", "comment": "Prueba Grupo", "user": "OBI WAN KENOBI"}
    ]
