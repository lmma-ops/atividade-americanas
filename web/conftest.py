import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="session")
def driver():
    """Fixture para inicializar e fechar o navegador Chrome."""
    
    # Instala e gerencia o ChromeDriver automaticamente
    service = ChromeService(ChromeDriverManager().install())
    
    # Inicializa o navegador
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(10) # Espera implícita de 10 segundos
    driver.maximize_window() # Maximiza a janela
    
    # Retorna o driver para os testes
    yield driver
    
    # Fecha o navegador após todos os testes da sessão
    driver.quit()