from datetime import datetime

from src.validations.utils.validations_rules import ValidationsRules
from tests.validations.utils.util import ValidationRuleDataFake


def test_street_address(mambu, mocker):
    mocker.patch("setup.adapters.podemos_mambu.Clients._model_rest")

    client = mambu.clients.build(
        id="12345",
        first_name="Taylor",
        last_name="Swift",
        addresses=[mambu.addresses.build(line_1="|")],
    )

    validations = ValidationsRules(clients=[client])

    response = validations.street_address()

    assert response["data_response"][0]["message"] == (
        "Calle y número invalidos. La dirección de la integrante Taylor Swift - (ID: 12345), presenta "
        "errores en los campos: Calle y Número.\n"
    )
    assert not response["status"]

    client = mambu.clients.build(
        id="12345",
        first_name="Taylor",
        last_name="Swift",
        addresses=[mambu.addresses.build(line_1=None)],
    )

    validations = ValidationsRules(clients=[client])

    response = validations.street_address()

    assert response["data_response"][0]["message"] == (
        "Calle y número invalidos. La dirección de la integrante Taylor Swift - (ID: 12345), presenta "
        "errores en los campos: Calle y Número.\n"
    )
    assert not response["status"]

    client = mambu.clients.build(
        id="12345",
        first_name="Taylor",
        last_name="Swift",
        addresses=[mambu.addresses.build(line_1="")],
    )

    validations = ValidationsRules(clients=[client])

    response = validations.street_address()

    assert response["data_response"][0]["message"] == (
        "Calle y número invalidos. La dirección de la integrante Taylor Swift - (ID: 12345), presenta "
        "errores en los campos: Calle y Número.\n"
    )
    assert not response["status"]

    client = mambu.clients.build(
        id="12345",
        first_name="Taylor",
        last_name="Swift",
        addresses=[mambu.addresses.build(line_1="prueba #3")],
    )

    validations = ValidationsRules(clients=[client])

    response = validations.street_address()

    assert response["data_response"] == []
    assert response["status"]

    client = mambu.clients.build(
        id="12345",
        first_name="Taylor",
        last_name="Swift",
        addresses=[mambu.addresses.build(line_1="prueba S//N")],
    )

    validations = ValidationsRules(clients=[client])

    response = validations.street_address()

    assert (
        response["data_response"][0]["message"]
        == "Calle/Numero de Taylor Swift (12345) en formato incorrecto (prueba S//N)\n"
    )
    assert not response["status"]


def test_street_address_exception(mocker, mambu):
    mocker.patch("setup.adapters.podemos_mambu.Clients._model_rest")
    mock_street = mocker.patch(
        "src.validations.utils.digital_validations_rules.extract_streetnumber"
    )

    mock_street.side_effect = Exception("Prueba")

    client = mambu.clients.build(
        id="12345",
        first_name="Taylor",
        last_name="Swift",
        addresses=[mambu.addresses.build(line_1="prueba #3")],
    )

    validations = ValidationsRules(clients=[client])

    response = validations.street_address()
    assert response["data_response"][0]["message"] == (
        "Error desconocido validando calle/numero de la direccion de la integrante Taylor Swift (12345)"
        " (error: Exception('Prueba'), favor de informar este mensaje completo a TI)\n"
    )
    assert not response["status"]


def test_colony_address(mocker, mambu):
    mocker.patch("setup.adapters.podemos_mambu.Clients._model_rest")

    client = mambu.clients.build(
        id="12345",
        first_name="Taylor",
        last_name="Swift",
        addresses=[mambu.addresses.build(line_2="")],
    )

    validations = ValidationsRules(clients=[client])

    response = validations.colony_address()
    assert response["data_response"][0]["message"] == (
        "Colonia invalida. La dirección de la integrante Taylor Swift - "
        "(ID: 12345), presenta un error en el campo: Colonia.\n"
    )
    assert not response["status"]

    client = mambu.clients.build(
        id="12345",
        first_name="Taylor",
        last_name="Swift",
        addresses=[mambu.addresses.build(line_2=None)],
    )

    validations = ValidationsRules(clients=[client])

    response = validations.colony_address()

    assert response["data_response"][0]["message"] == (
        "Colonia invalida. La dirección de la integrante Taylor Swift - "
        "(ID: 12345), presenta un error en el campo: Colonia.\n"
    )
    assert not response["status"]

    client = mambu.clients.build(
        id="12345",
        first_name="Taylor",
        last_name="Swift",
        addresses=[mambu.addresses.build(line_2="Prueba")],
    )

    validations = ValidationsRules(clients=[client])

    response = validations.colony_address()

    assert response["data_response"] == []
    assert response["status"]


def test_municipality_address(mambu, mocker):
    mocker.patch("setup.adapters.podemos_mambu.Clients._model_rest")

    rule_data_validation = [
        ValidationRuleDataFake(
            id=1,
            llave="Atizapán de Zaragoza",
            valor="Atizapán de Zaragoza",
            tipo_dato="str",
        ),
    ]
    client = mambu.clients.build(
        id="12345",
        first_name="Taylor",
        last_name="Swift",
        addresses=[mambu.addresses.build(city="")],
    )

    validations = ValidationsRules(
        clients=[client], rule_data_validation=rule_data_validation
    )

    response = validations.municipality_address()

    assert response["data_response"][0]["message"] == (
        "El Municipio es inválido. La dirección de la "
        "integrante Taylor Swift - (ID: 12345), tiene un error en el campo Municipio. \n"
    )
    assert not response["status"]

    client = mambu.clients.build(
        id="12345",
        first_name="Taylor",
        last_name="Swift",
        addresses=[mambu.addresses.build(city=None)],
    )

    validations = ValidationsRules(
        clients=[client], rule_data_validation=rule_data_validation
    )

    response = validations.municipality_address()

    assert response["data_response"][0]["message"] == (
        "El Municipio es inválido. La dirección de la "
        "integrante Taylor Swift - (ID: 12345), tiene un error en el campo Municipio. None\n"
    )
    assert not response["status"]

    client = mambu.clients.build(
        id="12345",
        first_name="Taylor",
        last_name="Swift",
        addresses=[mambu.addresses.build(city="Atizapán de Zaragoza")],
    )

    validations = ValidationsRules(
        clients=[client], rule_data_validation=rule_data_validation
    )

    response = validations.municipality_address()

    assert response["data_response"] == []
    assert response["status"]


def test_validate_curp_pcp(mambu):
    id_document = mambu.id_documents.build(
        document_id="TOGM920527HDFRNR06", document_type="CURP"
    )

    client = mambu.clients.build(
        id_documents=[id_document],
        first_name="MARCO ANDRES",
        last_name="TORRE GONZALEZ",
        birth_date=datetime.strptime("1992-05-27", "%Y-%m-%d"),
    )
    rule_data_validation = [
        ValidationRuleDataFake(id=1, llave="COCA", valor="CXCA", tipo_dato="str"),
        ValidationRuleDataFake(id=2, llave="RUIN", valor="RXIN", tipo_dato="str"),
    ]

    validations = ValidationsRules(
        type_validation="PCP", clients=[client], rule_data_validation=rule_data_validation
    )
    response = validations.validate_curp()

    assert response["message"] == "CURP valido"
    assert response["status"]
