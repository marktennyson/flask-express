import typing as t
import os as os

if t.TYPE_CHECKING:
    from flask_express import FlaskExpress

def test_flash_response(app:"FlaskExpress", client):
    @app.get("/simple-flash")
    def simple_flash(req, res):
        return res.flash("this is the flash message")

    rv = client.get("/simple-flash")
    assert rv.data == b""

def test_end_response(app:"FlaskExpress", client):
    @app.get("/simple-end")
    def simple_end(req, res):
        return res.end()

    @app.get("/customished-end-404")
    def customished_end_404(req, res):
        return res.end(404)

    @app.get("/customished-end-400")
    def customished_end_400(req, res):
        return res.end(400)

    @app.get("/customished-end-403")
    def customished_end_403(req, res):
        return res.end(403)

    @app.get("/customished-end-405")
    def customished_end_405(req, res):
        return res.end(405)

    @app.get("/customished-end-406")
    def customished_end_406(req, res):
        return res.end(406)

    @app.get("/customished-end-408")
    def customished_end_408(req, res):
        return res.end(408)

    @app.get("/customished-end-409")
    def customished_end_409(req, res):
        return res.end(409)

    @app.get("/customished-end-410")
    def customished_end_410(req, res):
        return res.end(410)

    @app.get("/customished-end-411")
    def customished_end_411(req, res):
        return res.end(411)

    rv = client.get("/simple-end")
    rv_404 = client.get("/customished-end-404")
    rv_400 = client.get("/customished-end-400")
    rv_403 = client.get("/customished-end-403")
    rv_405 = client.get("/customished-end-405")
    rv_406 = client.get("/customished-end-406")
    rv_408 = client.get("/customished-end-408")
    rv_409 = client.get("/customished-end-409")
    rv_410 = client.get("/customished-end-410")
    rv_411 = client.get("/customished-end-411")

    assert rv.data == b""

    assert rv_404.data == b'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n<title>404 Not Found</title>\n<h1>Not Found</h1>\n<p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>\n'

    assert rv_400.data == b'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n<title>401 Unauthorized</title>\n<h1>Unauthorized</h1>\n<p>The server could not verify that you are authorized to access the URL requested. You either supplied the wrong credentials (e.g. a bad password), or your browser doesn&#x27;t understand how to supply the credentials required.</p>\n'
    assert rv_403.data == b'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n<title>403 Forbidden</title>\n<h1>Forbidden</h1>\n<p>You don&#x27;t have the permission to access the requested resource. It is either read-protected or not readable by the server.</p>\n'
    assert rv_405.data == b'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n<title>405 Method Not Allowed</title>\n<h1>Method Not Allowed</h1>\n<p>The method is not allowed for the requested URL.</p>\n'
    assert rv_406.data == b'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n<title>406 Not Acceptable</title>\n<h1>Not Acceptable</h1>\n<p>The resource identified by the request is only capable of generating response entities which have content characteristics not acceptable according to the accept headers sent in the request.</p>\n'
    assert rv_408.data == b'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n<title>408 Request Timeout</title>\n<h1>Request Timeout</h1>\n<p>The server closed the network connection because the browser didn&#x27;t finish the request within the specified time.</p>\n'
    assert rv_409.data == b'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n<title>409 Conflict</title>\n<h1>Conflict</h1>\n<p>A conflict happened while processing the request. The resource might have been modified while the request was being processed.</p>\n'
    assert rv_410.data == b'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n<title>410 Gone</title>\n<h1>Gone</h1>\n<p>The requested URL is no longer available on this server and there is no forwarding address. If you followed a link from a foreign page, please contact the author of this page.</p>\n'
    assert rv_411.data == b'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n<title>411 Length Required</title>\n<h1>Length Required</h1>\n<p>A request with this method requires a valid &lt;code&gt;Content-Length&lt;/code&gt; header.</p>\n'

def test_send_response(app, client):
    @app.get("/test-send-str")
    def test_send_str_response(req, res):
        return res.send("OK")

    @app.get("/test-send-dict")
    def test_send_dict_response(req, res):
        return res.send(dict(data="this is data"))

    @app.get("/test-send-list")
    def test_send_list_response(req, res):
        return res.send([1,2,3,4])

    rv_str = client.get("/test-send-str")
    rv_dict = client.get("/test-send-dict")
    rv_list = client.get("/test-send-list")

    assert rv_str.data == b'OK'
    assert rv_dict.data == b'{"data": "this is data"}'
    assert rv_list.data == b'[1, 2, 3, 4]'

def test_json_response(app:"FlaskExpress", client):
    @app.get("/test-json")
    def test_simple_json(req, res):
        return res.json(name="test_simple_json")

    @app.get("/test-json-list")
    def test_json_list(req, res):
        return res.json([1, 2, 3, 4])

    @app.get("/test-json-dict")
    def test_json_dict(req, res):
        return res.json(dict(data="this is data"))

    rv_simple = client.get("/test-json")
    rv_list = client.get("/test-json-list")
    rv_dict = client.get("/test-json-dict")

    assert rv_simple.data == b'{"name": "test_simple_json"}'
    assert rv_list.data == b'[1, 2, 3, 4]'
    assert rv_dict.data == b'{"data": "this is data"}'

def test_set_status_response(app:"FlaskExpress", client):
    @app.get("/test-set-status-201")
    def test_set_status_201_response(req, res):
        return res.set_status(201).end()

    @app.get("/test-set-status-404")
    def test_set_status_404_response(req,res):
        return res.set_status(404).end()

    @app.get("/test-set-status-500")
    def test_set_status_500_response(req,res):
        return res.set_status(500).end()

    @app.get("/test-set-status-403-with-data")
    def test_set_status_403_with_data(req,res):
        return res.set_status(403).send("simple data")

    rv_201 = client.get("/test-set-status-201")
    rv_404 = client.get("/test-set-status-404")
    rv_403 = client.get("/test-set-status-403-with-data")
    rv_500 = client.get("/test-set-status-500")

    assert rv_201.status_code == 201
    assert rv_404.status_code == 404
    assert rv_500.status_code == 500
    
    assert rv_403.status_code == 403
    assert rv_403.data == b'simple data'

def test_render_response(app:"FlaskExpress", client):
    @app.get("/test-raw-html-render")
    def test_raw_html_render(req, res):
        return res.render("<h1>This is the index page</h1>")

    # @app.get("/test-html-file-render")
    # def test_html_file_render(req, res):
    #     return res.render("index.html")

    @app.get("/test-raw-html-render-with-context")
    def test_raw_html_render_with_context(req, res):
        return res.render("<h1>This is the {{index}} page</h1>", index='index.html')

    rv_raw_html = client.get("/test-raw-html-render")
    rv_raw_ctx_html = client.get("/test-raw-html-render-with-context")
    # rv_file_html s= client.get("/test-file-html-render")

    assert rv_raw_html.data == b'<h1>This is the index page</h1>'
    assert rv_raw_ctx_html.data == b"<h1>This is the index.html page</h1>"
    # assert rv_file_html.data == b'<h1>This is the index page</h1>'

def test_attachment_response(app:"FlaskExpress", client):
    @app.get("/test-attachment-response")
    def test_attachment_response(req, res):        
        return res.attachment("index.html")

    rv_test_attachment = client.get("/test-attachment-response")
    assert rv_test_attachment.status_code == 200

def test_get_set_header(app:"FlaskExpress", client):
    @app.get("/test-get-set-header")
    def test_get_set_header(req, res):
        ...