# Some basic examples of Flask-Express

```python
from flask_express import FlaskExpress
from flask import session, current_app
from flask_express.typing import Request, Response

app = FlaskExpress(__name__)


app.config['SECRET_KEY'] = "this is the secret key."
# app.config['ATTACHMENTS_FOLDER'] = 'templates'

@app.route("/")
async def index(req:Request, res:Response):
    context = dict(name="Aniket sarkar", description="basic demo page.")
    return res.render("index.html", context=context)

@app.route("/set-status")
def set_statuser(req:Request, res:Response):
    # return res.Response(json.dumps({"status":200}), mimetype="application/json")
    return res.send_status(404).send("your requested page is not found.")

@app.route("/mrp")
def mrp(req:Request, res:Response):
    print (current_app.config.get("ATTACHMENTS_FOLDER"))
    res.type("application/json")
    print (res.get("Content-Type"))
    res.set_cookie("cookie_key", 'aniketsarkar')
    print (res.headers)
    print (app.config)
    print (app.config['ATTACHMENTS_FOLDER'])
    return res.attachment("hello.txt") # attachment should be stored in attachment folder.

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
    return res.send(req.header["Accept-Encoding"])

@app.get("/redirect")
def redirector(req:Request, res:Response):
    return res.send_status(308).redirect("https://www.google.com")

@app.get("/set-session")
def set_session(req:Request, res:Response):
    req.session['username'] = 'aniketsarkar'
    return res.send('OK')

@app.get("/get-session")
def get_session(req:Request, res:Response):
    username = req.session.get('username')
    return res.send(dict(username=username))

@app.get("/check-flash")
def check_flash(req:Request, res:Response):
    return res.send_status(403).send(dict(name="test_simple_json"))

@app.get("/check-type")
def check_type(req:Request, res:Response):
    return res.type("json").end()




if __name__ == "__main__":
    app.run(debug=True, port=8080)
```
## Example with flask-admin
#### app.py file
```python
from flask_express import FlaskExpress
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
import typing as t
from models import *

if t.TYPE_CHECKING:
    from flask_express.typing import Request, Response


app = FlaskExpress(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'world-secret-key'

admin = Admin(app, name='microblog', template_mode='bootstrap4')

db.init_app(app)

admin.add_view(ModelView(AgentChangePasswordOtp, db.session))

_ = Migrate(app, db)

@app.get('/')
def index(req:"Request", response:"Response"):
    return response.json(name='index')

@app.get("/index")
def index_2(req:"Request", res:"Response"):
    return res.flash("message").end(404)


if __name__ == '__main__':
    app.run(debug=True)
```
#### models.py file
```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db:"SQLAlchemy" = SQLAlchemy()

class AgentChangePasswordOtp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contactnumber = db.Column(db.String(100))
    otp = db.Column(db.String(100))
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.now())
```