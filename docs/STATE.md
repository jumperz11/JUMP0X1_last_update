# JUMP01X - Project State

**Updated:** 2024-12-24
**Status:** Phase 1 Paper Trading (Collecting Data)

---

## Current Status

| Item | Status |
|------|--------|
| Strategy | RULEV3+ Phase 1 |
| Mode | Paper Trading |
| Config | LOCKED (see PHASE1_LOCKED.md) |
| Trade Size | $5.00 per trade |
| Target | 50 trades before review |

---

## Phase 1 Configuration

```
ZONE_MODE          = CORE-only (T3 = 3:00-3:29)
EDGE_THRESHOLD     = 0.64
SAFETY_CAP         = 0.72
SPREAD_MAX         = 0.02
ALPHA_GATE         = REMOVED (structural bug)
MAX_TRADES_SESSION = 1
POSITION_SIZE      = $5.00
```

---

## Gate Order (Phase 1)

1. **MODE_ZONE_GATE** - Only CORE zone allowed
2. **BOOK_GATE** - Must have valid bid/ask
3. **SESSION_CAP** - Max 1 trade per session
4. **EDGE_GATE** - edge >= 0.64
5. **HARD_PRICE_GATE** - ask <= 0.72
6. **PRICE_GATE** - ask < 0.72
7. **BAD_BOOK** - spread >= 0 AND bid <= ask
8. **SPREAD_GATE** - spread <= 0.02
9. **EXECUTOR_VALIDATION** - zone limits, cooldowns

---

## Backtest Results (Phase 1)

| Metric | Value |
|--------|-------|
| Total sessions | 2,085 |
| Total trades | 1,064 |
| Win rate | 72.09% |
| AvgPnL/trade | $0.3276 |
| Total PnL | $348.58 |
| Max drawdown | $65.35 |

---

## Paper Trade Progress

| Metric | Current | Target |
|--------|---------|--------|
| Trades collected | 3 | 50 |
| W/L | 2/1 | - |
| Win rate | 67% | ~72% |
| AvgPnL | $+0.05 | ~$0.33 |

---

## Files

### Core System

| File | Purpose |
|------|---------|
| `ui_dashboard_live.py` | Main trading dashboard |
| `trade_executor.py` | Order execution engine |
| `polymarket_connector.py` | WebSocket + CLOB API |
| `backtest_alpha_test.py` | Phase 1 backtest |
| `.env` | Configuration |

### Logs

| Location | Content |
|----------|---------|
| `logs/paper/` | Paper trade logs |
| `logs/real/` | Real trade logs |

### Documentation

| File | Content |
|------|---------|
| `PHASE1_LOCKED.md` | Locked Phase 1 config |
| `docs/STATE.md` | This file |
| `docs/STRATEGY.md` | Strategy details |
| `VERSION` | Version tag |

---

## Periodic Stats Format

```
[STATS] 5m | Sessions: 6 (skip:4) | Trades: 2 (pend:1) | W/L: 1/0 (100%) | AvgPnL: $+2.69 | PnL: $+2.69
```

Note: `AvgPnL` = cumulative PnL / settled trades (renamed from EV for clarity)

---

## Kill Rules

| Trigger | Threshold | Action |
|---------|-----------|--------|
| Max Drawdown | > $130.70 (2x backtest) | STOP |
| Structural Deviation | Wrong zone/sizing/gate | STOP |
| Execution Error | Bad fills, cap failure | STOP |
| AvgPnL Negative | Over 20+ trades | REVIEW |

---

## History

### December 24, 2024
- Phase 1 LOCKED
- Removed alpha gate (structural bug: always negative)
- Added spread hygiene gate (spread <= 0.02)
- Renamed EV → AvgPnL in [STATS] log (label only)
- Created PHASE1_LOCKED.md
- Created VERSION file
- 3 paper trades collected (2W/1L)

### December 22-23, 2024
- First successful live trade executed
- Switched to paper mode for extended testing
- Added win/loss settlement tracking
- Completed pre-live verification (44 tests)

---

## Next Steps

1. Continue paper trading (collect 50 trades)
2. Monitor metrics vs backtest
3. Review after 50 trades or kill rule
4. Phase 2: Build p_model for true alpha calculation

---

**Mode:** Paper
**Strategy:** RULEV3+ Phase 1
**Config:** LOCKED
