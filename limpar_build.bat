@echo off
echo ========================================
echo    LIMPEZA DOS ARQUIVOS DE BUILD
echo ========================================
echo.

echo Removendo arquivos de build desnecessarios...
echo.

REM Remover pasta build (contém arquivos temporários)
if exist "build" (
    echo Removendo pasta build...
    rmdir /s /q "build"
    echo ✓ Pasta build removida
) else (
    echo Pasta build nao encontrada
)

REM Remover arquivos .spec (exceto o principal)
for %%f in (*.spec) do (
    if not "%%f"=="ComponentCount.spec" (
        echo Removendo %%f...
        del "%%f"
        echo ✓ %%f removido
    )
)

REM Remover arquivos .pyc
if exist "*.pyc" (
    echo Removendo arquivos .pyc...
    del "*.pyc"
    echo ✓ Arquivos .pyc removidos
)

REM Remover arquivos __pycache__
for /d %%d in (__pycache__) do (
    if exist "%%d" (
        echo Removendo %%d...
        rmdir /s /q "%%d"
        echo ✓ %%d removido
    )
)

echo.
echo ========================================
echo    LIMPEZA CONCLUIDA!
echo ========================================
echo.
echo Arquivos mantidos:
echo - dist\ComponentCount.exe (executavel final)
echo - ComponentCount.spec (especificacao)
echo - Todos os arquivos fonte (.py, .md, .bat)
echo.
echo O executavel esta pronto para distribuicao!
echo.
pause 