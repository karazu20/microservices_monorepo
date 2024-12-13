import json

import pytest

from setup import config as config_setup
from src.cdc import config


@pytest.fixture(scope="module")
def etapa_validations(validations_session):
    etapas = (
        "PENDIENTE DE APROBACION",
        "APROBADO",
        "DESEMBOLSO",
        "ACTIVO",
        "CONSULTA CDC",
    )

    for etapa_val in etapas:
        validations_session.execute(
            "INSERT INTO etapas (etapa) VALUES (:etapa)",
            dict(
                etapa=etapa_val,
            ),
        )
        validations_session.commit()


@pytest.fixture(scope="module")
def estatus_ejecucion_reglas(validations_session):
    estatus_reglas = ("ACTIVO", "INACTIVO")

    for estatus_regla in estatus_reglas:
        validations_session.execute(
            "INSERT INTO estatus_ejecucion_reglas (estatus) VALUES (:estatus)",
            dict(
                estatus=estatus_regla,
            ),
        )
        validations_session.commit()


@pytest.mark.usefixtures("postgres_db")
def test_create_stage(client, token_user):
    data = {
        "etapa": "APROBADO",
    }

    url = config.get_api_url()
    response = client.post(
        f"{url}/validations/stage",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )
    assert response.status_code == 201

    response = client.get(
        f"{url}/validations/stage", headers={config_setup.TOKEN_HEADER: token_user}
    )
    assert response.status_code == 200


@pytest.mark.usefixtures("postgres_db")
def test_create_rule(client, token_user):

    data = {
        "regla": "group_risk",
        "cantidad": 2,
    }

    url = config.get_api_url()
    response = client.post(
        f"{url}/validations/rule",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )
    assert response.status_code == 201

    response = client.get(
        f"{url}/validations/rule", headers={config_setup.TOKEN_HEADER: token_user}
    )
    assert response.status_code == 200


@pytest.mark.usefixtures("postgres_db")
def test_create_rule_execution_status(client, token_user):

    data = {
        "estatus": "ACTIVO",
    }

    url = config.get_api_url()
    response = client.post(
        f"{url}/validations/rule_execution_status",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )
    assert response.status_code == 201

    response = client.get(
        f"{url}/validations/rule_execution_status",
        headers={config_setup.TOKEN_HEADER: token_user},
    )
    assert response.status_code == 200


@pytest.mark.usefixtures("postgres_db")
def test_create_rule_exception_type(client, token_user):

    data = {
        "tipo": "CREDITO",
    }

    url = config.get_api_url()
    response = client.post(
        f"{url}/validations/rule_exception_type",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )
    assert response.status_code == 201

    response = client.get(
        f"{url}/validations/rule_exception_type",
        headers={config_setup.TOKEN_HEADER: token_user},
    )
    assert response.status_code == 200


@pytest.mark.usefixtures("postgres_db")
def test_create_rule_execution(client, token_user):

    data = {
        "etapa_id": 1,
        "regla_id": 1,
        "estatus_ejecucion_regla_id": 1,
    }

    url = config.get_api_url()
    response = client.post(
        f"{url}/validations/rule_execution",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )
    assert response.status_code == 201

    response = client.get(
        f"{url}/validations/rule_execution",
        headers={config_setup.TOKEN_HEADER: token_user},
    )
    assert response.status_code == 200

    response = client.get(
        f"{url}/validations/rule_execution?estatus=INACTIVO",
        headers={config_setup.TOKEN_HEADER: token_user},
    )
    assert response.status_code == 200
    assert not json.loads(response.data)

    response = client.get(
        f"{url}/validations/rule_execution?etapa=APROBADO",
        headers={config_setup.TOKEN_HEADER: token_user},
    )
    assert response.status_code == 200
    assert json.loads(response.data) == [
        {"id": 1, "regla": "group_risk", "estatus": "ACTIVO", "etapa": "APROBADO"}
    ]


@pytest.mark.usefixtures("postgres_db")
def test_create_rule_exception(client, token_user):

    data = {
        "regla_id": 1,
        "tipo_excepcion_regla_id": 1,
        "id_mambu": "58847",
    }

    url = config.get_api_url()
    response = client.post(
        f"{url}/validations/rule_exception",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )
    assert response.status_code == 201

    response = client.get(
        f"{url}/validations/rule_exception",
        headers={config_setup.TOKEN_HEADER: token_user},
    )
    assert response.status_code == 200

    response = client.get(
        f"{url}/validations/rule_exception?id_mambu=58847",
        headers={config_setup.TOKEN_HEADER: token_user},
    )
    assert response.status_code == 200
    assert json.loads(response.data) == [
        {
            "id": 1,
            "id_mambu": "58847",
            "regla": "group_risk",
            "tipo_excepcion": "CREDITO",
            "regla_id": 1,
        }
    ]


@pytest.mark.usefixtures("postgres_db")
def test_create_role(client, token_user):

    data = {
        "rol": "admin",
    }

    url = config.get_api_url()
    response = client.post(
        f"{url}/validations/role",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )
    assert response.status_code == 201

    response = client.get(
        f"{url}/validations/role", headers={config_setup.TOKEN_HEADER: token_user}
    )
    assert response.status_code == 200


@pytest.mark.usefixtures("postgres_db")
def test_create_role_rule(client, token_user):

    data = {
        "regla_id": 1,
        "rol_id": 1,
    }

    url = config.get_api_url()
    response = client.post(
        f"{url}/validations/role_rule",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )
    assert response.status_code == 201

    response = client.get(
        f"{url}/validations/role_rule", headers={config_setup.TOKEN_HEADER: token_user}
    )
    assert response.status_code == 200


@pytest.mark.usefixtures("postgres_db")
def test_validations_execute(client, mambu, token_user):

    group_fake = mambu.groups.build(
        id="ZX870", encoded_key="ZX87000", riesgo_grupo="BAJO"
    )
    mambu.groups.add(group_fake)
    loan_fake = mambu.loans.build(id="58847", account_holder=group_fake)
    mambu.loans.add(loan_fake)
    client_fake = mambu.clients.build(id="OYH804", group_keys=["ZX87000"])
    client_fake.groups = [group_fake]
    mambu.clients.add(client_fake)
    group_member_fake = mambu.group_members.build(client=client_fake)
    group_fake.group_members = [group_member_fake]

    url = config.get_api_url()
    data = {
        "regla": "group_risk",
    }

    client.post(
        f"{url}/validations/rule",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )
    data = {
        "etapa_id": 1,
        "regla_id": 2,
        "estatus_ejecucion_regla_id": 1,
    }

    client.post(
        f"{url}/validations/rule_execution",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )
    data = [
        {
            "id_mambu": "OYH804",
            "etapa": "APROBADO",
            "tipo": "INTEGRANTE",
        },
        {
            "id_mambu": "ZX870",
            "etapa": "DESEMBOLSO",
            "tipo": "GRUPO",
        },
        {
            "id_mambu": "58847",
            "etapa": "ACTIVO",
            "tipo": "CREDITO",
        },
    ]

    response = client.post(
        f"{url}/validations/execute_validations",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )
    assert response.status_code == 200

    assert (
        response.data
        == b'{"code": 200, "data": [{"id_mambu": "OYH804", "status": true, "messag'
        + b'es": []}, {"id_mambu": "ZX870", "status": true, "messages": []}, {"id_'
        + b'mambu": "58847", "status": false, "messages": [{"error": "Error al obt'
        + b'ener el ID en Mambu 58847"}]}], "msg": "Success"}\n'
    )


@pytest.mark.usefixtures("postgres_db")
def test_field_validation(client, token_user):

    data = {
        "regla_id": 1,
        "campo": "parentesco_referencia_2",
        "requerido": 1,
    }

    url = config.get_api_url()
    response = client.post(
        f"{url}/validations/field_validation",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )
    assert response.status_code == 201

    response = client.get(
        f"{url}/validations/field_validation",
        headers={config_setup.TOKEN_HEADER: token_user},
    )
    assert response.status_code == 200


@pytest.mark.usefixtures("postgres_db")
def test_create_custom_rule(
    client, token_user, etapa_validations, estatus_ejecucion_reglas
):
    data = {
        "regla_id": 1,
        "id_object_mambu": "123",
        "tipo": "CREDITO",
        "etapa_id": 2,
        "estatus_ejecucion_regla_id": 2,
    }

    url = config.get_api_url()
    response = client.post(
        f"{url}/validations/custom_rule_set",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )
    assert response.status_code == 201

    response = client.get(
        f"{url}/validations/custom_rule_set",
        headers={config_setup.TOKEN_HEADER: token_user},
    )
    assert response.status_code == 200


@pytest.mark.usefixtures("postgres_db")
def test_validations_custom_rules_execute(client, mambu, token_user):
    group_fake = mambu.groups.build(id="12345", riesgo_grupo="BAJO")
    mambu.groups.add(group_fake)
    loan_fake = mambu.loans.build(id="OYH804", account_holder=group_fake)
    mambu.loans.add(loan_fake)
    clien_fake = mambu.clients.build(
        id="HK307", groups=[group_fake], group_keys=[group_fake]
    )
    clien_fake.groups = [group_fake]
    mambu.clients.add(clien_fake)
    group_member_fake = mambu.group_members.build(client=clien_fake)
    group_fake.group_members = [group_member_fake]

    url = config.get_api_url()
    data = {
        "regla": "group_risk",
    }

    response = client.post(
        f"{url}/validations/rule",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )

    data = {
        "regla_id": 1,
        "id_object_mambu": "HK307",
        "tipo": "INTEGRANTE",
        "etapa_id": 1,
        "estatus_ejecucion_regla_id": 1,
    }

    client.post(
        f"{url}/validations/custom_rule_set",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )

    data = [
        {
            "id_mambu": "OYH804",
            "etapa": "DESEMBOLSO",
            "tipo": "CREDITO",
        },
        {
            "id_mambu": "HK307",
            "etapa": "APROBADO",
            "tipo": "INTEGRANTE",
        },
        {
            "id_mambu": "12345",
            "etapa": "ACTIVO",
            "tipo": "GRUPO",
        },
    ]

    response = client.post(
        f"{url}/validations/execute_validations",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )

    assert response.status_code == 200
    assert (
        response.data
        == b'{"code": 200, "data": [{"id_mambu": "OYH804", "status": false, '
        + b'"messages": [{"error": "Error al obtener el ID en Mambu OYH804"}'
        + b']}, {"id_mambu": "HK307", "status": true, "messages": []}, {"id_'
        + b'mambu": "12345", "status": true, "messages": []}], "msg": "Success"}\n'
    )

    data = [
        {
            "id_mambu": "OYH801",
            "etapa": "DESEMBOLSO",
            "tipo": "CREDITO",
        },
    ]

    response = client.post(
        f"{url}/validations/execute_validations",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )

    assert response.status_code == 200
    assert (
        response.data
        == b'{"code": 200, "data": [{"id_mambu": "OYH801", "status": false, "messages": '
        + b'[{"error": "Error al obtener el ID en Mambu OYH801"}]}], "msg": "Success"}\n'
    )


@pytest.mark.usefixtures("postgres_db")
def test_create_especified_rule(mocker, client, mambu, token_user):

    group_fake = mambu.groups.build(id="ZX870", riesgo_grupo="BAJO")
    mambu.groups.add(group_fake)
    clien_fake = mambu.clients.build(id="HK307")
    group_member_fake = mambu.group_members.build(client=clien_fake)
    group_fake.group_members = [group_member_fake]

    url = config.get_api_url()
    data = {
        "regla": "group_risk",
    }

    client.post(
        f"{url}/validations/rule",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )

    data = {
        "regla_id": 1,
        "id_object_mambu": "ZX870",
        "tipo": "GRUPO",
        "etapa_id": 1,
        "estatus_ejecucion_regla_id": 1,
    }
    response = client.post(
        f"{url}/validations/custom_rule_set",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )
    assert response.status_code == 201

    data = [
        {
            "id_mambu": "ZX870",
            "etapa": "APROBADO",
            "tipo": "GRUPO",
        },
    ]

    response = client.post(
        f"{url}/validations/execute_validations",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )
    assert response.data == (
        b'{"code": 200, "data": [{"id_mambu": "ZX870", "status": true'
        + b', "messages": []}], "msg": "Success"}\n'
    )

    mock_validations = mocker.patch(
        "src.validations.services_layer.handlers.ValidationsRules.group_risk"
    )
    mock_validations.return_value = {"status": False, "message": "prueba"}
    response = client.post(
        f"{url}/validations/execute_validations",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )
    assert response.data == (
        b'{"code": 200, "data": [{"id_mambu": "ZX870", "'
        + b'status": false, "messages": [{"error": "prueba"'
        + b'}]}], "msg": "Success"}\n'
    )


@pytest.mark.usefixtures("postgres_db")
def test_create_validation_data_identifier(client, token_user):

    data = {
        "identificador": "curp",
        "descripcion": "Prueba",
    }

    url = config.get_api_url()
    response = client.post(
        f"{url}/validations/validation_data_identifier",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )
    assert response.status_code == 201


@pytest.mark.usefixtures("postgres_db")
def test_create_validation_data(client, token_user):

    data = {
        "identificador_dato_validacion_id": 1,
        "valor": "TXTO",
        "llave": "prueba_key",
        "tipo_dato": "str",
    }

    url = config.get_api_url()
    response = client.post(
        f"{url}/validations/validation_data",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )
    assert response.status_code == 201


@pytest.mark.usefixtures("postgres_db")
def test_create_validation_rule_data(client, token_user):

    data = {
        "identificador_dato_validacion_id": 1,
        "regla_id": 1,
    }

    url = config.get_api_url()
    response = client.post(
        f"{url}/validations/validation_rule_data",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )
    assert response.status_code == 201


@pytest.mark.usefixtures("postgres_db")
def test_validations_execute_cdc(client, mambu, token_user):
    client_fake = mambu.clients.build(
        id="ABCD",
        last_name="ALGO",
        first_name="TESTO",
        middle_name="PODEMOS",
        state="",
        birth_date="1992-11-15",
        id_documents=[{"IDDocuments": "ABCD123456QWERTY4321"}],
    )
    mambu.clients.add(client_fake)
    url = config.get_api_url()
    data = {"regla": "black_list_client", "cantidad": 0}

    client.post(
        f"{url}/validations/rule",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )
    client.get(f"{url}/validations/rule", headers={config_setup.TOKEN_HEADER: token_user})
    data = {
        "etapa_id": 2,
        "regla_id": 2,
        "estatus_ejecucion_regla_id": 1,
    }
    client.post(
        f"{url}/validations/rule_execution",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )
    data = {
        "etapa": "CONSULTA CDC",
    }

    response = client.post(
        f"{url}/validations/stage",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )
    data = {
        "curp": "ABCD123456QWERTY4321",
        "first_name": "ALGO",
        "last_name": "TESTO",
        "middle_name": "PODEMOS",
        "birth_date": "1992-11-15",
        "numero": "5512345678",
    }
    response = client.post(
        f"{url}/validations/execute_validations_cdc",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )
    assert response.status_code == 200
