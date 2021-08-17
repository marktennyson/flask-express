from inspect import (signature, 
            iscoroutinefunction as is_async_func
            )
from functools import wraps
from .response import Response
from flask.globals import request
import typing as t

from asgiref.sync import async_to_sync as asgiref_async_to_sync

def async_to_sync(func):
    return asgiref_async_to_sync(func)

def get_main_ctx_view(func:t.Callable):
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