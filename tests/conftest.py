import flask_express as fe
import pytest as pt
import os

import typing as t

if t.TYPE_CHECKING:
    from flask.testing import FlaskClient
    from flask_express.response import Response

BASE_DIR:str = os.path.abspath(os.path.dirname(__file__))

@pt.fixture
def app() -> "fe.FlaskExpress":
    app = fe.FlaskExpress(__name__)
    app.secret_key = "top-secret-key"
    app.testing = True
    app.template_folder = os.path.join(BASE_DIR, 'files')
    app.config['ATTACHMENTS_FOLDER'] = os.path.join(BASE_DIR, 'files')
    return app


@pt.fixture
def client(app:"fe.FlaskExpress") -> "FlaskClient":
    return app.test_client()

# @pt.fixture
# def response(app:"fe.FlaskExpress") -> "Response":
#     return 