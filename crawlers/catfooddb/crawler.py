from utils.http_client import HttpClient
from bs4 import BeautifulSoup
from furl import furl
from .parser import parse_brand_links
import json
from datetime import datetime, timezone


class CatFoodDb:
    def __init__(self):
        self.client = HttpClient()
        self.entryUrl = "https://catfooddb.com"

        # tree structure to crawl site
        self.visited = set()
        self.queue = []

        self.products = []
        self.brand_lookup = {}

    async def crawl(self):

        self.queue.append(self.entryUrl)

        while self.queue:
            url = self.queue.pop(0)
            if url in self.visited:
                continue

            await self.handle(url)
            self.visited.add(url)

        with open("data/catfooddb/productsRAW.jsonl", "w", encoding="utf-8") as f:
            for product in self.products:
                json.dump(product, f, ensure_ascii=False)
                f.write("\n")

    async def handle(self, url):
        f = furl(url)

        if url == self.entryUrl:
            await self.handle_main_page(url)

    async def handle_main_page(self, url):

        response = await self.client.get(url)

        html = await response.text()
        soup = BeautifulSoup(html, "html.parser")

        links = parse_brand_links(soup, url)
        [print(l) for l in links]

    async def handle_brand_page(self, url):
        pass

    async def handle_review_page(self, url):
        pass
