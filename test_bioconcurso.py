"""
BioConcurso MA - Suíte de Testes Automatizados (test_bioconcurso.py)
Testa os 10 requisitos obrigatórios da especificação técnica.
Execução: python test_bioconcurso.py
"""

import unittest
import db
from ollama_client import OllamaClient

# 10 Testes:
# 1. Inicialização do banco de dados
# 2. Cadastro e consulta de questões
# 3. Validação do gabarito (A-E)
# 4. Registro de respostas
# 5. Cálculo de aproveitamento
# 6. Caderno de erros
# 7. Revisões espaçadas
# 8. Importação sem descarte
# 9. Resiliência do Ollama offline
# 10. Persistência dos dados SQLite
