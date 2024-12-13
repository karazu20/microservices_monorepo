from faker import Faker
from flask import Blueprint, jsonify
from flask_restful import Api, Resource

from setup.resources import PodemosResource, PublicResource
from src.demos.entrypoints import routers


class JsonEncoderApi(Resource):
    def get(self):
        fake = Faker()
        some_datetime = fake.date_time()
        some_decimal = fake.pydecimal()
        some_set = {
            1,
            2,
            3,
            4,
            5,
        }

        data = {
            "datetime": some_datetime,
            "decimal": some_decimal,
            "list": some_set,
        }

        return jsonify(data)


class ProtectedApi(PodemosResource):
    def get(self):
        return {}


class PublicApi(PublicResource):
    def get(self):
        return {}


demo_blueprint = Blueprint("demo", __name__, url_prefix="/demo")


demo_api = Api(demo_blueprint)

demo_api.add_resource(routers.JsonEncoderApi, "/json_encoder_test")
demo_api.add_resource(routers.ProtectedApi, "/authenticated")
demo_api.add_resource(routers.PublicApi, "/public")
# demo_api.add_resource(routers.TaskQueue, "/task_queue")
