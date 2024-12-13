import os

from setup.config import DOCS_PATH, LOGS_PATH, Logs
from setup.data_bases import PodemosDBs, get_session


def get_api_url():
    host = os.environ.get("API_HOST", "127.0.0.1")
    http = os.environ.get("API_PROTOCOL", "http")
    port = 5000 if host == "127.0.0.1" else 80
    return f"{http}://{host}:{port}"


DEFAULT_SESSION_FACTORY_VALIDATIONS = get_session(PodemosDBs.validations)
DEFAULT_SESSION_FACTORY_DIGITALIZATION = get_session(PodemosDBs.digitalization)

DOCS_PATH_VALIDATIONS = f"{DOCS_PATH}/validations"

LOGS_PATH = f"{LOGS_PATH}/validations.log"

SOURCE_PATH = "src.validations"

Logs.add_logs(SOURCE_PATH, LOGS_PATH)

DAYS = {
    "LUNES": 1,
    "MARTES": 2,
    "MIERCOLES": 3,
    "JUEVES": 4,
    "VIERNES": 5,
    "MONDAY": 1,
    "TUESDAY": 2,
    "WEDNESDAY": 3,
    "THURSDAY": 4,
    "FRIDAY": 5,
    "MI\xc3\xa9RCOLES": 3,
    "MIÉRCOLES": 3,
}
