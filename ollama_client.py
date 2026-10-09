"""
BioConcurso MA - Módulo de Integração com Ollama (ollama_client.py)
Comunicação HTTP local com Ollama para geração de questões de Biologia (FCC),
explicações de alternativas, mapas de revisão e resumos.
"""

import json
import re
import urllib.request
import urllib.error
from typing import Dict, Any, Optional, Tuple, List

DEFAULT_OLLAMA_URL = "http://localhost:11434"
DEFAULT_MODEL = "qwen2.5:3b"

class OllamaClient:
    def __init__(self, base_url: str = DEFAULT_OLLAMA_URL, model: str = DEFAULT_MODEL):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def testar_conexao(self) -> Tuple[bool, str, List[str]]:
        try:
            req = urllib.request.Request(f"{self.base_url}/api/tags")
            with urllib.request.urlopen(req, timeout=2) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                modelos = [m.get("name", "") for m in data.get("models", [])]
                return True, f"Ollama conectado! ({len(modelos)} modelo(s))", modelos
        except Exception as e:
            return False, f"Ollama offline: {str(e)}", []
