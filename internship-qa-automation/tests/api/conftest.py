import uuid
import pytest
import requests
from config.env_config import API_BASE_URL, REQUEST_TIMEOUT



@pytest.fixture(scope="session")
def base_url():
    return API_BASE_URL.rstrip("/")

@pytest.fixture()
def unique_email():
    # Gera e-mail único por teste
    return f"qa_{uuid.uuid4().hex[:10]}@example.com"

@pytest.fixture()
def strong_password():
    return "StrongPass123!"

@pytest.fixture()
def register_user(base_url, unique_email, strong_password):
    payload = {"email": unique_email, "password": strong_password}
    r = requests.post(f"{base_url}/auth/register", json=payload, timeout=REQUEST_TIMEOUT)
    # Alguns ambientes podem retornar 200 ou 201; o desafio cita 200 OK
    assert r.status_code in (200, 201), f"Falha ao registrar usuário: {r.text}"
    return {"email": unique_email, "password": strong_password, "data": r.json()}

@pytest.fixture()
def login_token(base_url, register_user):
    payload = {"username": register_user["email"], "password": register_user["password"]}
    r = requests.post(f"{base_url}/auth/login", data=payload, timeout=REQUEST_TIMEOUT)
    assert r.status_code == 200, f"Falha no login: {r.text}"
    token = r.json().get("access_token")
    assert token, f"Resposta de login sem access_token: {r.text}"
    return token

@pytest.fixture()
def auth_header(login_token):
    return {"Authorization": f"Bearer {login_token}"}

@pytest.fixture()
def create_wishlist(base_url, auth_header):
    def _create(name):
        r = requests.post(
            f"{base_url}/wishlists",
            headers=auth_header,
            json={"name": name},
            timeout=REQUEST_TIMEOUT,
        )
        return r
    return _create

@pytest.fixture()
def create_product(base_url, auth_header):
    def _create(wishlist_id: int, product_name: str = "New Gadget", price: str = "99.99", zipcode: str = "12345678"):
        r = requests.post(
            f"{base_url}/wishlists/{wishlist_id}/products",
            headers=auth_header,
            json={"Product": product_name, "Price": price, "Zipcode": zipcode},
            timeout=REQUEST_TIMEOUT,
        )
        return r
    return _create