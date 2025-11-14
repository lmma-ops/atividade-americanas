# tests_api/conftest.py
import os
import time
import uuid
import pytest
import requests


API_BASE_URL = os.environ.get("API_BASE_URL", "http://127.0.0.1:8000")


class HttpClient(requests.Session):
    def __init__(self, base_url: str):
        super().__init__()
        self.base_url = base_url.rstrip("/")
        self.last_response = None

    def request(self, method, url, **kwargs):
        full_url = url if url.startswith("http") else f"{self.base_url}{url}"
        response = super().request(method, full_url, **kwargs)
        self.last_response = response
        return response


@pytest.fixture(scope="session")
def http_client() -> HttpClient:
    return HttpClient(API_BASE_URL)


def _uniq() -> str:
    return uuid.uuid4().hex[:8]


def generate_unique_username(prefix: str = "usuario") -> str:
    return f"{prefix}_{int(time.time()*1000)}_{_uniq()}"


def generate_unique_email(domain: str = "exemplo.com") -> str:
    return f"usuario_{int(time.time()*1000)}_{_uniq()}@{domain}"


def create_new_user_payload() -> dict:
    return {
        "email": generate_unique_email(),
        "password": "Senha123!",
        "username": generate_unique_username(),
    }


def register_user(user_payload: dict) -> requests.Response:
    return requests.post(f"{API_BASE_URL}/auth/register", json=user_payload, timeout=10)


def login_and_get_token(email: str, password: str) -> str:
    response = requests.post(
        f"{API_BASE_URL}/auth/login",
        json={"email": email, "password": password},
        timeout=10,
    )
    response.raise_for_status()
    body = response.json()
    return body["access_token"]


def build_auth_header(access_token: str) -> dict:
    return {"Authorization": f"Bearer {access_token}"}


def create_wishlist(access_token: str, name: str | None = None) -> requests.Response:
    wishlist_name = name or f"wishlist_{int(time.time()*1000)}_{_uniq()}"
    return requests.post(
        f"{API_BASE_URL}/wishlists",
        json={"name": wishlist_name},
        headers=build_auth_header(access_token),
        timeout=10,
    )


def add_product_to_wishlist(
    access_token: str,
    wishlist_id: int,
    Product: str = "Produto Genérico",
    Price: str = "10.00",
    Zipcode: str = "01001-000",
    delivery_estimate: str = "2 dias",
    shipping_fee: str = "0.00",
) -> requests.Response:
    payload = {
        "Product": Product,
        "Price": Price,
        "Zipcode": Zipcode,
        "delivery_estimate": delivery_estimate,
        "shipping_fee": shipping_fee,
    }
    return requests.post(
        f"{API_BASE_URL}/wishlists/{wishlist_id}/products",
        json=payload,
        headers=build_auth_header(access_token),
        timeout=10,
    )


def list_wishlist_products(
    access_token: str,
    wishlist_id: int,
    params: dict | None = None,
) -> requests.Response:
    return requests.get(
        f"{API_BASE_URL}/wishlists/{wishlist_id}/products",
        params=params or {},
        headers=build_auth_header(access_token),
        timeout=10,
    )


def update_product(
    access_token: str,
    product_id: int,
    **fields,
) -> requests.Response:
    return requests.put(
        f"{API_BASE_URL}/products/{product_id}",
        json=fields,
        headers=build_auth_header(access_token),
        timeout=10,
    )


def delete_product(
    access_token: str,
    product_id: int,
) -> requests.Response:
    return requests.delete(
        f"{API_BASE_URL}/products/{product_id}",
        headers=build_auth_header(access_token),
        timeout=10,
    )
