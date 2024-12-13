import os

from setup.config import DOCS_PATH, LOGS_PATH, Logs
from setup.data_bases import PodemosDBs, get_session


def get_api_url():
    host = os.environ.get("API_HOST", "127.0.0.1")
    http = os.environ.get("API_PROTOCOL", "http")
    port = 5000 if host == "127.0.0.1" else 80
    return f"{http}://{host}:{port}"


DEFAULT_SESSION_FACTORY = get_session(PodemosDBs.pambu)

DOCS_PATH_PAMBU = f"{DOCS_PATH}/pambu"

LOGS_PATH = f"{LOGS_PATH}/pambu.log"

SOURCE_PATH = "src.pambu"

Logs.add_logs(SOURCE_PATH, LOGS_PATH)
