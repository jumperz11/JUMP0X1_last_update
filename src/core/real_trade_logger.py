#!/usr/bin/env python3
"""
REAL TRADE LOGGER
=================
Dedicated logging for REAL trades only.
Paper/simulation NEVER writes here.

Log file: logs/real_trading.log
All lines prefixed with [REAL]

Lifecycle order:
  SIGNAL → SUBMIT → FILLED → SETTLED → (optional) KILL
"""

import os
import json
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Optional
from pathlib import Path


class RealTradeLogger:
    """
    Dedicated logger for REAL trades only.
    Writes to logs/real_trading.log with [REAL] prefix.
    """

    def __init__(self, log_dir: str = "logs", enabled: bool = False):
        """
        Args:
            log_dir: Directory for log files
            enabled: If False, all logging is silently skipped (paper mode)
        """
        self.enabled = enabled
        self.log_dir = Path(log_dir)
        self.log_file: Optional[Path] = None
        self._file_handle = None

        if self.enabled:
            self._init_log_file()

    def _init_log_file(self):
        """Initialize the real trading log file."""
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / "real_trading.log"

    def _write(self, category: str, data: dict):
        """
        Write a log entry. Only writes if enabled (real mode).

        Args:
            category: Log category (SIGNAL, SUBMIT, FILLED, etc.)
            data: Dictionary of key=value pairs to log
        """
        if not self.enabled:
            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        # Build log line
        lines = [f"[REAL][{category}]"]
        lines.append(f"time={timestamp}")

        for key, value in data.items():
            if isinstance(value, float):
                lines.append(f"{key}={value:.6f}")
            elif isinstance(value, bool):
                lines.append(f"{key}={str(value).lower()}")
            else:
                lines.append(f"{key}={value}")

        log_entry = "\n".join(lines) + "\n"

        # Write to file (flush immediately for crash safety)
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)
            f.write("\n")  # Blank line between entries
            f.flush()  # Force write to disk - real money logs must survive crashes

    # =========================================================================
    # LIFECYCLE LOGS
    # =========================================================================

    def log_start(self, balance: float, config: dict):
        """Log trading session start."""
        self._write("START", {
            "balance": balance,
            "config_snapshot": json.dumps(config, default=str),
        })

    def log_stop(self, reason: str, final_balance: float, final_pnl: float):
        """
        Log trading session stop.

        Args:
            reason: manual | kill_switch | error
            final_balance: Ending balance
            final_pnl: Total PnL for session
        """
        self._write("STOP", {
            "reason": reason,
            "final_balance": final_balance,
            "final_pnl": final_pnl,
        })

    def log_signal(
        self,
        market_id: str,
        question: str,
        zone: str,
        edge: float,
        direction: str,
        best_bid: float,
        best_ask: float,
        spread: float
    ):
        """Log signal detection (Step A)."""
        self._write("SIGNAL", {
            "market_id": market_id,
            "question": question,
            "zone": zone,
            "edge": edge,
            "direction": direction,
            "best_bid": best_bid,
            "best_ask": best_ask,
            "spread": spread,
        })

    def log_submit(
        self,
        order_id: str,
        side: str,
        limit_price: float,
        shares: float,
        max_loss_estimate: float
    ):
        """Log order submission (Step B)."""
        self._write("SUBMIT", {
            "order_id": order_id,
            "side": side,
            "limit_price": limit_price,
            "shares": shares,
            "max_loss_estimate": max_loss_estimate,
        })

    def log_filled(
        self,
        order_id: str,
        fill_price: float,
        fill_time: str,
        slippage_bps: float,
        degraded: bool
    ):
        """Log order fill (Step C)."""
        self._write("FILLED", {
            "order_id": order_id,
            "fill_price": fill_price,
            "fill_time": fill_time,
            "slippage_bps": slippage_bps,
            "degraded": degraded,
        })

    def log_settled(
        self,
        order_id: str,
        market_id: str,
        won: bool,
        trade_pnl: float,
        cumulative_pnl: float,
        consecutive_losses: int
    ):
        """Log trade settlement (Step D)."""
        self._write("SETTLED", {
            "order_id": order_id,
            "market_id": market_id,
            "won": won,
            "trade_pnl": trade_pnl,
            "cumulative_pnl": cumulative_pnl,
            "consecutive_losses": consecutive_losses,
        })

    def log_kill(self, reason: str, value: str):
        """
        Log killswitch activation (Step E - optional).

        Args:
            reason: consec_losses | pnl_floor | degraded_fills
            value: The value that triggered the kill
        """
        self._write("KILL", {
            "reason": reason,
            "value": value,
        })


# =============================================================================
# SINGLETON INSTANCE
# =============================================================================

_real_logger: Optional[RealTradeLogger] = None


def init_real_logger(log_dir: str = "logs", enabled: bool = False) -> RealTradeLogger:
    """
    Initialize the real trade logger singleton.

    Args:
        log_dir: Directory for log files
        enabled: True ONLY if TRADING_MODE == real

    Returns:
        RealTradeLogger instance
    """
    global _real_logger
    _real_logger = RealTradeLogger(log_dir=log_dir, enabled=enabled)
    return _real_logger


def get_real_logger() -> Optional[RealTradeLogger]:
    """Get the real trade logger singleton."""
    return _real_logger


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def real_log_start(balance: float, config: dict):
    """Log session start (only if real mode)."""
    if _real_logger:
        _real_logger.log_start(balance, config)


def real_log_stop(reason: str, final_balance: float, final_pnl: float):
    """Log session stop (only if real mode)."""
    if _real_logger:
        _real_logger.log_stop(reason, final_balance, final_pnl)


def real_log_signal(
    market_id: str,
    question: str,
    zone: str,
    edge: float,
    direction: str,
    best_bid: float,
    best_ask: float,
    spread: float
):
    """Log signal (only if real mode)."""
    if _real_logger:
        _real_logger.log_signal(
            market_id, question, zone, edge, direction,
            best_bid, best_ask, spread
        )


def real_log_submit(
    order_id: str,
    side: str,
    limit_price: float,
    shares: float,
    max_loss_estimate: float
):
    """Log order submit (only if real mode)."""
    if _real_logger:
        _real_logger.log_submit(order_id, side, limit_price, shares, max_loss_estimate)


def real_log_filled(
    order_id: str,
    fill_price: float,
    fill_time: str,
    slippage_bps: float,
    degraded: bool
):
    """Log fill (only if real mode)."""
    if _real_logger:
        _real_logger.log_filled(order_id, fill_price, fill_time, slippage_bps, degraded)


def real_log_settled(
    order_id: str,
    market_id: str,
    won: bool,
    trade_pnl: float,
    cumulative_pnl: float,
    consecutive_losses: int
):
    """Log settlement (only if real mode)."""
    if _real_logger:
        _real_logger.log_settled(
            order_id, market_id, won, trade_pnl,
            cumulative_pnl, consecutive_losses
        )


def real_log_kill(reason: str, value: str):
    """Log killswitch (only if real mode)."""
    if _real_logger:
        _real_logger.log_kill(reason, value)
