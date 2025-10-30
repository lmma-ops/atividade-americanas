# web/pages/login_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from web.pages.base_page import BasePage

class LoginPage(BasePage):
    # --- Locators (Seletores) ---
    # !! USE O SELECTORSHUB PARA CONFIRMAR ESTES VALORES !!
    EMAIL_FIELD = (By.NAME, "email")
    PASSWORD_FIELD = (By.NAME, "password")
    BODY = (By.TAG_NAME, "body")

    # --- Métodos de Ação ---
    def __init__(self, driver):
        super().__init__(driver)

    def do_login(self, email, password):
        print(f"Preenchendo login com: {email}")
        self.send_keys(self.EMAIL_FIELD, email)
        self.send_keys(self.PASSWORD_FIELD, password)
        self.send_keys(self.PASSWORD_FIELD, Keys.ENTER)

    def get_page_text_for_error(self):
        print("Obtendo texto da página para validar erro...")
        return self.get_element_text(self.BODY)