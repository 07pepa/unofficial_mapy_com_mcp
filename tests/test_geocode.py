import pytest
from inline_snapshot import external, outsource, snapshot

from unofficial_mapy_com_mcp.models.mapy.geocode.requests import GeocodeRequest, ReverseGeocodeRequest


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_geocode(mcp_client):
    async with mcp_client:
        request = GeocodeRequest(query='Vaclav Havel Airport Prague', limit=1, lang='en')

        result = await mcp_client.call_tool('maps_geocode', arguments={'query': request.model_dump()})
        assert outsource(result[0].text) == snapshot(external('c7cc6a1bf497*.txt'))


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_reverse_geocode(mcp_client):
    async with mcp_client:
        request = ReverseGeocodeRequest(lon=16.6085958, lat=49.1948039, lang='en')

        result = await mcp_client.call_tool('maps_reverse_geocode', arguments={'query': request.model_dump()})
        assert outsource(result[0].text) == snapshot(external('81e52bf8d7ef*.txt'))
