import logging

from flasgger import swag_from
from flask import Blueprint, request
from flask_restful import Api

from setup.resources import PodemosResource
from src.loans_status import broker
from src.loans_status.config import DOCS_PATH_LOAN_STATUS
from src.loans_status.domain import commands, queries
from src.loans_status.entrypoints import routers  # type: ignore

logger = logging.getLogger(__name__)


class LoanStatusResource(PodemosResource):
    def get(self):
        try:
            qry = queries.GetLoanStatus.Schema().load(request.json)  # type: ignore
            logger.info("GetLoanStatus: query %s", qry)
            loans_status = broker.handle(qry)
            return {"code": 200, "data": loans_status, "msg": "Success"}, 200
        except Exception as e:  # pragma: no cover
            return {"message": str(e)}, 500
        return "OK", 200

    @swag_from(f"{DOCS_PATH_LOAN_STATUS}/create_loan_status.yml")
    def post(self):
        try:
            for value in request.json:  # type: ignore
                cmd = commands.ADDLoanStatus.Schema().load(value)  # type: ignore
                logger.info("LoanStatusResource: command %s", cmd)
                broker.handle(cmd)
            return {"code": 201, "data": "OK", "msg": "Success"}, 201
        except Exception as e:
            logger.error("Existió un error al registrar un Estatus de Crédito %s", e)
            return {"message": str(e)}, 500


loans_status_blueprint = Blueprint("loans_status", __name__, url_prefix="/loans_status")


loan_status_api = Api(loans_status_blueprint)

loan_status_api.add_resource(routers.LoanStatusResource, "")
