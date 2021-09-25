import flask_express as fe
import pytest as pt
import os

import typing as t

if t.TYPE_CHECKING:
    from flask.testing import FlaskClient

@pt.fixture
def app() -> "fe.FlaskExpress":
    app = fe.FlaskExpress(__name__)
    app.secret_key = "top-secret-key"
    app.testing = True
    app.template_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'files')
    app.config['ATTACHMENTS_FOLDER'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'files')
    return app


@pt.fixture
def client(app:"fe.FlaskExpress") -> "FlaskClient":
    return app.test_client()