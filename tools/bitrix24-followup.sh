#!/bin/bash
# Bitrix24 Follow-up напоминания
# Находит сделки застрявшие на этапе более 3 дней

set -e

BITRIX_API="https://onlineturplus.bitrix24.ru/rest/1/2grdams84czxo5h8"
DAYS_THRESHOLD=3
DATE_THRESHOLD=$(date -v-${DAYS_THRESHOLD}d +"%Y-%m-%dT00:00:00")

# Временные файлы для результатов
TMP_DIR=$(mktemp -d)
trap "rm -rf $TMP_DIR" EXIT

# Стадии для follow-up (главная воронка, категория 0)
# NEW → "Новая заявка" → Позвонить, выявить потребность
# 1 → "Потребность выявлена" → Подготовить и отправить КП
# PREPARATION → "КП отправлено" → Уточнить решение по КП
# EXECUTING → "Забронировал заявку" → Проверить статус брони

# Получаем сделки по стадии
fetch_deals() {
    local stage=$1
    curl -s "${BITRIX_API}/crm.deal.list" \
        -d "filter[STAGE_ID]=${stage}" \
        -d "filter[CLOSED]=N" \
        -d "filter[<DATE_MODIFY]=${DATE_THRESHOLD}" \
        -d "select[]=ID" \
        -d "select[]=TITLE" \
        -d "select[]=DATE_MODIFY" \
        -d "select[]=CONTACT_ID" \
        -d "select[]=OPPORTUNITY" \
        -d "order[DATE_MODIFY]=ASC"
}

# Получаем имя контакта
get_contact_name() {
    local contact_id=$1
    if [ -z "$contact_id" ] || [ "$contact_id" = "null" ]; then
        echo ""
        return
    fi
    local result=$(curl -s "${BITRIX_API}/crm.contact.get?id=${contact_id}")
    local name=$(echo "$result" | jq -r '.result.NAME // ""')
    local lastname=$(echo "$result" | jq -r '.result.LAST_NAME // ""')
    echo "${name} ${lastname}" | sed 's/^ *//;s/ *$//'
}

# Считаем дни с последнего изменения
days_since() {
    local date_str=$1
    local date_ts=$(date -j -f "%Y-%m-%dT%H:%M:%S" "${date_str%+*}" +%s 2>/dev/null || echo 0)
    local now_ts=$(date +%s)
    echo $(( (now_ts - date_ts) / 86400 ))
}

# Обрабатываем стадию
process_stage() {
    local stage=$1
    local action=$2
    local emoji=$3
    local summary_name=$4
    local outfile=$5
    
    local result=$(fetch_deals "$stage")
    local deals=$(echo "$result" | jq -r '.result // []')
    local count=$(echo "$deals" | jq 'length')
    
    echo "$count" > "${TMP_DIR}/${stage}_count"
    
    if [ "$count" -gt 0 ]; then
        echo "" >> "$outfile"
        echo "${emoji} ${action}:" >> "$outfile"
        
        for i in $(seq 0 $((count - 1))); do
            local deal=$(echo "$deals" | jq ".[$i]")
            local title=$(echo "$deal" | jq -r '.TITLE')
            local date_modify=$(echo "$deal" | jq -r '.DATE_MODIFY')
            local contact_id=$(echo "$deal" | jq -r '.CONTACT_ID')
            local opportunity=$(echo "$deal" | jq -r '.OPPORTUNITY // 0')
            
            local days=$(days_since "$date_modify")
            local contact_name=$(get_contact_name "$contact_id")
            
            # Форматируем сумму
            local opp_str=""
            if [ "$opportunity" != "0" ] && [ "$opportunity" != "null" ] && [ -n "$opportunity" ]; then
                local opp_int=$(printf "%.0f" "$opportunity" 2>/dev/null || echo "$opportunity")
                if [ "$opp_int" != "0" ]; then
                    opp_str=" (${opp_int}₽)"
                fi
            fi
            
            # Добавляем контакт если есть
            if [ -n "$contact_name" ] && [ "$contact_name" != " " ]; then
                echo "   • ${title}${opp_str} — ${contact_name} [${days}д]" >> "$outfile"
            else
                echo "   • ${title}${opp_str} [${days}д]" >> "$outfile"
            fi
        done
    fi
}

# Основной файл вывода
OUTPUT="${TMP_DIR}/output.txt"

# Обрабатываем каждую стадию
process_stage "NEW" "Позвонить, выявить потребность" "📞" "Позвонить (потребность)" "$OUTPUT"
process_stage "1" "Подготовить и отправить КП" "📧" "Отправить КП" "$OUTPUT"
process_stage "PREPARATION" "Уточнить решение по КП" "🔄" "Уточнить решение" "$OUTPUT"
process_stage "EXECUTING" "Проверить статус брони" "✅" "Проверить бронь" "$OUTPUT"

# Подсчитываем итоги
count_new=$(cat "${TMP_DIR}/NEW_count" 2>/dev/null || echo 0)
count_1=$(cat "${TMP_DIR}/1_count" 2>/dev/null || echo 0)
count_prep=$(cat "${TMP_DIR}/PREPARATION_count" 2>/dev/null || echo 0)
count_exec=$(cat "${TMP_DIR}/EXECUTING_count" 2>/dev/null || echo 0)

total=$((count_new + count_1 + count_prep + count_exec))

if [ "$total" -eq 0 ]; then
    echo "✅ Нет застрявших сделок (все активны менее ${DAYS_THRESHOLD} дней)"
    exit 0
fi

# Формируем финальный отчёт
echo "⏰ Follow-up напоминания"
echo ""
echo "📊 Сводка:"

[ "$count_new" -gt 0 ] && echo "📞 Позвонить (потребность): ${count_new}"
[ "$count_1" -gt 0 ] && echo "📧 Отправить КП: ${count_1}"
[ "$count_prep" -gt 0 ] && echo "🔄 Уточнить решение: ${count_prep}"
[ "$count_exec" -gt 0 ] && echo "✅ Проверить бронь: ${count_exec}"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━"

cat "$OUTPUT"

echo ""
echo "💡 Сделки без изменений более ${DAYS_THRESHOLD} дней"
