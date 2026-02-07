#!/bin/bash
# Транскрипция голосовых сообщений
# Использование: ./tools/transcribe.sh <audio_file> [язык]
INPUT="$1"
LANG="${2:-ru}"
MODEL="/Users/bond/.openclaw/models/ggml-small.bin"
TMP="/tmp/voice_$(date +%s).wav"

if [ -z "$INPUT" ]; then
  echo "Usage: $0 <audio_file> [lang]"
  exit 1
fi

# Конвертация в WAV 16kHz mono (поддержка .oga, .ogg, .mp3 и т.д.)
/opt/homebrew/bin/ffmpeg -i "$INPUT" -ar 16000 -ac 1 -y "$TMP" </dev/null 2>/tmp/voice_ffmpeg.log
if [ $? -ne 0 ]; then
  echo "[Ошибка конвертации аудио]"
  cat /tmp/voice_ffmpeg.log >&2
  exit 1
fi

# Транскрипция
/opt/homebrew/bin/whisper-cli -m "$MODEL" -l "$LANG" -f "$TMP" --no-timestamps -np 2>/tmp/voice_whisper.log
EXIT_CODE=$?

rm -f "$TMP"

if [ $EXIT_CODE -ne 0 ]; then
  echo "[Ошибка транскрипции]"
  cat /tmp/voice_whisper.log >&2
  exit 1
fi
