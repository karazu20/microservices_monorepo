import abc
import logging
import os

from jinja2 import Environment
from requests import Session
from zeep import Client  # type: ignore
from zeep.transports import Transport  # type: ignore

from setup.domain import Model
from shared.cdc_utils import CDCResponse
from src.cdc import config, errors
from src.cdc.adapters import xml_service
from src.cdc.domain.models import Prospecto

logger = logging.getLogger(__name__)


class CreditService(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def consult(cls, person: Model, folio, nip):
        raise NotImplementedError


class CDCService(CreditService):
    @classmethod
    def make_consulta_cdc(cls, prospecto: Prospecto, folio: str, nip: str) -> CDCResponse:
        xml_response = cls.consult(prospecto, folio, nip)
        xmlservice = xml_service.CDCXmlService()

        try:
            is_success = False
            credit_data = CDCResponse.from_response(
                response=xml_response, claves_permitidas=config.CLAVES_PERMITIDAS
            )
        except Exception as ex:  # pragma: no cover
            # ERROR: querycdc.estatus_consulta_id = 5
            logger.exception("Error en formato de respuesta de CDC: %s", str(ex))
            raise errors.CdcServiceError("Error en respuesta de CDC.")
        finally:
            is_success = credit_data.error is None
            xmlservice.save(folio=folio, xml_response=xml_response, is_success=is_success)
        if not is_success:
            # FALLO: querycdc.estatus_consulta_id = 4
            logger.error(
                "Error con consulta a círculo de credito de %s, folio CDC: %s folio: %s",
                prospecto.curp,
                credit_data.encabezado.folio_consulta,
                folio,
            )
            raise errors.CdcServiceFallo("Error con consulta a círculo de credito")

        return credit_data

    @classmethod
    def _query_template(cls, person: Model, folio, nip) -> str:
        directory = os.path.abspath(os.getcwd()) + config.CDC_QUERY_TEMPLATE
        read_file = open(directory, "r")
        tempenv = Environment(autoescape=True).from_string(read_file.read())
        xml_render = tempenv.render(
            cdc_grantor_key=config.CDC_GRANTOR_KEY,
            cdc_username=config.CDC_USERNAME,
            cdc_password=config.CDC_PASSWORD,
            cdc_xml_version=config.CDC_XML_VERSION,
            cdc_grantor_query=folio,
            cdc_required_product=config.CDC_REQUIRED_PRODUCT,
            cdc_account_type=config.CDC_ACCOUNT_TYPE,
            cdc_currency=config.CDC_CURRENCY,
            nip=nip,
            persons=[person],
        )

        return xml_render

    @classmethod
    def consult(cls, person: Model, folio, nip) -> str:
        xml_render = cls._query_template(person, folio, nip)

        session_cdc = Session()
        session_cdc.proxies = {
            config.CDC_HOST_HTTPS: config.CDC_SOCK,
            config.CDC_HOST_HTTP: config.CDC_SOCK,
        }
        session_cdc.verify = False
        client_api_cdc = Client(config.WSDL_CDC_PATH, Transport(session=session_cdc))
        client_api_cdc.wsse = None

        try:
            return client_api_cdc.service.generaReporte(xml_render)
        except Exception as e:
            logger.error("Error en obtener datos de integrante desde CDC %s", str(e))
            raise e
