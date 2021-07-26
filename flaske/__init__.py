from flask import Flask as OldFlask
from flask import *
from flask.scaffold import (setupmethod, 
                _endpoint_from_view_func
                )
import typing as t
from .request import Request
from .response import Response as Responser
from ._helper import get_main_ctx_view
from os import path


class Flask(OldFlask):
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
        super(Flask, self).__init__(import_name=import_name, 
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
        # print (self.config['ATTACHMENTS_FOLDER'])

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

           Flaske will suppress any server error with a generic error page
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