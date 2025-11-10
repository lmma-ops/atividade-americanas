from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class HomePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.URL = "https://www.americanas.com.br/"

        
        self.LOGIN_SIGNUP = "/html/body/div[1]/header/div/section[1]/div/a[2]/div[2]"
        self.URL_EMAIL = "https://temp-mail.io/en"

        
        self.HEADER_EMAIL = "/html/body/div[1]/header/div/section[1]/div/a[2]/div[2]/span[1]"
        
        self.HEADER_MINHA_CONTA = "/html/body/div[1]/header/div/section[1]/div/a[2]/div[2]"
        
        self.MENU_AUTENTICACAO = "//a[contains(.,'autenticação') or contains(.,'autenticacao')]"
        self.MENU_CADASTRO = "//a[contains(.,'cadastro')]"

    def open_home(self):
        return self.driver.get(self.URL)

    def go_to_login(self):
        self.click_element(By.XPATH, self.LOGIN_SIGNUP)
        from pages.login_page import LoginPage
        return LoginPage(self.driver)

    def open_email(self, driver):
        from pages.temp_mail_page import TempMailPage
        return TempMailPage(self.driver)

    def ve_se_ta_na_homepage(self):
        return self.driver.current_url

    
    def texto_email_no_header(self) -> str:
        return self.get_element_text(By.XPATH, self.HEADER_EMAIL)

    def abrir_menu_minha_conta(self):
        self.click_forcado(By.XPATH, self.HEADER_MINHA_CONTA)

    def ir_para_autenticacao(self):
        self.abrir_menu_minha_conta()
        self.click_forcado(By.XPATH, self.MENU_AUTENTICACAO)
        from pages.authentication_page import AuthenticationPage
        return AuthenticationPage(self.driver)

    def ir_para_cadastro(self):
        self.abrir_menu_minha_conta()
        self.click_forcado(By.XPATH, self.MENU_CADASTRO)
        from pages.profile_page import ProfilePage
        return ProfilePage(self.driver)
