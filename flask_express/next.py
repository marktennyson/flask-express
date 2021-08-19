import typing as t
from flask.globals import current_app

if t.TYPE_CHECKING is True:
    from .typing import Request, Response

class Next:
    def __init__(self,req:"Request", res:"Response", next):
        ...

    def _app_before_request(self):
        current_app.before_request_funcs\
                .setdefault(None, [])\
                    .append(mw_class._before_request)

    def __call__(self):
        ...