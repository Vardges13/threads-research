#!/bin/bash
# WHOOP API Data Fetcher

CONFIG_FILE="$(dirname "$0")/config.json"
ACCESS_TOKEN=$(jq -r '.access_token' "$CONFIG_FILE")
API_BASE="https://api.prod.whoop.com/developer/v1"

case "$1" in
  profile)
    curl -s "$API_BASE/user/profile/basic" -H "Authorization: Bearer $ACCESS_TOKEN"
    ;;
  cycle)
    curl -s "$API_BASE/cycle?limit=${2:-1}" -H "Authorization: Bearer $ACCESS_TOKEN"
    ;;
  sleep)
    curl -s "$API_BASE/activity/sleep?limit=${2:-1}" -H "Authorization: Bearer $ACCESS_TOKEN"
    ;;
  workout)
    curl -s "$API_BASE/activity/workout?limit=${2:-1}" -H "Authorization: Bearer $ACCESS_TOKEN"
    ;;
  recovery)
    curl -s "$API_BASE/cycle" -H "Authorization: Bearer $ACCESS_TOKEN" | jq '.records[0]'
    ;;
  body)
    curl -s "$API_BASE/user/measurement/body" -H "Authorization: Bearer $ACCESS_TOKEN"
    ;;
  refresh)
    # Refresh token flow
    CLIENT_ID=$(jq -r '.client_id' "$CONFIG_FILE")
    CLIENT_SECRET=$(jq -r '.client_secret' "$CONFIG_FILE")
    REFRESH_TOKEN=$(jq -r '.refresh_token' "$CONFIG_FILE")
    
    RESPONSE=$(curl -s -X POST "https://api.prod.whoop.com/oauth/oauth2/token" \
      -H "Content-Type: application/x-www-form-urlencoded" \
      -d "grant_type=refresh_token" \
      -d "refresh_token=$REFRESH_TOKEN" \
      -d "client_id=$CLIENT_ID" \
      -d "client_secret=$CLIENT_SECRET")
    
    NEW_TOKEN=$(echo "$RESPONSE" | jq -r '.access_token')
    if [ "$NEW_TOKEN" != "null" ]; then
      jq --arg token "$NEW_TOKEN" '.access_token = $token' "$CONFIG_FILE" > tmp.json && mv tmp.json "$CONFIG_FILE"
      echo "Token refreshed successfully"
    else
      echo "Failed to refresh token: $RESPONSE"
    fi
    ;;
  *)
    echo "Usage: $0 {profile|cycle|sleep|workout|recovery|body|refresh} [limit]"
    ;;
esac
