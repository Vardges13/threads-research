#!/bin/bash
# Edge TTS voice generator for Bond
# Usage: tts-edge.sh "текст" [output.ogg] [voice]
# Voices: ru-RU-DmitryNeural (male), ru-RU-SvetlanaNeural (female)

TEXT="$1"
OUTPUT="${2:-/tmp/bond_voice.ogg}"
VOICE="${3:-ru-RU-DmitryNeural}"
TMP_MP3="/tmp/edge_tts_tmp.mp3"

if [ -z "$TEXT" ]; then
  echo "Usage: tts-edge.sh \"текст\" [output.ogg] [voice]"
  exit 1
fi

edge-tts --voice "$VOICE" --text "$TEXT" --write-media "$TMP_MP3" 2>/dev/null \
  && ffmpeg -y -i "$TMP_MP3" -c:a libopus "$OUTPUT" 2>/dev/null \
  && rm -f "$TMP_MP3" \
  && echo "$OUTPUT"
