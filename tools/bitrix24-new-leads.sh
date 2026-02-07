#!/bin/bash
# Bitrix24 New Deals Monitor
# Проверяет новые сделки и отправляет уведомления в Telegram

BITRIX_API="https://onlineturplus.bitrix24.ru/rest/1/2grdams84czxo5h8"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LAST_DEAL_FILE="$SCRIPT_DIR/bitrix24-last-deal.txt"

# Получаем ID последней проверенной сделки
if [[ -f "$LAST_DEAL_FILE" ]]; then
    LAST_ID=$(cat "$LAST_DEAL_FILE")
else
    LAST_ID=0
fi

# Получаем новые сделки (отсортированы по ID по возрастанию, фильтр >LAST_ID)
DEALS=$(curl -s "$BITRIX_API/crm.deal.list" \
    -d "select[]=ID" \
    -d "select[]=TITLE" \
    -d "select[]=OPPORTUNITY" \
    -d "select[]=DATE_CREATE" \
    -d "filter[>ID]=$LAST_ID" \
    -d "order[ID]=ASC")

# Проверяем есть ли результаты
TOTAL=$(echo "$DEALS" | jq -r '.total // 0')

if [[ "$TOTAL" -eq 0 ]]; then
    echo "$(date): Новых сделок нет"
    exit 0
fi

echo "$(date): Найдено новых сделок: $TOTAL"

# Обрабатываем каждую сделку
MAX_ID=$LAST_ID
echo "$DEALS" | jq -c '.result[]' | while read -r DEAL; do
    ID=$(echo "$DEAL" | jq -r '.ID')
    TITLE=$(echo "$DEAL" | jq -r '.TITLE')
    OPPORTUNITY=$(echo "$DEAL" | jq -r '.OPPORTUNITY // "0"')
    DATE_CREATE=$(echo "$DEAL" | jq -r '.DATE_CREATE')
    
    # Форматируем дату
    DATE_FORMATTED=$(echo "$DATE_CREATE" | cut -d'T' -f1,2 | tr 'T' ' ' | cut -d'+' -f1)
    
    # Формируем сообщение
    MESSAGE="🔔 Новая заявка в CRM!
👤 $TITLE
💰 $OPPORTUNITY ₽
📅 $DATE_FORMATTED"
    
    echo "Отправляю уведомление о сделке #$ID: $TITLE"
    
    # Отправляем через OpenClaw message
    openclaw message send \
        --channel telegram \
        --target 58584187 \
        --message "$MESSAGE" \
        2>/dev/null
    
    # Обновляем максимальный ID
    if [[ "$ID" -gt "$MAX_ID" ]]; then
        MAX_ID=$ID
    fi
    
    # Сохраняем ID после каждой обработанной сделки
    echo "$MAX_ID" > "$LAST_DEAL_FILE"
    
    sleep 1  # Пауза между уведомлениями
done

# Сохраняем последний проверенный ID
NEW_MAX=$(echo "$DEALS" | jq -r '.result | last | .ID // empty')
if [[ -n "$NEW_MAX" ]]; then
    echo "$NEW_MAX" > "$LAST_DEAL_FILE"
    echo "$(date): Обновлён last ID: $NEW_MAX"
fi
