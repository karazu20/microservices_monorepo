import json

from setup import config as config_setup
from setup.adapters.mambu_models import Installments
from src.transactions import config


def test_get_transactions(client, mambu, token_user, mocker):
    mocker.patch("setup.adapters.podemos_mambu.Loans._model_rest")
    mocker.patch("setup.adapters.podemos_mambu.Users._model_rest")
    mock_transactions = mocker.patch("setup.adapters.podemos_mambu.Transactions.search")

    loan = mambu.loans.build(
        id="12345",
    )
    transaction = mambu.transactions.build(id="123456", type_transaction="FEE_APPLIED")
    user = mambu.users.build(first_name="Gabriela", last_name="Montez")
    mock_transactions.return_value = [transaction]

    mambu.loans.add(loan)

    url = config.get_api_url()
    response = client.get(
        f"{url}/transactions?loan_id=12345",
        headers={config_setup.TOKEN_HEADER: token_user},
    )

    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["data"]["transactions"][0]["id"] == "123456"
    assert data["data"]["transactions"][0]["type"] == "Cargo aplicado"


def test_get_closed_loans_exception(client, mambu, token_user, mocker):
    mocker.patch("setup.adapters.podemos_mambu.Loans._model_rest")
    mocker.patch("setup.adapters.podemos_mambu.Users._model_rest")
    mock_transactions = mocker.patch("setup.adapters.podemos_mambu.Transactions.search")

    loan = mambu.loans.build(
        id="12345",
    )
    transaction = mambu.transactions.build(id="123456", type_transaction="FEE_APPLIED")
    user = mambu.users.build(first_name="Gabriela", last_name="Montez")

    mock_transactions.side_effect = Exception("Error")

    url = config.get_api_url()
    response = client.get(
        f"{url}/transactions?loan_id=12870",
        headers={config_setup.TOKEN_HEADER: token_user},
    )

    data = json.loads(response.data)

    assert data["error"]["msg_error"] == "Ocurrió un error vuelve a intentarlo"


def test_get_installments(client, mambu, token_user, mocker):
    mocker.patch("setup.adapters.podemos_mambu.Loans._model_rest")

    loan = mambu.loans.build(
        id="12345", installments=[Installments(last_paid_date="2022-07-25T07:06:05")]
    )
    # user = mambu.users.build(first_name="Gabriela", last_name="Montez")
    # mock_transactions.return_value = [transaction]

    mambu.loans.add(loan)

    url = config.get_api_url()
    response = client.get(
        f"{url}/transactions/installments?loan_id=12345",
        headers={config_setup.TOKEN_HEADER: token_user},
    )

    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["data"]["installments"][0]["last_paid_date"] == "2022-07-25T07:06:05"


def test_get_installments_exception(client, mambu, token_user, mocker):
    mocker.patch("setup.adapters.podemos_mambu.Loans._model_rest")
    mocker.patch("setup.adapters.podemos_mambu.Users._model_rest")
    mock_loan = mocker.patch("setup.adapters.podemos_mambu.Loans.get")

    loan = mambu.loans.build(
        id="12345", installments=[Installments(last_paid_date="2022-07-25T07:06:05")]
    )

    mock_loan.side_effect = Exception("Error")

    url = config.get_api_url()
    response = client.get(
        f"{url}/transactions/installments?loan_id=12870",
        headers={config_setup.TOKEN_HEADER: token_user},
    )

    data = json.loads(response.data)

    assert data["error"]["msg_error"] == "Ocurrió un error vuelve a intentarlo"
