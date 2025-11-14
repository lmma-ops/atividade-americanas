from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver, ):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def send_keys_to_element(self, by, locator, text):
        self.find_element(by, locator).send_keys(text)

    def find_element(self, by, locator):
        return self.wait.until(EC.presence_of_element_located((by, locator)))
    
    def click_forcado(self, by, locator):
        el = self.find_element(by, locator)
        self.driver.execute_script("arguments[0].click();", el)
        return el
    
    def click_element(self, by, locator):
        self.find_element(by, locator).click()

    def get_element_text(self, by, locator):
        return self.find_element(by, locator).text
    
    def is_element_displayed(self, by, locator):
        try:
            return self.find_element(by, locator).is_displayed()
        except:
            return False
        
    def is_element_enabled(self, by, locator):
        try:
            return self.find_element(by, locator).is_enabled()
        except:
            return False