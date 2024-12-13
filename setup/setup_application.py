from flasgger import Swagger
from flask import Flask
from flask_wtf.csrf import CSRFProtect

from setup import config
from setup.encoders import JsonEncoder

csrf = CSRFProtect()


def create_application(name, env):
    app = Flask(name)
    if env not in ["dev", "test"]:
        app.config["SECRET_KEY"] = config.SECRET_KEY
        csrf.init_app(app)
    app.config["SWAGGER"] = config.SWAGGER
    app.json_encoder = JsonEncoder
    Swagger(app)
    app = config.Logs.config_logs(app, env)
    return app
