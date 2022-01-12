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
from uvicorn.config import Config
from uvicorn.server import Server
from uvicorn.supervisors import ChangeReload, Multiprocess
from uvicorn.supervisors.watchgodreload import WatchGodReload
from asgiref.sync import async_to_sync as asgiref_async_to_sync

import typing as t
import os as os
import uvicorn as uv

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


# def run_async_simple(host, port, app, debug, **kwargs):
#     uv.run(app, host=host, port=port, reload=debug, **kwargs)

def run_async_simple(host, port, app, debug:bool=False, **kwargs) -> None:
    if 'reload' in kwargs:
        kwargs.pop('reload')
    config = Config(app=app, host=host, port=port, debug=debug, **kwargs)
    server = Server(config)
    if debug is True:
        sock = config.bind_socket()
        WatchGodReload(config, target=server.run, sockets=[sock]).run()

    elif config.workers > 1:
        sock = config.bind_socket()
        Multiprocess(config, target=server.run, sockets=[sock]).run()
    else:
        server.run()