import logging
from datetime import datetime

from src.cdc.adapters import credit_service, pdf_service
from src.cdc.domain.models import Prospecto

logging.disable(logging.CRITICAL)


def test_cdcservice_consult(mocker):
    credit_data = credit_service.CDCResponse()
    credit_data.error = None

    mock_cdc_client = mocker.patch("src.cdc.adapters.credit_service.Client")

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
    template = credit_service.CDCService._query_template(model, folio, nip)

    credit_service.CDCService.consult(
        person=model,
        folio=folio,
        nip=nip,
    )
    mock_cdc_client.return_value.service.generaReporte.assert_called_with(template)


def test_pdfservice_getsituacion_normal():
    cuenta = pdf_service.CuentaData()
    situacion = pdf_service.get_situation(cuenta)

    assert "" == situacion


def test_pdfservice_getsituacion_noreconocible():
    cuenta = pdf_service.CuentaData()
    cuenta.clave_prevencion = "SOMETHING STRANGE"
    situacion = pdf_service.get_situation(cuenta)

    assert "Situacion no reconocible por el sistema. Informe a TI" == situacion


def test_pdfservice_getsituacion_observacion():
    cuenta = pdf_service.CuentaData()
    cuenta.clave_prevencion = "AD"
    situacion = pdf_service.get_situation(cuenta)

    assert "Cuenta o monto en aclaracion" == situacion


def test_pdfservice_getsituacion_observacion_revolvente():
    cuenta = pdf_service.CuentaData()
    cuenta.clave_prevencion = "AD"
    cuenta.tipo_cuenta = "R"
    situacion = pdf_service.get_situation(cuenta)

    assert "Revolvente. Cuenta o monto en aclaracion" == situacion


def test_pdfservice_gefilename():
    PATH_PDF = pdf_service.PATH_PDF
    pdfs = pdf_service.CDCPdfService()

    names = pdf_service.NombreData()
    names.nombres = "UNA FULANITA"
    names.apellido_paterno = "DE"
    names.apellido_materno = "TAL"
    names.curp = "DETU123456"

    filename = pdfs.get_file_name(
        folio="ABCDEFG123456", nombres=names, fecha_consulta=datetime.now()
    )
    assert filename == "{}{}{}.pdf".format(
        PATH_PDF,
        "UNAFULANITADETAL_DETU123456_ABCDEFG123456_",
        datetime.now().strftime("%Y%m%d"),
    )


def test_pdfservice_save(mocker):
    mock_locale = mocker.patch("src.cdc.adapters.pdf_service.locale")
    mock_locale.setlocale.return_value = ""
    mock_cdc_pdfkit = mocker.patch("src.cdc.adapters.pdf_service.pdfkit")
    mock_cdc_pdfkit.from_string.return_value = True
    mock_cdc_jinja_env = mocker.patch("src.cdc.adapters.pdf_service.Environment")
    mock_cdc_jinja_env.return_value.get_template.return_value.render.return_value = (
        "pdf_mocked_response"
    )

    PATH_PDF_back = pdf_service.PATH_PDF[:]
    pdf_service.PATH_PDF = "/tmp/"
    pdfs = pdf_service.CDCPdfService()

    credit = pdf_service.CDCResponse()
    credit.nombre = pdf_service.NombreData()
    credit.nombre.nombres = "UNA FULANITA"
    credit.nombre.apellido_paterno = "DE"
    credit.nombre.apellido_materno = "TAL"
    credit.nombre.curp = "DETU123456"

    fname, result = pdfs.save(folio="ABCDEFG123456", credit_data=credit)

    assert fname == "/tmp/UNAFULANITADETAL_DETU123456_ABCDEFG123456_{}.pdf".format(
        datetime.now().strftime("%Y%m%d")
    )
    assert result == True
    mock_cdc_pdfkit.from_string.assert_called_with(
        "pdf_mocked_response",
        output_path=fname,
        css=["src/cdc/templates/css/resumen_cdc.css"],
    )

    pdf_service.PATH_PDF = PATH_PDF_back
