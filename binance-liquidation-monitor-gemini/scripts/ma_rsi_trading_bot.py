"""
Simple Binance trading bot that uses moving average (MA) and relative strength index (RSI)
indicators to decide whether to buy or sell.  The bot fetches recent market data from the
Binance REST API via `ccxt`, calculates the indicators, and executes a market order
according to basic rules:

- If the price is above the moving average and RSI is below the oversold threshold -> **buy**
- If the price is below the moving average and RSI is above the overbought threshold -> **sell**
- Otherwise -> **hold**

API keys are read from the environment variables `BINANCE_API_KEY` and `BINANCE_API_SECRET`.

This script is intentionally minimal and only intended for educational purposes.  Do not
risk real funds without fully understanding the code and the market.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List

try:
    import ccxt  # type: ignore
except Exception as exc:  # pragma: no cover - only used during runtime
    raise SystemExit("ccxt is required: pip install ccxt") from exc


@dataclass
class IndicatorConfig:
    """Configuration for the MA and RSI indicators."""

    ma_period: int = 20
    rsi_period: int = 14
    overbought: float = 70.0
    oversold: float = 30.0


def fetch_close_prices(
    exchange: "ccxt.binance",
    symbol: str,
    timeframe: str = "1m",
    limit: int = 100,
) -> List[float]:
    """Fetch close prices from Binance using ccxt."""

    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    return [candle[4] for candle in ohlcv]


def moving_average(prices: List[float], period: int) -> float:
    """Return simple moving average for the last ``period`` prices."""

    if len(prices) < period:
        raise ValueError("not enough data for moving average")
    return sum(prices[-period:]) / float(period)


def rsi(prices: List[float], period: int) -> float:
    """Compute Relative Strength Index (RSI)."""

    if len(prices) < period + 1:
        raise ValueError("not enough data for RSI")

    gains: List[float] = []
    losses: List[float] = []

    for i in range(-period, 0):
        change = prices[i] - prices[i - 1]
        if change >= 0:
            gains.append(change)
            losses.append(0.0)
        else:
            gains.append(0.0)
            losses.append(abs(change))

    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period
    if avg_loss == 0:
        return 100.0

    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def decide_action(prices: List[float], cfg: IndicatorConfig) -> str:
    """Return 'buy', 'sell', or 'hold' based on MA and RSI."""

    ma_value = moving_average(prices, cfg.ma_period)
    rsi_value = rsi(prices, cfg.rsi_period)
    last_price = prices[-1]

    if last_price > ma_value and rsi_value < cfg.oversold:
        return "buy"
    if last_price < ma_value and rsi_value > cfg.overbought:
        return "sell"
    return "hold"


def execute_order(exchange: "ccxt.binance", symbol: str, side: str, amount: float) -> None:
    """Execute a market order.  This function assumes ``amount`` is valid for the symbol."""

    exchange.create_market_order(symbol, side, amount)


def run(symbol: str = "BTC/USDT", amount: float = 0.001) -> str:
    """Fetch data, decide action, and optionally execute an order."""

    key = os.environ.get("BINANCE_API_KEY")
    secret = os.environ.get("BINANCE_API_SECRET")
    if not key or not secret:
        raise SystemExit("BINANCE_API_KEY and BINANCE_API_SECRET environment variables are required")

    exchange = ccxt.binance({"apiKey": key, "secret": secret})
    prices = fetch_close_prices(exchange, symbol)
    action = decide_action(prices, IndicatorConfig())

    if action in {"buy", "sell"}:
        execute_order(exchange, symbol, action, amount)
    return action


if __name__ == "__main__":  # pragma: no cover - manual invocation only
    result = run()
    print(f"Action: {result}")
