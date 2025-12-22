# JUMP01X - RULEV3+ Polymarket Trading Bot

Directional trading bot for Polymarket BTC 15-minute Up/Down prediction markets.

## What It Does

Trades Polymarket's "Will BTC go up in the next 15 minutes?" markets using RULEV3+ strategy.

**The Strategy:**
- Enter in specific time windows (CORE: 3:00-3:29, RECOVERY: 5:00-5:59)
- Edge threshold >= 0.64 (mid price of stronger side)
- Safety cap < 0.72 (avoid overpaying)
- Auto-settlement at session end (no need to sell)

**Example:**
```
Session starts: 00:00:00
CORE window:    00:03:00 - 00:03:29
Signal: UP @ $0.65, Edge = 0.64

Buy 7.69 UP shares @ $0.65 = $5.00
If BTC goes up: Win $7.69 - $5.00 = +$2.69
If BTC goes down: Lose $5.00
```

## Quick Start

```bash
# 1. Install dependencies
pip install rich py-clob-client python-dotenv websockets aiohttp

# 2. Configure
cp .env.example .env
# Edit .env with your Polymarket credentials

# 3. Run (paper mode by default)
python ui_dashboard_live.py
```

## Trading Modes

| Mode | Settings | Description |
|------|----------|-------------|
| **Paper** | `TRADING_MODE=paper` | Simulated trades, no real money |
| **Real (blocked)** | `TRADING_MODE=real`, `EXECUTION_ENABLED=false` | Shows signals but blocks orders |
| **Real (live)** | `TRADING_MODE=real`, `EXECUTION_ENABLED=true` | Actual order execution |

## Project Structure

```
JUMP01X/
├── ui_dashboard_live.py      # Main trading dashboard
├── trade_executor.py         # Order execution engine
├── polymarket_connector.py   # WebSocket + API connector
├── .env                      # Configuration (private keys, settings)
│
├── logs/
│   ├── paper/               # Paper trade logs
│   └── real/                # Real trade logs
│
├── docs/
│   ├── STRATEGY.md          # RULEV3+ strategy details
│   ├── STATE.md             # Current project status
│   └── SETUP.md             # Installation guide
│
└── backtest_full_logs/      # Historical backtest data
    ├── scripts/             # Backtest scripts
    └── reports/             # Analysis reports
```

## Configuration (.env)

```bash
# Trading Mode
TRADING_MODE=paper           # paper or real
EXECUTION_ENABLED=false      # true to allow real orders
MAX_LIVE_TRADES_PER_RUN=1    # Safety limit (0 = unlimited)

# Polymarket Credentials
PM_PRIVATE_KEY=0x...         # Your wallet private key
PM_WALLET_ADDRESS=0x...      # Proxy wallet address
PM_FUNDER_ADDRESS=0x...      # Funder address
PM_SIGNATURE_TYPE=2          # 0=EOA, 1=Poly, 2=Gnosis

# Strategy Settings
PM_CASH_PER_TRADE=5.00       # $ per trade
PM_MAX_POSITION=8.00         # Max position size
PM_EDGE_THRESHOLD=0.64       # Min edge to trade
PM_SAFETY_CAP=0.72           # Max price to pay
```

## Dashboard Features

```
┌─────────────────────────────────────────────────────────────────────┐
│ RULEV3+ LIVE PAPER │ S:6(2skip) | T:3(1pend) | W/L:1/1(50%) | PnL:$-2.31 │
└─────────────────────────────────────────────────────────────────────┘
```

**Live Stats:**
- `S:6(2skip)` - Sessions seen (skipped without signal)
- `T:3(1pend)` - Total trades (pending settlement)
- `W/L:1/1(50%)` - Wins/Losses (win rate)
- `PnL:$-2.31` - Running profit/loss

**Panels:**
- Live prices (UP/DOWN bid/ask)
- Order book depth
- Session info (zone, elapsed, countdown)
- Performance (trades, W/L, EV, PnL)
- Zones (CORE/RECOVERY entries)
- Config (strategy parameters)
- Logs (real-time activity)

## Safety Features

1. **Double lock** - Requires BOTH `TRADING_MODE=real` AND `EXECUTION_ENABLED=true`
2. **Trade limiter** - `MAX_LIVE_TRADES_PER_RUN` caps live orders
3. **Kill switch** - Auto-stops after 2 degraded fills
4. **Zone limits** - Max 1 trade per zone per session
5. **Cooldown** - 5s between trades

## Logs

**Paper trades:** `logs/paper/trades_YYYYMMDD_HHMMSS.log`
**Real trades:** `logs/real/trades_YYYYMMDD_HHMMSS.log`

**Log contents:**
- Session rollovers
- Trade entries with full details (edge, price, shares, EV)
- Settlement results (win/loss, PnL)
- Periodic stats (every 5 min)
- Final session summary

## First Live Trade

**Date:** 2025-12-22
**Result:** FILLED

```
Direction: UP
Zone: CORE
Edge: 0.640
Ask: $0.65
Shares: 7.69
Cost: $5.00
Slippage: 0bps
Latency: 942ms
Order ID: 0x7205e791...
```

## Docs

| File | Description |
|------|-------------|
| [docs/STRATEGY.md](docs/STRATEGY.md) | RULEV3+ strategy logic |
| [docs/STATE.md](docs/STATE.md) | Current project status |
| [docs/SETUP.md](docs/SETUP.md) | Installation guide |

---

**Status:** Live Trading Active (Dec 2025)
**Strategy:** RULEV3+ Directional
**Mode:** Paper (testing)
