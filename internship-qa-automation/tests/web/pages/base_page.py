import re, time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver, timeout=20):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url: str):
        self.driver.get(url)
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def scroll_into_view(self, el):
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)

    def click_hard(self, locator):
        el = self.clickable(locator)
        self.scroll_into_view(el)
        el.click()

    def try_click(self, locator) -> bool:
        try:
            el = self.visible(locator)
            self.scroll_into_view(el)
            ActionChains(self.driver).move_to_element(el).pause(0.15).click().perform()
            return True
        except Exception:
            try:
                el = self.find(locator)
                self.scroll_into_view(el)
                self.driver.execute_script("arguments[0].click();", el)
                return True
            except Exception:
                return False

    def click_any(self, locators) -> bool:
        for loc in locators:
            if self.try_click(loc):
                return True
        return False

    def send_keys_js(self, el, text):
        self.driver.execute_script("arguments[0].value = arguments[1];", el, text)

    def get_text(self, locator) -> str:
        return self.visible(locator).text.strip()

    def wait_text_anywhere(self, *keywords, timeout=12) -> bool:
        stop = time.time() + timeout
        while time.time() < stop:
            html = (self.driver.page_source or "").lower()
            if any(k.lower() in html for k in keywords):
                return True
            time.sleep(0.35)
        return False

    @staticmethod
    def find_code_6d(text: str) -> str:
        m = re.search(r"\b(\d{6})\b", text or "")
        return m.group(1) if m else ""

    @property
    def title(self) -> str:
        return (self.driver.title or "").strip()

    @property
    def current_url(self) -> str:
        return (self.driver.current_url or "").strip()
