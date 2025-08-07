from sys import stderr
from utils.http_client import HttpClient
from bs4 import BeautifulSoup
from furl import furl
from .parser import parse_profile_links, parse_profile_page
import json
from datetime import datetime, timezone


class PurrfectCompanions:
    def __init__(self):
        self.client = HttpClient()
        self.entryUrl = "https://www.purrfectcompanions.ca/adopt"

        # tree structure to crawl site
        self.visited = set()
        self.stack = []

        self.profiles = []

    async def crawl(self):

        self.stack.append(self.entryUrl)

        while self.stack:
            url = self.stack.pop()
            if url in self.visited:
                continue

            await self.handle(url)
            self.visited.add(url)

        with open("data/purrfect-companions/profiles.jsonl", "w", encoding="utf-8") as f:
            for profile in self.profiles:
                json.dump(profile, f, ensure_ascii=False)
                f.write("\n")


    async def handle(self, url):
        f = furl(url)

        if url == self.entryUrl:
            await self.handle_main_page(url)
        else:
            await self.handle_profile_page(url)


    async def handle_main_page(self, url):

        response = await self.client.get(url)

        html = await response.text()
        soup = BeautifulSoup(html, "html.parser")
        links = parse_profile_links(soup, url)

        for link in links:
            print(link)
        self.stack += links


    async def handle_profile_page(self, url):

        response = await self.client.get(url)

        html = await response.text()
        soup = BeautifulSoup(html, "html.parser")

        profile = parse_profile_page(soup)
        print(json.dumps(profile, indent=2))
        self.profiles.append(profile)
