import logging

from flasgger import swag_from
from flask import Blueprint, request
from flask_restful import Api
from MambuPy.mambuutil import MambuError
from sqlalchemy.exc import IntegrityError

from setup.resources import PublicResource
from src.pambu import broker
from src.pambu.config import DOCS_PATH_PAMBU
from src.pambu.domain import commands, queries
from src.pambu.entrypoints import routers
from src.pambu.services_layer.handlers import EmailException

logger = logging.getLogger(__name__)


class UserAppResource(PublicResource):
    @swag_from(f"{DOCS_PATH_PAMBU}/create_user_app.yml")
    def post(self):
        try:
            cmd = commands.ADDUser.Schema().load(request.json)  # type: ignore
            logger.info("ADDUser Resource: command %s", request.json)
            broker.handle(cmd)
            return {
                "code": "PAM201",
                "data": {
                    "msg_success": "Alta exitosa",
                },
                "msg": "Success",
            }, 201
        except MambuError:
            return {
                "code": "PAM401",
                "error": {
                    "email": "soportepodemosti@podemosprogresar.freshdesk.com",
                    "subject": "Error: registro de usuario movil",
                    "body": "Buen día <br> He tenido problema al realizar mi registro "
                    + "solicité acceso con los siguientes datos:<br> username:"
                    + request.json["username"]  # type: ignore
                    + "<br> email: "
                    + request.json["email"],  # type: ignore
                    "msg_error": "Error para encontrar usuario en mambu.",
                },
                "msg": "fail",
            }, 401
        except IntegrityError:
            return {
                "code": "PAM401",
                "error": {
                    "email": "",
                    "body": "",
                    "subject": "",
                    "msg_error": "Usuario duplicado",
                },
                "msg": "fail",
            }, 401
        except EmailException:
            return {
                "code": "PAM401",
                "error": {
                    "email": "soportepodemosti@podemosprogresar.freshdesk.com",
                    "subject": "Error: registro de usuario movil",
                    "body": "Buen día <br> He tenido problema al realizar mi registro "
                    + "solicité acceso con los siguientes datos:<br> username:"
                    + request.json["username"]  # type: ignore
                    + "<br> email: "
                    + request.json["email"],  # type: ignore
                    "msg_error": "Error para encontrar usuario en mambu.",
                },
                "msg": "fail",
            }, 401
        except Exception as e:
            logger.error("Error al crear usuario %s:", str(e))
            return {"code": "PAM501", "error": str(e), "msg": "fail"}, 501


class GetReleaseResource(PublicResource):
    def get(self):
        try:
            cmd = queries.GetRelease.Schema().load(request.args)  # type: ignore
            logger.info("GetRelease Resource: command %s", request.args)
            response = broker.handle(cmd)
            return {
                "code": "PAM200",
                "data": {"msg_success": "OK", "url_version": response},
                "msg": "Success",
            }, 200
        except Exception as e:  # pragma: no cover
            logger.error("Error en obtener ultima version %s:", str(e))
            return {
                "code": "PAM500",
                "error": {
                    "msg_error": "Error al obtener última version, favor contacte a soporte"
                },
                "msg": "fail",
            }, 500


pambu_blueprint = Blueprint("pambu", __name__, url_prefix="/pambu")
pambu_api = Api(pambu_blueprint)
pambu_api.add_resource(routers.UserAppResource, "/new_user")
pambu_api.add_resource(routers.GetReleaseResource, "/app_last_version")
