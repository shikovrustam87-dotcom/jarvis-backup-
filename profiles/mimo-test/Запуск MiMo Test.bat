@echo off
chcp 65001 >nul
echo Запуск Hermes с моделью MiMo-V2.6-Flash (профиль mimo-test)
echo.
set HERMES_PROFILE=mimo-test
hermes
pause
