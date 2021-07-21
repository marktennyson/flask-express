# from flask.ctx import has_request_context
from flask.wrappers import Request as RequestBase
from flask.globals import session
import typing as t
from munch import munchify

if t.TYPE_CHECKING:
    from munch import Munch


class Request(RequestBase):

    def __init__(self, *wargs, **kwargs) -> None:
        super(Request, self).__init__(*wargs, **kwargs)

    @property
    def json(self) ->t.Type["Munch"]:
        return munchify(self.get_json())

    @property
    def query(self) ->t.Type["Munch"]:
        return munchify(self.args)

    @property
    def body(self) ->t.Type["Munch"]:
        return munchify(self.form)

    @property
    def session():
        return session