#!/bin/bash
# Скрипт патча OpenClaw для Local Bot API
# Запускать после каждого openclaw update

cd /opt/homebrew/lib/node_modules/openclaw/dist

echo "🔧 Patching OpenClaw for Local Bot API..."

# Найти и пропатчить все файлы с api.telegram.org
for f in $(grep -l "api.telegram.org" *.js 2>/dev/null); do
  cp "$f" "${f}.bak"
  sed -i '' 's|https://api.telegram.org|http://localhost:8081|g' "$f"
  echo "✅ $f"
done

echo ""
echo "🔄 Restarting OpenClaw gateway..."
openclaw gateway restart

echo ""
echo "✅ Done! Local Bot API enabled (2GB file limit)"
