Python Hermes: `%LOCALAPPDATA%/hermes/tools/python-*/python.exe` (версия маскируется — glob); модули ставить `python.exe -c "import pm; pm.sync_venv(['<extra>'], explicit=True)`.
§
Рустам общается голосом (диктовка, русский), команды в терминал не набирает — механические шаги (правки конфигов, .env, проверки) делать за него; ему оставлять только то, что может сделать лишь он (вставить секрет, нажать кнопку), результат проверять чтением файла, а не словом «готово».
§
Windows Hermes: `$LOCALAPPDATA/hermes/.env` с CRLF — дописывать с `\r\n`, иначе строки склеиваются; после сохранения в Блокноте правки агента, сделанные при открытом окне, теряются — дописывать до открытия и перечитывать после сохранения.
§
База знаний — Obsidian vault `C:\Users\Пользователь\Documents\JarvisVault` (OBSIDIAN_VAULT_PATH в .env): raw/ (источники, только добавлять), wiki/ (по-русски), daily/, inbox/, index.md, log.md; правила — ПРАВИЛА.md в корне (читать).
§
Визуал: только http://127.0.0.1:8765/figura_sveta_v1.html (visual_server.py, автозапуск jarvis_http.ps1; origin в api_server.cors_origins). vosk 8001 (Python311, PYTHONPATH не наследовать), TTS 8000/synthesize, ядро 8642. speak() ждёт unlockTTS. Проверять: computer_use capture + vision_analyze.
§
Hermes Mobile v3.0.1 connected via Happ tunnel (Android↔Windows). API Server at http://10.6.7.1:8642 (health: 200). API_SERVER_KEY=2WAFkxYtDDeCK_9uSHGK2sGlipXPkTulhwFMvRUgCyM. TCP proxy: 10.6.7.1:8642 → 127.0.0.1:8642 (PID 22688). config.yaml platforms.api_server.extra.host=0.0.0.0. Happ tunnel: Windows 10.6.7.1, Android 10.6.7.2, port 57208.
§
Hermes Mobile must use HTTP (not TLS/mTLS) to connect to API server at http://100.118.249.102:8642, as the local server only supports HTTP on port 8642.
§
1C client 8.3.27.1688 installed at C:\Program Files\1cv8\8.3.27.1688\, comcntr.dll present at bin\comcntr.dll. Python 3.11.6 with pywin32 312 installed, win32com import verified working.