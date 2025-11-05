"""
Helpers para interagir com temp-mail via Selenium.
Nota: usar a API pública (se disponível) é mais robusto, mas muitos serviços mudam.
Este arquivo contém funções que usam Selenium para abrir a aba do temp-mail e extrair o email mais recente.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def open_temp_mail_and_get_address(driver, timeout=20):
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get("https://temp-mail.io/")
    wait = WebDriverWait(driver, timeout)

    # ### UPDATE SELECTORS HERE
    # Ajuste o seletor abaixo para o elemento que contém o e-mail gerado
    # Exemplo: ".address" ou "#mail" dependendo do DOM
    mail_address_selector = (By.CSS_SELECTOR, ".address")  

    addr_elem = wait.until(EC.visibility_of_element_located(mail_address_selector))
    address = addr_elem.text.strip()
    return address

def get_latest_email_body(driver, timeout=60, poll_interval=2):
    """
    Supõe que já esteja na aba do temp-mail.
    Retorna o corpo do email mais recente (string).
    """
    wait = WebDriverWait(driver, timeout)
    end_time = time.time() + timeout

    # ### UPDATE SELECTORS HERE
    # Ajuste os seletores abaixo conforme o DOM do temp-mail
    inbox_item_selector = (By.CSS_SELECTOR, ".inbox .mail-item")  # exemplo
    mail_body_selector = (By.CSS_SELECTOR, ".mail-content")       # exemplo

    while time.time() < end_time:
        try:
            items = driver.find_elements(*inbox_item_selector)
            if items:
                items[0].click()
                body = wait.until(EC.visibility_of_element_located(mail_body_selector))
                return body.text
        except Exception:
            pass
        time.sleep(poll_interval)
        driver.refresh()
    return None
