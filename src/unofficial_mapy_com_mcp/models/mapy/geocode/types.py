from typing import Literal

GeocodeType = Literal[
    'regional',
    'regional.country',
    'regional.region',
    'regional.municipality',
    'regional.municipality_part',
    'regional.street',
    'regional.address',
    'poi',
    'coordinate',
]
