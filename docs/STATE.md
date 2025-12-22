# JUMP01X - Project State

**Updated:** 2025-12-23
**Status:** Live Trading Active (Paper Mode)

---

## Current Status

| Item | Status |
|------|--------|
| Strategy | RULEV3+ v1.0 |
| Mode | Paper Trading |
| Trade Size | $5.00 per trade |
| First Live Trade | 2025-12-22 (SUCCESS) |

## First Live Trade

**Date:** December 22, 2025
**Session:** btc-updown-15m-1766438100

```
Direction: UP
Zone: CORE
Edge: 0.640
Ask: $0.65
Shares: 7.69
Cost: $5.00
Slippage: 0bps
Latency: 942ms
Order ID: 0x7205e791158e74755ac95a02641379b8e51bdd146f4561cd5a3661eb49fc77eb
Status: FILLED
```

---

## Configuration

### .env Settings

```bash
TRADING_MODE=paper
EXECUTION_ENABLED=false
MAX_LIVE_TRADES_PER_RUN=0

PM_CASH_PER_TRADE=5.00
PM_MAX_POSITION=8.00
PM_EDGE_THRESHOLD=0.64
PM_SAFETY_CAP=0.72
```

### Strategy Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| CORE Window | 3:00-3:29 | Primary entry window |
| RECOVERY Window | 5:00-5:59 | Secondary entry window |
| Edge Threshold | >= 0.64 | Minimum edge to trade |
| Safety Cap | < 0.72 | Maximum price to pay |
| Trade Size | $5.00 | Per trade |
| Max Position | $8.00 | Total exposure limit |

---

## Files

### Core System

| File | Purpose |
|------|---------|
| `ui_dashboard_live.py` | Main trading dashboard |
| `trade_executor.py` | Order execution engine |
| `polymarket_connector.py` | WebSocket + CLOB API |
| `.env` | Configuration |

### Logs

| Location | Content |
|----------|---------|
| `logs/paper/` | Paper trade logs |
| `logs/real/` | Real trade logs |
| `real_logs/` | First live trade archive |

### Documentation

| File | Content |
|------|---------|
| `README.md` | Project overview |
| `docs/STRATEGY.md` | RULEV3+ strategy details |
| `docs/STATE.md` | This file |
| `docs/SETUP.md` | Installation guide |

---

## Dashboard Features

### Header Stats (Live)
```
S:6(2skip) | T:3(1pend) | W/L:1/1(50%) | PnL:$-2.31
```

- `S:6(2skip)` - Sessions seen (skipped)
- `T:3(1pend)` - Trades total (pending settlement)
- `W/L:1/1(50%)` - Wins/Losses (win rate)
- `PnL:$-2.31` - Running profit/loss

### Panels

1. **Live Prices** - UP/DOWN bid/ask spreads
2. **Order Book** - Depth and mid prices
3. **Session Info** - Zone, elapsed, countdown
4. **Performance** - Trades, W/L, EV, PnL
5. **Zones** - CORE/RECOVERY entry counts
6. **Config** - Strategy parameters
7. **Logs** - Real-time activity

---

## Safety Features

| Feature | Status |
|---------|--------|
| Double execution lock | Active |
| Trade limiter | Active (0 = unlimited) |
| Kill switch | Ready (2 degraded fills) |
| Zone limits | Active (1 per zone) |
| Cooldown | Active (5 seconds) |

---

## Logging

### Paper Trade Log Entry
```
==================================================
PAPER TRADE #1
==================================================
TIME:      2025-12-22 23:05:02.921
SESSION:   btc-updown-15m-1766440800
ZONE:      RECOVERY
DIRECTION: Up
FILL:      FILLED (spread: $0.0200)
EDGE:      0.6400
ASK:       $0.6500
BID:       $0.6300
SHARES:    7.6923
COST:      $5.00
IF_WIN:    +$2.69
IF_LOSE:   -$5.00
EV/TRADE:  +$0.42
```

### Settlement Log
```
SESSION SETTLEMENT: btc-updown-15m-1766440800
==================================================
FINAL UP:   $0.9500
FINAL DOWN: $0.0500
WINNER:     UP
TRADE #1: Up @ $0.65
  RESULT: WIN | PnL: +$2.69
```

### Periodic Stats (every 5 min)
```
[STATS] 5m | Sessions: 6 (skip:4) | Trades: 2 (pend:1) | W/L: 1/0 (100%) | EV: $+2.69 | PnL: $+2.69
```

---

## History

### December 22, 2025
- First successful live trade executed
- Switched to paper mode for extended testing
- Added win/loss settlement tracking
- Added sessions skipped counter
- Added EV per trade calculation
- Added bid fill status tracking
- Enhanced logging with all metrics

### December 21, 2025
- Completed pre-live verification (44 tests)
- Added double execution lock
- Added trade limiter
- Added kill switch

---

## Next Steps

1. Run paper trading overnight
2. Collect 50+ settled trades
3. Analyze win rate by zone (CORE vs RECOVERY)
4. Validate EV calculations
5. Consider going live with small position

---

**Mode:** Paper
**Strategy:** RULEV3+ v1.0
**Balance:** $11.90 USDC
