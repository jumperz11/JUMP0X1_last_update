# SETUP.md - Installation and Environment Setup

## Prerequisites

### 1. Rust Toolchain

```bash
# Install Rust (if not already installed)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Verify installation
rustc --version  # Should be 1.70+
cargo --version
```

### 2. System Dependencies

**macOS:**
```bash
# Xcode command line tools (for compilation)
xcode-select --install
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install build-essential pkg-config libssl-dev
```

---

## Project Setup

### 1. Clone/Navigate to Project

```bash
cd /Users/jumperz/PROJES/JUMP01X
```

### 2. Verify Structure

```bash
ls -la
# Should see:
# - PK8_PH/          (Rust framework)
# - markets_paper/   (Tick data - 14GB)
# - README.md, STRATEGY.md, etc.
```

### 3. Build the Project

```bash
cd PK8_PH
cargo build --release
```

First build takes 2-5 minutes (compiles all dependencies).

---

## Configuration

### 1. Environment File

```bash
# The .env file should already exist
cat .env
```

### 2. Key Settings Explained

```bash
# ===================
# LOGGING
# ===================
RUST_LOG=info                          # Log level (debug, info, warn, error)
PM_LOG_TO_FILE=1                       # Write logs to file
PM_LOG_FILE=logs/live_console.log      # Log file path
PM_JSONL_LOG_FILE=logs/events.jsonl    # Structured event log

# ===================
# STRATEGY
# ===================
PM_STRATEGY=balanced_arb               # Our strategy (change from noop)

# ===================
# MARKETS
# ===================
PM_WATCHLIST=BTC:15m,ETH:15m,SOL:15m,XRP:15m   # Markets to watch
PM_TRADELIST=BTC:15m,ETH:15m,SOL:15m,XRP:15m   # Markets to trade

# ===================
# SAFETY (KEEP THESE ON FOR TESTING)
# ===================
PM_PAPER_TRADING=1                     # Paper mode - NO real orders
PM_DRY_RUN=1                           # Extra safety layer
PM_TRADE_ENABLED=1                     # Enable trade logic

# ===================
# PAPER TRADING SIMULATION
# ===================
PM_PAPER_STARTING_CASH=10000           # Starting balance for paper
PM_PAPER_POST_LATENCY_MS=50            # Simulated order latency
PM_PAPER_CANCEL_REQ_LATENCY_MS=50      # Simulated cancel latency
PM_PAPER_FLOW_BASE=5                   # Base fill rate
PM_PAPER_SEED=1                        # RNG seed for reproducibility

# ===================
# EXECUTION
# ===================
PM_WARMUP_SECONDS=5.0                  # Wait before trading on startup
PM_MIN_REQUOTE_SECONDS=1.0             # Min time between requotes
PM_REQUOTE_MIN_TICKS=3                 # Min price change to requote
PM_MIN_ORDER_NOTIONAL=1.0              # Minimum order size ($)
PM_CASH_UTILIZATION=1                  # Use 100% of available cash

# ===================
# STRATEGY PARAMETERS (for balanced_arb)
# ===================
PM_TAU0_SECONDS=120                    # Entry window (first 2 min)
PM_STOP_NEW_SECONDS=30                 # Exit window (last 30 sec)
PM_SPREAD_THRESHOLD=0.98               # Max combined ask
PM_MAX_ONE_SIDED=6                     # Balance limit

# ===================
# LIVE TRADING (DO NOT SET UNTIL READY)
# ===================
# PM_PRIVATE_KEY=0xYOUR_KEY            # Wallet private key
# PM_SIGNATURE_TYPE=1                   # Signature type
# PM_LIVE_WALLET_ADDRESS=0xYOUR_ADDR   # Wallet address
```

### 3. Update Strategy

Edit `.env` to use our strategy:

```bash
# Change from:
PM_STRATEGY=noop

# To:
PM_STRATEGY=balanced_arb
```

---

## Running

### Paper Trading (Safe)

```bash
cd PK8_PH
cargo run --bin live_console
```

You'll see the terminal UI:
- Markets panel (BTC, ETH, SOL, XRP quotes)
- Portfolio panel (positions, P&L)
- Logs panel (trade decisions)

**Controls:**
- `q` - Quit
- Arrow keys - Navigate
- Tab - Switch panels

### Backtesting

```bash
# Run backtest on historical data
cargo run --bin backtest -- --base ../markets_paper

# Limit to specific number of markets
cargo run --bin backtest -- --base ../markets_paper --limit-markets 100

# With summary output
cargo run --bin backtest -- --base ../markets_paper --summary-json
```

### Optimization

```bash
# Monte Carlo parameter sweep
cargo run --bin optimizer -- \
  --trials 50 \
  --base ../markets_paper \
  --limit-markets 500

# With custom ranges
cargo run --bin optimizer -- \
  --trials 100 \
  --range PM_TAU0_SECONDS=60:180 \
  --range PM_MAX_ONE_SIDED=4:8
```

---

## Going Live (When Ready)

### 1. Create Polymarket Account
- Go to polymarket.com
- Connect wallet
- Fund with USDC on Polygon

### 2. Export Private Key
- Export from your wallet (MetaMask, etc.)
- **NEVER share this key**
- **NEVER commit to git**

### 3. Update .env

```bash
# Disable paper trading
PM_PAPER_TRADING=0
PM_DRY_RUN=0

# Add credentials
PM_PRIVATE_KEY=0xYOUR_ACTUAL_PRIVATE_KEY
PM_LIVE_WALLET_ADDRESS=0xYOUR_WALLET_ADDRESS
PM_SIGNATURE_TYPE=1
```

### 4. Start Small

```bash
# Set low cash utilization first
PM_CASH_UTILIZATION=0.10  # Only use 10% of balance

# Monitor closely
cargo run --bin live_console
```

---

## Troubleshooting

### Build Errors

**"linker not found"**
```bash
# macOS
xcode-select --install

# Linux
sudo apt install build-essential
```

**"openssl not found"**
```bash
# macOS
brew install openssl

# Linux
sudo apt install libssl-dev
```

### Runtime Errors

**"missing PM_PRIVATE_KEY"**
- This only matters for live trading
- Paper trading works without credentials

**"strategy not found"**
- Check PM_STRATEGY in .env matches a valid strategy
- Valid: `noop`, `balanced_arb`

**"connection refused"**
- Check internet connection
- Polymarket API might be down

### Performance Issues

**Slow builds**
```bash
# Use release mode
cargo build --release
cargo run --release --bin live_console
```

**High CPU usage**
- Normal during active trading
- Check PM_MIN_REQUOTE_SECONDS isn't too low

---

## File Locations

| Path | Purpose |
|------|---------|
| `PK8_PH/.env` | Configuration |
| `PK8_PH/logs/` | Log files |
| `markets_paper/` | Historical tick data |
| `PK8_PH/target/release/` | Compiled binaries |

---

## Security Checklist

- [ ] Private key NOT in git (check .gitignore)
- [ ] Paper trading enabled for testing
- [ ] Cash utilization set low for live start
- [ ] Logs not containing sensitive data
- [ ] .env permissions restricted (`chmod 600 .env`)
