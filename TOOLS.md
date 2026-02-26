# TOOLS.md — Инструменты Бонда

## 🎙️ Голосовые (STT)
- **whisper-cli** (brew, v1.8.3)
- Модель: `/Users/bond/.openclaw/models/ggml-small.bin` (multilingual small)
- Скрипт: `tools/transcribe.sh <audio_file> [lang]`
- По умолчанию: русский (`ru`)
- Конвертация + транскрипция за 2-5 сек

## 🤖 Локальные модели (Ollama)
- **Ollama** v0.15.2 (brew services, автозапуск)
- Модель: `llama3.1:8b` (4.7 ГБ, ~2с на ответ)
- API: `http://localhost:11434`
- RAM: 16 ГБ (Mac mini)
- Для: простые задачи, черновики, перефразирование — бесплатно

## 📧 Email (Himalaya)
- **Gmail**: Vardges13@gmail.com (default)
- **Mail.ru**: vardges13@mail.ru
- Пароли: macOS Keychain (не в конфигах)
- Конфиг: `~/.config/himalaya/config.toml`
- Команды: `himalaya envelope list`, `himalaya message read <id>`
- Для Mail.ru: `himalaya envelope list --account mailru`

## 🔊 TTS (голосовые ответы)
- **Edge TTS** — единственный провайдер (ElevenLabs/OpenAI удалены)
- Голос: `ru-RU-DmitryNeural` (мужской, бодрый, позитивный)
- Настройки: pitch +10%, rate +20%
- **Отправка:** ТОЛЬКО через `tts()` tool (теги `[[tts]]` НЕ работают)
- Скрипт-бэкап: `tools/tts-edge.sh "текст" [output.ogg] [voice]`
- Конфиг: `messages.tts` в openclaw.json

## 💬 Каналы
- **Telegram (личка)**: @vardges (id:58584187) — основной
- **Telegram-канал**: @vardges13 (chatId: -1001909283235) — публикация постов, Бонд = админ

## 🔧 GitHub
- Аккаунт: **Vardges13**
- CLI: `gh` (авторизован)
- Репо канбана: `Vardges13/bond-kanban`

## 📋 Канбан
- URL: https://vardges13.github.io/bond-kanban/
- Бот: `@Bond007_007_bot`
- Кнопка меню: «📋 Канбан»
- Данные: Telegram CloudStorage (`kanban_tasks_v3`)

## 📄 PDF/Документы
- **Встроено в OpenClaw** — PDF обрабатывается автоматически!
- Библиотека: `pdfjs-dist@5.4.624`
- Лимиты: 5MB, 4 страницы, 200k символов
- Альтернативный скрипт: `tools/pdf-to-text.sh <file.pdf>`
- Зависимость: `pdftotext` (poppler) — уже установлен
- Документация: `docs/PDF-SUPPORT.md`

## 🧠 Скиллы (ClawHub)
- blog-writer — написание статей
- focus-deep-work — фокус и deep work
- 50-ai-templates — шаблоны промптов
- flowmind — управление задачами
- skill-email-management — работа с почтой
- adhd-body-doubling — продуктивность
- yahoo-finance — финансовые данные
- **model-router** ✅ — умный выбор модели

## 🤖 Smart Router
Автоматический выбор оптимальной модели:
```bash
cd skills/model-router
python3 scripts/classify_task.py "твоя задача"
```

**Модели:**
- 🟢 **llama** (бесплатно) — простые вопросы, факты, расчёты
- 🟡 **sonnet** (средний) — анализ, планы, письма, исследования  
- 🔴 **opus** (максимум) — код, архитектура, креатив, сложные задачи

**Экономия: 70-80%** на API при правильном роутинге

## 📁 Workspace структура
```
/Users/bond/.openclaw/workspace/
├── AGENTS.md          — правила поведения
├── SOUL.md            — личность Бонда
├── USER.md            — профиль Вардгеса
├── IDENTITY.md        — ID карточка
├── MEMORY.md          — долгосрочная память
├── HEARTBEAT.md       — проактивные проверки
├── TOOLS.md           — этот файл
├── memory/            — дневные логи
│   ├── YYYY-MM-DD.md
│   └── heartbeat-state.json
├── tools/             — скрипты
│   ├── transcribe.sh
│   └── pdf-to-text.sh
├── docs/              — документация
│   └── PDF-SUPPORT.md
├── kanban-app/        — Telegram Mini App
│   └── index.html
└── skills/            — установленные ClawHub скиллы
```
