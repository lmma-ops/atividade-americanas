from pages.home_page import HomePage
import time

def test_cenario_6(driver):
    dados = {
        "email": "testadortestantedostestes@gmail.com",
        "senha_valida": "Teste123!" 
    }
    email = dados["email"]
    senha = dados["senha_valida"]

    home_page = HomePage(driver)
    home_page.open_home()
    login_page = home_page.go_to_login()
    login_page.clicar_email_password()
    login_page.colocar_email(email)
    login_page.colocar_senha(senha)
    login_page.clicar_botao_entrar()
    time.sleep(3)

    assert home_page.ve_se_ta_na_homepage() == "https://www.americanas.com.br/"
