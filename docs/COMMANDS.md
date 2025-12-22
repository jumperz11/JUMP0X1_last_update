# JUMP01X Commands Reference

Quick reference for all runner scripts and commands.

---

## Runner Scripts (All Terminals)

All scripts are in `PK8_PH/scripts/`. Run from `PK8_PH/` directory.

### Run Everything

**Git Bash / Mac / Linux:**
```bash
./scripts/run_all.sh
```

**PowerShell:**
```powershell
bash scripts/run_all.sh
```

- Starts both A/B test and collector
- Creates timestamped directories
- Uses tmux split if available, otherwise background mode

### Run A/B Test Only

**Git Bash / Mac / Linux:**
```bash
./scripts/run_ab.sh
```

**PowerShell:**
```powershell
cd C:\Users\Mega-PC\Desktop\JUMP0X1\PK8_PH
$env:PATH = "C:\msys64\mingw64\bin;$env:USERPROFILE\.cargo\bin;$env:PATH"
$env:LOG_DIR = "logs\runs\$(Get-Date -Format 'yyyyMMdd_HHmm')_AB"
$env:AB_TEST = "1"
$env:ENABLE_ORDERS_JSONL = "1"
$env:MAX_TRADES_PER_SESSION = "1"
New-Item -ItemType Directory -Force -Path $env:LOG_DIR
.\target\release\live_console.exe
```

**CMD:**
```cmd
cd C:\Users\Mega-PC\Desktop\JUMP0X1\PK8_PH
set PATH=C:\msys64\mingw64\bin;%USERPROFILE%\.cargo\bin;%PATH%
set LOG_DIR=logs\runs\%date:~-4%%date:~4,2%%date:~7,2%_AB
set AB_TEST=1
set ENABLE_ORDERS_JSONL=1
set MAX_TRADES_PER_SESSION=1
mkdir %LOG_DIR% 2>nul
target\release\live_console.exe
```

- Runs `live_console` with paper_baseline vs rule_v1
- Creates `YYYYMMDD_HHMM_AB` directory
- Updates `LATEST_AB` symlink

### Run Collector Only

**Git Bash / Mac / Linux:**
```bash
./scripts/run_collector.sh
```

**PowerShell:**
```powershell
cd C:\Users\Mega-PC\Desktop\JUMP0X1\PK8_PH
$env:PATH = "C:\msys64\mingw64\bin;$env:USERPROFILE\.cargo\bin;$env:PATH"
$env:LOG_DIR = "logs\runs\$(Get-Date -Format 'yyyyMMdd_HHmm')_COLLECT"
New-Item -ItemType Directory -Force -Path $env:LOG_DIR
.\target\release\multi_signal_recorder.exe
```

**CMD:**
```cmd
cd C:\Users\Mega-PC\Desktop\JUMP0X1\PK8_PH
set PATH=C:\msys64\mingw64\bin;%USERPROFILE%\.cargo\bin;%PATH%
set LOG_DIR=logs\runs\collect_run
mkdir %LOG_DIR% 2>nul
target\release\multi_signal_recorder.exe
```

- Runs `multi_signal_recorder` for price/signal data
- Creates `YYYYMMDD_HHMM_COLLECT` directory
- Updates `LATEST_COLLECT` symlink

### Check Status

**Git Bash / Mac / Linux:**
```bash
./scripts/check_status.sh
```

**PowerShell:**
```powershell
Get-Content logs\runs\LATEST_AB\orders_*.jsonl | Select-String '"action":"FILL"' | Measure-Object
```

**CMD:**
```cmd
findstr /c:"\"action\":\"FILL\"" logs\runs\LATEST_AB\orders_*.jsonl | find /c /v ""
```

- Shows fill counts for both strategies
- Shows rule_v1 W/L and P&L

---

## Manual Commands

### Quick Fill Count

**Git Bash / Mac / Linux:**
```bash
grep -c '"action":"FILL"' logs/runs/LATEST_AB/orders_*.jsonl
```

**PowerShell:**
```powershell
(Get-Content logs\runs\LATEST_AB\orders_*.jsonl | Select-String '"action":"FILL"').Count
```

**CMD:**
```cmd
findstr /c:"\"action\":\"FILL\"" logs\runs\LATEST_AB\orders_*.jsonl | find /c /v ""
```

### rule_v1 Performance

**Git Bash / Mac / Linux:**
```bash
cat logs/runs/LATEST_AB/orders_rule_v1.jsonl | jq -s '
  [.[] | select(.action == "FILL")] |
  {
    wins: [.[] | select(.outcome == "up")] | length,
    losses: [.[] | select(.outcome == "down")] | length,
    pnl: [.[] | if .outcome == "up" then (1 - .avg_fill_q) else (0 - .avg_fill_q) end] | add
  }'
```

**PowerShell (requires jq):**
```powershell
Get-Content logs\runs\LATEST_AB\orders_rule_v1.jsonl | jq -s '[.[] | select(.action == \"FILL\")] | {wins: [.[] | select(.outcome == \"up\")] | length, losses: [.[] | select(.outcome == \"down\")] | length}'
```

### Price Bucket Analysis (rule_v1 only)

**Git Bash / Mac / Linux:**
```bash
cat logs/runs/LATEST_AB/orders_rule_v1.jsonl | jq -s '
  [.[] | select(.action == "FILL")] | group_by(
    if .avg_fill_q < 0.54 then "0.50-0.54"
    elif .avg_fill_q < 0.58 then "0.54-0.58"
    elif .avg_fill_q < 0.64 then "0.58-0.64"
    else "0.64+"
    end
  ) | map({
    bucket: .[0] | (if .avg_fill_q < 0.54 then "0.50-0.54" elif .avg_fill_q < 0.58 then "0.54-0.58" elif .avg_fill_q < 0.64 then "0.58-0.64" else "0.64+" end),
    n: length,
    wins: [.[] | select(.outcome == "up")] | length,
    pnl: [.[] | if .outcome == "up" then (1 - .avg_fill_q) else (0 - .avg_fill_q) end] | add
  }) | sort_by(.bucket)'
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LOG_DIR` | required | Output directory for logs |
| `AB_TEST` | 0 | Enable dual-strategy (1=on) |
| `ENABLE_ORDERS_JSONL` | 0 | Log order events (1=on) |
| `MAX_TRADES_PER_SESSION` | unlimited | Trades per 15m session |

### Example Manual Run

**Git Bash / Mac / Linux:**
```bash
LOG_DIR=./logs/runs/MY_TEST AB_TEST=1 ENABLE_ORDERS_JSONL=1 MAX_TRADES_PER_SESSION=1 ./target/release/live_console
```

**PowerShell:**
```powershell
$env:LOG_DIR="logs\runs\MY_TEST"; $env:AB_TEST="1"; $env:ENABLE_ORDERS_JSONL="1"; $env:MAX_TRADES_PER_SESSION="1"; mkdir $env:LOG_DIR -Force; .\target\release\live_console.exe
```

**CMD:**
```cmd
set LOG_DIR=logs\runs\MY_TEST && set AB_TEST=1 && set ENABLE_ORDERS_JSONL=1 && set MAX_TRADES_PER_SESSION=1 && mkdir %LOG_DIR% 2>nul && target\release\live_console.exe
```

---

## Output Files

| File | Contents |
|------|----------|
| `orders_paper_baseline.jsonl` | Baseline strategy events |
| `orders_rule_v1.jsonl` | rule_v1 strategy events |
| `multi_signal_sessions_btc.jsonl` | Collector snapshots |

---

## Symlinks

| Symlink | Points To |
|---------|-----------|
| `logs/runs/LATEST_AB` | Most recent A/B test run |
| `logs/runs/LATEST_COLLECT` | Most recent collector run |

---

## Build

**All Terminals (with cargo in PATH):**

```bash
cargo build --release --bin live_console
cargo build --release --bin multi_signal_recorder
```

Or build all:
```bash
cargo build --release
```

**Windows - ensure PATH includes:**
```
C:\msys64\mingw64\bin
%USERPROFILE%\.cargo\bin
```

---

## Terminal Quick Reference

| Terminal | Best For | Notes |
|----------|----------|-------|
| **Git Bash** | Running .sh scripts directly | Comes with Git for Windows |
| **PowerShell** | Native Windows, scripting | Use `$env:VAR` for env vars |
| **CMD** | Simple commands | Use `set VAR=value` for env vars |
| **Windows Terminal** | All of the above | Select profile for shell type |
| **MSYS2** | Full Linux-like environment | Best compatibility with bash scripts |
