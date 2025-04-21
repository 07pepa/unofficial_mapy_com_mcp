from typing import Annotated, Literal

from pydantic import BaseModel, Field

Longitude = Annotated[float, Field(ge=-180, le=180.0, description='Longitude')]
Latitude = Annotated[float, Field(ge=-90, le=90.0, description='Latitude')]
AvailableLanguages = Literal['cs', 'de', 'el', 'en', 'es', 'fr', 'it', 'nl', 'pl', 'pt', 'ru', 'sk', 'tr', 'uk']


class Coordinates(BaseModel):
    lon: Longitude
    lat: Latitude
