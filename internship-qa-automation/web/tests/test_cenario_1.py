from pages.home_page import HomePage


def test_cenario_01(driver):
    home = HomePage(driver)
    home.open_home()
    home.go_to_login()

    home.open_email()
    

def test_cenario_0(driver, state):
    driver.switch_to.new_window('tab')
    state.tempmail_tab = driver.window_handles[1]
    tmp = TempMailPage(driver)
    tmp.open_site()
    state.email = tmp.current_email()
    assert "@" in state.email

# def test_step03_fill_email_and_send(driver, state):
#     driver.switch_to.window(state.americanas_tab)
#     login = LoginPage(driver)
#     login.open_login()
#     login.fill_email_and_send(state.email)

# def test_step04_open_mail_and_get_code(driver, state):
#     driver.switch_to.window(state.tempmail_tab)
#     tmp = TempMailPage(driver)
#     tmp.wait_first_mail_and_open(timeout=45)
#     state.code = tmp.extract_code_6d()
#     assert state.code.isdigit() and len(state.code) == 6

# def test_step05_submit_code(driver, state):
#     driver.switch_to.window(state.americanas_tab)
#     login = LoginPage(driver)
#     login.type_code(state.code)

# def test_step06_validate_logged_header(driver):
#     base = BasePage(driver)
#     assert base.wait_text_anywhere("minha conta", timeout=20), "Não apareceu 'minha conta' no header"
