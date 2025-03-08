from pydantic import BaseModel
from typing import Any, List, Dict, Union
from litestar.response import Response


OK = "OK"
ERROR = "Error"


# class Response(BaseModel):
#     status: str


# class ResponseWithMessage(Response):
#     message: str


# class ResponseWithData(Response):
#     data: Dict


# class ResponseWithMessageAndData(Response):
#     message: str
#     data: Dict


def NewJSONResponseOK(status_code: int) -> Response:
    return Response(
            content={"status": OK},
            media_type="application/json",
            status_code=status_code
        )

def NewJSONResponseERROR(status_code: int) -> Response:
    return Response(
            content={"status": ERROR},
            media_type="application/json",
            status_code=status_code
        )


def NewResponseWithMessageOK(status_code: int, message: str) -> Response:
    return Response(
            content={"status": OK, "message": message},
            media_type="application/json",
            status_code=status_code
        )

def NewResponseWithMessageERROR(status_code: int, message: str) -> Response:
    return Response(
            content={"status": ERROR, "message": message},
            media_type="application/json",
            status_code=status_code
        )


def NewResponseWithData(status_code: int, data: Union[Dict[str, Any], str, Any]) -> Response:
    return Response(
            content={"status": OK, "data": data},
            media_type="application/json",
            status_code=status_code
        )

def NewResponseWithMessageAndData(status_code: int, message: str, data: Union[Dict[str, Any], str, Any]) -> Response:
    return Response(
            content={"status": OK, "message": message, "data": data},
            media_type="application/json",
            status_code=status_code
        )
