from flask.wrappers import Request as RequestBase
from flask.globals import session
import typing as t
from .munch import Munch

if t.TYPE_CHECKING:
    from flask.sessions import SessionMixin


if t.TYPE_CHECKING:
    from munch import Munch

class Request(RequestBase):
    """
    The default response class for the flaske app.
    """
    def __init__(self, *wargs, **kwargs) -> None:
        super(Request, self).__init__(*wargs, **kwargs)

    @property
    def json(self) -> t.Type["Munch"]:
        """
        it provides you the json based data. 

        :for example::

            @app.post("/get-json")
            def get_json(req, res):
                username = req.json.username
                password = req.json.password
                return res.json(username=username, password=password)
        """
        return Munch(self.get_json())

    @property
    def query(self) -> t.Type["Munch"]:
        """
        it provides you the args based data. 

        :for example::

            @app.get("/get-query")
            def get_json(req, res):
                username = req.query.username
                password = req.query.password
                return res.json(username=username, password=password)
        """
        return Munch(self.args)

    @property
    def body(self) -> t.Type["Munch"]:
        """
        it provides you the form based data. 

        :for example::

            @app.post("/get-body")
            def get_json(req, res):
                username = req.body.username
                password = req.body.password
                return res.json(username=username, password=password)
        """
        return Munch(self.form)

    @property
    def header(self) -> t.Type["Munch"]:
        """
        it provides you the headers based data. 

        :for example::

            @app.get("/get-body")
            def get_json(req, res):
                return res.json(req.header)
        """
        return Munch(self.headers)

    @property
    def session(self) -> "SessionMixin":
        """
        it provides you the default session object of flask globals.
        :for example::

            @app.get("/set-session")
            def set_session(req, res):
                req.session['username'] = 'aniketsarkar'
                return res.send('OK')

            @app.get("/get-session")
            def get_session(req, res):
                username = req.session.get('username')
                return res.send(dict(username=username))
        """
        return session