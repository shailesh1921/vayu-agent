#!/usr/bin/env python3
import os, asyncio, aiohttp, ssl, certifi, pytz
from datetime import datetime
import yfinance as yf
from ta import trend, momentum, volatility

IST=pytz.timezone('Asia/Kolkata')
TOKEN=os.getenv('TELEGRAM_BOT_TOKEN'); CHAT=os.getenv('TELEGRAM_CHAT_ID')
UNIV=['RELIANCE.NS','INFY.NS','TCS.NS','HDFCBANK.NS','ICICIBANK.NS','SBIN.NS','ITC.NS','BHARTIARTL.NS','STLTECH.NS','HAL.NS','BEL.NS','MARUTI.NS','BAJFINANCE.NS']

async def send(m):
    ctx=ssl.create_default_context(cafile=certifi.where())
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ctx)) as s:
        await s.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",json={'chat_id':CHAT,'text':m,'parse_mode':'HTML'})

async def analyze(sym):
    try:
        df=yf.download(sym,period='4mo',interval='1d',progress=False,auto_adjust=True)
        if len(df)<60: return None
        close=df['Close'].squeeze(); high=df['High'].squeeze(); low=df['Low'].squeeze(); vol=df['Volume'].squeeze()
        ema20=trend.EMAIndicator(close,20).ema_indicator().squeeze()
        ema50=trend.EMAIndicator(close,50).ema_indicator().squeeze()
        ema200=trend.EMAIndicator(close,200).ema_indicator().squeeze()
        rsi=momentum.RSIIndicator(close,14).rsi().squeeze()
        macd=trend.MACD(close); macdl=macd.macd().squeeze(); macds=macd.macd_signal().squeeze()
        adx=trend.ADXIndicator(high,low,close,14).adx().squeeze()
        atr=volatility.AverageTrueRange(high,low,close,14).average_true_range().squeeze()
        p=float(close.iloc[-1]); sc=0
        if p>float(ema20.iloc[-1]): sc+=12
        if p>float(ema50.iloc[-1]): sc+=8
        if p>float(ema200.iloc[-1]): sc+=10
        if 40<float(rsi.iloc[-1])<70: sc+=10
        if float(macdl.iloc[-1])>float(macds.iloc[-1]): sc+=10
        if float(adx.iloc[-1])>25: sc+=8
        if float(vol.iloc[-1])>float(vol.iloc[-20:-1].mean()): sc+=12
        if sc>=55:
            sl=p-1.4*float(atr.iloc[-1]); t1=p+1.6*float(atr.iloc[-1]); t2=p+3*float(atr.iloc[-1]); t3=p+4.5*float(atr.iloc[-1]); rr=(t1-p)/(p-sl)
            return (sym.replace('.NS',''),sc,p,sl,t1,t2,t3,rr)
    except: return None

async def main():
    res=[]
    for s in UNIV:
        r=await analyze(s)
        if r: res.append(r)
    res.sort(key=lambda x:x[1],reverse=True)
    if not res: await send("VAYU: No setups today (min 55)"); return
    txt="<b>VAYU SETUPS</b> "+datetime.now(IST).strftime('%H:%M')+"\n"
    for i,x in enumerate(res[:3],1):
        txt+=f"#{i} {x[0]} {x[1]}/100 P{x[2]:.0f} SL{x[3]:.0f} T1{x[4]:.0f} RR{x[7]:.1f}\n"
    await send(txt)

if __name__=='__main__':
    asyncio.run(main())
