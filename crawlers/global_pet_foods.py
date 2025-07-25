from utils.http_client import HttpClient
from bs4 import BeautifulSoup

class GlobalPetFoodsCrawler:
	def __init__(self):
		self.client = HttpClient()
		self.entryUrl = "https://brantford.globalpetfoods.com/products/list/?categories=00040003"

	async def crawl(self):

		await self.fetch_main_page()

	async def fetch_main_page(self):
		response = await self.client.get(self.entryUrl)
		print(response.status_code)

		html = await response.text()
		soup = BeautifulSoup(html, 'html.parser')
		links = soup.find_all('a', class_='cart-btn')

		for link in links:
			href = link.get('href')
			print(href)

		return html

spider = GlobalPetFoodsCrawler()