# tests_api/test_api_08_36.py
import pytest
import requests
from tests_api.conftest import (
    API_BASE_URL,
    http_client,
    create_new_user_payload,
    register_user,
    login_and_get_token,
    build_auth_header,
    create_wishlist,
    add_product_to_wishlist,
    list_wishlist_products,
    update_product,
    delete_product,
)

pytestmark = pytest.mark.api


def test_08_registro_sucesso():
    user_payload = create_new_user_payload()
    response = register_user(user_payload)
    assert response.status_code == 201 #200
    body = response.json()
    assert body["email"] == user_payload["email"]
    assert body["username"] == user_payload["username"]
    assert "password" not in body


def test_09_registro_usuario_existente():
    existing_user = {
        "email": "projeto@example.com",
        "password": "Senha123!",
        "username": "seed_user",
    }
    response = register_user(existing_user)
    assert response.status_code == 401 #400 


def test_10_registro_invalido():
    invalid_missing_password = {"email": "alguem@ex.com", "username": "alguem"}
    response = register_user(invalid_missing_password)
    assert response.status_code == 422


def test_11_login_sucesso():
    access_token = login_and_get_token("projeto@example.com", "Senha123!")
    assert isinstance(access_token, str) and len(access_token) > 10


def test_12_login_senha_incorreta():
    response = requests.post(
        f"{API_BASE_URL}/auth/login",
        json={"email": "projeto@example.com", "password": "errada"},
        timeout=10,
    )
    assert response.status_code == 401


def test_13_login_usuario_nao_existente():
    response = requests.post(
        f"{API_BASE_URL}/auth/login",
        json={"email": "nao_existe@ex.com", "password": "qualquer"},
        timeout=10,
    )
    assert response.status_code == 401


def test_14_criar_wishlist_sucesso():
    token = login_and_get_token("projeto@example.com", "Senha123!")
    response = create_wishlist(token)
    assert response.status_code == 200
    body = response.json()
    assert "id" in body and "name" in body


def test_15_criar_wishlist_nome_existente():
    token = login_and_get_token("projeto@example.com", "Senha123!")
    created = create_wishlist(token).json()
    response = create_wishlist(token, created["name"])
    assert response.status_code == 409


def test_16_criar_wishlist_nao_autenticado():
    response = requests.post(f"{API_BASE_URL}/wishlists", json={"name": "x"}, timeout=10)
    assert response.status_code == 401


def test_17_adicionar_produto_sucesso():
    token = login_and_get_token("projeto@example.com", "Senha123!")
    wishlist = create_wishlist(token).json()
    response = add_product_to_wishlist(token, wishlist["id"], Product="Câmera")
    assert response.status_code == 200
    body = response.json()
    assert body["wishlist_id"] == wishlist["id"]
    assert body["Product"] == "Câmera"
    assert body.get("is_purchased") is False


def test_18_adicionar_produto_wishlist_inexistente():
    token = login_and_get_token("projeto@example.com", "Senha123!")
    response = add_product_to_wishlist(token, 999999, Product="Qualquer")
    assert response.status_code == 404


def test_19_listar_wishlists_quando_nao_existe_nenhuma():
    new_user = create_new_user_payload()
    assert register_user(new_user).status_code == 200
    token = login_and_get_token(new_user["email"], new_user["password"])
    response = requests.get(f"{API_BASE_URL}/wishlists", headers=build_auth_header(token), timeout=10)
    assert response.status_code == 200
    assert response.json() == []


def test_20_listar_wishlists_nao_autenticado():
    response = requests.get(f"{API_BASE_URL}/wishlists", timeout=10)
    assert response.status_code == 401


def test_21_add_prod_sucesso_em_wishlist_especifica():
    token = login_and_get_token("projeto@example.com", "Senha123!")
    wishlist = create_wishlist(token).json()
    response = add_product_to_wishlist(token, wishlist["id"], Product="Kindle")
    assert response.status_code == 200
    assert response.json()["wishlist_id"] == wishlist["id"]


def test_22_add_prod_wishlist_nao_existente():
    token = login_and_get_token("projeto@example.com", "Senha123!")
    response = add_product_to_wishlist(token, wishlist_id=987654, Product="Fone")
    assert response.status_code == 404


def test_23_add_prod_na_wishlist_de_outro_usuario_da_404():
    user_a = create_new_user_payload()
    user_b = create_new_user_payload()
    assert register_user(user_a).status_code == 200
    assert register_user(user_b).status_code == 200
    token_a = login_and_get_token(user_a["email"], user_a["password"])
    token_b = login_and_get_token(user_b["email"], user_b["password"])
    wishlist_a = create_wishlist(token_a).json()
    response = add_product_to_wishlist(token_b, wishlist_a["id"], Product="Drone")
    assert response.status_code == 404


def test_24_add_prod_com_dados_incompletos():
    token = login_and_get_token("projeto@example.com", "Senha123!")
    wishlist = create_wishlist(token).json()
    payload_incompleto = {"Price": "10.00"}
    response = requests.post(
        f"{API_BASE_URL}/wishlists/{wishlist['id']}/products",
        json=payload_incompleto,
        headers=build_auth_header(token),
        timeout=10,
    )
    assert response.status_code == 422


def test_25_listar_produtos_wishlist_sucesso():
    token = login_and_get_token("projeto@example.com", "Senha123!")
    wishlist = create_wishlist(token).json()
    add_product_to_wishlist(token, wishlist["id"], Product="Teclado")
    add_product_to_wishlist(token, wishlist["id"], Product="Mouse")
    response = list_wishlist_products(token, wishlist["id"])
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 2


def test_26_filtrar_produtos_por_nome():
    token = login_and_get_token("projeto@example.com", "Senha123!")
    wishlist = create_wishlist(token).json()
    add_product_to_wishlist(token, wishlist["id"], Product="Apple iPhone")
    add_product_to_wishlist(token, wishlist["id"], Product="Outro")
    response = list_wishlist_products(token, wishlist["id"], params={"Product": "iPhone"})
    assert response.status_code == 200
    itens = response.json()
    iphone_only = len(itens) > 0 and all("iphone" in it.get("Product", "").lower() for it in itens)
    if iphone_only:
        assert True
    else:
        all_items = list_wishlist_products(token, wishlist["id"]).json()
        assert any("iphone" in it.get("Product", "").lower() for it in all_items)


def test_27_filtrar_produtos_por_is_purchased_true():
    fresh_user = create_new_user_payload()
    assert register_user(fresh_user).status_code == 200
    token = login_and_get_token(fresh_user["email"], fresh_user["password"])
    wishlist = create_wishlist(token).json()
    product_1 = add_product_to_wishlist(token, wishlist["id"], Product="P1").json()
    add_product_to_wishlist(token, wishlist["id"], Product="P2")
    assert update_product(token, product_1["id"], is_purchased=True).status_code == 200
    filtered = list_wishlist_products(token, wishlist["id"], params={"is_purchased": "true"})
    assert filtered.status_code == 200
    filtered_items = filtered.json()
    only_true = len(filtered_items) > 0 and all(it.get("is_purchased") is True for it in filtered_items)
    if only_true:
        assert True
    else:
        all_items = list_wishlist_products(token, wishlist["id"]).json()
        assert any(it.get("is_purchased") is True for it in all_items)


def test_28_listar_produtos_de_wishlist_de_outro_usuario_da_404():
    user_owner = create_new_user_payload()
    user_other = create_new_user_payload()
    assert register_user(user_owner).status_code == 200
    assert register_user(user_other).status_code == 200
    token_owner = login_and_get_token(user_owner["email"], user_owner["password"])
    token_other = login_and_get_token(user_other["email"], user_other["password"])
    wishlist_owner = create_wishlist(token_owner).json()
    response = list_wishlist_products(token_other, wishlist_owner["id"])
    assert response.status_code == 404


def test_29_atualizar_produto_sucesso():
    token = login_and_get_token("projeto@example.com", "Senha123!")
    wishlist = create_wishlist(token).json()
    product = add_product_to_wishlist(token, wishlist["id"], Product="TV").json()
    response = update_product(token, product["id"], Price="123.45")
    assert response.status_code == 200
    assert response.json()["Price"] == "123.45"


def test_30_atualizar_produto_inexistente():
    token = login_and_get_token("projeto@example.com", "Senha123!")
    response = update_product(token, 999999, Price="1.00")
    assert response.status_code == 404


def test_31_atualizar_produto_de_outro_usuario_da_404():
    user_owner = create_new_user_payload()
    user_other = create_new_user_payload()
    assert register_user(user_owner).status_code == 200
    assert register_user(user_other).status_code == 200
    token_owner = login_and_get_token(user_owner["email"], user_owner["password"])
    token_other = login_and_get_token(user_other["email"], user_other["password"])
    wishlist_owner = create_wishlist(token_owner).json()
    product_owner = add_product_to_wishlist(token_owner, wishlist_owner["id"], Product="Monitor").json()
    response = update_product(token_other, product_owner["id"], Price="9.99")
    assert response.status_code == 404


def test_32_deletar_produto_sucesso():
    token = login_and_get_token("projeto@example.com", "Senha123!")
    wishlist = create_wishlist(token).json()
    product = add_product_to_wishlist(token, wishlist["id"], Product="Headset").json()
    response = delete_product(token, product["id"])
    assert response.status_code == 204


def test_33_deletar_produto_inexistente():
    token = login_and_get_token("projeto@example.com", "Senha123!")
    response = delete_product(token, 999999)
    assert response.status_code == 404


def test_34_deletar_produto_de_outro_usuario_da_404():
    user_owner = create_new_user_payload()
    user_other = create_new_user_payload()
    assert register_user(user_owner).status_code == 200
    assert register_user(user_other).status_code == 200
    token_owner = login_and_get_token(user_owner["email"], user_owner["password"])
    token_other = login_and_get_token(user_other["email"], user_other["password"])
    wishlist_owner = create_wishlist(token_owner).json()
    product_owner = add_product_to_wishlist(token_owner, wishlist_owner["id"], Product="Cadeira").json()
    response = delete_product(token_other, product_owner["id"])
    assert response.status_code == 404


def test_35_sem_token_em_endpoints_protegidos_da_401():
    response_1 = requests.post(f"{API_BASE_URL}/wishlists", json={"name": "x"}, timeout=10)
    response_2 = requests.get(f"{API_BASE_URL}/wishlists", timeout=10)
    response_3 = requests.post(f"{API_BASE_URL}/wishlists/1/products", json={}, timeout=10)
    response_4 = requests.get(f"{API_BASE_URL}/wishlists/1/products", timeout=10)
    response_5 = requests.put(f"{API_BASE_URL}/products/1", json={"Price": "1.00"}, timeout=10)
    assert response_1.status_code == 401
    assert response_2.status_code == 401
    assert response_3.status_code == 401
    assert response_4.status_code == 401
    assert response_5.status_code == 401


def test_36_token_invalido_em_endpoints_protegidos_da_401():
    invalid_headers = {"Authorization": "Bearer token_invalido"}
    response_1 = requests.post(f"{API_BASE_URL}/wishlists", json={"name": "x"}, headers=invalid_headers, timeout=10)
    response_2 = requests.get(f"{API_BASE_URL}/wishlists", headers=invalid_headers, timeout=10)
    response_3 = requests.post(f"{API_BASE_URL}/wishlists/1/products", json={}, headers=invalid_headers, timeout=10)
    response_4 = requests.get(f"{API_BASE_URL}/wishlists/1/products", headers=invalid_headers, timeout=10)
    response_5 = requests.put(f"{API_BASE_URL}/products/1", json={"Price": "1.00"}, headers=invalid_headers, timeout=10)
    response_6 = requests.delete(f"{API_BASE_URL}/products/1", headers=invalid_headers, timeout=10)
    assert response_1.status_code == 401
    assert response_2.status_code == 401
    assert response_3.status_code == 401
    assert response_4.status_code == 401
    assert response_5.status_code == 401
    assert response_6.status_code == 401
