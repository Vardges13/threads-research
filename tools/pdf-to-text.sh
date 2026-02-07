#!/bin/bash
# PDF to Text extraction using pdftotext (poppler)
# Usage: ./pdf-to-text.sh <input.pdf> [output.txt]
#
# Это альтернативный скрипт для извлечения текста из PDF
# OpenClaw уже поддерживает PDF через pdfjs-dist
# Этот скрипт полезен для тестирования или больших файлов

set -e

# Проверка аргументов
if [ $# -lt 1 ]; then
    echo "Usage: $0 <input.pdf> [output.txt]" >&2
    exit 1
fi

INPUT="$1"
OUTPUT="${2:-}"

# Проверка существования файла
if [ ! -f "$INPUT" ]; then
    echo "Error: File not found: $INPUT" >&2
    exit 1
fi

# Проверка что это PDF
if ! file "$INPUT" | grep -q "PDF"; then
    echo "Error: Not a PDF file: $INPUT" >&2
    exit 1
fi

# Проверка pdftotext
PDFTOTEXT="/opt/homebrew/bin/pdftotext"
if [ ! -x "$PDFTOTEXT" ]; then
    PDFTOTEXT=$(which pdftotext 2>/dev/null || true)
fi

if [ -z "$PDFTOTEXT" ] || [ ! -x "$PDFTOTEXT" ]; then
    echo "Error: pdftotext not found. Install with: brew install poppler" >&2
    exit 1
fi

# Извлечение текста
if [ -n "$OUTPUT" ]; then
    # Вывод в файл
    "$PDFTOTEXT" -layout "$INPUT" "$OUTPUT"
    echo "Text extracted to: $OUTPUT"
    echo "Characters: $(wc -c < "$OUTPUT")"
else
    # Вывод в stdout
    "$PDFTOTEXT" -layout "$INPUT" -
fi
