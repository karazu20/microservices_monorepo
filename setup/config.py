import logging
import os
from logging import FileHandler, StreamHandler
from typing import List

from flask import has_request_context, request


def get_redis_host_and_port():
    host = os.environ.get("REDIS_HOST", "localhost")
    port = os.environ.get("REDIS_PORT", 6379)
    password = os.environ.get("REDIS_PASS", None)
    return dict(host=host, port=port, password=password)


TWILIO_ACCOUNTSID = os.environ.get("TWILIO_ACCOUNTSID", "TWILIO_ACCOUNTSID")
TWILIO_AUTHTOKEN = os.environ.get("TWILIO_AUTHTOKEN", "TWILIO_AUTHTOKEN")
TWILIO_FROMNUMBER = os.environ.get("TWILIO_FROMNUMBER", "TWILIO_FROMNUMBER")


SETUP_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.dirname(SETUP_PATH)
DOCS_PATH = f"{ROOT_PATH}/docs"
LOGS_PATH = f"{ROOT_PATH}/logs"

SWAGGER = {
    "title": "Podemos Microservices",
    "uiversion": 3,
}


FORMAT_LOGGER = (
    "[%(levelname)s - %(asctime)s] %(remote_addr)s "
    "requested %(url)s in %(module)s: %(message)s"
)

SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(32))
CHECK_CSRF = os.environ.get("CHECK_CSRF", "False") == "True"
ORIGINS_CORS = os.environ.get("ORIGINS_CORS", "*")


FORMAT_LOGGER_BUS = "[%(levelname)s - %(name)s - %(asctime)s ] Adapter Bus: %(message)s"

FORMAT_LOGGER_MS = "[%(levelname)s - %(name)s - %(asctime)s ] %(funcName)s: %(message)s"

FORMAT_LOGGER_MAMBU = (
    "[%(levelname)s - %(name)s - %(asctime)s] Adapter Mambu: %(message)s"
)

APPLICATION_ROOT = os.environ.get("APPLICATION_ROOT", "")

TOKEN_HEADER = "token-user"

CIPHERKEY = os.environ.get("CIPHERKEY", "DummykeyDragonBall0000")

EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 465))
EMAIL_USER = os.getenv("EMAIL_USER", "your-user-email")
EMAIL_PASS = os.getenv("EMAIL_PASS", "your-super-pass")
EMAIL_SENDER = os.getenv("EMAIL_SENDER", "email-sender@domain.com")
EMAIL_HUB = str(os.getenv("EMAIL_HUB", "email@separated-by.comma,")).split(",")

# S3 Login
SERVICE_NAME = os.environ.get("SERVICE_NAME", "")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
PATH_S3 = os.environ.get("PATH_S3", "/tmp/")
EXPIRES_IN = os.environ.get("EXPIRES_IN", 0)


class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.remote_addr = None
        return super().format(record)


class Logs:
    logs_modules: List[dict] = []

    @classmethod
    def config_logs(cls, app, env):
        formatter_ws = RequestFormatter(FORMAT_LOGGER)
        if app:
            if env in ["dev", "test"]:
                handler_alejandria = StreamHandler()
                handler_alejandria.setFormatter(formatter_ws)
                app.logger.addHandler(handler_alejandria)
                app.logger.setLevel(level=logging.INFO)
            else:
                handler_alejandria = FileHandler(f"{LOGS_PATH}/alejandria.log")
                handler_alejandria.setFormatter(formatter_ws)
                app.logger.addHandler(handler_alejandria)
                app.logger.setLevel(level=logging.INFO)

        for log in cls.logs_modules:
            cls.config_logs_modules(log.get("source_path"), log.get("logs_path"), env)

        return app

    @classmethod
    def add_logs(cls, source_path, logs_path):
        cls.logs_modules.append({"source_path": source_path, "logs_path": logs_path})

    @classmethod
    def config_logs_modules(cls, source_path, logs_path, env):
        formatter_ws = RequestFormatter(FORMAT_LOGGER_MS)
        ms_logger = logging.getLogger(source_path)

        if env in ["dev", "test"]:
            handler_ms = StreamHandler()
            handler_ms.setFormatter(formatter_ws)
            ms_logger.addHandler(handler_ms)
            ms_logger.setLevel(level=logging.INFO)
        else:
            handler_ms = FileHandler(logs_path)
            handler_ms.setFormatter(formatter_ws)
            ms_logger.addHandler(handler_ms)
            ms_logger.setLevel(level=logging.INFO)


Logs.add_logs("setup.adapters.bus", f"{LOGS_PATH}/bus.log")
Logs.add_logs("setup.adapters.cache", f"{LOGS_PATH}/cache.log")
Logs.add_logs("setup.adapters.mambu_models", f"{LOGS_PATH}/mambu_adapter.log")
Logs.add_logs("setup.adapters.messenger_service", f"{LOGS_PATH}/twilio.log")
Logs.add_logs("setup.adapters.storage", f"{LOGS_PATH}/storage.log")
