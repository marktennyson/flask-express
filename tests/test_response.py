from flask_express.response import Response
import typing as t

if t.TYPE_CHECKING:
    from flask_express import FlaskExpress

def test_flash_response(app:"FlaskExpress", client):
    ...
