#!/bin/bash
# Очистка сессий OpenClaw при переполнении контекста

SESSIONS_DIR="$HOME/.openclaw/agents/main/sessions"

# Подсчёт файлов
COUNT=$(ls -1 "$SESSIONS_DIR"/*.json 2>/dev/null | wc -l | tr -d ' ')

if [ "$COUNT" -gt 0 ]; then
    rm -f "$SESSIONS_DIR"/*.json
    echo "Удалено $COUNT сессий"

    # Перезапуск gateway
    openclaw gateway restart 2>/dev/null | grep -v DEP0040 | grep -v "trace-deprecation"
    echo "Gateway перезапущен"
else
    echo "Сессий нет"
fi
