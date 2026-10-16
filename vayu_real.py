#!/usr/bin/env python3
import os, sys, asyncio, aiohttp, pytz
from datetime import datetime, time, timedelta
import yfinance as yf
import pandas as pd
import numpy as np
from ta import trend, momentum, volatility

IST = pytz.timezone("Asia/Kolkata")
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT = os.getenv("TELEGRAM_CHAT_ID")

UNIVERSE = ["RELIANCE.NS","HDFCBANK.NS","ICICIBANK.NS","INFY.NS","TCS.NS","STLTECH.NS","HAL.NS","BEL.NS","ITC.NS","SBIN.NS","BAJFINANCE.NS","BHARTIARTL.NS","ADANIPORTS.NS"]

async def send(m):
    if not TOKEN or not CHAT:
        return
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    async with aiohttp.ClientSession() as s:
        await s.post(url, json={"chat_id":CHAT,"text":m,"parse_mode":"HTML","disable_web_page_preview":True})

async def analyze(sym):
    try:
        df = yf.download(sym, period="5mo", interval="1d", progress=False, auto_adjust=True)
        if df.empty or len(df) < 60:
            return None
        df['ema20'] = trend.EMAIndicator(df['Close'], 20).ema_indicator()
        df['ema50'] = trend.EMAIndicator(df['Close'], 50).ema_indicator()
        df['ema200'] = trend.EMAIndicator(df['Close'], 200).ema_indicator()
        df['rsi'] = momentum.RSIIndicator(df['Close'], 14).rsi()
        macd = trend.MACD(df['Close'])
        df['macd'] = macd.macd()
        df['macds'] = macd.macd_signal()
        df['adx'] = trend.ADXIndicator(df['High'], df['Low'], df['Close'], 14).adx()
        df['atr'] = volatility.AverageTrueRange(df['High'], df['Low'], df['Close'], 14).average_true_range()
        d = df.iloc[-1]
        score = 0
        p = d['Close']
        if p > d['ema20']: score += 12
        if p > d['ema50']: score += 8
        if p > d['ema200']: score += 10
        if d['rsi'] > 40 and d['rsi'] < 70: score += 10
        if d['macd'] > d['macds']: score += 10
        if d['adx'] > 25: score += 8
        vol = df['Volume']
        if vol.iloc[-1] > vol.iloc[-20:-1].mean(): score += 12
        if score >= 62:
            sl = p - 1.4 * d['atr']
            t1 = p + 1.6 * d['atr']
            t2 = p + 3 * d['atr']
            t3 = p + 4.5 * d['atr']
            rr = (t1 - p) / (p - sl) if p > sl else 0
            return (sym.replace('.NS',''), min(score,95), round(p,2), round(sl,2), round(t1,2), round(t2,2), round(t3,2), round(rr,1))
    except Exception:
        pass
    return None
async def main():
    res = []
    for s in UNIVERSE[:15]:
        r = await analyze(s)
        if r: res.append(r)
        await asyncio.sleep(0.2)
    res.sort(key=lambda x: x[1], reverse=True)
    res = res[:3]
    if not res:
        await send("🤖 VAYU: No setups today (min 62)")
        return
    txt = "🤖 <b>VAYU REAL SWING SETUPS</b>\n" + datetime.now(IST).strftime('%d %b %Y %H:%M IST') + "\n" + "━"*20 + "\n"
    for i,(s,sc,p,sl,t1,t2,t3,rr) in enumerate(res,1):
        txt += f"<b>#{i} {s}</b> | {sc}/100\nIDEAL {p} | SL {sl}\nT1 {t1} | T2 {t2} | T3 {t3} | R:R 1:{rr}\n\n"
    txt += "<i>Max 2% risk • Hard SL • No averaging down</i>"
    await send(txt)

if __name__ == "__main__":
    if "--once" in sys.argv:
        asyncio.run(main())
    else:
        asyncio.run(main())
