from flask.wrappers import Request as RequestBase
from flask.globals import session
import typing as t
from .munch import Munch


if t.TYPE_CHECKING:
    from munch import Munch
    from flask.sessions import SessionMixin

class Request(RequestBase):
    """
    The default response class for the flask-express app.
    """
    def __init__(self, *wargs, **kwargs) -> None:
        super(Request, self).__init__(*wargs, **kwargs)

    @property
    def json(self) -> t.Type["Munch"]:
        """
        it provides you the json based data. 
        """
        return Munch(self.get_json())

    @property
    def query(self) -> t.Type["Munch"]:
        """
        it provides you the args based data. 
        """
        return Munch(self.args)

    @property
    def body(self) -> t.Type["Munch"]:
        """
        it provides you the form based data. 
        """
        return Munch(self.form)

    @property
    def header(self) -> t.Type["Munch"]:
        """
        it provides you the headers based data. 
        """
        return Munch(self.headers)

    @property
    def session(self) -> t.Type["SessionMixin"]:
        """
        it provides you the default session object of flask 
        globals as a property of `request.Request` class.
        """
        return session

    def set_session(self, key:t.Any, value:t.Any) -> "SessionMixin":
        """
        set the session object by providing the kay value name.

        added in version 1.0.4

        for example::

            @app.route('/set-session') 
            def ss(req, res):
                req.set_session('name', 'aniket')
                return res.send("OK)
        """
        session[key] = value

        return session

    def set_sessions(self, key_value:t.Tuple[t.Any, t.Any]) -> "SessionMixin":
        """
        set multiple sessions at a same time 
        by sending the key, value pair in a tuple.

        added in version 1.0.4

        for example::

            @app.get("/set-sessions")
            def sss(req, res):
                req.set_sessions(('name_1', 'aniket'), ('name_2', 'sarkar'))
                return res.send('OK')
        """
        for item in key_value:
            self.set_session(item)

        return session

    def get_session(self, key:t.Any) -> t.Optional[t.Any]:
        """
        get the session value as per the provided key name.

        added in version 1.0.4

        for example::

            @app.route('/get-session') 
            def gs(req, res):
                req.get_session('name')
                return res.send("OK)
        """
        return session.get(key, None)