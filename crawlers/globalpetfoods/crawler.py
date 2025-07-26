from utils.http_client import HttpClient
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, parse_qs
from .parser import parse_brands, parse_brand_product_links, parse_product, parse_brand_from_url
import json

class GlobalPetFoodsCrawler:
	def __init__(self):
		self.client = HttpClient()
		self.entryUrl = "https://brantford.globalpetfoods.com/products/list/?categories=00040003"
		
		# tree structure to crawl site
		self.visited = set()
		self.queue = []
		self.parent = {}

		self.data = {}

	async def crawl(self):

		self.queue.append(self.entryUrl)
		self.parent[self.entryUrl] = None

		while self.queue:
			url = self.queue.pop(0)
			if url in self.visited:
				continue

			await self.handle(url)
			self.visited.add(url)


	async def handle(self, url):
		parsed = urlparse(url)
		query_params = parse_qs(parsed.query)

		if 'brand' in query_params:
			await self.handle_brand_products(url)
		elif 'list' not in parsed.path.lower() and 'products' in parsed.path.lower():
			await self.handle_product_page(url)
		else:
			await self.handle_main_page(url)

	async def handle_main_page(self, url):
		response = await self.client.get(url)
		print(response.status_code)

		html = await response.text()
		soup = BeautifulSoup(html, 'html.parser')

		links = parse_brands(soup)
		for link in links:
			query = link.get('href')
			brand_filter_link = urljoin(url, query)
			self.queue.append(brand_filter_link)
			self.parent[brand_filter_link] = url
			
			brand_name = link.text.strip()
			query_params = parse_qs(query.lstrip('?'))
			brand_list = query_params.get('brand')
			brand_id = brand_list[0] if brand_list else None

			self.data[brand_id] = {
				'brand': brand_name,
				'products': {}
			}

	
	async def handle_brand_products(self, url):

		response = await self.client.get(url)
		print(response.status_code)

		html = await response.text()
		soup = BeautifulSoup(html, 'html.parser')

		links = soup.find_all('a', class_='cart-btn')
		for link in links:
			href = link.get('href')
			parsed = urlparse(url)
			base = f"{parsed.scheme}://{parsed.netloc}"
			full_url = urljoin(base, href)

			self.queue.append(full_url)
			self.parent[full_url] = url


	async def handle_product_page(self, url):
		response = await self.client.get(url)
		print(response.status_code)
		html = await response.text()
		soup = BeautifulSoup(html, 'html.parser')
		data = parse_product(soup)

		parent = self.parent[url]

		brand_name = self.data[parse_brand_from_url(parent)]['brand']
		print(brand_name)
		print(json.dumps(data, indent=2))

spider = GlobalPetFoodsCrawler()
