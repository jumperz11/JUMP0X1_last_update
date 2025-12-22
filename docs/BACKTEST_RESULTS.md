# Backtest Results

**Date:** 2025-12-20
**Dataset:** 8,340 markets (23 days of tick data)
**Strategy:** balanced_arb

## Summary

| Metric | Value |
|--------|-------|
| Markets processed | 8,340 |
| Markets with trades | 8,286 (99.4%) |
| Total trades | 304,061 |
| Win rate | **98.5%** |
| Total PnL | **$35,584.85** |
| Avg PnL per market | $4.60 |

## Configuration Used

```env
PM_TAU0_SECONDS=600        # 10 min entry window (data starts at 10.8min left)
PM_STOP_NEW_SECONDS=30     # Exit 30 sec before settlement
PM_SPREAD_THRESHOLD=1.02   # Max combined ask price
PM_MAX_ONE_SIDED=6         # Max imbalance
PM_BASE_QTY=5              # 5 shares per trade
PM_MIN_PRICE=0.40          # Min bid price
PM_MAX_PRICE=0.55          # Max bid price
PM_PRICE_BUFFER=0.02       # Bid below mid
```

## Spread Threshold Analysis

| Threshold | Trades | PnL | Win Rate |
|-----------|--------|-----|----------|
| 0.98 | 1 | -$2.00 | 0% |
| 1.00 | 4 | -$4.50 | 25% |
| 1.01 | 203 | $26.65 | 58% |
| **1.02** | **304,061** | **$35,584** | **98.5%** |
| 1.10 | 331,302 | $38,114 | 100% |

**Key Finding:** 0.98 threshold is too tight - spreads rarely that good. 1.02 is optimal.

## Trade Constraints

- Min 5 seconds between trades
- Max 20 trades per side per market (100 shares each side)
- Only trade within entry window (first 10 min of 15 min market)
- Stop trading last 30 seconds

## Sample Market Results

```
btc-updown-15m-1764261900: 40 trades, up=100 down=100, up_won=true,  pnl=$4.98
btc-updown-15m-1764262800: 40 trades, up=100 down=100, up_won=true,  pnl=$5.08
btc-updown-15m-1764263700: 40 trades, up=100 down=100, up_won=false, pnl=$5.23
btc-updown-15m-1764264600: 40 trades, up=100 down=100, up_won=true,  pnl=$5.40
btc-updown-15m-1764265500: 40 trades, up=100 down=100, up_won=true,  pnl=$4.00
```

**Note:** Profit regardless of outcome because balanced positions always settle to $1 total.

## Data Limitations

- Tick data starts ~4.2 minutes into each market (10.8 min left)
- True 2-minute entry window not captured in historical data
- Backtest assumes limit orders fill at our price (optimistic)
- Real trading will have partial fills and slippage

## Next Steps

1. Run live paper trading with PM_SPREAD_THRESHOLD=1.02
2. Monitor actual fill rates vs backtest assumptions
3. Tune entry window based on live data availability
