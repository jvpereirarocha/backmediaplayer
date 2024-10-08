from flask import Flask
from config import envs
from db.mappers import start_mappers


def create_app(environment: str) -> str:
    app = Flask(__name__)
    current_config = envs.get(environment)
    app.config.from_object(current_config)
    app.register_blueprint()
    start_mappers()
    return app