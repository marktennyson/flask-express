"""
created by: Aniket Sarkar(https://github.com/marktennyson)
Please contribute to this project.
"""
from os import path
from flask import cli 

from asgiref.wsgi import WsgiToAsgiInstance

from werkzeug.datastructures import Headers

from flask.scaffold import setupmethod
from flask.json import jsonify
from flask.globals import request as grequest
from flask.scaffold import _endpoint_from_view_func                                
from flask.app import Flask
from flask.helpers import get_debug_flag
from flask.helpers import get_env
from flask.helpers import get_load_dotenv

from .request import Request
from .response import Response
from ._helper import (
    get_main_ctx_view, 
    _show_asgi_server_banner
    )

import sys as sys
import os as os
import typing as t


from typing import *
import warnings
import asyncio
import signal
from asgiref.wsgi import WsgiToAsgi
from hypercorn.asyncio import serve
from flask.logging import create_logger
from hypercorn.config import Config as HyperConfig 

if t.TYPE_CHECKING:
    from flask.typing import ResponseReturnValue


class FlaskExpress(Flask):
    request_class = Request
    response_class = Response

    def __init__(self,
        import_name: str,
        static_url_path: t.Optional[str] = None,
        static_folder: t.Optional[str] = "static",
        static_host: t.Optional[str] = None,
        host_matching: bool = False,
        subdomain_matching: bool = False,
        template_folder: t.Optional[str] = "templates",
        instance_path: t.Optional[str] = None,
        instance_relative_config: bool = False,
        root_path: t.Optional[str] = None,
        _async:bool= False,
    ) -> None:
        super(FlaskExpress, self).__init__(
            import_name=import_name, 
            static_url_path=static_url_path, 
            static_folder=static_folder, 
            host_matching=host_matching, 
            subdomain_matching=subdomain_matching,
            template_folder=template_folder,
            instance_path=instance_path,
            root_path=root_path,
            instance_relative_config=instance_relative_config, 
            static_host=static_host
            )
        attachment_loc = path.join(path.abspath(path.dirname(self.import_name)), "attachments")
        self.config.setdefault("ATTACHMENTS_FOLDER", attachment_loc)
        # self.is_async = _async
        # if self.is_async is True:
        #     _self:"WsgiToAsgi" = WsgiToAsgi(self)
        #     self = _self.wsgi_application
        


    @setupmethod
    def add_url_rule(
        self,
        rule: str,
        endpoint: t.Optional[str] = None,
        view_func: t.Optional[t.Callable] = None,
        provide_automatic_options: t.Optional[bool] = None,
        **options: t.Any,
    ) -> None:
        if endpoint is None:
            endpoint = _endpoint_from_view_func(view_func)  # type: ignore
        options["endpoint"] = endpoint
        methods = options.pop("methods", None)

        # if the methods are not given and the view_func object knows its
        # methods we can use that instead.  If neither exists, we go with
        # a tuple of only ``GET`` as default.
        if methods is None:
            methods = getattr(view_func, "methods", None) or ("GET",)
        if isinstance(methods, str):
            raise TypeError(
                "Allowed methods must be a list of strings, for"
                ' example: @app.route(..., methods=["POST"])'
            )
        methods = {item.upper() for item in methods}

        # Methods that should always be added
        required_methods = set(getattr(view_func, "required_methods", ()))

        # starting with Flask 0.8 the view_func object can disable and
        # force-enable the automatic options handling.
        if provide_automatic_options is None:
            provide_automatic_options = getattr(
                view_func, "provide_automatic_options", None
            )

        if provide_automatic_options is None:
            if "OPTIONS" not in methods:
                provide_automatic_options = True
                required_methods.add("OPTIONS")
            else:
                provide_automatic_options = False

        # Add the required methods now.
        methods |= required_methods

        rule = self.url_rule_class(rule, methods=methods, **options)
        rule.provide_automatic_options = provide_automatic_options  # type: ignore

        self.url_map.add(rule)
        if view_func is not None:
            old_func = self.view_functions.get(endpoint)
            if old_func is not None and old_func != view_func:
                raise AssertionError(
                    "View function mapping is overwriting an existing"
                    f" endpoint function: {endpoint}"
                )
            view_func = get_main_ctx_view(view_func)
            self.view_functions[endpoint] = view_func


    def make_response(self, rv: "ResponseReturnValue") -> Response:
        """Convert the return value from a view function to an instance of
        :attr:`response_class`.

        :param rv: the return value from the view function. The view function
            must return a response. Returning ``None``, or the view ending
            without returning, is not allowed. The following types are allowed
            for ``view_rv``:

            ``str``
                A response object is created with the string encoded to UTF-8
                as the body.

            ``bytes``
                A response object is created with the bytes as the body.

            ``dict``
                A dictionary that will be jsonify'd before being returned.

            ``tuple``
                Either ``(body, status, headers)``, ``(body, status)``, or
                ``(body, headers)``, where ``body`` is any of the other types
                allowed here, ``status`` is a string or an integer, and
                ``headers`` is a dictionary or a list of ``(key, value)``
                tuples. If ``body`` is a :attr:`response_class` instance,
                ``status`` overwrites the exiting value and ``headers`` are
                extended.

            :attr:`response_class`
                The object is returned unchanged.

            other :class:`~werkzeug.wrappers.Response` class
                The object is coerced to :attr:`response_class`.

            :func:`callable`
                The function is called as a WSGI application. The result is
                used to create a response object.

        .. versionchanged:: 0.9
           Previously a tuple was interpreted as the arguments for the
           response object.
        """
        status = headers = None

        # unpack tuple returns
        if isinstance(rv, tuple):
            len_rv = len(rv)

            # a 3-tuple is unpacked directly
            if len_rv == 3:
                rv, status, headers = rv
            # decide if a 2-tuple has status or headers
            elif len_rv == 2:
                if isinstance(rv[1], (Headers, dict, tuple, list)):
                    rv, headers = rv
                else:
                    rv, status = rv
            # other sized tuples are not allowed
            else:
                raise TypeError(
                    "The view function did not return a valid response tuple."
                    " The tuple must have the form (body, status, headers),"
                    " (body, status), or (body, headers)."
                )

        # the body must not be None
        if rv is None:
            raise TypeError(
                f"The view function for {grequest.endpoint!r} did not"
                " return a valid response. The function either returned"
                " None or ended without a return statement."
            )

        # make sure the body is an instance of the response class
        respObj = self.response_class()
        
        if not isinstance(rv, self.response_class):
            if isinstance(rv, (str, bytes, bytearray)):
                # let the response class set the status and headers instead of
                # waiting to do it manually, so that the class can handle any
                # special logic
                rv = respObj.make_response(rv, status=status, headers=headers) # this requires a default type `Response` class.
                status = headers = None
            elif isinstance(rv, dict):
                rv = jsonify(rv)
            elif isinstance(rv, Response) or callable(rv):
                # evaluate a WSGI callable, or coerce a different response
                # class to the correct type
                try:
                    rv = respObj.force_type(rv, grequest.environ)  # type: ignore  # noqa: B950
                except TypeError as e:
                    raise TypeError(
                        f"{e}\nThe view function did not return a valid"
                        " response. The return type must be a string,"
                        " dict, tuple, Response instance, or WSGI"
                        f" callable, but it was a {type(rv).__name__}."
                    ).with_traceback(sys.exc_info()[2])
            else:
                raise TypeError(
                    "The view function did not return a valid"
                    " response. The return type must be a string,"
                    " dict, tuple, Response instance, or WSGI"
                    f" callable, but it was a {type(rv).__name__}."
                )

        rv = t.cast(Response, rv) 
       
        return respObj.make_response_from_obj(rv)


    def run(
            self,
            host: t.Optional[str] = None,
            port: t.Optional[int] = None,
            debug: t.Optional[bool] = None,
            load_dotenv: bool = True,
            **options: t.Any,
        ) -> None:
        """
        Binds and listens for connections on the specified host and port
        It's very similar to :func:`flask.Flask.run`

        .. admonition:: Keep in Mind

           Flask-Express will suppress any server error with a generic error page
           unless it is in debug mode.  As such to enable just the
           interactive debugger without the code reloading, you have to
           invoke :meth:`listen` with ``debug=True`` and ``use_reloader=False``.
           Setting ``use_debugger`` to ``True`` without being in debug mode
           won't catch any exceptions because there won't be any to
           catch.

        :param host: the hostname to listen on. Set this to ``'0.0.0.0'`` to
            have the server available externally as well. Defaults to
            ``'127.0.0.1'`` or the host in the ``SERVER_NAME`` config variable
            if present.
        :param port: the port of the webserver. Defaults to ``5000`` or the
            port defined in the ``SERVER_NAME`` config variable if present.
        :param debug: if given, enable or disable debug mode. See
            :attr:`debug`.
        :param load_dotenv: Load the nearest :file:`.env` and :file:`.flaskenv`
            files to set environment variables. Will also change the working
            directory to the directory containing the first file found.
        :param options: the options to be forwarded to the underlying Werkzeug
            server. See :func:`werkzeug.serving.run_simple` for more
            information. If the `MAKE_ASGI_APP` config value is True 
            then the option to be forwarded to the underlying Uvicorn ASGI server.
        """
        if os.environ.get("FLASK_RUN_FROM_CLI") == "true":
            from flask.debughelpers import explain_ignored_app_run

            explain_ignored_app_run()
            return

        if get_load_dotenv(load_dotenv):
            cli.load_dotenv()

            # if set, let env vars override previous values
            if "FLASK_ENV" in os.environ:
                self.env = get_env()
                self.debug = get_debug_flag()
            elif "FLASK_DEBUG" in os.environ:
                self.debug = get_debug_flag()

        # debug passed to method overrides all other sources
        if debug is not None:
            self.debug = bool(debug)

        server_name = self.config.get("SERVER_NAME")
        sn_host = sn_port = None

        if server_name:
            sn_host, _, sn_port = server_name.partition(":")

        if not host:
            if sn_host:
                host = sn_host
            else:
                host = "127.0.0.1"

        if port or port == 0:
            port = int(port)
        elif sn_port:
            port = int(sn_port)
        else:
            port = 5000

        try:
            options.setdefault("use_reloader", self.debug)

            if self.config.get('MAKE_ASGI_APP', False) is not True:
                cli.show_server_banner(self.env, self.debug, self.name, False) 
                options.setdefault("use_debugger", self.debug)
                options.setdefault("threaded", True)
                from werkzeug.serving import run_simple
                run_simple(t.cast(str, host), port, self, **options)
            else:
                _show_asgi_server_banner(self.env, self.debug, self.name, False)
                options.setdefault("debug", self.debug)
                self.async_run(host, port, **options)
        finally:
            # reset the first request information if the development server
            # reset normally.  This makes it possible to restart the server
            # without reloader and that stuff from an interactive shell.
            self._got_first_request = False



    def listen(self, 
        port: t.Optional[int] = None,
        host: t.Optional[str] = None,
        debug: t.Optional[bool] = None,
        load_dotenv: bool = True,
        **options: t.Any
        ) -> None:
        """
        Binds and listens for connections on the specified host and port
        It's very similar to :func:`flask.Flask.run`

        .. admonition:: Keep in Mind

           Flask-Express will suppress any server error with a generic error page
           unless it is in debug mode.  As such to enable just the
           interactive debugger without the code reloading, you have to
           invoke :meth:`listen` with ``debug=True`` and ``use_reloader=False``.
           Setting ``use_debugger`` to ``True`` without being in debug mode
           won't catch any exceptions because there won't be any to
           catch.

        :param host: the hostname to listen on. Set this to ``'0.0.0.0'`` to
            have the server available externally as well. Defaults to
            ``'127.0.0.1'`` or the host in the ``SERVER_NAME`` config variable
            if present.
        :param port: the port of the webserver. Defaults to ``5000`` or the
            port defined in the ``SERVER_NAME`` config variable if present.
        :param debug: if given, enable or disable debug mode. See
            :attr:`debug`.
        :param load_dotenv: Load the nearest :file:`.env` and :file:`.flaskenv`
            files to set environment variables. Will also change the working
            directory to the directory containing the first file found.
        :param options: the options to be forwarded to the underlying Werkzeug
            server. See :func:`werkzeug.serving.run_simple` for more
            information.
        """
        return self.run(host, port, debug, load_dotenv, **options)



    def async_run(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        debug: Optional[bool] = None,
        use_reloader: bool = True,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        ca_certs: Optional[str] = None,
        certfile: Optional[str] = None,
        keyfile: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Run this application.
        This is best used for development only, see Hypercorn for
        production servers.
        Arguments:
            host: Hostname to listen on. By default this is loopback
                only, use 0.0.0.0 to have the server listen externally.
            port: Port number to listen on.
            debug: If set enable (or disable) debug mode and debug output.
            use_reloader: Automatically reload on code changes.
            loop: Asyncio loop to create the server in, if None, take default one.
                If specified it is the caller's responsibility to close and cleanup the
                loop.
            ca_certs: Path to the SSL CA certificate file.
            certfile: Path to the SSL certificate file.
            keyfile: Path to the SSL key file.
        """
        if kwargs:
            warnings.warn(
                f"Additional arguments, {','.join(kwargs.keys())}, are not supported.\n"
                "They may be supported by Hypercorn, which is the ASGI server Flask-Express "
                "uses by default. This method is meant for development and debugging."
            )

        if loop is None:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        loop.set_debug(self.debug)

        shutdown_event = asyncio.Event()

        def _signal_handler(*_: Any) -> None:
            shutdown_event.set()

        try:
            loop.add_signal_handler(signal.SIGTERM, _signal_handler)
            loop.add_signal_handler(signal.SIGINT, _signal_handler)
        except (AttributeError, NotImplementedError):
            pass

        task = self.run_task(
            host,
            port,
            debug,
            use_reloader,
            ca_certs,
            certfile,
            keyfile,
            shutdown_trigger=shutdown_event.wait,  # type: ignore
        )
        scheme = "https" if certfile is not None and keyfile is not None else "http"

        try:
            loop.run_until_complete(task)
        finally:
            try:
                _cancel_all_tasks(loop)
                loop.run_until_complete(loop.shutdown_asyncgens())
            finally:
                asyncio.set_event_loop(None)
                loop.close()

    def run_task(
        self,
        host: str = "127.0.0.1",
        port: int = 5000,
        debug: Optional[bool] = None,
        use_reloader: bool = True,
        ca_certs: Optional[str] = None,
        certfile: Optional[str] = None,
        keyfile: Optional[str] = None,
        shutdown_trigger: Optional[Callable[..., Awaitable[None]]] = None,
    ) -> Coroutine[None, None, None]:
        """Return a task that when awaited runs this application.
        This is best used for development only, see Hypercorn for
        production servers.
        Arguments:
            host: Hostname to listen on. By default this is loopback
                only, use 0.0.0.0 to have the server listen externally.
            port: Port number to listen on.
            debug: If set enable (or disable) debug mode and debug output.
            use_reloader: Automatically reload on code changes.
            ca_certs: Path to the SSL CA certificate file.
            certfile: Path to the SSL certificate file.
            keyfile: Path to the SSL key file.
        """
        config = HyperConfig()
        config.access_log_format = '%(h)s - - "%(r)s" %(s)s'
        config.accesslog = create_logger(self)
        config.bind = [f"{host}:{port}"]
        config.ca_certs = ca_certs
        config.certfile = certfile
        if debug is not None:
            self.debug = debug
        config.errorlog = config.accesslog
        config.keyfile = keyfile
        config.use_reloader = use_reloader

        return serve(WsgiToAsgi(self), config, shutdown_trigger=shutdown_trigger)

    def asgi_app(self) -> WsgiToAsgi:
        return WsgiToAsgi(self)

    async def __call__(self, scope, receive, send):

        await WsgiToAsgiInstance(self.wsgi_app)(scope, receive, send)

    # def __call__(self, environ: dict, start_response: t.Callable) -> t.Any:
    #     """The WSGI server calls the Flask application object as the
    #     WSGI application. This calls :meth:`wsgi_app`, which can be
    #     wrapped to apply middleware.
    #     """
    #     return self.wsgi_app(environ, start_response)


def _cancel_all_tasks(loop: asyncio.AbstractEventLoop) -> None:
    tasks = [task for task in asyncio.all_tasks(loop) if not task.done()]
    if not tasks:
        return

    for task in tasks:
        task.cancel()
    loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))

    for task in tasks:
        if not task.cancelled() and task.exception() is not None:
            loop.call_exception_handler(
                {
                    "message": "unhandled exception during shutdown",
                    "exception": task.exception(),
                    "task": task,
                }
            )