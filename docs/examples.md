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
## Example with flask-admin, flask-sqlalchemy
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

## Example with Flask-Tortoise
**Flask-Tortoise** provides a simple asynchronous ORM service. Here I have tried to add some examples of **Flask-Express** with **Flask-Tortoise**.

#### app.py file
```python
# from flask import jsonify, Flask
from flask_express import FlaskExpress
from models import *
from random import choice
from script import GenerateData

import typing as t

if t.TYPE_CHECKING:
    from flask_express.typing import Request, Response


STATUSES = ["New", "Old", "Gone"]

app:"FlaskExpress" = FlaskExpress(__name__)
app.config['TORTOISE_ORM_DATABASE_URI'] = 'sqlite://db.sqlite3'
app.config['TORTOISE_ORM_MODELS'] = "models"

models.init_app(app)

@app.get("/")
async def list_all(req:"Request", res:"Response"):
    users = await Users.all()
    workers = await Workers.all()
    co_workers = await CoWorker.all()
    return res.json(
        {"users": [str(user) for user in users], "workers": [str(worker) for worker in workers], "co-wrokers": [str(co_worker) for co_worker in co_workers]}
    )


@app.get("/user")
async def add_user(req:"Request", res:"Response", ):
    user = await Users.create(status=choice(STATUSES))  # nosec
    return str(user)


@app.get("/worker")
async def add_worker(req:"Request", res:"Response", ):
    worker = await Workers.create(status=choice(STATUSES))  # nosec
    return str(worker)

@app.get("/get-worker")
async def get_worker(req:"Request", res:"Response", ):
    worker:"Workers" = await Workers.get(id=1)
    return str(worker.status)

@app.get("/co-workers")
async def co_workers(req:"Request", res:"Response", ):
    user = await Users.get(id=1)
    co_worker:"CoWorker" = await CoWorker.create(name="Aniket Sarkar", rltn=user)
    return str(co_worker)

@app.get("/get-coworker/<int:id>")
async def aniket(req:"Request", res:"Response", id):
    pk=id
    co_worker =await CoWorker.get_or_404(pk=pk, description=f"user object not found at ID: {pk}")
    return res.json(name=str(co_worker.name))

@app.get("/delete-coworker/<int:id>")
async def delete_coworker(id):
    c = await CoWorker.get_or_404(id=id)
    await c.delete()
    return "object deleted"

@app.get("/sarkar")
async def sarkar(req:"Request", res:"Response", ):
    user = await Users.filter(pk=1).first_or_404()
    return res.json(name=str(user))

@app.get("/paginate")
async def paginator(req:"Request", res:"Response", ):
    user = await Users.paginate()
    print (user)
    return res.send("none")

@app.get("/create-data")
async def create_data(req:"Request", res:"Response"):
    r1 = await GenerateData.generate_user()
    r2 = await GenerateData.generate_worker()
    r3 = await GenerateData.generate_co_worker()
    return res.send("Done")

@app.get("/create-co-worker")
async def create_co_worker(req:"Request", res:"Response"):
    await GenerateData.generate_co_worker()
    return res.send("Done")

if __name__ == '__main__':
    app.run(debug=True, port=8080)
```

#### models.py file
```python
from flask_tortoise import Tortoise, Manager

models:"Tortoise" = Tortoise()


class Users(models.Model):
    id = models.IntField(pk=True)
    status = models.CharField(20)
    # name = fields.CharField(20, null=True)

    def __str__(self):
        return f"User {self.id}: {self.status}"
    class Meta:
        manager = Manager()


class Workers(models.Model):
    id = models.IntField(pk=True)
    status = models.CharField(20)

    def __str__(self):
        return f"Worker {self.id}: {self.status}"

    class Meta:
        manager = Manager()

class CoWorker(models.Model):
    id = models.IntField(pk=True)
    name = models.CharField(max_length=255)
    rltn = models.ForeignKeyField(f"models.Users", on_delete=models.CASCADE)
    created_at = models.DatetimeField(auto_now_add=True)

    class Meta:
        manager = Manager()

    def __str__(self):
        return f"Co-Worker {self.id}: {self.name}"
```