import os
from dotenv import load_dotenv


load_dotenv()


# Base URL da API (rodando local via uvicorn)
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")


# Timeout padrão para requests (segundos)
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "15"))


# Flag para rodar apenas API em CI (evitando intermitência de e2e)
RUN_E2E = os.getenv("RUN_E2E", "false").lower() in ("1", "true", "yes")