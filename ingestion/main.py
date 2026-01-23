import asyncio
import aiohttp
import psycopg2
import os
from fetch_exchange import fetch
from normalize import normalize
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

async def main():

    def get_last_timestamp(conn):
        with conn.cursor() as cur:
            cur.execute("""
                SELECT MAX(timestamp)
                FROM bronze.raw_ohlc
                WHERE symbol = %s
                  AND interval = %s
                  AND exchange = %s
            """, ("BTCUSDT", "1m", "binance"))
            row = cur.fetchone()
            return row[0]

    # get last timestamp
    last_ts = get_last_timestamp(conn)

    # compute start_time_ms
    if last_ts is None:
        start_time_ms = None
    else:
        start_time_ms = last_ts * 1000

    # 3build paramameter
    params = {
        "symbol": "BTCUSDT",
        "interval": "1m",
        "limit": 1000
    }

    if start_time_ms is not None:
        params["startTime"] = start_time_ms

    # fetch + normalize
    async with aiohttp.ClientSession() as session:
        raw = await fetch(session, params)
        candles = normalize(raw, "BTCUSDT", "1m")

    # 5️⃣ prepare rows
    rows = [
        (
            c["timestamp"],
            c["open"],
            c["high"],
            c["low"],
            c["close"],
            c["volume"],
            c["symbol"],
            c["interval"],
            c["exchange"],
        )
        for c in candles
    ]

    # insert to psql
    with conn.cursor() as cur:
        cur.executemany(
            """
            INSERT INTO bronze.raw_ohlc
            (timestamp, open, high, low, close, volume, symbol, interval, exchange)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (timestamp, symbol, interval, exchange) DO NOTHING
            """,
            rows
        )
        conn.commit()
    print(start_time_ms)

asyncio.run(main())
