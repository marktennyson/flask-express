
import typing as t

if t.TYPE_CHECKING:
    from flask_express import FlaskExpress
    from flask.testing import FlaskClient
    from flask_express.typing import Request, Response


def test_json_request(app:"FlaskExpress", client:"FlaskClient"):
    @app.post("/test-json-request")
    def test_json_request(req:"Request", res:"Response"):
        assert req.json.name == "Aniket Sarkar"
        assert req.json.planet == "Pluto"
        return res.json(status=1)

    rv_test_json = client.post('/test-json-request', json=dict(name="Aniket Sarkar", planet="Pluto"))
    assert rv_test_json.status_code == 200
    assert rv_test_json.data == b'{"status": 1}'
    

def test_queryargs_request(app:"FlaskExpress", client:"FlaskClient"):
    @app.get("/test-query-request")
    def test_queryargs_request(req:"Request", res:"Response"):
        assert req.query.name == "Aniket Sarkar"
        assert req.query.plannet == "Pluto"
        return res.json(status=1)

    rv_test_json = client.get('/test-query-request?name=Aniket Sarkar&plannet=Pluto')
    assert rv_test_json.status_code == 200
    assert rv_test_json.data == b'{"status": 1}'

def test_set_get_session_func(app:"FlaskExpress", client:"FlaskClient"):
    @app.get("/test-set-get-session-request")
    def set_get_session_request(req:"Request", res:"Response"):
        req.set_session("username", "expo_9071")
        assert req.session.get("username") == "expo_9071"
        assert req.get_session("username") == "expo_9071"
        return res.json(username=req.get_session("username"))

    rv_test_json = client.get('/test-set-get-session-request')
    assert rv_test_json.status_code == 200
    assert rv_test_json.data == b'{"username": "expo_9071"}'