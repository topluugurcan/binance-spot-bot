# Binance Spot — signal-only starter bot
# SAFE MODE: public market data only. No API keys. No orders are submitted.

import os
from datetime import datetime, timezone

import requests

BASE_URL = "https://data-api.binance.vision"
SYMBOL = os.getenv("SYMBOL", "BTCUSDT")
INTERVAL = os.getenv("INTERVAL", "5m")
FAST_EMA = 9
SLOW_EMA = 21


def get_closed_candles():
    response = requests.get(
        f"{BASE_URL}/api/v3/klines",
        params={"symbol": SYMBOL, "interval": INTERVAL, "limit": 100},
        timeout=20,
    )
    response.raise_for_status()
    candles = response.json()

    if not isinstance(candles, list) or len(candles) < SLOW_EMA + 3:
        raise RuntimeError("Not enough candle data returned by Binance.")

    # Binance's last kline may still be forming. Exclude it.
    return candles[:-1]


def ema(values, period):
    alpha = 2 / (period + 1)
    current = values[0]
    for value in values[1:]:
        current = alpha * value + (1 - alpha) * current
    return current


def main():
    candles = get_closed_candles()
    closes = [float(candle[4]) for candle in candles]

    fast_prev = ema(closes[:-1], FAST_EMA)
    slow_prev = ema(closes[:-1], SLOW_EMA)
    fast_now = ema(closes, FAST_EMA)
    slow_now = ema(closes, SLOW_EMA)

    if fast_prev <= slow_prev and fast_now > slow_now:
        signal = "BUY SIGNAL"
    elif fast_prev >= slow_prev and fast_now < slow_now:
        signal = "SELL SIGNAL"
    else:
        signal = "WAIT"

    print("=== BINANCE SPOT SIGNAL BOT ===")
    print("UTC:", datetime.now(timezone.utc).isoformat())
    print("Symbol:", SYMBOL)
    print("Interval:", INTERVAL)
    print("Last closed candle close:", f"{closes[-1]:.8f} USDT")
    print(f"EMA {FAST_EMA}:", round(fast_now, 4))
    print(f"EMA {SLOW_EMA}:", round(slow_now, 4))
    print("Signal:", signal)
    print("MODE: SIGNAL ONLY — NO REAL ORDERS")
    print("Note: This simple indicator is not a guarantee of profit.")


if __name__ == "__main__":
    main()
