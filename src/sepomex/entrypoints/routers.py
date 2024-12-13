import logging

from flasgger import swag_from
from flask import Blueprint, request
from flask_restful import Api

from setup.resources import PodemosResource
from src.sepomex import broker
from src.sepomex.config import DOCS_PATH_SEPOMEX
from src.sepomex.domain import commands, queries
from src.sepomex.entrypoints import routers

logger = logging.getLogger(__name__)


class DataFromCPResource(PodemosResource):
    @swag_from(f"{DOCS_PATH_SEPOMEX}/colonies_from_cp.yml")
    def get(self):
        try:
            qry = queries.GetDataFromCP.Schema().load(request.args)  # type: ignore

            logger.info("MasterDataResource: query %s", qry)
            colonias = broker.handle(qry)
            colonias["msg_success"] = ""
            return {"code": "SEP200", "data": colonias, "msg": "success"}, 200
        except Exception as e:
            return {"code": "SEP500", "error": {"msg_error": str(e)}, "msg": "fail"}, 500
        return "OK", 200


class ColoniasResource(PodemosResource):
    def get(self):
        try:
            qry = queries.GetColonias.Schema().load(request.args)  # type: ignore
            logger.info("ColoniasResource: query %s", qry)
            colonias = broker.handle(qry)
            return {"code": 200, "data": colonias, "msg": "success"}, 200
        except Exception as e:
            return {"message": str(e)}, 500
        return "OK", 200

    @swag_from(f"{DOCS_PATH_SEPOMEX}/create_colony.yml")
    def post(self):
        try:
            cmd = commands.ADDColonia.Schema().load(request.json)  # type: ignore
            logger.info("ColoniasResource: command %s", cmd)
            broker.handle(cmd)
            return {"code": 201, "data": {}, "msg": "success"}, 201
        except Exception as e:
            return {"message": str(e)}, 500


class MunicipiosResource(PodemosResource):
    def get(self):
        try:
            qry = queries.GetMunicipios.Schema().load(request.args)  # type: ignore
            logger.info("MunicipiosResource: query %s", qry)
            municipios = broker.handle(qry)
            return {"code": 200, "data": municipios, "msg": "success"}, 200
        except Exception as e:
            return {"message": str(e)}, 500
        return "OK", 200

    def post(self):
        try:
            cmd = commands.ADDMunicipio.Schema().load(request.json)  # type: ignore
            logger.info("MunicipiosResource: command %s", cmd)
            broker.handle(cmd)
            return {"code": 201, "data": {}, "msg": "success"}, 201
        except Exception as e:
            return {"message": str(e)}, 500


class EstadosResource(PodemosResource):
    def get(self):
        try:
            qry = queries.GetEstados.Schema().load(request.args)  # type: ignore
            logger.info("EstadosResource: query %s", qry)
            estados = broker.handle(qry)
            return {"code": 200, "data": estados, "msg": "success"}, 200
        except Exception as e:
            return {"message": str(e)}, 500
        return "OK", 200

    def post(self):
        try:
            cmd = commands.ADDEstado.Schema().load(request.json)  # type: ignore
            logger.info("EstadosResource: command %s", cmd)
            broker.handle(cmd)
            return {"code": 201, "data": {}, "msg": "success"}, 201
        except Exception as e:
            return {"message": str(e)}, 500


sepomex_blueprint = Blueprint("sepomex", __name__, url_prefix="/sepomex")


sepomex_api = Api(sepomex_blueprint)

sepomex_api.add_resource(routers.EstadosResource, "/estados")
sepomex_api.add_resource(routers.MunicipiosResource, "/municipios")
sepomex_api.add_resource(routers.ColoniasResource, "/colonias")
sepomex_api.add_resource(routers.DataFromCPResource, "/colonias_cp")
