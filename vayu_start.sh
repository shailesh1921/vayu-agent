#!/bin/bash
export TELEGRAM_BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-}"
export TELEGRAM_CHAT_ID="${TELEGRAM_CHAT_ID:-}"
cd /Users/shaileshsingh/vayu-agent
python3 vayu_real.py --once
