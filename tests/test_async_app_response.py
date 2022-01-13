import pytest as pt

import typing as t

if t.TYPE_CHECKING:
    from flask_express import FlaskExpress


def test_asend_response(app, client):
    @app.get("/test-send-str")
    async def test_send_str_response(req, res):
        return res.send("OK")

    @app.get("/test-send-dict")
    async def test_send_dict_response(req, res):
        return res.send(dict(data="this is data"))

    @app.get("/test-send-list")
    async def test_send_list_response(req, res):
        return res.send([1,2,3,4])

    rv_str = client.get("/test-send-str")
    rv_dict = client.get("/test-send-dict")
    rv_list = client.get("/test-send-list")

    assert rv_str.data == b'OK'
    assert rv_dict.data == b'{"data": "this is data"}'
    assert rv_list.data == b'[1, 2, 3, 4]'