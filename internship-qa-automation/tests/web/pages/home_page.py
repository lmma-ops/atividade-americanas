from .base_page import BasePage

class HomePage(BasePage):
    URL = "https://www.americanas.com.br/"

    def open_home(self):
        self.open(self.URL)
