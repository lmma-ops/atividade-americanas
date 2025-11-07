from selenium.webdriver.common.by import By
from .base_page import BasePage

class HomePage(BasePage):
    URL = "https://www.americanas.com.br/"

    # Tentativas de clique (se existir); depois caímos no fallback por URL
    LOGIN_LINKS = [
        (By.XPATH, "//a[contains(translate(.,'ENTRAR','entrar'),'entrar') or contains(translate(.,'LOGIN','login'),'login') or contains(translate(.,'CADASTRE','cadastre'),'cadastre')]"),
        (By.CSS_SELECTOR, "a[href*='/login']"),
        (By.CSS_SELECTOR, "[data-testid='login-link'], [data-testid='h_user']"),
    ]

    def open_home(self):
        self.open(self.URL)

    def go_to_login(self) -> bool:
        if self.click_any(self.LOGIN_LINKS):
            return True
        # fallback robusto – exatamente a URL que aparece na sua imagem
        self.open("https://www.americanas.com.br/api/jfo/login")
        return True
