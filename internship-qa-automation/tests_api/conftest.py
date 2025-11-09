# tests_api/conftest.py
import os
import time
import random
import string
import pytest
import requests

# Base URL: usa variável de ambiente se existir, senão 127.0.0.1:8000
BASE_URL = os.environ.get("API_BASE_URL", "http://127.0.0.1:8000").rstrip("/")

# Usuário seed (já existe ao subir a API)
SEED_EMAIL = "projeto@example.com"
SEED_PASSWORD = "Senha123!"

def _rand(n=6) -> str:
    """String aleatória simples para evitar colisão de e-mail/nome."""
    alf = string.ascii_lowercase + string.digits
    return "".join(random.choices(alf, k=n))

@pytest.fixture(scope="session")
def api():
    """Sessão HTTP simples (requests) com base_url e timeout."""
    s = requests.Session()
    s.headers.update({"Accept": "application/json"})
    # Smoke: garante que a API está de pé
    r = s.get(f"{BASE_URL}/", timeout=10)
    assert r.status_code == 200, f"API fora do ar em {BASE_URL}: {r.status_code}"
    return s

# ------- HELPERS CURTINHOS (usados nos testes) -------

def novo_usuario():
    """Gera um payload válido de usuário único."""
    now = int(time.time())
    return {
        "username": f"user_{_rand()}",
        "email": f"u{now}_{_rand()}@example.com",
        "password": "Senha123!"
    }

def login_token(api_session, email=SEED_EMAIL, password=SEED_PASSWORD) -> str:
    r = api_session.post(f"{BASE_URL}/auth/login",
                         json={"email": email, "password": password},
                         timeout=10)
    assert r.status_code == 200, f"login falhou: {r.status_code} {r.text}"
    data = r.json()
    assert "access_token" in data, "login não retornou access_token"
    return data["access_token"]

def bearer(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}

def criar_wishlist(api_session, token: str, name: str = None):
    name = name or f"wl_{_rand()}"
    r = api_session.post(f"{BASE_URL}/wishlists",
                         json={"name": name},
                         headers=bearer(token),
                         timeout=10)
    assert r.status_code == 200, f"criar wishlist falhou: {r.status_code} {r.text}"
    return r.json()

def add_prod(api_session, token: str, wishlist_id: int, **over):
    payload = {
        "Product": "Produto QA",
        "Price": "199.90",
        "Zipcode": "01001-000",
        "delivery_estimate": "5 dias",
        "shipping_fee": "9.90",
    }
    payload.update(over)
    r = api_session.post(f"{BASE_URL}/wishlists/{wishlist_id}/products",
                         json=payload,
                         headers=bearer(token),
                         timeout=10)
    return r  # deixo o teste decidir o assert (200, 422, etc.)
