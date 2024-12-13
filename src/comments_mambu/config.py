import os

from setup.config import DOCS_PATH, LOGS_PATH, Logs


def get_api_url():
    host = os.environ.get("API_HOST", "127.0.0.1")
    port = 5000 if host == "127.0.0.1" else 80
    return f"http://{host}:{port}"


DOCS_PATH_COMMENTS = f"{DOCS_PATH}/comments_mambu"

LOGS_PATH = f"{LOGS_PATH}/comments_mambu.log"

SOURCE_PATH = "src.comments_mambu"

Logs.add_logs(SOURCE_PATH, LOGS_PATH)
