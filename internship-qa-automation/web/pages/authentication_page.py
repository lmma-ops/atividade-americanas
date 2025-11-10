from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class AuthenticationPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.link_definir_senha = "//a[contains(.,'definir senha')]"
        self.campo_codigo = "//label[contains(.,'código') or contains(.,'codigo')]/following::input[1]"
        self.campo_nova_senha = "//label[contains(.,'nova senha')]/following::input[1]"
        self.botao_salvar = "//button[contains(.,'salvar senha')]"
        self.mascara_senha = "//div[contains(@class,'password') or contains(.,'senha')]//span[contains(text(),'•') or contains(text(),'●') or contains(text(),'*')]"

    def abrir_definir_senha(self):
        self.click_forcado(By.XPATH, self.link_definir_senha)

    def preencher_codigo(self, codigo):
        self.send_keys_to_element(By.XPATH, self.campo_codigo, codigo)

    def digitar_nova_senha(self, senha):
        self.send_keys_to_element(By.XPATH, self.campo_nova_senha, senha)

    def limpar_nova_senha(self):
        el = self.find_element(By.XPATH, self.campo_nova_senha)
        el.clear()

    def botao_salvar_esta_desabilitado(self) -> bool:
        return not self.is_element_enabled(By.XPATH, self.botao_salvar)

    def clicar_salvar(self):
        self.click_forcado(By.XPATH, self.botao_salvar)

    def pegar_texto_mascarado(self) -> str:
        try:
            return self.get_element_text(By.XPATH, self.mascara_senha)
        except:
            return ""
