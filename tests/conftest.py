import os
from os.path import dirname, join
import tempfile

import pytest

from wallet_api import create_app
from wallet_api.db import get_db, init_db


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app(
        {
            "TESTING": True,
            "DATABASE": db_path,
        }
    )

    with app.app_context():
        # Create and initialise a database with preconfigured test data for the
        # unit tests.
        init_db()
        with open(join(dirname(__file__), "test_data.sql"), "rb") as f:
            sql = f.read().decode("utf8")
        get_db().executescript(sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
