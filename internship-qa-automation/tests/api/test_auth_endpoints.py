import pytest
import requests
from config.env_config import API_BASE_URL, REQUEST_TIMEOUT

pytestmark = pytest.mark.api

BASE = API_BASE_URL.rstrip("/")

@pytest.mark.auth
def test_08_successful_user_registration(unique_email):
    payload = {"email": unique_email, "password": "Password123"}
    r = requests.post(f"{BASE}/auth/register", json=payload, timeout=REQUEST_TIMEOUT)
    assert r.status_code in (200, 201)
    body = r.json()
    assert body.get("email") == payload["email"]
    assert "password" not in body

@pytest.mark.auth
def test_09_registration_existing_email(register_user):
    email = register_user["email"]
    payload = {"email": email, "password": "AnotherPass123"}
    r = requests.post(f"{BASE}/auth/register", json=payload, timeout=REQUEST_TIMEOUT)
    assert r.status_code in (400, 409), r.text

@pytest.mark.auth
@pytest.mark.parametrize(
    "payload",
    [
        {"email": "not-an-email", "password": "Password123"},
        {"email": "invalid@example.com"},  # sem password
    ],
)
def test_10_registration_invalid_data(payload):
    r = requests.post(f"{BASE}/auth/register", json=payload, timeout=REQUEST_TIMEOUT)
    assert r.status_code == 422, r.text

@pytest.mark.auth
def test_11_successful_login(register_user):
    payload = {"username": register_user["email"], "password": register_user["password"]}
    r = requests.post(f"{BASE}/auth/login", data=payload, timeout=REQUEST_TIMEOUT)
    assert r.status_code == 200
    data = r.json()
    assert data.get("token_type") == "bearer"
    assert data.get("access_token")

@pytest.mark.auth
def test_12_login_incorrect_password(register_user):
    payload = {"username": register_user["email"], "password": "wrong_password"}
    r = requests.post(f"{BASE}/auth/login", data=payload, timeout=REQUEST_TIMEOUT)
    assert r.status_code == 401, r.text

@pytest.mark.auth
def test_13_login_non_existent_user():
    payload = {"username": "nouser@example.com", "password": "Any12345"}
    r = requests.post(f"{BASE}/auth/login", data=payload, timeout=REQUEST_TIMEOUT)
    assert r.status_code == 401, r.text

@pytest.mark.auth
@pytest.mark.parametrize(
    "headers",
    [None, {"Authorization": "Bearer invalidtoken"}],
)
def test_36_invalid_or_expired_token_in_auth_endpoints(headers):
    # Usa endpoint que requer token; exemplo wishlists
    r = requests.get(f"{BASE}/wishlists", headers=headers, timeout=REQUEST_TIMEOUT)
    assert r.status_code == 401, r.text