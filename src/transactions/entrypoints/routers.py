import logging

from flask import Blueprint, jsonify, request
from flask_restful import Api

from setup.resources import PodemosResource
from src.transactions import broker
from src.transactions.domain import queries

logger = logging.getLogger(__name__)


class TransactionResource(PodemosResource):
    def get(self):
        try:
            query = queries.GetTransactions.Schema().load(request.args)  # type: ignore
            logger.info("GroupResource: query %s", query)
            transaction = broker.handle(query)
            return jsonify(
                {
                    "code": "TR200",
                    "data": {
                        "transactions": transaction,
                        "msg_success": "Consulta Correcta",
                    },
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


class InstallmentsResource(PodemosResource):
    def get(self):
        try:
            query = queries.GetInstallments.Schema().load(request.args)  # type: ignore
            logger.info("GroupResource: query %s", query)
            installments = broker.handle(query)
            return jsonify(
                {
                    "code": "TR200",
                    "data": {
                        "installments": installments,
                        "msg_success": "Consulta Correcta",
                    },
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


transactions_blueprint = Blueprint(
    "transactions",
    __name__,
    url_prefix="/transactions",
)


transactions_api = Api(transactions_blueprint)

transactions_api.add_resource(TransactionResource, "")
transactions_api.add_resource(InstallmentsResource, "/installments")
