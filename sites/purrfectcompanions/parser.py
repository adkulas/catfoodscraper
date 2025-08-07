from furl import furl


def parse_profile_links(soup, url):
    parsed = furl(url)
    return [
        parsed.copy().join(a["href"]).url
        for a in soup.select("a.summary-thumbnail-container")
        if a.get("href")
    ]


def parse_profile_page(soup):
    name = soup.select_one("h1.p-name").get_text(" ", strip=True)

    all_p_tags = soup.select("div.image-subtitle > p")
    appearance = {}
    appearance_text = ""
    for p in all_p_tags:
        if p.get_text(strip=True).startswith("Breed:"):
            appearance_text = p.get_text("|")
            break
    for item in appearance_text.split("|"):
        if not item.strip():
            continue
        kv_pair = list(filter(None, item.split(":")))
        if len(kv_pair) != 2:
            continue
        key = kv_pair[0].strip()
        value = kv_pair[1].strip()
        appearance[key] = value

    medical = {}
    medical_text = ""
    for p in all_p_tags:
        if p.get_text(strip=True).startswith("Spayed"):
            medical_text = p.get_text("|")
            break
    for item in medical_text.split("|"):
        if not item.strip():
            continue
        kv_pair = list(filter(None, item.split(":")))
        if len(kv_pair) != 2:
            continue
        key = kv_pair[0].strip()
        value = kv_pair[1].strip()
        medical[key] = value

    description = soup.select_one("div > h3 + p").get_text(" ", strip=True)

    return {
        "name": name,
        "appearance": appearance,
        "medical": medical,
        "description": description,
        "appearance_raw": appearance_text,
        "medical_raw": medical_text,
    }


def parse_category(url):
    f = furl(url)
    url_path = f.path.segments

    if "male-cats" in url_path:
        return "adult"
    elif "female-cats" in url_path:
        return "adult"
    elif "male-kittens" in url_path:
        return "kitten"
    elif "female-kittens" in url_path:
        return "kitten"
    else:
        return ""


def parse_image_url(soup):
    img_elem = soup.select_one("figure img")

    if not img_elem:
        return ""

    return img_elem["src"]
