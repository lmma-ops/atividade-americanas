import uuid, pytest
from config.env_config import REQUEST_TIMEOUT

pytestmark = [pytest.mark.api, pytest.mark.wishlist]

def test_create_wishlist_ok(http, api_url, authz):
    name = f"wl_{uuid.uuid4().hex[:6]}"
    r = http.post(f"{api_url}/wishlists", json={"name": name}, headers=authz, timeout=REQUEST_TIMEOUT)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["name"] == name
    wid = data["id"]

    # criar duplicada deve dar 409
    r2 = http.post(f"{api_url}/wishlists", json={"name": name}, headers=authz, timeout=REQUEST_TIMEOUT)
    assert r2.status_code == 409, f"esperado 409, veio {r2.status_code}: {r2.text}"

    # listar e encontrar a criada
    r3 = http.get(f"{api_url}/wishlists", headers=authz, timeout=REQUEST_TIMEOUT)
    assert r3.status_code == 200, r3.text
    ids = [w["id"] for w in r3.json()]
    assert wid in ids
