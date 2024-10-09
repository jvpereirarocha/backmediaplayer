from flask import Flask
from config import envs
from db.session import close_db_session
from dotenv import load_dotenv
from app.routes import api


def create_app(environment: str) -> str:
    app = Flask(__name__)
    current_config = envs.get(environment)
    app.config.from_object(current_config)
    app.register_blueprint(api)
    load_dotenv()

    @app.teardown_appcontext
    def teardown(exc):
        return close_db_session()

    return app