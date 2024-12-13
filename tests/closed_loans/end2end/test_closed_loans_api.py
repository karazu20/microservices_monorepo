import json
from datetime import datetime

from setup import config as config_setup
from src.closed_loans import config


def test_get_closed_loans(client, mambu, token_user, mocker):
    mocker.patch("setup.adapters.podemos_mambu.Loans._model_rest")
    mocker.patch("setup.adapters.podemos_mambu.Groups._model_rest")
    mock_search = mocker.patch("setup.adapters.podemos_mambu.Loans.search")

    loan = mambu.loans.build(
        id="12345",
        loan_name="Prueba",
        loan_amount=12356.5,
        interest_settings={"prueba": 2},
        closed_date=datetime.now(),
        account_state="CLOSED",
        account_sub_state="REPAID",
    )
    mock_search.return_value = [loan]

    group_fake = mambu.groups.build(id="ZX870", group_name="TestName")
    mambu.groups.add(group_fake)

    url = config.get_api_url()
    response = client.get(
        f"{url}/closed_loans/groups?group_id=ZX870",
        headers={config_setup.TOKEN_HEADER: token_user},
    )

    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["data"]["closed_loans"][0]["id"] == "12345"
    assert data["data"]["closed_loans"][0]["loan_name"] == "Prueba"
    assert data["data"]["closed_loans"][0]["amount"] == 12356.5
    assert data["data"]["closed_loans"][0]["account_state"] == "CLOSED"
    assert data["data"]["closed_loans"][0]["account_sub_state"] == "REPAID"
    assert (
        data["data"]["closed_loans"][0]["account_sub_state_label"]
        == "Todas las Obligaciones Cumplidas"
    )


def test_get_closed_loans_exception(client, mambu, token_user, mocker):
    mocker.patch("setup.adapters.podemos_mambu.Loans._model_rest")
    mocker.patch("setup.adapters.podemos_mambu.Groups._model_rest")
    mock_search = mocker.patch("setup.adapters.podemos_mambu.Loans.search")

    mock_search.side_effect = Exception("Error")

    group_fake = mambu.groups.build(id="ZX870", group_name="TestName")
    mambu.groups.add(group_fake)

    url = config.get_api_url()
    response = client.get(
        f"{url}/closed_loans/groups?group_id=ZX870",
        headers={config_setup.TOKEN_HEADER: token_user},
    )

    data = json.loads(response.data)

    assert data["error"]["msg_error"] == "Ocurrió un error vuelve a intentarlo"
