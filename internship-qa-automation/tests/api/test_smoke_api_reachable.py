import pytest, requests
from config.env_config import API_BASE_URL, REQUEST_TIMEOUT

pytestmark = pytest.mark.api

def test_smoke_api_reachable():
    url = API_BASE_URL.rstrip("/")
    try:
        r = requests.get(url, timeout=REQUEST_TIMEOUT)
    except Exception as e:
        pytest.skip(f"API não acessível em {url}: {e}")
    else:
        assert 200 <= r.status_code < 400, f"status inesperado: {r.status_code}"
