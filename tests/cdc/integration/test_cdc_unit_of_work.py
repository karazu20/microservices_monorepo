from datetime import datetime

import pytest

from shared.cdc_utils import CDCResponse
from src.cdc import config
from src.cdc.domain.models import DireccionProspecto, Prospecto
from src.cdc.services_layer import unit_of_work
from tests.cdc.utils import XML_TEST_EVALUATIONS_RULES


def prospecto_test():
    credit_response = CDCResponse.from_response(
        XML_TEST_EVALUATIONS_RULES, config.CLAVES_PERMITIDAS
    )
    prospecto = Prospecto(
        "MAVK030710MDFRRRA3",
        "KARLA",
        "RUBY",
        "MARQUEZ",
        "VERA",
        datetime(2003, 7, 10),
        "MX",
        "1111111111",
    )
    prospecto.set_consulta_data(credit_response)
    direccion_cero = DireccionProspecto(
        "Diagonal 2",
        "#16",
        "",
        "San Fernando",
        "Huixquilucan de Degollado",
        "Mexico",
        "Mexico",
        "52765",
    )
    prospecto.add_direccion(direccion_cero)

    return prospecto


@pytest.mark.usefixtures("postgres_db")
def test_unit_of_work():
    uow = unit_of_work.UnitOfWorkCdc()  # type: ignore
    session = uow.session_factory()  # type: ignore
    prospecto = prospecto_test()

    with uow:
        uow.prospecto.add_prospecto(prospecto)
        uow.commit()

    with uow:
        session = uow.session_factory()  # type: ignore

        [[name]] = session.execute(
            "SELECT first_name FROM cliente WHERE curp='MAVK030710MDFRRRA3'"
        )

        prospecto_db = uow.prospecto.get_prospecto("MAVK030710MDFRRRA3")
        curp = prospecto_db.curp
        nacionalidad = prospecto_db.nacionalidad

    assert name == "KARLA"
    assert curp == "MAVK030710MDFRRRA3"
    assert nacionalidad == "MX"
