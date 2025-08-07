from furl import furl

def parse_profile_links(soup, url):
    parsed = furl(url)
    return [
        parsed.copy().join(a["href"]).url
        for a in soup.select('a.summary-thumbnail-container')
        if a.get("href")
    ]

def parse_profile_page(soup):
    name = soup.select_one('h1.p-name').get_text(" ", strip=True)

    appearance = {}
    appearance_text = soup.select_one('div.image-subtitle > p').get_text("\n", strip=True)
    # lines = appearance_text.splitlines()
    # for line in lines:
    #     if ':' not in line:
    #         continue
    #     key, value = line.split(':', 1)
    #     appearance[key.strip()] = value.strip()

    medical = {}
    medical_text = soup.select('div.image-subtitle > p')[2].get_text()  
    # lines = medical_text.splitlines()
    # for line in lines:
    #     if ':' not in line:
    #         continue
    #     key, value = line.split(':', 1)
    #     medical[key.strip()] = value.strip()

    description = soup.select_one('div > h3 + p').get_text(" ", strip=True)

    return {
        'name': name,
        'appearance': appearance_text,
        'medical': medical_text,
        'description': description
    }

    