from furl import furl


def parse_brand_links(soup, url):
    parsed = furl(url)
    links = {
        parsed.copy().join(a["href"]).url
        for a in soup.select('a[href^="brand/"]')
        if a.get("href")
    }

    return list(sorted(links))


def parse_review_links(soup, url):
    base = furl(url).origin
    buttons = soup.find_all("button", class_="btn-review")
    links = []
    for button in buttons:
        a = button.find_parent("a")
        if a and a.get("href"):
            link = furl(base).join(a["href"]).url
            links.append(link)

    return links


def parse_brand(soup):
    bold_tag = soup.select_one("div.panel-heading > h2 > b")
    if bold_tag:
        return bold_tag.get_text(" ", strip=True)
    return None
