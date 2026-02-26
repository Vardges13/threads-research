#!/bin/bash
# Tochka Bank API - Get Balance
# Uses token from macOS Keychain

TOKEN=$(security find-generic-password -a "bond" -s "tochka-api-token" -w 2>/dev/null)

if [ -z "$TOKEN" ]; then
    echo "Error: Token not found in Keychain"
    exit 1
fi

# Get accounts list
curl -s -X GET "https://enter.tochka.com/api/v2/account/list" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json"
