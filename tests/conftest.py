import flask_express as fe
import pytest

import typing as t

if t.TYPE_CHECKING:
    from flask.testing import FlaskClient

@pytest.fixture
def app() -> "fe.FlaskExpress":
    app = fe.FlaskExpress(__name__)
    app.secret_key = "top-secret-key"
    app.testing = True
    return app


@pytest.fixture
def client(app:"fe.FlaskExpress") -> "FlaskClient":
    return app.test_client()