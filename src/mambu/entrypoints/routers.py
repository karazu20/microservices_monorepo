import logging

from flask import Blueprint, jsonify, request
from flask_restful import Api

from setup.resources import PodemosResource
from src.mambu import broker
from src.mambu.domain import queries

logger = logging.getLogger(__name__)


class GroupResource(PodemosResource):
    def get(self):
        try:
            query = queries.GetGroup.Schema().load(request.args)  # type: ignore
            logger.info("GroupResource: query %s", query)
            group = broker.handle(query)
            return jsonify(group)
        except Exception as e:  # pragma: no cover
            return {"message": str(e)}, 500


class ClientResource(PodemosResource):
    def get(self):
        try:
            query = queries.GetClient.Schema().load(request.args)  # type: ignore
            logger.info("ClientResource: query %s", query)
            client = broker.handle(query)
            return jsonify(client)
        except Exception as e:  # pragma: no cover
            return {"message": str(e)}, 500


class LoanResource(PodemosResource):
    def get(self):
        try:
            query = queries.GetLoan.Schema().load(request.args)  # type: ignore
            logger.info("LoanResource: query %s", query)
            loan = broker.handle(query)
            return jsonify(loan)
        except Exception as e:  # pragma: no cover
            return {"message": str(e)}, 500


class ClientIdResource(PodemosResource):
    def get(self, id):
        try:
            query = queries.GetClientId(id=id)  # type: ignore
            logger.info("ClientIdResource: query %s", query)
            client = broker.handle(query)
            return jsonify(client)
        except Exception as e:  # pragma: no cover
            return {"message": str(e)}, 500


class LoanIdResource(PodemosResource):
    def get(self, id):
        try:
            query = queries.GetLoanId(id=id)  # type: ignore
            logger.info("LoanIdResource: query %s", query)
            loan = broker.handle(query)
            return jsonify(loan)
        except Exception as e:  # pragma: no cover
            return {"message": str(e)}, 500


class GroupIdResource(PodemosResource):
    def get(self, id):
        try:
            query = queries.GetGroupId(id=id)  # type: ignore
            logger.info("GroupIdResource: query %s", query)
            group = broker.handle(query)
            return jsonify(group)
        except Exception as e:  # pragma: no cover
            return {"message": str(e)}, 500


mambu_integration_blueprint = Blueprint(
    "mambu",
    __name__,
    url_prefix="/mambu",
)


podemos_mambu_api = Api(mambu_integration_blueprint)

podemos_mambu_api.add_resource(GroupResource, "/groups")
podemos_mambu_api.add_resource(ClientResource, "/clients")
podemos_mambu_api.add_resource(LoanResource, "/loans")
podemos_mambu_api.add_resource(ClientIdResource, "/clients/<string:id>")
podemos_mambu_api.add_resource(LoanIdResource, "/loans/<string:id>")
podemos_mambu_api.add_resource(GroupIdResource, "/groups/<string:id>")
