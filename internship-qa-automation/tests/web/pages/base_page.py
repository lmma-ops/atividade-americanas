from selenium.webdriver.support.ui import WebDriverWait

class BasePage:
    def __init__(self, driver, timeout=20):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url: str):
        self.driver.get(url)
        # aguarda DOM completo (reduz flakiness)
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

    @property
    def title(self) -> str:
        return self.driver.title or ""

    @property
    def current_url(self) -> str:
        return self.driver.current_url or ""
