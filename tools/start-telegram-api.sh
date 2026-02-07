#!/bin/bash
# Start local Telegram Bot API server
# Removes the 20MB download limit (supports up to 2GB)
# Requires: api_id and api_hash from https://my.telegram.org

API_ID="${TELEGRAM_API_ID:?Set TELEGRAM_API_ID}"
API_HASH="${TELEGRAM_API_HASH:?Set TELEGRAM_API_HASH}"
PORT="${TELEGRAM_API_PORT:-8081}"
DATA_DIR="${TELEGRAM_API_DATA:-/Users/bond/.openclaw/telegram-bot-api-data}"

mkdir -p "$DATA_DIR"

exec /usr/local/bin/telegram-bot-api \
  --api-id="$API_ID" \
  --api-hash="$API_HASH" \
  --http-port="$PORT" \
  --dir="$DATA_DIR" \
  --local \
  --log=/Users/bond/.openclaw/logs/telegram-bot-api.log \
  --verbosity=2
