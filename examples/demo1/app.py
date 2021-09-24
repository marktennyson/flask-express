from flask_express import FlaskExpress
from flask_admin import Admin
# from flask import Flask
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
import typing as t
from models import *

if t.TYPE_CHECKING:
    from flask_express.typing import Request, Response


app = FlaskExpress(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'key'

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