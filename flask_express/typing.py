import typing as t

if t.TYPE_CHECKING:
    from .request import Request as BaseRequest
    from .response import Response as BaseResponse

Request = t.TypeVar("Request", bound="BaseRequest")
Response = t.TypeVar("Response", bound="BaseResponse")