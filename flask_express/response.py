from flask import (json, 
            redirect as redirector, 
            flash, 
            send_file as file_sender, 
            request,
            send_from_directory
            )
from json.decoder import JSONDecodeError
from flask.wrappers import Response as ResponseBase
from flask.templating import (render_template, 
                    render_template_string
                    )
import typing as t
from munch import Munch
from werkzeug.exceptions import *
from flask import current_app
from werkzeug.datastructures import Headers


if t.TYPE_CHECKING:
    from http import HTTPStatus
    from datetime import (datetime, 
                        timedelta
                        )
    from os import PathLike

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
    The default response class for flask-express app.
    """
    status_code = 200

    def __init__(self, *wargs, **kwargs):

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

    def send(self, content:t.Union[str, dict, t.List[t.Any]]) -> t.Type["Response"]:
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
            return self.make_response(content)

        except Exception as e:
            raise TypeError("provided data type is not supported for `send` function.")

    def json(self, *wargs:t.Any, **kwargs:t.Any) -> "Response":
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

        return self.make_response(data, mimetype="application/json")
    
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
            raise ERROR_DICT[code]

        else:
            return self.make_response("")

    def set_status(self, code:int) -> t.Type["Response"]:
        """
        set the web response status code.
        :param code: 
            The web response status.
        :for example::

            @app.route("/set-status")
            def set_statuser(req, res):
                return res.set_status(404).send("your requested page is not found.")
        """
        self.status_code = code
        return self

    def render(self, template_or_raw:str, *wargs:t.Any, **context:t.Any) -> t.Type[str]:
        """
        Renders a html and sends the rendered HTML string to the client.

        :param template_or_raw: 
            provide the template name or the html string to be rendered.

        :param wargs: 
            The dictionary type context for the jinja2 template.

        :param context: 
            the kwargs type context for the jinja2 template.

        :for example::

            @app.route('/render')
            def renderer(req, res):
                context=dict(name="Aniket Sarkar", planet="Pluto")
                return res.render("index.html", context)
                #or
                return res.render("index.html", name="Aniket Sarkar", planet="Pluto")
        """
        if len(wargs) and not isinstance(wargs[0], dict): 
            raise TypeError(f"for template context a dict type data is required. got: {type(wargs[1]).__name__}")
    
        if len(wargs) and isinstance(wargs[0], dict):
            context.update(wargs[0])
    
        if not template_or_raw.endswith(".html") and not template_or_raw.endswith(".htm"):
            return self.make_response(render_template_string(template_or_raw, **context))
    
        else: 
            return self.make_response(render_template(template_or_raw, **context))

    def redirect(self, route:str):
        """
        redirect to specified route.
        
        :param route:
            str based value, the default 
            path where you want to redirect.

        example::
            @app.post("/login")
            def login(req, res):
                #if login success
                return res.redirect("/dashboard")
        """
        return redirector(route)


    def get(self,key:str) -> str:
        """
        get the response headers.
        
        :param key:
            the key to get the headers from response.

        :for example::

            @app.route("/get")
            def getter(req, res):
                print (res.get("Content-Type"))
                return res.end()
        """
        return self.headers.get(key, None)

    def set(self, *wargs):
        """
        set the default header.

        :param wargs: 
            dictionary or Headers type data.

        :for example::

            @app.route("/header-seter")
            def header_setter(req, res):
                res.set('Content-Type', 'application/json')
                #or
                res.set({'Content-Type':'application/json'})
                return res.end()
        """
        if not len(wargs):
            raise ValueError("Atleast one argument must be provided")

        if len(wargs) == 1:
            if not isinstance(wargs[0], (dict, Headers)):
                raise TypeError(f"only dict or Headers type data is supported. Got: {type(wargs).__name__}")

            else:
                self.headers.update(wargs[0])
                return self

        if len(wargs) > 1:
            _headers = {wargs[0]: wargs[1]}
            self.headers.update(_headers)

        return self

    def type(self, type:str):
        """
        Sets the Content-Type HTTP header to the 
        MIME type as determined by the specified type.

        :param type:
            The desired mine type to set.

        :for example::

            @app.route("/set-mime")
            def mimer(req, res):
                res.type('application/json')
                #or
                res.type(".html")
                #or
                res.type("json")
        """
        _mimetype:t.Optional[str] = None
        if "/" in type:
            _mimetype = type
        else:
            if not type.startswith("."):
                _mimetype = f"file.{type}"
            else:
                _mimetype = f"file{type}"

        return self.set('Content-Type', _mimetype)

    def attachment(self, file_name:str):
        """
        send the attachments by using this method.
        The default attachment folder name is `attachments`.
        You can always change it by changing the config parameter.
        the config parameter is `ATTACHMENTS_FOLDER`.

        :param file_name:
            the file you want to server as attachment.

        :for example::

            @app.route('/attachments')
            def attach(req, res):
                filename = req.query.filename
                return res.attachment(file_name)
        """
        return send_from_directory(current_app.config['ATTACHMENTS_FOLDER'], 
                    file_name, 
                    as_attachment=True), self.status_code

    def send_file(self,
            path_or_file: t.Union["PathLike", str, t.BinaryIO],
            mimetype: t.Optional[str] = None,
            as_attachment: bool = False,
            download_name: t.Optional[str] = None,
            attachment_filename: t.Optional[str] = None,
            conditional: bool = True,
            etag: t.Union[bool, str] = True,
            add_etags: t.Optional[bool] = None,
            last_modified: t.Optional[t.Union["datetime", int, float]] = None,
            max_age: t.Optional[
                t.Union[int, t.Callable[[t.Optional[str]], t.Optional[int]]]
            ] = None,
            cache_timeout: t.Optional[int] = None
            ) -> t.Type["Response"]:
        """
        Send the contents of a file to the client.
        Its internally using the send_file method from werkzeug.

        :param path_or_file: The path to the file to send, relative to the
        current working directory if a relative path is given.
        Alternatively, a file-like object opened in binary mode. Make
        sure the file pointer is seeked to the start of the data.
        :param mimetype: The MIME type to send for the file. If not
            provided, it will try to detect it from the file name.
        :param as_attachment: Indicate to a browser that it should offer to
            save the file instead of displaying it.
        :param download_name: The default name browsers will use when saving
            the file. Defaults to the passed file name.
        :param conditional: Enable conditional and range responses based on
            request headers. Requires passing a file path and ``environ``.
        :param etag: Calculate an ETag for the file, which requires passing
            a file path. Can also be a string to use instead.
        :param last_modified: The last modified time to send for the file,
            in seconds. If not provided, it will try to detect it from the
            file path.
        :param max_age: How long the client should cache the file, in
            seconds. If set, ``Cache-Control`` will be ``public``, otherwise
            it will be ``no-cache`` to prefer conditional caching.
        """
        return file_sender(
            path_or_file=path_or_file,
            environ=request.environ,
            mimetype=mimetype,
            as_attachment=as_attachment,
            download_name=download_name,
            attachment_filename=attachment_filename,
            conditional=conditional,
            etag=etag,
            add_etags=add_etags,
            last_modified=last_modified,
            max_age=max_age,
            cache_timeout=cache_timeout,
        )

    def set_cookie(self,
            key: str,
            value: str = "",
            max_age: t.Optional[t.Union["timedelta", int]] = None,
            expires: t.Optional[t.Union[str, datetime, int, float]] = None,
            path: t.Optional[str] = "/",
            domain: t.Optional[str] = None,
            secure: bool = False,
            httponly: bool = False,
            samesite: t.Optional[str] = None
            ) -> t.Type["Response"]:

        """
        Sets a cookie.

        A warning is raised if the size of the cookie header exceeds
        :attr:`max_cookie_size`, but the header will still be set.

        :param key: the key (name) of the cookie to be set.
        :param value: the value of the cookie.
        :param max_age: should be a number of seconds, or `None` (default) if
                        the cookie should last only as long as the client's
                        browser session.
        :param expires: should be a `datetime` object or UNIX timestamp.
        :param path: limits the cookie to a given path, per default it will
                     span the whole domain.
        :param domain: if you want to set a cross-domain cookie.  For example,
                       ``domain=".example.com"`` will set a cookie that is
                       readable by the domain ``www.example.com``,
                       ``foo.example.com`` etc.  Otherwise, a cookie will only
                       be readable by the domain that set it.
        :param secure: If ``True``, the cookie will only be available
            via HTTPS.
        :param httponly: Disallow JavaScript access to the cookie.
        :param samesite: Limit the scope of the cookie to only be
            attached to requests that are "same-site".
        """

        super(Response, self).set_cookie(
                    key = key,
                    value = value,
                    max_age = max_age,
                    expires = expires,
                    path = path,
                    domain = domain,
                    secure = secure,
                    httponly = httponly,
                    samesite =samesite,
        )


    def setCookie(self, *wargs, **kwargs):
        """
        Set a cookie.
        This is the same function as set_cookie.

        All the parameters are same as for set_cookie.
        """
        return super(Response, self).set_cookie(*wargs, **kwargs)

    def clear_cookie(self,
            key: str,
            path: str = "/",
            domain: t.Optional[str] = None,
            secure: bool = False,
            httponly: bool = False,
            samesite: t.Optional[str] = None
            ) -> t.Type["Response"]:
        """
        Clear a cookie.  Fails silently if key doesn't exist.

        :param key: the key (name) of the cookie to be deleted.
        :param path: if the cookie that should be deleted was limited to a
                     path, the path has to be defined here.
        :param domain: if the cookie that should be deleted was limited to a
                       domain, that domain has to be defined here.
        :param secure: If ``True``, the cookie will only be available
            via HTTPS.
        :param httponly: Disallow JavaScript access to the cookie.
        :param samesite: Limit the scope of the cookie to only be
            attached to requests that are "same-site".
        """
        return super(Response, self).delete_cookie(
                    key=key, 
                    path=path, 
                    domain=domain, 
                    secure=secure,
                    httponly=httponly,
                    samesite=samesite
                    )


    def clearCookie(self, *wargs, **kwargs):
        """
        Clear a cookie.  Fails silently if key doesn't exist.

        It takes the same arguments as clear_cookies.
        """
        return self.clear_cookie(*wargs, **kwargs)
        

    def make_response(self,
                response: t.Optional[
                    t.Union[t.Iterable[bytes], bytes, t.Iterable[str], str]
                ] = None,
                status: t.Optional[t.Union[int, str, "HTTPStatus"]] = None,
                headers: t.Optional[
                    t.Union[
                        t.Mapping[str, t.Union[str, int, t.Iterable[t.Union[str, int]]]],
                        t.Iterable[t.Tuple[str, t.Union[str, int]]],
                    ]
                ] = None,
                mimetype: t.Optional[str] = None,
                content_type: t.Optional[str] = None,
                direct_passthrough: bool = False
                ) -> t.Type["ResponseBase"]:
        """
        the base function for this class to create the final response.
        """

        self.status_code = status or self.status_code
        self.headers = headers or self.headers
        self.mimetype = mimetype or self.mimetype
        self.content_type = content_type or self.content_type
        self.direct_passthrough = direct_passthrough or self.direct_passthrough

        return self.__class__(response=response, 
                status=self.status, 
                mimetype=self.mimetype, 
                content_type=self.content_type, 
                direct_passthrough=self.direct_passthrough, 
                headers=self.headers
                )