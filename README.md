# VAYU — Elite Indian Market Trading Intelligence Agent

> *"The wind that reveals the trend, the discipline that captures it."*

A complete, production-ready trading intelligence system for NSE/BSE markets. Combines 25 years of quantitative + discretionary expertise into a structured, repeatable framework.

---

## 📦 Package Contents

```
vayu-agent/
├── vayu.md                    # Complete agent definition (system prompt)
├── kilo.json                  # Kilo configuration with commands
├── CHEATSHEET.md              # Quick reference for daily trading
├── WATCHLIST_TEMPLATE.md      # Daily watchlist template
├── TRADE_JOURNAL_TEMPLATE.md  # Trade logging & analysis template
├── MARKET_CONTEXT_TEMPLATE.md # Pre-market context template
└── README.md                  # This file
```

---

## 🚀 Quick Start

### 1. As a Kilo Agent
```bash
# Copy to your project's .kilo/agent/ directory
cp vayu.md .kilo/agent/vayu.md
cp kilo.json .kilo/kilo.json  # or merge with existing
```

### 2. As a Standalone System Prompt
Use `vayu.md` as the system prompt for any LLM with web search capability.

### 3. As a Manual Framework
Print `CHEATSHEET.md` and use templates daily.

---

## 🎯 Core Commands (via Kilo)

| Command | Description |
|---------|-------------|
| `/vayu-analyze SYMBOL [TIMEFRAME]` | Full confluence analysis + trade signal |
| `/vayu-watchlist` | Generate daily top 5-8 setups |
| `/vayu-market-context` | Current market snapshot |
| `/vayu-premarket` | Pre-market brief (8:00 AM) |
| `/vayu-sector-analysis` | Sector rotation + top picks |

**Examples:**
```
/vayu-analyze RELIANCE
/vayu-analyze HDFCBANK 1-WEEK_SWING
/vayu-analyze STLTECH 2-WEEK_POSITIONAL
/vayu-watchlist
/vayu-premarket
```

---

## 🧠 The VAYU Methodology

### 1. **Top-Down Analysis** (Never Bottom-Up First)
```
Global Macro → India Macro → Sector Rotation → Stock Selection
     ↓              ↓              ↓              ↓
  Fed/China    RBI/FII/DII    Momentum Rank   Confluence Score
  Yields/Crude  VIX/Budget     Top 3 Sectors   ≥60 = Trade
```

### 2. **Multi-Timeframe Confluence** (8 Timeframes)
| Trade Type | Trend TF | Entry TF |
|------------|----------|----------|
| Intraday | 1H | 5m/3m |
| Swing (1W) | Daily | 1H/4H |
| Positional (2W) | Weekly | Daily/4H |

### 3. **20+ Indicator Technical Engine**
- **Trend**: EMA Ribbon, SuperTrend, ADX, Ichimoku
- **Momentum**: RSI, MACD, StochRSI, CCI, Williams%R
- **Volume**: VPVR, VWAP, OBV, Delivery%, Vol MA
- **Structure**: Pivots, Fibonacci, Price Action, PDH/PDL, ORB
- **Volatility**: Bollinger Bands, ATR, India VIX

### 4. **Confluence Scoring** (0-100)
| Factor | Weight | Max |
|--------|--------|-----|
| Multi-TF Trend | Critical | 15 |
| Key S/R Confluence | Critical | 15 |
| Volume Confirmation | High | 12 |
| Momentum Alignment | High | 12 |
| Price Action | Medium | 10 |
| Fundamental Quality | Medium | 10 |
| FII/DII Flow | Medium | 8 |
| Sector Strength | Medium | 8 |
| Market Breadth/VIX | Low | 5 |
| Risk:Reward | Low | 5 |
| **TOTAL** | | **100** |

### 5. **Signal Thresholds**
- **≥75** → ⚡ HIGH CONVICTION (Full size)
- **60-74** → ✅ GOOD SETUP (75% size)
- **45-59** → ⚠️ WATCHLIST (Wait)
- **<45** → ❌ NO TRADE (Skip)

---

## 📊 Trade Signal Output Format

Every analysis produces a structured signal:

```
═══════════════════════════════════════════════════
📊 TRADE SIGNAL — STOCK NAME (NSE:SYMBOL)
═══════════════════════════════════════════════════
🏷️ Signal Type    : 1-WEEK SWING
🎯 Direction      : LONG (BUY)
⚡ Conviction     : ✅ GOOD — Confluence Score: 68/100
📅 Date/Time      : 13 Oct 2026, 08:40 IST
⏰ Validity       : Valid until 27 Oct or breach ₹XXX

━━━ PRICE LEVELS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ BUY ZONE       : ₹XXX — ₹XXX
   (Ideal Entry)  : ₹XXX
🎯 TARGET 1       : ₹XXX (+X%) — Book 40%
🎯 TARGET 2       : ₹XXX (+X%) — Book 35%
🎯 TARGET 3       : ₹XXX (+X%) — Trail 25%
🛑 STOP LOSS      : ₹XXX (-X%) — HARD STOP
📐 Risk:Reward    : 1:X.X

━━━ POSITION SIZING ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 Capital at Risk : X% (max 2%)
📦 Suggested Qty  : XX shares
💸 Max Loss       : ₹X,XXX

━━━ TECHNICAL RATIONALE ━━━━━━━━━━━━━━━━━━━━━━━━━
📈 Trend (HTF)    : BULLISH — Reason
📊 Structure      : HH/HL, pullback to 20 DMA
🔵 Key S/R        : Support ₹XX, Resistance ₹XX
📉 Indicators     : MACD>0, RSI 55, ADX 35, SuperTrend BUY
📊 Volume         : OBV rising, delivery 52%, >2x avg on breakout
🕯️ Price Action   : Bullish engulfing at support

━━━ FUNDAMENTAL SNAPSHOT ━━━━━━━━━━━━━━━━━━━━━━━
🏢 Sector         : Sector — Rank: X/11
📊 Market Cap     : ₹XX,XXX Cr (Mid Cap)
💹 PE / PEG       : XX.X / X.X
📈 Rev Growth     : QoQ X%, YoY X%
🏛️ FII/DII        : FII +X%, DII +X%
👔 Promoter       : XX%, Pledge: 0%

━━━ CONFLUENCE BREAKDOWN ━━━━━━━━━━━━━━━━━━━━━━
[Detailed factor-by-factor scoring table]

━━━ RISK FACTORS & MANAGEMENT ━━━━━━━━━━━━━━━━━
⚠️ Risks          : 1. Specific risk  2. Specific risk  3. Specific risk
📋 Exit Rules     : Trail SL after T1, time stop, structure stop
🔄 Re-entry       : Conditions for re-entry if stopped
═══════════════════════════════════════════════════
```

---

## 🛡️ Risk Management (Non-Negotiable)

| Rule | Limit |
|------|-------|
| Risk per trade | 2% of capital (max) |
| Total portfolio risk | 6% (max concurrent) |
| Single stock exposure | 20% (max) |
| Intraday trades/day | 3 (max) |
| Daily loss limit | 3% → STOP TRADING |
| Consecutive losses | 2 → reduce size 50% |
| VIX > 22 | Reduce size 50% |
| VIX > 28 | Intraday only |
| Sector concentration | 2 trades max/sector |

**Stop Loss:** Sacred. Pre-defined. Never widened. Never averaged down.

---

## 📅 Daily Routine

```
08:00  Pre-market: GIFT Nifty, Globals, FII/DII, VIX, Gaps
08:30  Watchlist: Update levels, scan 200+ stocks
09:15  Wait for 15-min candle (NO TRADES 9:15-9:18)
09:30  Execute pre-planned signals
10:00  Sector rotation check
11:30  Mid-session: Trail stops, book partials
13:30  Lunch break (reduce screen time)
14:30  Carry-forward decisions for swings
15:15  Square off ALL intraday
15:30  EOD review, journal, update watchlist
16:00  Scan daily charts for new swing setups
17:00  Done
```

---

## 📈 Specialized Strategies

### Intraday (Same-Day Exit)
- **ORB**: Opening Range Breakout (15-min)
- **VWAP Reversion**: ±2σ mean reversion (5-min)
- **Gap & Go/Fade**: Gap >1% with catalyst (3-min)
- **Pivot Bounce**: S1/R1 with confirmation (15-min)

### Swing (1-Week)
- **Pullback to MA**: 21 EMA in uptrend (Daily)
- **Volume Breakout**: Consolidation break >2x vol (Daily)
- **RSI Divergence**: Price low, RSI higher low (Daily+4H)

### Positional (2-Week)
- **Weekly Breakout**: Multi-week base + volume (Weekly)
- **Sector Rotation**: Strongest stock in strongest sector (Daily+Weekly)
- **Earnings Momentum**: Post-result gap hold, buy pullback (Daily)

---

## 🔍 Data Sources Used

| Category | Sources |
|----------|---------|
| **Price/Technical** | NSE/BSE, TradingView, ChartInk, yfinance, Trendlyne |
| **Fundamental** | Screener.in, Company filings, MoneyControl, ET |
| **Institutional** | NSE FII/DII reports, Trendlyne, Tijori, BSE bulk deals |
| **Macro** | RBI, CMIE, MOSPI, Investing.com, Bloomberg |
| **News/Flow** | MoneyControl, ET, Mint, CNBC-TV18, Twitter/X |

---

## ⚠️ What VAYU NEVER Does

- ❌ Trade without stop loss
- ❌ Chase moves >3% from ideal entry
- ❌ Revenge trade after losses
- ❌ Trade penny stocks / SME / illiquid (<₹5 Cr/day)
- ❌ Trade first 3 minutes (9:15-9:18)
- ❌ Hold intraday overnight without swing thesis
- ❌ Ignore stop loss hits
- ❌ Trade tips/rumors/WhatsApp forwards
- ❌ Overtrade (2-3 quality > 10 mediocre)
- ❌ Increase size after winning streak
- ❌ Trade unknown businesses (for swings)
- ❌ Go all-in on single trade

---

## 📋 Templates Included

1. **CHEATSHEET.md** — One-page reference for levels, patterns, sizing, rules
2. **WATCHLIST_TEMPLATE.md** — Daily top 5 longs + 3 shorts + sector watch
3. **TRADE_JOURNAL_TEMPLATE.md** — Complete entry → management → analysis log
4. **MARKET_CONTEXT_TEMPLATE.md** — Pre-market brief structure

Print these. Use daily. Build the habit.

---

## 🎓 Calibration Guide

**Month 1:** Paper trade only. Track every signal. Compare predicted vs actual.
**Month 2:** 25% capital. Focus on execution discipline.
**Month 3:** 50% capital. Refine confluence thresholds for your style.
**Month 4+:** Full capital. Monthly review: win rate, R-multiple, drawdown.

**Target Metrics:**
- Win Rate: 65-75%
- Avg R-Multiple: >2.0
- Max Drawdown: <6%
- Profit Factor: >1.5

---

## 🔧 Customization

Adjust in `vayu.md`:
- **Risk tolerance** → Position sizing rules
- **Time availability** → Intraday vs Swing vs Positional focus
- **Capital size** → Absolute position limits
- **Sector preference** → Sector rotation priority
- **Indicator weights** → Confluence scoring

---

## 📜 License & Disclaimer

**MIT License** — Use freely, modify, share.

> **DISCLAIMER:** VAYU is a decision-support framework, not financial advice. All trading involves risk. Past performance ≠ future results. Never risk money you can't afford to lose. Consult a SEBI-registered advisor for personalized advice.

---

## 🤝 Contributing

Found an edge? Improving a strategy? Adding a data source?
1. Fork the framework
2. Test rigorously (6+ months out-of-sample)
3. Document the change + evidence
4. Share back

---

## 🙏 Acknowledgments

Built on the shoulders of:
- Indian market microstructure researchers
- Quantitative finance pioneers
- Discretionary trading legends
- The NSE/BSE ecosystem
- Every trader who journaled their losses honestly

---

**VAYU** — Where wind meets discipline.

*May your stops be tight, your targets wide, and your mind calm.*