from src.mambu.domain.queries import GetClient
from src.mambu.utils import util


def test_get_json_group(mambu):
    group_fake = mambu.groups.build(id="ZX870", group_name="TestName")

    response = util.get_json_group(group_fake)

    assert response["id"] == "ZX870"
    assert response["group_name"] == "TestName"


def test_get_json_data_roles(mambu):
    group_member_fake = mambu.group_members.build(
        roles=[], client=mambu.clients.build(id="JHN123")
    )
    group_fake = mambu.groups.build(
        id="ZX870",
        group_name="TestName",
        group_members=[group_member_fake],
    )

    response = util.get_json_data_roles(clients=group_fake.group_members)
    assert not response

    group_member_fake = mambu.group_members.build(
        roles=[mambu.group_roles.build(role_name="Lider")],
        client=mambu.clients.build(
            id="JHN123",
            first_name="Wan",
            last_name="SkyWalker",
            home_phone="5547551732",
            mobile_phone="5567928651",
        ),
    )

    group_fake.group_members = [group_member_fake]
    response = util.get_json_data_roles(clients=group_fake.group_members)

    assert response["full_name"] == "Wan SkyWalker"
    assert response["mobile_phone"] == "5567928651"
    assert response["home_phone"] == "5547551732"

    response = util.get_json_data_roles(clients=[])

    assert not response


def test_get_criteria_data():
    queries_fields = GetClient("12345", "Anakin", "Wan", "SkyWalker", "GOGM920330", 10, 2)

    array_search_key = {
        "client_id": ("id", "startwith"),
        "first_name": ("firstName", "startwith"),
        "middle_name": ("middleName", "startwith"),
        "last_name": ("lastName", "startwith"),
        "rfc": ("_datossolicitante_integrante.rfc", "startwith"),
    }

    response = util.get_criteria_data(
        array_search_key=array_search_key, criteria=queries_fields
    )

    assert response[0][0] == "id"
    assert response[0][2] == "12345"
    assert response[1][0] == "firstName"
    assert response[1][2] == "Anakin"
    assert response[2][0] == "middleName"
    assert response[2][2] == "Wan"

    queries_fields = GetClient(None, "Anakin", "Wan", "SkyWalker", "GOGM920330", 10, 2)

    response = util.get_criteria_data(
        array_search_key=array_search_key, criteria=queries_fields
    )

    assert response[0][0] == "firstName"
    assert response[0][2] == "Anakin"


def test_get_json_client(mambu):
    client_fake = mambu.clients.build(
        id="JHN123",
        first_name="Wan",
        last_name="SkyWalker",
        home_phone="5547551732",
        mobile_phone="5567928651",
    )

    response = util.get_json_client(client=client_fake)

    assert response["id"] == "JHN123"
    assert response["full_name"] == "Wan SkyWalker"
    assert response["mobile_phone"] == "5567928651"
    assert response["home_phone"] == "5547551732"


def test_get_json_client_addresses(mambu):
    address_fake = mambu.addresses.build(
        line_1="2A CDA HUEXOTITLA",
        line_2="SAN PEDRO",
        city="TLALPAN",
        region="CDMX",
        postcode="14640",
        country="MEXICO",
    )

    client_fake = mambu.clients.build(
        id="JHN123",
        addresses=[address_fake],
    )

    response = util.get_json_client_addresses(addresses=client_fake.addresses)

    assert response[0]["street"] == "2A CDA HUEXOTITLA"
    assert response[0]["colony"] == "SAN PEDRO"
    assert response[0]["municipality"] == "TLALPAN"
    assert response[0]["state"] == "CDMX"
    assert response[0]["postal_code"] == "14640"
    assert response[0]["country"] == "MEXICO"

    response = util.get_json_client_addresses(addresses=[])

    assert not response


def test_get_json_loan(mambu):
    loan_fake = mambu.loans.build(id="12345", encoded_key="54321", account_state="ACTIVE")

    response = util.get_json_loan(loan=loan_fake)

    assert response["id"] == "12345"
    assert response["encoded_key"] == "54321"
    assert response["status"] == "ACTIVE"


def test_get_disbursement_details(mambu):

    disbursement_details_fake = mambu.disbursements_details.build(
        expected_disbursement_date="2022-07-11",
        disbursement_date="2022-07-11",
        first_repayment_date="2022-07-18",
        transaction_details={"transactionChannelId": "CASH"},
    )

    loan_fake = mambu.loans.build(
        id="12345",
        encoded_key="54321",
        account_state="ACTIVE",
        disbursement_details=disbursement_details_fake,
    )

    response = util.get_disbursement_details(disbursement_details=[])

    assert not response

    response = util.get_disbursement_details(
        disbursement_details=loan_fake.disbursement_details
    )

    assert response["expected_disbursement_date"] == "2022-07-11"
    assert response["disbursement_date"] == "2022-07-11"
    assert response["first_payment_date"] == "2022-07-18"
    assert response["payment_method"] == "CASH"


def test_get_disbursement_details_incomplete_data(mambu):
    disbursement_details_fake = mambu.disbursements_details.build(
        expected_disbursement_date="2022-07-11",
        first_repayment_date="2022-07-18",
        transaction_details={"transactionChannelId": "CASH"},
    )
    loan_fake = mambu.loans.build(
        id="12345",
        encoded_key="54321",
        account_state="ACTIVE",
        disbursement_details=disbursement_details_fake,
    )

    response = util.get_disbursement_details(
        disbursement_details=loan_fake.disbursement_details
    )

    assert response["expected_disbursement_date"] == "2022-07-11"
    assert response["disbursement_date"] == None
    assert response["first_payment_date"] == "2022-07-18"
    assert response["payment_method"] == "CASH"
