from typing import Annotated

from pydantic import BaseModel, Field


class RouteResponse(BaseModel):
    length: Annotated[int, Field(description='Length of the route in meters')]
    duration: Annotated[int, Field(description='Duration of the route in seconds')]


class RouteErrorResponseDetail(BaseModel):
    errorCode: int
    msg: str


class RouteErrorResponse(BaseModel):
    detail: Annotated[list[RouteErrorResponseDetail], Field(description='List of error details', min_length=1)]
