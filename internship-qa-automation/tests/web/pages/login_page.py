from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from .base_page import BasePage

class LoginPage(BasePage):
    URL = "https://www.americanas.com.br/api/jfo/login"

    EMAIL_INPUT = (By.CSS_SELECTOR, "input[type='email']")
    SEND_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")

    CODE_INPUTS = [
        (By.CSS_SELECTOR, "input[placeholder*='código' i]"),
        (By.CSS_SELECTOR, "input[name*='code' i]"),
        (By.CSS_SELECTOR, "input[type='tel']"),
    ]
    CONFIRM_BUTTON = (By.XPATH, "//button[contains(.,'confirmar')]")

    def open_login(self):
        self.open(self.URL)

    def fill_email_and_send(self, email: str) -> None:
        el = self.visible(self.EMAIL_INPUT)
        el.clear()
        el.send_keys(email)
        self.click_hard(self.SEND_BUTTON)
        # feedback simples – a página troca para a tela do código
        WebDriverWait(self.driver, 12).until(
            EC.visibility_of_element_located(self.CODE_INPUTS[0]) or
            EC.visibility_of_element_located(self.CODE_INPUTS[1]) or
            EC.visibility_of_element_located(self.CODE_INPUTS[2])
        )

    def type_code(self, code: str) -> None:
        # caixa única
        for loc in self.CODE_INPUTS:
            try:
                el = self.visible(loc)
                el.clear(); el.send_keys(code)
                break
            except Exception:
                continue
        self.click_hard(self.CONFIRM_BUTTON)
