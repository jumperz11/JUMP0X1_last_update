<!-- MIND MEMORY - Append as you work. Write naturally.
Keywords: decided, problem, learned, tried, fixed, blocked, KEY, important
Wikilinks: Use [[MEMORY#L123]] to link to specific lines (Obsidian-compatible)
Sync: To sync across devices, add .mind/ folder to your Obsidian vault -->

# JUMP01X

## Project State
- Goal:
- Stack: (add your stack)
- Blocked: None

## Gotchas
<!-- Project-specific gotchas -->

---

## Session Log

## 2025-12-20

(Start writing here)

<!-- End session with: ## DATE | summary of what happened | mood: X -->
---

decided: GABAGOOL V3 - Polymarket binary options arbitrage bot project. User acquired Rust framework (PK8_PH/) + 23 days tick data (8,340 markets in markets_paper/). Framework has: WebSocket feeds, paper trading sim, order execution, optimizer shell. MISSING: actual strategy code (only noop exists), backtest binary. Previous TEST1: 84% win rate but lost money due to one-sided position accumulation. Key insight: early balanced entries (4+4, 5+5 shares) correlate with wins.
decided: PROJECT: JUMP01X (Polymarket arbitrage bot). USER: JUMPERZ (UX background, learning to code). ANALYST: Claude Opus (separate). SOURCE: InsideTrader (17yr dev, gave framework + data).
learned: CRITICAL STRATEGY RULES: 1) MAX_ONE_SIDED=6 (never >6 shares one side without balance), 2) Edge decay = first 2 minutes only, 3) Don't snipe 0.99 = never trade last 30 seconds, 4) Balanced positions = profit, Unbalanced = death, 5) Spread threshold: up_ask + down_ask < $0.98
learned: TEST1 FAILURE ANALYSIS: 84% win rate but LOST money. Problem: one-sided accumulation (10+0 shares). Winning trades had balanced early entries (4+4, 5+5). Fix: prioritize lagging side, stop if imbalanced.
learned: INSIDETRADER INTEL: Binance klines 98% match Chainlink oracle (settlement source). 500ms taker speedbump killed latency arb. Need PREDICTIVE edge not speed. His balanced positions = profit, tracked users' unbalanced = losses.
fixed: Phase 1 COMPLETE: Created all documentation files - README.md (overview), STRATEGY.md (balanced arb logic), SETUP.md (installation), KNOWLEDGE.md (InsideTrader intel), ARCHITECTURE.md (framework internals). Ready for Phase 2: strategy implementation.
learned: TEST1 ENTRY INSIGHT: 0.46-0.48 price range worked well for getting fills. Apply this to balanced_arb - don't chase worse prices.
fixed: Phase 2 COMPLETE: Created balanced_arb.rs strategy with all TEST1 lessons applied. Registered in mod.rs, configured in .env. Rust not installed on system - user needs to install to verify build.
learned: Strategy debugging: tracing logs don't appear in TUI log file - modified set_decision() in live_console.rs to log all strategy decisions via FILE_LOG_TX channel. Now can see why="entry_closed" when outside the 2-minute entry window.
decided: Backtester built and tested on 8340 markets (23 days). Results: spread_threshold=1.02 yields 304K trades, $35K profit, 98.5% win rate. Changed live config from 0.98 to 1.02 spread threshold. The 0.98 was too tight - only 1 trade in 23 days of historical data.
learned: Backtest analysis complete - 98.5% win rate is misleading: balanced positions (53%) have 99% win rate, one-sided (47%) only 54%. ALL one-sided are UP-heavy, suggesting DOWN fills are harder to get. No partial fills/queue simulation means real results will be worse.
learned: Telegram chat analysis complete - Key insights: 1) Gabagool always ends with perfect variance (+/- X shares), suggesting privileged access or insider edge 2) Kizo Azuki noted impossible fill precision 3) InsideTrader says strategy is mathematically doomed without edge 4) Fill problem is universal - everyone struggles with DOWN fills 5) Speed/latency critical 6) Felix Poirier confirms robust backtesting is waste of time
learned: CRITICAL ALPHA from Telegram: 1) Binance leads Chainlink by ~150ms - directional edge, 2) 500ms taker speed bump killed taker strategies - Gabagool survives with MAKER orders only, 3) 15m markets use Chainlink, 1h markets use Binance candles for resolution, 4) dhanush was profitable until speed bump, 5) Sub-200ms infrastructure needed
decided: MAJOR PIVOT: Abandoning balanced arb (impossible fills). New strategy: DIRECTIONAL trading with predictive signals. Goal: Find which price source LEADS Chainlink to predict settlement. InsideTrader claims 5-9% edge from data testing. Build multi-source price recorder to find lead/lag relationships.
fixed: Built correlation_analyzer tool: records prices at checkpoints (T+0, T+30s, T+60s, T+2m, T+5m, T+10m, T+13m, T+14m, T+14m30s, T+14m59s) from 4 sources (binance_spot, binance_futures, coinbase, bybit). Run --live to collect, --analyze to see correlation % by checkpoint.
fixed: Built multi_signal_recorder with 14 sources: Price (binance_spot, binance_futures, coinbase, bybit, kraken, okx, chainlink_rtds, pyth) + Sentiment (funding_rate, open_interest, long_short_ratio, liquidations, orderbook_imbalance, cvd, fear_greed). Records at 17 checkpoints per 15m session.

<!-- Promoted from SESSION.md on 2025-12-20 -->
learned: Phase 4 critical: Build correlation analyzer comparing Binance/Coinbase/Bybit price direction at various timestamps (T+0, T+60s, T+14m, T+14m59s) against actual Polymarket 15m settlement winner. Goal: find when signal correlation peaks.

fixed: multi_signal_recorder v2.0 built and running with clean output - no more Connected spam, shows session headers and checkpoint data
fixed: multi_signal_recorder v3.0 complete: 14/14 sources working, real-time trading terminal UI with colors, session history, running accuracy tracking. Fixed Chainlink RTDS (wss://ws-live-data.polymarket.com) and Pyth Network connections.
fixed: Fixed UI spamming by using cursor_home() instead of clear_screen() for within-session updates. Only clears screen on new session, otherwise just moves cursor to home and overwrites.
fixed: Fixed 3 UI issues: 1) FLAT epsilon for zero delta, 2) Baseline vs Exchange direction labels, 3) Lead-lag only shows on real moves
fixed: Fixed CONSENSUS to show "DOWN (0% UP)" format, and checkpoints now show ? for missed, (session ending) when done
learned: Lead-lag analyzer bug caught and fixed. Key learnings: 1) $0.50 threshold was noise, need $17.60 (0.02%) for real events. 2) Tick resolution ~130ms means cannot claim sub-100ms leads. 3) After proper clustering (3s cooldown), only ~12 real events in 3hrs, not thousands. 4) Speed is NOT the edge - structural oracle staleness (seconds) is. 5) Coinbase may lead but MEDIUM confidence with small sample. 6) Keep recording until 50-100 events before drawing conclusions. DECISION: Freeze analyzer v2.0, focus on dislocation persistence not ms-latency.
learned: Lead-lag analyzer v2.0: Event ordering, not fake ms precision. With ~130ms tick resolution, cannot claim sub-100ms leads. Key insight: Coinbase moves first ~75% of events within resolution window.
decided: Rule v1 for directional trading: Entry T+30s-T+60s, OB_slope >= +0.5, dislocation >= $25 persisting 60s+, price 48-52c. Edge is STRUCTURAL (classification), not SPEED (milliseconds).
learned: Chainlink behavior: 840ms median tick gap, frozen for seconds while exchanges move $30+. Settlement oracle lags by design. Don't race it - watch for persistent dislocation.
learned: OB slope predicts better than raw OB: OB at T+0 is noise, OB CHANGE from T+0 to T+60s is the signal. Example: OB started -0.83, became +0.04, slope +0.87 correctly predicted UP.
learned: CVD lags at session start: Wrong at T+60s (-0.29), correct at T+10m (+3.47). Use CVD for late confirmation, not early prediction. OB slope is the early signal.
learned: Codebase audit complete: Bot exists but it's ARBITRAGE (balanced_arb), not DIRECTIONAL. Has: CLOB execution, config system, paper broker, position balance. Missing: directional signal integration, OB slope in trade path, profit-lock, kill switch, proper EV math.
fixed: Implemented versioned run directories with LOG_DIR env var. Run dir: logs/runs/20251221_0323_V1. Orders.jsonl wired with sanity checks (ack_ms >= 0, fill_ms >= 0, FILL requires avg_fill_q). Schema adds run_id and schema_version to both sessions.jsonl and orders.jsonl. Backward compat verified - old analyzer parses 29 sessions correctly.
fixed: orders.jsonl VALIDATED: Added telemetry to paper broker (SUBMIT/ACK/CANCEL), startup print shows LOG_DIR + writer status, VALIDATION_ORDER flag triggers test lifecycle. V2 run confirmed: ["SUBMIT","ACK","CANCEL"] with run_id + schema_version.
fixed: Completed multi_signal_recorder updates: startup print with LOG_DIR/RUN_ID, config.json with ALL thresholds (move_threshold_pct, move_window_ms, cooldown_ms, dislocation_*, epsilon_flat_pct, staleness_ms, outlier_pct, checkpoints), RUN_START on startup, RUN_END on Ctrl+C with reason='ctrl_c'. Validated with test run 20251221_TEST_V1.
fixed: Completed all 4 lead engineer tasks: (1) multi_signal_recorder with RUN_START/RUN_END/config.json, (2) session_outcome_analyzer CLI showing signal accuracy by checkpoint, (3) paper_baseline strategy trading after T+60s when edge >= 55%, (4) rule_v1 strategy with 3-tier entry logic based on session_outcome_analyzer insights (T+45s OB 0.6+, T+60s edge 0.55+, T+3m edge 0.52+). Available via PM_STRATEGY=paper_baseline or PM_STRATEGY=rule_v1.
learned: Lead-lag analyzer command: /Users/jumperz/PROJES/JUMP01X/PK8_PH/target/release/lead_lag_analyzer /Users/jumperz/PROJES/JUMP01X/logs/price_ticks_*.jsonl - shows source ranking from leader to lagger
learned: BUG FIX: PaperBroker FILL events not logging to JSONL. Console showed [paper][fill] but orders_*.jsonl had FILL:0. Fix: Added emit_order_event() call in apply_paper_fill() function (paper.rs:913-967) with FILL/PARTIAL_FILL action types. Also added strategy_id field to PaperOrder struct for A/B routing.
fixed: Created STATE.md in docs/ - comprehensive project status report with edge analysis, price bucket EV, and next actions. Key finding: rule_v1 outperforming (71% WR, +$2.42), cheap fills <=0.54 are +$0.33/trade, expensive >=0.64 are -$0.40/trade.
learned: Price gate update: New data (n=51 fills) shows break-even at $0.58, not $0.64. Below $0.58: 88% WR, +$0.35/trade. At $0.58+: 50% WR, -$0.15/trade. Next run should skip best_ask >= 0.58.
fixed: Added strategy indicator to paper.rs console logs - now shows [paper_baseline] or [rule_v1] instead of generic [paper]
decided: Added price gate rule to rule_v1: skip if best_ask >= $0.58. Data showed 80% win rate below vs 54% above threshold
decided: Built settlement verifier: verify_settlements binary. Converts assumed wins to ground truth. First real test: rule_v1 62.5% win rate, +$0.035 EV vs paper_baseline 60.9%, +$0.022 EV
decided: Built replay_realism binary. Key finding: EV stays positive at (500ms, +2 ticks) but dies at +3 ticks. Latency 250-1000ms doesn't kill edge; slippage does.
decided: Added live trading caps: KILL_SWITCH file check, MAX_TRADES/NOTIONAL/POSITION caps. Live path now has same rails as paper.

<!-- Promoted from SESSION.md on 2025-12-22 -->
learned: Starting settlement verifier implementation in Rust - post-hoc audit infrastructure

decided: LIVE MODE ENABLED: PM_STRATEGY=rule_v1, PM_DRY_RUN=0, PM_PAPER_TRADING=0. Wallet has $9.97 USDC + 19.9 MATIC.
fixed: Added USDC balance pre-check to live trading startup - fails fast if balance < max_worst_total_usd
fixed: Added observation mode (PM_ARMED=0): console shows data + "Would trade" logs but doesn't place orders
learned: CORRECTION: rule_v1 is DIRECTIONAL strategy (picks UP or DOWN), NOT balanced arb. Was incorrectly explaining it as hedging both sides. Updated .env comments to reflect this.
decided: Raised price_gate from $0.58 to $0.60. Backtest (n=24) showed $0.58 gate = -$0.46 loss, $0.60 = breakeven. More volume, same risk profile.
decided: Shifted entry timing 15s earlier: Tier1 T+30s (was T+45s), Tier2 T+45s (was T+60s). Reason: market decides early, prices move before old T+45s window.
decided: Implemented balanced tiered approach: Tier0 T+0-15s (58%/$0.55), Tier1 T+15-45s (60%/$0.58), Tier2 T+45s-3m (55%/$0.62), Tier3 T+3m+ (52%/$0.65). Per-tier gates based on backtest: strict early (flip risk), loose late (market decided).
decided: User decision: revert to locked config (Tier1 T+30s @64%, Tier2 T+45s @55%, Tier3 T+3m @52%, gate $0.58). Add shadow logging for balanced approach - no execution, just observation.
decided: RULE_V1.1 update: Removed $0.58 hard price gate (data showed it blocked 97% winners causing negative P&L). Changed Tier 1 threshold from 64% to 58%. Key insight: LATE > CHEAP - optimize for decision completion not cheap entries. Price now logged only, not blocked.
learned: V1.2 backtest results: Skipping T2 turned P&L from -$4.66 to +$8.57. T3 now catches trades that T2 was grabbing (838 vs 12). Early OR Late only = profitable. Middle = noise.