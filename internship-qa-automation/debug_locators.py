# debug_locators.py
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import traceback

try:
    from tests.web.pages import registration_page
except Exception:
    import tests.web.pages.registration_page as registration_page

def start_driver():
    opts = Options()
    opts.add_argument("--headless=new")  # pode remover para ver o navegador abrindo
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=opts)
    driver.set_window_size(1366, 900)
    return driver

def test_locators():
    print("Testando locators da RegistrationPage...\n")
    rp = registration_page.RegistrationPage
    keys = [
        "LOGIN_OR_SIGNUP", "EMAIL_INPUT", "SEND_CODE_BTN", "CODE_INPUT",
        "CONFIRM_BTN", "HEADER_USER_EMAIL", "MY_ACCOUNT",
        "AUTH_SECTION", "SET_PASSWORD_BTN", "NEW_PASSWORD_INPUT",
        "SAVE_PASSWORD_BTN", "PASSWORD_ASTERISKS"
    ]
    for k in keys:
        val = getattr(rp, k, None)
        print(f"\n{k} = {val!r}")
        if val is None:
            continue
        if not (isinstance(val, tuple) and len(val) == 2):
            print(f"❌  INVALID: locator deve ser uma tupla (By.TIPO, 'seletor')")
            continue
        by, selector = val
        try:
            d = start_driver()
            d.get("https://www.americanas.com.br/")
            d.find_element(by, selector)
            print("✅  Locator válido e encontrado na página.")
        except Exception as e:
            print("⚠️  Erro ao usar locator:")
            traceback.print_exc(limit=1)
        finally:
            d.quit()

if __name__ == "__main__":
    test_locators()
