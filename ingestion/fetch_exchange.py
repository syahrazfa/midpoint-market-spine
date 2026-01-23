import aiohttp

URL = "https://data-api.binance.vision/api/v3/klines"

async def fetch(session, params):
    async with session.get(URL, params=params) as r:
        r.raise_for_status()
        return await r.json()
