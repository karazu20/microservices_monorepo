import os
from datetime import datetime
from unittest import mock

import pytest
from flask import g

from fakes.adapters import FakeBus, FakeCache, FakeUnitOfWork
from setup import inject, sessions
from src.cdc.domain.commands import ADDPerson
from src.cdc.domain.queries import GetPerson
from src.cdc.services_layer import handlers
from tests.cdc.utils import XML_TEST_ACCOUNTS


@pytest.fixture
def broker():
    broker = inject.start_broker(
        handlers=handlers,
        orm=None,
        uow=FakeUnitOfWork(),
        bus=FakeBus(),
        cache=FakeCache(),
    )
    yield broker


@mock.patch.dict(os.environ, {"CDC_EMAIL_ACTIVE": "ON"})
def test_broker_persona(mocker, broker, mambu):
    mock_cdc_service = mocker.patch("src.cdc.services_layer.handlers.CDCService.consult")
    mock_cdc_service.return_value = XML_TEST_ACCOUNTS

    mock_template = mocker.patch("pdfkit.from_string")
    mock_template.return_value = True

    g.user = sessions.User("user.fake", "user.fake@fakedomain.com")

    branch = mambu.branches.build(id="12345", name="Branch1")
    fake_user = mambu.users.build(
        id="12345",
        username="user.fake",
        tribus_usuario=[{"UnidadesCoordinador": "TribuNR-2", "_index": 0}],
        id_empleado="12345",
        assigned_branch=branch,
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
    persona = ADDPerson(
        nombre="Nombre Prueba",
        apellido_paterno="Paterno",
        apellido_materno="Materno",
        fecha_nacimiento="1992-05-27",
        curp="TOGM920527HDFRNR06",
        rfc="TOGM920527HDFRNR06",
        nacionalidad=None,
        direccion="2A CDA HUEXOTITLA",
        colonia="SAN PEDRO MARTIR",
        delegacion="TLALPAN",
        ciudad="CDMX",
        estado="CDMX",
        codigo_postal="14640",
        es_referida=False,
        timestamp_aprobacion_tyc=datetime.now(),
        timestamp_aprobacion_consulta=datetime.now(),
        nip="12345",
    )
    broker.handle(persona)
    get_persons = GetPerson()
    personas = broker.handle(get_persons)

    assert len(personas) == 1
