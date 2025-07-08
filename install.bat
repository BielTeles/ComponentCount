@echo off
echo Instalando Calculadora de Componentes em Bobinas...
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Por favor, instale Python 3.6 ou superior de https://python.org
    pause
    exit /b 1
)

echo Python encontrado!
echo.

REM Instalar dependências
echo Instalando dependencias...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERRO: Falha ao instalar dependencias!
    pause
    exit /b 1
)

echo.
echo Instalacao concluida com sucesso!
echo Para executar a aplicacao, use: python main.py
echo.
pause 