from setup.blueprints import mount_api
from setup.setup_application import create_application
from src.nip.entrypoints.routers import nip_blueprint

app = create_application(__name__, "dev")
mount_api.register_blueprint(nip_blueprint)
app.register_blueprint(mount_api)
