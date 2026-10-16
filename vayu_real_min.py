#!/usr/bin/env python3
import os, asyncio, aiohttp, ssl, certifi, pytz
from datetime import datetime
import yfinance as yf
from ta import trend, momentum, volatility

IST=pytz.timezone('Asia/Kolkata')
TOKEN=os.getenv('TELEGRAM_BOT_TOKEN'); CHAT=os.getenv('TELEGRAM_CHAT_ID')
UNIV=['RELIANCE.NS','INFY.NS','TCS.NS','HDFCBANK.NS','ICICIBANK.NS','SBIN.NS','ITC.NS','BHARTIARTL.NS','STLTECH.NS','HAL.NS','BEL.NS','TATAMOTORS.NS','MARUTI.NS','BAJFINANCE.NS']

async def send(m):
    ctx=ssl.create_default_context(cafile=certifi.where())
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ctx)) as s:
        await s.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",json={'chat_id':CHAT,'text':m,'parse_mode':'HTML'})

async def analyze(sym):
    try:
        df=yf.download(sym,period='4mo',interval='1d',progress=False,auto_adjust=True)
        if len(df)<60: return None
        close=df['Close'].squeeze()
        ema20=trend.EMAIndicator(close,20).ema_indicator().squeeze()
        ema50=trend.EMAIndicator(close,50).ema_indicator().squeeze()
        ema200=trend.EMAIndicator(close,200).ema_indicator().squeeze()
        rsi=momentum.RSIIndicator(close,14).rsi().squeeze()
        macd=trend.MACD(close); macd_l=macd.macd().squeeze(); macds=macd.macd_signal().squeeze()
        adx=trend.ADXIndicator(df['High'],df['Low'],df['Close'],14).adx().squeeze()
        atr=volatility.AverageTrueRange(df['High'],df['Low'],df['Close'],14).average_true_range().squeeze()
        p=float(close.iloc[-1]); sc=0
        if p>float(ema20.iloc[-1]): sc+=12
        if p>float(ema50.iloc[-1]): sc+=8
        if p>float(ema200.iloc[-1]): sc+=10
        if 40<float(rsi.iloc[-1])<70: sc+=10
        if float(macd_l.iloc[-1])>float(macds.iloc[-1]): sc+=10
        if float(adx.iloc[-1])>25: sc+=8
        v=df['Volume'].squeeze()
        if float(v.iloc[-1])>float(v.iloc[-20:-1].mean()): sc+=12
        if sc>=55:
            sl=p-1.4*float(atr.iloc[-1]); t1=p+1.6*float(atr.iloc[-1]); t2=p+3*float(atr.iloc[-1]); t3=p+4.5*float(atr.iloc[-1])
            rr=(t1-p)/(p-sl)
            return (sym.replace('.NS',''),min(sc,95),round(p,2),round(sl,2),round(t1,2),round(t2,2),round(t3,2),round(rr,1))
    except: return None

async def main():
    res=[]
    for s in UNIV:
        r=await analyze(s)
        if r: res.append(r)
    res.sort(key=lambda x:x[1],reverse=True)
    if not res:
        await send("VAYU: No setups today (min 55)")
        return
    txt="<b>VAYU SETUPS</b>\n"+datetime.now(IST).strftime('%d %b %H:%M')+"\n"
    for i,x in enumerate(res[:3],1):
        txt+=f"#{i} {x[0]} {x[1]}/100 P{x[2]} SL{x[3]} T1{x[4]} R:R{x[7]:.1f}\n"
    await send(txt)

if __name__=='__main__':
    asyncio.run(main())
