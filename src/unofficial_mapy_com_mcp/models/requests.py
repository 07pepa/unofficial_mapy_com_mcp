from typing import Annotated

from pydantic import BaseModel, Field

from unofficial_mapy_com_mcp.models.mapy.common.types import Coordinates
from unofficial_mapy_com_mcp.models.mapy.route.types import RouteType


class ApiRouteRequest(BaseModel):
    start: Coordinates
    end: Coordinates
    route_type: RouteType
    waypoints: Annotated[list[Coordinates] | None, Field(default=None)]
    avoid_toll: Annotated[bool | None, Field(default=False)]
