from pydantic import BaseModel, Field

from unofficial_mapy_com_mcp.models.mapy.common.types import AvailableLanguages, Latitude, Longitude


class GeocodeRequest(BaseModel):
    query: str
    lang: AvailableLanguages
    limit: int = Field(default=5, le=15, ge=1)


class ReverseGeocodeRequest(BaseModel):
    lon: Longitude
    lat: Latitude
    lang: AvailableLanguages
