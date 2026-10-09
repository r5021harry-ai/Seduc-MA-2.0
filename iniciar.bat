@echo off
chcp 65001 > nul
title BioConcurso MA - Preparatorio SEDUC-MA Biologia FCC

echo ======================================================================
echo           BIOCONCURSO MA - PREPARATORIO SEDUC-MA (BIOLOGIA - FCC)
echo ======================================================================
echo.
echo [1/4] Verificando instalacao do Python no sistema...

where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERRO CRITICO] O Python nao foi encontrado no seu sistema!
    echo Instale o Python 3.10+ marcando "Add Python to PATH": https://www.python.org/
    pause
    exit /b 1
)

python --version
echo [OK] Python detectado com sucesso.
echo.

cd /d "%~dp0"

echo [2/4] Verificando ambiente virtual (venv)...
if not exist "venv" (
    echo Criando novo ambiente virtual 'venv'...
    python -m venv venv
)

if exist "venv\Scripts\activate.bat" (
    call "venv\Scripts\activate.bat"
)

echo [3/4] Instalando dependencias (requirements.txt)...
pip install -r requirements.txt --quiet
echo [OK] Dependencias verificadas.
echo.

echo [4/4] Inicializando o aplicativo Streamlit no navegador...
streamlit run app.py --server.headless=false
pause
