import locale
import logging
from datetime import datetime
from typing import Any, Tuple

import pdfkit
from jinja2 import Environment, PackageLoader, select_autoescape

from shared.cdc_utils import CDCResponse, CuentaData, NombreData
from src.cdc.adapters.file_service import FileService
from src.cdc.config import CATALOG_OBSERVATIONS, PATH_PDF

logger = logging.getLogger(__name__)


def get_situation(cuenta: CuentaData) -> str:
    situacion: str = ""
    if cuenta.clave_prevencion and cuenta.clave_prevencion in CATALOG_OBSERVATIONS:
        try:
            observation = CATALOG_OBSERVATIONS[cuenta.clave_prevencion]
        except KeyError:  # pragma: no cover
            observation = ""

        situacion = observation

        if cuenta.tipo_cuenta == "R":
            situacion = "Revolvente. {}".format(situacion)
    elif cuenta.clave_prevencion:
        situacion = "Situacion no reconocible por el sistema. Informe a TI"
    else:
        situacion = ""

    return situacion


def to_date(value: Any) -> str:
    temp_value = datetime.strptime(value, "%Y-%m-%d")
    return "{}".format(temp_value.strftime("%d/%b/%y"))


def comma_numbers(value: Any) -> str:
    temp_value = value
    if not isinstance(value, int):
        temp_value = int(value)
    return "{:,}".format(int(temp_value))


class CDCPdfService(FileService):
    file_extension = "pdf"

    def get_file_name(  # type: ignore
        self, folio: str, nombres: NombreData, fecha_consulta: datetime
    ) -> str:
        nombre_completo = (
            "{}{}{}".format(
                nombres.nombres, nombres.apellido_paterno, nombres.apellido_materno
            )
            .replace(" ", "")
            .upper()
        )
        filename = "{}_{}_{}_{}".format(
            nombre_completo, nombres.curp, folio, fecha_consulta.strftime("%Y%m%d")
        )
        return "{}{}.{}".format(PATH_PDF, filename, self.file_extension)

    def get_rendered_template(
        self, credit_data: CDCResponse, fecha_consulta: datetime
    ) -> str:
        env = Environment(
            loader=PackageLoader("src.cdc", "templates"), autoescape=select_autoescape()
        )
        env.filters["get_situation"] = get_situation
        env.filters["to_date"] = to_date
        env.filters["comma_numbers"] = comma_numbers
        template = env.get_template("resumen_cdc.html")
        return template.render(credit=credit_data, fecha_consulta=fecha_consulta)

    def save(self, folio: str, credit_data: CDCResponse) -> Tuple[str, bool]:  # type: ignore
        try:
            logger.info("Se almacena PDF del folio: %s", folio)
            locale.setlocale(locale.LC_ALL, "es_MX.utf8")
            fecha_consulta = datetime.now()
            filename = self.get_file_name(folio, credit_data.nombre, fecha_consulta)  # type: ignore
            html = self.get_rendered_template(credit_data, fecha_consulta)
            logger.info("Pdf name: %s", filename)
            result = pdfkit.from_string(
                html, output_path=filename, css=["src/cdc/templates/css/resumen_cdc.css"]
            )
            logger.info("Result: %s", str(result))
            return filename, result
        except Exception as ex:
            logger.error("Error al guardar pdf del folio: %s %s", folio, str(ex))
            return "", False
