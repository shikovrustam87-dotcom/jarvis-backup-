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
Telegram-магазин Рустама развернут в C:/Users/Пользователь/jarvis-shop-bot/. Технологии: aiogram 3 + SQLite. Файлы: bot.py (бот), requirements.txt, .env (нужно заполнить токены), README_SETUP.md (инструкция). Бот поддерживает каталог, корзину, заказ с телефоном/адресом, оплату онлайн через ЮKassa или наличными при получении, уведомления админу. Нужно: токен от @BotFather, платёжный токен ЮKassa (или пусто для наличных), свой Telegram ID в ADMIN_IDS. Запуск: .venv\Scripts\activate && python bot.py. Для 24/7 — перенести на VPS.
§
Инструмент patch некорректно обрабатывает Python-файлы с экранированными обратными слэшами (\n, \t) — возникает ошибка 'Escape-drift detected'. Для правок таких файлов использовать execute_code (read + write) вместо patch.