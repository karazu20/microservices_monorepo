import os

from dotenv import load_dotenv

from src.application import create_application

load_dotenv()
env = os.environ.get("ENV", "prod")
app = create_application(__name__, env)
