from setup.blueprints import mount_api
from setup.setup_application import create_application
from shared.healtcheck.entrypoints.routers import healtcheck_blueprint
from src.closed_loans.entrypoints.routers import closed_loans_integration_blueprint

app = create_application(__name__, "dev")
closed_loans_integration_blueprint.register_blueprint(healtcheck_blueprint)
mount_api.register_blueprint(closed_loans_integration_blueprint)
app.register_blueprint(mount_api)
