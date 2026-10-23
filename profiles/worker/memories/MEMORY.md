Windows Hermes install: the managed Python is `$LOCALAPPDATA/hermes/tools/python-*/python.exe` — the version dir name is partly masked in tool output, so resolve it with a glob (`ls -d .../tools/python-*/`), never a copied literal path (a literal fails with 'No such file or directory'). Install Python extras with `python.exe -c "import pm; pm.sync_venv(['<extra>'], explicit=True)"` run from the hermes-agent source dir.
§
STT on this machine: local faster-whisper (extra `stt-whisper`), `stt.provider: local`, `stt.local.model: small`, `stt.language: ru`. No cloud STT key configured.
§
Рустам общается с Hermes голосом (диктовка, русский) и не набирает команды в терминал вручную — ввод с голоса/перепечатка ломают команды. Механические шаги (правка конфигов, append в .env, проверки) делать за него самому; ему оставлять только действие, которое может сделать лишь он (вставить секрет, нажать кнопку), и проверять результат чтением файла, а не по слову «готово».
§
Windows Hermes: файл `$LOCALAPPDATA/hermes/.env` имеет CRLF-переводы строк. При программном дописывании использовать `\r\n`, иначе строки склеиваются; после сохранения в Блокноте любые правки, сделанные агентом после открытия окна, теряются — дописывать до открытия редактора и перечитывать после каждого сохранения.
§
Windows-аккаунт кириллический (`Пользователь`): MSYS bash искажает вывод нативных команд и реестра на таких путях (mojibake, `grep -P` падает). Юникод-данные (реестр, имена значений) читать и писать через PowerShell — не через `reg`/grep.
§
faster-whisper на Windows: av==16.0.1 совместим; av==19.x ломается TypeError (metadata_errors). При установке: uv pip install faster-whisper av==16.0.1.
§
База знаний Рустама — Obsidian vault: `C:\Users\Пользователь\Documents\JarvisVault` (путь также в .env как `OBSIDIAN_VAULT_PATH`). Структура: raw/ (источники, только добавлять), wiki/ (страницы знаний, кратко по-русски, ссылки [[...]]), daily/ (ГГГГ-ММ-ДД.md), inbox/ (мысли владельца), index.md (оглавление), log.md (журнал). Полные правила ведения — в файле `ПРАВИЛА.md` в корне базы; перед работой с базой читать его и следовать ему.
§
NOTE: memory is full. Do not add more entries this session.