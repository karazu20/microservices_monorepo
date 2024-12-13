import logging

from flasgger import swag_from
from flask import Blueprint, request
from flask_restful import Api
from marshmallow.exceptions import ValidationError

from setup.adapters.messenger_service import SMSError
from setup.resources import PodemosResource
from shared.errors import BaseErrorsTypes
from src.nip import broker
from src.nip.config import DOCS_PATH_NIP
from src.nip.domain import commands
from src.nip.entrypoints import routers
from src.nip.errors import NipError

logger = logging.getLogger(__name__)


class GenerateNip(PodemosResource):
    @swag_from(f"{DOCS_PATH_NIP}/generate_nip.yml")
    def post(self):
        try:
            cmd = commands.GenerateNip.Schema().load(request.json)  # type: ignore
            logger.info("GenerateNip Recurso:comando %s", request.json)
            nip = broker.handle(cmd)
            return {
                "code": "NIP201",
                "data": {
                    "nip": nip,
                    "msg_success": "Nip generado exitosamente",
                },
                "msg": "success",
            }, 201
        except ValidationError as e:
            logger.error(
                "ValidationError to GenerateNip: {}".format(e.normalized_messages())
            )
            message = ""
            normalized_messages = e.normalized_messages()
            for value in normalized_messages:
                message += normalized_messages[value][0] + ","

            return {
                "code": "NIP400",
                "error": {"type_error": BaseErrorsTypes.EDITAR, "msg_error": message},
                "msg": "fail",
            }, 400
        except SMSError as e:  # pragma: no cover
            logger.error("Exception Twlio to GenerateNip: {}".format(e))
            return {
                "code": "NIP400",
                "error": {"type_error": BaseErrorsTypes.EDITAR, "msg_error": str(e)},
                "msg": "fail",
            }, 400
        except NipError as e:  # pragma: no cover
            logger.error("Error to GenerateNip: {}".format(e))
            return {"code": "NIP400", "error": {"msg_error": str(e)}, "msg": "fail"}, 400


class ValidateNip(PodemosResource):
    @swag_from(f"{DOCS_PATH_NIP}/validate_nip.yml")
    def post(self):
        try:
            cmd = commands.ValidateNip.Schema().load(request.json)  # type: ignore
            logger.info("ValidateNip Recurso: comando %s", request.json)
            nip = broker.handle(cmd)
            return {
                "code": "NIP201",
                "data": {
                    "nip": nip,
                    "msg_sucess": "Nip validado exitosamente",
                },
                "msg": "success",
            }, 201

        except NipError as e:  # pragma: no cover
            logger.error("Error to ValidateNip: {}".format(e))
            return {"code": "NIP400", "error": {"msg_error": str(e)}, "msg": "fail"}, 400


class ResendNip(PodemosResource):
    @swag_from(f"{DOCS_PATH_NIP}/resend_nip.yml")
    def post(self):
        try:
            cmd = commands.ResendNip.Schema().load(request.json)  # type: ignore
            logger.info("ResendNip Recurso: comando %s", request.json)
            nip = broker.handle(cmd)
            return {
                "code": "NIP201",
                "data": {
                    "nip": nip,
                    "msg_sucess": "Nip re-enviado exitosamente",
                },
                "msg": "success",
            }, 201
        except SMSError as e:  # pragma: no cover
            logger.error("Exception Twilio to ResendNip: {}".format(e))
            return {"code": "NIP400", "error": {"msg_error": str(e)}, "msg": "fail"}, 400

        except NipError as e:  # pragma: no cover
            logger.error("Error to ResendNip: {}".format(e))
            return {"code": "NIP400", "error": {"msg_error": str(e)}, "msg": "fail"}, 400


class GenerateMassiveNip(PodemosResource):
    @swag_from(f"{DOCS_PATH_NIP}/generate_massive_nip.yml")
    def post(self):
        response = []
        try:
            for value in request.json:  # type: ignore
                try:
                    cmd = commands.GenerateNip.Schema().load(value)  # type: ignore
                    logger.info("GenerateMassiveNip Recurso:comando %s", value)
                    nip = broker.handle(cmd)
                    response.append(
                        {
                            "curp": cmd.curp,
                            "nip": nip,
                            "status_msg": "",
                            "code": "NIP200",
                            "type_error": None,
                        }
                    )
                except ValidationError as e:
                    logger.error(
                        "ValidationError to GenerateMassiveNip: {}".format(
                            e.normalized_messages()
                        )
                    )
                    message = ""
                    normalized_messages = e.normalized_messages()
                    for value in normalized_messages:
                        message += normalized_messages[value][0] + ","

                    response.append(
                        {
                            "curp": None,
                            "nip": None,
                            "status_msg": message,
                            "code": "NIP400",
                            "type_error": BaseErrorsTypes.EDITAR,
                        }
                    )
                except SMSError as e:  # pragma: no cover
                    logger.error("Exception Twlio to GenerateMassiveNip: {}".format(e))
                    response.append(
                        {
                            "curp": cmd.curp,
                            "nip": None,
                            "status_msg": str(e),
                            "code": "NIP400",
                            "type_error": BaseErrorsTypes.EDITAR,
                        }
                    )
                except NipError as e:
                    logger.error("Error to GenerateMassiveNip: {}".format(e))
                    try:
                        curp = cmd.curp
                    except Exception:
                        curp = None

                    response.append(
                        {
                            "curp": curp,
                            "nip": None,
                            "status_msg": str(e),
                            "code": "NIP400",
                            "type_error": BaseErrorsTypes.NO_EDITAR,
                        }
                    )
            return {
                "code": "NIP201",
                "data": {
                    "prospectas": response,
                    "msg_success": "Nip generado exitosamente",
                },
                "msg": "success",
            }, 201
        except NipError as e:  # pragma: no cover
            logger.error("Error to GenerateMassiveNip: {}".format(e))
            return {"code": "NIP400", "error": {"msg_error": str(e)}, "msg": "fail"}, 400


nip_blueprint = Blueprint("nip", __name__, url_prefix="/nip")
nip_api = Api(nip_blueprint)
nip_api.add_resource(routers.GenerateNip, "/generateNIP")
nip_api.add_resource(routers.ValidateNip, "/validateNIP")
nip_api.add_resource(routers.ResendNip, "/resendNIP")
nip_api.add_resource(routers.GenerateMassiveNip, "/generateMassiveNIP")
