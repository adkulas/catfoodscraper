from utils.http_client import HttpClient
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, parse_qs
from .parser import parse_brands, parse_brand_product_links, parse_product, parse_alt_size_for_product
import json

class GlobalPetFoodsCrawler:
	def __init__(self):
		self.client = HttpClient()
		self.entryUrl = "https://brantford.globalpetfoods.com/products/list/?categories=00040003"
		
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


		print(json.dumps(self.products, indent=2))


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

		html = await response.text()
		soup = BeautifulSoup(html, 'html.parser')

		links = parse_brands(soup)
		for query, brand_name in links:
			brand_filtered_products_link = urljoin(url, query)
			self.queue.append(brand_filtered_products_link)
			
			query_params = parse_qs(query.lstrip('?'))
			brand_list = query_params.get('brand')
			brand_id = brand_list[0] if brand_list else None
			
			self.brand_lookup[brand_filtered_products_link] = {
				'brand_id': brand_id,
				'brand_name': brand_name,
			}


	async def handle_brand_products(self, url):

		response = await self.client.get(url)

		html = await response.text()
		soup = BeautifulSoup(html, 'html.parser')

		links = parse_brand_product_links(soup)
		links = links[:1]
		for link in links:
			parsed = urlparse(url)
			base = f"{parsed.scheme}://{parsed.netloc}"
			full_url = urljoin(base, link)

			self.queue.append(full_url)
			self.brand_lookup[full_url] = self.brand_lookup[url]

	async def handle_product_page(self, url):

		response = await self.client.get(url)

		html = await response.text()
		soup = BeautifulSoup(html, 'html.parser')

		brand_name = self.brand_lookup[url]['brand_name']
		product = parse_product(soup)

		product['url'] = url
		product['brand'] = brand_name

		self.products.append(product)

		links_to_variations = parse_alt_size_for_product(soup, url)
		self.queue[:0] = links_to_variations

		for link in links_to_variations:
			self.brand_lookup[link] = self.brand_lookup[url]

spider = GlobalPetFoodsCrawler()
