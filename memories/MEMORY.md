Python Hermes: `%LOCALAPPDATA%/hermes/tools/python-*/python.exe` — версия маскируется в выводе (****), брать только glob-ом; модули ставить `python.exe -c "import pm; pm.sync_venv(['<extra>'], explicit=True)` из папки hermes-agent.
§
Рустам общается с Hermes голосом (диктовка, русский) и не набирает команды в терминал вручную — ввод с голоса/перепечатка ломают команды. Механические шаги (правка конфигов, append в .env, проверки) делать за него самому; ему оставлять только действие, которое может сделать лишь он (вставить секрет, нажать кнопку), и проверять результат чтением файла, а не по слову «готово».
§
Windows Hermes: файл `$LOCALAPPDATA/hermes/.env` имеет CRLF-переводы строк. При программном дописывании использовать `\r\n`, иначе строки склеиваются; после сохранения в Блокноте любые правки, сделанные агентом после открытия окна, теряются — дописывать до открытия редактора и перечитывать после каждого сохранения.
§
База знаний — Obsidian vault `C:\Users\Пользователь\Documents\JarvisVault` (OBSIDIAN_VAULT_PATH в .env): raw/ (источники, только добавлять), wiki/ (по-русски), daily/, inbox/, index.md, log.md; правила — ПРАВИЛА.md в корне (читать).
§
Chrome speechSynthesis gate: требует user gesture (click/key) для speak(); ошибка 'not-allowed' до первого жеста. Фикс: volume=0 warm-up speak при первом взаимодействии (unlockTTS). sticky — хватает на всю сессию.
§
Фоновый terminal-джоб идёт через WSL (свой Python без uvicorn/vosk) — сервисы 8000/8001 там падают. Windows-сервисы: execute_code → subprocess.Popen([glob-py, script], creationflags=DETACHED_PROCESS|CREATE_NEW_PROCESS_GROUP, stdout→лог) — живут без сессии. Ловушка: распознавание vosk не открывает кириллицу в пути модели — в vosk_server.py есть ascii_path() (8.3).
§
Визуал (figura_sveta_v1.html): проверять результат самому — скриншот через computer_use capture + vision_analyze, а не просить Рустама присылать/смотреть. Он прямо попросил: «на будущее сам проверяй визуал проверяя изображение».