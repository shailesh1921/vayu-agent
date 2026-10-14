# VAYU Auto Swing Bot — Deployment Guide

## 🎯 What This Does
- Runs **every trading day at 9:15 AM IST**
- Scans 80+ liquid F&O stocks
- Applies VAYU confluence scoring
- Sends top 3 swing setups to **Telegram** (WhatsApp via workaround)

---

## 🚀 Quick Deploy (VPS/Server)

### 1. Get Telegram Bot Token
```
1. Open Telegram → Search @BotFather
2. /newbot → Name: "VAYU Trader" → Username: "vayu_trader_bot"
3. Copy the token: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```

### 2. Get Your Chat ID
```
1. Message your bot: /start
2. Visit: https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
3. Find "chat":{"id":123456789} → that's your CHAT_ID
```

### 3. Deploy on VPS (Ubuntu/Debian)

```bash
# SSH into your VPS
ssh root@your-vps-ip

# Install dependencies
apt update && apt install -y python3 python3-pip python3-venv git

# Clone your agent (or copy files)
mkdir -p /opt/vayu-bot
cd /opt/vayu-bot

# Copy vayu_bot.py here (or git clone)

# Create virtualenv
python3 -m venv venv
source venv/bin/activate
pip install aiohttp pytz python-dotenv

# Set environment variables
cat > .env << 'EOF'
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789
EOF

# Test run
python vayu_bot.py
# Should print "Next run: 2026-10-14 09:15 IST"
# Press Ctrl+C to stop test
```

### 4. Run as Systemd Service (Auto-start on boot)

```bash
# Create service file
cat > /etc/systemd/system/vayu-bot.service << 'EOF'
[Unit]
Description=VAYU Auto Swing Trade Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/vayu-bot
EnvironmentFile=/opt/vayu-bot/.env
ExecStart=/opt/vayu-bot/venv/bin/python /opt/vayu-bot/vayu_bot.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Enable and start
systemctl daemon-reload
systemctl enable vayu-bot
systemctl start vayu-bot

# Check status
systemctl status vayu-bot
journalctl -u vayu-bot -f  # View logs
```

---

## ☁️ Free Cloud Options (No VPS Cost)

### Option A: GitHub Actions (Free, runs on schedule)
```yaml
# .github/workflows/vayu-daily.yml
name: VAYU Daily Swing
on:
  schedule:
    - cron: '15 3 * * 1-5'  # 9:15 AM IST = 3:45 UTC (adjust for DST)
  workflow_dispatch:

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install aiohttp pytz
      - run: python vayu_bot.py
        env:
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
```
**Add secrets** in GitHub repo: Settings → Secrets → Actions

### Option B: Render.com (Free tier)
- Connect GitHub repo
- Background Worker service
- Set env vars in dashboard
- Runs 24/7 (sleeps after 15 min inactivity — may miss 9:15)

### Option C: Railway.app (Free $5 credit/month)
- Similar to Render, better uptime

### Option D: PythonAnywhere (Free tier)
- Always-on tasks (paid) or scheduled tasks (free, limited)

---

## 📱 WhatsApp Alternative

Telegram is **recommended** (free Bot API). For WhatsApp:

### Option 1: Twilio WhatsApp API (Paid)
```python
# In vayu_bot.py, replace send_telegram with:
from twilio.rest import Client
client = Client(account_sid, auth_token)
client.messages.create(
    from_='whatsapp:+14155238886',
    body=message,
    to='whatsapp:+91XXXXXXXXXX'
)
```

### Option 2: WhatsApp Web Automation (Fragile)
- Use `selenium` or `pywhatkit` — breaks often, not recommended

### Option 3: Telegram → WhatsApp Forward
- Create Telegram channel
- Add WhatsApp forward bot (many free ones exist)
- Or use IFTTT/Zapier: Telegram message → WhatsApp

---

## 🔧 Customize the Bot

### Edit `SWING_UNIVERSE` in vayu_bot.py
```python
# Add/remove symbols
SWING_UNIVERSE = ["YOUR", "FAVORITE", "STOCKS"]
```

### Adjust `MIN_CONFLUENCE`
```python
MIN_CONFLUENCE = 65  # Higher = fewer but better signals
```

### Add Real Data Source
Replace `analyze_universe()` with real API calls:
```python
# Example: NSE API (requires auth)
async def fetch_nse_data(symbol):
    async with aiohttp.ClientSession() as session:
        headers = {"User-Agent": "Mozilla/5.0"}
        url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol}"
        async with session.get(url, headers=headers) as resp:
            return await resp.json()

# Use yfinance (free, rate limited)
import yfinance as yf
data = yf.download("RELIANCE.NS", period="6mo", interval="1d")
```

### Add Holiday Calendar
```python
# Fetch from NSE API or maintain list
NSE_HOLIDAYS_2026 = [
    "2026-01-26", "2026-02-19", "2026-03-14", "2026-04-02", "2026-04-14",
    "2026-05-01", "2026-08-15", "2026-10-02", "2026-10-20", "2026-11-05",
    "2026-11-24", "2026-12-25"
]
```

---

## 📊 Expected Output on Telegram

```
🤖 VAYU DAILY SWING SETUPS
📅 14 Oct 2026, 09:15 IST
📊 Universe: 80 stocks scanned
━━━━━━━━━━━━━━━━━━━━━━━

🟢 VAYU SWING ALERT #1 — RELIANCE
━━━━━━━━━━━━━━━━━━━━━━━
⚡ Confluence: 72/100 (GOOD)
🎯 Direction: LONG
📐 R:R 1:2.1

💰 BUY ZONE: ₹2,850 — ₹2,880
   Ideal: ₹2,865

🎯 TARGETS:
   T1: ₹2,980 (+4.0%)
   T2: ₹3,100 (+8.2%)
   T3: ₹3,250 (+13.4%)

🛑 STOP LOSS: ₹2,780 (-3.0%)

📝 Rationale: Pullback to 20 DMA in uptrend, FII accumulation, sector leader

⏰ Valid for 1-2 weeks. Manage risk: max 2% capital per trade.
```

---

## ✅ Checklist Before Going Live

- [ ] Telegram bot created and token saved
- [ ] Chat ID tested (send test message)
- [ ] VPS/server timezone = Asia/Kolkata (`timedatectl set-timezone Asia/Kolkata`)
- [ ] Holiday calendar updated for current year
- [ ] `MIN_CONFLUENCE` set to your comfort (60-70)
- [ ] Paper trade signals for 2 weeks before real money
- [ ] Log rotation configured (`journalctl --vacuum-time=30d`)

---

## 🛑 To Stop/Update

```bash
# Stop
systemctl stop vayu-bot

# Update code
cd /opt/vayu-bot
git pull  # or copy new files
systemctl restart vayu-bot

# View logs
journalctl -u vayu-bot -f
```

---

## ⚠️ Disclaimer
**This is a decision-support tool, not financial advice.** 
- Paper trade first (2+ weeks)
- Never risk more than you can lose
- Validate signals with your own analysis
- Markets can gap past stop losses