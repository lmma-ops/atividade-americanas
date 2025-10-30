# web/tests/test_login.py
import pytest
import time
# As importações agora começam em 'web', a nossa pasta principal
from web.pages.home_page import HomePage
from web.pages.login_page import LoginPage
# O 'driver' vem automaticamente do conftest.py na pasta 'web'

# --- Configurações de Teste ---
# !! TROQUE ESTES DADOS PELOS SEUS DADOS DE TESTE REAIS !!
EMAIL_VALIDO = "seu-email-real@gmail.com"  
SENHA_VALIDA = "SuaSenhaReal123"          
SENHA_INCORRETA = "senha-errada-999"

def test_cenario_6_login_com_sucesso(driver):
    """ [Cenário 6] Valida o login com credenciais corretas. """
    print(f"\nRodando Cenário 6: Login com Sucesso")

    home_page = HomePage(driver) # Isto abre o site
    home_page.go_to_login_page()

    login_page = LoginPage(driver)
    login_page.do_login(EMAIL_VALIDO, SENHA_VALIDA)

    time.sleep(5) # Espera o login e o redirecionamento

    header_text = home_page.get_header_text()
    assert EMAIL_VALIDO in header_text, f"Validação falhou! O e-mail '{EMAIL_VALIDO}' não foi encontrado."
    print("Cenário 6 passou: Login validado com sucesso.")

def test_cenario_7_login_senha_incorreta(driver):
    """ [Cenário 7] Valida a mensagem de erro com senha incorreta. """
    print(f"\nRodando Cenário 7: Login com Senha Incorreta")

    home_page = HomePage(driver) # Isto abre o site
    home_page.go_to_login_page()

    login_page = LoginPage(driver)
    login_page.do_login(EMAIL_VALIDO, SENHA_INCORRETA)

    time.sleep(2) # Espera a mensagem de erro

    page_text = login_page.get_page_text_for_error()
    assert "E-mail ou senha inválidos" in page_text, "Validação falhou! Mensagem de erro não encontrada."
    print("Cenário 7 passou: Mensagem de erro validada.")