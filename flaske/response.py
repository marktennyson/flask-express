from flask import json, redirect, flash
from json.decoder import JSONDecodeError
from flask.wrappers import Response as ResponseBase
from flask.templating import (render_template, 
                    render_template_string
                    )
import typing as t
from munch import Munch
from werkzeug.exceptions import *

ERROR_DICT:dict = {
            400 : Unauthorized,
            403 : Forbidden,
            404 : NotFound,
            405 : MethodNotAllowed,
            406 : NotAcceptable,
            408 : RequestTimeout,
            409 : Conflict,
            410 : Gone,
            411 : LengthRequired,
            412 : PreconditionFailed,
            413 : RequestEntityTooLarge,
            414 : RequestURITooLarge,
            415 : UnsupportedMediaType,
            416 : RequestedRangeNotSatisfiable,
            417 : ExpectationFailed,
            418 : ImATeapot,
            422 : UnprocessableEntity,
            423 : Locked,
            424 : FailedDependency,
            428 : PreconditionRequired,
            429 : TooManyRequests,
            431 : RequestHeaderFieldsTooLarge,
            451 : UnavailableForLegalReasons,
            500 : InternalServerError,
            501 : NotImplemented,
            502 : BadGateway,
            503 : ServiceUnavailable,
            504 : GatewayTimeout,
            505 : HTTPVersionNotSupported,
}


class Response(ResponseBase):
    """
    The default response class for navycut app.
    """
    def __init__(self, *wargs, **kwargs):
        self.status_code = 200

        super(Response, self).__init__(*wargs, **kwargs)

    def flash(self, message:str, category:str="info") -> t.Type["Response"]:
        """
        to flash a message.

        :param message: the message to flash.
        :param category: the category of flash message. Default is "info".
        for example::

            @app.route('/flash')
            def flasher(req, res):
                return res.flash("this is the flash message").end()
        """
        flash(message, category=category)
        return self

    def send(self, content:t.Union[str, dict, t.List[t.Any]]) -> t.Type[ResponseBase]:
        """
        Sends the HTTP response.

        :param content: the content to send.
        for example::

            @app.route("/send")
            def sender(req, res):
                return res.send("hello world")
                #or
                return res.send("<h1>hello world</h1>")
                #or
                return res.set_status(404).send("not found")
        """
        
        if isinstance(content, (dict, list)):
            return self.json(content)

        if isinstance(content, Munch): # for munch object.
            return self.json(content.toDict())

        try:
            _ = json.loads(content)
            return self.json(content)

        except JSONDecodeError:
            return self(content, status_code=self.status_code)

        except Exception as e:
            raise TypeError("provided data type is not supported for `send` function.")

    def json(self, *wargs:t.Any, **kwargs:t.Any) -> ResponseBase:
        """
        return the json seriliazed data.

        :param wargs: dict or list type value.
        :param kwargs: kwargs type value. it will create 
        a dictionary with the provided values of kwargs.
        for example::

            @app.route("/json")
            def jsoner(req, res):
                return res.json(name="aniket sarkar")
                #or
                return res.json({'name': 'aniket sarkar'})
                #or
                return res.json([1,2,3,4])
        """
        data:str = json.dumps(dict())
        
        if len(wargs):
            try:
                data:str = json.dumps(wargs[0])
            
            except TypeError:
                if hasattr(wargs[0], 'toDict'):
                    data:str = json.dumps(wargs[0].to_dict())
                
                else:
                    raise TypeError
            
            except Exception as e:
                raise ValueError(e)

        else:
            if kwargs is not None:
                data:str = json.dumps(kwargs)

        return ResponseBase(data, mimetype="application/json", status=self.status_code)

    def end(self, code:int=None):
        """
        end the current resonse process.
        :param code: provide the web error code, 
        if you want to close this response with a http error.
        for example::

            @app.route("/end")
            def ender(req, res):
                return res.end()
                #or
                return res.end(404) # to raise a 404 error.
        """
        if code is not None and code in ERROR_DICT:
            self.set_status(code)

        else:
            return ResponseBase("", status=self.status_code)

    def set_status(self, code:int) -> t.Optional["Response"]:
        
        if code in ERROR_DICT:
            raise ERROR_DICT.get(code)
        
        else:
            self.status_code = code
            return self

    def render(self, *wargs:t.Any, **context:t.Any) -> t.Type[str]:

        if not len(wargs):
            raise ValueError("atleast 1 argument is required for render method.")

        if len(wargs) > 1 and not isinstance(wargs[1], dict): 
            raise TypeError(wargs[1], "template rendering", "dict")
    
        if len(wargs) > 1 and isinstance(wargs[1], dict):
            context.update(wargs[1])
    
        if isinstance(wargs[0], str):
            if not wargs[0].endswith(".html") and not wargs[0].endswith(".htm"):
                return render_template_string(wargs[0], **context), self.status_code
        
            else: 
                return render_template(wargs[0], **context), self.status_code

    def redirect(self, route:str):
        """
        redirect to specified route.
        
        :param route:
            str based value, the default 
            path where you want to redirect.

        example::

            def login(req, res):
                #if login success
                return res.redirect("/dashboard")
        """
        return redirect(route)