@echo off
:: Перемикаємо кодування консолі на UTF-8 для коректного відображення кирилиці
chcp 65001 >nul
title Ukrposhta Fast-Track Pro Launcher
setlocal

echo ====================================================
echo    UKRPOSHTA FAST-TRACK PRO: ЗАПУСК СИСТЕМИ
echo ====================================================

:: Перевірка наявності uv у системному PATH або локально
uv --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [УВАГА] Менеджер 'uv' не знайдено.
    echo Спроба автоматичного встановлення...
    
    :: Використовуємо більш стабільний метод завантаження через PowerShell
    powershell -NoProfile -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://astral.sh/uv/install.ps1'))"
    
    :: Додаємо локальний шлях встановлення uv до поточної сесії (стандарт для uv)
    set "PATH=%PATH%;%USERPROFILE%\.cargo\bin;%LOCALAPPDATA%\uv"
    
    :: Повторна перевірка
    uv --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo.
        echo [ПОМИЛКА] Не вдалося автоматично встановити 'uv'.
        echo Будь ласка, встановіть його вручну, виконавши команду в PowerShell:
        echo irm astral.sh/uv/install.ps1 ^| iex
        echo.
        pause
        exit /b
    )
)

:: Створення та налаштування оточення
if not exist ".venv" (
    echo [ІНФО] Створення віртуального середовища Python 3.12...
    uv venv --python 3.12
)

:: Перевірка структури папок
if not exist "templates" (
    echo [ПОМИЛКА] Папка 'templates' не знайдена! 
    echo Створіть папку 'templates' та покладіть туди index.html
    pause
    exit /b
)

:: Встановлення залежностей
echo [ІНФО] Синхронізація бібліотек та перевірка залежностей...
uv pip install -r requirements.txt

:: Запуск додатка
echo [УСПІХ] Запуск локального сервера...
echo Адреса: http://127.0.0.1:5000
echo.
echo Для виходу закрийте це вікно.
echo ----------------------------------------------------

:: Відкриваємо браузер автоматично
start http://127.0.0.1:5000

:: Запуск Python додатка через uv
uv run python app.py

pause