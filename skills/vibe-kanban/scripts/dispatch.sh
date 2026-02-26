#!/bin/bash

# dispatch.sh - Скрипт для запуска кодинг-агентов по задачам
# Использование: ./dispatch.sh '{"title":"Task","agent":"Claude Code","description":"..."}'

set -e

# Проверка аргументов
if [ $# -eq 0 ]; then
    echo "❌ Ошибка: Не передан JSON задачи"
    echo "Использование: $0 '{\"title\":\"Task\",\"agent\":\"Claude Code\",\"description\":\"...\"}'"
    exit 1
fi

TASK_JSON="$1"

# Парсинг JSON (простая версия с jq если доступно, иначе базовый grep)
if command -v jq >/dev/null 2>&1; then
    TITLE=$(echo "$TASK_JSON" | jq -r '.title // "Untitled Task"')
    AGENT=$(echo "$TASK_JSON" | jq -r '.agent // "Claude Code"')
    DESCRIPTION=$(echo "$TASK_JSON" | jq -r '.description // ""')
    PRIORITY=$(echo "$TASK_JSON" | jq -r '.priority // "medium"')
else
    # Fallback без jq
    TITLE=$(echo "$TASK_JSON" | grep -o '"title":"[^"]*' | cut -d'"' -f4 | head -1)
    AGENT=$(echo "$TASK_JSON" | grep -o '"agent":"[^"]*' | cut -d'"' -f4 | head -1)
    DESCRIPTION=$(echo "$TASK_JSON" | grep -o '"description":"[^"]*' | cut -d'"' -f4 | head -1)
    PRIORITY=$(echo "$TASK_JSON" | grep -o '"priority":"[^"]*' | cut -d'"' -f4 | head -1)
    
    # Значения по умолчанию
    [ -z "$TITLE" ] && TITLE="Untitled Task"
    [ -z "$AGENT" ] && AGENT="Claude Code"
    [ -z "$PRIORITY" ] && PRIORITY="medium"
fi

echo "🚀 Диспатчинг задачи: $TITLE"
echo "👤 Агент: $AGENT"
echo "📊 Приоритет: $PRIORITY"
[ -n "$DESCRIPTION" ] && echo "📝 Описание: $DESCRIPTION"
echo "---"

# Формирование команды в зависимости от агента
case "$AGENT" in
    "Claude Code")
        echo "💡 Команда для Claude Code (OpenClaw):"
        echo "openclaw exec '$TITLE'"
        if [ -n "$DESCRIPTION" ]; then
            echo "# Контекст: $DESCRIPTION"
        fi
        echo ""
        echo "🔧 Для выполнения скопируйте команду выше"
        ;;
        
    "Cursor")
        echo "💡 Команда для Cursor CLI:"
        echo "cursor-compose '$TITLE'"
        if [ -n "$DESCRIPTION" ]; then
            echo "# $DESCRIPTION"
        fi
        echo ""
        echo "🔧 Для выполнения:"
        echo "1. Откройте проект в Cursor"
        echo "2. Используйте Cmd+K для Composer"
        echo "3. Введите: $TITLE"
        ;;
        
    "Copilot"|"GitHub Copilot")
        echo "💡 Команда для GitHub Copilot CLI:"
        echo "gh copilot suggest '$TITLE'"
        if [ -n "$DESCRIPTION" ]; then
            echo "# Context: $DESCRIPTION"
        fi
        echo ""
        echo "🔧 Для выполнения:"
        echo "1. Убедитесь что установлен: gh extension install github/gh-copilot"
        echo "2. Выполните команду выше"
        ;;
        
    "Custom"|*)
        echo "💡 Кастомная задача:"
        echo "Задача: $TITLE"
        if [ -n "$DESCRIPTION" ]; then
            echo "Описание: $DESCRIPTION"
        fi
        echo ""
        echo "🔧 Выполните вручную или настройте интеграцию"
        ;;
esac

echo ""
echo "✨ Диспатчинг завершён!"

# Логирование (опционально)
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
LOG_DIR="$(dirname "$0")/../logs"
mkdir -p "$LOG_DIR"

echo "[$TIMESTAMP] Dispatched: $TITLE -> $AGENT" >> "$LOG_DIR/dispatch.log"

# Возврат успешного кода
exit 0