from setup.blueprints import mount_api
from setup.setup_application import create_application
from shared.healtcheck.entrypoints.routers import healtcheck_blueprint
from src.loans_status.entrypoints.routers import loans_status_blueprint

app = create_application(__name__, "dev")
loans_status_blueprint.register_blueprint(healtcheck_blueprint)
mount_api.register_blueprint(loans_status_blueprint)
app.register_blueprint(mount_api)
