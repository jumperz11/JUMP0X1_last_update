# RULEV3+ GO-LIVE CHECKLIST

## Strategy Validation
- [x] T3-only mode validated (T1 disabled)
- [x] Time window 3:00-3:29 (CORE) validated
- [x] Time window 5:00-5:59 (RECOVERY) validated
- [x] Edge threshold >= 0.64 validated
- [x] Safety cap < 0.72 validated
- [x] Backtest: 1157 trades, 71.91% WR, +$48.24 PnL
- [x] Bootstrap CI: P(EV > 0) = 100%
- [x] Walk-forward validation passed
- [x] Both directions (Up/Down) profitable

## Bot Code
- [x] `strategy_rulev3_plus.py` - Strategy definition
- [x] `bot_rulev3_plus.py` - Main bot logic
- [x] `test_bot.py` - Test scenarios
- [x] `evaluate_tick()` function working
- [x] Zone detection working (WAITING/CORE/DEAD/RECOVERY)
- [ ] Polymarket API integration
- [ ] WebSocket connection handler
- [ ] Order execution logic
- [ ] Error handling & retries

## UI Dashboard
- [ ] Terminal UI (TUI) built
- [ ] Live prices panel
- [ ] Positions panel
- [ ] Performance stats panel
- [ ] Order history panel
- [ ] Skipped opportunities panel
- [ ] Live logs panel
- [ ] Config display panel

## Risk Management
- [ ] Max drawdown limit: $100
- [ ] Max consecutive losses: 10
- [ ] Min win rate threshold: 55% (over 100 trades)
- [ ] Position sizing: $10-25 per trade (Phase 1)
- [ ] Session skip on API errors
- [ ] Auto-pause on guardrail breach

## Infrastructure
- [ ] Stable internet connection
- [ ] Polymarket API keys configured
- [ ] Wallet funded
- [ ] Logging to file enabled
- [ ] Backup/recovery plan

## Pre-Launch
- [ ] Paper trade for 24 hours
- [ ] Verify order fills match expected
- [ ] Check latency (< 1 second)
- [ ] Confirm settlement tracking
- [ ] Test guardrail triggers

## Go-Live Protocol
1. [ ] Start with minimum size ($10/trade)
2. [ ] Monitor first 10 trades manually
3. [ ] Check execution vs backtest assumptions
4. [ ] Scale up after 100+ successful trades
5. [ ] Weekly performance review

---

## LOCKED PARAMETERS

```
STRATEGY:     RULEV3+
MODE:         T3-only
CORE:         3:00-3:29 (180-209s elapsed)
RECOVERY:     5:00-5:59 (300-359s elapsed)
THRESHOLD:    >= 0.64
SAFETY CAP:   < 0.72
MAX TRADES:   1 per session
```

## GUARDRAILS

| Condition | Action |
|-----------|--------|
| Drawdown > $100 | PAUSE |
| 10 consecutive losses | PAUSE |
| WR < 55% (100 trades) | PAUSE |
| EV < -0.02 (200 trades) | PAUSE |
| API error | Skip session |
| Slippage > 2 ticks | Alert |

## CONTACTS

- Strategy: RULEV3+ v1.0
- Backtest Period: Nov 27 - Dec 20, 2025
- Expected EV: +0.0417/trade
- Expected WR: 71.91%
