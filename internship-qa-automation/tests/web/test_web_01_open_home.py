import pytest
from .pages.home_page import HomePage   # <- POM com import relativo

pytestmark = pytest.mark.e2e

def test_web01_open_home(browser):
    home = HomePage(browser)
    home.open_home()
    assert len(home.title) > 0, "Título vazio (página não carregou?)"
    assert "americanas" in home.current_url.lower(), f"URL inesperada: {home.current_url}"
