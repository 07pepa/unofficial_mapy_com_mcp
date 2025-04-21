from typing import Annotated, Self

from pydantic import BaseModel, Field, model_serializer

from unofficial_mapy_com_mcp.models.mapy.common.types import Coordinates
from unofficial_mapy_com_mcp.models.mapy.route.types import RouteType
from unofficial_mapy_com_mcp.models.requests import ApiRouteRequest


class RouteCoordinates(Coordinates):
    @model_serializer()
    def serialize_model(self) -> str:
        return f'{self.lon},{self.lat}'


class RouteRequest(BaseModel):
    start: RouteCoordinates
    end: RouteCoordinates
    routeType: RouteType
    waypoints: Annotated[list[Coordinates] | None, Field(default=None)]
    avoid_toll: Annotated[bool | None, Field(default=False)]

    @classmethod
    def from_api_model(cls, model: ApiRouteRequest) -> Self:
        return cls(
            start=RouteCoordinates(lat=model.start.lat, lon=model.start.lon),
            end=RouteCoordinates(lat=model.end.lat, lon=model.end.lon),
            routeType=model.route_type,
            waypoints=[RouteCoordinates(lat=w.lat, lon=w.lon) for w in model.waypoints] if model.waypoints else None,
            avoid_toll=model.avoid_toll,
        )
