import json
from datetime import date

import pytest

from setup import config as config_setup
from src.groups import config


@pytest.fixture(scope="module")
def usuarios(digitalization_session):
    digitalization_session.execute(
        "INSERT INTO usuario (username, first_name, first_surname, insert_date) VALUES (:username, :first_name, :first_surname, :insert_date)",
        dict(
            username="user.fake",
            first_name="pepe",
            first_surname="perez",
            insert_date=date.today(),
        ),
    )
    digitalization_session.commit()


@pytest.mark.usefixtures("postgres_db")
def test_groups(mocker, client, token_user, usuarios):
    url = config.get_api_url()
    data = {"nombre": "grupo_dummy"}
    response = client.post(
        f"{url}/groups/grupo", headers={config_setup.TOKEN_HEADER: token_user}, json=data
    )
    assert response.status_code == 201

    response = client.get(
        f"{url}/groups/grupo", headers={config_setup.TOKEN_HEADER: token_user}
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert len(response_data["data"]["grupos"]) == 1
