# RULEV3+ GO-LIVE CHECKLIST

**Updated:** 2024-12-24
**Status:** Phase 1 Paper Trading

---

## Strategy Validation

- [x] CORE-only mode validated (T3 = 3:00-3:29)
- [x] Edge threshold >= 0.64 validated
- [x] Safety cap <= 0.72 validated
- [x] Spread gate <= 0.02 validated
- [x] Alpha gate REMOVED (structural bug)
- [x] Backtest: 1064 trades, 72.09% WR, +$348.58 PnL
- [x] Max 1 trade per session validated

---

## Bot Code

- [x] `ui_dashboard_live.py` - Main dashboard
- [x] `trade_executor.py` - Order execution
- [x] `polymarket_connector.py` - WebSocket + API
- [x] `backtest_alpha_test.py` - Phase 1 backtest
- [x] Gate logic implemented (9 gates)
- [x] Paper trade settlement tracking
- [x] Periodic stats logging

---

## UI Dashboard

- [x] Terminal UI (TUI) built with Rich
- [x] Live prices panel
- [x] Order book panel
- [x] Session info panel
- [x] Performance stats panel
- [x] Zones panel
- [x] Config panel
- [x] Live logs panel

---

## Safety Features

- [x] Double execution lock (zone limits)
- [x] Session trade cap (max 1)
- [x] Kill switch (2 degraded fills)
- [x] Cooldown between trades
- [x] Spread gate (hygiene)
- [x] Safety cap (max ask price)

---

## Infrastructure

- [x] Polymarket WebSocket connected
- [x] CLOB API connected
- [x] Wallet configured
- [x] Logging to file enabled
- [x] Paper/Real mode separation

---

## Phase 1 Progress

- [x] Config LOCKED (PHASE1_LOCKED.md)
- [x] VERSION file created
- [ ] 50 paper trades collected (current: 3)
- [ ] Kill rules validated in live
- [ ] Review metrics vs backtest

---

## Kill Rules

| Trigger | Threshold | Status |
|---------|-----------|--------|
| Max Drawdown | > $130.70 | Monitoring |
| Structural Deviation | Wrong gate | Monitoring |
| AvgPnL Negative | Over 20+ trades | Monitoring |

---

## LOCKED PARAMETERS (Phase 1)

```
STRATEGY:     RULEV3+ Phase 1
ZONE_MODE:    CORE-only (T3)
CORE:         3:00-3:29 (180-209s elapsed)
THRESHOLD:    >= 0.64
SAFETY CAP:   <= 0.72
SPREAD_MAX:   <= 0.02
ALPHA_GATE:   REMOVED
MAX TRADES:   1 per session
POSITION:     $5.00
```

---

## Go-Live Protocol (After Phase 1 Validation)

1. [ ] Collect 50 paper trades
2. [ ] Validate metrics match backtest (~72% WR, ~$0.33 AvgPnL)
3. [ ] No kill rules triggered
4. [ ] Switch TRADING_MODE=real, EXECUTION_ENABLED=true
5. [ ] Start with MAX_LIVE_TRADES_PER_RUN=1
6. [ ] Monitor first 10 real trades
7. [ ] Scale up after validation

---

## Phase 2 (Future)

- [ ] Build p_model from historical calibration
- [ ] Reintroduce alpha = p_model - ask
- [ ] Create PHASE2_LOCKED.md

---

**Config Signature:** `PHASE1-SPREAD-0.02-EDGE-0.64-CAP-0.72-CORE-ONLY`
