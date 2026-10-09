"""
BioConcurso MA - Aplicação Principal Streamlit (app.py)
Preparatório Inteligente para o Concurso SEDUC-MA - Professor de Biologia (Banca FCC).
Integração com SQLite, Inteligência Artificial Local (Ollama) e Exportação em PDF.
"""

import streamlit as st
import pandas as pd
import os
import json
import io
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

import db
from ollama_client import OllamaClient

# Configuração da Página
st.set_page_config(
    page_title="BioConcurso MA — SEDUC-MA Biologia (FCC)",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar Banco de Dados SQLite
db.init_db()

# Inicialização de Session State
if "questao_atual_id" not in st.session_state:
    st.session_state.questao_atual_id = None
if "resposta_confirmada" not in st.session_state:
    st.session_state.resposta_confirmada = False
if "resultado_ultimo" not in st.session_state:
    st.session_state.resultado_ultimo = None
if "simulado_ativo" not in st.session_state:
    st.session_state.simulado_ativo = None
if "simulado_respostas" not in st.session_state:
    st.session_state.simulado_respostas = {}
if "ia_questao_gerada" not in st.session_state:
    st.session_state.ia_questao_gerada = None

def get_ollama_client() -> OllamaClient:
    url = db.obter_config("ollama_url", "http://localhost:11434")
    modelo = db.obter_config("ollama_modelo", "qwen2.5:3b")
    return OllamaClient(base_url=url, model=modelo)

# Sidebar
with st.sidebar:
    st.markdown("### 🧬 BioConcurso MA")
    st.caption("SEDUC-MA • Professor de Biologia • Banca FCC")
    st.divider()

    modulo = st.radio(
        "Navegação do Sistema:",
        [
            "🏠 Painel Inicial",
            "📚 Banco de Questões",
            "✍️ Resolução de Questões",
            "🤖 IA Local (Ollama)",
            "📕 Caderno de Erros",
            "⏱️ Simulados Personalizados",
            "🔄 Revisão Espaçada",
            "📅 Planejador de Estudos",
            "📤 Importação e Exportação",
            "⚙️ Configurações & Conexão"
        ]
    )
    st.divider()
    client = get_ollama_client()
    online, _, _ = client.testar_conexao()
    if online:
        st.success(f"🟢 Ollama Online ({client.model})")
    else:
        st.info("⚪ Ollama Offline (Estudo offline ativo)")

# Renderização do Módulo Selecionado...
# (Consulte o arquivo bioconcurso_ma/app.py completo no repositório)
