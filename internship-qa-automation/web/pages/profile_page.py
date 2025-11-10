from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ProfilePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.email_cadastro = "//div[contains(@class,'cadastro') or contains(@class,'profile')]//div[contains(text(),'email')]/following-sibling::div[1]"

    def texto_email_cadastro(self) -> str:
        return self.get_element_text(By.XPATH, self.email_cadastro)
