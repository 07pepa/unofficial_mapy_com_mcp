import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from fastmcp import FastMCP

from unofficial_mapy_com_mcp.async_mapy_client import ApiMapyClientManager
from unofficial_mapy_com_mcp.models.mapy.geocode.requests import GeocodeRequest, ReverseGeocodeRequest
from unofficial_mapy_com_mcp.models.mapy.geocode.response import GeoCodeResult
from unofficial_mapy_com_mcp.models.mapy.route.request import RouteRequest
from unofficial_mapy_com_mcp.models.mapy.route.response import RouteResponse
from unofficial_mapy_com_mcp.models.requests import ApiRouteRequest
from unofficial_mapy_com_mcp.models.settings import Settings


@asynccontextmanager
async def live_span(_: FastMCP[Any]) -> AsyncIterator[None]:
    settings = Settings()  # pyright: ignore
    ApiMapyClientManager.setup_client(settings.api_key.get_secret_value())
    try:
        yield
    finally:
        await ApiMapyClientManager.tear_down_client()


mcp: FastMCP[None] = FastMCP(
    'mapy_unofficial',
    instructions='this server provides way to retrive real world mapping data amd cad no routing',
    lifespan=live_span,
)


@mcp.tool()
async def maps_geocode(query: GeocodeRequest) -> GeoCodeResult:
    """
    Geocode an address.
    """
    client = ApiMapyClientManager.get_client()
    return await client.geo_code(query)


@mcp.tool()
async def maps_reverse_geocode(query: ReverseGeocodeRequest) -> GeoCodeResult:
    """
    based-on-coordinates reverse geocode an address
    """
    client = ApiMapyClientManager.get_client()
    return await client.reverse_geocode(query)


@mcp.tool()
async def maps_route(query: ApiRouteRequest) -> RouteResponse:
    """
    route from start to end via waypoints (optional)
    bike_road type means bike route suitable for road bike
    bike_mountain type means bike route suitable for mountain bike
    car_fast_traffic type means car route with traffic
    :returns
        length: Length of the route in meters
        duration: Duration of the route in seconds
    """
    client = ApiMapyClientManager.get_client()
    return await client.route(request=RouteRequest.from_api_model(query))


def entry_point() -> None:  # pragma: nocover
    loop_factory = None
    try:
        import uvloop

        loop_factory = uvloop.new_event_loop
    except ImportError:
        pass

    with asyncio.Runner(loop_factory=loop_factory) as runner:
        runner.run(mcp.run_sse_async())


if __name__ == '__main__':
    entry_point()  # pragma: nocover
