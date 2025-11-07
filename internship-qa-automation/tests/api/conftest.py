import uuid
import pytest
import requests
from config.env_config import API_BASE_URL, REQUEST_TIMEOUT

@pytest.fixture(scope="session")
def api_url():
    return API_BASE_URL.rstrip("/")

@pytest.fixture(scope="session")
def http():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    return s

def _auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture(scope="session")
def seed_credentials():
    # usuário que vem no setup.json da sua API
    return {"email": "projeto@example.com", "password": "Senha123!"}

@pytest.fixture(scope="session")
def bearer_token(http, api_url, seed_credentials):
    # tenta logar no seed; se falhar, cria um usuário novo e loga nele
    r = http.post(f"{api_url}/auth/login",
                  json={"email": seed_credentials["email"], "password": seed_credentials["password"]},
                  timeout=REQUEST_TIMEOUT)
    if r.status_code == 200:
        return r.json()["access_token"]

    # cria um usuário “descartável”
    rnd = uuid.uuid4().hex[:8]
    email = f"qa_{rnd}@example.com"
    payload = {"username": f"qa_{rnd}", "email": email, "password": "Abcd1234!"}
    rr = http.post(f"{api_url}/auth/register", json=payload, timeout=REQUEST_TIMEOUT)
    assert rr.status_code == 200, f"Falha registrando usuário descartável: {rr.status_code} {rr.text}"

    rl = http.post(f"{api_url}/auth/login",
                   json={"email": email, "password": "Abcd1234!"},
                   timeout=REQUEST_TIMEOUT)
    assert rl.status_code == 200, f"Falha ao logar após registro: {rl.status_code} {rl.text}"
    return rl.json()["access_token"]

@pytest.fixture
def authz(bearer_token):
    return _auth_headers(bearer_token)
