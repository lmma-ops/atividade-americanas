from typing import Optional
import re

def extract_code_from_text(text: str) -> Optional[str]:
    """
    Tenta extrair um código numérico de 4 a 6 dígitos de um corpo de e-mail/texto.
    Ajuste a regex se os códigos forem diferentes.
    """
    m = re.search(r'(\d{4,6})', text)
    return m.group(1) if m else None
