import flask_express as fe
import pytest


@pytest.fixture
def app():
    app = fe.FlaskExpress(__name__)
    app.secret_key = "top-secret-key"
    app.testing = True
    return app


@pytest.fixture
def client(app:"fe.FlaskExpress"):
    return app.test_client()