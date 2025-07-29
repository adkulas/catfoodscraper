from furl import furl

def parse_brand_links(soup, url):
	parsed = furl(url)
	links = {parsed.copy().join(a['href']).url for a in soup.select('a[href^="brand/"]') if a.get("href")}
	
	return list(sorted(links))