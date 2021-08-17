from flask.wrappers import Request as RequestBase
from flask.globals import session
import typing as t
from .munch import Munch


if t.TYPE_CHECKING:
    from munch import Munch

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
    def session(self):
        """
        it provides you the default session object of flask globals.
        """
        return session