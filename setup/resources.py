import os
import time
from functools import wraps

from flask import current_app as app
from flask_restful import Resource

from setup.sessions import current_user

env = os.environ.get("ENV", "prod")


def handler_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        try:
            result = func(*args, **kwargs)
            elapsed = time.time() - start
            app.logger.info(f"time:{elapsed}")
            return result
        except Exception as e:
            app.logger.error("Error inesperado con la Exception : {}".format(e))
            return {
                "code": "ERR500",
                "error": {
                    "msg_error": f"Error inesperado, contacta a tu proveedor de servicio",
                },
                "msg": "fail",
            }, 500

    return wrapper


def authenticated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user() and env != "dev":
            return {
                "code": "ERR401",
                "error": {
                    "msg_error": "Se requiere login de usuario para acceder a este recurso",
                },
                "msg": "fail",
            }, 401
        else:
            return func(*args, **kwargs)

    return wrapper


class PodemosResource(Resource):
    method_decorators = [authenticated, handler_request]


class PublicResource(Resource):
    method_decorators = [handler_request]
