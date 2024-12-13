import json

from flasgger import Swagger
from flask import Blueprint, Flask, g, request
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect

from setup import config, sessions
from setup.adapters.cache import RedisCache
from setup.encoders import JsonEncoder
from src.approvals.entrypoints.routers import approval_blueprint
from src.cdc.entrypoints.routers import cdc_blueprint
from src.closed_loans.entrypoints.routers import closed_loans_integration_blueprint
from src.comments_mambu.entrypoints.routers import comments_mambu_blueprint
from src.demos.entrypoints.routers import demo_blueprint
from src.groups.entrypoints.routers import groups_blueprint
from src.loans_status.entrypoints.routers import loans_status_blueprint  # type: ignore
from src.mambu.entrypoints.routers import mambu_integration_blueprint
from src.nip.entrypoints.routers import nip_blueprint
from src.pambu.entrypoints.routers import pambu_blueprint
from src.sepomex.entrypoints.routers import sepomex_blueprint
from src.storage.entrypoints.routers import storage_blueprint
from src.transactions.entrypoints.routers import transactions_blueprint
from src.validations.entrypoints.routers import validations_blueprint

csrf = CSRFProtect()


def create_application(name, env):
    app = Flask(name)
    CORS(app, resources={r"/*": {"origins": config.ORIGINS_CORS}})
    if env not in ["dev", "test"]:
        app.config["SECRET_KEY"] = config.SECRET_KEY
        csrf.init_app(app)
        app.config["WTF_CSRF_CHECK_DEFAULT"] = config.CHECK_CSRF
    app.config["SWAGGER"] = config.SWAGGER
    app.json_encoder = JsonEncoder
    Swagger(app)

    mount_api = Blueprint("", __name__)

    mount_api.register_blueprint(sepomex_blueprint)
    mount_api.register_blueprint(cdc_blueprint)
    mount_api.register_blueprint(nip_blueprint)
    mount_api.register_blueprint(validations_blueprint)
    mount_api.register_blueprint(approval_blueprint)
    mount_api.register_blueprint(loans_status_blueprint)
    mount_api.register_blueprint(mambu_integration_blueprint)
    mount_api.register_blueprint(pambu_blueprint)
    mount_api.register_blueprint(comments_mambu_blueprint)
    mount_api.register_blueprint(closed_loans_integration_blueprint)
    mount_api.register_blueprint(transactions_blueprint)
    mount_api.register_blueprint(storage_blueprint)
    mount_api.register_blueprint(groups_blueprint)

    if env in ["dev", "test"]:
        mount_api.register_blueprint(demo_blueprint)

    app.register_blueprint(mount_api)
    app = config.Logs.config_logs(app, env)

    # key None apply to all request
    app.before_request_funcs = {
        None: [
            load_user,
        ]
    }
    return app


def load_user():
    from flask import current_app as app

    app.logger.info("Get user from redis")
    try:
        token_app = request.headers[config.TOKEN_HEADER]
        user_email = RedisCache.get("user:token:" + str(token_app)).decode("utf-8")
        user_data = json.loads(
            RedisCache.get("user:data:" + str(user_email)).decode("utf-8")
        )
        g.user = sessions.User(user_data["username"], user_data["email"])
        app.logger.info(
            "User requested: username=%s, email=%s",
            user_data["username"],
            user_data["email"],
        )
    except (AttributeError, KeyError):
        app.logger.error("Not user in redis")
        g.user = None
