from setup import config as config_setup
from src.cdc import config


def test_validations_execute(client, mambu, token_user):
    loan = mambu.loans.build(id="12345", account_state="APPROVE")
    mambu.loans.add(loan)
    loan2 = mambu.loans.build(id="54321", account_state="APPROVE")
    mambu.loans.add(loan2)
    url = config.get_api_url()
    data = [
        {
            "id_mambu": "12345",
        },
        {
            "id_mambu": "54321",
        },
    ]

    response = client.post(
        f"{url}/approvals/add_approval",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )
    assert response.status_code == 200

    loan = mambu.loans.get("12345")
    loan.account_state = "PENDING_APPROVAL"

    url = config.get_api_url()
    data = [
        {
            "id_mambu": "12345",
        },
    ]
    response = client.post(
        f"{url}/approvals/add_approval",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )
    assert response.status_code == 200
