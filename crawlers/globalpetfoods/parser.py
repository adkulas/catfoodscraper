from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, parse_qs, urlunparse

def parse_brands(soup):
	return [a for a in soup.find_all("a", class_="data-loader") if a.get("href")]

def parse_brand_product_links(soup):
	return [a["href"] for a in soup.find_all("a", class_="cart-btn") if a.get("href")]

def parse_product(soup):
	title = soup.select_one('h1[tabindex="0"]').get_text(" ", strip=True)
	category = soup.select_one('h3.categor-title').get_text(" ", strip=True)
	price = float(soup.select_one('span.current-price').get_text(strip=True).replace('$',''))
	size_text = soup.select_one('div.size-box h3.option-label').get_text(strip=True)
	description = soup.select_one('div#description p').get_text(strip=True)
	description_table = {}
	description_rows = soup.select('div#description div.table-info div.row')
	for description_row in description_rows:
		divs = description_row.find_all('div', recursive=False)
		if len(divs) >= 2:
			label = divs[0].get_text(" ", strip=True)
			value = divs[1].get_text(" ", strip=True)
			description_table[label] = value
	ingredients = soup.select_one('div#nutritional-info p').get_text(strip=True)
	nutritional_table = {}
	nutritional_rows = soup.select('div#nutritional-info div.table-info div.row')
	for nutritional_row in nutritional_rows:
		divs = nutritional_row.find_all('div', recursive=False)
		if len(divs) >= 2:
			label = divs[0].get_text(" ", strip=True)
			value = divs[1].get_text(" ", strip=True)
			nutritional_table[label] = value

	return {
		'title': title,
		'category': category,
		'price': price,
		'size': size_text,
		'description': description,
		'additionalDescription': description_table,
		'ingredients': ingredients,
		'nutritionaltable': nutritional_table
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

def parse_brand_from_url(url):
	parsed = urlparse(url)
	query_params = parse_qs(parsed.query)
	brand_list = query_params.get('brand')
	brand_id = brand_list[0] if brand_list else None
	return brand_id

