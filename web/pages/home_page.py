from selenium.webdriver.common.by import By
from web.pages.base_page import BasePage

class HomePage(BasePage):
    LOGIN_BUTTON = (By.XPATH, '//*[@id="__next"]/header/div/section[1]/div/a[2]/div[2]/span[1]')
    LOGIN_LINK = (By.XPATH, "//a[contains(@href, 'login')]")
    USER_HEADER = (By.ID, "src-header-user")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get("https://www.americanas.com.br")

    def go_to_login_page(self):
        print("Acessando a página de login...")
        self.click(self.LOGIN_BUTTON)
        self.click(self.LOGIN_LINK)

    def get_header_text(self):
        print("Obtendo texto do cabeçalho para validação...")
        return self.get_element_text(self.USER_HEADER)