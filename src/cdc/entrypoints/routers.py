import logging

from flasgger import swag_from
from flask import Blueprint

logger = logging.getLogger(__name__)

from flask import request
from flask_restful import Api

from setup.resources import PodemosResource
from src.cdc import broker
from src.cdc.config import DOCS_PATH_CDC
from src.cdc.domain import commands, queries
from src.cdc.entrypoints import routers
from src.cdc.errors import CdcError


class PersonResource(PodemosResource):
    def get(self):
        try:
            qry = queries.GetPerson.Schema().load(request.args)  # type: ignore
            logger.info("PersonResource: query %s", qry)
            person = broker.handle(qry)
            return person, 200
        except Exception as e:  # pragma: no cover
            return {"message": str(e)}, 500


class BasicConsultResource(PodemosResource):
    command = commands.ADDPerson

    @swag_from(f"{DOCS_PATH_CDC}/create_person.yml")
    def post(self):
        try:
            cmd = self.command.Schema().load(request.json)  # type: ignore
            logger.info("%s Resource: command %s", str(self.command), cmd)
            response = broker.handle(cmd)
            message = "success"
            status_code = 201
            return {
                "code": "CDC201",
                "data": response,
                "msg": message,
            }, status_code

        except CdcError as e:  # pragma: no cover
            logger.error("Error to generated consult cdc: %s", str(e))
            return {
                "code": "CDC400",
                "error": {
                    "id": e.id,
                    "estatus": e.estatus,
                    "curp": e.curp,
                    "folio": e.folio,
                    "timestamp_consulta": e.timestamp_consulta,
                    "fallo_regla": e.fallo_regla,
                    "msg_error": e.msg_error,
                },
                "msg": "fail",
            }, 400
        except Exception as e:  # pragma: no cover
            logger.exception("Excepcion en consulta: %s", str(e))
            return {
                "code": "CDC400",
                "error": {"msg_error": str(e)},
                "msg": "fail",
            }, 400


class ConsultaV2Resource(BasicConsultResource):
    command = commands.ValidateConsultaCDC  # type: ignore

    @swag_from(f"{DOCS_PATH_CDC}/consulta_cdc.yml")
    def post(self):
        return super(ConsultaV2Resource, self).post()


class ConsultListResource(PodemosResource):
    def get(self):
        try:
            cmd = queries.GetConsultCDC.Schema().load(request.args)  # type: ignore
            logger.info("GetConsultCDC Resource: command %s", request.args)
            response = broker.handle(cmd)
            return {
                "code": "CDC200",
                "data": {"consultas": response, "msg_success": "OK"},
                "msg": "success",
            }, 200
        except Exception as e:  # pragma: no cover
            return {
                "code": "CDC500",
                "error": {"msg_error": str(e)},
                "msg": "fail",
            }, 500


cdc_blueprint = Blueprint("cdc", __name__, url_prefix="/cdc")
cdc_api = Api(cdc_blueprint)
cdc_api.add_resource(routers.PersonResource, "/person")
cdc_api.add_resource(routers.BasicConsultResource, "/consultaCDC")
cdc_api.add_resource(routers.ConsultListResource, "/consult_list")
cdc_api.add_resource(routers.ConsultaV2Resource, "/v2/consultaCDC")
