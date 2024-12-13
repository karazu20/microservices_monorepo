import logging

from flask import Blueprint, jsonify, request
from flask_restful import Api

from setup.resources import PodemosResource
from src.closed_loans import broker
from src.closed_loans.domain import queries

logger = logging.getLogger(__name__)


class ClosedLoansResource(PodemosResource):
    def get(self):
        try:
            query = queries.GetClosedLoans.Schema().load(request.args)  # type: ignore
            logger.info("GroupResource: query %s", query)
            group = broker.handle(query)
            return jsonify(
                {
                    "code": "CL200",
                    "data": {"closed_loans": group, "msg_success": "Consulta Correcta"},
                    "msg": "success",
                }
            )
        except Exception as e:
            logger.exception(
                "Existio un error al obtener los créditos cerrados %s : %s",
                str(e),
                request.args,
            )
            return {
                "code": "CL500",
                "error": {
                    "error": str(e),
                    "msg_error": "Ocurrió un error vuelve a intentarlo",
                },
                "msg": "fail",
            }, 500


closed_loans_integration_blueprint = Blueprint(
    "closed_loans",
    __name__,
    url_prefix="/closed_loans",
)


closed_loans_api = Api(closed_loans_integration_blueprint)

closed_loans_api.add_resource(ClosedLoansResource, "/groups")
