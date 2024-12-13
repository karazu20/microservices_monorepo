import os

from setup.config import DOCS_PATH, LOGS_PATH, Logs
from setup.data_bases import PodemosDBs, get_session


def get_api_url():
    host = os.environ.get("API_HOST", "127.0.0.1")
    port = 5000 if host == "127.0.0.1" else 80
    return f"http://{host}:{port}"


DEFAULT_SESSION_FACTORY = get_session(PodemosDBs.digitalization)

DOCS_PATH_GROUPS = f"{DOCS_PATH}/groups"

LOGS_PATH = f"{LOGS_PATH}/groups.log"

SOURCE_PATH = "src.groups"

Logs.add_logs(SOURCE_PATH, LOGS_PATH)
