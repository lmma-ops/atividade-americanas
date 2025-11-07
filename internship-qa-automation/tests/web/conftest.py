import os, time, pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

ART_DIR = os.path.join(os.getcwd(), "artifacts")
os.makedirs(ART_DIR, exist_ok=True)

def _make_driver():
    opts = Options()
    # Deixe visível (comente o headless). Descomente se quiser headless.
    # opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1366,900")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=opts)

@pytest.fixture(scope="function")
def browser(request):
    driver = _make_driver()
    # anexa o driver ao item de teste para o hook acessar
    request.node._driver = driver
    yield driver

    # só fecha se: não falhou E não pedimos para manter
    rep_call = getattr(request.node, "rep_call", None)
    failed = bool(rep_call and rep_call.failed)
    keep = os.getenv("KEEP_BROWSER", "0") == "1"

    if failed or keep:
        print("\n⚠️  Mantendo navegador aberto para inspeção."
              "\n    Pressione ENTER para fechar...")
        try:
            input()
        except EOFError:
            pass

    try:
        driver.quit()
    except Exception:
        pass

# ---------- HOOKS CORRETOS ----------

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """
    Hook com hookwrapper=True (correto): captura o report,
    salva screenshot se falhar e disponibiliza o rep_call no item.
    """
    outcome = yield
    rep = outcome.get_result()

    # expõe o report da fase 'call' para o teardown da fixture
    if rep.when == "call":
        setattr(item, "rep_call", rep)

        # screenshot automático em caso de falha
        drv = getattr(item, "_driver", None)
        if drv and rep.failed:
            ts = time.strftime("%Y%m%d-%H%M%S")
            path = os.path.join(ART_DIR, f"{item.name}-{ts}.png")
            try:
                drv.save_screenshot(path)
                print(f"\n[artifact] screenshot salvo em: {path}")
            except Exception as e:
                print(f"\n[artifact] falha ao salvar screenshot: {e}")
