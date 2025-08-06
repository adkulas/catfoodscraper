# utils/http_client.py

from rnet import Client, Impersonate
import asyncio
import random


class HttpClient:
    def __init__(self, *, proxies=None, delay_range=(0.9, 2.0)):
        self.client = Client(impersonate=Impersonate.Firefox136, proxies=proxies)
        self.min_delay, self.max_delay = delay_range

    async def get(self, url: str, *, delay=True, **kwargs):
        if delay:
            await self._random_delay()
        print(f"[GET] {url}")
        return await self.client.get(url, **kwargs)

    async def post(self, url: str, *, delay=True, **kwargs):
        if delay:
            await self._random_delay()
        print(f"[POST] {url}")
        return await self.client.post(url, **kwargs)

    async def _random_delay(self):
        await asyncio.sleep(random.uniform(self.min_delay, self.max_delay))
