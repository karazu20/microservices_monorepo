import os

from setup.config import DOCS_PATH, LOGS_PATH, Logs
from setup.data_bases import PodemosDBs, get_session


def get_api_url():
    host = os.environ.get("API_HOST", "127.0.0.1")
    http = os.environ.get("API_PROTOCOL", "http")
    port = 5000 if host == "127.0.0.1" else 80
    return f"{http}://{host}:{port}"


DEFAULT_SESSION_FACTORY = get_session(PodemosDBs.digitalization)
DOCS_PATH_NIP = f"{DOCS_PATH}/nip"

TWILIO_ACCOUNTSID = os.environ.get("TWILIO_ACCOUNTSID", "TWILIO_ACCOUNTSID")
TWILIO_AUTHTOKEN = os.environ.get("TWILIO_AUTHTOKEN", "TWILIO_AUTHTOKEN")
TWILIO_FROMNUMBER = os.environ.get("TWILIO_FROMNUMBER", "TWILIO_FROMNUMBER")

MAX_NIP: int = 2
MAX_NIPS_POR_TEL: int = 2
HOURS_BEFORE_NIP_CREATION: int = 24
HOURS_LIMT_TO_CREATE_NEW_NIPS: int = 24
MAX_RESEND_NIPS: int = 2
LEN_NIP: int = 7
MAX_RETRIES: int = 10


LOGS_PATH = f"{LOGS_PATH}/nip.log"

SOURCE_PATH = "src.nip"

Logs.add_logs(SOURCE_PATH, LOGS_PATH)
