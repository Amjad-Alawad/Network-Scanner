@echo off
title AMJD ALAWAD - GitHub Upload
color 0A

cd /d "%~dp0"

echo =====================================
echo       AMJD ALAWAD - UPLOADER
echo =====================================
echo.

set "REPO=https://github.com/Amjad-Alawad/Network-Scanner.git"

where git >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed.
    pause
    exit /b 1
)

if not exist ".git" (
    git init
    if errorlevel 1 goto error
)

(
echo .venv/
echo venv/
echo __pycache__/
echo *.pyc
echo *.db
echo *.sqlite
echo *.sqlite3
echo *.log
echo build/
echo dist/
echo *.spec
echo data/
echo reports/
) > .gitignore

git branch -M main
if errorlevel 1 goto error

git remote get-url origin >nul 2>&1
if errorlevel 1 (
    git remote add origin "%REPO%"
) else (
    git remote set-url origin "%REPO%"
)
if errorlevel 1 goto error

git add -A
if errorlevel 1 goto error

git status --short

git diff --cached --quiet
if errorlevel 1 (
    git commit -m "Upload Network Scanner files"
    if errorlevel 1 goto error
)

echo.
echo Uploading all project files to GitHub...
git push -u origin main
if errorlevel 1 goto error

echo.
echo =====================================
echo          UPLOAD SUCCESSFUL
echo =====================================
echo https://github.com/Amjad-Alawad/Network-Scanner
pause
exit /b 0

:error
echo.
echo UPLOAD FAILED. Check the error above.
pause
exit /b 1