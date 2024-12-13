from freezegun import freeze_time

from setup.adapters.mambu_models import Addresses, Branches, Users
from src.validations.domain import models
from src.validations.utils.util import convert_value_to_data_type
from src.validations.utils.validations_rules import ValidationsRules
from tests.validations.utils.util import ValidationRuleDataFake


def test_black_list_client(mocker, mambu):

    validations = ValidationsRules(
        clients=None,
        group=None,
        loan=None,
    )

    response = validations.black_list_client()

    assert response["status"]
    assert response["message"] == ""

    client = mambu.clients.build(id="OYH804", state="PRUEBA")
    validations = ValidationsRules(
        clients=[client],
        group=None,
        loan=None,
    )

    response = validations.black_list_client()
    assert response["status"]
    assert response["message"] == ""

    client = mambu.clients.build(id="OYH804", state="BLACKLISTED")
    validations = ValidationsRules(
        clients=[client],
        group=None,
        loan=None,
    )

    response = validations.black_list_client()

    assert not response["status"]
    assert (
        response["message"]
        == "Esta persona OYH804 no esta autorizada para recibir créditos en Podemos Progresar\n"
    )


def test_client_risk(mocker, mambu):

    validations = ValidationsRules(
        clients=None,
        group=None,
        loan=None,
    )

    response = validations.client_risk()

    assert response["status"]
    assert response["data_response"] == []

    client = mambu.clients.build(id="OYH804")
    validations = ValidationsRules(
        clients=[client],
        group=None,
        loan=None,
    )

    response = validations.client_risk()
    assert response["status"]
    assert response["data_response"] == []

    client = mambu.clients.build(
        id="OYH804",
        riesgo_integrante="Alto",
    )
    validations = ValidationsRules(
        clients=[client],
        group=None,
        loan=None,
    )

    response = validations.client_risk()

    assert not response["status"]
    assert (
        response["data_response"][0]["message"]
        == "La integrante OYH804 tiene riesgo Alto"
    )

    client = mambu.clients.build(
        id="OYH804",
        riesgo_integrante="Bajo",
    )
    validations = ValidationsRules(
        clients=[client],
        group=None,
        loan=None,
    )

    response = validations.client_risk()

    assert response["status"]
    assert response["data_response"] == []


def test_product_member_number(mambu):
    loan = mambu.loans.build(id="12345", assigned_centre="PRUEBA")
    client = mambu.clients.build(id="OYH804")
    rule_data_validation = [
        ValidationRuleDataFake(id=1, llave="123", valor="10", tipo_dato="int")
    ]
    validations = ValidationsRules(
        clients=[client], loan=loan, rule_data_validation=rule_data_validation
    )

    response = validations.product_member_number()

    assert response["status"] == False
    assert (
        response["data_response"][0]["message"]
        == "La cantidad de miembros del credito: 12345 no cubre el minimo necesario (10)"
    )

    rule_data_validation = [
        ValidationRuleDataFake(id=1, llave="123", valor="1", tipo_dato="int")
    ]
    validations = ValidationsRules(
        clients=[client], loan=loan, rule_data_validation=rule_data_validation
    )

    response = validations.product_member_number()

    assert response["status"] == True
    assert response["data_response"] == []

    rule_data_validation = [
        ValidationRuleDataFake(id=1, llave="Insoluto-v2", valor="1", tipo_dato="int")
    ]
    validations = ValidationsRules(
        clients=[client], loan=loan, rule_data_validation=rule_data_validation
    )

    response = validations.product_member_number()

    assert response["status"] == True
    assert response["data_response"] == []


def test_convert_value_to_data_type():
    response = convert_value_to_data_type(data_type="str", value="Prueba 1")
    assert response == "Prueba 1"

    response = convert_value_to_data_type(data_type="float", value="1.55")
    assert response == 1.55

    response = convert_value_to_data_type(data_type="int", value="10")
    assert response == 10


def test_product_validate(mambu):
    loan = mambu.loans.build(id="12345")

    validations = ValidationsRules(
        loan=loan,
    )

    response = validations.product_validate()

    assert not response["status"]
    assert (
        response["data_response"][0]["message"]
        == "El crédito: 12345 no tiene un producto de crédito activo"
    )

    loan = mambu.loans.build(
        id="12345", product_type=mambu.products.build(state="ACTIVE")
    )

    validations = ValidationsRules(
        loan=loan,
    )

    response = validations.product_validate()

    assert response["status"]
    assert response["data_response"] == []


def test_client_address_cp(mambu):
    client = mambu.clients.build(id="12345")

    validations = ValidationsRules(
        clients=[client],
    )

    response = validations.client_address_cp()

    assert not response["status"]
    assert (
        response["data_response"][0]["message"]
        == "El cliente 12345 no tiene código postal"
    )

    client = mambu.clients.build(id="12345", addresses=[Addresses(postcode="123456")])

    validations = ValidationsRules(
        clients=[client],
    )

    response = validations.client_address_cp()

    assert not response["status"]
    assert (
        response["data_response"][0]["message"]
        == "El código postal del cliente: 12345 es incorrecto"
    )


def test_client_address_state(mambu):
    client = mambu.clients.build(id="12345")

    rule_data_validation = [
        ValidationRuleDataFake(id=1, llave="AS", valor="AGUASCALIENTES", tipo_dato="str")
    ]

    validations = ValidationsRules(
        clients=[client],
        rule_data_validation=rule_data_validation,
    )

    response = validations.client_address_state()

    assert not response["status"]
    assert (
        response["data_response"][0]["message"]
        == "El cliente 12345 no tiene estado (dirección) registrado"
    )

    client = mambu.clients.build(id="12345", addresses=[Addresses(region="PRUEBA")])

    validations = ValidationsRules(
        clients=[client],
        rule_data_validation=rule_data_validation,
    )

    response = validations.client_address_state()

    assert not response["status"]
    assert (
        response["data_response"][0]["message"]
        == "El estado (dirección) del cliente: 12345 es incorrecto"
    )

    client = mambu.clients.build(
        id="12345", addresses=[Addresses(region="AGUASCALIENTES")]
    )

    validations = ValidationsRules(
        clients=[client],
        rule_data_validation=rule_data_validation,
    )

    response = validations.client_address_state()

    assert response["status"]
    assert response["data_response"] == []


def test_validate_curp():
    mambu_clients = [
        models.InitClient(
            "ABCD",
            "SIPJ800707MDFNBN03",
            "JUAN",
            "PRUEBA",
            "SIETE",
            "1980-01-07",
        )
    ]
    rule_data_validation = [
        ValidationRuleDataFake(id=1, llave="COCA", valor="CXCA", tipo_dato="str"),
        ValidationRuleDataFake(id=2, llave="RUIN", valor="RXIN", tipo_dato="str"),
    ]

    validations = ValidationsRules(
        clients=mambu_clients, rule_data_validation=rule_data_validation
    )
    response = validations.validate_curp()

    assert response["status"] == False
    assert (
        response["message"]
        == "El CURP (SIPJ800707MDFNBN03) es invalido (CURP no coincide con apellido paterno de integrante)"
    )

    mambu_clients = [
        models.InitClient(
            "ABCD",
            "SIPJ800707",
            "JUAN",
            "PRUEBA",
            "SIETE",
            "1980-01-07",
        )
    ]

    validations = ValidationsRules(
        clients=mambu_clients, rule_data_validation=rule_data_validation
    )
    response = validations.validate_curp()

    assert response["status"] == False
    assert (
        response["message"]
        == "El CURP (SIPJ800707) es invalido (longitud invalida, deben ser 18 caracteres)"
    )

    mambu_clients = [
        models.InitClient(
            "ABCD",
            "SIPÑ800707MDFNBN03",
            "JUAN",
            "PRUEBA",
            "SIETE",
            "1980-01-07",
        )
    ]

    validations = ValidationsRules(
        clients=mambu_clients, rule_data_validation=rule_data_validation
    )
    response = validations.validate_curp()

    assert response["status"] == False
    assert (
        response["message"]
        == "El CURP (SIPÑ800707MDFNBN03) es invalido (no se permiten Ñs en el CURP)"
    )

    mambu_clients = [
        models.InitClient(
            "ABCD",
            "PUSJ800707FDFNBN03",
            "JUAN",
            "PRUEBA",
            "SIETE",
            "1980-01-07",
        )
    ]

    validations = ValidationsRules(
        clients=mambu_clients, rule_data_validation=rule_data_validation
    )
    response = validations.validate_curp()

    assert response["status"] == False
    assert (
        response["message"]
        == "El CURP (PUSJ800707FDFNBN03) es invalido (CURP no coincide con apellido paterno de integrante, 1er consonante)"
    )

    mambu_clients = [
        models.InitClient(
            "ABCD",
            "RAIA921115PDFNBN03",
            "ANDREA",
            "RANGEL",
            "IBARRA",
            "1992-11-15",
        )
    ]

    validations = ValidationsRules(
        clients=mambu_clients, rule_data_validation=rule_data_validation
    )
    response = validations.validate_curp(validar=["GENERO"])

    assert response["status"] == False
    assert (
        response["message"]
        == "El CURP (RAIA921115PDFNBN03) es invalido (solo se permite genero H o M)"
    )

    mambu_clients = [
        models.InitClient(
            "ABCD",
            "RAIA921115PDFNBN03",
            "LILIANA",
            "RANGEL",
            "IBARRA",
            "1992-11-15",
        )
    ]

    validations = ValidationsRules(
        clients=mambu_clients, rule_data_validation=rule_data_validation
    )
    response = validations.validate_curp()

    assert response["status"] == False
    assert (
        response["message"]
        == "El CURP (RAIA921115PDFNBN03) es invalido (CURP no coincide con nombre de integrante)"
    )

    mambu_clients = [
        models.InitClient(
            "ABCD",
            "RAIA921115PDFNBN03",
            "ANDREA",
            "RANGEL",
            "IBARRA",
            "1992-11-25",
        )
    ]

    validations = ValidationsRules(
        clients=mambu_clients, rule_data_validation=rule_data_validation
    )
    response = validations.validate_curp()

    assert response["status"] == False
    assert (
        response["message"]
        == "El CURP (RAIA921115PDFNBN03) es invalido (fecha de nacimiento invalida)"
    )

    mambu_clients = [
        models.InitClient(
            "ABCD",
            "RAIA921115PDFNBN03",
            "ANDREA",
            "RANGEL",
            "LOPEZ",
            "1992-11-25",
        )
    ]

    validations = ValidationsRules(
        clients=mambu_clients, rule_data_validation=rule_data_validation
    )
    response = validations.validate_curp()

    assert response["status"] == False
    assert (
        response["message"]
        == "El CURP (RAIA921115PDFNBN03) es invalido (CURP no coincide con apellido materno de integrante)"
    )

    mambu_clients = [
        models.InitClient(
            "ABCD",
            "RAIN921115MDFNBD03",
            "NADIA",
            "RANGEL",
            "IBARRA",
            "1992-11-15",
        )
    ]

    validations = ValidationsRules(
        clients=mambu_clients, rule_data_validation=rule_data_validation
    )
    response = validations.validate_curp()

    assert response["status"] == True
    assert response["message"] == "CURP valido"

    mambu_clients = [
        models.InitClient(
            "ABCD",
            "RAIN921115MDFNBD03",
            "NADIA",
            "RANGEL",
            "",
            "1992-11-15",
        )
    ]

    validations = ValidationsRules(
        clients=mambu_clients, rule_data_validation=rule_data_validation
    )
    response = validations.validate_curp()

    assert response["status"] == False
    assert (
        response["message"]
        == "El CURP (RAIN921115MDFNBD03) es invalido (CURP no coincide, no hay apellido materno)"
    )

    mambu_clients = [
        models.InitClient(
            "ABCD",
            "RARN921115MDFNBD03",
            "MARIA NADIA",
            "RANGEL",
            "RUIZ",
            "1992-11-15",
        )
    ]

    validations = ValidationsRules(
        clients=mambu_clients, rule_data_validation=rule_data_validation
    )
    response = validations.validate_curp()

    assert response["status"] == False
    assert (
        response["message"]
        == "El CURP (RARN921115MDFNBD03) es invalido (CURP no coincide con apellido materno de integrante, 2da consonante)"
    )

    mambu_clients = [
        models.InitClient(
            "ABCD",
            "PEPS800324MDFXRL01",
            "SU HELEN EDITH",
            "PEÑA",
            "PEREZ",
            "1980-03-24",
        )
    ]

    validations = ValidationsRules(
        clients=mambu_clients, rule_data_validation=rule_data_validation
    )
    response = validations.validate_curp()

    assert response["status"] == False
    assert (
        response["message"]
        == "El CURP (PEPS800324MDFXRL01) es invalido (CURP no coincide con nombre de integrante, 3a consonante)"
    )

    mambu_clients = [
        models.InitClient(
            "ABCD",
            "PEZE800324MDFRUD01",
            "EDITH PEREZ Z",
            "PEREZ",
            "ZU",
            "1980-03-24",
        )
    ]

    validations = ValidationsRules(
        clients=mambu_clients, rule_data_validation=rule_data_validation
    )
    response = validations.validate_curp()

    assert response["status"] == False
    assert (
        response["message"]
        == "El CURP (PEZE800324MDFRUD01) es invalido (CURP no coincide con apellido materno de integrante, 2da consonante)"
    )

    mambu_clients = [
        models.InitClient(
            "ABCD",
            "PEZE801801MDFRXD01",
            "EDITH PEREZ Z",
            "PEREZ",
            "ZU",
            "1980-03-24",
        )
    ]

    validations = ValidationsRules(
        clients=mambu_clients, rule_data_validation=rule_data_validation
    )
    response = validations.validate_curp()

    assert response["status"] == False
    assert (
        response["message"]
        == "El CURP (PEZE801801MDFRXD01) es invalido (fecha de nacimiento invalida)"
    )

    mambu_clients = [
        models.InitClient(
            "ABCD",
            "PEZE801801MDFRXD01",
            "EDITH PEREZ Z",
            "PEREZ",
            "ZU",
            "1980-03-24",
        )
    ]

    validations = ValidationsRules(
        clients=mambu_clients, rule_data_validation=rule_data_validation
    )
    response = validations.validate_curp()

    assert response["status"] == False
    assert (
        response["message"]
        == "El CURP (PEZE801801MDFRXD01) es invalido (fecha de nacimiento invalida)"
    )


def test_validate_consult_cdc():
    clients = [
        models.InitClient(
            "ABCD", "PEZE801801MDFRXD01", "EDITH PEREZ Z", "PEREZ", "ZU", "1980-03-24"
        )
    ]

    validate_data = {"id": "algo"}
    validations = ValidationsRules(clients=clients, validate_data=validate_data)
    response = validations.validate_consult_cdc()

    assert response["status"] == False
    assert (
        response["message"]
        == "Lo sentimos la información de esta emprendedora ya fue consultada."
    )
    validate_data = {}
    validations = ValidationsRules(clients=clients, validate_data=validate_data)
    response = validations.validate_consult_cdc()
    assert response["status"] == True


@freeze_time("2022-05-27")
def test_first_meeting_date(mambu):
    loan = mambu.loans.build(id="12345")

    validations = ValidationsRules(
        loan=loan,
    )

    response = validations.first_meeting_date()

    assert response["status"] == False
    assert response["message"] == "Fecha de la primer reunión es incorrecta: None"
    loan.fecha_de_la_primer_reunion_loan = "27/05/2022"

    validations = ValidationsRules(
        loan=loan,
    )

    response = validations.first_meeting_date()

    assert response["status"] == True
    assert response["message"] == ""

    loan.fecha_de_la_primer_reunion_loan = "26-05-2022"

    validations = ValidationsRules(
        loan=loan,
    )

    response = validations.first_meeting_date()

    assert response["status"] == False
    assert (
        response["message"]
        == "La primera reunión aún no ha comenzado. Fecha de la primera reunión: 2022-05-26 00:00:00"
    )

    loan.fecha_de_la_primer_reunion_loan = "26052022"

    validations = ValidationsRules(
        loan=loan,
    )

    response = validations.first_meeting_date()

    assert response["status"] == False
    assert (
        response["message"]
        == "La fecha de primer reunión tiene un formato incorrecto. Formato correcto dd/mm/AAAA: (Ej. 26052022)"
    )


def test_validate_status_pending_approval(mambu):
    loan = mambu.loans.build(id="12345")

    validations = ValidationsRules(
        loan=loan,
    )

    response = validations.validate_status_pending_approval()

    assert response["status"] == False
    assert response["message"] == "La cuenta: 12345 no esta en Pendiente de Aprobación"

    loan.account_state = "ACTIVE"
    validations = ValidationsRules(
        loan=loan,
    )

    response = validations.validate_status_pending_approval()

    assert response["status"] == False
    assert response["message"] == "La cuenta: 12345 no esta en Pendiente de Aprobación"

    loan.account_holder_key = "fadsrqwe1234123"
    validations = ValidationsRules(
        loan=loan,
    )

    response = validations.validate_status_pending_approval()

    assert response["status"] == True
    assert response["message"] == ""

    loan.account_state = "PENDING_APPROVAL"
    validations = ValidationsRules(
        loan=loan,
    )

    response = validations.validate_status_pending_approval()

    assert response["status"] == True
    assert response["message"] == ""


def test_verify_coordinator_exists(mambu):
    group = mambu.groups.build(id="123")
    group.group_name = "Prueba"
    group.id = "1234"

    validations = ValidationsRules(
        group=group,
    )

    response = validations.verify_coordinator_exists()

    assert response["status"] == False
    assert (
        response["message"]
        == "El grupo Prueba - (ID: 1234), no tiene coordinador asignado."
    )

    group.assigned_user = Users
    group.assigned_user.encoded_key = None

    validations = ValidationsRules(
        group=group,
    )

    response = validations.verify_coordinator_exists()

    assert response["status"] == False
    assert (
        response["message"]
        == "El grupo Prueba - (ID: 1234), no tiene coordinador asignado."
    )

    group.assigned_user.encoded_key = "fadgqwer1312412"

    validations = ValidationsRules(
        group=group,
    )

    response = validations.verify_coordinator_exists()

    assert response["status"] == True
    assert response["message"] == ""


def test_verify_center_exists(mambu):
    group = mambu.groups.build(id="123")
    group.group_name = "Prueba"
    group.id = "1234"

    validations = ValidationsRules(
        group=group,
    )

    response = validations.verify_center_exists()

    assert response["status"] == False
    assert (
        response["message"]
        == "El grupo Prueba - (ID: 1234), no tiene unidad ni centro asignado. Por favor asigna una unidad y un centro al grupo."
    )

    group.assigned_branch = Branches
    group.assigned_branch.encoded_key = None

    validations = ValidationsRules(
        group=group,
    )

    response = validations.verify_center_exists()

    assert response["status"] == False
    assert (
        response["message"]
        == "El grupo Prueba - (ID: 1234), no tiene unidad ni centro asignado. Por favor asigna una unidad y un centro al grupo."
    )

    group.assigned_branch.encoded_key = "fadgqwer1312412"

    validations = ValidationsRules(
        group=group,
    )

    response = validations.verify_center_exists()

    assert response["status"] == True
    assert response["message"] == ""


def test_member_number_custom_field_in_loan(mambu):
    client = mambu.clients.build(id="OYH804")
    loan = mambu.loans.build(id="12345")

    loan.num_de_miembros_loan_accounts = "ASD"

    validations = ValidationsRules(
        loan=loan,
    )

    response = validations.member_number_custom_field_in_loan()

    assert response["status"] == False
    assert (
        response["message"]
        == "La cantidad de miembros indicada en la cuenta es inválida."
    )

    loan.num_de_miembros_loan_accounts = 0

    validations = ValidationsRules(
        loan=loan,
    )

    response = validations.member_number_custom_field_in_loan()

    assert response["status"] == False
    assert (
        response["message"]
        == "La cantidad de miembros indicada en la cuenta es inválida."
    )

    loan.num_de_miembros_loan_accounts = 2

    validations = ValidationsRules(loan=loan, clients=[client])

    response = validations.member_number_custom_field_in_loan()

    assert response["status"] == False
    assert (
        response["message"]
        == "La cantidad de miembros indicada en la cuenta es inválida."
    )

    loan.num_de_miembros_loan_accounts = 1

    validations = ValidationsRules(loan=loan, clients=[client])

    response = validations.member_number_custom_field_in_loan()

    assert response["status"] == True
    assert response["message"] == ""


def test_quote_validation_in_addresses_group(mambu):
    group = mambu.groups.build(id="123")

    validations = ValidationsRules(
        group=group,
    )

    response = validations.quote_validation_in_addresses_group()

    assert response["status"] == False
    assert response["message"] == "El grupo 123 no tiene dirección registrada"

    group = mambu.groups.build(
        id="123",
        addresses=[
            Addresses(
                line_1="2A CDA HUEXOTITLA",
                line_2="MZ 14 LT 44",
                city="CDMX",
                region="CDMX",
                postcode=14640,
                country="MEXICO",
            )
        ],
    )

    validations = ValidationsRules(
        group=group,
    )

    response = validations.quote_validation_in_addresses_group()

    assert response["status"] == True
    assert response["message"] == ""

    group = mambu.groups.build(
        id="123",
        addresses=[
            Addresses(
                line_1='2A "CDA" HUEXOTITLA',
                line_2="MZ 14 LT 44",
                city="CDMX",
                region="CDMX",
                postcode=14640,
                country="MEXICO",
            )
        ],
    )

    validations = ValidationsRules(
        group=group,
    )

    response = validations.quote_validation_in_addresses_group()

    assert response["status"] == False
    assert (
        response["message"] == "La dirección 0 del grupo 123 no puede contener comillas("
        ").\n"
    )

    group = mambu.groups.build(
        id="123",
        addresses=[
            Addresses(
                line_1="2A 'CDA' HUEXOTITLA",
                line_2="MZ 14 LT 44",
                city="CDMX",
                region="CDMX",
                postcode=14640,
                country="MEXICO",
            )
        ],
    )

    validations = ValidationsRules(
        group=group,
    )

    response = validations.quote_validation_in_addresses_group()

    assert response["status"] == False
    assert (
        response["message"] == "La dirección 0 del grupo 123 no puede contener comillas("
        ").\n"
    )


def test_quote_validation_in_addresses_client(mambu):
    client = mambu.clients.build(id="OYH804")

    validations = ValidationsRules(
        clients=[client],
    )

    response = validations.quote_validation_in_addresses_client()

    assert response["status"] == False
    assert (
        response["data_response"][0]["message"]
        == "El cliente OYH804 no tiene dirección registrada"
    )

    client = mambu.clients.build(
        id="OYH804",
        addresses=[
            Addresses(
                line_1="2A CDA HUEXOTITLA",
                line_2="MZ 14 LT 44",
                city="CDMX",
                region="CDMX",
                postcode=14640,
                country="MEXICO",
            )
        ],
    )

    validations = ValidationsRules(
        clients=[client],
    )

    response = validations.quote_validation_in_addresses_client()

    assert response["status"] == True
    assert response["data_response"] == []

    client = mambu.clients.build(
        id="OYH804",
        addresses=[
            Addresses(
                line_1='2A "CDA" HUEXOTITLA',
                line_2="MZ 14 LT 44",
                city="CDMX",
                region="CDMX",
                postcode=14640,
                country="MEXICO",
            )
        ],
    )

    validations = ValidationsRules(
        clients=[client],
    )

    response = validations.quote_validation_in_addresses_client()

    assert response["status"] == False
    assert (
        response["data_response"][0]["message"]
        == "La dirección 0 del cliente OYH804 no puede contener comillas("
        ")."
    )

    client = mambu.clients.build(
        id="OYH804",
        addresses=[
            Addresses(
                line_1="2A 'CDA' HUEXOTITLA",
                line_2="MZ 14 LT 44",
                city="CDMX",
                region="CDMX",
                postcode=14640,
                country="MEXICO",
            )
        ],
    )

    validations = ValidationsRules(
        clients=[client],
    )

    response = validations.quote_validation_in_addresses_client()

    assert response["status"] == False
    assert (
        response["data_response"][0]["message"]
        == "La dirección 0 del cliente OYH804 no puede contener comillas("
        ")."
    )
