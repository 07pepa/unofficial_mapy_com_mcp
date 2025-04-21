from typing import Annotated

from pydantic import BaseModel, Field

from unofficial_mapy_com_mcp.models.mapy.common.types import Coordinates
from unofficial_mapy_com_mcp.models.mapy.geocode.types import GeocodeType


class RegionalStructureItem(BaseModel):
    name: str
    type: GeocodeType


class GeoCodeResultItem(BaseModel):
    name: str
    label: str
    position: Coordinates
    type: GeocodeType
    zip: Annotated[str | None, Field(default=None)]
    regionalStructure: Annotated[list[RegionalStructureItem] | None, Field(default=None)]


class GeoCodeResult(BaseModel):
    items: list[GeoCodeResultItem]
