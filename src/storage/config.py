import os

from setup.config import DOCS_PATH, LOGS_PATH, Logs
from setup.data_bases import PodemosDBs, get_session


def get_api_url():
    host = os.environ.get("API_HOST", "127.0.0.1")
    http = os.environ.get("API_PROTOCOL", "http")
    port = 5000 if host == "127.0.0.1" else 80
    return f"{http}://{host}:{port}"


DEFAULT_SESSION_FACTORY = get_session(PodemosDBs.documents)

DOCS_PATH_STORAGE = f"{DOCS_PATH}/storage"

LOGS_PATH = f"{LOGS_PATH}/storage.log"

SOURCE_PATH = "src.storage"

Logs.add_logs(SOURCE_PATH, LOGS_PATH)


TIPO_ENTIDAD = (
    "PROSPECTO",
    "INTEGRANTE",
    "CREDITO",
    "GRUPO",
)

BUCKET = os.environ.get("BUCKET", "dev-documents-podemos")
PATH_S3 = os.environ.get("PATH_S3", "/tmp/")
