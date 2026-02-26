#!/bin/bash
# Local TTS using macOS built-in voice (Milena for Russian)
# Usage: tts-local.sh "текст" [output.ogg] [voice]

TEXT="$1"
OUTPUT="${2:-/tmp/tts-local.ogg}"
VOICE="${3:-Milena}"  # Russian voice

if [ -z "$TEXT" ]; then
    echo "Usage: tts-local.sh \"text\" [output.ogg] [voice]"
    echo "Voices: Milena (ru), Lesya (uk), Samantha (en)"
    exit 1
fi

# Temp files
AIFF_FILE="/tmp/tts-temp-$$.aiff"

# Generate speech with macOS say
say -v "$VOICE" -o "$AIFF_FILE" "$TEXT"

# Convert to ogg (Telegram voice format)
ffmpeg -y -i "$AIFF_FILE" -c:a libopus -b:a 64k "$OUTPUT" 2>/dev/null

# Cleanup
rm -f "$AIFF_FILE"

echo "$OUTPUT"
