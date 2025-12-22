# RULEV3+ Strategy

Directional trading strategy for Polymarket BTC 15-minute Up/Down markets.

## Core Concept

Instead of arbitrage (buying both sides), RULEV3+ makes directional bets based on:
- **Edge** - The mid price of the stronger side (proxy for market conviction)
- **Timing** - Specific windows where signals are most reliable
- **Position limits** - One trade per zone per session

## Trading Windows

```
Session Timeline (15 minutes):
0:00 ──────────────────────────────────────────── 15:00
     │         │     │         │     │
     0min      3min  3:29      5min  5:59    6min+
     │         │─────│         │─────│       │
     WAIT      CORE            RECOVERY      LATE (no trade)
```

| Zone | Elapsed Time | Action |
|------|--------------|--------|
| WAIT | 0:00 - 2:59 | No trade - too early |
| **CORE** | 3:00 - 3:29 | Primary entry window |
| WAIT | 3:30 - 4:59 | No trade - between windows |
| **RECOVERY** | 5:00 - 5:59 | Secondary entry window |
| LATE | 6:00+ | No trade - too late |

## Entry Conditions

All conditions must be TRUE to enter:

### 1. Time Window
```python
if zone not in ["CORE", "RECOVERY"]:
    return NO_TRADE
```

### 2. Edge Threshold (>= 0.64)
```python
edge = max(up_mid, down_mid)  # Mid price of stronger side
if edge < 0.64:
    return NO_TRADE
```

### 3. Safety Cap (< 0.72)
```python
ask = up_ask if direction == "Up" else down_ask
if ask >= 0.72:
    return NO_TRADE  # Too expensive
```

### 4. Zone Limit (max 1 per zone)
```python
if zone_trades[zone] >= 1:
    return NO_TRADE
```

### 5. Cooldown (5 seconds)
```python
if time_since_last_trade < 5:
    return NO_TRADE
```

## Direction Selection

```python
up_mid = (up_bid + up_ask) / 2
down_mid = (down_bid + down_ask) / 2

if up_mid > down_mid:
    direction = "Up"
    edge = up_mid
else:
    direction = "Down"
    edge = down_mid
```

The direction with higher mid price shows stronger market conviction.

## Position Sizing

```python
shares = cash_per_trade / ask_price

# Example:
# $5.00 / $0.65 = 7.69 shares
```

## Expected Value

```python
# If we buy at ask price:
if_win = shares * 1.00 - cost   # Shares pay $1 each
if_lose = -cost                  # Lose entire stake

# EV calculation:
# edge represents implied win probability
ev = edge * if_win - (1 - edge) * if_lose
```

| Entry @ | Shares ($5) | If Win | If Lose | Break-even WR |
|---------|-------------|--------|---------|---------------|
| $0.65 | 7.69 | +$2.69 | -$5.00 | 65% |
| $0.60 | 8.33 | +$3.33 | -$5.00 | 60% |
| $0.55 | 9.09 | +$4.09 | -$5.00 | 55% |

## Settlement

Polymarket auto-settles at session end:
- If BTC went up: UP shares pay $1.00 each, DOWN pays $0
- If BTC went down: DOWN shares pay $1.00 each, UP pays $0

**No need to sell** - just hold until settlement.

## Safety Features

### Double Execution Lock
```
TRADING_MODE=real AND EXECUTION_ENABLED=true
```
Both must be true for real orders.

### Trade Limiter
```python
MAX_LIVE_TRADES_PER_RUN = 1  # or 0 for unlimited
```

### Kill Switch
```python
if degraded_fills >= 2:
    kill_switch = True  # Stop all trading
```

### Zone Limits
```python
max_trades_per_zone = 1
# Only 1 CORE and 1 RECOVERY trade per session
```

## Backtest Results

Based on 100+ sessions:

| Metric | Value |
|--------|-------|
| Win Rate | ~63% |
| Avg Entry | $0.575 |
| Sweet Spot (< $0.58) | 80% WR |
| EV/Trade | +$0.024 |

### Entry Price Analysis

| Price Bucket | Win Rate | EV/Trade |
|--------------|----------|----------|
| < $0.58 | **80%** | **+$0.26** |
| $0.58 - $0.64 | 54% | -$0.07 |
| > $0.64 | 50% | -$0.27 |

## Configuration

```bash
# .env settings
PM_EDGE_THRESHOLD=0.64    # Min edge to trade
PM_SAFETY_CAP=0.72        # Max price to pay
PM_CASH_PER_TRADE=5.00    # $ per trade
PM_MAX_POSITION=8.00      # Max total position
```

## Key Insights

1. **Edge = Classification, not Speed**
   - We're not racing on milliseconds
   - We're classifying which side has conviction

2. **Timing Windows Matter**
   - CORE (3:00-3:29): Primary signal
   - RECOVERY (5:00-5:59): Second chance
   - LATE (6:00+): Signal already priced in

3. **Entry Price is Critical**
   - Below $0.58: Strong +EV
   - Above $0.64: Likely -EV
   - Safety cap at $0.72 prevents overpaying

4. **One Trade Per Zone**
   - Prevents overtrading
   - Forces selectivity
   - Limits exposure per session

## What NOT to Do

| Bad Practice | Why |
|--------------|-----|
| Trade in LATE zone | Signal already priced in |
| Chase high prices (>$0.72) | Negative EV |
| Multiple trades per zone | Overexposure |
| Ignore edge threshold | Random entries |
| Trade both directions | Defeats directional edge |

---

**Strategy Version:** RULEV3+ v1.0
**Last Updated:** December 2025
