from datetime import datetime

from freezegun import freeze_time

from setup.adapters.mambu_models import (
    Branches,
    DisbursementsDetails,
    Installments,
    Loans,
    Users,
)
from src.validations.utils.util import disbursement_date
from src.validations.utils.validations_rules import ValidationsRules
from tests.validations.utils.util import ValidationRuleDataFake


@freeze_time("2022-05-27")
def test_calendar_validate(mambu):
    loan = mambu.loans.build(id="12345")

    validations = ValidationsRules(
        loan=loan,
    )

    response = validations.calendar_validate()

    assert response["status"] == False
    assert (
        response["data_response"][0]["message"]
        == "La cuenta debe tener un calendario de pagos asignado"
    )

    loan = mambu.loans.build(
        id="12345", installments=[Installments(due_date=datetime.now())]
    )

    validations = ValidationsRules(
        loan=loan,
    )

    response = validations.calendar_validate()

    assert response["status"] == True
    assert response["data_response"] == []

    loan = mambu.loans.build(id="12345", installments=[Installments(due_date="")])

    validations = ValidationsRules(
        loan=loan,
    )

    response = validations.calendar_validate()

    assert response["status"] == False
    assert (
        response["data_response"][0]["message"]
        == "La cuenta debe tener un calendario de pagos asignado"
    )


def test_validate_tribe_in_group(mambu):
    loan = mambu.loans.build(id="12345")
    group = mambu.groups.build(id="ABC123")

    validations = ValidationsRules(loan=loan, group=group)

    response = validations.validate_tribe_in_group()

    assert (
        response["data_response"][0]["message"]
        == "El crédito: 12345 no tiene asignado coordinador"
    )
    assert (
        response["data_response"][1]["message"]
        == "El grupo: ABC123 no tiene asignado coordinador"
    )
    assert response["status"] == False

    loan = mambu.loans.build(id="12345", assigned_user=Users(id="1234"))
    group = mambu.groups.build(id="ABC123", assigned_user=Users(id="1234"))

    validations = ValidationsRules(loan=loan, group=group)

    response = validations.validate_tribe_in_group()

    assert response["status"] == True
    assert response["data_response"] == []

    loan = mambu.loans.build(id="12345", assigned_user=Users(id="12345"))
    group = mambu.groups.build(id="ABC123", assigned_user=Users(id="1234"))

    validations = ValidationsRules(loan=loan, group=group)

    response = validations.validate_tribe_in_group()

    assert response["status"] == False
    assert (
        response["data_response"][0]["message"]
        == "El coordinador del grupo no coincide con el del crédito"
    )


def test_weeks_mix_interest(mambu, mocker):
    mocker.patch("setup.adapters.podemos_mambu.Loans._model_rest")
    mocker.patch("setup.adapters.podemos_mambu.Groups._model_rest")
    mock_search = mocker.patch("setup.adapters.podemos_mambu.Loans.search")

    loan = mambu.loans.build(
        id="12345",
        loan_name="Prueba",
        account_state="PRUEBA",
        installments=[Installments(due_date=datetime.now())],
    )
    group = mambu.groups.build(id="ABC123")

    validations = ValidationsRules(loan=loan, group=group)

    response = validations.weeks_mix_interest()

    assert response["status"] == True
    assert response["data_response"] == []

    loan = mambu.loans.build(
        id="12345",
        loan_name="INTERES MIXTO INSOLUTO",
        account_state="ACTIVE",
        installments=[
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
        ],
        original_account_key="1231232",
    )

    validations = ValidationsRules(loan=loan, group=group)

    response = validations.weeks_mix_interest()

    assert response["status"] == True
    assert response["data_response"] == []

    mock_search.return_value = []
    loan = mambu.loans.build(
        id="12345",
        loan_name="INTERES MIXTO INSOLUTO",
        account_state="PENDING_APPROVAL",
        installments=[
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
        ],
        original_account_key="1231232",
    )

    validations = ValidationsRules(loan=loan, group=group)

    response = validations.weeks_mix_interest()

    assert response["status"] == True
    assert response["data_response"] == []

    loan = mambu.loans.build(
        id="12345",
        loan_name="INTERES MIXTO INSOLUTO",
        account_state="PENDING_APPROVAL",
        installments=[
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
        ],
        original_account_key="1231232",
    )

    validations = ValidationsRules(loan=loan, group=group)

    response = validations.weeks_mix_interest()

    assert response["status"] == True
    assert response["data_response"] == []

    mock_search.return_value = [Loans(id="12345", account_state="ACTIVE")]
    loan = mambu.loans.build(
        id="12345",
        loan_name="INTERES MIXTO INSOLUTO",
        account_state="PENDING_APPROVAL",
        installments=[
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
        ],
    )

    validations = ValidationsRules(loan=loan, group=group)

    response = validations.weeks_mix_interest()

    assert response["status"] == True
    assert response["data_response"] == []

    loan = mambu.loans.build(
        id="12345",
        loan_name="INTERES MIXTO INSOLUTO",
        account_state="PENDING_APPROVAL",
        installments=[
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
            Installments(due_date=datetime.now()),
        ],
        original_account_key="1231232",
    )
    validations = ValidationsRules(loan=loan, group=group)

    response = validations.weeks_mix_interest()

    assert response["status"] == False
    assert (
        response["data_response"][0]["message"]
        == "La cuenta 12345 INTERES MIXTO INSOLUTO, solo puede tener 11, 15 o 23 semanas"
    )


def test_client_notes(mambu, mocker):
    mocker.patch("setup.adapters.podemos_mambu.Loans._model_rest")
    mocker.patch("setup.adapters.podemos_mambu.Clients._model_rest")

    loan = mambu.loans.build(id="12345", integrantes_loan=[])
    client = mambu.clients.build(id="OYH804")

    validations = ValidationsRules(loan=loan, clients=[client])

    response = validations.client_notes()

    assert response["status"] == False
    assert response["data_response"][0]["message"] == (
        "La cantidad de miembros indicada en la cuenta, no es la "
        "misma que la cantidad de integrantes del crédito."
    )

    loan = mambu.loans.build(
        id="12345",
        integrantes_loan=[
            {
                "montoanterior": 11000,
                "monto": 11000,
                "integrante": "8a818f44761ff694017623e0ae093e01",
                "_index": 0,
            }
        ],
        num_de_miembros_loan_accounts=1,
    )
    client = mambu.clients.build(
        id="OYH804", encoded_key="8a818f44761ff694017623e0ae093e01"
    )

    validations = ValidationsRules(loan=loan, clients=[client])

    response = validations.client_notes()

    assert response["status"] == True
    assert response["data_response"] == []

    loan = mambu.loans.build(
        id="12345",
        integrantes_loan=[
            {"montoanterior": 11000, "monto": 11000, "integrante": "123214", "_index": 0}
        ],
        num_de_miembros_loan_accounts=1,
    )
    client = mambu.clients.build(
        id="OYH804", encoded_key="8a818f44761ff694017623e0ae093e01"
    )

    validations = ValidationsRules(loan=loan, clients=[client])

    response = validations.client_notes()

    assert response["status"] == False
    assert (
        response["data_response"][0]["message"]
        == "La integrante 123214 no pertenece a este grupo."
    )


def test_authorization_op(mambu, mocker):
    mocker.patch("setup.adapters.podemos_mambu.Loans._model_rest")
    mocker.patch("setup.adapters.podemos_mambu.Groups._model_rest")
    mock_search = mocker.patch("setup.adapters.podemos_mambu.Loans.search")

    loan = mambu.loans.build(id="12345")
    group = mambu.groups.build(id="ABC123")

    validations = ValidationsRules(loan=loan, group=group)

    response = validations.authorization_op()

    assert response["status"] == False
    assert response["data_response"][0]["message"] == (
        "Un credito del ciclo 1 debe tener: " "Generalidades de Autorización Operativa"
    )

    loan = mambu.loans.build(id="12345", generalidades_loan_accounts="0")
    product = mambu.products.build(name="Credito Adicional")
    mock_search.return_value = [
        Loans(id="12345", account_state="ACTIVE", product_type=product)
    ]

    validations = ValidationsRules(loan=loan, group=group)

    response = validations.authorization_op()

    assert response["status"] == False
    assert (
        response["data_response"][0]["message"]
        == "Un credito del ciclo 1 debe tener: Generalidades de Autorización Operativa"
    )

    loan = mambu.loans.build(
        id="12345", generalidades_loan_accounts=0, renovacion_loan_accounts="0"
    )

    validations = ValidationsRules(loan=loan, group=group)

    response = validations.authorization_op()
    assert response["status"] == False
    assert (
        response["data_response"][0]["message"]
        == "Un crédito en Renovación debe tener Renovación de Autorización Operativa"
    )

    user_one = mambu.users.build(id="12345")
    user_two = mambu.users.build(id="54321")
    user_three = mambu.users.build(id="78945")

    loan = mambu.loans.build(
        id="12345",
        generalidades_loan_accounts=0,
        renovacion_loan_accounts=0,
        autlegmenu=user_one,
        autopmenu=user_one,
    )

    validations = ValidationsRules(loan=loan, group=group)

    response = validations.authorization_op()

    assert response["status"] == False
    assert (
        response["data_response"][0]["message"]
        == "El usuario que hizo la Autorización Operativa, es el mismo que el que hizo la Autorizacion Legal."
    )

    loan = mambu.loans.build(
        id="12345",
        generalidades_loan_accounts=0,
        renovacion_loan_accounts=0,
        autlegmenu=user_one,
        autopmenu=user_two,
        intgpomenu=user_two,
    )

    validations = ValidationsRules(loan=loan, group=group)

    response = validations.authorization_op()

    assert response["status"] == False
    assert (
        response["data_response"][0]["message"]
        == "El usuario que hizo la Autorización Operativa, es el mismo que el que hizo la Integración."
    )

    loan = mambu.loans.build(
        id="12345",
        generalidades_loan_accounts=0,
        renovacion_loan_accounts=0,
        autlegmenu=user_one,
        autopmenu=user_two,
        intgpomenu=user_one,
    )

    validations = ValidationsRules(loan=loan, group=group)

    response = validations.authorization_op()

    assert response["status"] == False
    assert (
        response["data_response"][0]["message"]
        == "El usuario que hizo la Autorización Legal, es el mismo que el que hizo la Integración."
    )

    loan = mambu.loans.build(
        id="12345",
        generalidades_loan_accounts=0,
        renovacion_loan_accounts=0,
        autlegmenu=user_one,
        autopmenu=user_two,
        intgpomenu=user_three,
    )

    validations = ValidationsRules(loan=loan, group=group)

    response = validations.authorization_op()

    assert response["status"] == True
    assert response["data_response"] == []


def test_endorsement_exceed(mambu, mocker):
    mocker.patch("setup.adapters.podemos_mambu.Loans._model_rest")
    mocker.patch("setup.adapters.podemos_mambu.Groups._model_rest")
    mocker.patch("setup.adapters.podemos_mambu.Loans.search")

    loan = mambu.loans.build(
        id="12345",
        integrantes_loan=[
            {"montoanterior": 11000, "monto": 11000, "integrante": "123214", "_index": 0}
        ],
    )
    group = mambu.groups.build(id="ABC123")
    rule_data_validation = [
        ValidationRuleDataFake(id=1, llave="123", valor="0.375", tipo_dato="float")
    ]

    validations = ValidationsRules(
        loan=loan, group=group, rule_data_validation=rule_data_validation
    )

    response = validations.endorsement_exceed()

    assert response["status"] == False
    assert (
        response["data_response"][0]["message"]
        == "Deben existir los roles de lider y tesorera en el grupo: ABC123"
    )

    role_tesorera = mambu.group_roles.build(role_name="Tesorera")
    role_lider = mambu.group_roles.build(role_name="Lider")
    client = mambu.clients.build(id="OYH804", encoded_key="12435643")
    client_lider = mambu.clients.build(id="MATI12", encoded_key="12345643")
    group_member = mambu.group_members.build(
        roles=[role_tesorera], encoded_key="12345", client=client
    )
    group_member_lider = mambu.group_members.build(
        roles=[role_lider], encoded_key="54321", client=client_lider
    )
    group = mambu.groups.build(id="123", group_members=[group_member, group_member_lider])

    validations = ValidationsRules(
        loan=loan, group=group, rule_data_validation=rule_data_validation
    )

    response = validations.endorsement_exceed()

    assert response["data_response"][0]["message"] == (
        "No se puede endosar a la Tesorera del grupo: 123, los roles Tesorera y Lider "
        "necesitan endosar. Por favor cambia los endosos o  los roles del grupo e inténtalo de nuevo."
    )
    assert response["status"] == False

    loan = mambu.loans.build(
        id="12345",
        integrantes_loan=[
            {
                "montoanterior": 11000,
                "monto": 11000,
                "integrante": "54321",
                "_index": 0,
                "endoso": True,
            }
        ],
    )
    validations = ValidationsRules(
        loan=loan, group=group, rule_data_validation=rule_data_validation
    )

    response = validations.endorsement_exceed()

    assert (
        response["data_response"][0]["message"]
        == "Solo se puede endosar a la Tesorera un maximo del 0.375 de integrantes del grupo"
    )
    assert response["status"] == False

    client_first = mambu.clients.build(id="OYH805", encoded_key="120870")
    client_second = mambu.clients.build(id="OYH806", encoded_key="110119")
    client_third = mambu.clients.build(id="OYH807", encoded_key="270592")
    group_member_first = mambu.group_members.build(
        roles=[], encoded_key="120399", client=client_first
    )
    group_member_second = mambu.group_members.build(
        roles=[], encoded_key="030594", client=client_second
    )
    group_member_third = mambu.group_members.build(
        roles=[], encoded_key="280168", client=client_third
    )

    group = mambu.groups.build(
        id="123",
        group_members=[
            group_member,
            group_member_lider,
            group_member_first,
            group_member_second,
            group_member_third,
        ],
    )
    loan = mambu.loans.build(
        id="12345",
        integrantes_loan=[
            {
                "montoanterior": 11000,
                "monto": 11000,
                "integrante": "12435643",
                "_index": 0,
                "endoso": True,
            },
            {"montoanterior": 11000, "monto": 11000, "integrante": "12345", "_index": 0},
            {"montoanterior": 11000, "monto": 11000, "integrante": "120870", "_index": 0},
            {"montoanterior": 11000, "monto": 11000, "integrante": "110119", "_index": 0},
            {"montoanterior": 11000, "monto": 11000, "integrante": "270592", "_index": 0},
        ],
    )

    validations = ValidationsRules(
        loan=loan, group=group, rule_data_validation=rule_data_validation
    )

    response = validations.endorsement_exceed()

    assert response["data_response"] == []
    assert response["status"] == True


def test_client_address_cp(mambu):
    client = mambu.clients.build(
        id="12345", addresses=[mambu.addresses.build(postcode=123456)]
    )

    validations = ValidationsRules(
        clients=[client],
    )

    response = validations.client_address_cp()

    assert not response["status"]
    assert (
        response["data_response"][0]["message"]
        == "El código postal del cliente: 12345 es incorrecto"
    )

    client = mambu.clients.build(
        id="12345", addresses=[mambu.addresses.build(postcode=14470)]
    )

    validations = ValidationsRules(
        clients=[client],
    )

    response = validations.client_address_cp()

    assert response["status"]
    assert response["data_response"] == []


def test_role_authorization(mambu, mocker):
    mocker.patch("setup.adapters.podemos_mambu.Loans._model_rest")

    loan = mambu.loans.build(id="12345")

    validations = ValidationsRules(
        loan=loan,
    )

    response = validations.role_authorization()

    assert response["status"] == False
    assert (
        response["data_response"][0]["message"] == "La cuenta no tiene un usuario user_cs"
    )
    assert (
        response["data_response"][1]["message"] == "La cuenta no tiene un usuario user_ca"
    )
    assert (
        response["data_response"][2]["message"] == "La cuenta no tiene un usuario user_ce"
    )

    loan = mambu.loans.build(
        id="12345",
        autopmenu=mambu.users.build(id="123"),
        autlegmenu=mambu.users.build(id="124"),
        intgpomenu=mambu.users.build(id="125"),
    )

    validations = ValidationsRules(
        loan=loan,
    )

    response = validations.role_authorization()

    assert response["status"] == False
    assert (
        response["data_response"][0]["message"]
        == "El usuario que hizo la Autorizacion Operativa no es Consejero. Escribiste 'None'"
    )
    assert (
        response["data_response"][1]["message"]
        == "El usuario que hizo la Autorizacion Legal no es Coordinador Administrativo. Escribiste 'None'"
    )
    assert (
        response["data_response"][2]["message"]
        == "El usuario que hizo la integracion no tiene permisos de CE. Escribiste 'None'"
    )

    loan = mambu.loans.build(
        id="12345",
        autopmenu=mambu.users.build(id="123", title="Consejero"),
        autlegmenu=mambu.users.build(id="124", title="Coordinador Administrativo"),
        intgpomenu=mambu.users.build(id="125", title="Coordinador de emprendedoras"),
    )

    validations = ValidationsRules(
        loan=loan,
    )

    response = validations.role_authorization()

    assert response["status"]
    assert response["data_response"] == []

    loan = mambu.loans.build(
        id="12345",
        autopmenu=mambu.users.build(id="123", title="Consejero"),
        autlegmenu=mambu.users.build(id="124", title="Coordinador Administrativo"),
        intgpomenu=mambu.users.build(
            id="125", title="Prueba", access={"creditOfficerAccess": True}
        ),
    )

    validations = ValidationsRules(
        loan=loan,
    )

    response = validations.role_authorization()

    assert response["status"]
    assert response["data_response"] == []


def test_group_in_client(mambu, mocker):
    mocker.patch("setup.adapters.podemos_mambu.Clients._model_rest")
    mocker.patch("setup.adapters.podemos_mambu.Groups._model_rest")
    mocker.patch("setup.adapters.podemos_mambu.Loans._model_rest")
    mock_search = mocker.patch("setup.adapters.podemos_mambu.Loans.search")

    client = mambu.clients.build(id="OYH804", groups=[])

    validations = ValidationsRules(
        clients=[client],
    )

    response = validations.group_in_client()

    assert response["status"]
    assert response["data_response"] == []

    loan = mambu.loans.build(id="12345", account_state="ACTIVE")
    mock_search.return_value = [loan]
    group = mambu.groups.build(id="ABC123")
    client = mambu.clients.build(id="OYH804", groups=[group])

    validations = ValidationsRules(
        clients=[client],
    )

    response = validations.group_in_client()

    assert response["status"]
    assert response["data_response"] == []
    mock_search.assert_called()

    mock_search.reset_mock()
    mock_search.return_value = []
    group = mambu.groups.build(id="ABC123")
    client = mambu.clients.build(id="OYH804", groups=[group])

    validations = ValidationsRules(
        clients=[client],
    )

    response = validations.group_in_client()
    assert response["status"]
    assert response["data_response"] == []
    mock_search.assert_called()

    mock_search.reset_mock()
    mock_search.return_value = [loan]
    branch = Branches(id="Anoat")
    group = mambu.groups.build(
        id="ABC123", group_name="Estrella de la Muerte", assigned_branch=branch
    )
    group_two = mambu.groups.build(
        id="123ABC", group_name="Vader", assigned_branch=branch
    )
    client = mambu.clients.build(
        id="OYH804", groups=[group, group_two], first_name="Anakin", last_name="Skywalker"
    )

    validations = ValidationsRules(
        clients=[client],
    )

    response = validations.group_in_client()

    assert not response["status"]
    assert response["data_response"][0]["message"] == (
        "La integrante Anakin Skywalker - (ID: OYH804) pertenece a más de "
        "un grupo solidario ['Estrella de la Muerte ABC123 Anoat', 'Vader 123ABC Anoat']"
    )


def test_renewal_num_member(mambu, mocker):
    mocker.patch("setup.adapters.podemos_mambu.Clients._model_rest")
    mocker.patch("setup.adapters.podemos_mambu.Groups._model_rest")
    mocker.patch("setup.adapters.podemos_mambu.Loans._model_rest")
    mock_search = mocker.patch("setup.adapters.podemos_mambu.Loans.search")

    rule_data_validation = [
        ValidationRuleDataFake(id=1, llave="123", valor="0.5", tipo_dato="float")
    ]

    group = mambu.groups.build(id="ABC123", loan_cycle=0)
    loan = mambu.loans.build(id="12345", account_holder=group)

    validations = ValidationsRules(loan=loan, rule_data_validation=rule_data_validation)

    response = validations.renewal_num_member()

    assert response["status"]
    assert response["data_response"] == []

    group = mambu.groups.build(id="ABC123", loan_cycle=1)
    loan = mambu.loans.build(id="12345", account_holder=group)

    validations = ValidationsRules(loan=loan, rule_data_validation=rule_data_validation)

    response = validations.renewal_num_member()

    assert response["status"]
    assert response["data_response"] == []

    group = mambu.groups.build(id="ABC123", loan_cycle=0)
    loan = mambu.loans.build(
        id="12345",
        account_holder=group,
        loan_name="Credito Adicional",
        account_state="ACTIVE",
        account_sub_state="",
    )

    validations = ValidationsRules(loan=loan, rule_data_validation=rule_data_validation)

    response = validations.renewal_num_member()

    assert response["status"]
    assert response["data_response"] == []

    mock_search.return_value = [
        Loans(
            id="123456",
            account_state="ACTIVE",
            integrantes_loan=[
                {
                    "montoanterior": 11000,
                    "monto": 11000,
                    "integrante": "8a818f44761ff694017623e0ae093e01",
                    "_index": 0,
                }
            ],
        )
    ]
    group = mambu.groups.build(id="ABC123", loan_cycle=1)
    loan = mambu.loans.build(
        id="12345",
        account_holder=group,
        loan_name="Prueba",
        integrantes_loan=[
            {
                "montoanterior": 11000,
                "monto": 11000,
                "integrante": "8a818f44761ff694017623e0ae093e01",
                "_index": 0,
            }
        ],
    )

    validations = ValidationsRules(loan=loan, rule_data_validation=rule_data_validation)

    response = validations.renewal_num_member()

    assert response["status"]
    assert response["data_response"] == []

    mock_search.return_value = [
        Loans(
            id="123456",
            account_state="ACTIVE",
            integrantes_loan=[
                {
                    "montoanterior": 11000,
                    "monto": 11000,
                    "integrante": "312321",
                    "_index": 0,
                }
            ],
        )
    ]
    group = mambu.groups.build(id="ABC123", loan_cycle=1)
    loan = mambu.loans.build(
        id="12345",
        account_holder=group,
        loan_name="Prueba",
        integrantes_loan=[
            {
                "montoanterior": 11000,
                "monto": 11000,
                "integrante": "8a818f44761ff694017623e0ae093e01",
                "_index": 0,
            }
        ],
    )

    validations = ValidationsRules(loan=loan, rule_data_validation=rule_data_validation)

    response = validations.renewal_num_member()

    assert not response["status"]
    assert (
        response["data_response"][0]["message"]
        == "La cuenta renovada debe tener al menos el 50% de las mismas integrantes que la anterior"
    )


@freeze_time("2022-05-27")
def test_disbursement_date(mambu):
    loan = mambu.loans.build(
        id="12345",
        disbursement_details=DisbursementsDetails(
            disbursement_date=datetime.strptime("2022-05-03", "%Y-%m-%d")
        ),
    )

    response = disbursement_date(loan=loan)

    assert datetime.strptime("2022-05-03", "%Y-%m-%d") == response

    loan = mambu.loans.build(
        id="12345",
        disbursement_details=DisbursementsDetails(
            disbursement_date=None,
            expected_disbursement_date=datetime.strptime("2022-03-12", "%Y-%m-%d"),
        ),
    )

    response = disbursement_date(loan=loan)
    assert datetime.strptime("2022-03-12", "%Y-%m-%d") == response

    loan = mambu.loans.build(id="12345", disbursement_details=None)

    response = disbursement_date(loan=loan)
    assert datetime.strptime("2022-05-27", "%Y-%m-%d") == response


def test_political_exposed(mambu):
    client = mambu.clients.build(id="12345", people_could_political_exposed="Prueba")

    validations = ValidationsRules(clients=[client])

    response = validations.political_exposed()

    assert response["status"]
    assert response["data_response"] == []

    client = mambu.clients.build(id="12345", people_could_political_exposed=131232)

    validations = ValidationsRules(clients=[client])

    response = validations.political_exposed()

    assert not response["status"]
    assert response["data_response"][0]["message"] == (
        "El campo 'Personas relacionadas que podrian ser "
        "politicamente expuestas' de 131232 debe ser un texto"
    )

    client = mambu.clients.build(
        id="12345",
    )

    validations = ValidationsRules(clients=[client])

    response = validations.political_exposed()

    assert response["status"]
    assert response["data_response"] == []
