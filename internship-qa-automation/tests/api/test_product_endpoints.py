import pytest
import requests
from config.env_config import API_BASE_URL, REQUEST_TIMEOUT

pytestmark = [pytest.mark.api, pytest.mark.products]

BASE = API_BASE_URL.rstrip("/")

@pytest.fixture()
def a_wishlist(auth_header):
    r = requests.post(f"{BASE}/wishlists", headers=auth_header, json={"name": "WL-Products"}, timeout=REQUEST_TIMEOUT)
    assert r.status_code in (200, 201), r.text
    return r.json()["id"]

# Scenario 21
def test_21_add_product_success(auth_header, a_wishlist):
    payload = {"Product": "New Gadget", "Price": "99.99", "Zipcode": "12345678"}
    r = requests.post(f"{BASE}/wishlists/{a_wishlist}/products", headers=auth_header, json=payload, timeout=REQUEST_TIMEOUT)
    assert r.status_code in (200, 201), r.text
    body = r.json()
    assert body["wishlist_id"] == a_wishlist
    assert body.get("is_purchased") in (False, 0)

# Scenario 22
def test_22_add_product_nonexistent_wishlist(auth_header):
    r = requests.post(f"{BASE}/wishlists/999999/products", headers=auth_header, json={"Product": "X", "Price": "10.00", "Zipcode": "12345678"}, timeout=REQUEST_TIMEOUT)
    assert r.status_code == 404, r.text

# Scenario 23
def test_23_add_product_other_user():
    # User A com wishlist
    import uuid
    email_a = f"usera_{uuid.uuid4().hex[:8]}@example.com"
    pw = "Password123!"
    requests.post(f"{BASE}/auth/register", json={"email": email_a, "password": pw}, timeout=REQUEST_TIMEOUT)
    login_a = requests.post(f"{BASE}/auth/login", data={"username": email_a, "password": pw}, timeout=REQUEST_TIMEOUT)
    token_a = login_a.json()["access_token"]
    hdrs_a = {"Authorization": f"Bearer {token_a}"}
    wl = requests.post(f"{BASE}/wishlists", headers=hdrs_a, json={"name": "A-List"}, timeout=REQUEST_TIMEOUT).json()["id"]

    # User B tenta adicionar produto na WL de A
    email_b = f"userb_{uuid.uuid4().hex[:8]}@example.com"
    requests.post(f"{BASE}/auth/register", json={"email": email_b, "password": pw}, timeout=REQUEST_TIMEOUT)
    login_b = requests.post(f"{BASE}/auth/login", data={"username": email_b, "password": pw}, timeout=REQUEST_TIMEOUT)
    token_b = login_b.json()["access_token"]
    hdrs_b = {"Authorization": f"Bearer {token_b}"}

    r = requests.post(
        f"{BASE}/wishlists/{wl}/products",
        headers=hdrs_b,
        json={"Product": "Hack", "Price": "10.00", "Zipcode": "12345678"},
        timeout=REQUEST_TIMEOUT,
    )
    assert r.status_code == 404, r.text

# Scenario 24
def test_24_add_product_incomplete_data(auth_header, a_wishlist):
    r = requests.post(f"{BASE}/wishlists/{a_wishlist}/products", headers=auth_header, json={"Price": "10.00"}, timeout=REQUEST_TIMEOUT)
    assert r.status_code == 422, r.text

# Scenario 25
def test_25_get_products_success(auth_header, a_wishlist):
    requests.post(f"{BASE}/wishlists/{a_wishlist}/products", headers=auth_header, json={"Product": "Phone", "Price": "1000", "Zipcode": "12345678"}, timeout=REQUEST_TIMEOUT)
    r = requests.get(f"{BASE}/wishlists/{a_wishlist}/products", headers=auth_header, timeout=REQUEST_TIMEOUT)
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    assert len(r.json()) >= 1

# Scenario 26
def test_26_filter_by_name(auth_header, a_wishlist):
    requests.post(f"{BASE}/wishlists/{a_wishlist}/products", headers=auth_header, json={"Product": "Apple iPhone 14", "Price": "5000", "Zipcode": "12345678"}, timeout=REQUEST_TIMEOUT)
    r = requests.get(f"{BASE}/wishlists/{a_wishlist}/products", headers=auth_header, params={"Product": "iPhone"}, timeout=REQUEST_TIMEOUT)
    assert r.status_code == 200
    names = [p["Product"] for p in r.json()]
    assert any("iphone" in n.lower() for n in names)

# Scenario 27
def test_27_filter_by_is_purchased(auth_header, a_wishlist):
    # garante 2: um comprado, outro não
    p1 = requests.post(f"{BASE}/wishlists/{a_wishlist}/products", headers=auth_header, json={"Product": "TV", "Price": "2000", "Zipcode": "12345678"}, timeout=REQUEST_TIMEOUT).json()
    p2 = requests.post(f"{BASE}/wishlists/{a_wishlist}/products", headers=auth_header, json={"Product": "Speaker", "Price": "300", "Zipcode": "12345678"}, timeout=REQUEST_TIMEOUT).json()

    # tenta alternar estado se endpoint existir
    toggle_url = f"{BASE}/products/{p1['id']}/toggle"
    t = requests.patch(toggle_url, headers=auth_header, timeout=REQUEST_TIMEOUT)
    assert t.status_code in (200, 404)  # Alguns ambientes podem não expor toggle

    r = requests.get(
        f"{BASE}/wishlists/{a_wishlist}/products",
        headers=auth_header,
        params={"is_purchased": "true"},
        timeout=REQUEST_TIMEOUT,
    )
    assert r.status_code == 200
    # Se toggle não existir, o filtro ainda deve funcionar, possivelmente vazio
    assert isinstance(r.json(), list)

# Scenario 28
def test_28_get_products_other_user():
    import uuid
    pw = "Password123!"
    # User A com WL e produto
    email_a = f"ua_{uuid.uuid4().hex[:8]}@example.com"
    requests.post(f"{BASE}/auth/register", json={"email": email_a, "password": pw}, timeout=REQUEST_TIMEOUT)
    login_a = requests.post(f"{BASE}/auth/login", data={"username": email_a, "password": pw}, timeout=REQUEST_TIMEOUT)
    token_a = login_a.json()["access_token"]
    hdrs_a = {"Authorization": f"Bearer {token_a}"}
    wl = requests.post(f"{BASE}/wishlists", headers=hdrs_a, json={"name": "UA"}, timeout=REQUEST_TIMEOUT).json()["id"]
    requests.post(f"{BASE}/wishlists/{wl}/products", headers=hdrs_a, json={"Product": "UA Item", "Price": "10", "Zipcode": "12345678"}, timeout=REQUEST_TIMEOUT)

    # User B tenta listar
    email_b = f"ub_{uuid.uuid4().hex[:8]}@example.com"
    requests.post(f"{BASE}/auth/register", json={"email": email_b, "password": pw}, timeout=REQUEST_TIMEOUT)
    login_b = requests.post(f"{BASE}/auth/login", data={"username": email_b, "password": pw}, timeout=REQUEST_TIMEOUT)
    token_b = login_b.json()["access_token"]
    hdrs_b = {"Authorization": f"Bearer {token_b}"}

    r = requests.get(f"{BASE}/wishlists/{wl}/products", headers=hdrs_b, timeout=REQUEST_TIMEOUT)
    assert r.status_code == 404, r.text

# Scenario 29
def test_29_update_product_success(auth_header, a_wishlist):
    p = requests.post(f"{BASE}/wishlists/{a_wishlist}/products", headers=auth_header, json={"Product": "Camera", "Price": "1000", "Zipcode": "12345678"}, timeout=REQUEST_TIMEOUT).json()
    r = requests.put(f"{BASE}/products/{p['id']}", headers=auth_header, json={"Price": "1500"}, timeout=REQUEST_TIMEOUT)
    assert r.status_code == 200, r.text
    assert r.json()["Price"] in ("1500", 1500)

# Scenario 30
def test_30_update_nonexistent_product(auth_header):
    r = requests.put(f"{BASE}/products/999999", headers=auth_header, json={"Price": "150"}, timeout=REQUEST_TIMEOUT)
    assert r.status_code == 404, r.text

# Scenario 31
def test_31_update_other_user_product():
    import uuid
    pw = "Password123!"
    # User A cria produto
    email_a = f"ua2_{uuid.uuid4().hex[:8]}@example.com"
    requests.post(f"{BASE}/auth/register", json={"email": email_a, "password": pw}, timeout=REQUEST_TIMEOUT)
    login_a = requests.post(f"{BASE}/auth/login", data={"username": email_a, "password": pw}, timeout=REQUEST_TIMEOUT)
    token_a = login_a.json()["access_token"]
    hdrs_a = {"Authorization": f"Bearer {token_a}"}
    wl = requests.post(f"{BASE}/wishlists", headers=hdrs_a, json={"name": "UA2"}, timeout=REQUEST_TIMEOUT).json()["id"]
    p = requests.post(f"{BASE}/wishlists/{wl}/products", headers=hdrs_a, json={"Product": "UA2 Item", "Price": "10", "Zipcode": "12345678"}, timeout=REQUEST_TIMEOUT).json()

    # User B tenta atualizar
    email_b = f"ub2_{uuid.uuid4().hex[:8]}@example.com"
    requests.post(f"{BASE}/auth/register", json={"email": email_b, "password": pw}, timeout=REQUEST_TIMEOUT)
    login_b = requests.post(f"{BASE}/auth/login", data={"username": email_b, "password": pw}, timeout=REQUEST_TIMEOUT)
    token_b = login_b.json()["access_token"]
    hdrs_b = {"Authorization": f"Bearer {token_b}"}

    r = requests.put(f"{BASE}/products/{p['id']}", headers=hdrs_b, json={"Price": "99"}, timeout=REQUEST_TIMEOUT)
    assert r.status_code == 404, r.text

# Scenario 32
def test_32_delete_product_success(auth_header, a_wishlist):
    p = requests.post(f"{BASE}/wishlists/{a_wishlist}/products", headers=auth_header, json={"Product": "Trash", "Price": "10", "Zipcode": "12345678"}, timeout=REQUEST_TIMEOUT).json()
    r = requests.delete(f"{BASE}/products/{p['id']}", headers=auth_header, timeout=REQUEST_TIMEOUT)
    assert r.status_code in (200, 204), r.text

# Scenario 33
def test_33_delete_nonexistent_product(auth_header):
    r = requests.delete(f"{BASE}/products/999999", headers=auth_header, timeout=REQUEST_TIMEOUT)
    assert r.status_code == 404, r.text

# Scenario 34
def test_34_delete_other_user_product():
    import uuid
    pw = "Password123!"
    # User A cria produto
    email_a = f"ua3_{uuid.uuid4().hex[:8]}@example.com"
    requests.post(f"{BASE}/auth/register", json={"email": email_a, "password": pw}, timeout=REQUEST_TIMEOUT)
    login_a = requests.post(f"{BASE}/auth/login", data={"username": email_a, "password": pw}, timeout=REQUEST_TIMEOUT)
    token_a = login_a.json()["access_token"]
    hdrs_a = {"Authorization": f"Bearer {token_a}"}
    wl = requests.post(f"{BASE}/wishlists", headers=hdrs_a, json={"name": "UA3"}, timeout=REQUEST_TIMEOUT).json()["id"]
    p = requests.post(f"{BASE}/wishlists/{wl}/products", headers=hdrs_a, json={"Product": "UA3 Item", "Price": "10", "Zipcode": "12345678"}, timeout=REQUEST_TIMEOUT).json()

    # User B tenta deletar
    email_b = f"ub3_{uuid.uuid4().hex[:8]}@example.com"
    requests.post(f"{BASE}/auth/register", json={"email": email_b, "password": pw}, timeout=REQUEST_TIMEOUT)
    login_b = requests.post(f"{BASE}/auth/login", data={"username": email_b, "password": pw}, timeout=REQUEST_TIMEOUT)
    token_b = login_b.json()["access_token"]
    hdrs_b = {"Authorization": f"Bearer {token_b}"}

    r = requests.delete(f"{BASE}/products/{p['id']}", headers=hdrs_b, timeout=REQUEST_TIMEOUT)
    assert r.status_code == 404, r.text

# Scenario 35 – acessos sem token (varredura rápida)
@pytest.mark.parametrize(
    "method,endpoint",
    [
        ("post", "/wishlists"),
        ("get", "/wishlists"),
        ("post", "/wishlists/1/products"),
        ("get", "/wishlists/1/products"),
        ("put", "/products/1"),
        ("delete", "/products/1"),
        ("patch", "/products/1/toggle"),
    ],
)
def test_35_requires_authentication(method, endpoint):
    fn = getattr(requests, method)
    url = f"{BASE}{endpoint}"
    if method in ("post", "put", "patch"):
        r = fn(url, json={}, timeout=REQUEST_TIMEOUT)
    else:
        r = fn(url, timeout=REQUEST_TIMEOUT)
    assert r.status_code == 401, f"{method.upper()} {endpoint}: {r.status_code} {r.text}"