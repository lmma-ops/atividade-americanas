# debug_locators_modal.py
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, InvalidSelectorException
import traceback
import time
import os

# importa sua page object
from tests.web.pages.registration_page import RegistrationPage
from selenium.webdriver.common.by import By

def start_driver(gui=True):
    opts = Options()
    if not gui:
        opts.add_argument("--headless=new")
    # permitir ver o navegador; se der problema, rode sem headless (gui=True)
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=opts)
    driver.set_window_size(1366, 900)
    return driver

def safe_find(driver, locator, timeout=10):
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    try:
        return WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))
    except Exception:
        return None

def main():
    driver = start_driver(gui=True)  # set gui=False para headless
    try:
        reg = RegistrationPage(driver)
        driver.get("https://www.americanas.com.br/")
        time.sleep(2)  # deixa a página carregar

        print(">>> Clicando no botão de login usando LOGIN_OR_SIGNUP...")
        try:
            # tenta clicar com o método do Page Object
            reg.open_login()
            print("  -> clique realizado (open_login).")
        except Exception as e:
            print("  -> falhou ao clicar via PageObject.open_login():")
            traceback.print_exc(limit=1)
            # tenta localizar manualmente e clicar
            try:
                by, sel = reg.LOGIN_OR_SIGNUP
                el = driver.find_element(by, sel)
                el.click()
                print("  -> clique manual realizado.")
            except Exception:
                print("  -> clique manual também falhou.")
                traceback.print_exc(limit=1)
                # salvar screenshot e sair
                driver.save_screenshot("debug_screenshot.png")
                print("Screenshot salva em debug_screenshot.png")
                return

        # aguarda um pouco para modal aparecer
        time.sleep(2)

        # lista de locators a testar (do seu RegistrationPage)
        locators = {
            "EMAIL_INPUT": getattr(reg, "EMAIL_INPUT", None),
            "SEND_CODE_BTN": getattr(reg, "SEND_CODE_BTN", None),
            "CODE_INPUT": getattr(reg, "CODE_INPUT", None),
            "CONFIRM_BTN": getattr(reg, "CONFIRM_BTN", None),
            "NEW_PASSWORD_INPUT": getattr(reg, "NEW_PASSWORD_INPUT", None),
            "SAVE_PASSWORD_BTN": getattr(reg, "SAVE_PASSWORD_BTN", None),
            "PASSWORD_ASTERISKS": getattr(reg, "PASSWORD_ASTERISKS", None),
        }

        for name, locator in locators.items():
            print(f"\nProcurando {name} -> {locator!r}")
            if locator is None:
                print(f"  -> Locator {name} não definido no RegistrationPage")
                continue
            try:
                elem = safe_find(driver, locator, timeout=8)
                if elem:
                    print(f"  ✅ {name} encontrado: tag={elem.tag_name}, text='{(elem.text or '')[:60]}'")
                else:
                    print(f"  ❌ {name} NÃO encontrado (timeout).")
                    # tirar screenshot para inspeção
                    fname = f"debug_{name}.png"
                    driver.save_screenshot(fname)
                    print(f"  Screenshot salva em {fname}")
            except InvalidSelectorException:
                print(f"  ❌ {name} -> InvalidSelectorException (seletor mal formado).")
                traceback.print_exc(limit=1)
            except Exception:
                print(f"  ❌ {name} -> outra exceção:")
                traceback.print_exc(limit=1)
                fname = f"debug_{name}_error.png"
                driver.save_screenshot(fname)
                print(f"  Screenshot salva em {fname}")

        print("\nTeste finalizado. Verifique screenshots geradas (se houver) e o estado da modal.")

    finally:
        # não fechar imediatamente para você inspecionar se gui=True; comentar se quiser que feche
        print("Aguardando 5s antes de encerrar o driver...")
        time.sleep(5)
        driver.quit()

if __name__ == "__main__":
    main()
