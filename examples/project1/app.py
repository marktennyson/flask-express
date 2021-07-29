from flaske import Flask, current_app, session
from flaske.typing import Request, Response

app = Flask(__name__)
app.config['SECRET_KEY'] = "this is the secret key."

@app.route("/")
async def index(req:Request, res:Response):
    context = dict(name="Aniket sarkar", description="basic demo page.")
    return res.render("index.html", context=context)

@app.route("/set-status")
def set_statuser(req:Request, res:Response):
    # return res.Response(json.dumps({"status":200}), mimetype="application/json")
    return res.set_status(404).send("your requested page is not found.")

@app.route("/mrp")
def mrp(req:Request, res:Response):
    # resp = make_response("file resp")
    # print (res.headers)
    # print (current_app.config.get("ATTACHMENTS_FOLDER"))
    res.type("application/json")
    print (res.get("Content-Type"))
    res.set_cookie("cookie_key", 'aniketsarkar')
    print (res.headers)
    return res.json(id=1)
    # return res.attachment("golang.png")

@app.route("/check-session")
def check_session(req:Request, res:Response):
    ss = dict(session)
    # print (ss)
    ss['name1'] = 'aniket'
    # session['name'] = "aniket"
    print (ss)
    return res.send("data")

@app.route("/check-session-2/")
def check_session_2(req:Request, res:Response):
    print (req.session)
    return res.send("data2")

@app.get("/check-query-params/")
def check_query_params(req:Request, res:Response):
    res.json(req.query)

@app.get("/check-headers/")
def check_headers(req:Request, res:Response):
    return res.send(req.header['Accept-Encoding'])

@app.get("/redirect")
def redirector(req:Request, res:Response):
    return res.set_status(308).redirect("https://www.google.com")

@app.get("/set-session")
def set_session(req:Request, res:Response):
    req.session['username'] = 'aniketsarkar'
    return res.send('OK')

@app.get("/get-session")
def get_session(req:Request, res:Response):
    username = req.session.get('username')
    return res.send(dict(username=username))

if __name__ == "__main__":
    app.listen(debug=True, port=8080)