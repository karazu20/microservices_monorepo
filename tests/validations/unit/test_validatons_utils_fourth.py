from datetime import datetime

from freezegun import freeze_time

from src.validations.utils.util import extract_min_max_levels, find_client
from src.validations.utils.validations_rules import ValidationsRules
from tests.validations.utils.util import ValidationRuleDataFake


def test_amnt_valid_client(mambu, mocker):
    mocker.patch("setup.adapters.podemos_mambu.Loans._model_rest")
    mocker.patch("setup.adapters.podemos_mambu.Clients._model_rest")
    mocker.patch("setup.adapters.podemos_mambu.Groups._model_rest")

    rule_data_validation = [
        ValidationRuleDataFake(id=1, llave="min", valor="8000", tipo_dato="int"),
        ValidationRuleDataFake(id=2, llave="min", valor="10001", tipo_dato="int"),
        ValidationRuleDataFake(id=3, llave="min", valor="15001", tipo_dato="int"),
        ValidationRuleDataFake(id=4, llave="min", valor="20001", tipo_dato="int"),
        ValidationRuleDataFake(id=5, llave="min", valor="25001", tipo_dato="int"),
        ValidationRuleDataFake(id=6, llave="min", valor="30001", tipo_dato="int"),
        ValidationRuleDataFake(id=7, llave="min", valor="35001", tipo_dato="int"),
        ValidationRuleDataFake(id=8, llave="max", valor="10000", tipo_dato="int"),
        ValidationRuleDataFake(id=9, llave="max", valor="15000", tipo_dato="int"),
        ValidationRuleDataFake(id=10, llave="max", valor="20000", tipo_dato="int"),
        ValidationRuleDataFake(id=11, llave="max", valor="25000", tipo_dato="int"),
        ValidationRuleDataFake(id=12, llave="max", valor="30000", tipo_dato="int"),
        ValidationRuleDataFake(id=13, llave="max", valor="35000", tipo_dato="int"),
        ValidationRuleDataFake(id=14, llave="max", valor="100000", tipo_dato="int"),
    ]

    client_one = mambu.clients.build(
        id="12345",
        encoded_key="12345",
        first_name="Anakin",
        last_name="SkyWalker",
    )
    client_two = mambu.clients.build(
        id="54321",
        encoded_key="54321",
        first_name="Obi",
        last_name="Wan",
    )
    client_three = mambu.clients.build(
        id="78945",
        encoded_key="78945",
        first_name="Troy",
        last_name="Bolton",
    )

    loan = mambu.loans.build(id="12345")

    validations = ValidationsRules(loan=loan)

    response = validations.amnt_valid_client()

    assert response["status"]
    assert response["data_response"] == []

    integrantes_loan = [
        {
            "monto": 30000,
            "integrante": "54321",
        },
        {
            "monto": 11000,
            "integrante": "12345",
        },
    ]
    loan = mambu.loans.build(id="12345", integrantes_loan=integrantes_loan)
    validations = ValidationsRules(
        loan=loan,
        clients=[client_one, client_two],
        rule_data_validation=rule_data_validation,
    )

    response = validations.amnt_valid_client()

    assert response["status"]
    assert response["data_response"] == []

    integrantes_loan = [
        {
            "monto": 300000,
            "integrante": "54321",
        },
        {
            "monto": -1,
            "integrante": "12345",
        },
        {
            "monto": 1000,
            "integrante": "78945",
        },
    ]
    loan = mambu.loans.build(id="12345", integrantes_loan=integrantes_loan)
    validations = ValidationsRules(
        loan=loan,
        clients=[client_one, client_two, client_three],
        rule_data_validation=rule_data_validation,
    )

    response = validations.amnt_valid_client()

    assert response["data_response"][0]["message"] == (
        "Las integrantes no pueden recibir una cantidad tan grande "
        "(Obi Wan (54321): $300000.00; max: $100000.00)"
    )
    assert response["data_response"][1]["message"] == (
        "La cantidad para Anakin SkyWalker - (ID: 12345) es invalida: $-1.00"
    )
    assert response["data_response"][2]["message"] == (
        "Las integrantes no pueden recibir una cantidad tan chica"
        " (Troy Bolton (78945): $1000.00; min: $8000.00)"
    )
    assert not response["status"]


def test_find_client(mambu, mocker):
    client = mambu.clients.build(id="OYH804", encoded_key="41242rqadf")
    response = find_client(id="41242rqadf", clients=[client])
    assert response == client

    response = find_client(id="41242", clients=[client])
    assert not response


def test_extract_min_max_levels(mambu, mocker):
    rule_data_validation = [
        ValidationRuleDataFake(id=1, llave="min", valor=8000, tipo_dato="int"),
        ValidationRuleDataFake(id=2, llave="min", valor=10001, tipo_dato="int"),
        ValidationRuleDataFake(id=3, llave="min", valor=15001, tipo_dato="int"),
        ValidationRuleDataFake(id=4, llave="min", valor=20001, tipo_dato="int"),
        ValidationRuleDataFake(id=5, llave="min", valor=25001, tipo_dato="int"),
        ValidationRuleDataFake(id=6, llave="min", valor=30001, tipo_dato="int"),
        ValidationRuleDataFake(id=7, llave="min", valor=35001, tipo_dato="int"),
        ValidationRuleDataFake(id=8, llave="max", valor=10000, tipo_dato="int"),
        ValidationRuleDataFake(id=9, llave="max", valor=15000, tipo_dato="int"),
        ValidationRuleDataFake(id=10, llave="max", valor=20000, tipo_dato="int"),
        ValidationRuleDataFake(id=11, llave="max", valor=25000, tipo_dato="int"),
        ValidationRuleDataFake(id=12, llave="max", valor=30000, tipo_dato="int"),
        ValidationRuleDataFake(id=13, llave="max", valor=35000, tipo_dato="int"),
        ValidationRuleDataFake(id=14, llave="max", valor=100000, tipo_dato="int"),
    ]

    response = extract_min_max_levels(data=rule_data_validation, value_to_extract="min")
    assert response == 8000

    response = extract_min_max_levels(data=rule_data_validation, value_to_extract="max")
    assert response == 100000

    response = extract_min_max_levels(data=rule_data_validation, value_to_extract="test")
    assert not response


def test_last_amnt_valid_client(mambu, mocker):
    mocker.patch("setup.adapters.podemos_mambu.Loans._model_rest")
    mocker.patch("setup.adapters.podemos_mambu.Clients._model_rest")
    mocker.patch("setup.adapters.podemos_mambu.Groups._model_rest")

    rule_data_validation = [
        ValidationRuleDataFake(id=1, llave="min", valor="8000", tipo_dato="int"),
        ValidationRuleDataFake(id=2, llave="min", valor="10001", tipo_dato="int"),
        ValidationRuleDataFake(id=3, llave="min", valor="15001", tipo_dato="int"),
        ValidationRuleDataFake(id=4, llave="min", valor="20001", tipo_dato="int"),
        ValidationRuleDataFake(id=5, llave="min", valor="25001", tipo_dato="int"),
        ValidationRuleDataFake(id=6, llave="min", valor="30001", tipo_dato="int"),
        ValidationRuleDataFake(id=7, llave="min", valor="35001", tipo_dato="int"),
        ValidationRuleDataFake(id=8, llave="max", valor="10000", tipo_dato="int"),
        ValidationRuleDataFake(id=9, llave="max", valor="15000", tipo_dato="int"),
        ValidationRuleDataFake(id=10, llave="max", valor="20000", tipo_dato="int"),
        ValidationRuleDataFake(id=11, llave="max", valor="25000", tipo_dato="int"),
        ValidationRuleDataFake(id=12, llave="max", valor="30000", tipo_dato="int"),
        ValidationRuleDataFake(id=13, llave="max", valor="35000", tipo_dato="int"),
        ValidationRuleDataFake(id=14, llave="max", valor="100000", tipo_dato="int"),
    ]

    client_one = mambu.clients.build(
        id="12345",
        encoded_key="12345",
        first_name="Anakin",
        last_name="SkyWalker",
    )
    client_two = mambu.clients.build(
        id="54321",
        encoded_key="54321",
        first_name="Obi",
        last_name="Wan",
    )

    loan = mambu.loans.build(id="12345")

    validations = ValidationsRules(loan=loan)

    response = validations.last_amnt_valid_client()

    assert response["status"]
    assert response["data_response"] == []

    integrantes_loan = [
        {
            "montoanterior": 30000,
            "integrante": "54321",
        },
        {
            "montoanterior": 11000,
            "integrante": "12345",
        },
    ]
    loan = mambu.loans.build(id="12345", integrantes_loan=integrantes_loan)
    validations = ValidationsRules(
        loan=loan,
        clients=[client_one, client_two],
        rule_data_validation=rule_data_validation,
    )

    response = validations.last_amnt_valid_client()

    assert response["status"]
    assert response["data_response"] == []

    integrantes_loan = [
        {
            "montoanterior": -10,
            "integrante": "54321",
        },
        {
            "montoanterior": 110000,
            "integrante": "12345",
        },
    ]
    loan = mambu.loans.build(id="12345", integrantes_loan=integrantes_loan)
    validations = ValidationsRules(
        loan=loan,
        clients=[client_one, client_two],
        rule_data_validation=rule_data_validation,
    )

    response = validations.last_amnt_valid_client()

    assert response["data_response"][0]["message"] == (
        "La cantidad anterior para Obi Wan (54321) es invalida: $-10.00"
    )
    assert response["data_response"][1]["message"] == (
        "Las integrantes no pudieron haber recibido una cantidad tan grande en "
        "su ultimo credito (Anakin SkyWalker (12345): $110000.00; max: $100000.00)"
    )
    assert not response["status"]


def test_total_amount_notes(mambu, mocker):
    mocker.patch("setup.adapters.podemos_mambu.Loans._model_rest")
    integrantes_loan = [
        {
            "monto": 15000,
            "integrante": "54321",
        },
        {
            "monto": 20000,
            "integrante": "12345",
        },
    ]

    loan = mambu.loans.build(
        id="12345", integrantes_loan=integrantes_loan, loan_amount=35000
    )

    validations = ValidationsRules(loan=loan)

    response = validations.total_amount_notes()

    assert response["status"]
    assert response["data_response"] == []

    loan = mambu.loans.build(
        id="12345",
        integrantes_loan=integrantes_loan,
        loan_amount=35000,
        original_account_key="123123",
    )

    validations = ValidationsRules(loan=loan)

    response = validations.total_amount_notes()

    assert response["status"]
    assert response["data_response"] == []

    integrantes_loan = [
        {
            "monto": 15000,
            "integrante": "54321",
        },
    ]

    loan = mambu.loans.build(
        id="12345",
        integrantes_loan=integrantes_loan,
        loan_amount=35000,
        original_account_key="123123",
    )

    validations = ValidationsRules(loan=loan)

    response = validations.total_amount_notes()

    assert not response["status"]
    assert response["data_response"][0]["message"] == (
        "Las cantidades asignadas a las integrantes, no suman el total de "
        "la cuenta. (Total de la cuenta: $35000.00, suma: $15000.00)"
    )


def test_num_members_in_notes(mambu, mocker):
    mocker.patch("setup.adapters.podemos_mambu.Clients._model_rest")
    mocker.patch("setup.adapters.podemos_mambu.Groups._model_rest")
    mocker.patch("setup.adapters.podemos_mambu.Loans._model_rest")
    mocker.patch("setup.adapters.podemos_mambu.Loans.search")

    client = mambu.clients.build(id="OYH804", encoded_key="12435643")
    group_member = mambu.group_members.build(encoded_key="12345", client=client)
    group = mambu.groups.build(id="ABC123", loan_cycle=0, group_members=[group_member])

    integrantes_loan = [
        {
            "monto": 15000,
            "integrante": "54321",
        },
        {
            "monto": 20000,
            "integrante": "12345",
        },
    ]

    loan = mambu.loans.build(
        id="12345", integrantes_loan=integrantes_loan, account_holder=group
    )

    validations = ValidationsRules(loan=loan)

    response = validations.num_members_in_notes()

    assert not response["status"]
    assert response["data_response"][0]["message"] == (
        "La cantidad de miembros del grupo ABC123, no es la misma que la cantidad de "
        "integrantes en las notas del crédito (Cantidad de miembros: 1, Notas de crédito: 2)"
    )

    integrantes_loan = [
        {
            "monto": 15000,
            "integrante": "54321",
        },
    ]

    loan = mambu.loans.build(
        id="12345", integrantes_loan=integrantes_loan, account_holder=group
    )

    validations = ValidationsRules(loan=loan)

    response = validations.num_members_in_notes()

    assert response["status"]
    assert response["data_response"] == []

    integrantes_loan = [
        {
            "monto": 15000,
            "integrante": "54321",
        },
        {
            "monto": 20000,
            "integrante": "12345",
        },
    ]

    loan = mambu.loans.build(
        id="12345",
        integrantes_loan=integrantes_loan,
        account_holder=group,
        loan_name="Credito Adicional",
    )

    validations = ValidationsRules(loan=loan)

    response = validations.num_members_in_notes()

    assert not response["status"]
    assert response["data_response"][0]["message"] == (
        "La cantidad de miembros del grupo ABC123, es menor a la cantidad de "
        "integrantes en las notas del crédito (Cantidad de miembros: 1, Notas de crédito: 2)"
    )

    integrantes_loan = [
        {
            "monto": 15000,
            "integrante": "54321",
        },
    ]

    loan = mambu.loans.build(
        id="12345",
        integrantes_loan=integrantes_loan,
        account_holder=group,
        loan_name="Credito Adicional",
    )

    validations = ValidationsRules(loan=loan)

    response = validations.num_members_in_notes()

    assert response["status"]
    assert response["data_response"] == []


def test_cycle_valid(mambu, mocker):
    mocker.patch("setup.adapters.podemos_mambu.Clients._model_rest")
    mocker.patch("setup.adapters.podemos_mambu.Groups._model_rest")
    mocker.patch("setup.adapters.podemos_mambu.Loans._model_rest")
    mocker.patch("setup.adapters.podemos_mambu.Products._model_rest")
    mock_search = mocker.patch("setup.adapters.podemos_mambu.Loans.search")
    mock_search.return_value = [mambu.loans.build(id="54321", account_state="ACTIVE")]

    loan = mambu.loans.build(
        id="12345",
    )

    validations = ValidationsRules(loan=loan)

    response = validations.cycle_valid()

    assert not response["status"]
    assert (
        response["data_response"][0]["message"]
        == "El ciclo en el crédito: 12345 es requerido"
    )

    loan = mambu.loans.build(
        id="12345", loan_name="Prueba", account_state="ACTIVE", ciclo=2
    )
    group = mambu.groups.build(id="ABC123")

    validations = ValidationsRules(loan=loan, group=group)

    response = validations.cycle_valid()

    assert response["status"]
    assert response["data_response"] == []

    mock_search.reset_mock()
    mock_search.return_value = []
    loan = mambu.loans.build(
        id="12345", loan_name="Prueba", account_state="ACTIVE", ciclo=2
    )
    group = mambu.groups.build(id="ABC123")

    products = [mambu.products.build(name="Prueba")]
    validations = ValidationsRules(loan=loan, group=group, products=products)

    response = validations.cycle_valid()

    assert response["data_response"][0]["message"] == (
        "La información del campo: Ciclo personalizado, no coincide con el "
        "número de cuentas validas cerradas, (Crédito: 12345, Ciclo: 2, Cuentas validas cerradas: 1)."
    )
    assert not response["status"]

    loan = mambu.loans.build(
        id="12345", loan_name="Prueba", account_state="ACTIVE", ciclo=1
    )
    group = mambu.groups.build(id="ABC123")

    products = [mambu.products.build(name="Prueba")]
    validations = ValidationsRules(loan=loan, group=group, products=products)

    response = validations.cycle_valid()

    assert response["data_response"] == []
    assert response["status"]

    mock_search.return_value = [
        mambu.loans.build(id="54321", account_sub_state="WITHDRAWN")
    ]
    loan = mambu.loans.build(
        id="12345", loan_name="Prueba", account_state="ACTIVE", ciclo=1
    )
    group = mambu.groups.build(id="ABC123")

    products = [mambu.products.build(name="Prueba")]
    validations = ValidationsRules(loan=loan, group=group, products=products)

    response = validations.cycle_valid()

    assert response["data_response"] == []
    assert response["status"]


def test_not_special_characters_in_name(mambu, mocker):
    mocker.patch("setup.adapters.podemos_mambu.Clients._model_rest")

    client = mambu.clients.build(id="OYH804", first_name="Troy", last_name="Bolton")

    validations = ValidationsRules(clients=[client])

    response = validations.not_special_characters_in_name()

    assert response["data_response"] == []
    assert response["status"]

    client = mambu.clients.build(id="OYH804", first_name="Troy%$", last_name="Bolton")

    validations = ValidationsRules(clients=[client])

    response = validations.not_special_characters_in_name()

    assert (
        response["data_response"][0]["message"]
        == "El nombre de la integrante Troy%$ Bolton (ID: OYH804), tiene caracteres inválidos"
    )
    assert not response["status"]


def test_curp_validate(mambu, mocker):
    mocker.patch("setup.adapters.podemos_mambu.Clients._model_rest")
    curp_mock = mocker.patch("setup.adapters.podemos_mambu.Clients.search_by_curp")

    client = mambu.clients.build(id="OYH804", first_name="Troy", last_name="Bolton")
    curp_mock.return_value = [client]

    validations = ValidationsRules(clients=[client])

    response = validations.curp_validate()

    assert response["data_response"] == []
    assert response["status"]
    curp_mock.assert_called()

    curp_mock.return_value = [client, client]

    validations = ValidationsRules(clients=[client])
    response = validations.curp_validate()

    assert response["data_response"][0]["message"] == (
        "CURP existente La CURP:  de la integrante"
        " Troy Bolton, pertenece a ['OYH804', 'OYH804'] ."
    )
    assert not response["status"]


def test_clients_in_group(mambu, mocker):
    mocker.patch("setup.adapters.podemos_mambu.Clients._model_rest")
    mocker.patch("setup.adapters.podemos_mambu.Groups._model_rest")
    mocker.patch("setup.adapters.podemos_mambu.Loans._model_rest")
    mocker.patch("setup.adapters.podemos_mambu.Loans.search")
    mock_client = mocker.patch("setup.adapters.podemos_mambu.Clients.get")

    integrantes_loan = [
        {
            "integrante": "54321",
        },
        {
            "integrante": "12345",
        },
        {
            "integrante": "78945",
        },
    ]

    client = mambu.clients.build(
        id="OYH804", encoded_key="12435643", first_name="Teodoro", last_name="Alvin"
    )
    mock_client.return_value = client
    group_member = mambu.group_members.build(encoded_key="12345", client=client)
    group = mambu.groups.build(id="ABC123", loan_cycle=0, group_members=[group_member])
    loan = mambu.loans.build(id="12345", integrantes_loan=integrantes_loan)

    validations = ValidationsRules(loan=loan, group=group)

    response = validations.clients_in_group()

    assert response["data_response"][0]["message"] == (
        "La cliente: Teodoro Alvin - OYH804 no esta en el grupo"
    )
    assert response["data_response"][1]["message"] == (
        "La cliente: Teodoro Alvin - OYH804 no esta en el grupo"
    )
    assert response["data_response"][2]["message"] == (
        "La cliente: Teodoro Alvin - OYH804 no esta en el grupo"
    )
    assert not response["status"]

    integrantes_loan = [
        {
            "integrante": "12435643",
        },
    ]

    client = mambu.clients.build(
        id="OYH804", encoded_key="12435643", first_name="Teodoro", last_name="Alvin"
    )
    mock_client.return_value = client
    group_member = mambu.group_members.build(encoded_key="12345", client=client)
    group = mambu.groups.build(id="ABC123", loan_cycle=0, group_members=[group_member])
    loan = mambu.loans.build(id="12345", integrantes_loan=integrantes_loan)

    validations = ValidationsRules(loan=loan, group=group)

    response = validations.clients_in_group()

    assert response["data_response"] == []
    assert response["status"]


def test_same_clients_in_loan(mambu, mocker):
    mocker.patch("setup.adapters.podemos_mambu.Clients._model_rest")
    mocker.patch("setup.adapters.podemos_mambu.Loans._model_rest")
    mock_client = mocker.patch("setup.adapters.podemos_mambu.Clients.get")

    integrantes_loan = [
        {
            "integrante": "15121989",
        },
        {
            "integrante": "05111987",
        },
        {
            "integrante": "16111992",
        },
    ]

    client_one = mambu.clients.build(
        id="JB121", encoded_key="15121989", first_name="Joe", last_name="Jonas"
    )
    client_two = mambu.clients.build(
        id="JB122", encoded_key="05111987", first_name="Kevin", last_name="Jonas"
    )
    client_three = mambu.clients.build(
        id="JB123", encoded_key="16111992", first_name="Nick", last_name="Jonas"
    )
    loan = mambu.loans.build(id="12345", integrantes_loan=integrantes_loan)

    validations = ValidationsRules(loan=loan)

    response = validations.same_clients_in_loan()

    assert response["data_response"] == []
    assert response["status"]

    integrantes_loan = [
        {
            "integrante": "15121989",
        },
        {
            "integrante": "05111987",
        },
        {
            "integrante": "16111992",
        },
        {
            "integrante": "16111992",
        },
    ]
    mock_client.return_value = client_three
    loan = mambu.loans.build(id="12345", integrantes_loan=integrantes_loan)

    validations = ValidationsRules(loan=loan)

    response = validations.same_clients_in_loan()

    assert (
        response["data_response"][0]["message"]
        == "Hay integrantes duplicadas en la cuenta:  - Nick Jonas (JB123)"
    )
    assert not response["status"]


def test_group_meeting_day(mambu, mocker):
    mocker.patch("setup.adapters.podemos_mambu.Groups._model_rest")
    mocker.patch("setup.adapters.podemos_mambu.Loans._model_rest")

    group = mambu.groups.build(id="ABC123")
    loan = mambu.loans.build(id="12345", account_holder=group)

    validations = ValidationsRules(loan=loan)

    response = validations.group_meeting_day()

    assert (
        response["data_response"][0]["message"]
        == "El campo: Día de reunión es necesario en el grupo ABC123"
    )
    assert not response["status"]

    group = mambu.groups.build(id="ABC123", dia_de_reunion_groups="MIERCOLES")
    loan = mambu.loans.build(id="12345", account_holder=group)

    validations = ValidationsRules(loan=loan)

    response = validations.group_meeting_day()

    assert (
        response["data_response"][0]["message"]
        == "El campo: Fecha de la primera reunión es necesario en el crédito 12345"
    )
    assert not response["status"]

    loan = mambu.loans.build(
        id="12345", account_holder=group, fecha_de_la_primer_reunion_loan="27051992"
    )

    validations = ValidationsRules(loan=loan)

    response = validations.group_meeting_day()

    assert response["data_response"][0]["message"] == (
        "La fecha de primer reunión tiene un formato incorrecto"
        ", formato correcto: dd/mm/AAAA del crédito: 12345"
    )
    assert not response["status"]

    loan = mambu.loans.build(
        id="12345", account_holder=group, fecha_de_la_primer_reunion_loan="27/05/1992"
    )

    validations = ValidationsRules(loan=loan)

    response = validations.group_meeting_day()

    assert response["data_response"] == []
    assert response["status"]

    loan = mambu.loans.build(
        id="12345", account_holder=group, fecha_de_la_primer_reunion_loan="28/05/1992"
    )

    validations = ValidationsRules(loan=loan)

    response = validations.group_meeting_day()
    assert response["data_response"][0]["message"] == (
        "El día de la primera reunión de la cuenta es (JUEVES),"
        " no coincide con el día de reunión del grupo (MIERCOLES)."
    )
    assert not response["status"]


def test_difference_of_days_in_day_meeting(mambu, mocker):
    mocker.patch("setup.adapters.podemos_mambu.Loans._model_rest")

    loan = mambu.loans.build(id="12345")

    validations = ValidationsRules(loan=loan)

    response = validations.difference_of_days_in_day_meeting()

    assert response["data_response"][0]["message"] == (
        "El campo: Día de pago, es necesario. En el crédito: 12345"
    )
    assert not response["status"]

    loan = mambu.loans.build(id="12345", dia_de_pago_loan_accounts="MIERCOLES")
    validations = ValidationsRules(loan=loan)

    response = validations.difference_of_days_in_day_meeting()

    assert (
        response["data_response"][0]["message"]
        == "El campo: Fecha de la primera reunión es necesario en el crédito 12345"
    )
    assert not response["status"]

    loan = mambu.loans.build(
        id="12345",
        dia_de_pago_loan_accounts="MIERCOLES",
        fecha_de_la_primer_reunion_loan="27051992",
    )
    validations = ValidationsRules(loan=loan)

    response = validations.difference_of_days_in_day_meeting()

    assert response["data_response"][0]["message"] == (
        "La fecha de primer reunión tiene un formato incorrecto"
        ", formato correcto: dd/mm/AAAA del crédito: 12345"
    )
    assert not response["status"]

    loan = mambu.loans.build(
        id="12345",
        dia_de_pago_loan_accounts="MIERCOLES",
        fecha_de_la_primer_reunion_loan="27/05/1992",
    )
    validations = ValidationsRules(loan=loan)

    response = validations.difference_of_days_in_day_meeting()

    assert response["data_response"] == []
    assert response["status"]

    loan = mambu.loans.build(
        id="12345",
        dia_de_pago_loan_accounts="VIERNES",
        fecha_de_la_primer_reunion_loan="27/05/1992",
    )
    validations = ValidationsRules(loan=loan)

    response = validations.difference_of_days_in_day_meeting()

    assert response["data_response"][0]["message"] == (
        "La diferencia entre el día de pago y día de reunion,"
        " no puede ser mayor a 1 día. Del crédito: 12345"
    )
    assert not response["status"]

    loan = mambu.loans.build(
        id="12345",
        dia_de_pago_loan_accounts="prueba",
        fecha_de_la_primer_reunion_loan="29/05/1992",
    )
    validations = ValidationsRules(loan=loan)

    response = validations.difference_of_days_in_day_meeting()

    assert response["data_response"][0]["message"] == (
        "El día PRUEBA, no puede ser elegido como fecha de primer reunión"
    )
    assert not response["status"]


def test_gender(mambu, mocker):
    mocker.patch("setup.adapters.podemos_mambu.Clients._model_rest")

    client = mambu.clients.build(id="OYH804", first_name="Taylor", last_name="Swift")

    validations = ValidationsRules(clients=[client])

    response = validations.gender()

    assert response["data_response"][0]["message"] == (
        "La integrante: Taylor Swift (ID: OYH804) no "
        "tiene género asignado (Género Hombre o Mujer)\n"
    )
    assert not response["status"]

    client = mambu.clients.build(
        id="OYH804", first_name="Taylor", last_name="Swift", gender="FEMALE"
    )

    validations = ValidationsRules(clients=[client])

    response = validations.gender()

    assert response["data_response"] == []
    assert response["status"]


def test_experience(mambu, mocker):
    mocker.patch("setup.adapters.podemos_mambu.Clients._model_rest")

    client = mambu.clients.build(
        id="OYH804",
        first_name="Taylor",
        last_name="Swift",
        experiencia=0,
        birth_date=datetime.strptime("1992-05-27", "%Y-%m-%d"),
    )

    validations = ValidationsRules(clients=[client])

    response = validations.experience()

    assert response["data_response"] == []
    assert response["status"]

    client = mambu.clients.build(
        id="OYH804",
        first_name="Taylor",
        last_name="Swift",
        experiencia=100,
        birth_date=datetime.strptime("1992-05-27", "%Y-%m-%d"),
    )

    validations = ValidationsRules(clients=[client])

    response = validations.experience()

    assert (
        "Los años de experiencia (100) de Taylor Swift"
        in response["data_response"][0]["message"]
    )
    assert not response["status"]


@freeze_time("2022-05-27")
def test_age_range(mambu, mocker):
    mocker.patch("setup.adapters.podemos_mambu.Clients._model_rest")

    client = mambu.clients.build(
        id="OYH804",
        first_name="Taylor",
        last_name="Swift",
        birth_date=datetime.strptime("1992-05-27", "%Y-%m-%d"),
        loan_cycle=1,
        group_loan_cycle=0,
    )

    validations = ValidationsRules(clients=[client])

    response = validations.age_range()

    assert response["data_response"] == []
    assert response["status"]

    client = mambu.clients.build(
        id="OYH804",
        first_name="Taylor",
        last_name="Swift",
        birth_date=datetime.strptime("2022-05-27", "%Y-%m-%d"),
        loan_cycle=0,
        group_loan_cycle=0,
    )

    validations = ValidationsRules(clients=[client])

    response = validations.age_range()

    assert response["data_response"][0]["message"] == (
        "El rango de edad de la integrante Taylor Swift"
        " (ID: OYH804), tiene que estar: 18 - 72 años."
    )
    assert not response["status"]

    client = mambu.clients.build(
        id="OYH804",
        first_name="Taylor",
        last_name="Swift",
        birth_date=datetime.strptime("1900-05-27", "%Y-%m-%d"),
        loan_cycle=0,
        group_loan_cycle=0,
    )

    validations = ValidationsRules(clients=[client])

    response = validations.age_range()

    assert response["data_response"][0]["message"] == (
        "El rango de edad de la integrante Taylor Swift"
        " (ID: OYH804), tiene que estar: 18 - 72 años."
    )
    assert not response["status"]
