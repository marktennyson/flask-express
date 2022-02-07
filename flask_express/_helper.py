from inspect import (
    signature, 
    iscoroutinefunction as is_async_func
    )
from functools import wraps
from .response import Response
from flask.globals import request
from flask.helpers import _prepare_send_file_kwargs
from werkzeug.exceptions import NotFound
from werkzeug.security import safe_join
from werkzeug.utils import send_file

from asgiref.sync import async_to_sync as asgiref_async_to_sync

import typing as t
import os as os
import click as c

if t.TYPE_CHECKING:
    from _typeshed.wsgi import WSGIEnvironment

def async_to_sync(func) -> t.Any:
    return asgiref_async_to_sync(func)


def get_main_ctx_view(func:t.Callable) -> t.Any:
    """
    adding the default request, response object with view function
    """
    request_param = signature(func).parameters.get('request', None) \
                            or signature(func).parameters.get('req', None)
    
    is_request:bool = True if request_param is not None else False

    response_param = signature(func).parameters.get('response', None) \
                            or signature(func).parameters.get('res', None)
    
    is_response:bool = True if response_param is not None else False

    if is_async_func(func) is not True:
        @wraps(func)
        def decorator(*args, **kwargs):
            if is_request is True:

                args:list = list(args)
                args.insert(0, request)

            if is_response is True:
                args:list = list(args)
                if len(args):
                    args.insert(1, Response())
                else:
                    args.insert(0, Response())
            
            args:tuple = tuple(args)
            return func(*args, **kwargs)
        return decorator
    else:
        @wraps(func)
        async def decorator(*args, **kwargs):
            if is_request is True:

                args:list = list(args)
                args.insert(0, request)

            if is_response is True:
                args:list = list(args)
                if len(args):
                    args.insert(1, Response())
                else:
                    args.insert(0, Response())
            
            args:tuple = tuple(args)
            return await func(*args, **kwargs)
        return decorator


class Utils(object):
    @classmethod
    def send_from_directory_helper(
        cls,
        directory: t.Union[os.PathLike, str],
        path: t.Union[os.PathLike, str],
        environ: "WSGIEnvironment",
        **kwargs: t.Any
        ) -> "Response":

        path = safe_join(os.fspath(directory), os.fspath(path))

        if path is None:
            raise NotFound("file path or directory not found.")
    
        # Flask will pass app.root_path, allowing its send_from_directory
        # wrapper to not have to deal with paths.
        if "_root_path" in kwargs:
            path = os.path.join(kwargs["_root_path"], path)

        try:
            if not os.path.isfile(path):
                raise NotFound(f"{path.rsplit('/', 1)[1]} not found at {directory}")

        except ValueError:
            # path contains null byte on Python < 3.8
            raise NotFound("invalid file or directory name.")
        
        return send_file(path, environ, **kwargs)

    @classmethod
    def send_from_directory(
        cls,
        directory: t.Union[os.PathLike, str],
        path: t.Union[os.PathLike, str],
        **kwargs: t.Any,
        ) -> "Response":
        
        return cls.send_from_directory_helper(
            directory, 
            path, 
            **_prepare_send_file_kwargs(**kwargs)
            )

def _show_asgi_server_banner(env, debug, app_import_path, eager_loading):
    """Show extra startup messages the first time the server is run,
    ignoring the reloader.
    """
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        return

    if app_import_path is not None:
        message = f" * Serving Flask-Express app {app_import_path!r} on ASGI Mode"

        if not eager_loading:
            message += " (lazy loading)"

        c.echo(message)

    c.echo(f" * Environment: {env}")

    if env == "production":
        c.secho(
            "   WARNING: This is a development server. Do not use it in"
            " a production deployment.",
            fg="red",
        )
        c.secho("   Use a production ASGI server(uvicorn/hypercorn) instead.", dim=True)

    if debug is not None:
        c.echo(f" * Debug mode: {'on' if debug else 'off'}")