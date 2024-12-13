import os

from setup.config import DOCS_PATH, LOGS_PATH, ROOT_PATH, Logs
from setup.data_bases import PodemosDBs, get_session


def get_api_url():
    host = os.environ.get("API_HOST", "127.0.0.1")
    port = 5000 if host == "127.0.0.1" else 80
    return f"http://{host}:{port}"


DEFAULT_SESSION_FACTORY = get_session(PodemosDBs.digitalization)

DOCS_PATH_CDC = f"{DOCS_PATH}/cdc"

CDC_WSDL_FILE = os.getenv("CDC_WSDL_FILE", "ConsultaReporteCCSandbox.wsdl")

WSDL_CDC_PATH = f"{ROOT_PATH}/src/cdc/templates/{CDC_WSDL_FILE}"

LOGS_PATH = f"{LOGS_PATH}/cdc.log"

SOURCE_PATH = "src.cdc"

Logs.add_logs(SOURCE_PATH, LOGS_PATH)

FOLIO_LEN_TRIBU = 6

FOLIO_LEN_ID_EMPLEADO = 8

PERIODO = int(os.getenv("PERIODO", 60))

PATH_XML = os.getenv("PATH_XML", "/files/cdc/xml/")

PATH_PDF = os.getenv("PATH_PDF", "/files/cdc/pdf/")

CLAVES_PERMITIDAS = ["FD", "IM", "PC", "SG", "UP"]


def get_email_active():
    temp = os.environ.get("CDC_EMAIL_ACTIVE", "OFF")
    return True if temp == "ON" else False


CDC_EMAIL_ACTIVE = get_email_active()


CDC_EMAIL_HUB = str(os.environ.get("CDC_EMAIL_HUB", "email@separated-by.comma,")).split(
    ","
)

CATALOG_OBSERVATIONS = {
    "AD": "Cuenta o monto en aclaracion",
    "CA": "Cartera al Corriente Vendida o cedida a un usuario de una Sociedad",
    "CC": "Cuenta cancelada o cerrada",
    "CD": "Convenio y disminución de pago",
    "CL": "Cuenta cerrada que estuvo en cobranza y fue pagada totalmente sin causar quebranto",
    "CO": "Credito en Controversia",
    "CP": (
        "Credito hipotecario con bien inmueble declarado como perdida parcial o total a causa de catastrofe natural, "
        "liquidado parcialmente por pago de Aseguradora"
    ),
    "CT": "Credito hipotecario con bien inmueble declarado como perdida parcial o total a causa de catastrofe natural",
    "CV": "Cuenta que no esta al corriente vendida o cedida a un usuario de una Sociedad",
    "GP": "Ejecucion de Garantia Prendaria o Fiduciaria en Pago por Credito",
    "FD": "Cuenta Fraudulenta",
    "FN": "Fraude no Atribuible al Consumidor",
    "FP": "Fianza pagada",
    "FR": "Adjudicacion o aplicacion de garantia",
    "IA": "Cuenta Inactiva",
    "IM": "Integrante causante de mora",
    "IS": "Integrante que fue subsidiado para evitar mora",
    "LC": "Convenio de finiquito o pago menor acordado con el Consumidor",
    "LG": (
        "Pago menor por programa institucional o de gobierno, "
        "incluyendo los apoyos a damnificados por catastrofes naturales"
    ),
    "LO": "En Localizacion",
    "LS": "Tarjeta de Credito Extraviada o Robada",
    "NA": "Cuenta al corriente vendida o cedida a un NO Usuario de una Sociedad",
    "NV": "Cuenta que no esta al corriente vendida o cedida a un NO Usuario de una Sociedad",
    "OV": "Credito que recibio apoyo por pandemia COVID-19",
    "PC": "Cuenta en Cobranza",
    "PD": "Prorroga otorgada debido a un desastre natural",
    "PE": "Prorroga otorgada al acreditado por situaciones especiales",
    "PI": "Prorroga otorgada al acreditado por invalidez, defuncion",
    "PR": "Prorroga otorgada debido a una perdida de relacion laboral",
    "RA": (
        "Cuenta reestructurada sin pago menor, "
        "por programa institucional o gubernamental, "
        "incluyendo los apoyos a damnificados por catastrofes naturales"
    ),
    "RI": "Robo de identidad",
    "RF": "Resolucion judicial favorable al cliente",
    "RN": "Cuenta reestructurada debido a un proceso judicial",
    "RV": "Cuenta reestructurada sin pago menor por modificacion de la situacion del cliente, a peticion de este",
    "SG": "Demanda por el Otorgante",
    "UP": "Cuenta que causa quebranto",
    "VR": "Dacion en Pago o Renta",
}

CDC_GRANTOR_KEY = os.getenv("CDC_GRANTOR_KEY", "")
CDC_USERNAME = os.getenv("CDC_USERNAME", "")
CDC_PASSWORD = os.getenv("CDC_PASSWORD", "")
CDC_XML_VERSION = os.getenv("CDC_XML_VERSION", "")
CDC_GRANTOR_QUERY = os.getenv("CDC_GRANTOR_QUERY", "")
CDC_REQUIRED_PRODUCT = os.getenv("CDC_REQUIRED_PRODUCT", "")
CDC_ACCOUNT_TYPE = os.getenv("CDC_ACCOUNT_TYPE", "")
CDC_CURRENCY = os.getenv("CDC_CURRENCY", "")

CDC_HOST_HTTPS = os.getenv("CDC_HOST_HTTPS", "")
CDC_HOST_HTTP = os.getenv("CDC_HOST_HTTP", "")
CDC_SOCK = os.getenv("CDC_SOCK", "")
CDC_QUERY_TEMPLATE = os.getenv("CDC_QUERY_TEMPLATE", "/src/cdc/templates/query_cdc.xml")
CDC_TIPO_CONSULTA = "PF"
PENDIENTE = "PENDIENTE"
PRE_APROBADO = "PRE APROBADO"
RECHAZADO = "RECHAZADO"
FALLO = "FALLO"
ERROR = "ERROR"
