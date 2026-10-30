Windows Hermes install: the managed Python is `$LOCALAPPDATA/hermes/tools/python-*/python.exe` — the version dir name is partly masked in tool output, so resolve it with a glob (`ls -d .../tools/python-*/`), never a copied literal path (a literal fails with 'No such file or directory'). Install Python extras with `python.exe -c "import pm; pm.sync_venv(['<extra>'], explicit=True)"` run from the hermes-agent source dir.
§
STT: stt.provider groq (whisper-large-v3, ключ в .env, ~2 с, проверено вживую); локальный faster-whisper small — запасной, откат = stt.provider: local (конфиг кэшится по подписи, без перезапуска). TTS: JarvisTools/dmitry_tts4.py — первым Яндекс SpeechKit (YANDEX_API_KEY в .env, kirill/neutral, ~0.8 с), откат на edge + тёплый Piper (piper_warm.py, 18734, 4–5 с); ffmpeg — JarvisTools/ffmpeg.exe.
§
Рустам общается с Hermes голосом (диктовка, русский) и не набирает команды в терминал вручную — ввод с голоса/перепечатка ломают команды. Механические шаги (правка конфигов, append в .env, проверки) делать за него самому; ему оставлять только действие, которое может сделать лишь он (вставить секрет, нажать кнопку), и проверять результат чтением файла, а не по слову «готово».
§
Windows Hermes: файл `$LOCALAPPDATA/hermes/.env` имеет CRLF-переводы строк. При программном дописывании использовать `\r\n`, иначе строки склеиваются; после сохранения в Блокноте любые правки, сделанные агентом после открытия окна, теряются — дописывать до открытия редактора и перечитывать после каждого сохранения.
§
Windows-аккаунт кириллический (`Пользователь`): MSYS bash искажает вывод нативных команд и реестра на таких путях (mojibake, `grep -P` падает). Юникод-данные (реестр, имена значений) читать и писать через PowerShell — не через `reg`/grep.
§
База знаний — Obsidian vault `C:\Users\Пользователь\Documents\JarvisVault` (OBSIDIAN_VAULT_PATH в .env): raw/ (источники, только добавлять), wiki/ (по-русски), daily/, inbox/, index.md, log.md; правила — ПРАВИЛА.md в корне (читать).
§
Instagram: вход в браузере, instagram.com/explore/search/keyword/?q=СЛОВО. Только смотреть. Навык: instagram-search. Источники: JarvisVault/Источники сводки.md