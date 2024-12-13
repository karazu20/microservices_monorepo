from setup.blueprints import mount_api
from setup.setup_application import create_application
from shared.healtcheck.entrypoints.routers import healtcheck_blueprint
from src.validations.entrypoints.routers import validations_blueprint

app = create_application(__name__, "dev")
validations_blueprint.register_blueprint(healtcheck_blueprint)
mount_api.register_blueprint(validations_blueprint)
app.register_blueprint(mount_api)
