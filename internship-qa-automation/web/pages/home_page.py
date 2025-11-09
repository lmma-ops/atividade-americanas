from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class HomePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.URL = "https://www.americanas.com.br/"
        self.LOGIN_SIGNUP = "/html/body/div[1]/header/div/section[1]/div/a[2]/div[2]"
        self.URL_EMAIL = "https://temp-mail.io/en"

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
    
# def test_cenario_02(driver, state):
#     driver.switch_to.new_window('tab')
#     state.tempmail_tab = driver.window_handles[1]
#     tmp = TempMailPage(driver)
#     tmp.open_site()
#     state.email = tmp.current_email()
#     assert "@" in state.email