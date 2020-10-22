from os import makedirs
from os.path import join
from typing import Union

from flask import Flask

from wallet_api.db import init_app
from wallet_api.api import bp


def create_app(test_config: Union[dict, None] = None) -> Flask:
    """Create the Flask application"""
    app = Flask(__name__, instance_relative_config=True)
    database_path = join(app.instance_path, "wallet.sqlite")
    app.config.from_mapping(SECRET_KEY="S3CR3T", DATABASE=database_path)

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    makedirs(app.instance_path, exist_ok=True)

    init_app(app)

    app.register_blueprint(bp)

    app.logger.info("Wallet API Server Started Up")

    return app
