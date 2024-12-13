import json
import os
from datetime import datetime
from unittest import mock

import pytest
from flask import g

from setup import config as config_setup
from setup import sessions
from src.cdc import config
from tests.cdc.utils import XML_TEST_ACCOUNTS, XML_TEST_ERROR, XML_TEST_NO_ACCOUNTS


@pytest.fixture(scope="module")
def status_consulta_cdc(digitalization_session):
    status_consulta = "status"

    for i in range(1, 4):
        digitalization_session.execute(
            "INSERT INTO status_consulta_cdc (status, id_status) VALUES (:status, :id_status)",
            dict(
                status=f"{status_consulta}_{i}",
                id_status=i,
            ),
        )
        digitalization_session.commit()


@mock.patch.dict(os.environ, {"CDC_EMAIL_ACTIVE": "ON"})
@pytest.mark.usefixtures("postgres_db")
def test_create_person(mocker, client, mambu, token_user, status_consulta_cdc):
    g.user = sessions.User("user.fake", "user.fake@fakedomain.com")

    mock_template = mocker.patch("pdfkit.from_string")
    mock_template.return_value = True

    mock_cdc_service = mocker.patch("src.cdc.services_layer.handlers.CDCService.consult")
    mock_cdc_service.return_value = XML_TEST_ACCOUNTS

    branch = mambu.branches.build(id="12345", name="Branch1")
    fake_user = mambu.users.build(
        id="12345",
        username="user.fake",
        tribus_usuario=[{"UnidadesCoordinador": "TribuNR-2", "_index": 0}],
        id_empleado="12345",
        assigned_branch=branch,
        unidades_coordinador_0="TribuNR-2",
    )
    mambu.users.add(fake_user)
    fake_consejero = mambu.users.build(
        id="23456",
        username="consejero.fake",
        email="consejero.fake@fakedomain.com",
        id_empleado="23456",
    )
    fake_centre = mambu.centres.build(
        id="TribuNR-2",
        consejero=fake_consejero,
    )
    mambu.centres.add(fake_centre)

    data = {
        "nombre": "JUAN",
        "apellido_paterno": "PRUEBA",
        "apellido_materno": "SIETE",
        "fecha_nacimiento": "1980-01-07",
        "curp": "SIPJ800107MDFNBN03",
        "rfc": "SIPJ800107",
        "nacionalidad": "MX",
        "direccion": "INSURGENTES SUR 1007",
        "colonia": "INSURGENTES",
        "delegacion": "BENITO JUAREZ",
        "ciudad": "BENITO JUAREZ",
        "estado": "CDMX",
        "codigo_postal": "11230",
        "es_referida": False,
        "timestamp_aprobacion_tyc": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "timestamp_aprobacion_consulta": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    url = config.get_api_url()
    response = client.post(
        f"{url}/cdc/consultaCDC",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )
    assert response.status_code == 201

    mock_cdc_service.return_value = XML_TEST_NO_ACCOUNTS

    url = config.get_api_url()
    response = client.post(
        f"{url}/cdc/consultaCDC",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )
    assert response.status_code == 201

    mock_cdc_service.return_value = XML_TEST_ERROR

    url = config.get_api_url()
    response = client.post(
        f"{url}/cdc/consultaCDC",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )
    assert response.status_code == 400

    empty_data = {}
    response = client.get(
        f"{url}/cdc/person",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=empty_data,
    )
    assert response.status_code == 200

    mambu.clear()

    fake_user2 = mambu.users.build(
        id="12345",
        username="user.fake",
        tribus_usuario=None,
        id_empleado="12345",
        unidades_coordinador_0=None,
    )
    mambu.users.add(fake_user2)

    mock_cdc_service.return_value = XML_TEST_ACCOUNTS
    response = client.post(
        f"{url}/cdc/consultaCDC",
        headers={config_setup.TOKEN_HEADER: token_user},
        json=data,
    )
    assert response.status_code == 201
    mock_cdc_service.return_value = None


@pytest.mark.usefixtures("postgres_db")
def test_consult_list(mocker, client, token_user):

    url = config.get_api_url()
    response = client.get(
        f"{url}/cdc/consult_list", headers={config_setup.TOKEN_HEADER: token_user}
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert len(response_data["data"]["consultas"]) == 4
