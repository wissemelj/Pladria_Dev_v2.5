@echo off
title Pladria v2.5 - Lanceur d'Application
color 0A

echo.
echo ================================================================
echo                    PLADRIA v2.5 - LANCEUR
echo ================================================================
echo.
echo Lancement de l'application Pladria...
echo.

REM Aller dans le dossier src
cd /d "%~dp0\src"

REM Verification Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python non detecte
    echo.
    echo Solutions:
    echo - Installez Python 3.8+ depuis python.org
    echo - Verifiez que Python est dans le PATH
    echo.
    pause
    exit /b 1
)

echo [INFO] Python detecte - OK
echo [INFO] Nettoyage des caches...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul

echo [INFO] Demarrage de Pladria v2.5...
echo.
python launch_app.py

REM Verification du resultat
if errorlevel 1 (
    echo.
    echo ================================================================
    echo                      ECHEC DU LANCEMENT
    echo ================================================================
    echo.
    echo [ERREUR] L'application n'a pas pu demarrer
    echo.
    echo Solutions recommandees:
    echo 1. Verifiez les dependances Python
    echo 2. Executez en tant qu'administrateur
    echo 3. Verifiez les parametres antivirus
    echo 4. Utilisez le build executable (Package\BUILD_FROM_EXPLORER.bat)
    echo.
) else (
    echo.
    echo ================================================================
    echo                    LANCEMENT REUSSI
    echo ================================================================
    echo.
    echo [SUCCES] Pladria v2.5 est maintenant actif
    echo.
    echo Modules disponibles:
    echo - Module 1: Generateur de Suivi
    echo - Module 2: Suivi Global
    echo - Module 3: Statistiques Equipe
    echo - Module 4: Visualiseur de Donnees
    echo - Module 5: Controle Qualite
    echo.
)

echo ================================================================
pause
