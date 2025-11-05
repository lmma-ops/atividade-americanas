import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="session")
def base_url():
	# Base URL for the Americanas site; can be overridden with BASE_URL env var
	return os.getenv("BASE_URL", "https://www.americanas.com.br")


@pytest.fixture(scope="session")
def chrome_options():
	opts = Options()
	# Allow running headless via env var
	if os.getenv("HEADLESS", "false").lower() in ("1", "true", "yes"):
		opts.add_argument("--headless=new")
	opts.add_argument("--no-sandbox")
	opts.add_argument("--disable-dev-shm-usage")
	opts.add_argument("--window-size=1920,1080")
	return opts


@pytest.fixture(scope="function")
def driver(chrome_options):
	"""Create a Chrome WebDriver instance for each test function and quit after test.

	Uses webdriver-manager to auto-download ChromeDriver that matches installed Chrome.
	"""
	service = ChromeService(ChromeDriverManager().install())
	driver = webdriver.Chrome(service=service, options=chrome_options)
	# Prefer explicit waits in tests/pages; keep implicit wait minimal
	driver.implicitly_wait(0)
	yield driver
	driver.quit()


@pytest.fixture
def switch_to_tab(driver):
	"""Helper fixture that returns a function to switch to a given tab index."""
	def _switch(index):
		handles = driver.window_handles
		if index < 0 or index >= len(handles):
			raise IndexError("Tab index out of range")
		driver.switch_to.window(handles[index])

	return _switch

