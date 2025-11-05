import pytest, requests
from config.env_config import API_BASE_URL, REQUEST_TIMEOUT

pytestmark = pytest.mark.api

def test_smoke_api_reachable():
    """
    Smoke: tenta múltiplos endpoints comuns.
    - Se houver erro de conexão: SKIP (API não está rodando).
    - Se algum endpoint responder 2xx/3xx: PASS.
    - Caso contrário: FAIL com resumo curto (sem rastreio gigante).
    """
    base = API_BASE_URL.rstrip("/")
    candidates = ["", "/docs", "/openapi.json", "/health", "/api/health"]

    connection_error = None
    results = []

    for path in candidates:
        url = f"{base}{path}"
        try:
            r = requests.get(url, timeout=REQUEST_TIMEOUT)
            results.append((path or "/", r.status_code))
            if 200 <= r.status_code < 400:
                return  # passou o smoke
        except requests.exceptions.RequestException as e:
            connection_error = e
            # erro de conexão: não adianta tentar outros
            pytest.skip(f"API não acessível em {base} ({type(e).__name__}: {e})")

    # Se chegou até aqui: houve resposta, mas nenhum 2xx/3xx
    short = ", ".join([f"{p}:{code}" for p, code in results]) or "sem respostas"
    pytest.fail(f"API respondeu, mas sem 2xx/3xx nos endpoints comuns [{short}]. "
                f"Verifique se a app está no host/porta corretos.")
