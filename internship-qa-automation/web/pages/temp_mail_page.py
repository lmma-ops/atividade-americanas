import time, re
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from base_page import BasePage

class TempMailPage(BasePage):
    URL = "https://temp-mail.io/en"

    EMAIL_INPUT = (By.CSS_SELECTOR, "main input[type='text']")
    REFRESH_BUTTON = (By.XPATH, "//button[contains(.,'refresh') or contains(.,'Refresh')]")
    MAIL_ROW_SELECTOR = (By.XPATH, "//*[contains(.,'Seu código de acesso')][self::div or self::li or self::a]")
    MAIL_BODY_CAND = [
        (By.CSS_SELECTOR, ".mail-view, .email-view, .content, .body, article, pre"),
        (By.XPATH, "//*[contains(@class,'mail') or contains(@class,'content') or name()='pre']"),
    ]

    def open_site(self):
        self.open(self.URL)

    def current_email(self) -> str:
        el = self.visible(self.EMAIL_INPUT)
        return (el.get_attribute("value") or "").strip()

    def wait_first_mail_and_open(self, timeout=45):
        end = time.time() + timeout
        while time.time() < end:
            try:
                row = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable(self.MAIL_ROW_SELECTOR)
                )
                row.click(); return
            except Exception:
                try: self.click_hard(self.REFRESH_BUTTON)
                except Exception: pass
                time.sleep(2)
        raise AssertionError("Nenhum e-mail com assunto 'Seu código de acesso' chegou a tempo.")

    def extract_code_6d(self) -> str:
        text = ""
        for loc in self.MAIL_BODY_CAND:
            try:
                el = self.visible(loc); text = el.text or ""
                if text: break
            except Exception: continue
        m = re.search(r"\b(\d{6})\b", text)
        if not m: raise AssertionError("Não achei código de 6 dígitos no corpo do e-mail.")
        return m.group(1)
