import re
import time
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class TempMailPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.URL = "https://temp-mail.io/en"

        
        self.input_email = "/html/body/div[1]/main/div[2]/div/div/div/input"
        self.botao_refresh = "/html/body/div[1]/main/div[6]/aside/div/div[1]/div/div[1]/button"
        self.primeira_linha_assunto = "/html/body/div[1]/main/div[6]/aside/div/div[3]/div/ul/li[1]/div[2]/span[1]"
        self.primeira_linha_tr = "//section[contains(@class,'inbox')]//tbody/tr[1]"
        self.corpo_mensagem = "//*[contains(@class,'email-content') or contains(@id,'mail') or contains(@class,'message-body')]"

    def open_site(self):
        self.driver.get(self.URL)

    def current_email(self) -> str:
        el = self.find_element(By.XPATH, self.input_email)
        return el.get_attribute("value")

    def _refresh(self):
        try:
            self.click_forcado(By.XPATH, self.botao_refresh)
        except:
            self.driver.refresh()

    def wait_and_get_code(self, subject_contains: str, timeout=120) -> str:
        fim = time.time() + timeout
        while time.time() < fim:
            self._refresh()
            try:
                assunto = self.get_element_text(By.XPATH, self.primeira_linha_assunto)
                if subject_contains.lower() in assunto.lower():
                    self.click_forcado(By.XPATH, self.primeira_linha_tr)
                    corpo = self.get_element_text(By.XPATH, self.corpo_mensagem)
                    m = re.search(r"\b(\d{6})\b", corpo)
                    if m:
                        return m.group(1)
            except:
                pass
            time.sleep(2)
        raise AssertionError("Código do e-mail não chegou a tempo no temp-mail.")
