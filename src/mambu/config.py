import os

from setup.config import LOGS_PATH, Logs


def get_api_url():
    host = os.environ.get("API_HOST", "127.0.0.1")
    http = os.environ.get("API_PROTOCOL", "http")
    port = 5000 if host == "127.0.0.1" else 80
    return f"{http}://{host}:{port}"


LOGS_PATH = f"{LOGS_PATH}/mambu.log"

SOURCE_PATH = "src.mambu"

Logs.add_logs(SOURCE_PATH, LOGS_PATH)
