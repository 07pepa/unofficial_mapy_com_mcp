import httpx

from unofficial_mapy_com_mcp.models.mapy.geocode.requests import GeocodeRequest, ReverseGeocodeRequest
from unofficial_mapy_com_mcp.models.mapy.geocode.response import GeoCodeResult
from unofficial_mapy_com_mcp.models.mapy.route.request import RouteRequest
from unofficial_mapy_com_mcp.models.mapy.route.response import RouteErrorResponse, RouteResponse

NOT_FOUND = 404


class AsyncMapyClient:
    def __init__(self, apikey: str):
        self.apikey = apikey
        self.client = httpx.AsyncClient(
            base_url='https://api.mapy.cz/v1', headers={'X-Mapy-Api-Key': apikey}, http2=True
        )

    async def aclose(self) -> None:
        await self.client.aclose()

    async def geo_code(self, request: GeocodeRequest) -> GeoCodeResult:
        resp = await self.client.get('/geocode', params=request.model_dump(exclude_none=True))
        resp.raise_for_status()
        return GeoCodeResult.model_validate_json(resp.content)

    async def reverse_geocode(self, request: ReverseGeocodeRequest) -> GeoCodeResult:
        resp = await self.client.get('/rgeocode', params=request.model_dump(exclude_none=True))
        resp.raise_for_status()
        return GeoCodeResult.model_validate_json(resp.content)

    async def route(self, request: RouteRequest) -> RouteResponse:
        resp = await self.client.get('/routing/route', params=request.model_dump(exclude_none=True))
        if resp.status_code == NOT_FOUND:
            data = RouteErrorResponse.model_validate_json(resp.content)
            found_errors_codes = set()
            errors = []
            for error in data.detail:
                if error.errorCode in found_errors_codes:
                    continue  # pragma: no cover
                found_errors_codes.add(error.errorCode)
                match error.errorCode:
                    case 7:
                        errors.append(
                            'The route point is outside the available route network for the selected type of transport.'
                        )
                    case 9:
                        errors.append(
                            'The route point is outside the available '
                            'route network for the selected type of transport.'
                            'For example, another continent.'
                        )
                    case _:
                        errors.append(error.msg)

            if len(errors) >= 2:  # noqa: PLR2004
                raise RuntimeError('Encountered following errors:\n' + '\n'.join([f'* {error}' for error in errors]))

            raise RuntimeError(errors[0])

        return RouteResponse.model_validate_json(resp.content)


class ApiMapyClientManager:
    _client: AsyncMapyClient | None = None

    @classmethod
    def get_client(cls) -> AsyncMapyClient:
        if cls._client is None:
            raise RuntimeError('No client available')  # pragma: no cover
        return cls._client

    @classmethod
    def setup_client(cls, api_key: str) -> None:
        cls._client = AsyncMapyClient(api_key)

    @classmethod
    async def tear_down_client(cls) -> None:
        if cls._client:
            await cls._client.aclose()
