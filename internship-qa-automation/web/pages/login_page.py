from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.email_and_password_btn = "/html/body/div[2]/div/div[1]/div/div[2]/div/div/div/section/div/div[2]/div/div[1]/div[1]/ul/li[1]/div/button"
        self.campo_email = "/html/body/div[2]/div/div[1]/div/div[2]/div/div/div/section/div/div[2]/div/div[2]/div/div/form/div[1]/label/div/input"
        self.campo_senha = "/html/body/div[2]/div/div[1]/div/div[2]/div/div/div/section/div/div[2]/div/div[2]/div/div/form/div[2]/div/label/div/input"
        self.text_senha_invalida = "/html/body/div[2]/div/div[1]/div/div[2]/div/div/div/section/div/div[2]/div/div[2]/div/div/form/div[3]"
        self.botao_entrar = "bg-action-primary"
    
    def clicar_email_password(self):
        self.click_forcado(By.XPATH, self.email_and_password_btn)
    
    def colocar_email(self, email):
        self.send_keys_to_element(By.XPATH, self.campo_email, email)

    def colocar_senha(self, senha):
        self.send_keys_to_element(By.XPATH, self.campo_senha, senha)

    def pegar_texto_senha_invalida(self):
        return self.get_element_text(By.XPATH, self.text_senha_invalida)
    
    def clicar_botao_entrar(self):
        self.click_forcado(By.CLASS_NAME, self.botao_entrar)
        from pages.home_page import HomePage
        return HomePage(self.driver)
    