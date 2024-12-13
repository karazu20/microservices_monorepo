import os
import shutil

from src.cdc import config
from src.cdc.adapters import credit_service
from src.cdc.domain.models import Prospecto


def test_make_consult(mocker):
    class MockCreditData:
        error = None

    PATH_XML_back = credit_service.xml_service.PATH_XML[:]

    credit_service.xml_service.PATH_XML = "/tmp/"
    try:
        os.mkdir("/tmp/success")
    except FileExistsError:
        pass

    mock_cdc_consult = mocker.patch("src.cdc.adapters.credit_service.CDCService.consult")
    mock_cdc_response = mocker.patch("src.cdc.adapters.credit_service.CDCResponse")

    model = Prospecto(
        nombre="JUAN",
        apellido_paterno="PRUEBA",
        apellido_materno="TRES",
        fecha_nacimiento="1980-01-02",
        curp="DOPJ800102CAJXBN02",
        nacionalidad="MX",
    )
    folio = "ABCDEFG123456"
    nip = "0192834"
    mock_cdc_consult.return_value = "xml_mocked_response"
    mock_cdc_response.from_response.return_value = MockCreditData()

    credit_service.CDCService.make_consulta_cdc(
        prospecto=model,
        folio=folio,
        nip=nip,
    )

    mock_cdc_consult.assert_called_with(model, folio, nip)
    mock_cdc_response.from_response.assert_called_with(
        response="xml_mocked_response", claves_permitidas=config.CLAVES_PERMITIDAS
    )

    with open("/tmp/success/ABCDEFG123456.xml") as f:
        assert "xml_mocked_response" == f.read()

    credit_service.xml_service.PATH_XML = PATH_XML_back
    shutil.rmtree("/tmp/success")
