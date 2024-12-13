from flask import Blueprint, current_app
from flask_restful import Api

from setup.resources import PublicResource


class HealthCheckResource(PublicResource):
    def get(self):
        return {
            "message": "Healthy",
            "version": "0.0.1",
            "blueprints": [blueprint for blueprint in current_app.blueprints.keys()],
        }


healtcheck_blueprint = Blueprint("healtcheck", __name__, url_prefix="/healthcheck")

healtcheck_api = Api(healtcheck_blueprint)

healtcheck_api.add_resource(HealthCheckResource, "/")
