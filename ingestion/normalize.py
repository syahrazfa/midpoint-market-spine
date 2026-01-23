def normalize(candles, symbol, interval):
    return [
        {
            "timestamp": int(c[0] // 1000),
            "open": float(c[1]),
            "high": float(c[2]),
            "low": float(c[3]),
            "close": float(c[4]),
            "volume": float(c[5]),
            "symbol": symbol,
            "interval": interval,
            "exchange": "binance",
        }
        for c in candles
    ]
