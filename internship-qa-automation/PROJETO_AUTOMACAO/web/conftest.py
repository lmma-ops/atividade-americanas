import pytest
from selenium import webdriver

@pytest.fixture
def driver():
    # Setup: initialize the WebDriver
    driver_instance = webdriver.Chrome()
    driver_instance.maximize_window()
    yield driver_instance
    # Teardown: close the WebDriver
    driver_instance.quit()