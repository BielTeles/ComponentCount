@echo off
echo Iniciando Calculadora de Componentes em Bobinas...
echo.

REM Tentar diferentes comandos Python
python main.py 2>nul
if %errorlevel% equ 0 goto :end

py main.py 2>nul
if %errorlevel% equ 0 goto :end

python3 main.py 2>nul
if %errorlevel% equ 0 goto :end

REM Tentar com caminho completo
"C:\Users\devte\AppData\Local\Programs\Python\Python*\python.exe" main.py 2>nul
if %errorlevel% equ 0 goto :end

echo ERRO: Nao foi possivel executar o Python!
echo Verifique se o Python esta instalado corretamente.
pause
exit /b 1

:end
echo.
echo Aplicacao finalizada.
pause 