from pydantic import BaseModel
from typing import List, Dict


OK = "OK"
ERROR = "Error"

class Response(BaseModel):
    status: str


class ResponseWithMessage(Response):
    message: str


class ResponseWithData(Response):
    data: Dict


class ResponseWithMessageAndData(Response):
    message: str
    data: Dict


def NewResponseOK() -> Response:
    return Response(status=OK)


def NewResponseError() -> Response:
    return Response(status=ERROR)


def NewResponseWithMessageOK(message: str) -> ResponseWithMessage:
    return ResponseWithMessage(status=OK, message=message)


def NewResponseWithMessageERROR(message: str) -> ResponseWithMessage:
    return ResponseWithMessage(status=ERROR, message=message)


def NewResponseWithData(data: Dict) -> ResponseWithData:
    return ResponseWithData(status=OK, data=data)


def NewResponseWithMessageAndData(message: str, data: Dict) -> ResponseWithMessageAndData:
    return ResponseWithMessageAndData(status=OK, message=message, data=data)
