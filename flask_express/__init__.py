"""
created by: Aniket Sarkar(https://github.com/marktennyson)
Please contribute in this project.
"""
from markupsafe import escape
from markupsafe import Markup
from werkzeug.exceptions import abort as abort
from werkzeug.utils import redirect as redirect

from flask import json as json
from flask.app import Response as Response
from flask.blueprints import Blueprint as Blueprint
from flask.config import Config as Config
from flask.ctx import after_this_request as after_this_request
from flask.ctx import copy_current_request_context as copy_current_request_context
from flask.ctx import has_app_context as has_app_context
from flask.ctx import has_request_context as has_request_context
from flask.globals import _app_ctx_stack as _app_ctx_stack
from flask.globals import _request_ctx_stack as _request_ctx_stack
from flask.globals import current_app as current_app
from flask.globals import g as g
from flask.globals import request as request
from flask.globals import session as session
from flask.helpers import flash as flash
from flask.helpers import get_flashed_messages as get_flashed_messages
from flask.helpers import get_template_attribute as get_template_attribute
from flask.helpers import make_response as make_response
from flask.helpers import safe_join as safe_join
from flask.helpers import send_file as send_file
from flask.helpers import send_from_directory as send_from_directory
from flask.helpers import stream_with_context as stream_with_context
from flask.helpers import url_for as url_for
from flask.json import jsonify as jsonify
from flask.signals import appcontext_popped as appcontext_popped
from flask.signals import appcontext_pushed as appcontext_pushed
from flask.signals import appcontext_tearing_down as appcontext_tearing_down
from flask.signals import before_render_template as before_render_template
from flask.signals import got_request_exception as got_request_exception
from flask.signals import message_flashed as message_flashed
from flask.signals import request_finished as request_finished
from flask.signals import request_started as request_started
from flask.signals import request_tearing_down as request_tearing_down
from flask.signals import signals_available as signals_available
from flask.signals import template_rendered as template_rendered
from flask.templating import render_template as render_template
from flask.templating import render_template_string as render_template_string


from flask.scaffold import setupmethod
from flask.scaffold import _endpoint_from_view_func                                
from flask.app import Flask
import typing as t
from .request import Request
from .response import Response as Responser
from ._helper import get_main_ctx_view
from os import path


__all__ = (
    "FlaskExpress",
    "escape",
    "Markup",
    "abort",
    "redirect",
    "json",
    "Response",
    "Blueprint",
    "Config",
    "after_this_request",
    "copy_current_request_context",
    "has_app_context",
    "has_request_context",
    "_app_ctx_stack",
    "_request_ctx_stack",
    "current_app",
    "g",
    "request",
    "session",
    "flash",
    "get_flashed_messages",
    "get_template_attribute",
    "make_response",
    "safe_join",
    "send_file",
    "send_from_directory",
    "stream_with_context",
    "url_for",
    "jsonify",
    "appcontext_pushed",
    "appcontext_popped",
    "appcontext_tearing_down",
    "before_render_template",
    "got_request_exception",
    "message_flashed",
    "request_finished",
    "request_tearing_down",
    "signals_available",
    "template_rendered",
    "render_template",
    "render_template_string",
    "Responser",
)


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
    ) -> None:
        super().__init__(import_name=import_name, 
                            static_url_path=static_url_path, 
                            static_folder=static_folder, 
                            host_matching=host_matching, 
                            subdomain_matching=subdomain_matching,
                            template_folder=template_folder,
                            instance_path=instance_path,
                            root_path=root_path,
                            instance_relative_config=instance_relative_config, 
                            static_host=static_host)
        self.config['ATTACHMENTS_FOLDER'] = path.join(path.abspath(path.dirname(self.import_name)), "attachments")

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