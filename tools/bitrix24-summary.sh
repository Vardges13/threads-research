#!/bin/bash
# Bitrix24 Daily Summary for OnlineTurPlus
# Sends morning summary to Telegram

set -euo pipefail

BITRIX_API="https://onlineturplus.bitrix24.ru/rest/1/2grdams84czxo5h8"
TELEGRAM_USER="58584187"  # Вардгес

# Даты
TODAY=$(date +%Y-%m-%d)
THREE_DAYS_AGO=$(date -v-3d +%Y-%m-%dT00:00:00 2>/dev/null || date -d "3 days ago" +%Y-%m-%dT00:00:00)

# Функция для API запросов
bitrix_request() {
    local method=$1
    shift
    curl -s -X POST "${BITRIX_API}/${method}" \
        -H "Content-Type: application/json" \
        -d "$@"
}

# 1. Новые сделки за сегодня
echo "📥 Получаю новые сделки за сегодня..."
NEW_DEALS=$(bitrix_request "crm.deal.list" "{
    \"filter\": {
        \">DATE_CREATE\": \"${TODAY}T00:00:00\"
    },
    \"select\": [\"ID\", \"TITLE\", \"OPPORTUNITY\", \"CURRENCY_ID\"]
}")

NEW_COUNT=$(echo "$NEW_DEALS" | jq -r '.total // 0')
NEW_SUM=$(echo "$NEW_DEALS" | jq -r '[.result[]?.OPPORTUNITY // 0 | tonumber] | add // 0')

# 2. Сделки в работе (не закрытые)
echo "🔄 Получаю сделки в работе..."
# Стадии OnlineTurPlus: NEW, 1, PREPARATION, EXECUTING, UC_XNZB94 (в работе)
# Закрытые: WON (Улетел), LOSE (СПАМ), 2 (Купил в др месте), APOLOGY (Передумал)
IN_PROGRESS=$(bitrix_request "crm.deal.list" "{
    \"filter\": {
        \"!STAGE_ID\": [\"WON\", \"LOSE\", \"2\", \"APOLOGY\"]
    },
    \"select\": [\"ID\", \"TITLE\", \"OPPORTUNITY\", \"DATE_MODIFY\", \"STAGE_ID\"]
}")

PROGRESS_COUNT=$(echo "$IN_PROGRESS" | jq -r '.total // 0')
PROGRESS_SUM=$(echo "$IN_PROGRESS" | jq -r '[.result[]?.OPPORTUNITY // 0 | tonumber] | add // 0')

# 3. Застрявшие сделки (>3 дней без изменений)
echo "⏰ Ищу застрявшие сделки..."
STUCK_DEALS=$(bitrix_request "crm.deal.list" "{
    \"filter\": {
        \"<DATE_MODIFY\": \"${THREE_DAYS_AGO}\",
        \"!STAGE_ID\": [\"WON\", \"LOSE\", \"2\", \"APOLOGY\"]
    },
    \"select\": [\"ID\", \"TITLE\", \"OPPORTUNITY\", \"DATE_MODIFY\"]
}")

STUCK_COUNT=$(echo "$STUCK_DEALS" | jq -r '.total // 0')

# Форматирование суммы с пробелами
format_money() {
    printf "%'d" "$1" 2>/dev/null | sed 's/,/ /g' || echo "$1"
}

NEW_SUM_FMT=$(format_money ${NEW_SUM%.*})
PROGRESS_SUM_FMT=$(format_money ${PROGRESS_SUM%.*})

# Формируем сообщение
MESSAGE="📊 *Bitrix24 — утренняя сводка*
_${TODAY}_

• Новых заявок: *${NEW_COUNT}* (сумма: ${NEW_SUM_FMT} ₽)
• В работе: *${PROGRESS_COUNT}* сделок на ${PROGRESS_SUM_FMT} ₽"

if [ "$STUCK_COUNT" -gt 0 ]; then
    MESSAGE="${MESSAGE}
• ⚠️ Застряли: *${STUCK_COUNT}* сделок"
fi

# Детали застрявших (если есть, до 5 штук)
if [ "$STUCK_COUNT" -gt 0 ]; then
    STUCK_DETAILS=$(echo "$STUCK_DEALS" | jq -r '.result[:5][] | "  └ \(.TITLE // "Без названия") — \(.DATE_MODIFY | split("T")[0])"' 2>/dev/null || echo "")
    if [ -n "$STUCK_DETAILS" ]; then
        MESSAGE="${MESSAGE}
${STUCK_DETAILS}"
    fi
fi

echo ""
echo "═══════════════════════════════════════"
echo "$MESSAGE"
echo "═══════════════════════════════════════"

# Отправка в Telegram через OpenClaw
if command -v openclaw &> /dev/null; then
    echo ""
    echo "📤 Отправляю в Telegram..."
    openclaw message send --target "${TELEGRAM_USER}" --message "${MESSAGE}"
    echo "✅ Отправлено!"
else
    echo "⚠️ openclaw не найден, сообщение не отправлено"
fi
