import logging

from flask import Blueprint

logger = logging.getLogger(__name__)

from datetime import datetime

from flasgger import swag_from
from flask import request
from flask_restful import Api

from setup.resources import PodemosResource
from src.groups import broker
from src.groups.config import DOCS_PATH_GROUPS
from src.groups.domain import commands, queries
from src.groups.entrypoints import routers
from src.groups.errors import GroupsError


class GrupoResource(PodemosResource):
    def get(self):
        try:
            cmd = queries.GetGrupo.Schema().load(request.args)  # type: ignore
            logger.info("GetGrupo command: %s", request.args)
            response = broker.handle(cmd)
            return {
                "code": "GRP200",
                "data": {"grupos": response, "msg_success": "OK"},
                "msg": "success",
            }, 200
        except Exception as e:  # pragma: no cover
            logger.error("Error en Grupo %s", str(e))
            return {
                "code": "GRP500",
                "error": {"msg_error": str(e)},
                "msg": "fail",
            }, 500

    @swag_from(f"{DOCS_PATH_GROUPS}/create_group.yml")
    def post(self):
        try:
            cmd = commands.ADDGroup.Schema().load(request.json)  # type: ignore
            logger.info("ADDGroup Resource: command %s", cmd)
            group = broker.handle(cmd)
            return {
                "code": "GRP201",
                "data": {
                    "id_grupo": group,
                    "created": datetime.now().strftime("%Y-%m-%d"),  # type: ignore
                    "msg_success": "OK",
                },
                "msg": "success",
            }, 201

        except GroupsError as e:  # pragma: no cover
            logger.error("Grupo ya existente %s:", str(e))
            return {
                "code": "GRP400",
                "error": {"msg_error": str(e)},
                "msg": "fail",
            }, 400

        except Exception as e:  # pragma: no cover
            logger.exception("Excepcion en consulta: %s", str(e))
            return {
                "code": "GRP400",
                "error": {"msg_error": str(e)},
                "msg": "fail",
            }, 400


groups_blueprint = Blueprint("groups", __name__, url_prefix="/groups")
groups_api = Api(groups_blueprint)
groups_api.add_resource(routers.GrupoResource, "/grupo")
