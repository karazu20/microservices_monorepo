import logging

from flasgger import swag_from
from flask import Blueprint, request
from flask_restful import Api

from setup.resources import PodemosResource
from src.comments_mambu import broker
from src.comments_mambu.config import DOCS_PATH_COMMENTS
from src.comments_mambu.domain import commands, queries
from src.comments_mambu.entrypoints import routers

logger = logging.getLogger(__name__)


class LoanCommentResource(PodemosResource):
    def get(self):
        try:
            qry = queries.GetLoanComments.Schema().load(request.args)  # type: ignore
            logger.info("GetLoanComments: query %s", qry)
            comments = broker.handle(qry)
            return {"code": 200, "msg": "Success", "data": comments}, 200
        except Exception as e:  # pragma: no cover
            return {"message": str(e)}, 500

    @swag_from(f"{DOCS_PATH_COMMENTS}/create_comment.yml")
    def post(self):
        try:
            cmd = commands.ADDCommentLoan.Schema().load(request.json)  # type: ignore
            logger.info("ADDCommentLoan Resource: query %s", cmd)
            response = broker.handle(cmd)

            if response["status"]:
                return {"code": 201, "msg": "Success", "data": response}, 201

            return {"code": 500, "msg": "Fail", "data": response}, 500
        except Exception as e:  # pragma: no cover
            return {"message": str(e)}, 500


class GroupCommentResource(PodemosResource):
    def get(self):
        try:
            qry = queries.GetGroupComments.Schema().load(request.args)  # type: ignore
            logger.info("GetGroupComments: query %s", qry)
            comments = broker.handle(qry)
            return {"code": 200, "msg": "Success", "data": comments}, 200
        except Exception as e:  # pragma: no cover
            return {"message": str(e)}, 500

    @swag_from(f"{DOCS_PATH_COMMENTS}/create_comment.yml")
    def post(self):
        try:
            cmd = commands.ADDCommentGroup.Schema().load(request.json)  # type: ignore
            logger.info("ADDCommentGroup Resource: query %s", cmd)
            response = broker.handle(cmd)

            if response["status"]:
                return {"code": 201, "msg": "Success", "data": response}, 201

            return {"code": 500, "msg": "Fail", "data": response}, 500
        except Exception as e:  # pragma: no cover
            return {"message": str(e)}, 500


class ClientCommentResource(PodemosResource):
    def get(self):
        try:
            qry = queries.GetClientComments.Schema().load(request.args)  # type: ignore
            logger.info("GetClientComments: query %s", qry)
            comments = broker.handle(qry)
            return {"code": 200, "msg": "Success", "data": comments}, 200
        except Exception as e:  # pragma: no cover
            return {"message": str(e)}, 500

    @swag_from(f"{DOCS_PATH_COMMENTS}/create_comment.yml")
    def post(self):
        try:
            cmd = commands.ADDCommentClient.Schema().load(request.json)  # type: ignore
            logger.info("ADDCommentClient Resource: query %s", cmd)
            response = broker.handle(cmd)

            if response["status"]:
                return {"code": 201, "msg": "Success", "data": response}, 201

            return {"code": 500, "msg": "Fail", "data": response}, 500
        except Exception as e:  # pragma: no cover
            return {"message": str(e)}, 500


comments_mambu_blueprint = Blueprint(
    "comments_mambu", __name__, url_prefix="/comments_mambu"
)


comments_mambu_api = Api(comments_mambu_blueprint)

comments_mambu_api.add_resource(routers.LoanCommentResource, "/loan")
comments_mambu_api.add_resource(routers.GroupCommentResource, "/group")
comments_mambu_api.add_resource(routers.ClientCommentResource, "/client")
