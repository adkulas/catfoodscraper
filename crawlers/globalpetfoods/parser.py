from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urlunparse

def parse_brands(soup):
	return [(a["href"], a.get_text(strip=True)) for a in soup.find_all("a", class_="data-loader") if a.get("href")]

def parse_brand_product_links(soup):
	return [a["href"] for a in soup.find_all("a", class_="cart-btn") if a.get("href")]

def parse_product(soup):
	def safe_text(selector, default="", **kwargs):
		elem = soup.select_one(selector)
		return elem.get_text(**kwargs) if elem else default

	def parse_table_rows(rows):
		table = {}
		for row in rows:
			divs = row.find_all('div', recursive=False)
			if len(divs) >= 2:
				label = divs[0].get_text(" ", strip=True)
				value = divs[1].get_text(" ", strip=True)
				table[label] = value
		return table

	title = safe_text('h1[tabindex="0"]', default="", strip=True, separator=" ")
	category = safe_text('h3.categor-title', default="", strip=True, separator=" ")
	price = safe_text('span.current-price', default="", strip=True)
	size_text = safe_text('div.size-box h3.option-label', default="", strip=True)
	description = safe_text('div#description p', default="", strip=True)

	description_rows = soup.select('div#description div.table-info div.row') or []
	description_table = parse_table_rows(description_rows)

	ingredients = safe_text('div#nutritional-info p', default="", strip=True)

	nutritional_rows = soup.select('div#nutritional-info div.table-info div.row') or []
	nutritional_table = parse_table_rows(nutritional_rows)

	return {
		"title": title,
		"category": category,
		"price": price,
		"size": size_text,
		"description": description,
		"description_table": description_table,
		"ingredients": ingredients,
		"nutritional_table": nutritional_table,
	}

def parse_alt_size_for_product(soup, url):
	paths = [a['href'] for a in soup.select('div.size-box a.data-loader') if a.get("href")]
	parsed = urlparse(url)
	base = f"{parsed.scheme}://{parsed.netloc}"
	query = parsed.query
	
	hrefs = []
	for path in paths:
		fixed_path = path.replace('/products/', '/products/brantford/')
		full_url = urljoin(base, fixed_path)
		parsed_full = urlparse(full_url)
		# Reconstruct with query from original URL
		rebuilt = parsed_full._replace(query=query)
		hrefs.append(urlunparse(rebuilt))

	return hrefs

def parse_next_page(soup, url):
	next_page = soup.find('a', string='Next')
	parsed = urlparse(url)
	base = f"{parsed.scheme}://{parsed.netloc}"
	next_page_href = urljoin(base, next_page['href']) if next_page else None
	return next_page_href

