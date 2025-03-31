#!/bin/bash
set -e

APP_NAME="kanji-test-maker"

echo "🔄 Pulling latest code..."
git pull origin main

echo "🧱 Rebuilding Docker image..."
docker compose build

echo "🚀 Restarting container..."
docker compose up -d

echo "✅ Done."