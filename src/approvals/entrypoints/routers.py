import logging

from flasgger import swag_from
from flask import Blueprint, request
from flask_restful import Api

from setup.resources import PodemosResource
from src.approvals import broker
from src.approvals.config import DOCS_PATH_APPROVALS
from src.approvals.domain import commands
from src.approvals.entrypoints import routers

logger = logging.getLogger(__name__)


class ApprovalResource(PodemosResource):
    @swag_from(f"{DOCS_PATH_APPROVALS}/create_approval.yml")
    def post(self):
        try:
            response = []
            for value in request.json:  # type: ignore
                cmd = commands.ADDApproval.Schema().load(value)  # type: ignore
                logger.info("ADDApproval Resource: query %s", cmd)
                response.append(broker.handle(cmd))
            return {"code": 200, "msg": "Success", "data": response}, 200
        except Exception as e:  # pragma: no cover
            return {"message": str(e)}, 500


approval_blueprint = Blueprint("approvals", __name__, url_prefix="/approvals")


approval_api = Api(approval_blueprint)

approval_api.add_resource(routers.ApprovalResource, "/add_approval")
