import os, asyncio, aiohttp, ssl, certifi, pytz
from datetime import datetime
import yfinance as yf
from ta import trend, momentum, volatility

IST=pytz.timezone('Asia/Kolkata')
TOKEN=os.getenv('TELEGRAM_BOT_TOKEN'); CHAT=os.getenv('TELEGRAM_CHAT_ID')
UNIV=['RELIANCE.NS','INFY.NS','HDFCBANK.NS']

async def send(m):
    ctx=ssl.create_default_context(cafile=certifi.where())
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ctx)) as s:
        await s.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",json={'chat_id':CHAT,'text':m,'parse_mode':'HTML'})

async def main():
    for sym in UNIV:
        df=yf.download(sym,period='4mo',interval='1d',progress=False,auto_adjust=True)
        if len(df)<50: continue
        close=df['Close'].squeeze()
        ema20=trend.EMAIndicator(close,20).ema_indicator().squeeze()
        p=float(close.iloc[-1])
        await send(f'<b>VAYU</b> {sym.replace(".NS","")} ₹{p:.2f}')
        break

asyncio.run(main())
