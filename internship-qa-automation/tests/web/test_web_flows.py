import pytest, time
from .pages.home_page import HomePage
from .pages.login_page import LoginPage
from .pages.temp_mail_page import TempMailPage
from .pages.base_page import BasePage

pytestmark = pytest.mark.e2e

def test_full_registration_and_password_flow(browser):
    base = BasePage(browser)

    # 1) HOME → abrir e ir para login
    home = HomePage(browser)
    home.open_home()
    assert "americanas" in home.current_url.lower()
    assert home.go_to_login()  # tenta clicar; se não, fallback por URL

    # 2) LOGIN (aba 1) + abrir TEMP-MAIL (aba 2)
    login = LoginPage(browser)
    login.open_login()
    # abre nova aba com temp-mail
    browser.switch_to.new_window('tab')
    tmp = TempMailPage(browser)
    tmp.open_site()
    email = tmp.current_email()
    assert "@" in email, "temp-mail não retornou um e-mail válido"

    # 3) voltar à aba da Americanas, preencher e enviar
    americanas_tab = browser.window_handles[0]
    tempmail_tab = browser.window_handles[1]

    browser.switch_to.window(americanas_tab)
    login.fill_email_and_send(email)

    # 4) voltar ao temp-mail, abrir o e-mail "Seu código de acesso"
    browser.switch_to.window(tempmail_tab)
    tmp.wait_first_mail_and_open(timeout=45)
    code = tmp.extract_code_6d()
    assert code.isdigit() and len(code) == 6

    # 5) retornar à Americanas e confirmar o código
    browser.switch_to.window(americanas_tab)
    login.type_code(code)

    # 6) redirecionado para a home e header com "minha conta"
    # (sua print mostra a home com “minha conta” visível)
    assert base.wait_text_anywhere("minha conta", timeout=20), "Não apareceu 'minha conta' no header."
