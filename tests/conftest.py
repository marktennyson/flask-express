import flask
import pytest


@pytest.fixture
def app(request):
    app = flask.Flask(request.module.__name__)
    app.testing = True
    return app