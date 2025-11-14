from pages.home_page import HomePage
import time

def test_cenario_7(driver):
    dados = {
        "email": "testadortestantedostestes@gmail.com",
        "senha_invalida": "senhaerrada"
    }
    email = dados["email"]
    senha = dados["senha_invalida"]
    texto_esperado = "Usuário e/ou senha incorretos"
    home_page = HomePage(driver)
    home_page.open_home()
    login_page = home_page.go_to_login()
    login_page.clicar_email_password()
    login_page.colocar_email(email)
    login_page.colocar_senha(senha)
    login_page.clicar_botao_entrar()
    time.sleep(3)
    assert login_page.pegar_texto_senha_invalida() == texto_esperado
    
    
    
