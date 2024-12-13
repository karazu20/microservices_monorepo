from flask import Blueprint

from setup import config

mount_api = Blueprint("alejandria", __name__, url_prefix=config.APPLICATION_ROOT)
