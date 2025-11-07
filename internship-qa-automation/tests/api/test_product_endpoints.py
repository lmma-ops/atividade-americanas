import uuid, pytest
from config.env_config import REQUEST_TIMEOUT

pytestmark = [pytest.mark.api, pytest.mark.products]

@pytest.fixture
def wishlist_id(http, api_url, authz):
    name = f"wl_prod_{uuid.uuid4().hex[:6]}"
    r = http.post(f"{api_url}/wishlists", json={"name": name}, headers=authz, timeout=REQUEST_TIMEOUT)
    assert r.status_code == 200, r.text
    return r.json()["id"]

def test_product_crud(http, api_url, authz, wishlist_id):
    # CREATE
    prod_body = {
        "Product": "Livro QA",
        "Price": "19.90",
        "Zipcode": "50000-000",
        "delivery_estimate": "5 dias",
        "shipping_fee": "7.90",
    }
    r = http.post(f"{api_url}/wishlists/{wishlist_id}/products", json=prod_body, headers=authz, timeout=REQUEST_TIMEOUT)
    assert r.status_code == 200, r.text
    created = r.json()
    pid = created["id"]
    assert created["Product"] == "Livro QA"

    # LIST
    r2 = http.get(f"{api_url}/wishlists/{wishlist_id}/products", headers=authz, timeout=REQUEST_TIMEOUT)
    assert r2.status_code == 200, r2.text
    ids = [p["id"] for p in r2.json()]
    assert pid in ids

    # UPDATE
    r3 = http.put(f"{api_url}/products/{pid}", json={"Price": "29.90"}, headers=authz, timeout=REQUEST_TIMEOUT)
    assert r3.status_code == 200, r3.text
    assert r3.json()["Price"] == "29.90"

    # DELETE
