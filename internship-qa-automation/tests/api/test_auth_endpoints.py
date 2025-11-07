import uuid, pytest
from config.env_config import REQUEST_TIMEOUT

pytestmark = [pytest.mark.api, pytest.mark.auth]

def test_register_success(http, api_url):
    rnd = uuid.uuid4().hex[:8]
    body = {"username": f"user_{rnd}", "email": f"user_{rnd}@example.com", "password": "Abcd1234!"}
    r = http.post(f"{api_url}/auth/register", json=body, timeout=REQUEST_TIMEOUT)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["email"] == body["email"]
    assert data["username"] == body["username"]

def test_register_duplicate_email(http, api_url):
    rnd = uuid.uuid4().hex[:8]
    email = f"dup_{rnd}@example.com"
    body = {"username": f"dup_{rnd}", "email": email, "password": "Abcd1234!"}
    r1 = http.post(f"{api_url}/auth/register", json=body, timeout=REQUEST_TIMEOUT)
    assert r1.status_code == 200, r1.text
    r2 = http.post(f"{api_url}/auth/register", json=body, timeout=REQUEST_TIMEOUT)
    assert r2.status_code == 400, f"esperado 400 duplicado, veio {r2.status_code}: {r2.text}"

@pytest.mark.parametrize("email", ["x", "foo@", "bar.com", "x@x"])
def test_register_invalid_email(http, api_url, email):
    rnd = uuid.uuid4().hex[:5]
    body = {"username": f"inv_{rnd}", "email": email, "password": "Abcd1234!"}
    r = http.post(f"{api_url}/auth/register", json=body, timeout=REQUEST_TIMEOUT)
    assert r.status_code == 422, f"esperado 422, veio {r.status_code}: {r.text}"

def test_login_success_with_seed(http, api_url, seed_credentials):
    r = http.post(f"{api_url}/auth/login", json=seed_credentials, timeout=REQUEST_TIMEOUT)
    assert r.status_code == 200, r.text
    data = r.json()
    assert "access_token" in data and data.get("token_type") == "bearer"

def test_login_wrong_password(http, api_url, seed_credentials):
    bad = {"email": seed_credentials["email"], "password": "errada!"}
    r = http.post(f"{api_url}/auth/login", json=bad, timeout=REQUEST_TIMEOUT)
    assert r.status_code == 401, f"esperado 401, veio {r.status_code}"
