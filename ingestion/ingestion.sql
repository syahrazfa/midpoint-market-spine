DROP TABLE IF EXISTS bronze.raw_ohlc;

CREATE TABLE IF NOT EXISTS bronze.raw_ohlc(
	timestamp BIGINT NOT NULL,
    open DOUBLE PRECISION NOT NULL,
    high DOUBLE PRECISION NOT NULL,
    low DOUBLE PRECISION NOT NULL,
    close DOUBLE PRECISION NOT NULL,
    volume DOUBLE PRECISION NOT NULL,
    symbol TEXT NOT NULL,
    interval TEXT NOT NULL,
    exchange TEXT NOT NULL,
    PRIMARY KEY (timestamp, symbol, interval, exchange)
);

SELECT * FROM bronze.raw_ohlc;

SELECT MAX(timestamp)
                FROM bronze.raw_ohlc
                WHERE symbol = 'BTCUSDT'
                  AND interval = '1m'
                  AND exchange = 'binance'
