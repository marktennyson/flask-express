
import typing as t

if t.TYPE_CHECKING:
    from flask_express import FlaskExpress


def test_json_request(app:"FlaskExpress", client):
    @app.get("/test-json-request")
    def test_json_request(req, res):
        ...