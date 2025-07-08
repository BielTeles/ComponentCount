@echo off
echo ========================================
echo    BUILD DO EXECUTAVEL COMPONENTCOUNT
echo ========================================
echo.

REM Verificar se PyInstaller está instalado
echo Verificando PyInstaller...
& "C:\Users\devte\AppData\Local\Programs\Python\Python*\python.exe" -c "import PyInstaller" 2>nul
if %errorlevel% neq 0 (
    echo Instalando PyInstaller...
    & "C:\Users\devte\AppData\Local\Programs\Python\Python*\python.exe" -m pip install pyinstaller
)

echo.
echo Iniciando build do executavel...
echo.

REM Limpar builds anteriores
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "*.spec" del "*.spec"

REM Fazer a build usando o arquivo de especificação
& "C:\Users\devte\AppData\Local\Programs\Python\Python*\python.exe" -m PyInstaller ComponentCount.spec

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo    BUILD CONCLUIDO COM SUCESSO!
    echo ========================================
    echo.
    echo O executavel foi criado em: dist\ComponentCount.exe
    echo.
    echo Para testar, execute: dist\ComponentCount.exe
    echo.
) else (
    echo.
    echo ERRO: Falha na build!
    echo.
)

pause 