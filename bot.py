#!/usr/bin/env python3
"""Binance Spot signal bot (safe mode only).

Uses only public market data from Binance and prints EMA 9/21 crossover
signals for BTCUSDT. This script does not use API keys, does not access
trading accounts, and does not place any orders.
"""

from __future__ import annotations

from datetime import datetime, timezone

import requests

BASE_URL = "https://data-api.binance.vision"
SYMBOL = "BTCUSDT"
INTERVAL = "5m"
FAST_EMA = 9
SLOW_EMA = 21
KLINE_LIMIT = 200


def fetch_closed_closes() -> list[float]:
    """Fetch recent closed candle close prices from Binance public data API."""
    response = requests.get(
        f"{BASE_URL}/api/v3/klines",
        params={"symbol": SYMBOL, "interval": INTERVAL, "limit": KLINE_LIMIT},
        timeout=20,
    )
    response.raise_for_status()
    candles = response.json()

    if not isinstance(candles, list) or len(candles) <= SLOW_EMA + 1:
        raise RuntimeError("Insufficient candle data received from Binance.")

    # Exclude the latest candle because it may still be open.
    closed_candles = candles[:-1]
    closes = [float(candle[4]) for candle in closed_candles]

    if len(closes) < SLOW_EMA + 2:
        raise RuntimeError("Not enough closed candles to compute EMA crossover signal.")

    return closes


def ema(series: list[float], period: int) -> float:
    """Compute EMA over a full series using standard smoothing."""
    alpha = 2 / (period + 1)
    value = series[0]
    for price in series[1:]:
        value = alpha * price + (1 - alpha) * value
    return value


def crossover_signal(closes: list[float]) -> str:
    """Return BUY, SELL, or WAIT signal from EMA 9/21 crossover."""
    fast_prev = ema(closes[:-1], FAST_EMA)
    slow_prev = ema(closes[:-1], SLOW_EMA)
    fast_now = ema(closes, FAST_EMA)
    slow_now = ema(closes, SLOW_EMA)

    if fast_prev <= slow_prev and fast_now > slow_now:
        return "BUY SIGNAL"
    if fast_prev >= slow_prev and fast_now < slow_now:
        return "SELL SIGNAL"
    return "WAIT"


def main() -> None:
    closes = fetch_closed_closes()
    signal = crossover_signal(closes)

    print("=== BINANCE SPOT SIGNAL BOT (SAFE MODE) ===")
    print("Timestamp (UTC):", datetime.now(timezone.utc).isoformat())
    print("Symbol:", SYMBOL)
    print("Interval:", INTERVAL)
    print("Last close:", f"{closes[-1]:.8f} USDT")
    print(f"EMA {FAST_EMA}:", round(ema(closes, FAST_EMA), 4))
    print(f"EMA {SLOW_EMA}:", round(ema(closes, SLOW_EMA), 4))
    print("Signal:", signal)
    print("Safety: public market data only, no API keys, no account access, no order placement.")


if __name__ == "__main__":
    main()
