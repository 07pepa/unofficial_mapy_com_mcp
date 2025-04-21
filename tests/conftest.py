import pytest
from fastmcp.client import Client

from unofficial_mapy_com_mcp.server import mcp


@pytest.fixture(scope='session')
def mcp_client():
    return Client(mcp)


@pytest.fixture(scope='session')
def vcr_config():
    return {
        'filter_headers': ['x-mapy-api-key'],
    }
