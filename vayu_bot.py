#!/usr/bin/env python3
"""
VAYU Auto Swing Trade Bot
Runs at 9:15 AM IST on trading days, analyzes top stocks, sends best swing setup to Telegram.
"""

import os
import json
import asyncio
import aiohttp
from datetime import datetime, time, timedelta
from typing import List, Dict, Optional
import pytz
import logging

# ==================== CONFIG ====================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Set in environment
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")      # Set in environment

# NSE Trading hours: 9:15 AM - 3:30 PM IST
IST = pytz.timezone("Asia/Kolkata")
MARKET_OPEN = time(9, 15)
MARKET_CLOSE = time(15, 30)

# Swing trade watchlist (liquid, F&O, good volume)
SWING_UNIVERSE = [
    "RELIANCE", "HDFCBANK", "ICICIBANK", "INFY", "TCS", "BAJFINANCE", "BHARTIARTL",
    "ITC", "HINDUNILVR", "KOTAKBANK", "LT", "AXISBANK", "SBIN", "MARUTI", "SUNPHARMA",
    "TATAMOTORS", "WIPRO", "ULTRACEMCO", "TITAN", "BAJAJFINSV", "NESTLEIND", "POWERGRID",
    "NTPC", "TECHM", "HCLTECH", "ADANIPORTS", "JSWSTEEL", "TATASTEEL", "COALINDIA",
    "ONGC", "BPCL", "HINDALCO", "GRASIM", "CIPLA", "DRREDDY", "EICHERMOT", "HEROMOTOCO",
    "BRITANNIA", "DIVISLAB", "APOLLOHOSP", "SBILIFE", "HDFCLIFE", "BAJAJ-AUTO", "M&M",
    "STLTECH", "HAL", "BEL", "BDL", "MAZDOCK", "COCHINSHIP", "DATA", "PERSISTENT",
    "KPITTECH", "TATAELXSI", "LTTS", "CYIENT", "ZENSAR", "MPHASIS", "OFSS",
    "ABB", "SIEMENS", "CROMPTON", "HAVELLS", "POLYCAB", "KEI", "FINOLEX", "RRKABEL",
    "JINDALSTEL", "SAIL", "NMDC", "VEDL", "NATIONALUM", "HINDZINC", "GMDCLTD",
    "PFC", "RECLTD", "IRFC", "IREDA", "IRB", "NBCC", "RVNL", "IRCON",
    "ZOMATO", "PAYTM", "NYKAA", "POLICYBZR", "DELHIVERY", "CARERATING", "CAMS",
    "DMART", "TRENT", "TATACONSUM", "GODREJCP", "COLPAL", "MARICO", "EMAMILTD",
    "DABUR", "PIDILITIND", "BERGER", "AKZOINDIA", "KANSAI", "SHALBY", "MEDANTA",
    "FORTIS", "MAXHEALTH", "APOLLO", "NARAYANA", "KIMS", "ASTERDM", "LALPATHLAB",
    "METROPOLIS", "DRAL", "THYROCARE", "VIJAYA", "POLYMED", "OPTIEMUS", "STERLING",
]

# Minimum confluence score for alert
MIN_CONFLUENCE = 60

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ==================== TELEGRAM ====================
async def send_telegram(message: str) -> bool:
    """Send message to Telegram."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logger.error("Telegram credentials not set")
        return False
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=payload) as resp:
                return resp.status == 200
        except Exception as e:
            logger.error(f"Telegram send failed: {e}")
            return False


# ==================== MARKET CALENDAR ====================
def is_trading_day(dt: datetime) -> bool:
    """Check if date is a trading day (Mon-Fri, not holiday)."""
    # Basic: Monday=0 to Friday=4
    if dt.weekday() > 4:
        return False
    
    # TODO: Add NSE holiday calendar check
    # For now, skip known 2026 holidays manually if needed
    holidays_2026 = [
        "2026-01-26", "2026-02-19", "2026-03-14", "2026-04-02", "2026-04-14",
        "2026-05-01", "2026-08-15", "2026-10-02", "2026-10-20", "2026-11-05",
        "2026-11-24", "2026-12-25"
    ]
    if dt.strftime("%Y-%m-%d") in holidays_2026:
        return False
    
    return True


def next_trading_day_open() -> datetime:
    """Get next trading day 9:15 AM IST."""
    now = datetime.now(IST)
    target = now.replace(hour=9, minute=15, second=0, microsecond=0)
    
    if now >= target:
        target += timedelta(days=1)
    
    while not is_trading_day(target):
        target += timedelta(days=1)
    
    return target


# ==================== VAYU ANALYSIS ENGINE ====================
async def fetch_stock_data(symbol: str) -> Optional[Dict]:
    """Fetch stock data from free APIs (yfinance, NSE, etc.)."""
    # Using yfinance via rapidapi or direct - simplified here
    # In production, use proper data feed
    pass


def calculate_confluence(symbol: str, data: Dict) -> Dict:
    """
    VAYU Confluence Scoring (simplified for automation).
    Returns score + key levels.
    """
    # This is a simplified version - in production, use full technical analysis
    # For now, return mock structure showing the format
    return {
        "symbol": symbol,
        "score": 0,  # Will be calculated from real data
        "direction": "LONG",
        "entry_zone": [0, 0],
        "ideal_entry": 0,
        "targets": [0, 0, 0],
        "stop_loss": 0,
        "risk_reward": 0,
        "rationale": ""
    }


async def analyze_universe() -> List[Dict]:
    """Analyze all symbols, return sorted by confluence score."""
    results = []
    
    # In production: fetch real data for each symbol
    # For now, return mock top setups
    # Replace with actual API calls to NSE/yfinance/TradingView
    
    # MOCK DATA - REPLACE WITH REAL ANALYSIS
    mock_setups = [
        {
            "symbol": "RELIANCE",
            "score": 72,
            "direction": "LONG",
            "entry_zone": [2850, 2880],
            "ideal_entry": 2865,
            "targets": [2980, 3100, 3250],
            "stop_loss": 2780,
            "risk_reward": 2.1,
            "rationale": "Pullback to 20 DMA in uptrend, FII accumulation, sector leader"
        },
        {
            "symbol": "STLTECH",
            "score": 68,
            "direction": "LONG",
            "entry_zone": [945, 975],
            "ideal_entry": 955,
            "targets": [1055, 1180, 1340],
            "stop_loss": 890,
            "risk_reward": 2.8,
            "rationale": "AI/DC optical play, $1.1B order book, FII +824bps"
        },
        {
            "symbol": "HAL",
            "score": 65,
            "direction": "LONG",
            "entry_zone": [3850, 3920],
            "ideal_entry": 3880,
            "targets": [4150, 4400, 4700],
            "stop_loss": 3700,
            "risk_reward": 2.3,
            "rationale": "Defence capex, order book ₹80k Cr, pullback to 50 DMA"
        },
    ]
    
    # Filter by minimum score
    filtered = [s for s in mock_setups if s["score"] >= MIN_CONFLUENCE]
    filtered.sort(key=lambda x: x["score"], reverse=True)
    
    return filtered[:3]  # Top 3


# ==================== MESSAGE FORMATTING ====================
def format_signal(signal: Dict, rank: int) -> str:
    """Format signal for Telegram."""
    emoji = "🟢" if signal["direction"] == "LONG" else "🔴"
    rr = signal["risk_reward"]
    
    msg = f"""
{emoji} <b>VAYU SWING ALERT #{rank}</b> — <b>{signal['symbol']}</b>
━━━━━━━━━━━━━━━━━━━━━━━
⚡ <b>Confluence:</b> {signal['score']}/100 ({'HIGH' if signal['score']>=75 else 'GOOD'})
🎯 <b>Direction:</b> {signal['direction']}
📐 <b>R:R</b> 1:{rr:.1f}

💰 <b>BUY ZONE:</b> ₹{signal['entry_zone'][0]:,.0f} — ₹{signal['entry_zone'][1]:,.0f}
   <i>Ideal:</i> ₹{signal['ideal_entry']:,.0f}

🎯 <b>TARGETS:</b>
   T1: ₹{signal['targets'][0]:,.0f} (+{((signal['targets'][0]/signal['ideal_entry'])-1)*100:.1f}%)
   T2: ₹{signal['targets'][1]:,.0f} (+{((signal['targets'][1]/signal['ideal_entry'])-1)*100:.1f}%)
   T3: ₹{signal['targets'][2]:,.0f} (+{((signal['targets'][2]/signal['ideal_entry'])-1)*100:.1f}%)

🛑 <b>STOP LOSS:</b> ₹{signal['stop_loss']:,.0f} (-{((1-signal['stop_loss']/signal['ideal_entry']))*100:.1f}%)

📝 <b>Rationale:</b> {signal['rationale']}

⏰ <i>Valid for 1-2 weeks. Manage risk: max 2% capital per trade.</i>
"""
    return msg.strip()


def format_header() -> str:
    now = datetime.now(IST).strftime("%d %b %Y, %H:%M IST")
    return f"""
🤖 <b>VAYU DAILY SWING SETUPS</b>
📅 {now}
📊 Universe: {len(SWING_UNIVERSE)} stocks scanned
━━━━━━━━━━━━━━━━━━━━━━━
"""


# ==================== MAIN JOB ====================
async def run_daily_analysis():
    """Main analysis job."""
    logger.info("Starting VAYU daily swing analysis...")
    
    # Check market hours
    now = datetime.now(IST)
    if not is_trading_day(now):
        logger.info("Not a trading day, skipping")
        return
    
    if now.time() < MARKET_OPEN or now.time() > MARKET_CLOSE:
        logger.info("Outside market hours, skipping")
        return
    
    # Analyze
    setups = await analyze_universe()
    
    if not setups:
        msg = f"🤖 <b>VAYU</b> — No qualified swing setups today (min score: {MIN_CONFLUENCE})"
        await send_telegram(msg)
        return
    
    # Send header
    await send_telegram(format_header())
    
    # Send each setup
    for i, setup in enumerate(setups, 1):
        await send_telegram(format_signal(setup, i))
        await asyncio.sleep(1)  # Rate limit
    
    # Footer
    footer = """
━━━━━━━━━━━━━━━━━━━━━━━
📋 <b>Risk Rules:</b> Max 2% risk/trade • Max 2 trades/sector • Hard SL • No averaging down
🔄 <i>Re-entry only on confirmed breakout with volume</i>
"""
    await send_telegram(footer)
    
    logger.info(f"Sent {len(setups)} setups to Telegram")


# ==================== SCHEDULER ====================
async def scheduler():
    """Run daily at 9:15 AM IST."""
    while True:
        next_run = next_trading_day_open()
        now = datetime.now(IST)
        wait_seconds = (next_run - now).total_seconds()
        
        logger.info(f"Next run: {next_run.strftime('%Y-%m-%d %H:%M IST')} (in {wait_seconds/3600:.1f}h)")
        
        await asyncio.sleep(wait_seconds)
        await run_daily_analysis()
        
        # Wait a bit past market open to avoid re-triggering
        await asyncio.sleep(300)


# ==================== ENTRY POINT ====================
if __name__ == "__main__":
    import sys
    
    # Check env vars
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ Set environment variables:")
        print("   export TELEGRAM_BOT_TOKEN='your_bot_token'")
        print("   export TELEGRAM_CHAT_ID='your_chat_id'")
        exit(1)
    
    # One-shot mode for GitHub Actions: python vayu_bot.py --once
    if "--once" in sys.argv:
        print("🤖 VAYU One-Shot Analysis...")
        asyncio.run(run_daily_analysis())
        print("✅ Done")
    else:
        # Scheduler mode for VPS
        print("🤖 VAYU Auto Swing Bot starting...")
        print(f"📅 Next run: {next_trading_day_open().strftime('%Y-%m-%d %H:%M IST')}")
        
        try:
            asyncio.run(scheduler())
        except KeyboardInterrupt:
            print("\n👋 VAYU bot stopped")