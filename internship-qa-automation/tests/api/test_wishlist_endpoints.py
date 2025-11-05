import pytest
import requests
from config.env_config import API_BASE_URL, REQUEST_TIMEOUT

pytestmark = [pytest.mark.api, pytest.mark.wishlist]

BASE = API_BASE_URL.rstrip("/")

def test_14_create_wishlist_success(auth_header):
    name = "My Tech Gadgets"
    r = requests.post(f"{BASE}/wishlists", headers=auth_header, json={"name": name}, timeout=REQUEST_TIMEOUT)
    assert r.status_code in (200, 201), r.text
    body = r.json()
    assert body["name"] == name
    assert "id" in body and "owner_id" in body

def test_15_create_wishlist_duplicate_name(auth_header):
    name = "Travel Plans"
    r1 = requests.post(f"{BASE}/wishlists", headers=auth_header, json={"name": name}, timeout=REQUEST_TIMEOUT)
    assert r1.status_code in (200, 201), r1.text
    r2 = requests.post(f"{BASE}/wishlists", headers=auth_header, json={"name": name}, timeout=REQUEST_TIMEOUT)
    assert r2.status_code == 409, r2.text

def test_16_create_wishlist_unauthenticated():
    r = requests.post(f"{BASE}/wishlists", json={"name": "Nope"}, timeout=REQUEST_TIMEOUT)
    assert r.status_code == 401, r.text

def test_17_create_wishlist_invalid_data(auth_header):
    r = requests.post(f"{BASE}/wishlists", headers=auth_header, json={}, timeout=REQUEST_TIMEOUT)
    assert r.status_code == 422, r.text

def test_18_get_all_wishlists(auth_header):
    # garante pelo menos uma
    requests.post(f"{BASE}/wishlists", headers=auth_header, json={"name": "List A"}, timeout=REQUEST_TIMEOUT)
    r = requests.get(f"{BASE}/wishlists", headers=auth_header, timeout=REQUEST_TIMEOUT)
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    assert len(r.json()) >= 1

def test_19_get_when_none_exists(auth_header):
    # cria novo usuário sem listas
    import uuid, requests as rq
    email = f"fresh_{uuid.uuid4().hex[:8]}@example.com"
    pw = "Password123!"
    rq.post(f"{BASE}/auth/register", json={"email": email, "password": pw}, timeout=REQUEST_TIMEOUT)
    login = rq.post(f"{BASE}/auth/login", data={"username": email, "password": pw}, timeout=REQUEST_TIMEOUT)
    token = login.json()["access_token"]
    hdrs = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{BASE}/wishlists", headers=hdrs, timeout=REQUEST_TIMEOUT)
    assert r.status_code == 200
    assert r.json() == []

def test_20_get_wishlists_unauthenticated():
    r = requests.get(f"{BASE}/wishlists", timeout=REQUEST_TIMEOUT)
    assert r.status_code == 401