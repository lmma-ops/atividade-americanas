# web/conftest.py
import pytest
import os  # <-- Importe o módulo 'os'
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService

@pytest.fixture
def driver():
    """
    Inicia o Google Chrome para os testes da pasta 'web'.
    """
    print("\n[conftest.py] Iniciando o Google Chrome...")

    # --- ESTA É A MUDANÇA ---
    # 1. Obter o caminho completo para a pasta raiz 'ATIVIDADE'
    #    (O '..' sobe um nível da pasta 'web' para a 'ATIVIDADE')
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

    # 2. Apontar para o 'chromedriver' que você baixou
    #    (No Mac, o ficheiro não tem '.exe')
    driver_path = os.path.join(project_root, 'chromedriver')

    # 3. Verificar se o ficheiro existe antes de o usar
    if not os.path.exists(driver_path):
        raise FileNotFoundError(f"Chromedriver não encontrado em {driver_path}. "
                                 f"Verifique se o 'chromedriver' (versão 141) está na sua pasta 'ATIVIDADE'.")

    print(f"[conftest.py] A usar o driver em: {driver_path}")

    # 4. Passar o caminho EXATO para o ChromeService
    service = ChromeService(executable_path=driver_path) 
    # --- FIM DA MUDANÇA ---

    navegador = webdriver.Chrome(service=service)
    navegador.maximize_window()

    yield navegador

    print("\n[conftest.py] Fechando o navegador Google Chrome.")
    navegador.quit()