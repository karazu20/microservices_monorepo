from datetime import datetime
from typing import List

from shared.cdc_utils import CDCResponse, CuentaData, DomicilioData
from shared.utils import json_to_xml
from src.cdc import config
from src.cdc.adapters.pdf_service import comma_numbers, get_situation, to_date
from src.cdc.utils import get_recipients_email
from src.cdc.validations.utils.evaluations_rules import EvaluateRules
from tests.cdc.utils import (
    XML_TEST_ACCOUNTS,
    XML_TEST_ERROR,
    XML_TEST_NO_ACCOUNTS,
    XML_TEST_ONE_ITEM,
)


def test_xml_json_function():
    evaluartest1 = """
    {"arrayColors":
        [
            {"nombreColor":"rojo","valorHexadec":"#f00"},
            { "nombreColor":"verde","valorHexadec":"#0f0"},
            { "nombreColor":"azul", "valorHexadec":"#00f"},
            { "nombreColor":"cyan", "valorHexadec":"#0ff"},
            { "nombreColor":"magenta", "valorHexadec":"#f0f"},
            { "nombreColor":"amarillo", "valorHexadec":"#ff0"},
            { "nombreColor":"negro", "valorHexadec":"#000"}
        ]
    }"""
    evaluartest2 = {
        "arrayColores": [
            {
                "rojo": "#f00",
                "verde": "#0f0",
                "azul": "#00f",
                "cyan": "#0ff",
                "magenta": "#f0f",
                "amarillo": "#ff0",
                "negro": "#000",
            }
        ]
    }

    evaluartest3 = {
        "rojo": "#f00",
        "verde": "#0f0",
        "azul": "#00f",
        "cyan": "#0ff",
        "magenta": "#f0f",
        "amarillo": "#ff0",
        "negro": "#000",
    }
    evaluartest4 = ["#f00", "#0f0", "#00f", "#0ff", "#f0f", "#ff0", "#000"]

    evaluartest5 = """
        {
            "rojo":"#f00",
            "verde":"#0f0",
            "azul":"#00f",
            "cyan":"#0ff",
            "magenta":"#f0f",
            "amarillo":"#ff0",
            "negro":"#000"
        }
    """

    json_to_xml(evaluartest1)

    json_to_xml(evaluartest2)

    json_to_xml(evaluartest3)

    json_to_xml(evaluartest4)

    json_to_xml(evaluartest5)


def test_validations():
    credit_response = CDCResponse.from_response(
        XML_TEST_ACCOUNTS, config.CLAVES_PERMITIDAS
    )
    cuentas: List[CuentaData] = credit_response.cuentas
    domicilios: List[DomicilioData] = credit_response.domicilios

    EvaluateRules(
        accounts=cuentas,
        addresses=domicilios,
        folio="FAKEFOLIO",
        curp="FAKECURP",
        username="FAKE_USER",
    ).evaluation_accounts()

    credit_response = CDCResponse.from_response(
        XML_TEST_NO_ACCOUNTS, config.CLAVES_PERMITIDAS
    )
    cuentas: List[CuentaData] = credit_response.cuentas
    domicilios: List[DomicilioData] = credit_response.domicilios
    EvaluateRules(
        accounts=cuentas,
        addresses=domicilios,
        folio="FAKEFOLIO",
        curp="FAKECURP",
        username="FAKE_USER",
    ).evaluation_accounts()

    credit_response = CDCResponse.from_response(XML_TEST_ERROR, config.CLAVES_PERMITIDAS)
    assert credit_response.error is not None
    assert credit_response.error.errores is not None
    assert len(credit_response.error.errores.descripcion_error) == 2


def test_template_filters(mocker):
    mock_pdf = mocker.patch("pdfkit.from_string")
    mock_pdf.return_value = True

    credit = CDCResponse.from_response(XML_TEST_ONE_ITEM, config.CLAVES_PERMITIDAS)
    assert len(credit.cuentas) == 0

    credit = CDCResponse.from_response(
        XML_TEST_ONE_ITEM, config.CLAVES_PERMITIDAS, exclude=False
    )
    assert len(credit.cuentas) == 1
    assert len(credit.consultas_efectuadas) == 1

    cuenta = credit.cuentas[0]
    consulta_efectuada = credit.consultas_efectuadas[0]

    situacion = get_situation(cuenta=cuenta)
    assert situacion == "Cuenta cancelada o cerrada"

    consulta_expected_date = datetime.strptime("2022-01-04", "%Y-%m-%d").strftime(
        "%d/%b/%y"
    )
    my_date = to_date(consulta_efectuada.fecha_consulta)
    assert my_date == consulta_expected_date

    my_number = comma_numbers(consulta_efectuada.importe_credito)
    assert my_number == "5,000"


def test_recipients_email():
    tribus_usuario: list = []
    consejeros: list = []

    to_s = get_recipients_email(tribus_usuario=tribus_usuario, consejeros=consejeros)

    assert len(to_s) == 1
    assert to_s[0] == "email@separated-by.comma"

    tribus_usuario = [{"UnidadesCoordinador": "TribuNR-2", "_index": 0}]
    consejeros = ["fake_consejero@fakedomain.com"]

    to_s = get_recipients_email(tribus_usuario=tribus_usuario, consejeros=consejeros)

    assert len(to_s) == 3
