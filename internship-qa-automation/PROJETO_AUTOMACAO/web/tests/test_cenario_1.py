import re
import time
import pytest

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.temp_mail_page import TempMailPage
from pages.authentication_page import AuthenticationPage
from pages.profile_page import ProfilePage

@pytest.mark.web
def test_cenario_1(driver):
    home = HomePage(driver)
    home.open_home()
    login = home.go_to_login()

    driver.switch_to.new_window('tab')
    temp = TempMailPage(driver)
    temp.open_site()
    email_temp = temp.current_email()
    assert "@" in email_temp

    driver.switch_to.window(driver.window_handles[0])
    login.enviar_email_para_receber_codigo(email_temp)

    driver.switch_to.window(driver.window_handles[1])
    codigo_login = temp.wait_and_get_code("Seu código de acesso é")
    assert re.fullmatch(r"\d{6}", codigo_login)

    driver.switch_to.window(driver.window_handles[0])
    login.informar_codigo_e_confirmar(codigo_login)
    time.sleep(2)
    assert home.ve_se_ta_na_homepage().startswith(home.URL)

    
    header_txt = home.texto_email_no_header().lower()
    assert email_temp.split("@")[0].lower() in header_txt

    
    perfil = home.ir_para_cadastro()
    assert email_temp.split("@")[0].lower() in perfil.texto_email_cadastro().lower()

    
    driver.back()  
    auth = home.ir_para_autenticacao()
    auth.abrir_definir_senha()

    driver.switch_to.window(driver.window_handles[1])
    codigo_senha = temp.wait_and_get_code("Seu código de verificação")
    assert re.fullmatch(r"\d{6}", codigo_senha)

    driver.switch_to.window(driver.window_handles[0])
    auth.preencher_codigo(codigo_senha)

    # regra 1: < 8 caracteres
    senha_menor_8 = "Abc12!"
    auth.digitar_nova_senha(senha_menor_8)
    time.sleep(0.5)
    assert auth.botao_salvar_esta_desabilitado() is True
    auth.limpar_nova_senha()

    # regra 2: sem número
    senha_sem_numero = "Abcdefgh"
    auth.digitar_nova_senha(senha_sem_numero)
    time.sleep(0.5)
    assert auth.botao_salvar_esta_desabilitado() is True
    auth.limpar_nova_senha()

    # regra 3: sem minúscula
    senha_sem_minuscula = "ABCDEFG1"
    auth.digitar_nova_senha(senha_sem_minuscula)
    time.sleep(0.5)
    assert auth.botao_salvar_esta_desabilitado() is True
    auth.limpar_nova_senha()

    # regra 4: sem maiúscula
    senha_sem_maiuscula = "abcdefg1"
    auth.digitar_nova_senha(senha_sem_maiuscula)
    time.sleep(0.5)
    assert auth.botao_salvar_esta_desabilitado() is True
    auth.limpar_nova_senha()

    # senha válida
    senha_valida = "Teste123!"
    auth.digitar_nova_senha(senha_valida)
    time.sleep(0.5)
    assert auth.botao_salvar_esta_desabilitado() is False
    auth.clicar_salvar()

    time.sleep(2)
    mask = auth.pegar_texto_mascarado().replace("•", "*").replace("●", "*")
    assert len(mask) == len(senha_valida)
