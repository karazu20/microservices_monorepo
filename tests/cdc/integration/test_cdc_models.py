from datetime import datetime

import pytest
from dateutil.relativedelta import relativedelta

from shared.cdc_utils import CDCResponse
from src.cdc import config
from src.cdc.domain.models import (
    CentroComunitario,
    ConsultaCdc,
    DireccionProspecto,
    Nip,
    Prospecto,
    StatusConsultaCdC,
    Usuario,
)
from src.cdc.errors import CdcDomainError
from tests.cdc.utils import XML_TEST_EVALUATIONS_RULES


def prospecto_test():
    prospecto = Prospecto(
        "MAVK030710MDFRRRA3",
        "KARLA",
        "RUBY",
        "MARQUEZ",
        "VERA",
        datetime(2003, 7, 10),
        "MEXICANA",
        "1111111111",
    )
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
    direccion_uno = DireccionProspecto(
        "Cda Polvora",
        "C",
        "81",
        "San Fernando",
        "Huixquilucan de Degollado",
        "Mexico",
        "Mexico",
        "52765",
    )
    direccion_dos = DireccionProspecto(
        "Porfirio Diaz Norte",
        "#47",
        "",
        "Buenavista",
        "Nicolas Romero",
        "Mexico",
        "Mexico",
        "54414",
    )
    prospecto.add_direccion(direccion_cero)
    prospecto.add_direccion(direccion_uno)
    prospecto.add_direccion(direccion_dos)

    return prospecto


def consulta_test():
    prospecto = prospecto_test()
    direcciones_prospecto = prospecto.get_direcciones()
    nip_uno = Nip("nip1", "AACN731113MMCLJR09")
    estatus_uno = StatusConsultaCdC("PENDIENTE")
    usuario_uno = Usuario("usuario1")
    centro_uno = CentroComunitario("CCNZ")
    consulta = ConsultaCdc(
        "876657434",
        "folio001",
        datetime.now(),
        datetime.now(),
        datetime.now(),
        "consulta cdc tipo 1",
        "fallo 1",
        False,
        prospecto,
        direcciones_prospecto[0],
        nip_uno,
        estatus_uno,
        usuario_uno,
        centro_uno,
    )

    return consulta


def credit_response_test():
    return CDCResponse.from_response(XML_TEST_EVALUATIONS_RULES, config.CLAVES_PERMITIDAS)


def test_validate_consulta():
    credit_response = credit_response_test()
    prospecto = prospecto_test()
    consulta = consulta_test()

    prospecto.add_consulta_prospecto(consulta)

    assert prospecto.curp == credit_response.nombre.curp  # type: ignore
    assert consulta._estatus.status == "PENDIENTE"

    prospecto.set_consulta_data(credit_response)
    response_validate_consulta = prospecto.validate_consulta_cdc(consulta)

    assert consulta.fallo_regla == ""
    assert response_validate_consulta == "PRE APROBADO"

    credit_response.domicilios = None
    prospecto.set_consulta_data(credit_response)
    response_validate_consulta = prospecto.validate_consulta_cdc(consulta)

    assert consulta.fallo_regla == ""
    assert response_validate_consulta == "PRE APROBADO"

    credit_response.cuentas = []
    prospecto.set_consulta_data(credit_response)
    response_validate_consulta = prospecto.validate_consulta_cdc(consulta)

    assert consulta.fallo_regla == ""
    assert response_validate_consulta == "PRE APROBADO"


def test_raise_errors():
    credit_response = credit_response_test()
    prospecto = prospecto_test()
    consulta = consulta_test()

    with pytest.raises(
        CdcDomainError,
        match="Error la consulta que se intenta validar no existe.",
    ):
        prospecto.validate_consulta_cdc(consulta)

    prospecto.add_consulta_prospecto(consulta)
    credit_response.encabezado.folio_consulta = "777777"  # type: ignore
    prospecto.set_consulta_data(credit_response)
    with pytest.raises(
        CdcDomainError,
        match="Error el folio de consulta del response debe coincidir con el folio de la consulta.",
    ):
        prospecto.validate_consulta_cdc(consulta)

    credit_response.domicilios = []
    credit_response.encabezado.folio_consulta = "876657434"  # type: ignore
    prospecto.set_consulta_data(credit_response)

    with pytest.raises(
        CdcDomainError,
        match="Error la prospecto no tiene domicilios para validar.",
    ):
        prospecto.validate_consulta_cdc(consulta)

    credit_response.encabezado.folio_consulta = None  # type: ignore
    prospecto.set_consulta_data(credit_response)

    with pytest.raises(
        CdcDomainError,
        match="Error, el response no tiene folio de consulta.",
    ):
        prospecto.validate_consulta_cdc(consulta)


def test_check_past_due_accounts():
    credit_response = credit_response_test()

    prospecto = prospecto_test()
    consulta = consulta_test()
    prospecto.add_consulta_prospecto(consulta)

    credit_response.cuentas[0].saldo_vencido = "3501"  # type: ignore
    prospecto.set_consulta_data(credit_response)
    response_validate_consulta = prospecto.validate_consulta_cdc(consulta)

    assert consulta.fallo_regla == "Cuentas vencidas."
    assert response_validate_consulta == "RECHAZADO"


def test_check_broken_accounts():
    credit_response = credit_response_test()

    prospecto = prospecto_test()
    consulta = consulta_test()
    prospecto.add_consulta_prospecto(consulta)

    credit_response.cuentas[-1].clave_prevencion = "UP"  # type: ignore
    prospecto.set_consulta_data(credit_response)
    response_validate_consulta = prospecto.validate_consulta_cdc(consulta)

    assert (
        consulta.fallo_regla
        == "Cuentas en quebranto, fraude, juicio ejecutivo, ilocalizables."
    )
    assert response_validate_consulta == "RECHAZADO"


def test_check_two_broken_accounts():
    credit_response = credit_response_test()

    prospecto = prospecto_test()
    consulta = consulta_test()
    prospecto.add_consulta_prospecto(consulta)

    credit_response.cuentas[0].clave_prevencion = "UP"  # type: ignore
    credit_response.cuentas[1].clave_prevencion = "SG"  # type: ignore
    prospecto.set_consulta_data(credit_response)
    response_validate_consulta = prospecto.validate_consulta_cdc(consulta)

    assert (
        consulta.fallo_regla
        == "Dos cuentas o más en quebranto, fraude, juicio ejecutivo, ilocalizable."
    )
    assert response_validate_consulta == "RECHAZADO"


def test_check_fraudulent_accounts():
    credit_response = credit_response_test()

    prospecto = prospecto_test()
    consulta = consulta_test()
    prospecto.add_consulta_prospecto(consulta)

    credit_response.cuentas[0].clave_prevencion = "IM"  # type: ignore
    prospecto.set_consulta_data(credit_response)
    response_validate_consulta = prospecto.validate_consulta_cdc(consulta)

    assert consulta.fallo_regla == "Cuenta fraudulenta,en demanda o en mora."
    assert response_validate_consulta == "RECHAZADO"


def test_check_three_addresses():
    today = datetime.today()
    credit_response = credit_response_test()
    credit_response.domicilios[0].fecha_registro_domicilio = (today - relativedelta(months=5)).strftime("%Y-%m-%d")  # type: ignore
    credit_response.domicilios[1].fecha_registro_domicilio = (today - relativedelta(months=4)).strftime("%Y-%m-%d")  # type: ignore
    credit_response.domicilios[2].fecha_registro_domicilio = (today - relativedelta(months=3)).strftime("%Y-%m-%d")  # type: ignore
    credit_response.domicilios[3].fecha_registro_domicilio = (today - relativedelta(months=2)).strftime("%Y-%m-%d")  # type: ignore

    credit_response.domicilios[0].cp = "11111"  # type: ignore
    credit_response.domicilios[1].cp = "11112"  # type: ignore
    credit_response.domicilios[2].cp = "11113"  # type: ignore
    credit_response.domicilios[3].cp = "11114"  # type: ignore

    prospecto = prospecto_test()
    consulta = consulta_test()
    prospecto.add_consulta_prospecto(consulta)
    prospecto.set_consulta_data(credit_response)
    response_validate_consulta = (
        response_validate_consulta
    ) = prospecto.validate_consulta_cdc(consulta)

    credit_response.domicilios[3].fecha_registro_domicilio = 1  # type: ignore
    prospecto.set_consulta_data(credit_response)
    response_validate_consulta = (
        response_validate_consulta
    ) = prospecto.validate_consulta_cdc(consulta)

    assert consulta.fallo_regla == "3 Domicilios en los ultimos 6 meses."
    assert response_validate_consulta == "RECHAZADO"
