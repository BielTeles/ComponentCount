@echo off
echo ========================================
echo    ComponentCount - Versao Melhorada
echo ========================================
echo.
echo Iniciando aplicativo com nova interface...
echo.
echo Melhorias implementadas:
echo - Design moderno e profissional
echo - Interface mais intuitiva
echo - Cores harmoniosas
echo - Tooltips informativos
echo - Layout responsivo
echo.
echo Aguarde...
echo.

if exist "dist\ComponentCount.exe" (
    start "" "dist\ComponentCount.exe"
    echo Aplicativo iniciado com sucesso!
) else (
    echo ERRO: Executavel nao encontrado!
    echo Execute 'python -m PyInstaller --onefile --windowed --name ComponentCount main.py' primeiro.
    pause
)

echo.
echo Pressione qualquer tecla para sair...
pause >nul 