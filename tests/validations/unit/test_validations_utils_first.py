from datetime import datetime

from src.validations.utils.validations_rules import ValidationsRules


class CustomFieldsFake(object):
    """Class Fake CustomFields"""

    def __init__(self, id, value=None, name=None):
        self.id = id
        self.value = value
        self.name = name


class FieldValidationsFake(object):
    """Class Fake FieldValidation"""

    def __init__(self, id, regla_id, campo, requerido):
        self.id = id
        self.regla_id = regla_id
        self.campo = campo
        self.requerido = requerido


def test_group_risk(mambu):
    group = mambu.groups.build(id="123")
    group.riesgo_grupo = "Bajo"

    validations = ValidationsRules(
        clients=None,
        group=group,
        loan=None,
    )

    response = validations.group_risk()
    assert response["status"]
    assert response["data_response"] == []

    group.riesgo_grupo = "Alto"
    validations = ValidationsRules(
        clients=None,
        group=group,
        loan=None,
    )
    response = validations.group_risk()
    assert not response["status"]
    assert response["data_response"][0]["message"] == "El grupo tiene riesgo Alto"


def test_len_custom_fields_groups(mambu):
    group = mambu.groups.build(id="123", ciclo_tipo_groups="C8 - CIMI")
    validations = ValidationsRules(
        clients=[None],
        group=group,
        loan=None,
        field_validations=[
            FieldValidationsFake(
                id=1, regla_id=1, campo="ciclo_tipo_groups", requerido=False
            )
        ],
    )

    response = validations.len_custom_fields_groups()
    assert response["status"]
    assert response["message"] == ""
    group = mambu.groups.build(id="123", ciclo_tipo_groups=None)
    validations = ValidationsRules(
        clients=[None],
        group=group,
        loan=None,
        field_validations=[
            FieldValidationsFake(id=1, regla_id=1, campo="prueba", requerido=True),
        ],
    )
    response = validations.len_custom_fields_groups()
    assert not response["status"]
    assert response["message"] == "Campos faltantes ID: 123 prueba\n"
    group = mambu.groups.build(id="123", ciclo_tipo_groups=None)
    validations = ValidationsRules(
        clients=[None],
        group=group,
        loan=None,
        field_validations=[
            FieldValidationsFake(
                id=1, regla_id=1, campo="ciclo_tipo_groups", requerido=True
            ),
        ],
    )

    response = validations.len_custom_fields_groups()
    assert not response["status"]
    assert response["message"] == "Campos faltantes ID: 123 ciclo_tipo_groups\n"


def test_len_custom_fields_client(mambu):
    client = mambu.clients.build(id="OYH804", datosdomicilioactual_integrante="Prueba")
    validations = ValidationsRules(
        clients=[client],
        group=None,
        loan=None,
        field_validations=[
            FieldValidationsFake(
                id=1, regla_id=1, campo="datosdomicilioactual_integrante", requerido=False
            ),
        ],
    )

    response = validations.len_custom_fields_client()
    assert response["status"]
    assert response["message"] == ""

    client = mambu.clients.build(id="OYH804", datosdomicilioactual_integrante=None)
    validations = ValidationsRules(
        clients=[client],
        group=None,
        loan=None,
        field_validations=[
            FieldValidationsFake(id=1, regla_id=1, campo="prueba", requerido=True),
        ],
    )

    response = validations.len_custom_fields_client()
    assert not response["status"]
    assert response["message"] == "\nCampos faltantes ID: OYH804 prueba\n"


def test_len_custom_fields_loan(mambu):

    loan = mambu.loans.build(id="12345", assigned_centre="PRUEBA")
    validations = ValidationsRules(
        clients=None,
        group=None,
        loan=loan,
        field_validations=[
            FieldValidationsFake(id=1, regla_id=1, campo="prueba", requerido=False),
        ],
    )

    response = validations.len_custom_fields_loans()
    assert not response["status"]
    assert response["message"] == "Campos faltantes ID: 12345 prueba\n"

    validations = ValidationsRules(
        clients=None,
        group=None,
        loan=loan,
        field_validations=[
            FieldValidationsFake(
                id=1, regla_id=1, campo="assigned_centre", requerido=True
            ),
        ],
    )

    response = validations.len_custom_fields_loans()
    assert response["status"]
    assert response["message"] == ""


def test_custom_field_empty_group(mambu):
    validations = ValidationsRules(
        clients=None,
        group=None,
        loan=None,
        field_validations=None,
    )

    response = validations.custom_field_empty_group()

    assert response["status"]
    assert response["message"] == ""

    group = mambu.groups.build(id="123")
    validations = ValidationsRules(
        clients=None,
        group=group,
        loan=None,
        field_validations=[
            FieldValidationsFake(
                id=1, regla_id=1, campo="ciclo_tipo_groups", requerido=True
            ),
        ],
    )

    response = validations.custom_field_empty_group()

    assert not response["status"]
    assert response["message"] == " El campo está vacío: ciclo_tipo_groups\n"


def test_custom_field_empty_loan(mambu):
    validations = ValidationsRules(
        clients=None,
        group=None,
        loan=None,
        field_validations=None,
    )

    response = validations.custom_field_empty_loan()

    assert response["status"]
    assert response["message"] == ""

    loan = mambu.loans.build(
        id="12345",
        loan_name="Interes Mixto",
    )
    validations = ValidationsRules(
        clients=None,
        group=None,
        loan=loan,
        field_validations=[
            FieldValidationsFake(id=1, regla_id=1, campo="loan_name", requerido=True),
        ],
    )

    response = validations.custom_field_empty_loan()
    assert response["status"]
    assert response["message"] == ""

    loan = mambu.loans.build(id="12345", loan_name="Interes Mixto")

    validations = ValidationsRules(
        clients=None,
        group=None,
        loan=loan,
        field_validations=[
            FieldValidationsFake(id=1, regla_id=1, campo="parentesco", requerido=True),
        ],
    )

    response = validations.custom_field_empty_loan()
    assert not response["status"]
    assert response["message"] == " Campo Faltante: parentesco\n"


def test_custom_field_empty_client(mambu):

    validations = ValidationsRules(
        clients=None,
        group=None,
        loan=None,
        field_validations=None,
    )

    response = validations.custom_field_empty_client()

    assert response["status"]
    assert response["message"] == ""

    client = mambu.clients.build(estado_civil_clients_old="Libre")
    validations = ValidationsRules(
        clients=[client],
        group=None,
        loan=None,
        field_validations=[
            FieldValidationsFake(
                id=1, regla_id=1, campo="estado_civil_clients_old", requerido=True
            ),
        ],
    )

    response = validations.custom_field_empty_client()
    assert response["status"]
    assert response["message"] == ""

    client = mambu.clients.build(id="OYH804", estado_civil_clients_old=None)
    validations = ValidationsRules(
        clients=[client],
        group=None,
        loan=None,
        field_validations=[
            FieldValidationsFake(
                id=1, regla_id=1, campo="estado_civil_clients_old", requerido=True
            ),
        ],
    )

    response = validations.custom_field_empty_client()
    assert not response["status"]
    assert response["message"] == "\n El campo está vacío: estado_civil_clients_old\n"

    validations = ValidationsRules(
        clients=[client],
        group=None,
        loan=None,
        field_validations=[
            FieldValidationsFake(id=1, regla_id=1, campo="parentesco", requerido=True),
        ],
    )

    response = validations.custom_field_empty_client()
    assert not response["status"]
    assert response["message"] == "\n Campo Faltante: parentesco\n"


def test_group_roles(mambu):
    role = mambu.group_roles.build(role_name="X")
    group_member = mambu.group_members.build(roles=[role])
    group = mambu.groups.build(id="123", group_members=[group_member])

    validations = ValidationsRules(
        clients=None,
        group=group,
        loan=None,
    )
    response = validations.group_roles()

    assert not response["status"]
    assert (
        response["data_response"][0]["message"]
        == "El grupo: 123 no tiene el ROL de ['LIDER', 'TESORERA']"
    )

    role = mambu.group_roles.build(role_name="TESORERA")
    group_member_tesorera = mambu.group_members.build(roles=[role])
    group = mambu.groups.build(id="123", group_members=[group_member_tesorera])
    validations = ValidationsRules(clients=None, group=group, loan=None, quantity=2)

    response = validations.group_roles()
    assert not response["status"]
    assert (
        response["data_response"][0]["message"]
        == "El grupo: 123 no tiene el ROL de ['LIDER']"
    )

    role = mambu.group_roles.build(role_name="LIDER")
    group_member_lider = mambu.group_members.build(roles=[role])
    group = mambu.groups.build(id="123", group_members=[group_member_lider])
    validations = ValidationsRules(
        clients=None,
        group=group,
        loan=None,
        quantity=1,
    )
    response = validations.group_roles()

    assert not response["status"]
    assert (
        response["data_response"][0]["message"]
        == "El grupo: 123 no tiene el ROL de ['TESORERA']"
    )

    group = mambu.groups.build(
        id="123",
        group_members=[
            group_member_lider,
            group_member_tesorera,
        ],
    )
    validations = ValidationsRules(
        clients=None,
        group=group,
        loan=None,
        quantity=1,
    )
    response = validations.group_roles()

    assert response["status"]
    assert response["data_response"] == []


def test_branch_client(mambu):

    validations = ValidationsRules(
        clients=None,
        group=None,
        loan=None,
        field_validations=None,
    )

    response = validations.branch_client()

    assert response["status"]
    assert response["data_response"] == []

    client = mambu.clients.build(id="OYH804")
    validations = ValidationsRules(clients=[client], group=None, loan=None)

    response = validations.branch_client()

    assert not response["status"]
    assert response["data_response"] == [
        {
            "message": "La integrante: OYH804 no tiene ningún centro comunitario asignado",
            "field": "assigned_branch_key",
            "client_id": "OYH804",
        }
    ]

    client = mambu.clients.build(id="OYH804", assigned_branch_key="123456")
    validations = ValidationsRules(
        clients=[client],
        group=None,
        loan=None,
    )

    response = validations.branch_client()

    assert response["status"]
    assert response["data_response"] == []


def test_no_user_assignment_ce(mambu):

    validations = ValidationsRules(
        clients=None,
        group=None,
        loan=None,
        field_validations=None,
    )

    response = validations.no_user_assignment_ce()

    assert response["status"]
    assert response["data_response"] == []

    client = mambu.clients.build(id="OYH804")
    validations = ValidationsRules(clients=[client], group=None, loan=None)

    response = validations.no_user_assignment_ce()
    assert response["status"]
    assert response["data_response"] == []

    client = mambu.clients.build(id="OYH804", assigned_user_key="123456")
    validations = ValidationsRules(
        clients=[client],
        group=None,
        loan=None,
    )

    response = validations.no_user_assignment_ce()

    assert not response["status"]
    assert (
        response["data_response"][0]["message"]
        == "La integrante: OYH804 no debe tener coordinador asignado"
    )


def test_date_birth_client(mambu):

    validations = ValidationsRules(
        clients=None,
        group=None,
        loan=None,
    )

    response = validations.date_birth_client()

    assert response["status"]
    assert response["data_response"] == []

    client = mambu.clients.build(id="OYH804", birth_date=datetime(1992, 5, 27))
    validations = ValidationsRules(
        clients=[client],
        group=None,
        loan=None,
    )

    response = validations.date_birth_client()

    assert response["status"]
    assert response["data_response"] == []

    client = mambu.clients.build(id="OYH804")

    validations = ValidationsRules(
        clients=[client],
        group=None,
        loan=None,
    )

    response = validations.date_birth_client()

    assert not response["status"]
    assert (
        response["data_response"][0]["message"]
        == "Falta fecha de cumpleaños en el cliente: OYH804"
    )

    client = mambu.clients.build(id="OYH804", birth_date="prueba")
    validations = ValidationsRules(
        clients=[client],
        group=None,
        loan=None,
    )

    response = validations.date_birth_client()

    assert not response["status"]
    assert (
        response["data_response"][0]["message"]
        == "Falta fecha de cumpleaños en el cliente: OYH804"
    )


def test_client_telephone(mambu):

    validations = ValidationsRules(
        clients=None,
        group=None,
        loan=None,
    )

    response = validations.client_telephone()

    assert response["status"]
    assert response["data_response"] == []

    client = mambu.clients.build(id="OYH804", home_phone="prueba")
    validations = ValidationsRules(
        clients=[client],
        group=None,
        loan=None,
        quantity=11,
    )

    response = validations.client_telephone()

    assert not response["status"]
    assert (
        response["data_response"][0]["message"]
        == "El teléfono de domicilio del cliente: OYH804 deben ser dígitos"
    )

    client = mambu.clients.build(id="OYH804", home_phone="5555554")
    validations = ValidationsRules(
        clients=[client],
        group=None,
        loan=None,
        quantity=11,
    )

    response = validations.client_telephone()

    assert not response["status"]
    assert (
        response["data_response"][0]["message"]
        == "El teléfono de domicilio del cliente: OYH804 debe contener al menos 11 dígitos"
    )


def test_client_without_telephone(mambu):

    client = mambu.clients.build(id="OYH804")

    validations = ValidationsRules(
        clients=[client],
        group=None,
        loan=None,
        quantity=11,
    )

    response = validations.client_telephone()

    assert response["status"]
    assert response["data_response"] == []


def test_validate_curp_client(mambu):
    id_document = mambu.id_documents.build(document_id="EN ESPERA", document_type="CURP")
    client = mambu.clients.build(
        id="OYH804",
        id_documents=[id_document],
    )
    validations = ValidationsRules(
        clients=[client],
        group=None,
        loan=None,
        field_validations=[
            FieldValidationsFake(id=1, regla_id=1, campo="EN ESPERA", requerido=True),
        ],
    )

    response = validations.validate_curp_client()

    assert response["status"]
    assert response["data_response"] == []

    id_document = mambu.id_documents.build(
        document_id="EN TOGM920527HDFRNR06", document_type="CURP"
    )
    client = mambu.clients.build(
        id="OYH804",
        id_documents=[id_document],
    )
    validations = ValidationsRules(
        clients=[client],
        group=None,
        loan=None,
        field_validations=[
            FieldValidationsFake(id=1, regla_id=1, campo="EN ESPERA", requerido=True),
        ],
    )

    response = validations.validate_curp_client()
    assert response["status"]
    assert response["data_response"] == []

    id_document = mambu.id_documents.build(
        document_id="TOGM920527HDFRNR06", document_type="PRUEBA"
    )
    client = mambu.clients.build(
        id="OYH804",
        id_documents=[id_document],
    )
    validations = ValidationsRules(
        clients=[client],
        group=None,
        loan=None,
        field_validations=[
            FieldValidationsFake(id=1, regla_id=1, campo="EN ESPERA", requerido=True),
        ],
    )

    response = validations.validate_curp_client()
    assert not response["status"]
    assert (
        response["data_response"][0]["message"]
        == "La integrante OYH804 no tiene CURP registrado"
    )
    assert response["data_response"][0]["field"] == "curp"


def test_validate_rfc(mambu):
    client = mambu.clients.build(id="OYH804")
    validations = ValidationsRules(
        clients=[client],
        group=None,
        loan=None,
    )

    response = validations.validate_rfc()

    assert not response["status"]
    assert (
        response["data_response"][0]["message"]
        == "La integrante OYH804 no tiene CURP registrado"
    )
    assert response["data_response"][0]["field"] == "curp"

    id_document = mambu.id_documents.build(
        document_id="TOGM920527HDFRNR06", document_type="CURP"
    )
    client = mambu.clients.build(
        id="OYH804",
        id_documents=[id_document],
    )
    validations = ValidationsRules(
        clients=[client],
        group=None,
        loan=None,
    )

    response = validations.validate_rfc()
    assert not response["status"]
    assert (
        response["data_response"][0]["message"]
        == "El RFC de la integrante OYH804 esta vacío"
    )
    assert response["data_response"][0]["field"] == "rfc"

    client = mambu.clients.build(
        id="OYH804",
        id_documents=[id_document],
        rfc="",
    )
    validations = ValidationsRules(
        clients=[client],
        group=None,
        loan=None,
    )
    response = validations.validate_rfc()
    assert not response["status"]
    assert (
        response["data_response"][0]["message"]
        == "El RFC de la integrante OYH804 esta vacío"
    )
    assert response["data_response"][0]["field"] == "rfc"

    client = mambu.clients.build(
        id="OYH804",
        id_documents=[id_document],
        rfc="TOGM920527",
    )

    validations = ValidationsRules(
        clients=[client],
        group=None,
        loan=None,
    )
    response = validations.validate_rfc()
    assert response["status"]
    assert response["data_response"] == []

    client = mambu.clients.build(
        id="OYH804",
        id_documents=[id_document],
        rfc="9578920527",
    )
    validations = ValidationsRules(
        clients=[client],
        group=None,
        loan=None,
    )
    response = validations.validate_rfc()

    assert not response["status"]
    assert (
        response["data_response"][0]["message"]
        == "El formato del RFC de la integrante: OYH804 es incorrecto"
    )
    assert response["data_response"][0]["field"] == "rfc"

    id_document = mambu.id_documents.build(document_id="EN ESPERA", document_type="CURP")
    client = mambu.clients.build(
        id="OYH804",
        id_documents=[id_document],
        rfc="TOGM920527",
    )

    validations = ValidationsRules(
        clients=[client],
        group=None,
        loan=None,
    )
    response = validations.validate_rfc()
    assert not response["status"]
    assert (
        response["data_response"][0]["message"]
        == "El RFC de la integrante: OYH804 es incorrecto"
    )
    assert response["data_response"][0]["field"] == "rfc"

    client = mambu.clients.build(
        id="OYH804",
        id_documents=[id_document],
        rfc="TOGM920527",
    )

    validations = ValidationsRules(
        clients=[client],
        group=None,
        loan=None,
        field_validations=[
            FieldValidationsFake(id=1, regla_id=1, campo="EN ESPERA", requerido=True),
        ],
    )
    response = validations.validate_rfc()
    assert response["status"]
    assert response["data_response"] == []


def test_client_email(mambu):
    validations = ValidationsRules(
        clients=None,
        group=None,
        loan=None,
    )

    response = validations.client_email()

    assert response["status"]
    assert response["data_response"] == []

    client = mambu.clients.build(id="OYH804")
    validations = ValidationsRules(
        clients=[client],
        group=None,
        loan=None,
    )

    response = validations.client_email()

    assert response["status"]
    assert response["data_response"] == []

    client = mambu.clients.build(id="OYH804", email_address="1")
    validations = ValidationsRules(
        clients=[client],
        group=None,
        loan=None,
        field_validations=[
            FieldValidationsFake(id=1, regla_id=1, campo="prueba", requerido=False)
        ],
    )

    response = validations.client_email()

    assert not response["status"]
    assert (
        response["data_response"][0]["message"]
        == "El email de la integrante: OYH804 tiene formato incorrecto"
    )
    assert response["data_response"][0]["field"] == "email_address"

    client = mambu.clients.build(id="OYH804", email_address="corre@correo.com")
    validations = ValidationsRules(
        clients=[client],
        group=None,
        loan=None,
        field_validations=[
            FieldValidationsFake(id=1, regla_id=1, campo="prueba", requerido=False)
        ],
    )

    response = validations.client_email()

    assert response["status"]
    assert response["data_response"] == []


def test_minimum_number_of_members_loan(mambu, mocker):
    mocker.patch("setup.adapters.podemos_mambu.Loans._model_rest")
    mock_search = mocker.patch("setup.adapters.podemos_mambu.Loans.search")
    loan = mambu.loans.build(id="12345")
    group = mambu.groups.build(id="123")

    mock_search.return_value = []
    client = mambu.clients.build(id="12345")
    validations = ValidationsRules(
        clients=[client],
        group=group,
        loan=loan,
        quantity=2,
    )

    response = validations.minimum_number_of_members_loan()

    assert not response["status"]
    assert (
        response["data_response"][0]["message"]
        == "El crédito: 12345 no cuenta con el mínimo número de miembros que es: 2\n"
    )

    validations = ValidationsRules(
        clients=[client],
        group=group,
        loan=loan,
        quantity=1,
    )

    response = validations.minimum_number_of_members_loan()

    assert response["status"]
    assert response["data_response"] == []


def test_validate_address_clients(mambu):

    validations = ValidationsRules(
        clients=None,
        group=None,
        loan=None,
    )

    response = validations.validate_address_clients()

    assert response["status"]
    assert response["data_response"] == []
    adress = mambu.addresses.build(
        city="ATIZAPAN",
        region="MEXICO",
        line_1="INSURGENTES SUR 1235",
        line_2="INSURGENTES",
    )
    client = mambu.clients.build(
        id="OYH804",
        addresses=[adress],
    )
    validations = ValidationsRules(
        clients=[client],
        group=None,
        loan=None,
    )

    response = validations.validate_address_clients()
    assert response["status"]
    assert response["data_response"] == []

    client = mambu.clients.build(id="OYH804", addresses=[])
    validations = ValidationsRules(
        clients=[client],
        group=None,
        loan=None,
    )

    response = validations.validate_address_clients()
    assert not response["status"]
    assert (
        response["data_response"][0]["message"]
        == "La integrante OYH804 no tiene dirección"
    )
    assert response["data_response"][0]["field"] == "address"


def test_family_home_restrictions_loan(mambu):

    loan = mambu.loans.build(id="12345")
    validations = ValidationsRules(
        clients=None,
        group=None,
        loan=loan,
    )

    response = validations.family_home_restrictions_loan()

    assert not response["status"]
    assert (
        response["data_response"][0]["message"]
        == "El crédito: 12345 no cumple las restricciones de familia, domicilio y/o distancia"
    )

    loan.restricciones_fam_dom_dist = True
    validations = ValidationsRules(
        clients=None,
        group=None,
        loan=loan,
    )

    response = validations.family_home_restrictions_loan()

    assert response["status"]
    assert response["data_response"] == []


def test_cycle_group_type(mambu):

    group = mambu.groups.build(id="123", ciclo_tipo_groups="C8 - CIMI")
    product = mambu.products.build(name="Credito Adicional")
    loan = mambu.loans.build(id="12345", ciclo=8, product_type=product)
    validations = ValidationsRules(
        clients=None,
        group=group,
        loan=loan,
    )

    response = validations.cycle_group_type()
    assert response["status"]
    assert response["data_response"] == []

    group = mambu.groups.build(id="123", ciclo_tipo_groups="PRUEBA")
    product = mambu.products.build(name="Credito Adicional")
    loan = mambu.loans.build(id="12345", product_type=product)
    validations = ValidationsRules(
        clients=None,
        group=group,
        loan=loan,
    )

    response = validations.cycle_group_type()
    assert not response["status"]
    assert (
        response["data_response"][0]["message"]
        == "El campo Ciclo-Tipo es incorrecto en el grupo: 123"
    )
    assert response["data_response"][0]["field"] == "ciclo_tipo_groups"


def test_cycle_group_type_without_cycle(mambu):
    product = mambu.products.build(name="Credito Adicional")
    loan = mambu.loans.build(id="12345", ciclo=7, product_type=product)
    group = mambu.groups.build(id="123", ciclo_tipo_groups="C8 - CIMI", loan_cycle=7)
    validations = ValidationsRules(
        clients=None,
        group=group,
        loan=loan,
    )

    response = validations.cycle_group_type()

    assert not response["status"]
    assert (
        response["data_response"][0]["message"]
        == "El número de ciclo no coincide con la información Ciclo-Tipo del grupo. Ciclo-Tipo: 8. Ciclo del grupo: 7"
    )
    assert response["data_response"][0]["field"] == "ciclo_tipo_groups"


def test_cycle_group_type_not_recognized_information(mambu):
    product = mambu.products.build(name="Prueba")
    group = mambu.groups.build(id="123", ciclo_tipo_groups="C3 - CIMI")
    loan = mambu.loans.build(id="12345", ciclo=3, product_type=product)
    validations = ValidationsRules(
        clients=None,
        group=group,
        loan=loan,
    )

    response = validations.cycle_group_type()

    assert not response["status"]
    assert (
        response["data_response"][0]["message"]
        == "El tipo de crédito no coincide con la informacion del Ciclo-Tipo del grupo 123 Producto: Prueba"
    )
    assert response["data_response"][0]["field"] == "ciclo_tipo_groups"

    product = mambu.products.build(name="Credito Adicional")
    loan = mambu.loans.build(id="12345", product_type=product, ciclo=3)
    validations = ValidationsRules(
        clients=None,
        group=group,
        loan=loan,
    )

    response = validations.cycle_group_type()

    assert response["status"]
    assert response["data_response"] == []


def test_black_list_client(mambu):

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


def test_client_risk(mambu):

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
