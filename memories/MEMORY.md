Python Hermes: `%LOCALAPPDATA%/hermes/tools/python-*/python.exe` (версия маскируется — glob); модули ставить `python.exe -c "import pm; pm.sync_venv(['<extra>'], explicit=True)`.
§
Рустам общается голосом (диктовка, русский), команды в терминал не набирает — механические шаги (правки конфигов, .env, проверки) делать за него; ему оставлять только то, что может сделать лишь он (вставить секрет, нажать кнопку), результат проверять чтением файла, а не словом «готово».
§
Windows Hermes: `$LOCALAPPDATA/hermes/.env` с CRLF — дописывать с `\r\n`, иначе строки склеиваются; после сохранения в Блокноте правки агента, сделанные при открытом окне, теряются — дописывать до открытия и перечитывать после сохранения.
§
База знаний — Obsidian vault `C:\Users\Пользователь\Documents\JarvisVault` (OBSIDIAN_VAULT_PATH в .env): raw/ (источники, только добавлять), wiki/ (по-русски), daily/, inbox/, index.md, log.md; правила — ПРАВИЛА.md в корне (читать).
§
Фоновый terminal-джоб идёт через WSL (без uvicorn/vosk) — сервисы 8000/8001 там падают. Windows-сервисы: execute_code → subprocess.Popen([glob-py, script], creationflags=DETACHED_PROCESS|CREATE_NEW_PROCESS_GROUP, stdout→лог) — живут без сессии. Vosk не открывает кириллицу в пути — ascii_path() (8.3) в vosk_server.py.
§
Визуал: только http://127.0.0.1:8765/figura_sveta_v1.html (visual_server.py, автозапуск jarvis_http.ps1; origin в api_server.cors_origins). vosk 8001 (Python311, PYTHONPATH не наследовать), TTS 8000/synthesize, ядро 8642. speak() ждёт unlockTTS. Проверять: computer_use capture + vision_analyze.
§
IPv6 сломан (TLS/DNS виснет) — фикс 05.11.2026: ipv6_off_all.ps1 (UAC) гасит ms_tcpip6 на всех адаптерах + реестр Tcpip6\Parameters DisabledComponents=0xFF (постоянно после ребута); всё по IPv4 (dzen, aitunnel). dzen в hosts (95.163.218.220). routing.json Happ не действует — не полагаться.
§
План Рустама: позже установить find-skills (Vercel) — `npx skills add https://github.com/vercel-labs/skills --skill find-skills`; после команды, проверив аудит на skills.sh.