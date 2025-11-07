from selenium.webdriver.common.by import By
from .base_page import BasePage

class HeaderUser(BasePage):
    USER_BADGES = [
        (By.CSS_SELECTOR, "[data-testid='user-email']"),
        (By.XPATH, "//header//*[contains(text(),'@')]"),
    ]
    ACCOUNT_MENU = [
        (By.CSS_SELECTOR, "[data-testid='account-menu']"),
        (By.XPATH, "//a[contains(.,'minha conta') or contains(.,'Minha conta')]"),
    ]

    def email_visible_in_header(self) -> bool:
        return self.click_any(self.USER_BADGES) or any(
            self.driver.find_elements(*loc) for loc in self.USER_BADGES
        )

    def open_my_account(self) -> bool:
        return self.click_any(self.ACCOUNT_MENU)

class PasswordSetupPage(BasePage):
    SET_PASSWORD_LINKS = [
        (By.XPATH, "//a[contains(translate(.,'DEFINIR','definir'),'definir') and contains(.,'senha')]"),
        (By.XPATH, "//button[contains(translate(.,'DEFINIR','definir'),'definir') and contains(.,'senha')]"),
    ]
    CODE_INPUT = (By.CSS_SELECTOR, "input[name*='code' i], input[type='tel']")

    PW_INPUT = (By.CSS_SELECTOR, "input[type='password']")
    SAVE_BUTTON = (By.CSS_SELECTOR, "button[type='submit'], button[data-testid*='save' i]")

    def go_to_set_password(self) -> bool:
        return self.click_any(self.SET_PASSWORD_LINKS)

    def insert_code(self, code: str) -> bool:
        try:
            el = self.visible(self.CODE_INPUT)
            el.clear(); el.send_keys(code)
            return True
        except Exception:
            return False

    def set_password_and_validate_rules(self, pwd: str, expect_enabled: bool) -> bool:
        # digita senha e checa se o botão fica habilitado/desabilitado
        try:
            pw = self.visible(self.PW_INPUT)
            pw.clear(); pw.send_keys(pwd)
            btn = self.visible(self.SAVE_BUTTON)
            disabled = (btn.get_attribute("disabled") is not None) or ("disabled" in (btn.get_attribute("class") or "").lower())
            return (not disabled) if expect_enabled else disabled
        except Exception:
            return False

    def save_password(self) -> bool:
        return self.try_click(self.SAVE_BUTTON)
